# Retrieval tool inventory

Type: research
Status: resolved
Blocked by: 

## Question

What tools do `paper-search-mcp` and `openreview-mcp` expose, with exact names, parameters, and return shapes? Given a seed paper, what sequence of calls performs one backward and one forward snowball hop? What rate limits and keys apply? Source: the package READMEs and code, and the live tool listings from the registered servers.

## Answer

Full findings: `docs/research/retrieval-tool-inventory.md` on branch `research/retrieval-tool-inventory` (commit 797e9f6), from live `tools/list` calls and the package source.

- **Neither server exposes a references or citations tool.** `paper-search-mcp` 0.1.4 registers 57 tools, all `search_*`, `download_*`, `read_*_paper`, plus `search_papers`, `download_with_fallback`, `download_scihub`, `get_crossref_paper_by_doi`. Its Semantic Scholar connector only calls `/graph/v1/paper/search` and `/graph/v1/paper/{id}`. `openreview-mcp` 0.1.0 registers 11 tools for venues, submissions, reviews, meta-reviews, rebuttals, decisions, profiles, and weakness aggregation.
- Seed search: `search_semantic(query, year=None, max_results=10)` returns the S2 sha as `paper_id`. `search_papers(query, sources="semantic,...")` also works.
- The snowball hop must call the Semantic Scholar Graph API directly: `GET /graph/v1/paper/{id}/references` (backward), `GET /graph/v1/paper/{id}/citations` (forward), `limit<=1000` with paging, then `POST /graph/v1/paper/batch` (500 ids) to materialise the frontier. `Paper.to_dict()` has a `references` key no connector fills.
- arXiv-only papers snowball fine via `ARXIV:<id>` (verified live). Frontier nodes often lack DOIs; dedupe on `paperId` or `CorpusId`.
- Semantic Scholar key is effectively required: the unauthenticated pool hit HTTP 429 after two or three requests, and the connector swallows 429s into an empty list. Keyed limit is 1 request per second. Env var `PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_API_KEY`.
- Unpaywall email is mandatory; the API returns 422 without it. Daily cap unverified.
- OpenReview is anonymous for public venues, caches to disk with 6 h to 7 d TTLs, and downloads a whole venue on first search.
- `download_with_fallback` defaults `use_scihub=True`; the plugin must pass `False`.
