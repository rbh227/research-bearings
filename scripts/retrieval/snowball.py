#!/usr/bin/env python3
"""snowball — the retrieval script for research-bearings.

Search and citation checking over four indexes. Standard library only. Every
invocation is one process that prints one JSON result and exits; nothing
stays resident.

  snowball.py status [--md]                    live probe of every source
  snowball.py health                           keys and paths; no network
  snowball.py search "query" [--limit N] [--index all|s2|openalex|arxiv]
  snowball.py batch <id> [<id> ...]            S2 metadata for many ids
  snowball.py verify [--title T]... [--id I]... [--limit N]
  snowball.py openalex search "q" | work <W|doi> | refs <W> | cited-by <W>
  snowball.py crossref doi <doi> | search "title"
  snowball.py arxiv search ["q"] [--cat cs.CV] [--from YYYY-MM-DD] [--to YYYY-MM-DD]
  snowball.py --selftest                       offline, seconds

Sources and keys are documented in docs/APIS.md. None is required:

  S2_API_KEY          x-api-key. 1 request/second with it, and the script paces
                      to that. Also read: SEMANTIC_SCHOLAR_API_KEY, and one line
                      in ~/.config/research-bearings/s2-api-key.
  OPENALEX_MAILTO     polite pool.  OPENALEX_API_KEY  optional.
  CROSSREF_MAILTO     polite pool.
  UNPAYWALL_EMAIL     required by that API; probed by status only.
  HF_TOKEN            bearer; probed by status only.
  ZOTERO_API_KEY, ZOTERO_USER_ID     probed by status only.
  RESEARCH_CACHE_DIR  default ~/.cache/research-bearings/. Raw responses, per
                      resolver, keyed by query, 30-day TTL. Disposable.
  RESEARCH_PROJECT_DIR  the project whose research/ receives records.
                      Default CLAUDE_PROJECT_DIR, else cwd.

One on-disk artifact under <project>/research/:
  .papers/<key>.json  one record per paper returned, written by the script
                      rather than by a model: hundreds of records through a
                      model's context costs tokens and invites transcription
                      errors.

Degradation is a result, never an error. `search` merges Semantic Scholar and
OpenAlex and reports which answered; `verify` tries S2, then OpenAlex, then
Crossref, and only an exact title match after folding certifies a paper. A
prefix or substring match is a `candidate`, named with its id, and never
resolved: measured 2026-09-14, "Attention Is All You Need for Wildfire Damage
Assessment" prefix-matched "Attention Is All You Need" and came back resolved,
carrying the wrong paper's id.
"""
from __future__ import annotations

import concurrent.futures
import contextlib
import datetime as _dt
import hashlib
import io
import json
import os
import random
import re
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

try:  # POSIX. Absent on Windows, where pacing and locks degrade to best effort.
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None  # type: ignore[assignment]


def _version() -> str:
    """The plugin's version, read from its manifest rather than kept here."""
    manifest = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..",
        ".claude-plugin", "plugin.json")
    try:
        with open(manifest, encoding="utf-8") as fh:
            return str(json.load(fh).get("version") or "unknown")
    except (OSError, ValueError):
        return "unknown"


VERSION = _version()
TIMEOUT = 60

S2_BASE = "https://api.semanticscholar.org/graph/v1"
OA_BASE = "https://api.openalex.org"
CR_BASE = "https://api.crossref.org"
ARXIV_BASE = "https://export.arxiv.org/api/query"
UNPAYWALL_BASE = "https://api.unpaywall.org/v2"
HF_BASE = "https://huggingface.co/api"
ZOTERO_BASE = "https://api.zotero.org"

# Fixed by contract, not caller-specified. A caller-chosen field list is a way
# for one landscape section to become quietly incomparable with the one beside it.
S2_FIELDS = (
    "paperId,title,year,externalIds,venue,authors,abstract,citationCount,"
    "referenceCount,influentialCitationCount,openAccessPdf,publicationTypes,"
    "fieldsOfStudy"
)
OA_FIELDS = (
    "id,doi,title,publication_year,cited_by_count,referenced_works,ids,"
    "primary_location,locations,authorships,type,open_access,"
    "abstract_inverted_index,best_oa_location"
)
CR_FIELDS = (
    "DOI,title,issued,created,is-referenced-by-count,container-title,author,"
    "published-online,published-print,abstract"
)

# Ticket 09 measured the documented 1 RPS model as wrong for the unkeyed pool:
# 429s survive 1.1 s spacing and never carry Retry-After. Keyed, the limit is
# real and the script paces to it. arXiv's terms are one call per 3 seconds.
PACE = {"s2": 1.0, "openalex": 0.1, "crossref": 0.05, "arxiv": 3.0}
ATTEMPTS = 5
BACKOFF_BASE = 0.5
BACKOFF_CAP = 8.0
# 0 is our own marker for a transport failure: connection reset, read timeout,
# truncated body. Those are exactly as retryable as a 429.
RETRYABLE = frozenset({0, 429, 500, 502, 503, 504})

DAY = 86400
TTL = 30 * DAY

BATCH_MAX = 500
SEARCH_MAX = 100
OA_FILTER_MAX = 50  # values per OR-filter on OpenAlex

KEY_FILE = "~/.config/research-bearings/s2-api-key"

# --------------------------------------------------------------------------
# config


def _env(name: str) -> str:
    return os.environ.get(name, "").strip()


def s2_key() -> str:
    """S2_API_KEY, the older name, then one line in KEY_FILE. No plugin config,
    no secrets store, nothing the sandbox cannot see: a file the user can cat."""
    key = _env("S2_API_KEY") or _env("SEMANTIC_SCHOLAR_API_KEY")
    if key:
        return key
    try:
        with open(os.path.expanduser(KEY_FILE), encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def keys_present() -> dict[str, bool]:
    return {
        "S2_API_KEY": bool(s2_key()),
        "OPENALEX_API_KEY": bool(_env("OPENALEX_API_KEY")),
        "OPENALEX_MAILTO": bool(_env("OPENALEX_MAILTO")),
        "CROSSREF_MAILTO": bool(_env("CROSSREF_MAILTO")),
        "UNPAYWALL_EMAIL": bool(_env("UNPAYWALL_EMAIL")),
        "HF_TOKEN": bool(_env("HF_TOKEN")),
        "ZOTERO_API_KEY": bool(_env("ZOTERO_API_KEY")),
        "ZOTERO_USER_ID": bool(_env("ZOTERO_USER_ID")),
    }


def user_agent() -> str:
    mailto = _env("OPENALEX_MAILTO") or _env("CROSSREF_MAILTO") or _env("UNPAYWALL_EMAIL")
    ua = f"research-bearings/{VERSION} (https://github.com/rbh227/research-bearings"
    return ua + (f"; mailto:{mailto})" if mailto else ")")


def cache_dir() -> str:
    return _env("RESEARCH_CACHE_DIR") or os.path.expanduser("~/.cache/research-bearings")


def project_dir() -> str:
    """RESEARCH_PROJECT_DIR, else CLAUDE_PROJECT_DIR (set for every Bash call
    Claude Code makes), else cwd."""
    return os.path.abspath(_env("RESEARCH_PROJECT_DIR") or _env("CLAUDE_PROJECT_DIR") or os.getcwd())


def records_dir() -> str:
    return os.path.join(project_dir(), "research", ".papers")


def today() -> str:
    return _dt.date.today().isoformat()


def err(message: str, attempts: int = 0, status: int | None = None) -> dict[str, Any]:
    """The one error shape. Verbs return it; they never raise, because a tool
    that throws leaves the model to invent what happened."""
    return {"error": message, "attempts": attempts, "status": status}


# --------------------------------------------------------------------------
# files, cache, pacing


def write_atomic(path: str, payload: Any) -> None:
    """Unique temp file in the same directory, then rename: a reader never
    sees half a file, and two writers never interleave."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=1, sort_keys=True)
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def cache_key(resolver: str, method: str, url: str, body: Any, keyed: bool) -> str:
    """Keyed by resolver and the full query. Distinguishes a keyed S2 request
    from an unkeyed one: the two pools return different data under load."""
    raw = "\n".join([resolver, method, url, json.dumps(body, sort_keys=True), "keyed" if keyed else "anon"])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def cache_path(resolver: str, key: str) -> str:
    return os.path.join(cache_dir(), resolver, key + ".json")


def cache_read(resolver: str, key: str, now: float | None = None) -> str | None:
    path = cache_path(resolver, key)
    if not os.path.exists(path):
        return None
    age = (now if now is not None else time.time()) - os.path.getmtime(path)
    if age > TTL:
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("text")
    except (OSError, ValueError, AttributeError):
        return None


def cache_write(resolver: str, key: str, text: str) -> None:
    with contextlib.suppress(OSError):  # a disposable cache is never worth failing a call over
        write_atomic(cache_path(resolver, key), {"text": text, "saved": today()})


@contextlib.contextmanager
def _locked(path: str):
    """An exclusive flock on `path`, or nothing where fcntl is absent."""
    if fcntl is None:
        yield
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    handle = open(path, "a+")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    finally:
        handle.close()


def pace_wait(last: float, now: float, gap: float) -> float:
    """Seconds still to wait so that this call is `gap` after the last."""
    return max(0.0, gap - (now - last))


def pace(resolver: str, gap: float) -> None:
    """Space requests to one resolver across processes: seven searchers in
    parallel must still make one arXiv call per 3 seconds between them. The
    timestamp file is held under a lock for the wait, so concurrent callers
    queue rather than all reading the same stale stamp."""
    if gap <= 0:
        return
    stamp = os.path.join(cache_dir(), f".pace-{resolver}")
    with contextlib.suppress(OSError):
        with _locked(stamp + ".lock"):
            try:
                last = os.path.getmtime(stamp)
            except OSError:
                last = 0.0
            wait = pace_wait(last, time.time(), gap)
            if wait > 0:
                time.sleep(wait)
            with open(stamp, "a"):
                os.utime(stamp, None)


# --------------------------------------------------------------------------
# HTTP


def http_fetch(method: str, url: str, body: Any, headers: dict[str, str]) -> tuple[int, bytes]:
    """One attempt. Returns (status, raw body), status 0 for a transport failure.
    Every read is inside the guard: `urlopen` succeeding does not mean the body
    arrives."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read()
        except Exception as read_exc:  # noqa: BLE001
            detail = f"<error body unreadable: {read_exc}>".encode()
        return exc.code, detail
    except urllib.error.URLError as exc:
        return 0, str(exc.reason).encode("utf-8")
    except Exception as exc:  # noqa: BLE001 - TimeoutError, ConnectionReset, IncompleteRead
        return 0, f"{type(exc).__name__}: {exc}".encode()


def fetch(
    resolver: str,
    method: str,
    url: str,
    params: dict[str, Any] | None = None,
    body: Any = None,
    headers: dict[str, str] | None = None,
    keyed: bool = False,
    use_cache: bool = True,
    attempts: int = ATTEMPTS,
) -> tuple[str | None, dict[str, Any] | None]:
    """Cache, pace, retry. Returns (text, None) or (None, error dict). Never raises."""
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    hdrs = {"User-Agent": user_agent(), **(headers or {})}
    ck = cache_key(resolver, method, url, body, keyed)
    if use_cache:
        cached = cache_read(resolver, ck)
        if cached is not None:
            return cached, None

    status: int | None = None
    detail = ""
    for attempt in range(attempts):
        # S2 paces only when keyed: unkeyed, spacing does not help (ticket 09).
        pace(resolver, PACE.get(resolver, 0.0) if (resolver != "s2" or keyed) else 0.0)
        status, raw = http_fetch(method, url, body, hdrs)
        if status == 200:
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                return None, err(f"{resolver}: undecodable response: {exc}", attempt + 1, status)
            if use_cache:
                cache_write(resolver, ck, text)
            return text, None
        detail = raw.decode("utf-8", "replace")[:300]
        if status not in RETRYABLE:
            return None, err(f"{resolver} request failed: {detail}", attempt + 1, status)
        if attempt < attempts - 1:
            # Full jitter. Retry is what works here; spacing is not.
            time.sleep(random.uniform(0, min(BACKOFF_CAP, BACKOFF_BASE * 2**attempt)))
    return None, err(
        f"{resolver} request failed after {attempts} attempts: {detail or 'no response'}",
        attempts, status,
    )


def fetch_json(resolver: str, method: str, url: str, **kw: Any) -> Any:
    text, problem = fetch(resolver, method, url, **kw)
    if problem:
        return problem
    try:
        return json.loads(text or "")
    except ValueError as exc:
        return err(f"malformed response from {resolver}: {exc}", 1, 200)


# --------------------------------------------------------------------------
# the unified record


def norm_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    d = str(doi).strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)
    d = re.sub(r"^doi:", "", d, flags=re.I)
    return d.lower() or None


ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?", re.I)


def norm_arxiv(value: str | None) -> str | None:
    """An arXiv id without its version: 2409.00665v1 and 2409.00665 are one paper."""
    if not value:
        return None
    m = ARXIV_ID.search(str(value))
    return m.group(1) if m else None


def norm_openalex(value: str | None) -> str | None:
    if not value:
        return None
    m = re.search(r"(W\d+)", str(value))
    return m.group(1) if m else None


def missing_fields(rec: dict[str, Any]) -> list[str]:
    """What a card must mark rather than fill in. Half of backward-hop rows
    have no abstract; that is a fact about the corpus, not a gap to guess at."""
    out = []
    if not (rec.get("abstract") or "").strip():
        out.append("abstract")
    if not (rec.get("venue") or "").strip():
        out.append("venue")
    if not (rec.get("externalIds") or {}).get("DOI"):
        out.append("doi")
    return out


def record_key(rec: dict[str, Any]) -> str | None:
    """The stable id a record is filed and deduplicated under: the S2 id, else
    the OpenAlex id, else the arXiv id, else the DOI."""
    ext = rec.get("externalIds") or {}
    if rec.get("paperId"):
        return rec["paperId"]
    if ext.get("OpenAlex"):
        return "oa-" + ext["OpenAlex"]
    if ext.get("ArXiv"):
        return "arxiv-" + ext["ArXiv"]
    if ext.get("DOI"):
        return "doi-" + ext["DOI"]
    return None


def dedupe_key(rec: dict[str, Any]) -> str:
    """Identity across indexes: DOI, else arXiv id, else the folded title."""
    ext = rec.get("externalIds") or {}
    if ext.get("DOI"):
        return "doi:" + norm_doi(ext["DOI"])  # type: ignore[operator]
    if ext.get("ArXiv"):
        return "arxiv:" + norm_arxiv(ext["ArXiv"])  # type: ignore[operator]
    return "title:" + normalised_title(rec.get("title") or "")


def finish(rec: dict[str, Any]) -> dict[str, Any]:
    rec["externalIds"] = {k: v for k, v in (rec.get("externalIds") or {}).items() if v}
    rec["key"] = record_key(rec)
    rec["missing"] = missing_fields(rec)
    return rec


def s2_pdf_url(paper: dict[str, Any]) -> str | None:
    """openAccessPdf.url comes back as "" even when status is GREEN or GOLD
    (ticket 09 6). An empty string is absence, not a link."""
    oa = paper.get("openAccessPdf")
    if not isinstance(oa, dict):
        return None
    url = (oa.get("url") or "").strip()
    return url or None


def s2_record(paper: dict[str, Any]) -> dict[str, Any]:
    ext = dict(paper.get("externalIds") or {})
    return finish({
        "paperId": paper.get("paperId"),
        "title": paper.get("title"),
        "year": paper.get("year"),
        "venue": paper.get("venue") or None,
        "authors": [a.get("name") for a in (paper.get("authors") or []) if a.get("name")],
        "abstract": paper.get("abstract") or None,
        "externalIds": {"DOI": ext.get("DOI"), "ArXiv": ext.get("ArXiv"), "CorpusId": ext.get("CorpusId")},
        "citationCount": paper.get("citationCount"),
        "referenceCount": paper.get("referenceCount"),
        "influentialCitationCount": paper.get("influentialCitationCount"),
        "publicationTypes": paper.get("publicationTypes") or [],
        "fieldsOfStudy": paper.get("fieldsOfStudy") or [],
        "pdfUrl": s2_pdf_url(paper),
        "source": "s2",
        "sources": ["s2"],
    })


def oa_abstract(inverted: dict[str, list[int]] | None) -> str | None:
    """OpenAlex ships abstracts as {word: [positions]}. Put the words back."""
    if not isinstance(inverted, dict) or not inverted:
        return None
    slots: dict[int, str] = {}
    for word, positions in inverted.items():
        for p in positions or []:
            if isinstance(p, int):
                slots[p] = word
    return " ".join(slots[i] for i in sorted(slots)) or None


def oa_record(work: dict[str, Any]) -> dict[str, Any]:
    ids = work.get("ids") or {}
    arxiv = None
    pdf = None
    venue = None
    for loc in [work.get("primary_location")] + list(work.get("locations") or []):
        if not isinstance(loc, dict):
            continue
        for u in (loc.get("landing_page_url"), loc.get("pdf_url")):
            if u and "arxiv.org" in u and not arxiv:
                arxiv = norm_arxiv(u)
        if not pdf and loc.get("pdf_url"):
            pdf = loc["pdf_url"]
        src = loc.get("source") or {}
        if not venue and isinstance(src, dict) and src.get("display_name") and src.get("type") != "repository":
            venue = src["display_name"]
    if not pdf:
        best = work.get("best_oa_location") or {}
        pdf = best.get("pdf_url") if isinstance(best, dict) else None
    return finish({
        "paperId": None,
        "title": work.get("title") or work.get("display_name"),
        "year": work.get("publication_year"),
        "venue": venue,
        "authors": [
            (a.get("author") or {}).get("display_name")
            for a in (work.get("authorships") or []) if (a.get("author") or {}).get("display_name")
        ],
        "abstract": oa_abstract(work.get("abstract_inverted_index")),
        "externalIds": {
            "DOI": norm_doi(work.get("doi") or ids.get("doi")),
            "ArXiv": arxiv,
            "OpenAlex": norm_openalex(work.get("id") or ids.get("openalex")),
        },
        "citationCount": work.get("cited_by_count"),
        "referenceCount": len(work.get("referenced_works") or []),
        "influentialCitationCount": None,
        "publicationTypes": [work.get("type")] if work.get("type") else [],
        "fieldsOfStudy": [],
        "pdfUrl": pdf,
        "referencedWorks": [norm_openalex(w) for w in (work.get("referenced_works") or []) if norm_openalex(w)],
        "source": "openalex",
        "sources": ["openalex"],
    })


def _cr_date(parts: Any) -> str | None:
    try:
        p = parts["date-parts"][0]
        return "-".join(f"{int(x):02d}" if i else str(int(x)) for i, x in enumerate(p))
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def cr_record(item: dict[str, Any]) -> dict[str, Any]:
    dates = {
        "issued": _cr_date(item.get("issued")),
        "created": _cr_date(item.get("created")),
        "published_online": _cr_date(item.get("published-online")),
        "published_print": _cr_date(item.get("published-print")),
    }
    year = None
    for d in (dates["issued"], dates["published_print"], dates["published_online"], dates["created"]):
        if d:
            year = int(d[:4])
            break
    titles = item.get("title") or []
    container = item.get("container-title") or []
    abstract = re.sub(r"<[^>]+>", " ", item.get("abstract") or "").strip() or None
    return finish({
        "paperId": None,
        "title": titles[0] if titles else None,
        "year": year,
        "venue": container[0] if container else None,
        "authors": [
            " ".join(x for x in (a.get("given"), a.get("family")) if x)
            for a in (item.get("author") or []) if a.get("family") or a.get("given")
        ],
        "abstract": abstract,
        "externalIds": {"DOI": norm_doi(item.get("DOI"))},
        "citationCount": item.get("is-referenced-by-count"),
        "referenceCount": None,
        "influentialCitationCount": None,
        "publicationTypes": [],
        "fieldsOfStudy": [],
        "pdfUrl": None,
        "dates": dates,
        "source": "crossref",
        "sources": ["crossref"],
    })


ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"


def arxiv_records(xml_text: str) -> dict[str, Any]:
    """Parse an arXiv Atom feed into records. Returns {papers, total} or error."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return err(f"malformed response from arxiv: {exc}", 1, 200)
    total_el = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    papers = []
    for entry in root.findall(ATOM + "entry"):
        raw_id = (entry.findtext(ATOM + "id") or "").strip()
        arxiv_id = norm_arxiv(raw_id)
        if not arxiv_id:
            continue
        pdf = None
        for link in entry.findall(ATOM + "link"):
            if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                pdf = link.get("href")
        published = (entry.findtext(ATOM + "published") or "")[:10]
        cats = [c.get("term") for c in entry.findall(ATOM + "category") if c.get("term")]
        primary = entry.find(ARXIV_NS + "primary_category")
        journal = (entry.findtext(ARXIV_NS + "journal_ref") or "").strip()
        papers.append(finish({
            "paperId": None,
            "title": " ".join((entry.findtext(ATOM + "title") or "").split()) or None,
            "year": int(published[:4]) if published[:4].isdigit() else None,
            "venue": journal or None,
            "authors": [
                " ".join((a.findtext(ATOM + "name") or "").split())
                for a in entry.findall(ATOM + "author") if (a.findtext(ATOM + "name") or "").strip()
            ],
            "abstract": " ".join((entry.findtext(ATOM + "summary") or "").split()) or None,
            "externalIds": {
                "ArXiv": arxiv_id,
                "DOI": norm_doi(entry.findtext(ARXIV_NS + "doi")),
            },
            "citationCount": None,
            "referenceCount": None,
            "influentialCitationCount": None,
            "publicationTypes": [],
            "fieldsOfStudy": cats,
            "primaryCategory": primary.get("term") if primary is not None else None,
            "published": published or None,
            "pdfUrl": pdf,
            "source": "arxiv",
            "sources": ["arxiv"],
        }))
    try:
        total = int((total_el.text or "0").strip()) if total_el is not None else None
    except ValueError:
        total = None
    return {"papers": papers, "total": total}


def merge_records(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """One paper seen by two indexes. Keep every id, note both sources, and
    fill blanks from the second without overwriting the first's values."""
    out = dict(a)
    for k, v in b.items():
        if k in ("sources", "externalIds", "missing", "key", "source"):
            continue
        if out.get(k) in (None, [], "") and v not in (None, [], ""):
            out[k] = v
    out["externalIds"] = {**(b.get("externalIds") or {}), **(a.get("externalIds") or {})}
    out["sources"] = sorted(set(a.get("sources") or []) | set(b.get("sources") or []))
    # The two indexes count citations differently; keep the second's figure too.
    for src, rec in ((a.get("source"), a), (b.get("source"), b)):
        if src and rec.get("citationCount") is not None:
            out.setdefault("citationCounts", {})[src] = rec["citationCount"]
    return finish(out)


def merge_lists(*lists: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge several lists of records into one, first-seen order, deduplicated
    by DOI, then arXiv id, then folded title."""
    seen: dict[str, int] = {}
    out: list[dict[str, Any]] = []
    for records in lists:
        for rec in records:
            k = dedupe_key(rec)
            if k in seen:
                out[seen[k]] = merge_records(out[seen[k]], rec)
            else:
                seen[k] = len(out)
                out.append(rec)
    return out


# --------------------------------------------------------------------------
# paper records on disk


def record_path(key: str) -> str | None:
    """Confined to research/.papers/ by this function, not by the write-scope
    guard: a PreToolUse hook on Write/Edit does not see a script's filesystem
    access."""
    base = records_dir()
    if not base or not key:
        return None
    safe = "".join(c for c in key if c.isalnum() or c in "-_.")
    if not safe:
        return None
    path = os.path.abspath(os.path.join(base, safe + ".json"))
    if os.path.commonpath([path, base]) != base:
        return None
    return path


def save_record(record: dict[str, Any]) -> bool:
    path = record_path(record.get("key") or "")
    if not path:
        return False
    try:
        write_atomic(path, record)
        return True
    except OSError:
        return False


def save_all(records: list[dict[str, Any]]) -> int:
    return sum(1 for r in records if save_record(r))


# --------------------------------------------------------------------------
# resolver: Semantic Scholar


def s2_get(path: str, params: dict[str, Any] | None = None, body: Any = None,
           method: str = "GET", use_cache: bool = True, attempts: int = ATTEMPTS) -> Any:
    key = s2_key()
    return fetch_json("s2", method, S2_BASE + path, params=params, body=body,
                      headers={"x-api-key": key} if key else {}, keyed=bool(key),
                      use_cache=use_cache, attempts=attempts)


def s2_search(query: str, limit: int = 20) -> dict[str, Any]:
    payload = s2_get("/paper/search", {"query": query, "limit": limit, "fields": S2_FIELDS})
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if isinstance(payload, dict) and "data" not in payload and payload.get("total") == 0:
        # Zero hits come back as {"total": 0, "offset": 0} with no data array at
        # all (measured 2026-09-15). That is an answer, not a malformed one.
        payload = {**payload, "data": []}
    if not isinstance(payload, dict) or "data" not in payload:
        return err("unexpected response shape from s2: no data array", 1, 200)
    return split_search(payload, query, limit)


def split_search(payload: dict[str, Any], query: str, limit: int) -> dict[str, Any]:
    rows = payload.get("data") or []
    papers = [s2_record(r) for r in rows if isinstance(r, dict) and r.get("paperId")]
    nxt = payload.get("next")
    return {
        "query": query, "limit": limit, "papers": papers,
        "resolved_count": len(papers), "malformed_count": len(rows) - len(papers),
        "rows_returned": len(rows), "total": payload.get("total"),
        "next": nxt, "truncated": nxt is not None,
    }


def batch_papers(ids: list[str]) -> dict[str, Any]:
    """S2 metadata for many ids in one call. Used by `verify` to resolve an id,
    and available on its own."""
    ids = [str(i).strip() for i in (ids or []) if str(i).strip()]
    if not ids:
        return err("ids is required")
    if len(ids) > BATCH_MAX:
        return err(f"at most {BATCH_MAX} ids per call, got {len(ids)}")
    payload = s2_get("/paper/batch", {"fields": S2_FIELDS}, {"ids": ids}, method="POST")
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if not isinstance(payload, list):
        return err("unexpected response shape from s2: not a list", 1, 200)
    papers, unresolvable_ids = [], []
    for asked, row in zip(ids, payload):
        if isinstance(row, dict) and row.get("paperId"):
            papers.append(s2_record(row))
        else:
            unresolvable_ids.append(asked)
    # POST /paper/batch does not collapse aliases (ticket 09 5): an arXiv id and
    # its own S2 id come back as two rows for one paper.
    seen, deduped, aliases = set(), [], 0
    for rec in papers:
        if rec["paperId"] in seen:
            aliases += 1
            continue
        seen.add(rec["paperId"])
        deduped.append(rec)
    return {
        "papers": deduped, "unresolvable_ids": unresolvable_ids,
        "resolved_count": len(deduped), "unresolvable_count": len(unresolvable_ids),
        "alias_rows_collapsed": aliases, "records_written": save_all(deduped),
    }


# --------------------------------------------------------------------------
# resolver: OpenAlex


def oa_params(extra: dict[str, Any]) -> dict[str, Any]:
    p = dict(extra)
    if _env("OPENALEX_MAILTO"):
        p["mailto"] = _env("OPENALEX_MAILTO")
    if _env("OPENALEX_API_KEY"):
        p["api_key"] = _env("OPENALEX_API_KEY")
    return p


def oa_get(path: str, params: dict[str, Any], use_cache: bool = True, attempts: int = ATTEMPTS) -> Any:
    return fetch_json("openalex", "GET", OA_BASE + path, params=oa_params(params),
                      use_cache=use_cache, attempts=attempts)


def oa_list(payload: Any, what: str) -> dict[str, Any]:
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if not isinstance(payload, dict) or "results" not in payload:
        return err(f"unexpected response shape from openalex: no results ({what})", 1, 200)
    rows = payload.get("results") or []
    papers = [oa_record(w) for w in rows if isinstance(w, dict) and w.get("id")]
    meta = payload.get("meta") or {}
    return {
        "papers": papers, "resolved_count": len(papers),
        "malformed_count": len(rows) - len(papers), "rows_returned": len(rows),
        "total": meta.get("count"),
    }


def oa_search(query: str, limit: int = 20) -> dict[str, Any]:
    query = (query or "").strip()
    if not query:
        return err("query is required")
    limit = max(1, min(int(limit or 20), SEARCH_MAX))
    out = oa_list(oa_get("/works", {"search": query, "per-page": limit, "select": OA_FIELDS}), "search")
    if "error" not in out:
        out.update({"query": query, "limit": limit, "truncated": (out.get("total") or 0) > limit})
    return out


def oa_work_path(ident: str) -> str | None:
    """An OpenAlex work by W id or DOI."""
    ident = (ident or "").strip()
    w = norm_openalex(ident) if not ident.lower().startswith("10.") else None
    if w:
        return f"/works/{w}"
    doi = norm_doi(ident)
    if doi and doi.startswith("10."):
        return "/works/https://doi.org/" + urllib.parse.quote(doi, safe="")
    return None


def oa_work(ident: str) -> dict[str, Any]:
    """One work: cited_by_count, referenced_works and the rest of the record."""
    path = oa_work_path(ident)
    if not path:
        return err("openalex work needs a W id or a DOI")
    payload = oa_get(path, {"select": OA_FIELDS})
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if not isinstance(payload, dict) or not payload.get("id"):
        return err("unexpected response shape from openalex: no work id", 1, 200)
    rec = oa_record(payload)
    return {"paper": rec, "cited_by_count": rec.get("citationCount"),
            "referenced_works": rec.get("referencedWorks") or [], "records_written": save_all([rec])}


def oa_by_ids(wids: list[str]) -> dict[str, Any]:
    """Records for many W ids, OA_FILTER_MAX per request."""
    papers: list[dict[str, Any]] = []
    for i in range(0, len(wids), OA_FILTER_MAX):
        chunk = wids[i:i + OA_FILTER_MAX]
        out = oa_list(oa_get("/works", {
            "filter": "openalex:" + "|".join(chunk), "per-page": len(chunk), "select": OA_FIELDS,
        }), "by ids")
        if "error" in out:
            return out
        papers.extend(out["papers"])
    return {"papers": papers, "resolved_count": len(papers), "asked": len(wids)}


def oa_referenced(ident: str) -> dict[str, Any]:
    """The works a work cites: one hop backward on OpenAlex."""
    work = oa_work(ident)
    if "error" in work:
        return work
    wids = work["referenced_works"]
    if not wids:
        return {"seed": work["paper"]["externalIds"].get("OpenAlex"), "papers": [], "resolved_count": 0,
                "asked": 0, "records_written": 0}
    out = oa_by_ids(wids)
    if "error" in out:
        return out
    out["seed"] = work["paper"]["externalIds"].get("OpenAlex")
    out["records_written"] = save_all(out["papers"])
    return out


def oa_cited_by(ident: str, limit: int = 50) -> dict[str, Any]:
    """The works citing a work: one hop forward on OpenAlex, most-cited first."""
    w = norm_openalex(ident)
    if not w:
        found = oa_work(ident)
        if "error" in found:
            return found
        w = found["paper"]["externalIds"].get("OpenAlex")
    limit = max(1, min(int(limit or 50), 200))
    out = oa_list(oa_get("/works", {
        "filter": f"cites:{w}", "per-page": limit, "select": OA_FIELDS, "sort": "cited_by_count:desc",
    }), "cited-by")
    if "error" in out:
        return out
    out.update({"seed": w, "limit": limit, "truncated": (out.get("total") or 0) > limit,
                "records_written": save_all(out["papers"])})
    return out


# --------------------------------------------------------------------------
# resolver: Crossref


def cr_params(extra: dict[str, Any]) -> dict[str, Any]:
    p = dict(extra)
    if _env("CROSSREF_MAILTO"):
        p["mailto"] = _env("CROSSREF_MAILTO")
    return p


def cr_get(path: str, params: dict[str, Any], use_cache: bool = True, attempts: int = ATTEMPTS) -> Any:
    return fetch_json("crossref", "GET", CR_BASE + path, params=cr_params(params),
                      use_cache=use_cache, attempts=attempts)


def cr_doi(doi: str) -> dict[str, Any]:
    """One DOI: title, is-referenced-by-count, and the dates Crossref holds."""
    d = norm_doi(doi)
    if not d or not d.startswith("10."):
        return err("crossref doi needs a DOI")
    payload = cr_get("/works/" + urllib.parse.quote(d, safe=""), {})
    if isinstance(payload, dict) and "error" in payload:
        return payload
    msg = payload.get("message") if isinstance(payload, dict) else None
    if not isinstance(msg, dict) or not msg.get("DOI"):
        return err("unexpected response shape from crossref: no message.DOI", 1, 200)
    rec = cr_record(msg)
    return {"paper": rec, "is_referenced_by_count": rec.get("citationCount"),
            "dates": rec.get("dates"), "records_written": save_all([rec])}


def cr_search(title: str, rows: int = 5) -> dict[str, Any]:
    """Bibliographic search, for confirming a title when no index has it."""
    title = (title or "").strip()
    if not title:
        return err("title is required")
    rows = max(1, min(int(rows or 5), 50))
    payload = cr_get("/works", {"query.bibliographic": title, "rows": rows, "select": CR_FIELDS})
    if isinstance(payload, dict) and "error" in payload:
        return payload
    msg = payload.get("message") if isinstance(payload, dict) else None
    if not isinstance(msg, dict) or "items" not in msg:
        return err("unexpected response shape from crossref: no message.items", 1, 200)
    items = msg.get("items") or []
    papers = [cr_record(i) for i in items if isinstance(i, dict) and i.get("DOI")]
    return {"query": title, "papers": papers, "resolved_count": len(papers),
            "rows_returned": len(items), "total": msg.get("total-results")}


# --------------------------------------------------------------------------
# resolver: arXiv


def arxiv_query(query: str | None, category: str | None, date_from: str | None, date_to: str | None) -> str:
    """arXiv's search_query string from the parts a caller gives."""
    parts = []
    if query and query.strip():
        q = query.strip()
        parts.append(f'all:"{q}"' if " " in q and not q.startswith('"') else f"all:{q}")
    if category:
        parts.append(f"cat:{category.strip()}")
    if date_from or date_to:
        lo = (date_from or "1991-01-01").replace("-", "") + "0000"
        hi = (date_to or today()).replace("-", "") + "2359"
        parts.append(f"submittedDate:[{lo} TO {hi}]")
    return " AND ".join(parts)


def arxiv_search(query: str | None = None, category: str | None = None,
                 date_from: str | None = None, date_to: str | None = None, limit: int = 20) -> dict[str, Any]:
    """Category and date-window search. Abstracts and PDF links on every row.
    Paced to one call per 3 seconds across processes."""
    sq = arxiv_query(query, category, date_from, date_to)
    if not sq:
        return err("arxiv search needs a query, a --cat, or a date window")
    limit = max(1, min(int(limit or 20), SEARCH_MAX))
    params = {
        "search_query": sq, "start": 0, "max_results": limit,
        "sortBy": "relevance" if query else "submittedDate", "sortOrder": "descending",
    }
    text, problem = fetch("arxiv", "GET", ARXIV_BASE, params=params)
    if problem:
        return problem
    out = arxiv_records(text or "")
    if "error" in out:
        return out
    out.update({"query": sq, "limit": limit, "rows_returned": len(out["papers"]),
                "resolved_count": len(out["papers"]),
                "truncated": (out.get("total") or 0) > limit,
                "records_written": save_all(out["papers"])})
    return out


# --------------------------------------------------------------------------
# verbs: search, verify


def search(query: str, limit: int = 20, index: str = "all") -> dict[str, Any]:
    """Papers by keyword, merged across Semantic Scholar and OpenAlex. Either
    index failing is reported under `indexes` and `degraded`; the call still
    returns whatever the other found. `--index arxiv` searches arXiv alone,
    since its 3-second pacing should not slow every search."""
    query = (query or "").strip()
    if not query:
        return err("query is required")
    limit = max(1, min(int(limit or 20), SEARCH_MAX))
    index = (index or "all").lower()
    if index not in ("all", "s2", "openalex", "arxiv"):
        return err("--index must be all, s2, openalex or arxiv")

    lists: list[list[dict[str, Any]]] = []
    indexes: dict[str, Any] = {}
    degraded: list[str] = []
    plan = {"all": ("s2", "openalex"), "s2": ("s2",), "openalex": ("openalex",), "arxiv": ("arxiv",)}[index]
    for name in plan:
        got = {"s2": s2_search, "openalex": oa_search}.get(name, lambda q, l: arxiv_search(q, limit=l))(query, limit)
        if "error" in got:
            indexes[name] = {"rows": 0, "error": got["error"], "status": got.get("status")}
            degraded.append(name)
            continue
        indexes[name] = {"rows": got["rows_returned"], "total": got.get("total"), "truncated": got.get("truncated")}
        lists.append(got["papers"])
    papers = merge_lists(*lists)
    if not lists:
        # every index asked failed: still one shape, so a caller can read it
        return {"query": query, "limit": limit, "index": index, "papers": [], "resolved_count": 0,
                "indexes": indexes, "degraded": degraded, "records_written": 0,
                "error": "every index failed: " + "; ".join(f"{k}: {v['error']}" for k, v in indexes.items())}
    return {
        "query": query, "limit": limit, "index": index, "papers": papers,
        "resolved_count": len(papers), "in_both": sum(1 for p in papers if len(p.get("sources") or []) > 1),
        "indexes": indexes, "degraded": degraded, "records_written": save_all(papers),
    }


def normalised_title(text: str) -> str:
    """A title folded for comparison: case, punctuation and spacing dropped."""
    folded = unicodedata.normalize("NFKD", text or "").lower().replace("&", " and ")
    kept = [c if (c.isalnum() or c.isspace()) else " " for c in folded]
    return " ".join("".join(kept).split())


def title_match(asked: str, found: str) -> str:
    """How `found` matches `asked`: exact, prefix, substring, or none."""
    a, f = normalised_title(asked), normalised_title(found)
    if not a or not f:
        return "none"
    if a == f:
        return "exact"
    if a.startswith(f) or f.startswith(a):
        return "prefix"
    shorter = a if len(a) <= len(f) else f
    if (a in f or f in a) and len(shorter.split()) >= 4:
        return "substring"
    return "none"


# Only an exact match, after folding, certifies a paper. Prefix and substring
# were resolving until 2026-09-14, when an adversarial review showed what they
# do: a remembered title handed a real identifier for a different paper.
RESOLVING_MATCHES = ("exact",)
NEAR_MATCHES = ("prefix", "substring")
VERIFY_ORDER = ("s2", "openalex", "crossref")


def _id_matches(asked: str, rec: dict[str, Any]) -> bool:
    a = (asked or "").strip()
    if not a:
        return False
    if a == rec.get("paperId"):
        return True
    ext = rec.get("externalIds") or {}
    low = a.lower()
    for prefix, key in (("arxiv:", "ArXiv"), ("doi:", "DOI"), ("corpusid:", "CorpusId")):
        if low.startswith(prefix):
            return str(ext.get(key) or "").lower() == low[len(prefix):]
    return any(str(v).lower() == low for v in ext.values())


def _best(asked: str, papers: list[dict[str, Any]]) -> tuple[str, dict[str, Any] | None]:
    order = RESOLVING_MATCHES + NEAR_MATCHES
    ranked = sorted(
        ((title_match(asked, p.get("title") or ""), p) for p in papers),
        key=lambda pair: order.index(pair[0]) if pair[0] in order else 9,
    )
    return ranked[0] if ranked else ("none", None)


def _ids_of(rec: dict[str, Any] | None) -> dict[str, Any]:
    if not rec:
        return {}
    out = {k: v for k, v in (rec.get("externalIds") or {}).items() if v}
    if rec.get("paperId"):
        out["S2"] = rec["paperId"]
    return out


def verify_title(asked: str, limit: int) -> dict[str, Any]:
    """S2, then OpenAlex, then Crossref, stopping at the first exact match.
    A near match from any of them is a candidate, and never resolved."""
    checked: list[str] = []
    errors: dict[str, str] = {}
    candidate: dict[str, Any] | None = None
    closest: dict[str, Any] | None = None
    rows = 0
    for source in VERIFY_ORDER:
        got = {"s2": s2_search, "openalex": oa_search, "crossref": cr_search}[source](asked, limit)
        if "error" in got:
            errors[source] = got["error"]
            continue
        checked.append(source)
        rows += got["rows_returned"]
        kind, best = _best(asked, got["papers"])
        if kind in RESOLVING_MATCHES and best:
            save_all([best])
            return {
                "query": asked, "kind": "title", "resolved": True, "match": "exact", "source": source,
                "paperId": best.get("paperId"), "ids": _ids_of(best), "title": best.get("title"),
                "year": best.get("year"), "candidate": None, "checked": checked, "errors": errors,
            }
        if kind in NEAR_MATCHES and best and candidate is None:
            candidate = {"kind": kind, "source": source, "title": best.get("title"),
                         "year": best.get("year"), "ids": _ids_of(best)}
        if closest is None and best:
            closest = {"source": source, "title": best.get("title"), "ids": _ids_of(best)}
    if candidate:
        # Deliberately NOT resolved: a near match is the dangerous case, not the
        # safe one. Name it so the caller can correct a typo, with the id so the
        # correction is one step - but the id does not go on the card until a
        # human or a later exact check says so.
        return {
            "query": asked, "kind": "title", "resolved": False, "match": "candidate", "source": None,
            "paperId": None, "ids": {}, "title": None, "year": None, "candidate": candidate,
            "note": f"{candidate['kind']} match only, NOT the same paper unless you say so: "
                    f"{candidate['title']} {candidate['ids']}",
            "checked": checked, "errors": errors,
        }
    return {
        "query": asked, "kind": "title", "resolved": False, "match": "none", "source": None,
        "paperId": None, "ids": {}, "title": None, "year": None, "candidate": None,
        "note": f"no title match in {rows} rows across {', '.join(checked) or 'no index'}"
                + (f"; closest: {closest['title']} ({closest['source']})" if closest else ""),
        "checked": checked, "errors": errors,
    }


def verify_ids(ids: list[str]) -> list[dict[str, Any]]:
    """Ids through S2 batch; a DOI S2 does not know goes to Crossref, an
    OpenAlex id to OpenAlex."""
    results: list[dict[str, Any]] = []
    got = batch_papers(ids)
    s2_papers = got.get("papers", []) if "error" not in got else []
    s2_error = got.get("error") if "error" in got else None
    for asked in ids:
        rec = next((r for r in s2_papers if _id_matches(asked, r)), None)
        checked = ["s2"] if not s2_error else []
        errors = {"s2": s2_error} if s2_error else {}
        if rec is None:
            low = asked.lower()
            if low.startswith("doi:") or low.startswith("10."):
                cr = cr_doi(asked.split(":", 1)[-1] if low.startswith("doi:") else asked)
                if "error" in cr:
                    errors["crossref"] = cr["error"]
                else:
                    checked.append("crossref")
                    rec = cr["paper"]
            elif norm_openalex(asked) and low.lstrip("openalex:").startswith("w"):
                oa = oa_work(asked)
                if "error" in oa:
                    errors["openalex"] = oa["error"]
                else:
                    checked.append("openalex")
                    rec = oa["paper"]
        results.append({
            "query": asked, "kind": "id", "resolved": rec is not None,
            "match": "id" if rec else "none", "source": rec.get("source") if rec else None,
            "paperId": rec.get("paperId") if rec else None, "ids": _ids_of(rec),
            "title": rec.get("title") if rec else None, "year": rec.get("year") if rec else None,
            "candidate": None, "checked": checked, "errors": errors,
            **({} if rec else {"note": "no record for this id"}),
        })
    return results


def verify(titles: list[str], ids: list[str], limit: int = 10) -> dict[str, Any]:
    """Resolve papers named in a written artifact against the record.

    Nothing is dropped: an unresolved row comes back marked, with the closest
    thing the indexes did return, so a reader sees exactly where memory outran
    the record. Charges nothing and has no budget: the papers were already
    named, and a ceiling that refused to check them would be the wrong shape.
    """
    titles = [t.strip() for t in (titles or []) if t and t.strip()]
    ids = [i.strip() for i in (ids or []) if i and i.strip()]
    if not titles and not ids:
        return err("verify needs at least one --title or --id")
    results: list[dict[str, Any]] = []
    if ids:
        results.extend(verify_ids(ids))
    for asked in titles:
        results.append(verify_title(asked, limit))
    resolved = sum(1 for r in results if r["resolved"])
    candidates = sum(1 for r in results if r["match"] == "candidate")
    return {
        "results": results, "resolved_count": resolved, "candidate_count": candidates,
        "unresolved_count": len(results) - resolved, "checked": len(results),
    }


# --------------------------------------------------------------------------
# verbs: health, status


def health() -> dict[str, Any]:
    """Keys and paths, without spending a request or inferring it from a failure."""
    return {
        "script": "snowball.py", "version": VERSION,
        "key_present": bool(s2_key()),  # kept: /setup and /scout read this name
        "keys": keys_present(), "cache_dir": cache_dir(),
        "project_dir": project_dir(), "records_dir": records_dir(),
    }


# One probe per source, the one-line test from docs/APIS.md. `needs` names
# the env vars that would move the source from connected-no-key to connected.
PROBES = [
    {"name": "semantic-scholar", "resolver": "s2", "needs": ["S2_API_KEY"],
     "where": "https://www.semanticscholar.org/product/api#api-key-form",
     "why": "the primary index stops rate-limiting; neighborhood gets citing sentences"},
    {"name": "openalex", "resolver": "openalex", "needs": ["OPENALEX_MAILTO"],
     "where": "https://openalex.org (any email; the key is optional)",
     "why": "polite pool on the index that carries the load when S2 throttles"},
    {"name": "crossref", "resolver": "crossref", "needs": ["CROSSREF_MAILTO"],
     "where": "nothing to sign up for; set any email",
     "why": "polite pool on the DOI record"},
    {"name": "arxiv", "resolver": "arxiv", "needs": [],
     "where": "no key exists", "why": ""},
    {"name": "unpaywall", "resolver": "unpaywall", "needs": ["UNPAYWALL_EMAIL"],
     "where": "https://unpaywall.org/products/api (an email is the signup)",
     "why": "open-access PDF locations by DOI"},
    {"name": "huggingface", "resolver": "huggingface", "needs": ["HF_TOKEN"],
     "where": "https://huggingface.co/settings/tokens (a read token)",
     "why": "daily papers and which models cite an arXiv id, at the keyed rate"},
    {"name": "zotero", "resolver": "zotero", "needs": ["ZOTERO_API_KEY", "ZOTERO_USER_ID"],
     "where": "https://www.zotero.org/settings/keys (key and user id are both there)",
     "why": "which of the papers found are already in your library"},
]


def probe_request(name: str) -> tuple[str, dict[str, str]]:
    """The URL and headers of one source's one-line test, given the env."""
    k = keys_present()
    if name == "semantic-scholar":
        return (S2_BASE + "/paper/search?query=xbd&limit=1", {"x-api-key": s2_key()} if k["S2_API_KEY"] else {})
    if name == "openalex":
        return (OA_BASE + "/works?" + urllib.parse.urlencode(oa_params({"search": "xbd", "per-page": 1})), {})
    if name == "crossref":
        return (CR_BASE + "/works/10.3390/rs12223808?" + urllib.parse.urlencode(cr_params({})), {})
    if name == "arxiv":
        return (ARXIV_BASE + "?search_query=all:xbd&max_results=1", {})
    if name == "unpaywall":
        q = {"email": _env("UNPAYWALL_EMAIL")} if k["UNPAYWALL_EMAIL"] else {}
        return (UNPAYWALL_BASE + "/10.1184/R1/8135576.V1?" + urllib.parse.urlencode(q), {})
    if name == "huggingface":
        return (HF_BASE + "/papers/search?q=xbd", {"Authorization": "Bearer " + _env("HF_TOKEN")} if k["HF_TOKEN"] else {})
    if name == "zotero":
        if k["ZOTERO_API_KEY"] and k["ZOTERO_USER_ID"]:
            return (f"{ZOTERO_BASE}/users/{urllib.parse.quote(_env('ZOTERO_USER_ID'))}/items?limit=1",
                    {"Zotero-API-Key": _env("ZOTERO_API_KEY")})
        return (ZOTERO_BASE + "/", {})
    raise KeyError(name)


def probe_state(http: int, keyed: bool) -> tuple[str, str]:
    """(state, note) from an HTTP status and whether a credential was sent.

    Any answer is reachability. 429 is a rate limit, not an outage. 401 and
    403 with a credential mean the credential was rejected; without one they
    mean the source wants one, which is connected-no-key by definition.
    """
    if http == 0 or http >= 500:
        return "not connected", f"http {http}" if http else "no response"
    if http in (401, 403) and keyed:
        return "not connected", f"credential rejected (http {http})"
    if not keyed:
        return "connected-no-key", "" if http < 400 else f"http {http} without a key"
    return "connected", "" if http < 400 else f"http {http}"


def probe(source: dict[str, Any]) -> dict[str, Any]:
    k = keys_present()
    keyed = bool(source["needs"]) and all(k.get(n) for n in source["needs"])
    if not source["needs"]:
        keyed = True  # a source with no credential is either connected or not
    url, headers = probe_request(source["name"])
    hdrs = {"User-Agent": user_agent(), **headers}
    t0 = time.time()
    http, _ = http_fetch("GET", url, None, hdrs)
    state, note = probe_state(http, keyed)
    missing = [n for n in source["needs"] if not k.get(n)]
    return {
        "name": source["name"], "state": state, "http": http, "ms": int((time.time() - t0) * 1000),
        "keyed": keyed, "missing": missing, "note": note, "test": "GET " + url.split("?")[0],
        "line": f"- {source['name']}: {state} ({today()})"
                + (f" — set {' and '.join(missing)}" if missing else "") + (f" — {note}" if note else ""),
    }


def suggest(results: list[dict[str, Any]], n: int = 3) -> list[dict[str, Any]]:
    """The first `n` sources, in PROBES order, that are missing a credential."""
    out = []
    by_name = {p["name"]: p for p in PROBES}
    for r in results:
        if r["missing"]:
            src = by_name[r["name"]]
            out.append({"env": r["missing"], "source": r["name"], "where": src["where"], "why": src["why"]})
        if len(out) == n:
            break
    return out


def status() -> dict[str, Any]:
    """Live. Never reads the cache, one attempt per source, all seven at once.
    A missing key is a state, not an error: the exit code is 0 whatever comes back."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(PROBES)) as pool:
        results = list(pool.map(probe, PROBES))
    return {
        "date": today(), "version": VERSION, "sources": results,
        "connected": [r["name"] for r in results if r["state"] == "connected"],
        "connected_no_key": [r["name"] for r in results if r["state"] == "connected-no-key"],
        "not_connected": [r["name"] for r in results if r["state"] == "not connected"],
        "suggest": suggest(results),
        "lines": [r["line"] for r in results],
    }


def status_md(out: dict[str, Any]) -> str:
    lines = list(out["lines"])
    if out["suggest"]:
        lines.append("")
        lines.append("Keys that would help most, in order:")
        for s in out["suggest"]:
            lines.append(f"- {' and '.join(s['env'])} — {s['why']}. Get it: {s['where']}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# command line


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(prog="snowball.py", description="Search and citation checking over four indexes. One JSON result per call.")
    ap.add_argument("--selftest", action="store_true", help="offline checks, then exit")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("status", help="probe every source live; keys and states")
    p.add_argument("--md", action="store_true", help="print the CONNECTIONS.md lines instead of JSON")
    sub.add_parser("health", help="key presence and paths; no network")
    p = sub.add_parser("search", help="papers by keyword, S2 and OpenAlex merged")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--index", default="all", help="all | s2 | openalex | arxiv")
    p = sub.add_parser("batch", help="S2 metadata for many ids at once")
    p.add_argument("ids", nargs="+")
    p = sub.add_parser("verify", help="do these papers exist? by title or id; exact match only")
    p.add_argument("--title", action="append", default=[], help="repeatable")
    p.add_argument("--id", action="append", default=[], dest="ids", help="repeatable")
    p.add_argument("--limit", type=int, default=10, help="rows to consider per title per index; the near match that makes a candidate is often below the top five")

    p = sub.add_parser("openalex", help="OpenAlex resolver")
    oa = p.add_subparsers(dest="sub")
    q = oa.add_parser("search"); q.add_argument("query"); q.add_argument("--limit", type=int, default=20)
    q = oa.add_parser("work"); q.add_argument("ident", help="W id or DOI")
    q = oa.add_parser("refs"); q.add_argument("ident", help="W id or DOI")
    q = oa.add_parser("cited-by"); q.add_argument("ident"); q.add_argument("--limit", type=int, default=50)

    p = sub.add_parser("crossref", help="Crossref resolver")
    cr = p.add_subparsers(dest="sub")
    q = cr.add_parser("doi"); q.add_argument("doi")
    q = cr.add_parser("search"); q.add_argument("title"); q.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("arxiv", help="arXiv resolver; one call per 3 seconds")
    ax = p.add_subparsers(dest="sub")
    q = ax.add_parser("search")
    q.add_argument("query", nargs="?", default=None)
    q.add_argument("--cat", default=None, help="e.g. cs.CV")
    q.add_argument("--from", dest="date_from", default=None, help="YYYY-MM-DD")
    q.add_argument("--to", dest="date_to", default=None, help="YYYY-MM-DD")
    q.add_argument("--limit", type=int, default=20)

    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.cmd:
        ap.print_help()
        return 2

    if args.cmd == "status":
        out: Any = status()
        if args.md:
            sys.stdout.write(status_md(out) + "\n")
            return 0
    elif args.cmd == "health":
        out = health()
    elif args.cmd == "search":
        out = search(args.query, args.limit, args.index)
    elif args.cmd == "verify":
        out = verify(args.title, args.ids, args.limit)
    elif args.cmd == "batch":
        out = batch_papers(args.ids)
    elif args.cmd == "openalex":
        out = {"search": lambda: oa_search(args.query, args.limit), "work": lambda: oa_work(args.ident),
               "refs": lambda: oa_referenced(args.ident), "cited-by": lambda: oa_cited_by(args.ident, args.limit),
               }.get(args.sub or "", lambda: err("openalex needs search, work, refs or cited-by"))()
    elif args.cmd == "crossref":
        out = {"doi": lambda: cr_doi(args.doi), "search": lambda: cr_search(args.title, args.limit),
               }.get(args.sub or "", lambda: err("crossref needs doi or search"))()
    else:
        out = arxiv_search(args.query, args.cat, args.date_from, args.date_to, args.limit) \
            if args.sub == "search" else err("arxiv needs search")

    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


# --------------------------------------------------------------------------
# selftest


def selftest() -> int:  # noqa: C901 - a flat list of cases reads better than a framework
    """Offline. Parsing on captured responses from all four resolvers, the
    cache, retry, pacing arithmetic, records, merged search and its
    degradation, verification across indexes, and the status state table."""
    failures: list[str] = []
    ran: list[str] = []
    os.environ["RESEARCH_CACHE_DIR"] = tempfile.mkdtemp(prefix="snowball-cache-")
    os.environ["RESEARCH_PROJECT_DIR"] = tempfile.mkdtemp(prefix="snowball-project-")
    for name in ("S2_API_KEY", "SEMANTIC_SCHOLAR_API_KEY", "OPENALEX_MAILTO", "OPENALEX_API_KEY",
                 "CROSSREF_MAILTO", "UNPAYWALL_EMAIL", "HF_TOKEN", "ZOTERO_API_KEY", "ZOTERO_USER_ID"):
        os.environ.pop(name, None)
    # the key file must not leak in either
    globals()["KEY_FILE"] = os.path.join(os.environ["RESEARCH_CACHE_DIR"], "no-such-key")
    saved_pace = dict(PACE)
    PACE.update({k: 0.0 for k in PACE})  # no sleeping in a selftest

    def check(case: str, ok: bool, detail: str = "") -> None:
        ran.append(case)
        print(f"{'ok  ' if ok else 'FAIL'} {case}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(case)

    def s2_payload(*rows: dict[str, Any]) -> bytes:
        return json.dumps({"total": len(rows), "data": list(rows)}).encode()

    def oa_payload(*rows: dict[str, Any]) -> bytes:
        return json.dumps({"meta": {"count": len(rows)}, "results": list(rows)}).encode()

    def cr_payload(*rows: dict[str, Any]) -> bytes:
        return json.dumps({"message": {"items": list(rows), "total-results": len(rows)}}).encode()

    def route(**by_host: Any):
        """A stub that answers per host: by_host = {s2: (status, bytes) | callable, ...}."""
        def stub(method, url, body, headers):
            for host, answer in by_host.items():
                if {"s2": "semanticscholar", "oa": "openalex", "cr": "crossref", "ax": "arxiv",
                    }[host] in url:
                    return answer(method, url, body, headers) if callable(answer) else answer
            return 0, b"unrouted"
        return stub

    xbd = "Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery"
    xbd_doi = "10.1184/R1/8135576.V1"
    s2_xbd = {"paperId": "ec58b594", "title": xbd, "year": 2019, "venue": "CVPR Workshops",
              "authors": [{"name": "R. Gupta"}], "externalIds": {"DOI": xbd_doi},
              "citationCount": 400, "influentialCitationCount": 60}
    oa_xbd = {"id": "https://openalex.org/W2967473420", "doi": "https://doi.org/10.1184/r1/8135576.v1",
              "title": xbd, "publication_year": 2019, "cited_by_count": 156,
              "authorships": [{"author": {"display_name": "Ritwik Gupta"}}], "referenced_works": []}

    # 1-4. Each resolver's envelope parses, on a real captured response.
    found = split_search(_fixture("search_dmg.json"), "building damage", 5)
    check("1  the S2 search envelope parses, and truncation is reported",
          found["resolved_count"] > 0 and found["truncated"] is (found["next"] is not None))
    oa = oa_list(_fixture("openalex_search.json"), "search")
    check("2  the OpenAlex envelope parses: W id, DOI, cited_by_count, authors, abstract",
          oa["resolved_count"] == 3 and oa["papers"][0]["externalIds"]["OpenAlex"] == "W2967473420"
          and oa["papers"][0]["externalIds"]["DOI"] == "10.1184/r1/8135576.v1"
          and oa["papers"][0]["citationCount"] > 0 and oa["papers"][0]["authors"]
          and (oa["papers"][0]["abstract"] or "").lower().startswith("we present a preliminary report"),
          f"got {json.dumps(oa['papers'][0])[:300] if oa.get('papers') else oa}")
    cr = _fixture("crossref_search.json")["message"]["items"]
    rec = cr_record(cr[0])
    check("3  the Crossref item parses: DOI, year from issued, is-referenced-by-count, dates",
          rec["externalIds"]["DOI"] == "10.3390/rs12223808" and rec["year"] == 2020
          and rec["citationCount"] is not None and rec["dates"]["issued"] and rec["venue"],
          f"got {json.dumps(rec)[:300]}")
    ax = arxiv_records(_fixture_text("arxiv_search.xml"))
    check("4  the arXiv Atom feed parses: id without version, abstract, pdf link, category, date",
          ax.get("total") and len(ax["papers"]) == 3
          and re.fullmatch(r"\d{4}\.\d{4,5}", ax["papers"][0]["externalIds"]["ArXiv"])
          and ax["papers"][0]["abstract"] and (ax["papers"][0]["pdfUrl"] or "").endswith(ax["papers"][0]["externalIds"]["ArXiv"] + ("v" + ax["papers"][0]["pdfUrl"].rsplit("v", 1)[-1] if "v" in ax["papers"][0]["pdfUrl"].rsplit("/", 1)[-1] else ""))
          and ax["papers"][0]["primaryCategory"] and ax["papers"][0]["published"],
          f"got {json.dumps(ax)[:400]}")

    # 5. A row with no paperId is dropped rather than carded as a blank.
    out = split_search({"total": 2, "data": [{"paperId": "good", "title": "T", "authors": []}, {"paperId": None}]}, "q", 5)
    check("5  a row with no paperId is counted as malformed, never returned",
          out["resolved_count"] == 1 and out["malformed_count"] == 1)

    # 5b. S2's zero-hit shape has no data array at all; that is zero rows, not an error.
    with _fetch(route(s2=(200, b'{"total": 0, "offset": 0}'))):
        zero = s2_search("a query with no hits")
    check("5b a zero-hit S2 answer is zero rows, not a malformed response",
          "error" not in zero and zero["rows_returned"] == 0, f"got {zero}")

    # 6-8. The transport: non-JSON, an error status, and a shape we did not expect.
    with _fetch(route(s2=(200, b"<html>not json</html>"))):
        check("6  a non-JSON body is an error, not a crash", "error" in s2_search("q"))
    with _fetch(route(s2=(404, b'{"error":"not found"}'))):
        check("7  an error status is reported as an error", "error" in s2_search("q"))
    with _fetch(route(s2=(200, b'{"ok":true}'))):
        check("8  a response with no data array is an error", "error" in s2_search("q"))

    # 9. Retry with jitter, not a fixed throttle.
    attempts = {"n": 0}

    def flaky(method, url, body, headers):
        attempts["n"] += 1
        if attempts["n"] < 3:
            return 429, b'{"error":"too many"}'
        return 200, s2_payload({"paperId": "p", "title": "T", "authors": []})

    saved = (globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"])
    globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"] = 0.0, 0.0
    with _fetch(route(s2=flaky)):
        retried = s2_search("a query no earlier case used")
    globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"] = saved
    check("9  a 429 is retried and the call succeeds", attempts["n"] == 3 and retried.get("resolved_count") == 1,
          f"attempts={attempts['n']} out={retried.get('error') or retried.get('resolved_count')}")

    # 10-11. The cache: a repeat is served without a second request, per resolver, and expires at 30 days.
    calls = {"n": 0}

    def counting(method, url, body, headers):
        calls["n"] += 1
        return 200, s2_payload({"paperId": "p", "title": "T", "authors": []})

    with _fetch(route(s2=counting)):
        s2_search("same query")
        s2_search("same query")
    check("10 a repeated call is served from cache, under the resolver's directory",
          calls["n"] == 1 and os.path.isdir(os.path.join(cache_dir(), "s2")), f"calls={calls['n']}")
    ck = cache_key("s2", "GET", "u", None, False)
    cache_write("s2", ck, "x")
    fresh = cache_read("s2", ck, now=time.time() + 29 * DAY)
    stale = cache_read("s2", ck, now=time.time() + 31 * DAY)
    check("11 a cache entry is served at 29 days and not at 31", fresh == "x" and stale is None)

    # 12. Pacing arithmetic: the wait is the gap minus the time already elapsed, never negative.
    check("12 pacing waits the remainder of the gap and never a negative time",
          abs(pace_wait(100.0, 100.4, 1.0) - 0.6) < 1e-9 and pace_wait(100.0, 105.0, 3.0) == 0.0
          and abs(pace_wait(100.0, 101.0, 3.0) - 2.0) < 1e-9)

    # 13. Records are written by the script, not carried through a model, for every source.
    with tempfile.TemporaryDirectory() as tmp:
        with _environ(RESEARCH_PROJECT_DIR=tmp, RESEARCH_CACHE_DIR=os.path.join(tmp, "c")):
            with _fetch(route(s2=(200, s2_payload({"paperId": "rec1", "title": "T", "authors": [{"name": "A"}]})),
                              oa=(200, oa_payload({"id": "https://openalex.org/W1", "title": "U", "doi": None,
                                                   "authorships": [], "referenced_works": []})))):
                wrote = search("q")
            on_disk = sorted(os.listdir(os.path.join(tmp, "research", ".papers")))
    check("13 every returned paper lands in research/.papers/, keyed by S2 id or oa- id",
          wrote["records_written"] == 2 and on_disk == ["oa-W1.json", "rec1.json"],
          f"written={wrote.get('records_written')} on_disk={on_disk}")

    # 14. A missing field is marked, never inferred.
    rec = s2_record({"paperId": "x", "title": "T", "authors": [], "abstract": None})
    check("14 an absent abstract is marked missing", "abstract" in rec["missing"] and rec["abstract"] is None)

    # 15-16. Merged search: one paper in both indexes is one row, and losing S2 is a degradation, not a failure.
    with _fetch(route(s2=(200, s2_payload(s2_xbd)), oa=(200, oa_payload(oa_xbd)))):
        both = search("xbd merged")
    check("15 a paper both indexes return is one row, marked in both, with both ids",
          both["resolved_count"] == 1 and both["in_both"] == 1
          and both["papers"][0]["sources"] == ["openalex", "s2"]
          and both["papers"][0]["externalIds"]["OpenAlex"] == "W2967473420"
          and both["papers"][0]["paperId"] == "ec58b594"
          and both["papers"][0]["citationCounts"] == {"s2": 400, "openalex": 156},
          f"got {json.dumps(both)[:400]}")
    with _fetch(route(s2=(429, b'{"error":"too many"}'), oa=(200, oa_payload(oa_xbd)))):
        globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"] = 0.0, 0.0
        one = search("xbd degraded")
        globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"] = saved
    check("16 with S2 failing, search still returns OpenAlex rows and names the degraded index",
          "error" not in one and one["resolved_count"] == 1 and one["degraded"] == ["s2"]
          and one["indexes"]["s2"]["status"] == 429, f"got {json.dumps(one)[:300]}")

    # 17-19. verify: exact resolves, a punctuation variant resolves, a miss is unresolved and names the closest.
    with _fetch(route(s2=(200, s2_payload(s2_xbd)), oa=(200, oa_payload()), cr=(200, cr_payload()))):
        exact = verify([xbd], [])
        variant = verify(["creating xBD - a dataset for assessing building damage from satellite imagery"], [])
        missing = verify(["A Unified Theory of Nothing Whatsoever"], [])
    check("17 an exact title resolves, through S2, with its ids",
          exact["resolved_count"] == 1 and exact["results"][0]["match"] == "exact"
          and exact["results"][0]["source"] == "s2" and exact["results"][0]["ids"]["S2"] == "ec58b594",
          f"got {exact['results'][0]}")
    check("18 punctuation and case do not break a title match",
          variant["resolved_count"] == 1 and variant["results"][0]["match"] == "exact")
    check("19 a title with no match is unresolved, checked all three, and names the closest row",
          missing["resolved_count"] == 0 and missing["results"][0]["match"] == "none"
          and missing["results"][0]["checked"] == ["s2", "openalex", "crossref"]
          and "closest" in missing["results"][0]["note"], f"got {missing['results'][0]}")

    # 20-21. The one an adversarial review found: a partial match is a candidate, never resolved.
    attn = {"paperId": "attn0001", "title": "Attention Is All You Need", "year": 2017, "authors": [], "externalIds": {}}
    with _fetch(route(s2=(200, s2_payload(attn)), oa=(200, oa_payload()), cr=(200, cr_payload()))):
        longer = verify(["Attention Is All You Need for Wildfire Damage Assessment"], [])
        shorter = verify(["Deep Learning"], [])
    r = longer["results"][0]
    check("20 a title that merely contains the found one is a candidate: not resolved, id named, not carried",
          longer["resolved_count"] == 0 and longer["candidate_count"] == 1 and r["match"] == "candidate"
          and r["paperId"] is None and r["candidate"]["ids"]["S2"] == "attn0001"
          and "NOT the same paper" in r["note"], f"got {r}")
    check("21 nor is a title the found one merely starts with",
          shorter["resolved_count"] == 0 and shorter["results"][0]["paperId"] is None)

    # 22-23. verify falls through: S2 down, OpenAlex has it; nobody but Crossref has it.
    # A fresh cache: case 17 cached S2's answer for this exact title, and a
    # cache hit would make S2 look up when the stub says it is down.
    with _environ(RESEARCH_CACHE_DIR=tempfile.mkdtemp(prefix="snowball-cache-")):
        with _fetch(route(s2=(500, b"down"), oa=(200, oa_payload(oa_xbd)), cr=(200, cr_payload()))):
            globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"] = 0.0, 0.0
            via_oa = verify([xbd], [])
            globals()["BACKOFF_BASE"], globals()["BACKOFF_CAP"] = saved
    check("22 with S2 down, an exact title resolves through OpenAlex and the S2 error is recorded",
          via_oa["resolved_count"] == 1 and via_oa["results"][0]["source"] == "openalex"
          and via_oa["results"][0]["ids"]["OpenAlex"] == "W2967473420" and "s2" in via_oa["results"][0]["errors"],
          f"got {via_oa['results'][0]}")
    cr_item = {"DOI": "10.3390/rs12223808", "title": [cr[0]["title"][0]], "issued": {"date-parts": [[2020, 11]]},
               "is-referenced-by-count": 40, "container-title": ["Remote Sensing"], "author": []}
    with _fetch(route(s2=(200, s2_payload()), oa=(200, oa_payload()), cr=(200, cr_payload(cr_item)))):
        via_cr = verify([cr[0]["title"][0]], [])
    check("23 a title only Crossref holds resolves through Crossref with its DOI",
          via_cr["resolved_count"] == 1 and via_cr["results"][0]["source"] == "crossref"
          and via_cr["results"][0]["ids"]["DOI"] == "10.3390/rs12223808", f"got {via_cr['results'][0]}")

    # 24. Ids: a good S2 id resolves, a bad DOI goes to Crossref and fails there too, each named.
    batch_payload = [dict(s2_xbd), None]
    with _fetch(route(s2=(200, json.dumps(batch_payload).encode()), cr=(404, b"{}"))):
        ids = verify([], ["ec58b594", "DOI:10.0000/nope"])
    check("24 a good id resolves and a bad one does not, each named, the DOI having tried Crossref",
          ids["resolved_count"] == 1 and ids["unresolved_count"] == 1
          and ids["results"][1]["query"] == "DOI:10.0000/nope" and "crossref" in ids["results"][1]["errors"],
          f"got {ids['results']}")

    # 25. The CLI reaches verify and prints JSON.
    with _fetch(route(s2=(200, s2_payload(s2_xbd)))):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["verify", "--title", xbd])
        try:
            argv_out = json.loads(buf.getvalue())
        except ValueError:
            argv_out = {}
    check("25 the CLI dispatches verify and prints JSON", rc == 0 and argv_out.get("resolved_count") == 1)
    check("26 verify with nothing to check is an error", "error" in verify([], []))

    # 27-28. OpenAlex hops: referenced works resolve in a batch; cited-by uses the cites: filter.
    seen_urls: list[str] = []

    def oa_router(method, url, body, headers):
        seen_urls.append(url)
        if "/works/W2967473420" in url:
            return 200, json.dumps({**oa_xbd, "referenced_works": ["https://openalex.org/W1", "https://openalex.org/W2"]}).encode()
        if "filter=openalex" in url:
            return 200, oa_payload({"id": "https://openalex.org/W1", "title": "Ref one", "authorships": []},
                                   {"id": "https://openalex.org/W2", "title": "Ref two", "authorships": []})
        if "filter=cites" in url:
            return 200, oa_payload({"id": "https://openalex.org/W9", "title": "Citer", "authorships": []})
        return 404, b"{}"

    with _fetch(route(oa=oa_router)):
        refs = oa_referenced("W2967473420")
        citers = oa_cited_by("W2967473420", 10)
    check("27 openalex refs resolves referenced_works to records in one batch",
          refs.get("resolved_count") == 2 and refs["seed"] == "W2967473420"
          and any("filter=openalex%3AW1%7CW2" in u or "filter=openalex:W1|W2" in urllib.parse.unquote(u) for u in seen_urls),
          f"got {refs} urls={seen_urls}")
    check("28 openalex cited-by asks for works citing the seed",
          citers.get("resolved_count") == 1 and citers["seed"] == "W2967473420"
          and any("cites" in u for u in seen_urls), f"got {citers}")

    # 29. arXiv: the query string is built from category and date window, and a search goes to export.arxiv.org.
    sq = arxiv_query(None, "cs.CV", "2024-09-01", "2024-09-02")
    check("29 an arXiv query carries the category and the date window",
          sq == "cat:cs.CV AND submittedDate:[202409010000 TO 202409022359]", sq)
    with _fetch(route(ax=(200, _fixture_text("arxiv_search.xml").encode()))):
        axs = arxiv_search("building damage assessment", "cs.CV", limit=3)
    check("30 an arXiv search returns records with abstracts and pdf links",
          axs.get("resolved_count") == 3 and all(p["abstract"] and p["pdfUrl"] for p in axs["papers"]),
          f"got {json.dumps(axs)[:300]}")

    # 31. Status: the state table. Any answer is reachable; 429 is not an outage; keyless is a state, not an error.
    table = [
        ((200, True), "connected"), ((200, False), "connected-no-key"), ((429, False), "connected-no-key"),
        ((422, False), "connected-no-key"), ((403, True), "not connected"), ((0, True), "not connected"),
        ((503, False), "not connected"), ((429, True), "connected"),
    ]
    bad = [(inp, probe_state(*inp)[0], want) for inp, want in table if probe_state(*inp)[0] != want]
    check("31 the status state table: reachable is a state, throttled is not an outage, keyless is not an error",
          not bad, f"wrong: {bad}")

    # 32. Status runs with no keys at all: seven sources, each in a state, and the top three suggestions named.
    def any_host(method, url, body, headers):
        return 200, b"{}"

    with _fetch(any_host):
        st = status()
    check("32 status with no keys probes all seven, marks them connected-no-key or connected, and suggests three keys",
          len(st["sources"]) == 7 and st["not_connected"] == [] and "arxiv" in st["connected"]
          and [s["env"] for s in st["suggest"]] == [["S2_API_KEY"], ["OPENALEX_MAILTO"], ["CROSSREF_MAILTO"]]
          and all(line.startswith("- ") for line in st["lines"]),
          f"got {json.dumps(st)[:400]}")
    with _environ(S2_API_KEY="k", OPENALEX_MAILTO="a@b", CROSSREF_MAILTO="a@b"):
        with _fetch(any_host):
            st2 = status()
    check("33 with the top three set, the suggestions move on to the next missing keys",
          st2["connected"][:3] == ["semantic-scholar", "openalex", "crossref"]
          and [s["env"] for s in st2["suggest"]] == [["UNPAYWALL_EMAIL"], ["HF_TOKEN"], ["ZOTERO_API_KEY", "ZOTERO_USER_ID"]],
          f"got {st2['suggest']}")

    # 34. Dedupe across sources: DOI form differences and arXiv versions do not make two papers.
    a = finish({"title": "X", "externalIds": {"DOI": "https://doi.org/10.1/ABC"}, "sources": ["s2"], "source": "s2"})
    b = finish({"title": "X", "externalIds": {"DOI": "10.1/abc"}, "sources": ["openalex"], "source": "openalex"})
    c = finish({"title": "Y", "externalIds": {"ArXiv": "2409.00665v2"}, "sources": ["arxiv"], "source": "arxiv"})
    d = finish({"title": "Y", "externalIds": {"ArXiv": "2409.00665"}, "sources": ["s2"], "source": "s2"})
    merged = merge_lists([a, c], [b, d])
    check("34 a DOI in two spellings and an arXiv id with and without a version dedupe to one paper each",
          len(merged) == 2 and merged[0]["sources"] == ["openalex", "s2"] and merged[1]["sources"] == ["arxiv", "s2"],
          f"got {[ (m['title'], m['sources']) for m in merged]}")

    PACE.update(saved_pace)
    print()
    if failures:
        print(f"{len(failures)} of {len(ran)} cases failed: {', '.join(failures)}")
        return 1
    print(f"{len(ran)} of {len(ran)} cases passed")
    return 0


FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _fixture(name: str) -> dict[str, Any]:
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return json.load(fh)


def _fixture_text(name: str) -> str:
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


@contextlib.contextmanager
def _environ(**pairs: str):
    old = {k: os.environ.get(k) for k in pairs}
    os.environ.update(pairs)
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@contextlib.contextmanager
def _fetch(stub):
    """Stand in for the network: stub(method, url, body, headers) -> (status, bytes)."""
    original = globals()["http_fetch"]
    globals()["http_fetch"] = stub
    try:
        yield
    finally:
        globals()["http_fetch"] = original


if __name__ == "__main__":
    sys.exit(main())
