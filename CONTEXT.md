# CONTEXT.md

Glossary for the research plugin effort. One meaning per word.

## Terms

- **map**: The wayfinder planning artifact for an effort, under `.scratch/<effort>/map.md`, with one child ticket per decision. Never used for anything the plugin produces.
- **landscape**: The plugin's Milestone 1 deliverable for a research question: the surveys diff, the concept matrix, the time slice, and the brief. The build plan's "map chain" is the sequence of skills that produces a landscape.
- **ticket**: A wayfinder child issue holding one decision or investigation. Not a plugin concept.
- **destination**: What a map is finding its way to. For this effort: Milestones 0 and 1 specified sharply enough to hand to `/to-spec`.
- **research-bearings**: The plugin this effort is building. A Claude Code plugin whose typed skills and contract-bound agents run the research loop; Milestone 1 produces a landscape.
- **acceptance run**: A trial of the built plugin on a real research question, performed by the user after handoff. Not part of any map; it produces the next map's loose idea.

## Retrieval terms

Added with chunk 2 for a snowballing skill, replaced with chunk 3's when that
skill was deleted (2026-09-14). All of these describe one `/research-bearings:scout`
run.

- **shape**: The problem written without the home field's nouns — what it is structurally, in words any field would recognise. The one step nothing else in the plugin does, and the rest of a run is only as good as it.
- **field**: One area that shares the shape and not the vocabulary, searched in its own words. A field whose papers would plausibly cite your seeds is not a field, it is the home field with a wider collar.
- **home vocabulary**: The words `## Vocabulary` in `research/QUESTION.md` lists. Stripped in step 1, banned from field names, and never used as a query — a query in your own words finds your own field.
- **transfer**: Why a field's method might move to your problem, and what is different about it. Grounded in the rows the search returned.
- **opportunity**: What you would actually try, per field. The one speculative thing in the file, and labelled as such.
- **nearest existing**: The opportunity put to the index, with a row count and the closest title. This is the only shape an absence claim may take here; "unexplored", "gap", "novel" and "nobody" do not appear at all.
- **verify**: Resolving every paper the file names against the record — by id, or by title with case, punctuation and spacing folded. **Only an exact match resolves.** A prefix or substring match is reported as a candidate and not certified: measured 2026-09-14, "Attention Is All You Need for Wildfire Damage Assessment" prefix-matched "Attention Is All You Need" and came back resolved, carrying the wrong paper's id.
- **unresolved**: A paper `verify` could not match. It stays in the file, marked, with the closest thing the search did return. Never deleted: where recall outran the record is what a reader wants to see.
- **framed** / **unframed**: Whether the run took its problem from `research/QUESTION.md`. Unframed runs are stamped as such, and are a normal way to use the skill.
- **bound**: Searches times `--limit`, where the searches are the field list the user approves before any of them run. There is no budget and no ledger: a citation walk compounds and needs a ceiling enforced per request, and search does not.

## Connection terms

Added with chunk 4 (2026-09-15), when the retrieval script grew from one index
to four resolvers and seven probes. `docs/APIS.md` is the reference.

- **source**: One external API the script can talk to. Seven: Semantic Scholar, OpenAlex, Crossref, arXiv, Unpaywall, Hugging Face papers, Zotero.
- **resolver**: The code in `snowball.py` that turns one source's answers into the unified record. Four exist: `s2`, `openalex`, `crossref`, `arxiv`. The other three sources are probed only.
- **index**: A source `search` queries for papers by keyword. Two: Semantic Scholar and OpenAlex, merged. arXiv is searched only when asked for by name.
- **connected** / **connected-no-key** / **not connected**: The three states `status` reports per source, defined in `docs/APIS.md`. Reachable is a state; throttled is not an outage; keyless is never an error.
- **degraded**: An index that failed inside one `search` call while the other answered. Named in the result, stamped in the file, never silently absorbed.
- **candidate**: What `verify` calls a prefix or substring title match. Reported with the id it nearly matched, and **never certified**: a candidate line stays unresolved until a human promotes it. Replaces the free-text "NOT the same paper" as the marker.
- **CONNECTIONS.md**: `research/CONNECTIONS.md`, written by `/setup` from `status --md`. One dated line per source. Every searching skill reads it first and adapts.
- **web rule**: `WebSearch` and `WebFetch` are allowed in exactly two places, the `searcher` agent's last resort and `/scout` reading a page an index pointed at, and the guard denies both to every other agent this plugin ships.

## Gathering terms

Added with chunk 5 (2026-09-15), the gathering cycle: `/surveys`, `/landscape`, and `/scout` rewired onto one agent.

- **neighborhood**: The script verb, and what it returns: the seeds for one query plus one hop backward and one forward from each, deduplicated and ranked inside itself. The depth tool, recovered from 249188a and rebuilt on two indexes.
- **seed**: One of the top 30 papers by relevance for a query, interleaved across Semantic Scholar and OpenAlex. Every seed is walked both ways before the next seed.
- **centrality**: How many neighborhood papers cite a paper, counted over the edges the walk actually saw. The primary rank; `influentialCitationCount`, citations per year and presence in both indexes break ties, in that order.
- **foundational** / **current** / **surveys**: The three groups every section carries. Older than five years; the last five years; title says survey, review or overview or the paper cites 100+ neighborhood papers.
- **section**: One searcher's file: `## Question`, the three groups, `## What was searched`, `## What returned nothing`. Under `research/landscape/sections/` or `research/analogs/sections/`. The only thing the merger reads.
- **searcher**: The one retrieval agent. One question, one field, one query, one section. Runs `neighborhood`; pastes lines; may WebSearch once, as a last resort, labelled. Replaces the deleted `paper-scout`.
- **merger**: The contract-bound agent that lays sections side by side into `matrix.md` and `timeslice.md`. Copies lines, names the query behind every empty cell, marks disagreements as contradictions, cannot add a claim.
- **cell probe**: One `search` per formulation × data regime pair, run by `/landscape` after the sections return and written as `sections/cells.md`, so the merger can name the query behind an empty cell without running one.
- **blocked**: The vocabulary a searcher's query may not use. In `/scout` it is the home vocabulary; the script refuses the query, so the home field cannot leak in by accident.
- **stop reason**: Why a walk ended: `complete`, `saturation` (a block of five seeds added under 5 percent), or `budget` (400 papers). Always recorded in `## What was searched`.

## Reading terms

Added with chunk 7 (2026-09-16), the reading milestone: `/read` and the seven
ledger and judgement skills built on the cards it writes.

- **card**: One paper, understood, at `research/papers/<slug>.md`. Sixteen fixed headings. Written by the `scorer` at the end of a `/read` run and edited afterwards only by the skill that owns a section. The unit every skill after this one reads.
- **pass**: Which of Keshav's three passes the read stopped at, recorded on every card. `full` is the three-agent protocol; `1` is a skim. A skim that does not say it is a skim is a full read to everything downstream, which is why `check_cards` requires the value.
- **intro text** / **full text**: The two files `fetch` writes per paper, in the cache. The intro text ends where the introduction ends. The predictor is handed the intro text and nothing else, so the rule that it must not see the method is a file boundary and not a sentence in a prompt.
- **split**: How `fetch` decided where the introduction ends: `heading` (the first section heading after it, named) or `page-cut` (the fallback, two pages). Recorded on the metadata record, because a page cut is the case where the predictor may have seen a little of the method.
- **unplaced**: A card written with no matrix to place it in, or whose paper appears in no cell. Marked, never guessed: a card that invents its own cell disagrees with the landscape later. `/read --place` fills it once a matrix exists.
- **tag**: What `/verify` appends to a reference line: `verified`, the candidate marker, or `not found` with the indexes checked. A reference with no tag is a `check_cards` failure. A not-found reference stays in the file, marked, exactly as an unresolved paper does in a section.
- **review notes**: The `## Reviews` section of a card, from OpenReview: ratings, the objections that recur, what the authors conceded, the decision. Reviewers say what authors will not.
- **leakage flag**: One line under `## Leakage`, one per Kapoor and Narayanan leakage type, each carrying a quoted passage or "could not determine, checked X and Y". Flags and evidence; no score and no verdict.
- **thesis group**: A set of cards that share a thesis, named by `/bits` on its first run and recorded in `BITS.md` with its slugs. Ré groups by thesis, not by topic, and the landscape has no such grouping to inherit: sections are per question and cells are formulation by data regime. Recorded rather than recomputed, so the file `/ideas` reads does not reshuffle between runs.
- **bit**: The assumption one thesis group shares, in one sentence, with the cards behind it and the cells they sit in. Method, evaluation or dataset. A group of one card is too thin to carry one, and is listed as such.
- **critique**: One fresh-context attack on one file, at `research/critiques/<file>-<date>.md`. Findings, then rebuttals scored one to five on the concession ladder. Never edits the file it judges.
