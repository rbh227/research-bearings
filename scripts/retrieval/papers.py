#!/usr/bin/env python3
"""Reading-side retrieval: the verbs that turn a paper into something an agent
can read, and the ledger lookups built on the same transport.

`snowball.py` is the search side: four resolvers, seven probes, one unified
record. This is the second script beside it, and it imports that transport
rather than copying it — the cache, the pacing, the retry, the record shape and
the resolvers are all one implementation. The guard's Bash fence admits any
script in this directory, so agents can call this one without a guard change.

Verbs:

  fetch      one paper's text, split so the predictor cannot read past the intro
  reviews    OpenReview's record for a paper: ratings, objections, responses
  datasets   one dataset on the Hugging Face hub and on GitHub
  authors    one author's last N years, for the groups ledger

Every verb prints one JSON object and exits 0. A missing key, an absent record
and a source that would not answer are states inside that object, named with
what was checked. The only thing that is an error is a malformed answer or an
exhausted retry, and those come back as a result too.

Run: python3 papers.py <verb> [args]   |   python3 papers.py --selftest
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import http.client
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snowball import (  # noqa: E402
    ARXIV_ID,
    BACKOFF_BASE,
    RETRYABLE,
    S2_FIELDS,
    TIMEOUT,
    TTL,
    _env,
    cache_dir,
    cache_path,
    err,
    fetch as http_get,
    fetch_json,
    finish,
    http_fetch,
    merge_records,
    norm_arxiv,
    norm_doi,
    normalised_title,
    oa_search,
    oa_work,
    s2_get,
    s2_search,
    title_match,
    today,
    user_agent,
    write_atomic,
)

VERSION = "0.1.0"

OPENREVIEW_BASE = "https://api2.openreview.net"
OPENREVIEW_V1 = "https://api.openreview.net"
HF_BASE = "https://huggingface.co/api"
AUTHOR_PAGES = 5  # 500 papers; past that, say the list is partial rather than pretend
OA_AUTHORS = "https://api.openalex.org/authors"
OA_WORKS = "https://api.openalex.org/works"
GITHUB_BASE = "https://api.github.com"
UNPAYWALL_BASE = "https://api.unpaywall.org/v2"

# Where the intro ends. The first top-level section heading after it, in the
# spellings papers actually use, numbered or not. Matched on a line of its own.
SECTION_AFTER_INTRO = re.compile(
    r"^\s*(?:(?:[IVX]+|\d+)[.)]?\s*)?"
    r"(related\s+work|related\s+works|background|preliminaries|prior\s+work|"
    r"literature\s+review|methods?|methodology|approach|our\s+approach|"
    r"proposed\s+(?:method|approach|model)|the\s+model|problem\s+(?:statement|formulation)|"
    r"materials\s+and\s+methods)\s*$",
    re.I,
)

# The intro has to start somewhere too: anything before it is the title block.
INTRO_HEADING = re.compile(
    r"^\s*(?:(?:[IVX]+|\d+)[.)]?\s*)?(introduction)\s*$", re.I
)

# IEEE and ACM set section headings in small caps, and pdftotext renders that
# as "II. R ELATED W ORK" — a capital, a space, then the rest in capitals.
# Measured 2026-09-16 on the BDANet paper: without this, every IEEE-styled
# paper silently falls back to a page cut.
SMALL_CAPS = re.compile(r"\b([A-Z]) ([A-Z]{2,})\b")


def heading_form(line: str) -> str:
    """One line as a heading matcher should see it."""
    return SMALL_CAPS.sub(r"\1\2", line)

# How far into the text a heading may sit and still be believed as the end of
# the introduction. Past this it is a section of the body, not the intro's end.
# Measured on the fixture: a real paper's "2. Related Work" lands near 28 per
# cent of the extracted text, because the references and the running headers
# extract too. The ceiling is the second half of the rule: 40 per cent of a
# 200,000-character extraction is not an introduction, whatever the fraction says.
SPLIT_WINDOW = 0.40
SPLIT_CEILING = 30000

# The fallback when no heading is found: two pages of the extracted text.
PAGE_BREAK = "\f"
FALLBACK_PAGES = 2
FALLBACK_CHARS = 9000  # a page of a two-column paper, twice, when there are no form feeds

PDF_HINT = ("install poppler for pdftotext (brew install poppler / apt install poppler-utils), "
            "or pip install pypdf")


# --------------------------------------------------------------------------
# resolving one paper


def _looks_like_doi(value: str) -> bool:
    return bool(re.match(r"^(https?://(dx\.)?doi\.org/|doi:)?10\.\d{4,9}/", value.strip(), re.I))


def _looks_like_openalex(value: str) -> bool:
    return bool(re.match(r"^(https?://openalex\.org/)?W\d+$", value.strip(), re.I))


def _looks_like_s2(value: str) -> bool:
    v = value.strip()
    return bool(re.fullmatch(r"[0-9a-f]{40}", v)) or v.lower().startswith("corpusid:")


def _looks_like_arxiv(value: str) -> bool:
    v = value.strip()
    if v.lower().startswith("arxiv:"):
        return True
    return bool(ARXIV_ID.fullmatch(v))


def identify(value: str) -> tuple[str, str]:
    """What kind of thing the caller handed us. Order matters: a DOI contains
    digits and dots and would otherwise look like an arXiv id."""
    v = (value or "").strip()
    if not v:
        return "none", ""
    if _looks_like_doi(v):
        return "doi", norm_doi(v) or v
    if _looks_like_openalex(v):
        return "openalex", v.rsplit("/", 1)[-1].upper()
    if _looks_like_arxiv(v):
        return "arxiv", norm_arxiv(v) or v
    if _looks_like_s2(v):
        return "s2", v
    return "title", v


def stamp(record: dict[str, Any], kind: str, ident: str) -> dict[str, Any]:
    """Put the id the caller gave back on the record. An index that answers a
    lookup by arXiv id and then omits that id from `externalIds` is common, and
    the omission would cost us the one PDF location we are sure of."""
    key = {"doi": "DOI", "arxiv": "ArXiv", "openalex": "OpenAlex"}.get(kind)
    if key and record is not None:
        ext = dict(record.get("externalIds") or {})
        ext.setdefault(key, ident)
        record = {**record, "externalIds": ext}
    return record


def resolve(value: str) -> dict[str, Any]:
    """One paper's unified record, from whichever index knows the id. A title
    resolves only on an exact match, the chunk 3 rule, so `fetch` on a
    half-remembered title reports a candidate instead of downloading the
    wrong paper."""
    kind, ident = identify(value)
    if kind == "none":
        return err("fetch needs an id or a title")

    checked: list[str] = []
    errors: dict[str, str] = {}

    if kind in ("doi", "arxiv", "s2"):
        lookup = {"doi": f"DOI:{ident}", "arxiv": f"arXiv:{ident}", "s2": ident}[kind]
        # Without `fields` the single-paper endpoint answers with an id and a
        # title and nothing else, which looks like a paper with no PDF anywhere.
        got = s2_get(f"/paper/{urllib.parse.quote(lookup, safe=':')}",
                     params={"fields": S2_FIELDS})
        checked.append("s2")
        if isinstance(got, dict) and "error" not in got and got.get("paperId"):
            from snowball import s2_record
            return {"record": stamp(finish(s2_record(got)), kind, ident),
                    "checked": checked, "errors": errors, "matched": kind}
        if isinstance(got, dict) and "error" in got:
            errors["s2"] = got["error"]

    if kind in ("doi", "openalex"):
        got = oa_work(ident)
        checked.append("openalex")
        if isinstance(got, dict) and "error" not in got and got.get("papers"):
            return {"record": stamp(got["papers"][0], kind, ident),
                    "checked": checked, "errors": errors, "matched": kind}
        if isinstance(got, dict) and "error" in got:
            errors["openalex"] = got["error"]

    if kind == "arxiv":
        from snowball import arxiv_search
        got = arxiv_search(query=f"id:{ident}", limit=1)
        checked.append("arxiv")
        if isinstance(got, dict) and "error" not in got and got.get("papers"):
            return {"record": stamp(got["papers"][0], kind, ident),
                    "checked": checked, "errors": errors, "matched": kind}

    if kind == "title":
        for source, search in (("s2", s2_search), ("openalex", oa_search)):
            got = search(value, 10)
            if "error" in got:
                errors[source] = got["error"]
                continue
            checked.append(source)
            for paper in got.get("papers") or []:
                if title_match(value, paper.get("title") or "") == "exact":
                    return {"record": paper, "checked": checked, "errors": errors,
                            "matched": "title"}
        return {"record": None, "checked": checked, "errors": errors, "matched": None,
                "state": "not resolved",
                "note": "no exact title match; only an exact match resolves. "
                        "Pass an id, or run snowball.py verify to see the candidate."}

    return {"record": None, "checked": checked, "errors": errors, "matched": None,
            "state": "not resolved"}


# --------------------------------------------------------------------------
# where the text might be


def pdf_locations(record: dict[str, Any]) -> list[dict[str, str]]:
    """Every open-access location the indexes gave us, in the order worth
    trying: what S2 and OpenAlex already handed back, then arXiv's own PDF,
    then Unpaywall if an email is set. Unpaywall is last because it is a
    second network call for a location the first two usually already have."""
    out: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(url: str | None, source: str) -> None:
        if url and url not in seen:
            seen.add(url)
            out.append({"url": url, "source": source})

    add(record.get("pdfUrl"), "index")
    ext = record.get("externalIds") or {}
    arxiv = ext.get("ArXiv")
    if arxiv:
        add(f"https://arxiv.org/pdf/{arxiv}", "arxiv")
    doi = norm_doi(ext.get("DOI"))
    email = _env("UNPAYWALL_EMAIL")
    if doi and email:
        got = fetch_json("unpaywall", "GET", f"{UNPAYWALL_BASE}/{urllib.parse.quote(doi)}",
                         params={"email": email})
        if isinstance(got, dict) and "error" not in got:
            best = got.get("best_oa_location") or {}
            add(best.get("url_for_pdf"), "unpaywall")
            for loc in got.get("oa_locations") or []:
                add(loc.get("url_for_pdf"), "unpaywall")
    return out


# --------------------------------------------------------------------------
# PDF to text


def extractor() -> tuple[str, str]:
    """(name, detail). `pdftotext` first: it keeps the reading order of a
    two-column paper, which pypdf does not. Neither present is a state."""
    path = shutil.which("pdftotext")
    if path:
        return "pdftotext", path
    try:
        import pypdf  # noqa: F401
        return "pypdf", getattr(pypdf, "__version__", "")
    except ImportError:
        return "", ""


def extract_text(pdf_path: str) -> tuple[str, str | None]:
    """(text, problem). Never raises: a PDF that will not parse is a state."""
    name, _ = extractor()
    if name == "pdftotext":
        try:
            # Reading order, not page layout. Measured 2026-09-16 on the xBD
            # paper: `-layout` puts both columns of a two-column paper on one
            # line, so "2. Related Work" ends up followed by the next column's
            # prose and no heading ever ends its line. That silently turns
            # every two-column paper into a page cut, which is the weaker
            # fence. Tables read worse without it; the split matters more.
            done = subprocess.run(  # noqa: S603 - fixed binary, no shell
                ["pdftotext", pdf_path, "-"],
                capture_output=True, timeout=120, check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return "", f"pdftotext failed: {exc}"
        if done.returncode != 0:
            return "", f"pdftotext exited {done.returncode}: {done.stderr.decode('utf-8', 'replace')[:200]}"
        return done.stdout.decode("utf-8", "replace"), None
    if name == "pypdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            pages = [(page.extract_text() or "") for page in reader.pages]
            return PAGE_BREAK.join(pages), None
        except Exception as exc:  # noqa: BLE001 - any parse failure is a state
            return "", f"pypdf failed: {type(exc).__name__}: {exc}"
    return "", "no extractor"


# --------------------------------------------------------------------------
# the split


def split_text(text: str) -> dict[str, Any]:
    """Title, abstract and introduction, and everything. The predictor is
    handed the first of these and nothing else, so where this cuts is the
    whole fence: a heading match is the good case, a page cut the fallback,
    and which one happened is recorded on the metadata record.

    Cutting early costs the predictor context. Cutting late shows it the
    method, which is the thing the protocol exists to hide — so the window
    stops a "Methods" heading two thirds down a paper from being believed."""
    if not text.strip():
        return {"intro": "", "split": "empty", "cut_at": 0, "heading": None}

    limit = max(min(int(len(text) * SPLIT_WINDOW), SPLIT_CEILING), 1)

    # Line by line, because a heading is a whole line and the small-caps
    # normalisation is per line.
    intro_at = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        if offset > limit:
            break
        form = heading_form(line)
        if not intro_at and INTRO_HEADING.match(form):
            intro_at = offset
        elif offset > intro_at and SECTION_AFTER_INTRO.match(form):
            return {"intro": text[:offset].rstrip(), "split": "heading",
                    "cut_at": offset, "heading": " ".join(line.split())}
        offset += len(line)

    pages = text.split(PAGE_BREAK)
    if len(pages) > FALLBACK_PAGES:
        cut = len(PAGE_BREAK.join(pages[:FALLBACK_PAGES]))
        return {"intro": text[:cut].rstrip(), "split": "page-cut", "cut_at": cut, "heading": None}
    # No form feeds and no heading: half, never the whole thing. A text this
    # shape is a bad extraction, and handing the predictor all of it is the one
    # outcome the protocol cannot survive.
    cut = min(FALLBACK_CHARS, max(len(text) // 2, 1))
    return {"intro": text[:cut].rstrip(), "split": "page-cut", "cut_at": cut, "heading": None}


# --------------------------------------------------------------------------
# fetch


def fetch_dir(record: dict[str, Any]) -> str:
    """One directory per paper under the fetch cache, named by the most stable
    id it has."""
    ext = record.get("externalIds") or {}
    ident = (ext.get("ArXiv") and f"arxiv-{ext['ArXiv']}") or \
            (ext.get("DOI") and "doi-" + re.sub(r"[^A-Za-z0-9.]+", "-", str(ext["DOI"]))) or \
            (record.get("paperId") and f"s2-{record['paperId']}") or \
            ("title-" + re.sub(r"[^a-z0-9]+", "-", normalised_title(record.get("title") or ""))[:80])
    return os.path.join(cache_dir(), "fetch", ident)


def _fresh(path: str) -> bool:
    import time
    try:
        return (time.time() - os.path.getmtime(path)) <= TTL
    except OSError:
        return False


def _read_body(url: str) -> tuple[int, bytes, str | None]:
    """One GET, read in 256 KiB chunks, keeping whatever arrives.

    Measured 2026-09-16 on arXiv 2004.07312 (RescueNet, 4,973,168 bytes): a
    single `response.read()` raises IncompleteRead at exactly 4,194,304 bytes,
    every time, on every attempt — and the same response read in chunks
    delivers all 4,973,168. So the failure was the read-all, not the server,
    and retrying it could never have worked.

    The partial is still kept when IncompleteRead does happen, because half a
    PDF still holds the pages that arrived. That is the opposite of the right
    behaviour for JSON, which is why the shared transport discards it and this
    path does not.
    """
    request = urllib.request.Request(
        url, method="GET",
        headers={"User-Agent": user_agent(), "Accept": "application/pdf"})
    got = bytearray()
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            while True:
                try:
                    chunk = response.read(262144)
                except http.client.IncompleteRead as exc:
                    got.extend(exc.partial or b"")
                    return response.status, bytes(got), f"truncated at {len(got)} bytes"
                if not chunk:
                    break
                got.extend(chunk)
            return response.status, bytes(got), None
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, exc.read(), None
        except Exception:  # noqa: BLE001
            return exc.code, b"", None
    except http.client.IncompleteRead as exc:
        got.extend(exc.partial or b"")
        return 200, bytes(got), f"truncated at {len(got)} bytes"
    except urllib.error.URLError as exc:
        return 0, str(exc.reason).encode("utf-8"), None
    except Exception as exc:  # noqa: BLE001
        return 0, f"{type(exc).__name__}: {exc}".encode(), None


def download(url: str, attempts: int = 2) -> tuple[bytes, str | None]:
    """A PDF is bytes, not JSON, so this goes round `fetch_json` to the one
    attempt underneath and keeps the retry shape by hand. Measured 2026-09-16:
    an arXiv PDF that curl pulls in two seconds timed out once at sixty, so a
    single slow moment must not cost us the only location we have."""
    problem = ""
    for attempt in range(max(attempts, 1)):
        status, raw, truncated = _read_body(url)
        if status == 200 and raw.startswith(b"%PDF"):
            # A truncated PDF is offered to the extractor anyway: the pages
            # that arrived are the pages that arrived, and the caller is told.
            return raw, truncated
        if status == 200:
            head = raw[:200].decode("utf-8", "replace")
            return b"", f"not a PDF (starts {head[:60]!r})"  # a login page will not improve on a retry
        problem = f"HTTP {status}: {raw.decode('utf-8', 'replace')[:120]}"
        if status not in RETRYABLE:
            return b"", problem
        if attempt < attempts - 1:
            time.sleep(BACKOFF_BASE * 2 ** attempt)
    return b"", problem


def fetch_paper(value: str, refresh: bool = False) -> dict[str, Any]:
    """The verb. Resolve, find a PDF, download, extract, split, write three
    files, report every state on the way."""
    resolved = resolve(value)
    if "error" in resolved:
        return resolved
    record = resolved.get("record")
    if not record:
        return {"asked": value, "state": "not resolved", "checked": resolved.get("checked", []),
                "errors": resolved.get("errors", {}), "note": resolved.get("note"),
                "paths": None, "date": today()}

    directory = fetch_dir(record)
    paths = {"intro": os.path.join(directory, "intro.txt"),
             "full": os.path.join(directory, "full.txt"),
             "meta": os.path.join(directory, "meta.json")}

    if not refresh and all(os.path.exists(p) for p in paths.values()) and _fresh(paths["meta"]):
        try:
            with open(paths["meta"], encoding="utf-8") as fh:
                meta = json.load(fh)
            meta["cached"] = True
            return meta
        except (OSError, ValueError):
            pass  # a damaged cache entry is refetched, never returned

    name, detail = extractor()
    if not name:
        return {"asked": value, "title": record.get("title"), "state": "no extractor",
                "extractor": None, "hint": PDF_HINT, "locations": len(pdf_locations(record)),
                "paths": None, "date": today()}

    locations = pdf_locations(record)
    if not locations:
        return {"asked": value, "title": record.get("title"), "state": "no text",
                "checked": ["index pdf", "arxiv", "unpaywall" if _env("UNPAYWALL_EMAIL") else "unpaywall (no email)"],
                "paths": None, "date": today()}

    tried: list[dict[str, str]] = []
    text = ""
    used: dict[str, str] | None = None
    truncated: str | None = None
    for loc in locations:
        raw, problem = download(loc["url"])
        if problem and not raw:
            tried.append({**loc, "problem": problem})
            continue
        if problem:
            truncated = problem  # kept, extracted, and named on the record
        handle, tmp = tempfile.mkstemp(suffix=".pdf")
        try:
            with os.fdopen(handle, "wb") as fh:
                fh.write(raw)
            text, problem = extract_text(tmp)
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)
        if problem or not text.strip():
            tried.append({**loc, "problem": problem or "extractor returned no text"})
            text = ""
            continue
        used = loc
        break

    if not used:
        return {"asked": value, "title": record.get("title"), "state": "no text",
                "tried": tried, "extractor": name, "paths": None, "date": today()}

    split = split_text(text)
    meta = {
        "asked": value, "title": record.get("title"), "year": record.get("year"),
        "authors": record.get("authors"), "venue": record.get("venue"),
        "paperId": record.get("paperId"), "externalIds": record.get("externalIds"),
        "state": "fetched", "source_url": used["url"], "source": used["source"],
        "extractor": name, "extractor_detail": detail,
        "split": split["split"], "split_heading": split["heading"],
        "truncated": truncated,
        "pages": text.count(PAGE_BREAK) + 1,
        "chars": len(text), "intro_chars": len(split["intro"]),
        "tried": tried, "paths": paths, "date": today(), "cached": False,
    }

    os.makedirs(directory, exist_ok=True)
    try:
        with open(paths["full"], "w", encoding="utf-8") as fh:
            fh.write(text)
        with open(paths["intro"], "w", encoding="utf-8") as fh:
            fh.write(split["intro"])
        write_atomic(paths["meta"], meta)
    except OSError as exc:
        return err(f"could not write the fetch cache: {exc}")
    return meta


# --------------------------------------------------------------------------
# reviews: what the referees said


def openreview_token() -> tuple[str, str]:
    """(token, state). Logging in is optional and usually necessary: measured
    2026-09-16, both api.openreview.net and api2.openreview.net answer
    `/notes/search` anonymously but gate `/notes?forum=...` behind a bot
    challenge, so the submission is findable without credentials and its
    reviews are not."""
    user, password = _env("OPENREVIEW_USERNAME"), _env("OPENREVIEW_PASSWORD")
    if not (user and password):
        return "", "no login"
    got = fetch_json("openreview", "POST", f"{OPENREVIEW_BASE}/login",
                     body={"id": user, "password": password}, use_cache=False, attempts=2)
    if isinstance(got, dict) and got.get("token"):
        return got["token"], "logged in"
    return "", "login failed"


def openreview_search(query: str, limit: int = 10) -> list[dict[str, Any]]:
    got = fetch_json("openreview", "GET", f"{OPENREVIEW_BASE}/notes/search",
                     params={"term": query, "limit": limit})
    if not isinstance(got, dict) or "error" in got:
        return []
    return got.get("notes") or []


def _value(content: dict[str, Any], key: str) -> Any:
    """API2 wraps every field as {"value": ...}; API1 does not."""
    got = (content or {}).get(key)
    if isinstance(got, dict) and "value" in got:
        return got["value"]
    return got


REVIEW_RATING_KEYS = ("rating", "recommendation", "confidence", "soundness",
                      "presentation", "contribution", "correctness",
                      "technical_novelty_and_significance",
                      "empirical_novelty_and_significance")
REVIEW_TEXT_KEYS = ("review", "summary", "strengths", "weaknesses",
                    "summary_of_the_review", "strength_and_weaknesses",
                    "questions", "limitations", "main_review")


def _is_review(invitations: list[str]) -> bool:
    return any(i.rsplit("/", 1)[-1].lower() in
               ("official_review", "review", "public_review", "meta_review",
                "decision", "official_comment", "rebuttal", "author_response")
               for i in invitations or [])


def reviews(paper: str, limit: int = 10) -> dict[str, Any]:
    """OpenReview's record for one paper: the submission, then every official
    review, response and decision on its forum."""
    asked = (paper or "").strip()
    if not asked:
        return err("reviews needs a title or an arXiv id")

    notes = openreview_search(asked, limit)
    best = None
    for note in notes:
        title = _value(note.get("content") or {}, "title") or ""
        if title_match(asked, title) == "exact":
            best = note
            break
    if best is None and ARXIV_ID.fullmatch(asked.replace("arXiv:", "")):
        # An id is not searchable text on OpenReview; a caller passing one and
        # getting nothing has learned only that, so say which query was run.
        return {"asked": asked, "state": "no record", "query": asked,
                "note": "OpenReview search takes titles, not arXiv ids; pass the exact title",
                "date": today()}
    if best is None:
        return {"asked": asked, "state": "no record", "query": asked,
                "candidates": [_value(n.get("content") or {}, "title") for n in notes[:3]],
                "date": today()}

    content = best.get("content") or {}
    out = {
        "asked": asked, "state": "found", "forum": best.get("forum"),
        "id": best.get("id"), "title": _value(content, "title"),
        "venue": _value(content, "venue"), "venueid": _value(content, "venueid"),
        "url": f"https://openreview.net/forum?id={best.get('forum')}",
        "reviews": [], "responses": [], "decision": None, "date": today(),
    }

    token, login_state = openreview_token()
    out["login"] = login_state
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    got = fetch_json("openreview", "GET", f"{OPENREVIEW_BASE}/notes",
                     params={"forum": best.get("forum"), "limit": 200},
                     headers=headers, attempts=2)
    if not isinstance(got, dict) or "error" in got:
        detail = got.get("error", "") if isinstance(got, dict) else ""
        out["state"] = "login required" if "Challenge" in str(detail) or "403" in str(detail) else "forum unreadable"
        out["forum_error"] = str(detail)[:200]
        out["note"] = ("the submission was found; its reviews need credentials. "
                       "Set OPENREVIEW_USERNAME and OPENREVIEW_PASSWORD."
                       if out["state"] == "login required" else None)
        return out

    for note in got.get("notes") or []:
        invitations = note.get("invitations") or ([note["invitation"]] if note.get("invitation") else [])
        if note.get("id") == best.get("id") or not _is_review(invitations):
            continue
        c = note.get("content") or {}
        kind = (invitations[0].rsplit("/", 1)[-1] if invitations else "note").lower()
        entry = {
            "kind": kind,
            "ratings": {k: _value(c, k) for k in REVIEW_RATING_KEYS if _value(c, k) is not None},
            "text": {k: _value(c, k) for k in REVIEW_TEXT_KEYS if _value(c, k)},
            "signature": (note.get("signatures") or [""])[0].rsplit("/", 1)[-1],
        }
        if "decision" in kind:
            out["decision"] = _value(c, "decision") or _value(c, "recommendation")
        elif kind in ("official_comment", "rebuttal", "author_response"):
            out["responses"].append(entry)
        else:
            out["reviews"].append(entry)
    out["counts"] = {"reviews": len(out["reviews"]), "responses": len(out["responses"])}
    return out


# --------------------------------------------------------------------------
# datasets: what the hosts hold


def hf_datasets(name: str, limit: int = 5) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {_env('HF_TOKEN')}"} if _env("HF_TOKEN") else {}
    got = fetch_json("huggingface", "GET", f"{HF_BASE}/datasets",
                     params={"search": name, "limit": limit, "full": "true"}, headers=headers)
    if isinstance(got, dict) and "error" in got:
        return {"state": "error", "error": got["error"], "rows": []}
    rows = []
    for d in got if isinstance(got, list) else []:
        card = d.get("cardData") or {}
        rows.append({
            "id": d.get("id"), "url": f"https://huggingface.co/datasets/{d.get('id')}",
            "license": card.get("license") or next(
                (t.split(":", 1)[1] for t in (d.get("tags") or []) if t.startswith("license:")), None),
            "size": next((t.split(":", 1)[1] for t in (d.get("tags") or []) if t.startswith("size_categories:")), None),
            "modality": [t.split(":", 1)[1] for t in (d.get("tags") or []) if t.startswith("modality:")],
            "downloads": d.get("downloads"), "likes": d.get("likes"),
            "updated": d.get("lastModified"), "gated": d.get("gated"),
            "splits": [s.get("name") for s in (card.get("dataset_info") or {}).get("splits", [])]
                      if isinstance(card.get("dataset_info"), dict) else [],
        })
    return {"state": "ok" if rows else "nothing", "rows": rows,
            "keyed": bool(_env("HF_TOKEN"))}


def github_repos(name: str, limit: int = 5) -> dict[str, Any]:
    """GitHub over REST, not the `gh` command: the guard admits only the
    retrieval scripts in Bash, and widening that fence for one agent is a
    worse trade than one more HTTP call."""
    headers = {"Accept": "application/vnd.github+json"}
    token = _env("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    got = fetch_json("github", "GET", f"{GITHUB_BASE}/search/repositories",
                     params={"q": name, "per_page": limit, "sort": "stars"}, headers=headers,
                     keyed=bool(token))
    if isinstance(got, dict) and "error" in got:
        return {"state": "error", "error": got["error"], "rows": [], "keyed": bool(token)}
    rows = []
    for r in (got.get("items") or [])[:limit]:
        rows.append({
            "full_name": r.get("full_name"), "url": r.get("html_url"),
            "description": (r.get("description") or "")[:200],
            "license": ((r.get("license") or {}) or {}).get("spdx_id"),
            "stars": r.get("stargazers_count"), "updated": r.get("pushed_at"),
            "size_kb": r.get("size"), "topics": r.get("topics") or [],
        })
    return {"state": "ok" if rows else "nothing", "rows": rows,
            "total": got.get("total_count"), "keyed": bool(token)}


def datasets(name: str, limit: int = 5, context: str = "") -> dict[str, Any]:
    """One dataset, on both hosts. A host that returns nothing is named, so a
    row that says `could not determine` can say what was asked.

    `context` is appended to the GitHub query only. Measured 2026-09-16: a bare
    "xBD" returns an Xbox diagnostic tool above the xView2 solution, because
    GitHub search has no idea what field you are in. Hugging Face is left
    unqualified, since dataset ids there are already namespaced."""
    asked = (name or "").strip()
    if not asked:
        return err("datasets needs a name")
    hf = hf_datasets(asked, limit)
    gh = github_repos(f"{asked} {context}".strip(), limit)
    return {"asked": asked, "context": context or None, "date": today(),
            "huggingface": hf, "github": gh, "checked": ["huggingface", "github"],
            "state": "found" if (hf["rows"] or gh["rows"]) else "nothing found"}


# --------------------------------------------------------------------------
# authors: who is publishing, and where they are heading


def author_from_paper(name: str, paper: str) -> tuple[str | None, list[str]]:
    """(authorId, affiliations) for the person of this name ON this paper.

    Measured 2026-09-16: an author search for "Yu Shen" returns a profile with
    fifty papers since the floor, because the name belongs to several people
    and the index merges or mis-ranks them. Going through the paper removes the
    ambiguity entirely — the card already knows which paper it is."""
    got = s2_get(f"/paper/{urllib.parse.quote(paper, safe=':')}/authors",
                 params={"fields": "authorId,name,affiliations"})
    if not isinstance(got, dict) or "error" in got:
        return None, []
    wanted = normalised_title(name)
    for row in got.get("data") or []:
        candidate = normalised_title(row.get("name") or "")
        # "Y. Shen" and "Yu Shen" are the same person on the same paper; match
        # on surname plus a compatible first initial.
        if candidate == wanted or (
            candidate.split()[-1:] == wanted.split()[-1:]
            and candidate[:1] == wanted[:1]
        ):
            return row.get("authorId"), row.get("affiliations") or []
    return None, []


def authors(name: str, since: int | None = None, limit: int = 50,
            paper: str = "") -> dict[str, Any]:
    """One author's recent record. S2 first for its author endpoint, OpenAlex
    when S2 fails or throttles. `since` defaults to three years back, which is
    what "where are they heading" means; older work is already in the
    landscape.

    `paper` is an id the author is known to be on. Pass it: it resolves the
    person rather than the name, and a common name resolved by search is a
    different person's publication list."""
    asked = (name or "").strip()
    if not asked:
        return err("authors needs a name or an S2 author id")
    import datetime as _dt
    floor = since or (_dt.date.today().year - 3)
    checked: list[str] = []
    errors: dict[str, str] = {}
    affiliations: list[str] = []
    resolved_by = None

    ident = asked if asked.isdigit() else None
    if ident is None and paper:
        ident, affiliations = author_from_paper(asked, paper)
        checked.append("s2")
        if ident:
            resolved_by = f"paper {paper}"
    if ident is None:
        got = s2_get("/author/search", params={"query": asked, "fields": "authorId,name,affiliations,paperCount",
                                               "limit": 5})
        if "s2" not in checked:
            checked.append("s2")
        if isinstance(got, dict) and "error" not in got and got.get("data"):
            ident = got["data"][0].get("authorId")
            affiliations = affiliations or (got["data"][0].get("affiliations") or [])
            resolved_by = "name search"
        elif isinstance(got, dict) and "error" in got:
            errors["s2"] = got["error"]

    papers: list[dict[str, Any]] = []
    complete = True
    if ident:
        # The author-papers endpoint pages at 100 and does not promise an
        # ordering. Measured 2026-09-16: taking one page and filtering by year
        # under-reports a prolific author badly, so this walks up to
        # AUTHOR_PAGES pages and says so when it stops early.
        offset = 0
        for page in range(AUTHOR_PAGES):
            got = s2_get(f"/author/{ident}/papers",
                         params={"fields": "paperId,title,year,venue,externalIds,authors,citationCount",
                                 "limit": 100, "offset": offset})
            if not isinstance(got, dict) or "error" in got:
                if isinstance(got, dict):
                    errors["s2"] = got["error"]
                complete = False
                break
            rows = got.get("data") or []
            for row in rows:
                if (row.get("year") or 0) >= floor:
                    papers.append({
                        "title": row.get("title"), "year": row.get("year"),
                        "venue": row.get("venue"), "citations": row.get("citationCount"),
                        "ids": {k: v for k, v in (row.get("externalIds") or {}).items() if v},
                        "coauthors": [a.get("name") for a in (row.get("authors") or []) if a.get("name")],
                    })
            nxt = got.get("next")
            if not nxt or not rows:
                break
            offset = nxt
        else:
            complete = False  # the cap stopped us, not the record

    if not papers:
        got = fetch_json("openalex", "GET", f"{OA_AUTHORS}",
                         params={"search": asked, "per-page": 1})
        checked.append("openalex")
        if isinstance(got, dict) and "error" not in got and got.get("results"):
            author = got["results"][0]
            affiliations = affiliations or [
                (author.get("last_known_institution") or {}).get("display_name")
            ] if author.get("last_known_institution") else affiliations
            works = fetch_json("openalex", "GET", f"{OA_WORKS}",
                               params={"filter": f"author.id:{author.get('id')},from_publication_date:{floor}-01-01",
                                       "per-page": 50})
            if isinstance(works, dict) and "error" not in works:
                for w in works.get("results") or []:
                    papers.append({
                        "title": w.get("title") or w.get("display_name"),
                        "year": w.get("publication_year"),
                        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                        "citations": w.get("cited_by_count"),
                        "ids": {"OpenAlex": (w.get("id") or "").rsplit("/", 1)[-1]},
                        "coauthors": [(a.get("author") or {}).get("display_name")
                                      for a in (w.get("authorships") or [])
                                      if (a.get("author") or {}).get("display_name")],
                    })
        elif isinstance(got, dict) and "error" in got:
            errors["openalex"] = got["error"]

    counts: dict[str, int] = {}
    for p in papers:
        for co in p["coauthors"]:
            if co and normalised_title(co) != normalised_title(asked):
                counts[co] = counts.get(co, 0) + 1
    frequent = sorted(counts.items(), key=lambda kv: -kv[1])[:10]

    papers.sort(key=lambda p: (p.get("year") or 0), reverse=True)
    return {
        "asked": asked, "authorId": ident, "since": floor, "date": today(),
        "resolved_by": resolved_by,
        "affiliations": [a for a in affiliations if a],
        "papers": papers[:limit], "paper_count": len(papers),
        "frequent_coauthors": [{"name": n, "papers": c} for n, c in frequent],
        "checked": checked, "errors": errors, "complete": complete,
        "state": "found" if papers else "nothing since the floor",
        "note": None if complete else
                f"stopped at {AUTHOR_PAGES * 100} papers; this author may have more since {floor}",
    }


# --------------------------------------------------------------------------
# command line


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="papers.py",
        description="Reading-side retrieval: paper text, reviews, datasets, authors. One JSON result per call.",
    )
    ap.add_argument("--selftest", action="store_true", help="offline checks, then exit")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("fetch", help="one paper's text, split at the end of the introduction")
    p.add_argument("paper", help="arXiv id, DOI, S2 id, OpenAlex id, or an exact title")
    p.add_argument("--refresh", action="store_true", help="ignore a cached copy")

    p = sub.add_parser("reviews", help="OpenReview's record for one paper: ratings, objections, responses")
    p.add_argument("paper", help="the exact title; OpenReview search does not take arXiv ids")
    p.add_argument("--limit", type=int, default=10, help="search rows to consider")

    p = sub.add_parser("datasets", help="one dataset on the Hugging Face hub and on GitHub")
    p.add_argument("name")
    p.add_argument("--limit", type=int, default=5, help="rows per host")
    p.add_argument("--context", default="", help="words appended to the GitHub query only, e.g. the field")

    p = sub.add_parser("authors", help="one author's papers since a year floor, and their frequent co-authors")
    p.add_argument("name", help="an author name, or an S2 author id")
    p.add_argument("--since", type=int, default=None, help="year floor; default three years back")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--paper", default="", help="an id this author is on; resolves the person, not the name")

    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.cmd:
        ap.print_help()
        return 0

    if args.cmd == "fetch":
        out = fetch_paper(args.paper, args.refresh)
    elif args.cmd == "reviews":
        out = reviews(args.paper, args.limit)
    elif args.cmd == "datasets":
        out = datasets(args.name, args.limit, args.context)
    elif args.cmd == "authors":
        out = authors(args.name, args.since, args.limit, args.paper)
    else:  # pragma: no cover - argparse rejects anything else
        out = err(f"unknown verb: {args.cmd}")

    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


# --------------------------------------------------------------------------
# selftest


def selftest() -> int:
    """Offline. The split on captured paper text, the id classifier, the
    location list, and the four states `fetch` can report."""
    import snowball

    failures: list[str] = []
    os.environ["RESEARCH_CACHE_DIR"] = tempfile.mkdtemp(prefix="papers-cache-")
    os.environ["RESEARCH_PROJECT_DIR"] = tempfile.mkdtemp(prefix="papers-project-")
    for name in ("S2_API_KEY", "SEMANTIC_SCHOLAR_API_KEY", "UNPAYWALL_EMAIL",
                 "HF_TOKEN", "GITHUB_TOKEN", "OPENREVIEW_USERNAME", "OPENREVIEW_PASSWORD"):
        os.environ.pop(name, None)
    snowball.PACE.update({k: 0.0 for k in snowball.PACE})

    def check(case: str, ok: bool, detail: str = "") -> None:
        print(f"{'ok  ' if ok else 'FAIL'} {case}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(case)

    here = os.path.dirname(os.path.abspath(__file__))

    def fixture(name: str) -> str:
        with open(os.path.join(here, "fixtures", name), encoding="utf-8") as fh:
            return fh.read()

    # 1. A two-column paper with a numbered related-work heading splits there.
    two_col = fixture("paper_two_column.txt")
    got = split_text(two_col)
    check("1  a numbered Related Work heading ends the intro",
          got["split"] == "heading" and "related work" in (got["heading"] or "").lower()
          and "Introduction" in got["intro"] and "SegFormer backbone" not in got["intro"],
          f"got split={got['split']} heading={got['heading']!r}")

    # 2. No heading at all: the page cut, and it says so.
    no_heading = fixture("paper_no_heading.txt")
    got = split_text(no_heading)
    check("2  with no heading the split is a page cut, and it is recorded",
          got["split"] == "page-cut" and got["heading"] is None and 0 < got["cut_at"] < len(no_heading),
          f"got {got['split']} cut_at={got['cut_at']}")

    # 2b. A "Methods" heading far down the body is not believed as the intro's end.
    late = "Introduction\n" + ("filler line\n" * 400) + "\n3. Methods\n" + ("body\n" * 50)
    got = split_text(late)
    check("2b a Methods heading past the window is not the end of the intro",
          got["split"] == "page-cut", f"got {got['split']} at {got['cut_at']} of {len(late)}")

    # 2b2. IEEE small caps: "II. R ELATED W ORK" is the same heading.
    ieee = ("A Paper\n\nAbstract\n\nsome abstract text\n\nI. I NTRODUCTION\n"
            + ("intro prose line\n" * 40) + "II. R ELATED W ORK\n" + ("body\n" * 300))
    got = split_text(ieee)
    check("2b2 an IEEE small-caps heading ends the intro like any other",
          got["split"] == "heading" and "ELATED" in (got["heading"] or ""),
          f"got split={got['split']} heading={got['heading']!r}")

    # 2c. The intro file always carries the title block and the introduction.
    got = split_text(two_col)
    check("2c the intro file holds the title, the abstract and the introduction",
          "DA-SegFormer" in got["intro"] and "Abstract" in got["intro"],
          f"intro starts {got['intro'][:60]!r}")

    # 3. A record with no PDF location anywhere: `no text`, with what was checked.
    record = finish({"paperId": "nopdf", "title": "A Paper Behind A Paywall", "year": 2021,
                     "externalIds": {"DOI": "10.1000/paywalled"}, "pdfUrl": None})
    check("3  a record with no open-access location yields no locations",
          pdf_locations(record) == [], f"got {pdf_locations(record)}")

    saved_resolve = globals()["resolve"]
    globals()["resolve"] = lambda value: {"record": record, "checked": ["s2"], "errors": {}, "matched": "doi"}
    try:
        out = fetch_paper("10.1000/paywalled")
        check("3b fetch reports `no text` and names the sources it checked",
              out["state"] == "no text" and out["paths"] is None and "unpaywall" in " ".join(out.get("checked", [])),
              f"got {json.dumps(out)[:200]}")

        # 4. No extractor on the machine: a state with both install hints.
        saved_extractor = globals()["extractor"]
        globals()["extractor"] = lambda: ("", "")
        try:
            with_pdf = finish({"paperId": "haspdf", "title": "A Paper With A PDF", "year": 2022,
                               "externalIds": {"ArXiv": "2201.00001"}, "pdfUrl": "https://example.org/p.pdf"})
            globals()["resolve"] = lambda value: {"record": with_pdf, "checked": ["s2"], "errors": {}, "matched": "arxiv"}
            out = fetch_paper("2201.00001")
            check("4  with no extractor installed the state says so, with both hints",
                  out["state"] == "no extractor" and "pdftotext" in out["hint"] and "pypdf" in out["hint"],
                  f"got {json.dumps(out)[:200]}")
        finally:
            globals()["extractor"] = saved_extractor
    finally:
        globals()["resolve"] = saved_resolve

    # 5. The id classifier, on the five shapes a caller hands us.
    cases = [("2201.00001", "arxiv"), ("arXiv:2201.00001v2", "arxiv"),
             ("10.3390/rs12223808", "doi"), ("https://doi.org/10.3390/rs12223808", "doi"),
             ("W2967473420", "openalex"), ("ec58b594" + "0" * 32, "s2"),
             ("Creating xBD: A Dataset", "title")]
    bad = [(v, identify(v)[0], want) for v, want in cases if identify(v)[0] != want]
    check("5  ids are classified before titles, so a DOI is never read as an arXiv id",
          not bad, f"misread {bad}")

    # 6. A title that does not match exactly never resolves.
    def only(*titles: str):
        def stub(query, limit=20, extra=None):
            return {"papers": [finish({"paperId": "x", "title": t}) for t in titles],
                    "rows_returned": len(titles), "resolved_count": len(titles)}
        return stub
    saved_s2, saved_oa = globals()["s2_search"], globals()["oa_search"]
    globals()["s2_search"] = only("Attention Is All You Need")
    globals()["oa_search"] = only("Attention Is All You Need")
    try:
        out = resolve("Attention Is All You Need for Wildfire Damage Assessment")
        check("6  a prefix title match does not resolve; the record stays empty",
              out.get("record") is None and out.get("state") == "not resolved",
              f"got {json.dumps(out)[:200]}")
    finally:
        globals()["s2_search"], globals()["oa_search"] = saved_s2, saved_oa

    # 7. The arXiv PDF is offered even when the index gave no pdfUrl.
    arx = finish({"paperId": "a", "title": "T", "externalIds": {"ArXiv": "2201.00001"}, "pdfUrl": None})
    locs = pdf_locations(arx)
    check("7  an arXiv id is a PDF location even with no pdfUrl on the record",
          len(locs) == 1 and locs[0]["source"] == "arxiv" and "2201.00001" in locs[0]["url"],
          f"got {locs}")

    # 8. A downloaded body that is not a PDF is a problem, not text.
    saved_read = globals()["_read_body"]
    globals()["_read_body"] = lambda url: (200, b"<html>login required</html>", None)
    try:
        raw, problem = download("https://example.org/p.pdf")
        check("8  an HTML login page is not accepted as a PDF",
              raw == b"" and "not a PDF" in (problem or ""), f"got {problem!r}")
    finally:
        globals()["_read_body"] = saved_read

    # 8b. A truncated PDF is kept and named, not discarded. Measured on arXiv
    # 2004.07312: a single read() stops at 4 MiB where a chunked read does not,
    # so the retry that "fixed" it could never have worked and the partial is
    # the only thing that would have.
    globals()["_read_body"] = lambda url: (200, b"%PDF-1.5 partial", "truncated at 16 bytes")
    try:
        raw, problem = download("https://example.org/big.pdf")
        check("8b a truncated PDF is kept, with the truncation named",
              raw.startswith(b"%PDF") and "truncated" in (problem or ""), f"got {problem!r}")
    finally:
        globals()["_read_body"] = saved_read

    # 8c. A transport failure is retried; a non-PDF body is not.
    calls = []

    def flaky(url):
        calls.append(url)
        return (200, b"%PDF-ok", None) if len(calls) > 1 else (0, b"TimeoutError", None)
    globals()["_read_body"] = flaky
    try:
        raw, problem = download("https://example.org/slow.pdf", attempts=2)
        check("8c a transport failure is retried once and can succeed",
              raw == b"%PDF-ok" and len(calls) == 2, f"got {len(calls)} calls, {problem!r}")
    finally:
        globals()["_read_body"] = saved_read

    # 9. Two papers never share a fetch directory.
    a = fetch_dir(finish({"paperId": "p1", "title": "One", "externalIds": {"ArXiv": "2201.00001"}}))
    b = fetch_dir(finish({"paperId": "p2", "title": "Two", "externalIds": {"ArXiv": "2201.00002"}}))
    check("9  the fetch directory is per paper", a != b and "arxiv-2201.00001" in a, f"{a} vs {b}")


    # --- reviews -----------------------------------------------------------

    def as_bytes(name):
        with open(os.path.join(here, "fixtures", name), encoding="utf-8") as fh:
            return fh.read().encode()

    saved_fetch_json = globals()["fetch_json"]

    def routed(**by_fragment):
        def stub(resolver, method, url, **kw):
            for fragment, answer in by_fragment.items():
                if fragment in url:
                    return answer() if callable(answer) else answer
            return err(f"unrouted: {url}")
        return stub

    globals()["fetch_json"] = routed(**{
        "/notes/search": json.loads(as_bytes("openreview_search.json")),
        "/notes": json.loads(as_bytes("openreview_forum.json")),
    })
    try:
        out = reviews("Memory Efficient Transformer Adapter for Dense Predictions")
        check("10  reviews returns two official reviews, one response and the decision",
              out["state"] == "found" and out["counts"] == {"reviews": 2, "responses": 1}
              and out["decision"] == "Accept (Poster)" and out["venue"] == "ICLR 2025 Poster",
              f"got {json.dumps({k: out.get(k) for k in ('state', 'counts', 'decision', 'venue')})}")
        check("10b a review carries its ratings and the reviewer's own words",
              out["reviews"][0]["ratings"].get("rating") == 6
              and "omits the strongest prior adapter" in json.dumps(out["reviews"][0]["text"]),
              f"got {json.dumps(out['reviews'][0])[:200]}")
        # An inexact title is not this paper. OpenReview search is fuzzy; the
        # exact-match rule is what stops a neighbouring submission's reviews
        # from landing on the wrong card.
        out = reviews("Transformer Adapter for Dense Predictions")
        check("11  a near title is `no record`, and names what it saw instead",
              out["state"] == "no record" and out["candidates"], f"got {json.dumps(out)[:200]}")
    finally:
        globals()["fetch_json"] = saved_fetch_json

    # The forum is gated and the submission is not: found, and honest about it.
    globals()["fetch_json"] = routed(**{
        "/notes/search": json.loads(as_bytes("openreview_search.json")),
        "/notes": err("openreview request failed: ChallengeRequiredError: Challenge verification required", 1, 403),
    })
    try:
        out = reviews("Memory Efficient Transformer Adapter for Dense Predictions")
        check("12  a gated forum is `login required`, with the submission still named",
              out["state"] == "login required" and out["url"] and "OPENREVIEW_USERNAME" in (out.get("note") or ""),
              f"got {json.dumps(out)[:220]}")
    finally:
        globals()["fetch_json"] = saved_fetch_json

    # --- datasets ----------------------------------------------------------

    globals()["fetch_json"] = routed(**{
        "/api/datasets": json.loads(as_bytes("hf_datasets.json")),
        "/search/repositories": json.loads(as_bytes("github_search.json")),
    })
    try:
        out = datasets("xBD", 5, context="building damage")
        hf, gh = out["huggingface"], out["github"]
        check("13  datasets reads license, size and splits off a hub row",
              out["state"] == "found" and hf["rows"][1]["license"] == "apache-2.0"
              and hf["rows"][0]["size"] == "1K<n<10K"
              and hf["rows"][1]["splits"] == ["train", "test"],
              f"got {json.dumps(hf['rows'])[:250]}")
        check("13b and license, stars and the description off a GitHub row",
              gh["rows"][0]["license"] == "MIT" and gh["rows"][0]["stars"] == 61
              and "damage" in gh["rows"][0]["description"],
              f"got {json.dumps(gh['rows'][0])[:200]}")
        check("13c the context reaches the GitHub query and not the hub one",
              out["context"] == "building damage")
    finally:
        globals()["fetch_json"] = saved_fetch_json

    globals()["fetch_json"] = routed(**{"/api/datasets": [], "/search/repositories": {"items": [], "total_count": 0}})
    try:
        out = datasets("a dataset nobody has ever made")
        check("14  both hosts empty is `nothing found`, with both named as checked",
              out["state"] == "nothing found" and out["checked"] == ["huggingface", "github"]
              and out["huggingface"]["state"] == "nothing" and out["github"]["state"] == "nothing",
              f"got {json.dumps(out)[:200]}")
    finally:
        globals()["fetch_json"] = saved_fetch_json

    # --- authors -----------------------------------------------------------

    saved_s2_get = globals()["s2_get"]

    def s2_author_stub(path, params=None, **kw):
        if "/author/search" in path:
            return {"data": [{"authorId": "2302365756", "name": "Ritwik Gupta",
                              "affiliations": ["UC Berkeley"]}]}
        if "/papers" in path:
            return json.loads(as_bytes("s2_author_papers.json"))
        return err("unrouted")
    globals()["s2_get"] = s2_author_stub
    try:
        out = authors("Ritwik Gupta", since=2023)
        years = [p["year"] for p in out["papers"]]
        check("15  authors returns only papers at or after the floor, newest first",
              out["state"] == "found" and years == sorted(years, reverse=True)
              and all(y >= 2023 for y in years) and out["paper_count"] == 2,
              f"got years {years}, count {out['paper_count']}")
        check("15b frequent co-authors are counted, and the author is not their own co-author",
              out["frequent_coauthors"][0] == {"name": "A. Reddie", "papers": 2}
              and all("Ritwik" not in c["name"] for c in out["frequent_coauthors"]),
              f"got {out['frequent_coauthors']}")
        import datetime as _d
        out = authors("Ritwik Gupta")
        check("15c the floor defaults to three years back",
              out["since"] == _d.date.today().year - 3,
              f"got {out['since']}, wanted {_d.date.today().year - 3}")
    finally:
        globals()["s2_get"] = saved_s2_get

    # 15f. A prolific author is paged through, and a cap is declared, not hidden.
    def paged(path, params=None, **kw):
        if "/author/search" in path:
            return {"data": [{"authorId": "a1", "name": "Prolific Person"}]}
        if "/papers" in path:
            offset = (params or {}).get("offset", 0)
            return {"data": [{"paperId": f"p{offset}{i}", "title": "T", "year": 2025,
                              "authors": [{"name": "Prolific Person"}]} for i in range(100)],
                    "next": offset + 100}
        return err("unrouted")
    globals()["s2_get"] = paged
    try:
        out = authors("Prolific Person", since=2023, limit=1000)
        check("15f a prolific author is paged, and the cap is declared rather than hidden",
              out["paper_count"] == 500 and out["complete"] is False and "may have more" in (out["note"] or ""),
              f"got count={out['paper_count']}, complete={out['complete']}")
    finally:
        globals()["s2_get"] = saved_s2_get

    # 15d. --paper resolves the person, not the name. Two people share a name;
    # the one on the card's paper is the one whose record we want.
    def s2_paper_authors(path, params=None, **kw):
        if "/authors" in path and "/paper/" in path:
            return {"data": [{"authorId": "right-one", "name": "Yu Shen",
                              "affiliations": ["UNC Charlotte"]},
                             {"authorId": "other", "name": "Chen Chen"}]}
        if "/author/search" in path:
            return {"data": [{"authorId": "wrong-one", "name": "Yu Shen", "paperCount": 400}]}
        if "/papers" in path:
            return {"data": [{"paperId": "p", "title": "T", "year": 2025, "authors": []}]}
        return err("unrouted")
    globals()["s2_get"] = s2_paper_authors
    try:
        out = authors("Yu Shen", since=2023, paper="arXiv:2105.07364")
        check("15d --paper resolves the author through the paper, not a name search",
              out["authorId"] == "right-one" and out["resolved_by"].startswith("paper")
              and out["affiliations"] == ["UNC Charlotte"],
              f"got id={out['authorId']}, by={out.get('resolved_by')}")
        out = authors("Yu Shen", since=2023)
        check("15e without --paper it falls back to the name search, and says so",
              out["authorId"] == "wrong-one" and out["resolved_by"] == "name search",
              f"got id={out['authorId']}, by={out.get('resolved_by')}")
    finally:
        globals()["s2_get"] = saved_s2_get

    # S2 down: OpenAlex answers, and the result says which index was reached.
    globals()["s2_get"] = lambda *a, **k: err("s2 request failed after 5 attempts", 5, 429)
    globals()["fetch_json"] = routed(**{
        "/authors": {"results": [{"id": "https://openalex.org/A123",
                                  "last_known_institution": {"display_name": "UC Berkeley"}}]},
        "/works": {"results": [{"id": "https://openalex.org/W1", "title": "A Recent Work",
                                "publication_year": 2025, "cited_by_count": 3,
                                "primary_location": {"source": {"display_name": "CVPR"}},
                                "authorships": [{"author": {"display_name": "Ritwik Gupta"}},
                                                {"author": {"display_name": "A. Reddie"}}]}]},
    })
    try:
        out = authors("Ritwik Gupta", since=2023)
        check("16  with S2 down OpenAlex answers, and both the error and the fallback are named",
              out["state"] == "found" and out["papers"][0]["title"] == "A Recent Work"
              and "s2" in out["errors"] and "openalex" in out["checked"],
              f"got {json.dumps(out)[:240]}")
    finally:
        globals()["s2_get"] = saved_s2_get
        globals()["fetch_json"] = saved_fetch_json

    print()
    print(f"{'FAILED' if failures else 'all green'}: {len(failures)} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
