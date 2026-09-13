# Snowball by hand

Type: prototype
Status: resolved
Blocked by: 04

## Question

Run one backward and one forward snowball hop on the acceptance-run topic, by hand: seed search through `paper-search-mcp`, then the hops through whatever mechanism ticket 10 picks (ticket 02 found no MCP tool for references or citations), and look at what comes back: metadata quality, duplicates, missing fields, rate-limit behaviour. Purpose: raise fidelity before any scout contract is written.

## Answer

Ran on 2026-09-13 against the live Graph API with the key from
`~/.config/paper-search-mcp/.env`. Two seeds off the acceptance-run topic, found
via `search_semantic`: **DeepDamageNet** (`d7e737d6…`, arXiv 2405.04800, 25 refs
/ 19 cites) and **CNN-BiLSTM wildfire spread** (`df2c6181…`, 37 refs / 82 cites).
One backward and one forward hop on each, plus a third backward hop through the
`ARXIV:2405.04800` alias. Throwaway CLI, not the MCP server — ticket 10 reserved
candidate (b) for exactly this human-attended run.

### 1. The 1 RPS throttle is the wrong design

Ticket 10 wrote its throttle from the documented limit and flagged keyed
behaviour as unexercised. Measured, it does not hold:

| condition | result |
|---|---|
| keyed, 10-call burst, no spacing | 8/10 succeeded — 429 on calls 1 and 2 only |
| keyed, 5 calls at 1.1 s spacing | **4/5 — one 429 anyway** |
| unauthenticated, 6-call burst | 2/6 succeeded |
| `Retry-After` header | **never sent, in any 429, keyed or not** |

429s are not a clean per-key token bucket. Spacing does not prevent them and
retry does; a 1 RPS gate costs wall-clock without buying reliability. Two of the
first three real calls of the session 429'd on attempt 0 and succeeded on
attempt 1. The server should drop the 1 s gate for **retry with exponential
backoff plus jitter, 4+ attempts, and a hard-coded fallback delay** since
`Retry-After` never arrives. The key still matters (2/6 versus 8/10), just not
the way the throttle assumed.

### 2. The two hops return different-quality data, and the asymmetry is age

Not a property of direction — of the decades each hop reaches.

| | backward (refs) | forward (cites) |
|---|---|---|
| year range | 1981–2023 | 2024–2026 |
| unresolvable rows | **3/25 and 2/37 (5–12%)** | 0/82 |
| missing abstract | 48% / 51% | 29% |
| missing venue | 36% / 35% | 0% |
| no DOI | 24% / 8% | **0%** |
| `fieldsOfStudy` missing | 12% | **73%** |
| `openAccessPdf.url` usable | 11/25 | 45/82 |

### 3. Unresolvable rows are grey literature, and they are a dead end

3 of 25 backward rows came back with `paperId: null`, `externalIds: null`,
`authors: []` and every count null — keeping only `title`, `venue`, `year`:
"Image semantics documentation" (venue `Imantics`), a crowdsourced-damage
technical report, and "Crowdai mapping challenge 2018: Baseline with mask rcnn"
(venue `:`). They are real cited works with no S2 record. **A scout cannot hop
from them and cannot dedupe them by id.** The contract needs a rule: keep them
as title-only cards, never follow them, never count them toward the asymptote.

### 4. `contextsWithIntent` is the find of this ticket

Not requested by ticket 10's `FIELDS`. Ask for
`isInfluential,intents,contextsWithIntent` and each reference row carries the
**sentences in which the seed paper describes the cited work**, tagged
`background` / `methodology` / `result`, plus an influence flag (true on 2 of the
first 5). That is a better paper-card field than the abstract — it is the citing
author's own characterization, it survives the 50% missing-abstract rate, and
`intents` gives the scout a free relevance filter before it spends a read.

### 5. Duplicates are not a within-hop problem

Zero duplicate `paperId` and zero duplicate titles inside any single hop. Zero
overlap between a seed's backward and forward sets, and zero between the two
seeds' reference lists. But `POST /paper/batch` **does not collapse aliases**:
passing `ARXIV:2405.04800` alongside its own S2 id returned the same paper as
two rows. So dedupe is needed at two seams only — **across the seven parallel
scouts, and across hop depths** — keyed on `paperId` after alias resolution, not
within one call.

### 6. Smaller facts for the contract

- Envelope is asymmetric: backward carries a top-level `citingPaperInfo`, forward
  has no `citedPaperInfo` counterpart. Rows nest under `citedPaper` /
  `citingPaper` respectively.
- Both hops returned complete at `limit=100` with `next: null` (25, 37, 82 rows).
  Paging is untested and will not bite until a seed with 100+ refs.
- `ARXIV:<id>` works as a hop key on `/references`, confirming ticket 02.
- `openAccessPdf.url` is `""` even when `status` is `GREEN`/`GOLD`; the real URL
  is buried in prose in the `disclaimer` string. Parse the disclaimer or treat
  the field as absent.
- `search_semantic` via paper-search-mcp returns `references`, `keywords` and
  `extra` as empty strings on every row, and `abstract: null` on some — it is a
  seed-finding tool only, not a card source.

### Consequences for the chunk-2 spec

1. Replace the 1 RPS gate with retry + jitter; hard-code the backoff.
2. Add `isInfluential,intents,contextsWithIntent` to the default `fields`, and
   make the context sentences a paper-card field.
3. Give the scout an explicit unresolvable-row rule (title-only, never hop,
   never count).
4. Put dedupe at the merger, keyed on resolved `paperId`, not in the scout.
5. Treat `fieldsOfStudy` as unusable for filtering (73% missing on recent work)
   and `openAccessPdf.url` as unreliable.
