# Snowball mechanism

Type: research
Status: resolved
Blocked by: 

## Question

Ticket 02 found that neither bundled MCP server exposes references or citations, and the snowball hop must call the Semantic Scholar Graph API (`/paper/{id}/references`, `/paper/{id}/citations`, `/paper/batch`). What should the plugin use for the hop? Candidates: (a) an existing MCP server that already exposes references and citations tools, such as one of the `semantic-scholar-mcp` packages on PyPI or GitHub, evaluated for maintenance, SDK version, tool names, key handling, and paging; (b) a small Python script under `scripts/` calling the Graph API with the key, cached, invoked via Bash; (c) a tiny custom MCP server in the plugin wrapping the same three endpoints. Compare on: zero-install path (ticket 01 found Python scripts get no auto-install), whether a scout agent can be denied `Bash` (ticket 03 recommends it), rate-limit handling, and determinism. Recommend one.

## Answer

Full findings: `docs/research/snowball-mechanism.md` on branch `research/snowball-mechanism` (commit aadbab9). Ten servers surveyed; the recommendation was prototyped and verified live.

**Recommended: (c), a single-file MCP server the plugin owns.** `servers/s2_snowball.py`, PEP 723 metadata pinning `mcp>=2,<3`, stdlib HTTP, launched from `.mcp.json` as `uv run --script ${CLAUDE_PLUGIN_ROOT}/servers/s2_snowball.py`. The prototype is 84 lines with three tools (`get_references`, `get_citations`, `get_papers_batch`), verified over stdio: a live references call in 0.38 s, batch in 0.23 s, repeat served from disk cache in 0.00 s, warm startup 0.9 s. Needs only `uv`, which the two bundled servers already require.

It is the only option meeting both hard constraints: scouts can carry `disallowedTools: Bash` because the tools arrive as `mcp__plugin_research-bearings_s2-snowball__*`, and nothing pins the superseded 1.x SDK line. The plugin owns the 1 RPS throttle, `Retry-After` handling, and cache location under `${CLAUDE_PLUGIN_DATA}`.

- **Runner-up: `uvx semantic-scholar-fastmcp` 0.1.2** (zongmin-yu, 166 stars, last commit 2026-03-20). The only PyPI server that starts on a fresh resolve without `--with 'mcp<2'`, since fastmcp pins `mcp<2` itself. Exposes `paper_references`, `paper_citations`, `paper_batch_details` with paging. Caveats: 16 tools of surface, opens a FastAPI bridge on `0.0.0.0:8000` unless disabled, and fastmcp 4 will force a port on the maintainer's schedule.
- Every surveyed Python server targets the v1 SDK. Those with bare `mcp` deps crash under 2.x (reproduced live) and need the pin.
- The official Ai2 Asta remote endpoint has citations but no references tool and no batch, so it cannot do the backward hop.
- **(b), a `scripts/` file via Bash, is rejected for the scout path** because it requires Bash, contradicting ticket 03. It survives as an optional CLI mode of the same file for the human-attended snowball-by-hand ticket.
- Open for `/to-spec`: per-endpoint cache TTL, whether the `fields` list is fixed by contract, key provisioning (`${SEMANTIC_SCHOLAR_API_KEY:-}` versus a sensitive `userConfig` entry), and a session-announce warning when the key is missing.
- Not exercised: keyed 1 RPS behaviour, since no key exists on this machine yet. The throttle is written from the documented limit, not measured.
