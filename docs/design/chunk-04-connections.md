# Chunk 4: connections

2026-09-15. The retrieval script stops being a Semantic Scholar client and
becomes a client of four indexes that degrade into each other, and the plugin
learns to say which of seven sources it can reach before any skill searches.
The reference for the sources themselves is `docs/APIS.md`.

## 1. Decision record

- **Why now.** Chunk 3's live checks kept hitting one wall: Semantic Scholar
  unkeyed 429s after two or three calls, and every verb was built on it alone.
  A `verify` that cannot reach its only index certifies nothing, and a search
  that returns zero rows for that reason looks, in the file, exactly like a
  field with no literature. Chunk 2 (`/landscape`, seven searchers in
  parallel) would have multiplied that by seven.
- **Degrade, never error.** A missing key is a state, reported and adapted to.
  `search` merges S2 and OpenAlex and names the index that failed under
  `degraded`; `verify` tries S2, then OpenAlex, then Crossref, and records the
  errors per index; `status` exits 0 whatever it finds. The only thing that is
  an error is a malformed answer or an exhausted retry, and those are still
  returned as a result, not raised.
- **Exact match only, everywhere.** The chunk 3 rule extends across three
  indexes unchanged. A prefix or substring match from any of them is a
  `candidate`, named with its id, never resolved, and the templates gain a
  `_candidate: …_` marker so a card can carry it without carrying the id.
- **Keys from the environment, one file for one of them.** `S2_API_KEY` (and
  the older name, and the key file, for continuity), `OPENALEX_API_KEY`,
  `OPENALEX_MAILTO`, `CROSSREF_MAILTO`, `UNPAYWALL_EMAIL`, `HF_TOKEN`,
  `ZOTERO_API_KEY`, `ZOTERO_USER_ID`. No plugin config, no secrets store: a
  variable the user can `echo`.
- **Pacing is per source and across processes.** Keyed S2 is 1 request per
  second, arXiv is one per 3 seconds, and seven parallel searchers must share
  both. A timestamp file per resolver, held under a lock for the wait, gives
  that without a server. Unkeyed S2 is not paced: ticket 09 measured spacing as
  useless there and retry with jitter as what works.
- **One cache, per resolver, 30 days.** `~/.cache/research-bearings/<resolver>/`,
  keyed by the full query, overridable with `RESEARCH_CACHE_DIR`. The
  direction-aware TTLs of chunk 2 (references never expire, citations 30 days)
  collapse to one number: the hops that justified them are chunk 2's to bring
  back, and 30 days is the shorter of the two. `status` bypasses the cache; it
  is the one verb whose job is the wire.
- **Web search is fenced by the guard, not by prose.** Two exceptions, named
  in `docs/APIS.md`: the `searcher` agent's `WebSearch` as a last resort, and
  `/scout`'s `WebFetch` of a page an index pointed at. The guard's PreToolUse
  matcher now covers `WebSearch|WebFetch` and denies both to every plugin
  agent except `searcher`, which gets `WebSearch` only. `/scout` runs in the
  main thread, which the guard never touches, so its `WebFetch` is the
  skill's allowed-tools grant. This is the ARS lesson again: the guard is the
  only enforcement that is not prompt text, so the rule that matters most goes
  there.
- **`/setup` reports and stops.** A connections step runs `status --md`,
  writes `research/CONNECTIONS.md` from it verbatim, names the three keys that
  would help most, and moves on. It does not ask the user to get a key and
  does not wait for one. `status` computes the three (`suggest`) from a fixed
  priority order, so the skill copies rather than judges.

## 2. What ships

| Piece | Change |
|---|---|
| `scripts/retrieval/snowball.py` | rewritten around a generic `fetch` (cache, pace, retry) and four resolvers; verbs `status`, `search --index`, `openalex …`, `crossref …`, `arxiv search`; `verify` across three indexes with `match: candidate`; unified record with `key`, `sources`, `externalIds.OpenAlex`; 35 offline cases on captured fixtures from all four sources |
| `docs/APIS.md` | new: every source, its env var, where to get it, its rate, its one-line test, and the web rule |
| `templates/research/CONNECTIONS.md` | new: `## Sources`, `## Keys that would help most`, both pasted from `status --md` |
| `skills/setup/SKILL.md` | step 1b, the connections step; three refusals |
| `skills/scout/SKILL.md` | reads `CONNECTIONS.md` first; `degraded` stamped, not treated as an empty field; candidate marker; `WebFetch` for one purpose; two refusals; stale `/snowball` references replaced with `/landscape` |
| `templates/research/analogs.md`, `CONTEXT.md` | candidate line, other id forms, degraded indexes in `## Status`; retrieval section points at `CONNECTIONS.md` |
| `hooks/guard.py`, `hooks/hooks.json` | web fence, five cases |
| `scripts/check_analogs.py` | OpenAlex ids and candidate lines are checked lines; nine cases |
| `scripts/check_headings.py` | `CONNECTIONS.md` → `/setup` |
| `CONTEXT.md` (root glossary) | connection terms |

Nothing deleted. The S2-only `verify` and `search` are subsumed, not removed;
`health` keeps its `key_present` field because `/setup` and `/scout` read it.

## 3. Done-check, run 2026-09-15

All three by hand, live, with `HOME` pointed at an empty directory so the key
file could not leak in.

1. **`status` with no keys.** Exit 0. Seven lines: arXiv `connected`; the
   other six `connected-no-key`; `suggest` named `S2_API_KEY`,
   `OPENALEX_MAILTO`, `CROSSREF_MAILTO` with their links. With the key file
   present, Semantic Scholar moved to `connected` and the suggestions moved on.
   Whole probe under 600 ms.
2. **A query with no keys.** `search "post-disaster building damage assessment
   satellite imagery" --limit 5`: five rows, all from OpenAlex, S2 reported
   under `degraded` with its 429 after five attempts. The result is a result.
3. **`verify` on "Attention Is All You Need for Wildfire Damage Assessment".**
   `match: candidate`, `resolved_count 0`, `candidate_count 1`; the candidate
   is a prefix match on a 2025 Crossref record titled "Attention Is All You
   Need", named with its DOI, and no id carried onto the asked title.

Two things the live run taught, both fixed before the check passed:

- **S2's zero-hit shape has no `data` array.** `{"total": 0, "offset": 0}`.
  The script had treated that as malformed since chunk 2, which turned every
  zero-hit search into an error. Case 5b.
- **The near match is often below the top five.** Crossref returned the
  short title as row 10 for the wildfire variant; at `--limit 5` there was no
  candidate to report. `verify` now considers ten rows per index per title.
  Same number of requests.

And one fact about the record: xBD's DOI is a DataCite DOI, so Crossref does
not hold it and `crossref search` cannot confirm the field's founding dataset.
The status probe uses a journal DOI for that reason, and `verify`'s order
(S2, OpenAlex, then Crossref) means Crossref only decides when the two indexes
have not.

## 4. Open

- Unpaywall, Hugging Face and Zotero are probed and not used. Their first verb
  lands with the skill that needs it (`/read` for PDFs, `/datasets` for the
  Hub, a library cross-check for Zotero), not before.
- `search --index all` does not include arXiv, because its 3-second pacing
  would slow every search. A skill that wants arXiv asks for it by name.
