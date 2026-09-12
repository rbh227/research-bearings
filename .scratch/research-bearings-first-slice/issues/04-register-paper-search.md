# Register paper-search on this machine

Type: task
Status: open
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

Status note: key requested 2026-09-12, awaiting approval. Anticipated volume: 2,000 requests per day. One landscape run is roughly 200 calls (seed searches, detail lookups, one backward and one forward hop over ~30 papers, a few batch calls); development means several partial runs a day. The binding constraint is the 1 request/second rate, not the daily total, so the scout must serialise calls and cache aggressively.
