#!/usr/bin/env python3
"""snowball — the citation walker for research-bearings, as a script.

Search, then hop, over the Semantic Scholar Graph API. Standard library only.
Every invocation is one process that prints one JSON result and exits; nothing
stays resident. Chunk 2 shipped this same code as an MCP server, and the server
turned out to be the wrong packaging: a persistent process, a dependency tree,
credentials in a file the eval sandbox could not see, and a 30 s cold start that
broke the suite. The methodology is unchanged; only the wrapper is gone.

  snowball.py health                    [--run R]
  snowball.py search "query"            [--limit N] [--run R] [--budget N]
  snowball.py references <id>           [--limit N] [--run R] [--budget N]
  snowball.py citations  <id>           [--limit N] [--run R] [--budget N]
  snowball.py batch <id> [<id> ...]                 [--run R] [--budget N]
  snowball.py --selftest                            (offline, seconds)

Environment:
  SEMANTIC_SCHOLAR_API_KEY  or one line in ~/.config/research-bearings/s2-api-key.
                            Optional. Without it the API 429s after a few calls;
                            the retry policy absorbs some of that, coverage drops,
                            and the scout stamps the section as degraded.
  S2_CACHE_DIR              raw responses keyed by request hash, disposable,
                            direction-aware expiry. Default ~/.cache/research-bearings/s2
  RESEARCH_PROJECT_DIR      the project whose research/ receives records and the
                            ledger. Default CLAUDE_PROJECT_DIR, else cwd.

Two on-disk artifacts under <project>/research/:
  .papers/<paperId>.json      one record per paper touched, written here rather
                              than by the scout: several hundred records through a
                              model's context costs tokens and invites transcription.
  .crawl/<run>.touched.json   the budget ledger: distinct resolved paperIds this run
                              has been handed. `--budget` refuses a hop once the
                              ledger reaches it, BEFORE spending the request. The
                              ceiling used to be a sentence in the agent's prompt;
                              told 40, it touched 114-160. Now it is a file.
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
TTL = {"references": None, "citations": 30 * DAY, "batch": 90 * DAY, "search": 7 * DAY}

BATCH_MAX = 500
HOP_MAX = 100
SEARCH_MAX = 100

NESTED = {"references": "citedPaper", "citations": "citingPaper"}

# --------------------------------------------------------------------------
# the budget
#
# "Papers touched" was a sentence in the agent's contract and nothing else, so
# it did not hold: measured 2026-09-13, three eval runs told to stop at 40
# touched 114, 130 and 160. An instruction a model can be optimistic about is
# not a limit. So the script counts, and because each call is its own process
# the count lives on disk: <project>/research/.crawl/<run>.touched.json holds
# the DISTINCT resolved paperIds this run has been handed. Once it reaches the
# caller's ceiling, hop and batch refuse before spending a request.
#
# Unresolvable rows are never counted, matching the agent contract: they carry
# title, venue and year only and cannot be hopped from. Search rows are not
# counted either - seeds are found, not touched (CONTEXT.md).


def ledger_path(run: str) -> str | None:
    safe = "".join(c for c in (run or "") if c.isalnum() or c in "-_")
    if not safe:
        return None
    return os.path.join(os.path.dirname(records_dir()), ".crawl", safe + ".touched.json")


def ledger_load(run: str) -> set[str] | None:
    """The run's ledger. An empty set when there is none yet; None when there is
    one and it cannot be trusted - unreadable or corrupt. None stops the crawl:
    treating a corrupt ledger as empty would quietly restart the budget."""
    path = ledger_path(run)
    if not path or not os.path.exists(path):
        return set()
    try:
        with open(path, encoding="utf-8") as fh:
            ids = json.load(fh)
    except (OSError, ValueError):
        return None
    return {str(i) for i in ids} if isinstance(ids, list) else None


def ledger_open(run: str) -> tuple[set[str], dict[str, Any] | None]:
    """Load the ledger and prove it can be written, BEFORE any request is spent.
    Adversarial review 2026-09-13: a ledger that could not be written let three
    papers through a budget of two with every response reporting success."""
    seen = ledger_load(run)
    path = ledger_path(run)
    if seen is None:
        return set(), err(
            f"ledger unreadable or corrupt: {path}. Not spending a request against "
            f"a budget that cannot be counted. Move or delete it to restart the run."
        )
    try:
        write_atomic(path, sorted(seen))
    except OSError as exc:
        return set(), err(f"ledger not writable: {path}: {exc}. Refusing to crawl uncounted.")
    return seen, None


def budget_block(touched: int, budget: int) -> dict[str, Any]:
    """The accounting every response carries."""
    out: dict[str, Any] = {"touched_total": touched}
    if budget > 0:
        out["budget"] = budget
        out["budget_remaining"] = max(0, budget - touched)
        out["budget_exhausted"] = touched >= budget
    return out


def charge(run: str, seen: set[str], records: list[dict[str, Any]], budget: int) -> dict[str, Any]:
    """Add these records to the run's ledger and report where the budget stands.
    Raises OSError if the ledger cannot be written: the caller turns that into a
    stop, because a count that did not land is not a count."""
    ids = {r["paperId"] for r in records if r.get("paperId")}
    if not run:
        return budget_block(len(ids), 0)
    seen = seen | ids
    write_atomic(ledger_path(run), sorted(seen))
    return budget_block(len(seen), budget)


def uncounted(run: str, exc: OSError, written: int) -> dict[str, Any]:
    out = err(
        f"ledger write failed after the request: {exc}. The rows are saved under "
        f"research/.papers/ but were NOT counted; stop the crawl, the budget is untrustworthy."
    )
    out["records_written"] = written
    out["ledger"] = ledger_path(run)
    return out


def refusal(what: str, budget: int, touched: int, **extra: Any) -> dict[str, Any]:
    return {
        "stopped": "budget",
        "message": (
            f"budget of {budget} papers touched is exhausted ({touched} touched). "
            f"No {what} was made. Write the section now with stop reason `budget`, "
            f"and say it is INCOMPLETE."
        ),
        "papers": [],
        "unresolvable": [],
        "resolved_count": 0,
        "unresolvable_count": 0,
        **extra,
        **budget_block(touched, budget),
    }


def err(message: str, attempts: int = 0, status: int | None = None) -> dict[str, Any]:
    """The one error shape. Tools return it; they never raise, because a tool
    that throws leaves the model to invent what happened."""
    return {"error": message, "attempts": attempts, "status": status}


# --------------------------------------------------------------------------
# environment


KEY_FILE = "~/.config/research-bearings/s2-api-key"


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
    """The project whose research/ receives records and the ledger.

    RESEARCH_PROJECT_DIR, else CLAUDE_PROJECT_DIR (set for every Bash call
    Claude Code makes), else cwd. One resolution, because `health` used to
    report only the first of the three and so printed null for a run whose
    ledger was landing somewhere real."""
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


def hop(
    hop_name: str, paper_id: str, limit: int, budget: int = 0, run: str = ""
) -> dict[str, Any]:
    paper_id = (paper_id or "").strip()
    if not paper_id:
        return err("paper_id is required")
    budget = max(0, int(budget or 0))
    seen: set[str] = set()
    if run:
        seen, problem = ledger_open(run)
        if problem:
            return problem
        if budget and len(seen) >= budget:
            # Refused BEFORE the request, not after. Stopping a crawl that has
            # already spent the call teaches the agent nothing.
            return refusal("hop", budget, len(seen), seed=paper_id, hop=hop_name)
    limit = max(1, min(int(limit or HOP_MAX), HOP_MAX))
    if budget and run:
        # Size the request to what the ledger leaves. The agent is told to do
        # this too; doing it here makes an overshoot impossible, not unlikely.
        limit = max(1, min(limit, budget - len(seen)))
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
    try:
        out.update(charge(run, seen, out["papers"], budget))
    except OSError as exc:
        return uncounted(run, exc, out["records_written"])
    return out


def batch_papers(ids: list[str], budget: int = 0, run: str = "") -> dict[str, Any]:
    ids = [str(i).strip() for i in (ids or []) if str(i).strip()]
    if not ids:
        return err("ids is required")
    budget = max(0, int(budget or 0))
    ledger: set[str] = set()
    deferred: list[str] = []
    if run:
        ledger, problem = ledger_open(run)
        if problem:
            return problem
        if budget and len(ledger) >= budget:
            return refusal("batch", budget, len(ledger), ids=ids)
        if budget:
            # A batch is a way to pull 500 papers into the model's context in
            # one call, which is exactly what the budget caps. Ids already in
            # the ledger are free; fresh ones are capped to what remains, and
            # the rest are handed back rather than dropped. Adversarial review
            # 2026-09-13: 100 papers came through a budget of 5 without this.
            fresh = [i for i in ids if i not in ledger]
            known = [i for i in ids if i in ledger]
            remaining = budget - len(ledger)
            deferred = fresh[remaining:]
            ids = known + fresh[:remaining]
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
    out = {
        "papers": deduped,
        "unresolvable_ids": unresolvable_ids,
        "resolved_count": len(deduped),
        "unresolvable_count": len(unresolvable_ids),
        "alias_rows_collapsed": aliases,
        "records_written": save_all(deduped),
        "deferred_ids": deferred,
        "deferred_count": len(deferred),
    }
    try:
        out.update(charge(run, ledger, deduped, budget))
    except OSError as exc:
        return uncounted(run, exc, out["records_written"])
    return out


def search(query: str, limit: int = 20, budget: int = 0, run: str = "") -> dict[str, Any]:
    """Seed papers by keyword. Rows are seeds, never cards: search results carry
    no citation edge, so there is no `Cited as` sentence to put on one. They do
    not charge the budget - seeds are found, not touched - but the response still
    reports where the ledger stands so the caller sizes the first hop right."""
    query = (query or "").strip()
    if not query:
        return err("query is required")
    budget = max(0, int(budget or 0))
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
    out.update(budget_block(len(ledger_load(run) or set()) if run else 0, budget))
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


RESOLVING_MATCHES = ("exact", "prefix", "substring")


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
        ranked = sorted(
            ((title_match(asked, p.get("title") or ""), p) for p in found["papers"]),
            key=lambda pair: RESOLVING_MATCHES.index(pair[0]) if pair[0] in RESOLVING_MATCHES else 9,
        )
        best_match, best = ranked[0] if ranked else ("none", None)
        ok = best_match in RESOLVING_MATCHES
        results.append({
            "query": asked,
            "kind": "title",
            "resolved": ok,
            "paperId": best["paperId"] if ok and best else None,
            "title": best["title"] if best else None,
            "year": best["year"] if best else None,
            # On a miss the closest row is still reported: a near-miss is a
            # typo to fix, a blank is a paper that is not there.
            "match": best_match if ok else (
                f"no title match in {found['rows_returned']} rows"
                + (f"; closest: {best['title']}" if best else "")
            ),
        })

    resolved = sum(1 for r in results if r["resolved"])
    return {
        "results": results,
        "resolved_count": resolved,
        "unresolved_count": len(results) - resolved,
        "checked": len(results),
    }


def health(run: str = "") -> dict[str, Any]:
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
        "run": run or None,
        "touched_total": len(ledger_load(run) or set()) if run else None,
        "ledger_ok": (ledger_load(run) is not None) if run else None,
    }


# --------------------------------------------------------------------------
# command line


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="snowball.py",
        description="Semantic Scholar search, citation hops and citation checking. One JSON result per call.",
    )
    ap.add_argument("--selftest", action="store_true", help="offline checks, then exit")
    sub = ap.add_subparsers(dest="cmd")

    def scoped(p: argparse.ArgumentParser) -> None:
        p.add_argument("--run", default="", help="run slug; scopes the touched ledger")
        p.add_argument("--budget", type=int, default=0, help="papers-touched ceiling; needs --run")

    scoped(sub.add_parser("health", help="key presence, paths, ledger size; no network"))
    p = sub.add_parser("search", help="seed papers by keyword")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=20)
    scoped(p)
    for name, blurb in (("references", "papers this one cites"), ("citations", "papers citing this one")):
        p = sub.add_parser(name, help=f"{blurb}; one hop")
        p.add_argument("paper_id", help="S2 id, ARXIV:<id>, or DOI:<doi>")
        p.add_argument("--limit", type=int, default=HOP_MAX)
        scoped(p)
    p = sub.add_parser("batch", help="metadata for many ids at once")
    p.add_argument("ids", nargs="+")
    scoped(p)
    p = sub.add_parser("verify", help="do these papers exist? by title or id; charges no budget")
    p.add_argument("--title", action="append", default=[], help="repeatable")
    p.add_argument("--id", action="append", default=[], dest="ids", help="repeatable")
    p.add_argument("--limit", type=int, default=5, help="search rows to consider per title")

    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.cmd:
        ap.print_help()
        return 2

    # verify takes no --run/--budget: it charges nothing, so the scoped pair is
    # absent from its parser and this guard must not assume every verb has them.
    if getattr(args, "budget", 0) and not getattr(args, "run", ""):
        out: dict[str, Any] = err("--budget needs --run: the ledger that enforces it is per run")
    elif args.cmd == "health":
        out = health(args.run)
    elif args.cmd == "search":
        out = search(args.query, args.limit, args.budget, args.run)
    elif args.cmd in ("references", "citations"):
        out = hop(args.cmd, args.paper_id, args.limit, args.budget, args.run)
    elif args.cmd == "verify":
        out = verify(args.title, args.ids, args.limit)
    else:
        out = batch_papers(args.ids, args.budget, args.run)

    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


# --------------------------------------------------------------------------
# selftest


FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _fixture(name: str) -> dict[str, Any]:
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return json.load(fh)


def selftest() -> int:  # noqa: C901 - a flat list of cases reads better than a framework
    import threading

    failures: list[str] = []
    # Every case that touches the network goes through a stub, and a real
    # response cached from an earlier run would bypass the stub silently. So
    # the selftest gets its own empty cache and its own empty project.
    os.environ["S2_CACHE_DIR"] = tempfile.mkdtemp(prefix="snowball-cache-")
    os.environ["RESEARCH_PROJECT_DIR"] = tempfile.mkdtemp(prefix="snowball-project-")

    ran: list[str] = []

    def check(case: str, ok: bool, detail: str = "") -> None:
        ran.append(case)
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

    # 13. The budget is counted by the script, in a ledger, and refuses before spending a call.
    #     This is the case that would have caught the 2026-09-13 overrun: the
    #     agent was told 40 and touched 114-160, because nothing enforced it.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):
            calls = {"n": 0}

            def counting_stub(method, url, body, key):
                calls["n"] += 1
                return 200, json.dumps(_fixture("refs_dmg_edges.json")).encode()

            with _fetch(counting_stub):
                first = hop("references", "ARXIV:2405.04800", 100, budget=5, run="t")
                after_first = calls["n"]
                second = hop("references", "ARXIV:2011.10328", 100, budget=5, run="t")
            check(
                "13 the budget refuses the next hop, before the network call",
                first.get("resolved_count", 0) > 5
                and first["limit"] == 5  # asked for 100, clamped to the 5 the budget leaves
                and first["touched_total"] == first["resolved_count"]
                and first["budget_exhausted"] is True
                and second.get("stopped") == "budget"
                and second["resolved_count"] == 0
                and calls["n"] == after_first,
                f"first={first.get('resolved_count')} touched={first.get('touched_total')} "
                f"second={second.get('stopped')} calls={calls['n']} (expected {after_first})",
            )

    # 14. Touched counts DISTINCT papers, so re-hopping the same edge list does
    #     not double-charge, and an absent budget enforces nothing.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):

            def same(method, url, body, key):
                return 200, json.dumps(_fixture("refs_dmg_edges.json")).encode()

            with _fetch(same):
                a = hop("references", "seedA", 100, budget=0, run="t2")
                b = hop("references", "seedB", 100, budget=0, run="t2")
            check(
                "14 touched counts distinct papers; no budget enforces nothing",
                a["touched_total"] == b["touched_total"] == a["resolved_count"]
                and "budget_remaining" not in a
                and b.get("stopped") is None,
                f"a={a['touched_total']} b={b['touched_total']} resolved={a['resolved_count']}",
            )

    # 15. A search envelope parses into seed records; a held-back page is flagged.
    found = split_search(_fixture("search_dmg.json"), "building damage", 5)
    unpaged = dict(_fixture("search_dmg.json"))
    unpaged.pop("next", None)
    check(
        "15 search rows become seed records, and paging is surfaced",
        found["resolved_count"] == found["rows_returned"] > 0
        and all(p["paperId"] and p["title"] for p in found["papers"])
        and all(p.get("edges") in (None, []) for p in found["papers"])
        and found["truncated"] is True  # the fixture is 5 of 2461; the API held the rest back
        and split_search(unpaged, "q", 5)["truncated"] is False,
        f"resolved={found['resolved_count']} rows={found['rows_returned']}",
    )

    # 16. The key comes from the environment, else from one file, else nowhere.
    with tempfile.TemporaryDirectory() as home:
        os.makedirs(os.path.join(home, ".config", "research-bearings"))
        with open(os.path.join(home, ".config", "research-bearings", "s2-api-key"), "w") as fh:
            fh.write("from-file\n")
        with _env(HOME=home, SEMANTIC_SCHOLAR_API_KEY=""):
            from_file = api_key()
        with _env(HOME=home, SEMANTIC_SCHOLAR_API_KEY="from-env"):
            from_env = api_key()
        with _env(HOME=tempfile.mkdtemp(), SEMANTIC_SCHOLAR_API_KEY=""):
            nothing = api_key()
        check(
            "16 the key is read from the environment, then the key file",
            from_file == "from-file" and from_env == "from-env" and nothing == "",
            f"file={from_file!r} env={from_env!r} none={nothing!r}",
        )

    # 17. Rows with no edge fields at all still parse; the card simply has no
    #     sentence to quote. This is the pre-edge-field capture from ticket 09.
    bare = split_rows(_fixture("refs_dmg.json"), "references", "ARXIV:2405.04800")
    check(
        "17 rows without citation contexts parse, with empty edges",
        bare["resolved_count"] == 22
        and bare["unresolvable_count"] == 3
        and all(p["edges"] and p["edges"][0]["contexts"] == [] for p in bare["papers"])
        and all(p["edges"][0]["describes"] == "this_paper" for p in bare["papers"]),
        f"resolved={bare['resolved_count']} unresolvable={bare['unresolvable_count']}",
    )

    # 18. A batch is capped to what the budget leaves; the rest is deferred, not dropped.
    #     Adversarial review 2026-09-13: 100 papers came through a budget of 5.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):
            write_atomic(ledger_path("b"), ["p1", "p2", "p3"])
            asked = {"ids": None}

            def echo(method, url, body, key):
                asked["ids"] = list(body["ids"])
                return 200, json.dumps([{"paperId": i, "title": i, "authors": []} for i in body["ids"]]).encode()

            with _fetch(echo):
                out = batch_papers([f"n{i}" for i in range(10)], budget=5, run="b")
            check(
                "18 a batch is capped to the remaining budget and defers the rest",
                asked["ids"] == ["n0", "n1"]
                and out["resolved_count"] == 2
                and out["deferred_count"] == 8
                and out["touched_total"] == 5
                and out["budget_exhausted"] is True,
                f"asked={asked['ids']} resolved={out.get('resolved_count')} deferred={out.get('deferred_count')} touched={out.get('touched_total')}",
            )

    # 19. A ledger that cannot be read or written stops the crawl before a request
    #     is spent. Silently restarting the budget was the review's third finding.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):
            calls = {"n": 0}

            def counting(method, url, body, key):
                calls["n"] += 1
                return 200, json.dumps(_fixture("refs_dmg_edges.json")).encode()

            os.makedirs(os.path.dirname(ledger_path("c")), exist_ok=True)
            with open(ledger_path("c"), "w") as fh:
                fh.write("{not json")
            with _fetch(counting):
                corrupt = hop("references", "X", 10, budget=5, run="c")
            crawl_dir = os.path.dirname(ledger_path("d"))
            os.makedirs(crawl_dir, exist_ok=True)
            os.chmod(crawl_dir, 0o500)
            try:
                with _fetch(counting):
                    unwritable = hop("references", "X", 10, budget=5, run="d")
            finally:
                os.chmod(crawl_dir, 0o700)
            check(
                "19 an unreadable or unwritable ledger refuses before the request",
                "error" in corrupt and "corrupt" in corrupt["error"]
                and "error" in unwritable and "not writable" in unwritable["error"]
                and calls["n"] == 0,
                f"corrupt={str(corrupt)[:70]} unwritable={str(unwritable)[:70]} requests={calls['n']}",
            )

    # 20-25. verify: the citation check chunk 3's posture rests on. A model
    #        that names a paper from memory is fine; a paper that does not
    #        exist reaching the page is not.
    xbd = "Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery"
    search_payload = {"total": 1, "data": [{
        "paperId": "ec58b5946c57f7d4d4a3cff0566941bb93291c95", "title": xbd,
        "year": 2019, "venue": "CVPR Workshops", "authors": [{"name": "R. Gupta"}],
        "externalIds": {"DOI": "10.1184/R1/8135576.V1"},
    }]}

    with _fetch(lambda *a, **k: (200, json.dumps(search_payload).encode())):
        exact = verify([xbd], [])
        variant = verify(["creating xBD - a dataset for assessing building damage from satellite imagery"], [])
    check(
        "20 an exact title resolves",
        exact["resolved_count"] == 1 and exact["results"][0]["match"] == "exact"
        and exact["results"][0]["paperId"] == "ec58b5946c57f7d4d4a3cff0566941bb93291c95",
        f"got {exact['results'][0]}",
    )
    check(
        "21 punctuation and case do not break a title match",
        variant["resolved_count"] == 1 and variant["results"][0]["match"] == "exact",
        f"got {variant['results'][0]['match']}",
    )

    with _fetch(lambda *a, **k: (200, json.dumps(search_payload).encode())):
        missing = verify(["A Unified Theory of Nothing Whatsoever"], [])
    check(
        "22 a title with no match is unresolved, and names the closest row",
        missing["resolved_count"] == 0
        and missing["results"][0]["resolved"] is False
        and "closest" in missing["results"][0]["match"]
        and missing["results"][0]["paperId"] is None,
        f"got {missing['results'][0]['match']}",
    )

    batch_payload = [{
        "paperId": "ec58b5946c57f7d4d4a3cff0566941bb93291c95", "title": xbd, "year": 2019,
        "externalIds": {"DOI": "10.1184/R1/8135576.V1", "ArXiv": None},
    }, None]
    with _fetch(lambda *a, **k: (200, json.dumps(batch_payload).encode())):
        ids = verify([], ["ec58b5946c57f7d4d4a3cff0566941bb93291c95", "DOI:10.0000/nope"])
    check(
        "23 a good id resolves and a bad one does not, each named",
        ids["resolved_count"] == 1 and ids["unresolved_count"] == 1
        and ids["results"][0]["resolved"] is True
        and ids["results"][1]["resolved"] is False
        and ids["results"][1]["query"] == "DOI:10.0000/nope",
        f"got {ids['results']}",
    )

    with _fetch(lambda method, url, body, key: (
        200, json.dumps(batch_payload if "batch" in url else search_payload).encode())):
        mixed = verify([xbd, "A Unified Theory of Nothing Whatsoever"],
                       ["ec58b5946c57f7d4d4a3cff0566941bb93291c95"])
    check(
        "24 a mixed batch reports every row, in order, ids first",
        mixed["checked"] == 3 and mixed["resolved_count"] == 2
        and [r["kind"] for r in mixed["results"]] == ["id", "title", "title"],
        f"got {[(r['kind'], r['resolved']) for r in mixed['results']]}",
    )

    # 25. Verification is not discovery: it must not spend the crawl's budget.
    with tempfile.TemporaryDirectory() as tmp:
        with _env(RESEARCH_PROJECT_DIR=tmp):
            with _fetch(lambda *a, **k: (200, json.dumps(search_payload).encode())):
                verify([xbd], [])
            after = ledger_load("v") or set()
    check(
        "25 verify charges no ledger",
        after == set() and "error" in verify([], []),
        f"ledger={len(after)}",
    )

    # 26. The CLI reaches verify. Case 20 called the function; this calls the
    #     command, which is where a verb missing --run/--budget first broke.
    argv_out: dict[str, Any] = {}
    with _fetch(lambda *a, **k: (200, json.dumps(search_payload).encode())):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["verify", "--title", xbd])
        try:
            argv_out = json.loads(buf.getvalue())
        except ValueError:
            argv_out = {}
    check(
        "26 the CLI dispatches verify and prints JSON",
        rc == 0 and argv_out.get("resolved_count") == 1,
        f"rc={rc} out={buf.getvalue()[:120]!r}",
    )

    print()
    if failures:
        print(f"{len(failures)} of {len(ran)} cases failed: {', '.join(failures)}")
        return 1
    print(f"{len(ran)} of {len(ran)} cases passed")
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
    sys.exit(main())
