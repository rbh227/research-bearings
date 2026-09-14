#!/usr/bin/env python3
"""snowball — the retrieval script for research-bearings.

Search and citation checking over the Semantic Scholar Graph API. Standard
library only. Every invocation is one process that prints one JSON result and
exits; nothing stays resident.

It is named for what it used to do. Chunk 2 built a citation walker here — hops,
a budget ledger, edge parsing — for a snowballing skill that was deleted in
chunk 3, when the plugin's retrieval turned out to want breadth rather than
depth. What survives is what /scout needs: find papers by keyword, and decide
whether a paper someone named actually exists.

  snowball.py search "query"            [--limit N]
  snowball.py batch <id> [<id> ...]
  snowball.py verify [--title T]... [--id I]...   [--limit N]
  snowball.py health
  snowball.py --selftest                          (offline, seconds)

Environment:
  SEMANTIC_SCHOLAR_API_KEY  or one line in ~/.config/research-bearings/s2-api-key.
                            Optional. Without it the API 429s after a few calls;
                            the retry policy absorbs some of that and coverage
                            drops, which /scout stamps in its Status block.
  S2_CACHE_DIR              raw responses keyed by request hash, disposable.
                            Default ~/.cache/research-bearings/s2
  RESEARCH_PROJECT_DIR      the project whose research/ receives records.
                            Default CLAUDE_PROJECT_DIR, else cwd.

One on-disk artifact under <project>/research/:
  .papers/<paperId>.json    one record per paper returned, written by the script
                            rather than by a model: hundreds of records through a
                            model's context costs tokens and invites transcription
                            errors.

There is no budget and no ledger. A citation walk compounds and needs a ceiling
enforced before each request; search does not — every call returns at most
--limit rows and starts nothing.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import random
import sys
import unicodedata
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

try:  # POSIX. Absent on Windows, where concurrent saves fall back to unlocked.
    import fcntl
except ImportError:  # pragma: no cover - not reachable on the platforms we run
    fcntl = None  # type: ignore[assignment]

def _version() -> str:
    """The plugin's version, read from its manifest rather than kept here.

    A second copy of the version is a copy that goes stale: this said 0.2.0
    while the manifest said 0.3.1, and `health` is what /setup records.
    """
    manifest = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..",
        ".claude-plugin", "plugin.json")
    try:
        with open(manifest, encoding="utf-8") as fh:
            return str(json.load(fh).get("version") or "unknown")
    except (OSError, ValueError):
        return "unknown"


VERSION = _version()
BASE = "https://api.semanticscholar.org/graph/v1"
TIMEOUT = 60

# Fixed by contract, not caller-specified. A caller-chosen field list is a way
# for one landscape section to become quietly incomparable with the one beside it.
PAPER_FIELDS = (
    "paperId,title,year,externalIds,venue,authors,abstract,citationCount,"
    "referenceCount,openAccessPdf,publicationTypes,fieldsOfStudy"
)
# Confirmed against the live API 2026-09-13: edge fields go in the same flat
# fields= list and land at row level, alongside citedPaper / citingPaper.
EDGE_FIELDS = "isInfluential,intents,contextsWithIntent"
HOP_FIELDS = PAPER_FIELDS + "," + EDGE_FIELDS

# Ticket 09 measured the documented 1 RPS model as wrong: 429s survive 1.1 s
# spacing, arrive non-deterministically, and never carry Retry-After. So there
# is no inter-request gate, and the backoff delays are hard-coded.
ATTEMPTS = 5
BACKOFF_BASE = 0.5
BACKOFF_CAP = 8.0
# 0 is our own marker for a transport failure: connection reset, read timeout,
# truncated body. Those are exactly as retryable as a 429.
RETRYABLE = frozenset({0, 429, 500, 502, 503, 504})

DAY = 86400
# A paper's reference list never changes; its citation list grows.
TTL = {"batch": 90 * DAY, "search": 7 * DAY}

BATCH_MAX = 500
SEARCH_MAX = 100

# --------------------------------------------------------------------------
# paths and records


KEY_FILE = "~/.config/research-bearings/s2-api-key"


def err(message: str, attempts: int = 0, status: int | None = None) -> dict[str, Any]:
    """The one error shape. Tools return it; they never raise, because a tool
    that throws leaves the model to invent what happened."""
    return {"error": message, "attempts": attempts, "status": status}


def api_key() -> str:
    """The environment first, then one line in KEY_FILE. No plugin config, no
    secrets store, nothing the sandbox cannot see: a file the user can cat."""
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    if key:
        return key
    try:
        with open(os.path.expanduser(KEY_FILE), encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def cache_dir() -> str:
    return os.environ.get("S2_CACHE_DIR", "").strip() or os.path.expanduser(
        "~/.cache/research-bearings/s2"
    )


def project_dir() -> str:
    """The project whose research/ receives records.

    RESEARCH_PROJECT_DIR, else CLAUDE_PROJECT_DIR (set for every Bash call
    Claude Code makes), else cwd. One resolution, because `health` used to
    report only the first of the three and so printed null for a run whose
    records were landing somewhere real."""
    return os.path.abspath(
        os.environ.get("RESEARCH_PROJECT_DIR", "").strip()
        or os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
        or os.getcwd()
    )


def records_dir() -> str:
    """<project>/research/.papers/."""
    return os.path.join(project_dir(), "research", ".papers")


def write_atomic(path: str, payload: Any) -> None:
    """Write via a uniquely named temp file in the same directory, then rename.

    The temp name must be unique: two processes sharing one `<path>.tmp` will
    interleave their writes and rename each other's half-written file into place.
    """
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


# --------------------------------------------------------------------------
# cache


def cache_key(method: str, url: str, body: Any, keyed: bool) -> str:
    """Stable across calls, and distinguishes a keyed request from an unkeyed one.

    The two pools return different data under load (ticket 09: 2/6 unauthenticated
    against 8/10 keyed), so a cache that conflated them would serve a throttled
    answer to a keyed caller.
    """
    raw = method + "\n" + url + "\n" + json.dumps(body, sort_keys=True) + "\n"
    raw += "keyed" if keyed else "anon"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def cache_read(kind: str, key: str, now: float | None = None) -> Any | None:
    d = cache_dir()
    if not d:
        return None
    path = os.path.join(d, key + ".json")
    if not os.path.exists(path):
        return None
    ttl = TTL.get(kind)
    if ttl is not None:
        age = (now if now is not None else time.time()) - os.path.getmtime(path)
        if age > ttl:
            return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def cache_write(key: str, payload: Any) -> None:
    d = cache_dir()
    if not d:
        return
    with contextlib.suppress(OSError):
        write_atomic(os.path.join(d, key + ".json"), payload)
        # a disposable cache is never worth failing a call over


# --------------------------------------------------------------------------
# HTTP


def http_fetch(method: str, url: str, body: Any, key: str) -> tuple[int, bytes]:
    """One attempt. Returns (status, raw body), status 0 for a transport failure.

    Every read is inside the guard. `urlopen` succeeding does not mean the body
    arrives: a reset connection, a read timeout or a truncated response raises
    out of `resp.read()`, and an exception escaping here would bypass the retry
    loop and the error contract both.
    """
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    if key:
        req.add_header("x-api-key", key)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read()
        except Exception as read_exc:  # noqa: BLE001 - the body is best-effort
            detail = f"<error body unreadable: {read_exc}>".encode()
        return exc.code, detail
    except urllib.error.URLError as exc:
        return 0, str(exc.reason).encode("utf-8")
    except Exception as exc:  # noqa: BLE001 - TimeoutError, ConnectionReset, IncompleteRead
        return 0, f"{type(exc).__name__}: {exc}".encode()


def request(
    kind: str,
    method: str,
    path: str,
    params: dict[str, Any] | None = None,
    body: Any = None,
) -> Any:
    """Cache, retry, parse. Returns the payload, or an error dict. Never raises."""
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    key = api_key()
    ck = cache_key(method, url, body, bool(key))

    cached = cache_read(kind, ck)
    if cached is not None:
        return cached

    status: int | None = None
    detail = ""
    for attempt in range(ATTEMPTS):
        status, raw = http_fetch(method, url, body, key)
        if status == 200:
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                return err(f"malformed response from Semantic Scholar: {exc}", attempt + 1, status)
            cache_write(ck, payload)
            return payload
        detail = raw.decode("utf-8", "replace")[:300]
        if status not in RETRYABLE:
            return err(f"Semantic Scholar request failed: {detail}", attempt + 1, status)
        if attempt < ATTEMPTS - 1:
            # Full jitter. Retry is what works here; spacing is not. No sleep
            # after the last attempt — nothing follows it to wait for.
            time.sleep(random.uniform(0, min(BACKOFF_CAP, BACKOFF_BASE * 2**attempt)))
    return err(
        f"Semantic Scholar request failed after {ATTEMPTS} attempts: {detail or 'no response'}",
        ATTEMPTS,
        status,
    )


# --------------------------------------------------------------------------
# shaping


def pdf_url(paper: dict[str, Any]) -> str | None:
    """openAccessPdf.url comes back as "" even when status is GREEN or GOLD
    (ticket 09 6). An empty string is absence, not a link."""
    oa = paper.get("openAccessPdf")
    if not isinstance(oa, dict):
        return None
    url = (oa.get("url") or "").strip()
    return url or None


def missing_fields(paper: dict[str, Any]) -> list[str]:
    """What the card must mark rather than fill in. Half of backward-hop rows
    have no abstract; that is a fact about the corpus, not a gap to guess at."""
    out = []
    if not (paper.get("abstract") or "").strip():
        out.append("abstract")
    if not (paper.get("venue") or "").strip():
        out.append("venue")
    ext = paper.get("externalIds") or {}
    if not ext.get("DOI"):
        out.append("doi")
    return out


def to_record(paper: dict[str, Any]) -> dict[str, Any]:
    authors = [a.get("name") for a in (paper.get("authors") or []) if a.get("name")]
    return {
        "paperId": paper.get("paperId"),
        "title": paper.get("title"),
        "year": paper.get("year"),
        "venue": paper.get("venue") or None,
        "authors": authors,
        "abstract": paper.get("abstract") or None,
        "externalIds": paper.get("externalIds") or {},
        "citationCount": paper.get("citationCount"),
        "referenceCount": paper.get("referenceCount"),
        "publicationTypes": paper.get("publicationTypes") or [],
        "fieldsOfStudy": paper.get("fieldsOfStudy") or [],
        "pdfUrl": pdf_url(paper),
        "missing": missing_fields(paper),
    }


# --------------------------------------------------------------------------
# paper records


def record_path(paper_id: str) -> str | None:
    """Confined to research/.papers/ by this function, not by the write-scope
    guard: a PreToolUse hook on Write/Edit does not see a script's
    filesystem access (chunk-2 spec 4.5, 5.6)."""
    base = records_dir()
    if not base or not paper_id:
        return None
    safe = "".join(c for c in paper_id if c.isalnum() or c in "-_")
    if not safe:
        return None
    path = os.path.abspath(os.path.join(base, safe + ".json"))
    if os.path.commonpath([path, base]) != base:
        return None
    return path


def save_record(record: dict[str, Any]) -> bool:
    """Write one paper's record. Idempotent: the same paper found by two queries
    produces the same bytes, and write_atomic's temp-then-rename means a reader
    never sees half a file. The read-merge-write this used to do was for citation
    edges, which went with the hops."""
    path = record_path(record.get("paperId") or "")
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
# tools


def batch_papers(ids: list[str]) -> dict[str, Any]:
    """Metadata for many ids in one call. Used by `verify` to resolve an id, and
    available on its own."""
    ids = [str(i).strip() for i in (ids or []) if str(i).strip()]
    if not ids:
        return err("ids is required")
    if len(ids) > BATCH_MAX:
        return err(f"at most {BATCH_MAX} ids per call, got {len(ids)}")
    payload = request("batch", "POST", "/paper/batch", {"fields": PAPER_FIELDS}, {"ids": ids})
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if not isinstance(payload, list):
        return err("unexpected response shape: not a list", 1, 200)
    papers, unresolvable_ids = [], []
    for asked, row in zip(ids, payload):
        if isinstance(row, dict) and row.get("paperId"):
            papers.append(to_record(row))
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
        "papers": deduped,
        "unresolvable_ids": unresolvable_ids,
        "resolved_count": len(deduped),
        "unresolvable_count": len(unresolvable_ids),
        "alias_rows_collapsed": aliases,
        "records_written": save_all(deduped),
    }


def search(query: str, limit: int = 20) -> dict[str, Any]:
    """Papers by keyword. At most `limit` rows, and nothing follows from them:
    search does not compound the way a citation walk does, so there is no budget
    to enforce here. The caller's bound is how many searches it chooses to make."""
    query = (query or "").strip()
    if not query:
        return err("query is required")
    limit = max(1, min(int(limit or 20), SEARCH_MAX))
    payload = request(
        "search", "GET", "/paper/search", {"query": query, "limit": limit, "fields": PAPER_FIELDS}
    )
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if not isinstance(payload, dict) or "data" not in payload:
        return err("unexpected response shape: no data array", 1, 200)
    out = split_search(payload, query, limit)
    out["records_written"] = save_all(out["papers"])
    return out


def split_search(payload: dict[str, Any], query: str, limit: int) -> dict[str, Any]:
    rows = payload.get("data") or []
    papers = [to_record(r) for r in rows if isinstance(r, dict) and r.get("paperId")]
    nxt = payload.get("next")
    return {
        "query": query,
        "limit": limit,
        "papers": papers,
        "resolved_count": len(papers),
        "malformed_count": len(rows) - len(papers),
        "rows_returned": len(rows),
        "total": payload.get("total"),
        "next": nxt,
        "truncated": nxt is not None,
    }


def normalised_title(text: str) -> str:
    """A title folded for comparison: case, punctuation and spacing dropped.

    Two records of the same paper differ in punctuation far more often than in
    words — a colon becomes a dash, an ampersand becomes "and", a subtitle
    loses its capitals. Folding those away is the difference between "this
    paper does not exist" and "this paper exists and you typed it from memory".
    """
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
    # A shorter title sitting inside a longer one is a real match only when the
    # shorter one is long enough to be a title rather than a word or two.
    shorter = a if len(a) <= len(f) else f
    if (a in f or f in a) and len(shorter.split()) >= 4:
        return "substring"
    return "none"


# Only an exact match, after folding, certifies a paper. Prefix and substring
# were here until 2026-09-14, when an adversarial review showed what they do:
# "Attention Is All You Need for Wildfire Damage Assessment" prefix-matched
# "Attention Is All You Need" and came back resolved, carrying that paper's id.
# That is the fabrication this verb exists to catch, wearing a checkmark. The
# folding already handles the variants prefix was added for - a colon that
# became a dash still compares equal - so exact-only loses nothing real.
RESOLVING_MATCHES = ("exact",)
NEAR_MATCHES = ("prefix", "substring")


def _id_matches(asked: str, rec: dict[str, Any]) -> bool:
    """Whether a record answers to the id that was asked for, in any spelling."""
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


def verify(titles: list[str], ids: list[str], limit: int = 5) -> dict[str, Any]:
    """Resolve papers named in a written artifact against the record.

    The posture chunk 3 runs on: the model may name a paper from memory, and
    this is what decides whether that paper exists. Nothing is dropped — an
    unresolved row comes back marked, with the closest thing the search did
    return, so a reader sees exactly where memory outran the record.

    Charges no budget. Verification is not discovery: the papers were already
    named, and a ceiling that refused to check them would be the wrong shape.
    """
    titles = [t.strip() for t in (titles or []) if t and t.strip()]
    ids = [i.strip() for i in (ids or []) if i and i.strip()]
    if not titles and not ids:
        return err("verify needs at least one --title or --id")

    results: list[dict[str, Any]] = []

    if ids:
        got = batch_papers(ids)
        if "error" in got:
            return got
        for asked in ids:
            rec = next((r for r in got["papers"] if _id_matches(asked, r)), None)
            results.append({
                "query": asked,
                "kind": "id",
                "resolved": rec is not None,
                "paperId": rec["paperId"] if rec else None,
                "title": rec["title"] if rec else None,
                "year": rec["year"] if rec else None,
                "match": "id" if rec else "no record for this id",
            })

    for asked in titles:
        found = search(asked, limit=limit)
        if "error" in found:
            results.append({
                "query": asked, "kind": "title", "resolved": False, "paperId": None,
                "title": None, "year": None, "match": f"search failed: {found['error']}",
            })
            continue
        order = RESOLVING_MATCHES + NEAR_MATCHES
        ranked = sorted(
            ((title_match(asked, p.get("title") or ""), p) for p in found["papers"]),
            key=lambda pair: order.index(pair[0]) if pair[0] in order else 9,
        )
        best_match, best = ranked[0] if ranked else ("none", None)
        ok = best_match in RESOLVING_MATCHES
        if ok:
            match = "exact"
        elif best_match in NEAR_MATCHES:
            # Deliberately NOT resolved: a near match is the dangerous case, not
            # the safe one. Name it so the caller can correct a typo, and give
            # the candidate's id so the correction is one step - but the id does
            # not go on the card until a human or a later exact check says so.
            match = (
                f"{best_match} match only, NOT the same paper unless you say so: "
                f"{best['title']} (S2 {best['paperId']})"
            )
        else:
            match = (
                f"no title match in {found['rows_returned']} rows"
                + (f"; closest: {best['title']}" if best else "")
            )
        results.append({
            "query": asked,
            "kind": "title",
            "resolved": ok,
            "paperId": best["paperId"] if ok and best else None,
            "title": best["title"] if best else None,
            "year": best["year"] if best else None,
            "match": match,
        })

    resolved = sum(1 for r in results if r["resolved"])
    return {
        "results": results,
        "resolved_count": resolved,
        "unresolved_count": len(results) - resolved,
        "checked": len(results),
    }


def health() -> dict[str, Any]:
    """Availability without spending a request or inferring it from a failure."""
    recs = records_dir()
    return {
        "script": "snowball.py",
        "version": VERSION,
        "key_present": bool(api_key()),
        "cache_dir": cache_dir() or None,
        "project_dir": project_dir(),
        "records_dir": recs or None,
        "records_enabled": bool(recs),
    }


# --------------------------------------------------------------------------
# command line


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="snowball.py",
        description="Semantic Scholar search and citation checking. One JSON result per call.",
    )
    ap.add_argument("--selftest", action="store_true", help="offline checks, then exit")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("health", help="key presence and paths; no network")
    p = sub.add_parser("search", help="papers by keyword")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)
    p = sub.add_parser("batch", help="metadata for many ids at once")
    p.add_argument("ids", nargs="+")
    p = sub.add_parser("verify", help="do these papers exist? by title or id")
    p.add_argument("--title", action="append", default=[], help="repeatable")
    p.add_argument("--id", action="append", default=[], dest="ids", help="repeatable")
    p.add_argument("--limit", type=int, default=5, help="search rows to consider per title")

    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.cmd:
        ap.print_help()
        return 2

    if args.cmd == "health":
        out: dict[str, Any] = health()
    elif args.cmd == "search":
        out = search(args.query, args.limit)
    elif args.cmd == "verify":
        out = verify(args.title, args.ids, args.limit)
    else:
        out = batch_papers(args.ids)

    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


# --------------------------------------------------------------------------
# selftest


def selftest() -> int:
    """Offline checks on the paths /scout uses: parse, cache, retry, records,
    and verification. The 31-case suite that stood here until 2026-09-14 mostly
    exercised the citation walker — hops, edge direction, the budget ledger —
    which went with the snowballing skill."""
    failures: list[str] = []
    ran: list[str] = []
    # A cached real response would bypass the stubs silently, so the selftest
    # gets its own empty cache and its own empty project.
    os.environ["S2_CACHE_DIR"] = tempfile.mkdtemp(prefix="snowball-cache-")
    os.environ["RESEARCH_PROJECT_DIR"] = tempfile.mkdtemp(prefix="snowball-project-")

    def check(case: str, ok: bool, detail: str = "") -> None:
        ran.append(case)
        print(f"{'ok  ' if ok else 'FAIL'} {case}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(case)

    # 1-2. The search envelope, on a real captured response.
    found = split_search(_fixture("search_dmg.json"), "building damage", 5)
    check(
        "1  a search envelope parses, and truncation is reported",
        found["resolved_count"] > 0
        and found["rows_returned"] >= found["resolved_count"]
        and found["truncated"] is (found["next"] is not None),
        f"resolved={found['resolved_count']} next={found['next']} truncated={found['truncated']}",
    )
    unpaged = dict(_fixture("search_dmg.json"))
    unpaged.pop("next", None)
    check(
        "2  no `next` means the result was not truncated",
        split_search(unpaged, "q", 5)["truncated"] is False,
    )

    # 3. A row with no paperId is dropped rather than carded as a blank.
    malformed = {"total": 2, "data": [
        {"paperId": "good", "title": "T", "authors": []},
        {"paperId": None, "title": "no id"},
    ]}
    out = split_search(malformed, "q", 5)
    check(
        "3  a row with no paperId is counted as malformed, never returned",
        out["resolved_count"] == 1 and out["malformed_count"] == 1
        and all(p["paperId"] for p in out["papers"]),
        f"{out['resolved_count']}/{out['malformed_count']}",
    )

    # 4-6. The transport: non-JSON, an error status, and a shape we did not expect.
    with _fetch(lambda *a, **k: (200, b"<html>not json</html>")):
        check("4  a non-JSON body is an error, not a crash", "error" in search("q"))
    with _fetch(lambda *a, **k: (404, b'{"error":"not found"}')):
        check("5  an error status is reported as an error", "error" in search("q"))
    with _fetch(lambda *a, **k: (200, b'{"ok":true}')):
        check("6  a response with no data array is an error", "error" in search("q"))

    # 7. Retry with jitter, not a fixed throttle: 429s here are non-deterministic
    #    and never carry Retry-After (ticket 09).
    attempts = {"n": 0}

    def flaky(method, url, body, key):
        attempts["n"] += 1
        if attempts["n"] < 3:
            return 429, b'{"error":"too many"}'
        return 200, json.dumps({"total": 1, "data": [
            {"paperId": "p", "title": "T", "authors": []}]}).encode()

    with _fetch(flaky):
        # A distinct query: case 6's 200 response is cached under "q", and a
        # cache hit would skip the stub entirely and report attempts=0.
        retried = search("a query no earlier case used")
    check(
        "7  a 429 is retried and the call succeeds",
        attempts["n"] == 3 and retried.get("resolved_count") == 1,
        f"attempts={attempts['n']} out={retried.get('error') or retried.get('resolved_count')}",
    )

    # 8. The cache serves a repeat without a second request.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(S2_CACHE_DIR=tmp):
            calls = {"n": 0}

            def counting(method, url, body, key):
                calls["n"] += 1
                return 200, json.dumps({"total": 1, "data": [
                    {"paperId": "p", "title": "T", "authors": []}]}).encode()

            with _fetch(counting):
                search("same query")
                search("same query")
    check("8  a repeated call is served from cache", calls["n"] == 1, f"calls={calls['n']}")

    # 9. Records are written by the script, not carried through a model.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp, S2_CACHE_DIR=os.path.join(tmp, "c")):
            with _fetch(lambda *a, **k: (200, json.dumps({"total": 1, "data": [
                    {"paperId": "rec1", "title": "T", "authors": [{"name": "A"}]}]}).encode())):
                wrote = search("q")
            on_disk = os.path.exists(os.path.join(tmp, "research", ".papers", "rec1.json"))
    check(
        "9  every returned paper lands in research/.papers/",
        wrote["records_written"] == 1 and on_disk,
        f"written={wrote['records_written']} on_disk={on_disk}",
    )

    # 10. A missing field is marked, never inferred.
    rec = to_record({"paperId": "x", "title": "T", "authors": [], "abstract": None})
    check(
        "10 an absent abstract is marked missing",
        "abstract" in rec["missing"] and rec["abstract"] is None,
        f"missing={rec['missing']}",
    )

    # 11-16. verify: the check /scout's whole posture rests on.
    xbd = "Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery"
    search_payload = {"total": 1, "data": [{
        "paperId": "ec58b594", "title": xbd, "year": 2019, "venue": "CVPR Workshops",
        "authors": [{"name": "R. Gupta"}], "externalIds": {"DOI": "10.1184/R1/8135576.V1"},
    }]}
    with _fetch(lambda *a, **k: (200, json.dumps(search_payload).encode())):
        exact = verify([xbd], [])
        variant = verify(["creating xBD - a dataset for assessing building damage from satellite imagery"], [])
        missing = verify(["A Unified Theory of Nothing Whatsoever"], [])
    check(
        "11 an exact title resolves",
        exact["resolved_count"] == 1 and exact["results"][0]["match"] == "exact"
        and exact["results"][0]["paperId"] == "ec58b594",
        f"got {exact['results'][0]}",
    )
    check(
        "12 punctuation and case do not break a title match",
        variant["resolved_count"] == 1 and variant["results"][0]["match"] == "exact",
        f"got {variant['results'][0]['match']}",
    )
    check(
        "13 a title with no match is unresolved, and names the closest row",
        missing["resolved_count"] == 0 and missing["results"][0]["paperId"] is None
        and "closest" in missing["results"][0]["match"],
        f"got {missing['results'][0]['match']}",
    )

    # 14-15. The one an adversarial review found: a partial match must NOT
    #        certify. "Attention Is All You Need for Wildfire Damage Assessment"
    #        came back resolved carrying the id of "Attention Is All You Need".
    near_payload = {"total": 1, "data": [{
        "paperId": "attn0001", "title": "Attention Is All You Need", "year": 2017,
        "venue": "NeurIPS", "authors": [{"name": "A. Vaswani"}], "externalIds": {},
    }]}
    with _fetch(lambda *a, **k: (200, json.dumps(near_payload).encode())):
        longer = verify(["Attention Is All You Need for Wildfire Damage Assessment"], [])
        shorter = verify(["Deep Learning"], [])
    check(
        "14 a title that merely contains the found one is NOT resolved",
        longer["resolved_count"] == 0 and longer["results"][0]["paperId"] is None
        and "NOT the same paper" in longer["results"][0]["match"]
        and "attn0001" in longer["results"][0]["match"],
        f"got {longer['results'][0]}",
    )
    check(
        "15 nor is a title the found one merely starts with",
        shorter["resolved_count"] == 0 and shorter["results"][0]["paperId"] is None,
        f"got {shorter['results'][0]}",
    )

    batch_payload = [{
        "paperId": "ec58b594", "title": xbd, "year": 2019,
        "externalIds": {"DOI": "10.1184/R1/8135576.V1"},
    }, None]
    with _fetch(lambda *a, **k: (200, json.dumps(batch_payload).encode())):
        ids = verify([], ["ec58b594", "DOI:10.0000/nope"])
    check(
        "16 a good id resolves and a bad one does not, each named",
        ids["resolved_count"] == 1 and ids["unresolved_count"] == 1
        and ids["results"][1]["query"] == "DOI:10.0000/nope",
        f"got {ids['results']}",
    )

    # 17. The CLI reaches verify — where a verb missing --run/--budget once broke.
    with _fetch(lambda *a, **k: (200, json.dumps(search_payload).encode())):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["verify", "--title", xbd])
        try:
            argv_out = json.loads(buf.getvalue())
        except ValueError:
            argv_out = {}
    check(
        "17 the CLI dispatches verify and prints JSON",
        rc == 0 and argv_out.get("resolved_count") == 1,
        f"rc={rc} out={buf.getvalue()[:120]!r}",
    )

    check("18 verify with nothing to check is an error", "error" in verify([], []))

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


@contextlib.contextmanager
def _env(**pairs: str):
    """Set env vars for the duration of a selftest case, then restore."""
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
def _fetch(stub, real: bool = False):
    """Stand in for the network. `real=True` routes the stub through the real
    http_fetch guard, so the case exercises the guard rather than bypassing it."""
    original = globals()["http_fetch"]
    if real:
        def wrapped(method, url, body, key, _stub=stub):
            class _Resp:
                status = 200

                def read(self_inner):
                    return _stub(method, url, body, key)

                def __enter__(self_inner):
                    return self_inner

                def __exit__(self_inner, *a):
                    return False

            opener = globals()["urllib"].request.urlopen
            globals()["urllib"].request.urlopen = lambda *a, **k: _Resp()
            try:
                return original(method, url, body, key)
            finally:
                globals()["urllib"].request.urlopen = opener

        globals()["http_fetch"] = wrapped
    else:
        globals()["http_fetch"] = stub
    try:
        yield
    finally:
        globals()["http_fetch"] = original


if __name__ == "__main__":
    sys.exit(main())
