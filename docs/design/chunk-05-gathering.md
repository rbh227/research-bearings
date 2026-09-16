# Chunk 5: the gathering cycle

2026-09-15. The depth tool comes back, on two indexes, as one script verb and
one agent; `/surveys` and `/landscape` are built on it; `/scout` is rewired
onto the same agent. `docs/design/chunk-04-connections.md` is the layer under
this one.

## 1. Decision record

- **Why the snowball returns.** Chunk 3 deleted it because the plugin wanted
  breadth first and the walker was S2-only, budget-ledgered, and fed an agent
  that authored prose. Breadth exists now (`/scout`). The landscape chain
  needs depth, and chunk 4 made depth survive an unkeyed S2. So the seed-and-
  snowball logic from 249188a comes back as `neighborhood`, with the parts
  that earned their place (hops, edge sentences, the unresolvable split, the
  dedupe) and without the ones that did not (the ledger, `--run`, the merge-
  on-write records).
- **One verb, one agent, three skills.** `neighborhood` does the whole walk
  in one process: seeds, hops, dedupe, rank, group, log. The `searcher` runs
  it and pastes. `/landscape` dispatches seven, `/surveys` one in survey mode,
  `/scout` one per analog field with the home vocabulary blocked. The
  alternative, a walker the agent drives call by call, is what chunk 2 built,
  and it put the budget arithmetic in the model's hands, where it was
  decorative by the end.
- **Rank inside the neighborhood, not by global citations.** Field centrality
  first: how many neighborhood papers cite it, over the edges the walk saw.
  Then `influentialCitationCount`, citations per year, presence in both
  indexes. Global citation count is what makes "Optimization by Simulated
  Annealing" the top reference of a damage-assessment walk; centrality is what
  puts the 2010 VHR-and-SAR paper above it.
- **Each seed both ways before the next seed.** The first cut walked every
  seed backward and then forward; at a budget of 80 that was 74 references
  and no citing paper, and the "current" group was empty. Now a seed's
  references and citations are fetched together, 25 rows per direction,
  and the budget stops the walk at a seed boundary. Saturation is judged per
  block of five seeds, since one seed's hop is noise.
- **Groups by age and title, not by judgement.** Foundational is older than
  five years; current is the last five; a survey is a title that says survey,
  review or overview, or a paper whose reference list overlaps the
  neighborhood by 100 or more. All three are decidable by looking, which is
  the standard every check here holds.
- **Every line verified by construction.** A neighborhood paper carries the
  id the index returned for it, so the line ends in `· verified` and the
  block says why. The searcher may add up to three remembered papers, each
  through `verify`, exact only. There is no separate verify pass over 400
  titles because there is nothing to verify: the index is the record.
- **The merger cannot run a query, so the skill runs the cell probes.** The
  contract says an empty cell is "query `<q>` returned zero rows". A merger
  with `Read` and `Write` cannot produce that line honestly, and seven
  question-shaped sections do not carry a query per axis pair. So
  `/landscape` derives the axes after the sections return, runs one `search`
  per formulation × regime pair, and writes `sections/cells.md` — an eighth
  section, script output, in the same line format. The merger reads it like
  any other. This is the one step the user's outline did not name, and it is
  here so the absence rule stays literal.
- **`/scout` keeps its fingerprint and gate.** The shape and the query plan
  are still shown before anything runs. What changed is under the gate: one
  searcher per field, in parallel, the home vocabulary passed as `--block` so
  the script, not the prompt, keeps the home field out; and the nearest
  existing attempt found by a small `neighborhood` walk in the home
  vocabulary, top paper and count, rather than one `search`.
- **The Bash fence returns to the guard.** The searcher is the first agent
  with Bash since `paper-scout`. The fence from 249188a is back with its
  cases: `python3 <plugin>/scripts/retrieval/<x>.py …`, no shell operators
  outside quotes, no command substitution anywhere.

## 2. What ships

| Piece | Change |
|---|---|
| `scripts/retrieval/snowball.py` | `s2_hop` with edge sentences; `oa_by_dois`; `neighborhood` (seeds, both-way hops per seed, dedupe, centrality rank, three groups, saturation and budget stops, `what_was_searched`, `returned_nothing`, `--block`, `--surveys-only`, `--write`); 44 offline cases |
| `agents/searcher.md` | 73 lines. One question, one field, one section. Bash for the script only; WebSearch once, last resort, labelled |
| `agents/merger.md` | Read and Write. Copies lines, names the query behind empty cells, marks contradictions, cannot add a claim |
| `agents/survey-differ.md` | Read, Write, Edit. Taxonomy and open challenges from abstracts in the records, marked as such; appends vocabulary to `QUESTION.md` |
| `skills/landscape/SKILL.md` | seven questions, one gate, seven searchers, axes, cell probes, merger, `check_landscape.py` |
| `skills/surveys/SKILL.md` | one searcher in survey mode, then the differ |
| `skills/scout/SKILL.md` | dispatches searchers with the home vocabulary blocked; nearest existing via a small walk |
| `templates/research/section.md`, `matrix.md`, `timeslice.md`, `surveys.md` | new, registered with `check_headings.py` |
| `scripts/check_landscape.py` | new: a cell with neither a paper nor a query-and-count line, a paper line neither verified nor candidate, a banned word, a matrix title in no section; 7 cases |
| `hooks/guard.py` | Bash fence restored; 35 cases |
| `evals/landscape/` | two run fixtures, `recall.py`, the runs and their report |

## 3. Done-check

Static: heading parity over nine templates; `check_landscape.py`,
`check_analogs.py`, guard and script selftests green; three manifests validate.

Live: §4.

## 4. Eval, 2026-09-15 to 16

`evals/landscape/README.md` has the queries, the numbers by gold heading, the
misses, and what the run says about the design. In one line each:

- wildfire, six headings: 56 of 98 gold papers; damage, two headings: 11 of
  27, with 10 of 14 on damage assessment itself. Structure loss scored 1–2 of
  13 in both because no query asked for it.
- Both matrices pass `check_landscape.py`. Most listed contradictions were the
  same paper under two indexes' ids; the merger's rule now says same-index
  ids only. The matrices were not regenerated.
- Two bugs found and fixed during the run: the OpenAlex reference hop had no
  row cap (fixed before the survey reruns and every landscape walk), and one
  failed S2 hop marked S2 degraded for the rest of a walk (fixed after the
  four agent-run wildfire sections, two of which show `Degraded: s2`, and
  before the other ten walks, none of which do). A third change came from cost: fourteen
  concurrent agents exhausted the account, so `neighborhood --write` now
  renders the section and the searcher pastes nothing.
- Read 2026-09-16; no rerun, no tuning. The user keeps the high-citation
  papers in the ranking on purpose.
- Findings left for the reader: centrality rewards ubiquitous methods papers;
  seed centrality is capped by the hop sample; surveys-only mode surfaces the
  references of reviews rather than the reviews; long queries get nothing
  from S2; the budget binds around seed ten.

Emulation note: agents were general-purpose subagents handed the contract
files, and after the limit hit, the main thread. The script calls, files and
checks are real; the `research-bearings:searcher` registration was not
exercised, and neither was the guard on these writes.
