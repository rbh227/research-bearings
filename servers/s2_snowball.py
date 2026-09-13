#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=2,<3"]
# ///
"""s2-snowball — the citation walker for research-bearings.

Three hops over the Semantic Scholar Graph API, plus a no-network health check.
Neither bundled MCP server exposes references or citations (ticket 02), so the
snowball hop is ours to own (ticket 10).

Two caches, deliberately different species (chunk-2 spec 4.5):

  S2_CACHE_DIR         raw API responses keyed by request hash, disposable,
                       shared across projects, direction-aware expiry.
  RESEARCH_PROJECT_DIR one JSON record per paper under research/.papers/,
                       research data, this project only. Written here rather
                       than by the scout: several hundred records through a
                       model's context costs tokens and invites transcription
                       errors.

Run as a server:   uv run --script servers/s2_snowball.py
Run the selftest:  python3 servers/s2_snowball.py --selftest   (offline, no SDK)

The SDK import is deliberately lazy so the selftest runs on bare python3.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import random
import sys
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

VERSION = "0.2.0"
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
TTL = {"references": None, "citations": 30 * DAY, "batch": 90 * DAY}

BATCH_MAX = 500
HOP_MAX = 100

NESTED = {"references": "citedPaper", "citations": "citingPaper"}


def err(message: str, attempts: int = 0, status: int | None = None) -> dict[str, Any]:
    """The one error shape. Tools return it; they never raise, because a tool
    that throws leaves the model to invent what happened."""
    return {"error": message, "attempts": attempts, "status": status}


# --------------------------------------------------------------------------
# environment


def api_key() -> str:
    return os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()


def cache_dir() -> str:
    return os.environ.get("S2_CACHE_DIR", "").strip()


def records_dir() -> str:
    """<project>/research/.papers/, or "" when no project dir was passed."""
    project = os.environ.get("RESEARCH_PROJECT_DIR", "").strip()
    if not project:
        return ""
    return os.path.join(os.path.abspath(project), "research", ".papers")


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


def edge_of(row: dict[str, Any], origin: str, hop: str) -> dict[str, Any]:
    """The citing author's own characterization of the cited work, tagged.

    Ticket 09's find: sharper than most abstracts, and it survives the measured
    48-51% missing-abstract rate on backward hops.

    **The two hops point their sentences in opposite directions**, and getting
    this backwards would put a sentence about the seed onto a card about some
    other paper:

      references  the seed cites this row. The sentences are the SEED's prose
                  describing THIS paper. -> describes: this_paper.
      citations   this row cites the seed. The sentences are THIS paper's prose
                  describing THE SEED. -> describes: origin_paper.

    So `describes` is carried explicitly rather than left to be inferred from
    `hop` by whoever reads the record.
    """
    contexts = []
    for item in row.get("contextsWithIntent") or []:
        if not isinstance(item, dict):
            continue
        sentence = (item.get("context") or "").strip()
        if sentence:
            contexts.append({"sentence": sentence, "intents": item.get("intents") or []})
    return {
        "origin": origin,
        "hop": hop,
        "describes": "this_paper" if hop == "references" else "origin_paper",
        "isInfluential": bool(row.get("isInfluential")),
        "intents": row.get("intents") or [],
        "contexts": contexts,
    }


def to_record(paper: dict[str, Any], edge: dict[str, Any] | None = None) -> dict[str, Any]:
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
        "edges": [edge] if edge else [],
    }


def split_rows(payload: dict[str, Any], hop: str, origin: str) -> dict[str, Any]:
    """Unnest rows, and separate the ones that cannot be hopped from.

    5-12% of backward-hop rows are real cited works with no S2 record - grey
    literature, mostly (ticket 09 3). They come back under a distinct key
    carrying title, venue and year only, so a scout cannot hop from them by
    construction rather than by being told not to.

    Nothing is dropped silently. A row the API shapes in a way we do not
    recognize is counted in `malformed_count`, because `resolved + unresolvable`
    is what the scout spends its budget against and an undercount there makes a
    partial crawl look complete.
    """
    nested = NESTED[hop]
    rows = payload.get("data") or []
    resolved: list[dict[str, Any]] = []
    unresolvable: list[dict[str, Any]] = []
    malformed = 0
    for row in rows:
        paper = row.get(nested) if isinstance(row, dict) else None
        if not isinstance(paper, dict):
            malformed += 1
            continue
        if not paper.get("paperId"):
            unresolvable.append(
                {
                    "title": paper.get("title"),
                    "venue": paper.get("venue") or None,
                    "year": paper.get("year"),
                }
            )
            continue
        resolved.append(to_record(paper, edge_of(row, origin, hop)))
    nxt = payload.get("next")
    return {
        "papers": resolved,
        "unresolvable": unresolvable,
        "resolved_count": len(resolved),
        "unresolvable_count": len(unresolvable),
        "malformed_count": malformed,
        "rows_returned": len(rows),
        "next": nxt,
        # A non-null `next` means the API held rows back. Paging is not built
        # (chunk-2 spec 8), so this hop is a SAMPLE of the edge list, not the
        # edge list. Saturation cannot be concluded from a truncated round.
        "truncated": nxt is not None,
    }


# --------------------------------------------------------------------------
# paper records


def record_path(paper_id: str) -> str | None:
    """Confined to research/.papers/ by this function, not by the write-scope
    guard: a PreToolUse hook on Write/Edit does not see an MCP server's
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


@contextlib.contextmanager
def record_lock(path: str):
    """Hold an exclusive lock across one read-merge-write on a single record.

    Two hops can reach the same paper from different seeds at the same time.
    Without this, both read the same record, each merges only its own edge, and
    the second write erases the first seed's citation provenance — silently,
    with both calls reporting success.

    flock is released by the OS if the process dies, so a crash cannot wedge a
    paper. On a platform without fcntl the lock degrades to a no-op and the
    race returns; that is stated rather than hidden.
    """
    if fcntl is None:
        yield
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    handle = open(path + ".lock", "a+")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    finally:
        handle.close()


def load_record(paper_id: str) -> dict[str, Any] | None:
    path = record_path(paper_id)
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def merge_edges(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    seen = {(e.get("origin"), e.get("hop")) for e in existing.get("edges") or []}
    merged = list(existing.get("edges") or [])
    for edge in incoming.get("edges") or []:
        if (edge.get("origin"), edge.get("hop")) not in seen:
            merged.append(edge)
            seen.add((edge.get("origin"), edge.get("hop")))
    return {**existing, **incoming, "edges": merged}


def save_record(record: dict[str, Any]) -> bool:
    """Merge edges into any existing record and write. Idempotent, and the whole
    read-merge-write happens under the record's lock."""
    paper_id = record.get("paperId") or ""
    path = record_path(paper_id)
    if not path:
        return False
    try:
        with record_lock(path):
            existing = load_record(paper_id)
            if existing:
                record = merge_edges(existing, record)
            write_atomic(path, record)
        return True
    except OSError:
        return False


def save_all(records: list[dict[str, Any]]) -> int:
    return sum(1 for r in records if save_record(r))


# --------------------------------------------------------------------------
# tools


def hop(hop_name: str, paper_id: str, limit: int) -> dict[str, Any]:
    paper_id = (paper_id or "").strip()
    if not paper_id:
        return err("paper_id is required")
    limit = max(1, min(int(limit or HOP_MAX), HOP_MAX))
    payload = request(
        hop_name,
        "GET",
        f"/paper/{urllib.parse.quote(paper_id, safe='')}/{hop_name}",
        {"limit": limit, "fields": HOP_FIELDS},
    )
    if isinstance(payload, dict) and "error" in payload:
        return payload
    if not isinstance(payload, dict) or "data" not in payload:
        return err("unexpected response shape: no data array", 1, 200)
    out = split_rows(payload, hop_name, paper_id)
    out["seed"] = paper_id
    out["hop"] = hop_name
    out["limit"] = limit
    out["records_written"] = save_all(out["papers"])
    return out


def get_papers_batch(ids: list[str]) -> dict[str, Any]:
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
    # its own S2 id come back as two rows for one paper. Collapsing that inside
    # one call is not the cross-scout dedupe chunk 3 owns - it stops a single
    # call from reporting one paper twice and double-charging the budget.
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


def health() -> dict[str, Any]:
    """Availability without spending a request or inferring it from a failure."""
    recs = records_dir()
    return {
        "server": "s2-snowball",
        "version": VERSION,
        "key_present": bool(api_key()),
        "cache_dir": cache_dir() or None,
        "project_dir": os.environ.get("RESEARCH_PROJECT_DIR", "") or None,
        "records_dir": recs or None,
        "records_enabled": bool(recs),
    }


# --------------------------------------------------------------------------
# server


def serve() -> None:
    from mcp.server.mcpserver import MCPServer  # lazy: the selftest needs no SDK

    server = MCPServer(name="s2-snowball", version=VERSION)

    @server.tool(
        description=(
            "Papers this one cites (one backward snowball hop). paper_id takes a "
            "Semantic Scholar id or an ARXIV:<id> alias. Rows with no Semantic "
            "Scholar record come back under 'unresolvable' and cannot be hopped "
            "from. A true 'truncated' means the API held rows back: this hop is a "
            "sample of the reference list, not the reference list."
        )
    )
    def get_references(paper_id: str, limit: int = HOP_MAX) -> dict[str, Any]:
        return hop("references", paper_id, limit)

    @server.tool(
        description=(
            "Papers citing this one (one forward snowball hop). paper_id takes a "
            "Semantic Scholar id or an ARXIV:<id> alias. A true 'truncated' means "
            "the API held rows back."
        )
    )
    def get_citations(paper_id: str, limit: int = HOP_MAX) -> dict[str, Any]:
        return hop("citations", paper_id, limit)

    server.tool(
        description=(
            "Metadata for many papers at once, up to 500 ids. Aliases are not "
            "collapsed upstream; an arXiv id and its own S2 id are one paper here."
        )
    )(get_papers_batch)

    server.tool(
        description=(
            "Key presence, cache and project directories, version. Makes no "
            "network call. Call this before a crawl to establish availability."
        )
    )(health)

    server.run()


# --------------------------------------------------------------------------
# selftest


FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _fixture(name: str) -> dict[str, Any]:
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return json.load(fh)


def selftest() -> int:  # noqa: C901 - a flat list of cases reads better than a framework
    import threading

    failures: list[str] = []

    def check(case: str, ok: bool, detail: str = "") -> None:
        print(f"{'ok  ' if ok else 'FAIL'} {case}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(case)

    # 1. Backward envelope parses; rows unnest from citedPaper.
    back = split_rows(_fixture("refs_dmg_edges.json"), "references", "ARXIV:2405.04800")
    check(
        "1  backward envelope unnests from citedPaper",
        back["resolved_count"] == 22 and back["unresolvable_count"] == 3,
        f"got {back['resolved_count']}/{back['unresolvable_count']}, want 22/3",
    )

    # 2. Forward envelope parses; rows unnest from citingPaper.
    fwd = split_rows(_fixture("cites_fire.json"), "citations", "seed-fire")
    check(
        "2  forward envelope unnests from citingPaper",
        fwd["resolved_count"] == 82 and fwd["unresolvable_count"] == 0,
        f"got {fwd['resolved_count']}/{fwd['unresolvable_count']}, want 82/0",
    )

    # 3. The null-paperId rows land in unresolvable, never in the main list.
    titles = {u["title"] for u in back["unresolvable"]}
    check(
        "3  grey literature is separated structurally",
        "Image semantics documentation" in titles
        and all(p["paperId"] for p in back["papers"])
        and all(set(u) == {"title", "venue", "year"} for u in back["unresolvable"]),
        f"unresolvable={sorted(titles)}",
    )

    # 4. contextsWithIntent survives, and each hop labels which paper it is about.
    fwd_edges = split_rows(_fixture("cites_dmg_edges.json"), "citations", "ARXIV:2405.04800")
    withctx = [p for p in back["papers"] if p["edges"][0]["contexts"]]
    fwd_ctx = [p for p in fwd_edges["papers"] if p["edges"][0]["contexts"]]
    sample = withctx[0]["edges"][0] if withctx else {}
    check(
        "4  contextsWithIntent survives, and its direction is labelled",
        bool(withctx)
        and bool(fwd_ctx)
        and isinstance(sample["contexts"][0]["sentence"], str)
        and sample["contexts"][0]["sentence"] != ""
        and isinstance(sample["contexts"][0]["intents"], list)
        and any(e["isInfluential"] for p in back["papers"] for e in p["edges"])
        # backward: the seed's prose about this paper. forward: this paper's
        # prose about the seed. Mixing them puts the wrong sentence on a card.
        and all(e["describes"] == "this_paper" for p in back["papers"] for e in p["edges"])
        and all(e["describes"] == "origin_paper" for p in fwd_edges["papers"] for e in p["edges"]),
        f"{len(withctx)} backward and {len(fwd_ctx)} forward rows carried contexts",
    )

    # 5. openAccessPdf.url == "" is absence, not an empty link.
    raw_rows = [r["citedPaper"] for r in _fixture("refs_dmg_edges.json")["data"]]
    empties = [
        r for r in raw_rows
        if isinstance(r.get("openAccessPdf"), dict) and r["openAccessPdf"].get("url") == ""
    ]
    check(
        "5  empty openAccessPdf url reads as absent",
        bool(empties)
        and all(pdf_url(r) is None for r in empties)
        and any(pdf_url(r) for r in raw_rows if isinstance(r.get("openAccessPdf"), dict)),
        f"{len(empties)} empty-url rows in the fixture",
    )

    # 6. A record round-trips to research/.papers/<paperId>.json and back unchanged.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):
            rec = back["papers"][0]
            wrote = save_record(rec)
            again = load_record(rec["paperId"])
            path = record_path(rec["paperId"]) or ""
            inside = path.startswith(os.path.join(os.path.abspath(tmp), "research", ".papers"))
            escape = record_path("../../../etc/passwd")
            check(
                "6  record round-trips under research/.papers/",
                wrote
                and again == rec
                and inside
                and escape is not None
                and os.path.dirname(escape).endswith(os.path.join("research", ".papers")),
                f"wrote={wrote} equal={again == rec} inside={inside}",
            )

    # 7. Cache key is stable, and distinguishes keyed from unkeyed.
    a = cache_key("GET", BASE + "/paper/X/references?limit=100", None, True)
    b = cache_key("GET", BASE + "/paper/X/references?limit=100", None, True)
    c = cache_key("GET", BASE + "/paper/X/references?limit=100", None, False)
    check("7  cache key stable and key-aware", a == b and a != c, f"{a[:8]} {b[:8]} {c[:8]}")

    # 8. References never expire; citations older than 30 days do.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(S2_CACHE_DIR=tmp):
            cache_write("k", {"data": []})
            stale = time.time() - 400 * DAY
            os.utime(os.path.join(tmp, "k.json"), (stale, stale))
            refs_hit = cache_read("references", "k") is not None
            cites_hit = cache_read("citations", "k") is not None
            batch_hit = cache_read("batch", "k") is not None
            fresh = cache_read("citations", "k", now=stale + 10) is not None
            check(
                "8  expiry is direction-aware",
                refs_hit and not cites_hit and not batch_hit and fresh,
                f"refs={refs_hit} cites={cites_hit} batch={batch_hit} fresh={fresh}",
            )

    # 9. A malformed response returns an error result rather than raising.
    with _fetch(lambda *a, **k: (200, b"<html>not json</html>")):
        bad_json = request("references", "GET", "/paper/X/references")
    with _fetch(lambda *a, **k: (404, b'{"error":"not found"}')):
        not_found = request("references", "GET", "/paper/X/references")
    with _fetch(lambda *a, **k: (200, b'{"ok":true}')):
        no_data = hop("references", "X", 10)
    cases = [bad_json, not_found, no_data]
    check(
        "9  malformed and error responses return, never raise",
        all(isinstance(c, dict) and "error" in c for c in cases)
        and not_found["status"] == 404
        and not_found["attempts"] == 1,
        f"{[str(c)[:60] for c in cases]}",
    )

    # 10. A body-read failure is retried, not raised past the tool.
    #     urlopen succeeding is not the same as the body arriving.
    for exc in (TimeoutError("read timed out"), ConnectionResetError(54, "reset")):
        attempts = {"n": 0}

        def raising(*_a, exc=exc, **_k):
            attempts["n"] += 1
            raise exc

        with _fetch(raising, real=True):
            t0 = time.time()
            out = request("references", "GET", "/paper/X/references")
            elapsed = time.time() - t0
        ok = (
            isinstance(out, dict)
            and "error" in out
            and out["attempts"] == ATTEMPTS
            and out["status"] == 0
            and attempts["n"] == ATTEMPTS
            and type(exc).__name__ in out["error"]
        )
        check(
            f"10 {type(exc).__name__} in the body read is retried, not raised",
            ok,
            f"attempts={attempts['n']} out={str(out)[:90]}",
        )
        if not ok:
            break
    else:
        # And the last attempt does not sleep: 5 attempts means 4 backoffs.
        check(
            "10 no backoff sleep after the final attempt",
            elapsed < (BACKOFF_CAP * (ATTEMPTS - 1)) + 1,
            f"{elapsed:.1f}s",
        )

    # 11. A non-null `next` marks the hop truncated; nothing is dropped silently.
    payload = dict(_fixture("refs_dmg_edges.json"))
    payload["next"] = 25
    payload["data"] = list(payload["data"]) + ["not-a-row", {"citedPaper": "also-not"}]
    trunc = split_rows(payload, "references", "seed")
    full = split_rows(_fixture("refs_dmg_edges.json"), "references", "seed")
    check(
        "11 truncation is surfaced and odd rows are counted, not dropped",
        trunc["truncated"] is True
        and trunc["next"] == 25
        and full["truncated"] is False
        and trunc["malformed_count"] == 2
        and trunc["rows_returned"]
        == trunc["resolved_count"] + trunc["unresolvable_count"] + trunc["malformed_count"],
        f"truncated={trunc['truncated']} malformed={trunc['malformed_count']} "
        f"rows={trunc['rows_returned']}",
    )

    # 12. Concurrent saves of one paper keep both seeds' edges.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):
            base_paper = {"paperId": "concurrent1", "title": "T", "authors": []}
            # Sized to the writers only. The main thread must not wait on it, or
            # it blocks for a second cycle that never comes.
            start = threading.Barrier(6, timeout=30)

            def writer(seed):
                rec = to_record(base_paper, {"origin": seed, "hop": "references", "contexts": []})
                start.wait()
                save_record(rec)

            threads = [threading.Thread(target=writer, args=(f"seed-{i}",)) for i in range(6)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=30)
            final = load_record("concurrent1") or {}
            origins = {e["origin"] for e in final.get("edges", [])}
            leftovers = [f for f in os.listdir(records_dir()) if f.startswith(".tmp-")]
            check(
                "12 concurrent saves keep every seed's edges",
                len(origins) == 6 and not leftovers,
                f"kept {sorted(origins)}, {len(leftovers)} stray temp files",
            )

    print()
    if failures:
        print(f"{len(failures)} of 12 cases failed: {', '.join(failures)}")
        return 1
    print("12 of 12 cases passed")
    return 0


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
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    serve()
