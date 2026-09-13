# Register paper-search on this machine

Type: task
Status: resolved
Blocked by: 

## Question

Register `paper-search-mcp` at user scope with the Unpaywall email and a Semantic Scholar API key (get one at https://www.semanticscholar.org/product/api; ticket 02 found the unauthenticated pool returns 429 after two or three requests, so the key is effectively required), using `uvx --with 'mcp<2' paper-search-mcp`. HITL: the user supplies the email. Resolved when `claude mcp list` shows it connected.

## Key request form answers

Endpoints declared on the Semantic Scholar API key request:

```
/graph/v1/paper/search
/graph/v1/paper/{paper_id}
/graph/v1/paper/{paper_id}/references
/graph/v1/paper/{paper_id}/citations
/graph/v1/paper/batch
/graph/v1/author/{author_id}/papers
```

Key requested 2026-09-12, awaiting approval.

Anticipated volume: 2,000 requests per day. One landscape run is roughly 200 calls (seed searches, detail lookups, one backward and one forward hop over ~30 papers, a few batch calls); development means several partial runs a day. The binding constraint is the 1 request/second rate, not the daily total, so the scout must serialise calls and cache aggressively.

## Resolution

Registered 2026-09-12: `claude mcp add --scope user paper-search -- uvx --with 'mcp<2' paper-search-mcp`. `claude mcp list` shows it connected.

Credentials live in `~/.config/paper-search-mcp/.env` (mode 600), which the server reads itself at startup — no key in `.claude.json`, no key in the plugin's `.mcp.json`, nothing to gitignore. `servers/s2_snowball.py` will read the same file rather than inventing a second home for the Semantic Scholar key.

Both keys arrived and were verified live against the real endpoints:

| Check | Result |
| --- | --- |
| S2 `/graph/v1/paper/search` | 200, 2,325 hits on the acceptance-run topic |
| S2 `/graph/v1/paper/ARXIV:<id>/references` | 200 — the snowball hop works, and `ARXIV:<id>` is accepted as a paper id, confirming ticket 02 |
| CORE `/v3/search/works` | 200 after following a 301 |

`realpath` and `uvx` are both present on this machine, so the macOS uvx-wrapper gotcha in the paper-search-mcp README does not apply.

### Two findings that change chunk 2

1. **CORE's endpoint 301-redirects** `/v3/search/works` → `/v3/search/works/`. A client that does not follow redirects gets an empty body, not an error. Any direct CORE call must send the trailing slash or follow redirects.
2. **CORE is a retrieval source, not a discovery source.** "wildfire spread prediction" returned 2,425,772 hits and the top result was an economics paper on private wildfire-mitigation incentives. But it returns **full text inline** — 60,593 characters on that first hit. So the scout contract should use Semantic Scholar and arXiv for discovery and CORE only to fetch full text for a paper already identified. This is a new capability the plugin did not have when ticket 02 was written: S2 gives metadata and abstracts, CORE gives the actual text.
