# Chunk 8: ideation

2026-09-16. The plugin learns to propose. Two skills and two agents turn the
bits, the analog opportunities, the merger's contradictions, the directions the
record shows were dropped, and the personas' questions into candidate ideas,
each carrying the nearest existing paper and the counts the walk came back with.
`docs/design/chunk-07-understanding.md` produced four of those five inputs; the
fifth has been waiting since chunk 5.

The spec is `.scratch/chunk-08-ideation/spec.md`, with nine tickets in
`issues/`. Not grilled: the milestone was planned in the build plan and in
`skills-and-agents.md` § Stage 4, and the spec follows that plan rather than
reopening it. Build only: no `evals/` cases and no live wildfire test. The
milestone's own test — run it on the wildfire map and check whether the top
ideas' nearest-paper rows are actually thin — is the acceptance run, and it
belongs to the user.

## 1. Decision record

- **The diversity rule is counted, not computed.** The measured rule is "refuse
  to stop while the set is less diverse than the field's own recent papers", and
  nothing in this plugin computes similarity — that decision struck
  `similarity.py` in chunk 3 and it stands. So `/ideas` may not stop while every
  surviving candidate shares one seed kind, or while every candidate's
  nearest-existing came back from a home-vocabulary query **with no field search
  behind any of them**. That last clause is load-bearing and was added during the
  review: the spec's unqualified form ("every candidate's nearest existing paper
  came from the home field's own vocabulary") is vacuously true, because step 3
  puts every candidate to the index in the home vocabulary by design — so
  without the clause the condition could never be false and the run could never
  stop. Either state sends the run back for one more planning round; a
  second occurrence is reported to the user rather than looped on. The
  per-seed-kind and per-field counts go in `## Status` every run, triggered or
  not, because the count is the only thing that makes the rule checkable from
  outside. A threshold with no measurement behind it would be decorative, and a
  decorative safety check is worse than none — prior art, chunk 3: the budget
  `/scout` passed and never charged.

- **Personas come from the record, with a warrant.** A persona is drawn from the
  decision-maker in `QUESTION.md`, a lab in the groups ledger, a venue on the
  cards, a dataset producer in the datasets ledger, or an adjacent field on an
  analog page, and it carries the line it came from. With none of those files it
  falls back to the five roles STORM's rule names and is stamped **unwarranted**
  in `## Status`. `persona-ideator`'s refusals table exists mostly to stop the
  one failure that matters here: an invented affiliation generates requirements
  nobody has, and every question that follows from it is fiction dressed as a
  constraint.

- **The planner names fields; it does not generate ideas.** A planner that also
  proposed the ideas would be planning retrieval toward its own answer, and the
  three searchers that follow would be confirmation. So `diversity-planner` gets
  Read and Write, writes the commonality *before* it proposes anything, and is
  told in its own contract that nowhere in its file does it say what could be
  tried.

- **Importance before feasibility, as an order in the file.** `/brainstorm`
  asks Hamming's questions first, Polya's seven transformations second, the
  stakeholders third, and asks nothing about feasibility at all — not "could
  you do it", not "do you have the data". `/premortem` owns that, after there
  are ideas to premortem. A session that asks what is achievable first
  converges on what is easy, and the important problem never gets said out
  loud.

- **The log is append-only, and an increment is kept.** A candidate whose
  nearest existing paper is the same idea is marked, logged under `## Dropped`
  with the title, the id and the counts, and never deleted. What was considered
  and set aside is what stops it being reconsidered from scratch next month.
  `check_ideas.py` enforces the other half: a slug under `## Promoted` with no
  page is a failure, because the log and the pages may not disagree.

- **No new verb and no new script.** `/ideas` needs one retrieval behaviour —
  put a candidate to the index and get the nearest existing paper back — and
  `snowball.py neighborhood` already has it. The same call `/scout` makes, so an
  idea page's `Nearest existing` and an analog page's mean the same thing.
  Retrieval for the diversity round is the existing `searcher`, in analog mode,
  writing under `research/ideas/sections/`.

- **The bound is the inventory and the field list.** One candidate per seed, two
  rounds, three fields per round, and the user approves the seed inventory
  before generation and the field list before any searcher runs. That is the
  same gate `/scout` puts at its step 3, and for the same reason: a person
  looking at the actual number before it is spent.

## 2. What ships

| Thing | Where |
|---|---|
| `/brainstorm` | `skills/brainstorm/SKILL.md` — the dump; three banks in a fixed order; four to six personas; decides nothing |
| `/ideas` | `skills/ideas/SKILL.md` — nine steps; five seed kinds; two rounds; the counted stop rule |
| `persona-ideator` | `agents/persona-ideator.md` — Read, Write; one stakeholder's questions with a warrant |
| `diversity-planner` | `agents/diversity-planner.md` — Read, Write; commonality first, then three to six fields |
| The running log | `templates/research/ideas-log.md` → `research/IDEAS.md`; four headings, append-only |
| The idea page | `templates/research/idea.md` → `research/ideas/<slug>.md`; nine headings |
| The persona file | `templates/research/persona.md` → `research/ideas/personas/<date>-<slug>.md`; five headings |
| The diversity plan | `templates/research/diversity.md` → `research/ideas/plans/diversity-<date>.md`; four headings |
| The checker | `scripts/check_ideas.py`, 19 selftest cases, over pages and over the log |
| Guard cases | `hooks/guard.py` selftest, 10 new cases; 73 in total, no behaviour change |
| Glossary | `CONTEXT.md` § Ideation terms, twelve entries |
| Docs | `README.md`, `docs/design/skills-and-agents.md` § Stage 4, the build plan's Milestone 4 status, manifest `0.8.0` |

Two kinds of existing file were touched. `agents/searcher.md`, whose contract
named two section directories and now names three, so an ideation round's
sections have somewhere to live that is not `/scout`'s directory. And the three
older checkers, which now import `scripts/checklib.py` — see § 4.

## 3. Done-check

```
python3 scripts/check_ideas.py --selftest      # 19 cases
python3 scripts/check_headings.py             # 21 templates, 2 agent contracts
python3 scripts/check_cards.py --selftest
python3 scripts/check_analogs.py --selftest
python3 scripts/check_landscape.py --selftest
python3 hooks/guard.py --selftest             # 73 cases
claude plugin validate .
```

All green 2026-09-16.

## 4. What the dry runs found, 2026-09-16

- **The row count saturates, and the page was about to report it as a
  measurement.** The call both `/scout` and `/ideas` make —
  `neighborhood "<candidate>" --seeds 5 --budget 30 --top 1` — was run live
  against "single image post-disaster building damage classification without
  pre-event imagery". It returned `counts.neighborhood: 30` against a 30-paper
  budget, which is what it will return for almost any query the search finds
  papers for. A bare "30 rows" on an idea page reads as a census and is not
  one. So the page carries two numbers: `Papers the query found: <n> of 5
  requested` (`counts.seeds`, the number that can actually be thin) and
  `Rows: <n> of a 30-paper budget`. `check_ideas.py` requires both, and the
  template says why. The analog pages still carry the row count alone; that is
  chunk 3's file and this chunk did not touch it, which means an idea page
  carries one number more than an analog page and says so.
- **The walk hands back a formatted, verified line.** `groups.current[0].line`
  comes out already in the shared paper-line shape, already carrying its id and
  `· verified`. The skill says to paste it rather than retype it — retyping is
  how a title drifts from the record it claims.
- **`seed` already meant something else.** The Gathering glossary defines a seed
  as one of the top thirty papers a walk starts from. The first draft of this
  chunk used the same word for where an idea came from, and put both senses on
  one page — `## Seed` above a `Seeds:` count that meant papers. The glossary's
  rule is one meaning per word, so the retrieval count on an idea page is
  written `Papers the query found`, and the glossary entry for the ideation
  sense names the collision instead of hiding it.
- **The checker's cross-check works on real files.** A scratch `research/` tree
  with one page and one log passed both modes; adding a `## Promoted` slug with
  no page failed with the slug named. That cross-check is the one rule here that
  no single file can satisfy on its own.
- **Four checkers held four copies of the same code.** The review found
  `sections()` byte-identical in `check_cards.py`, `check_analogs.py`,
  `check_landscape.py` and the new `check_ideas.py`, with the paper-line regex,
  the three verify tags and the four banned words copied across two to four of
  them — and the duplicated absence message in two of them already drifted
  apart, which is the cost arriving on schedule. They now import
  `scripts/checklib.py`: the file shape every checker shares, and nothing a
  single checker alone asks. The three older checkers lost 44 lines between
  them and every selftest stayed green, which is what made the change safe to
  make from inside this chunk. Precedent: chunk 7's `papers.py` imports the
  walker's helpers rather than copying them.
- **Every real run would have failed its own done-check.** `/ideas` wrote the
  diversity plan to `research/ideas/diversity-<date>.md` and then ran
  `check_ideas.py research/ideas/`, which reads every file in that directory as
  an idea page. Reproduced: the plan fails eight missing-heading rules while the
  page beside it passes. The pages directory now holds pages only; the plan
  moved to `research/ideas/plans/`, beside `personas/` and `sections/`, which
  the checker does not descend into. A selftest case now builds the whole
  generated tree on disk and checks it. Found by adversarial review 2026-09-17.
- **A re-run would have rewritten the evidence under an existing idea.**
  Sections and persona files used a fixed filename per field and per persona,
  and `snowball.py`'s `write_section` opens its path with `"w"`. A second run on
  the same field replaces the paper lines and the search log that a promoted
  idea cites *by path* — an append-only log pointing at mutable evidence. Both
  are dated now, and deduplicated by numeric suffix the way a duplicate slug is,
  with the rule written in both skills and in the glossary as **cited by path**.
  Same review.
- **The template's own guidance does not pass as content.** Both new templates
  are headings plus comments, and `check_ideas.py` strips comments before it
  looks for content, so a freshly copied template fails every content rule
  rather than passing as a filled page.

## 5. What is not done

- **No live run.** Neither skill has been run end to end. `/brainstorm` has
  never dispatched a persona, `/ideas` has never generated a candidate, and no
  `IDEAS.md` exists outside the scratch dry run. The milestone's test is the
  acceptance run and it belongs to the user, as it did for chunk 7.
- **The stop rule is unexercised.** Its two conditions are written and testable
  by reading, and nothing has yet triggered them on a real candidate set. The
  case that matters — a set that is all one seed kind, because the repo has
  bits and nothing else — is exactly what a first live run on a thin repo will
  produce, so it should trigger on the first real use and that is worth
  watching.
- **No evals.** `evals/` gains nothing for either skill, matching chunk 7.
- **Round two has never read a section.** The path from a `diversity-planner`
  field to a `searcher` section under `research/ideas/sections/` to a
  round-two candidate is written and unwalked. The two review findings above
  both live on that path, which is the part of the chunk a live run would test
  hardest.
- **`/premortem`, `/rank`, `/spec`.** Milestone 5. The page shape this chunk
  fixed is what they will read, and nothing has read it yet.
