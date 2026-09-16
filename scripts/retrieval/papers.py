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
import subprocess
import sys
import tempfile
import time
import urllib.parse
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snowball import (  # noqa: E402
    ARXIV_ID,
    BACKOFF_BASE,
    RETRYABLE,
    S2_FIELDS,
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
    re.I | re.M,
)

# The intro has to start somewhere too: anything before it is the title block.
INTRO_HEADING = re.compile(
    r"^\s*(?:(?:[IVX]+|\d+)[.)]?\s*)?(introduction)\s*$", re.I | re.M
)

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
            done = subprocess.run(  # noqa: S603 - fixed binary, no shell
                ["pdftotext", "-layout", pdf_path, "-"],
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
    intro_at = 0
    found = INTRO_HEADING.search(text[:limit])
    if found:
        intro_at = found.start()

    for match in SECTION_AFTER_INTRO.finditer(text):
        if match.start() <= intro_at:
            continue  # a "Methods" line inside the abstract is not the end of the intro
        if match.start() > limit:
            break
        return {"intro": text[:match.start()].rstrip(), "split": "heading",
                "cut_at": match.start(), "heading": match.group(0).strip()}

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


def download(url: str, attempts: int = 2) -> tuple[bytes, str | None]:
    """A PDF is bytes, not JSON, so this goes round `fetch_json` to the one
    attempt underneath and keeps the retry shape by hand. Measured 2026-09-16:
    an arXiv PDF that curl pulls in two seconds timed out once at sixty, so a
    single slow moment must not cost us the only location we have."""
    problem = ""
    for attempt in range(max(attempts, 1)):
        status, raw = http_fetch("GET", url, None,
                                 {"User-Agent": user_agent(), "Accept": "application/pdf"})
        if status == 200 and raw.startswith(b"%PDF"):
            return raw, None
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
    for loc in locations:
        raw, problem = download(loc["url"])
        if problem:
            tried.append({**loc, "problem": problem})
            continue
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

    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.cmd:
        ap.print_help()
        return 0

    if args.cmd == "fetch":
        out = fetch_paper(args.paper, args.refresh)
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
    saved_http = globals()["http_fetch"]
    globals()["http_fetch"] = lambda *a, **k: (200, b"<html>login required</html>")
    try:
        raw, problem = download("https://example.org/p.pdf")
        check("8  an HTML login page is not accepted as a PDF",
              raw == b"" and "not a PDF" in (problem or ""), f"got {problem!r}")
    finally:
        globals()["http_fetch"] = saved_http

    # 9. Two papers never share a fetch directory.
    a = fetch_dir(finish({"paperId": "p1", "title": "One", "externalIds": {"ArXiv": "2201.00001"}}))
    b = fetch_dir(finish({"paperId": "p2", "title": "Two", "externalIds": {"ArXiv": "2201.00002"}}))
    check("9  the fetch directory is per paper", a != b and "arxiv-2201.00001" in a, f"{a} vs {b}")

    print()
    print(f"{'FAILED' if failures else 'all green'}: {len(failures)} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
