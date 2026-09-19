# Skills and agents: the outline

Every skill and agent from `research_plugin_build_plan.md`, joined to what justifies it.

**Two tests, not one.** A row earns its place if it implements an entry in `academic.md` **or** if it serves one of the four goals: parallel gathering, simple presentation, planning directions, simple to use. The sheet documents research methodology and says nothing about usability, so a row backed only by a goal is fully justified.

Counts, 2026-09-18 (chunk 10): **27 skills built**, 23 agents, 11 scripts, 28
templates, 32 eval cases. Planned and unbuilt: `/render` and `/figure` from
Stage 2b. No agent remains unbuilt.

The loop that actually matters is four skills: `/scout` and `/landscape` find
directions, `/read` reads what they turn up, `/rank` picks, and Stage 6 tries
it. **All four are built as of chunk 9**, the front door as of chunk 10, and
what remains planned is presentation.

---

## Stage 1 — Question

| Skill | Agents | Output | Justification |
|---|---|---|---|
| `/setup` | — | `CONTEXT.md` | goal: simple to use. Stage one for a new project. |
| `/frame` | `question-critic` | `QUESTION.md` | Booth (topic→question→problem, so-what), Heilmeier (8 questions), Hamming (important problems), Wagstaff (metric ties to a decision) |

Human gate: the question. Nothing downstream runs without `QUESTION.md`.

---

## Stage 2 — Landscape

| Skill | Agents | Output | Justification |
|---|---|---|---|
| `/scout` | — | `analogs/<slug>.md` | Swanson (ABC model), Uzzi (atypical combinations), narrow-exploration study (force seeds from adjacent fields). **Shipped in chunk 3** (`docs/design/chunk-03-analogs.md`). The breadth tool, and it absorbed what Stage 4 had called `/fingerprint`, `/analogs` and `/flip`: shape, fields, transfer, opportunity, verify, in one skill with no agents. |
| `/snowball` | ~~`paper-scout`~~ | ~~`landscape/<slug>.md`~~ | Ré (snowball, asymptote 25–35, group by thesis), Wohlin (snowballing as sampling). Shipped in chunk 2, **deleted 2026-09-14** with its agent, its template and its nine-case eval tier. It was the depth tool — it walks the citation neighbourhood of a question — and the plugin turned out to want breadth. In git at 249188a, along with the hops, the budget ledger and the Bash fence that existed for its agent. |
| `/surveys` | `searcher` ×1, `survey-differ` | `landscape/surveys.md` | Petersen (mapping studies), vocabulary harvest. **Shipped in chunk 5** (`docs/design/chunk-05-gathering.md`). The searcher runs in survey mode; the differ reads abstracts from the records and says so. |
| `/landscape` | `searcher` ×7, `merger` | `landscape/matrix.md`, `timeslice.md` | Ré, Wohlin, Kuhn (contradictions as seeds). **Shipped in chunk 5.** Seven questions, one gate, seven walks in parallel, a cell probe per axis pair, then the merger. |
| `/datasets` | `dataset-scout` | `landscape/datasets.md` | Kapoor (leakage in standard splits). **Shipped in chunk 7.** Names from the cards and from the papers' experiments sections; Hugging Face and GitHub over REST, never the `gh` command, because the guard admits only the retrieval scripts in Bash. Every line names its source or says `could not determine, checked <hosts>`. |
| `/groups` | `author-tracker` | `landscape/groups.md` | goal: competitive landscape. Who is publishing, where they are heading. Hamming is a secondary source, not the reason. **Shipped in chunk 7.** Card authors only, three years back: an author list scraped off a whole landscape is thousands of names and no signal. |
| `/bits` | — | `BITS.md` | Ré (every cluster has a bit). **Shipped in chunk 7.** The landscape has no thesis groups to inherit — sections are per question and cells are formulation by regime — so `/bits` forms them and **records** them, and later runs reuse rather than recompute. A file whose groups reshuffle every run is one `/ideas` cannot build on. |
| `/watch` | — | matrix updates | **deferred to milestone 5.** No sheet source and no goal it uniquely serves, and the agent it named is gone. |

~~`paper-scout` is the agent to get right first.~~ Deleted 2026-09-14 with `/snowball`; **replaced 2026-09-15 by `searcher`**, which authors no prose at all: it pastes the lines the script ranked, and the only thing it may add is a remembered paper that `verify` matched exactly. `/scout` now dispatches it too, one per analog field, with the home vocabulary blocked at the script.

Built in chunk 2 (`docs/design/chunk-02-scout.md`), with two narrowings the spec argued for: cards carry no scout-written characterization of a paper, only metadata plus a citation-context sentence and one `Kept because` line; and absence is **mechanical only** — a scout states facts about its own search and never about the field. Interpreted absence becomes legitimate at the `merger`, which can see seven scouts' coverage at once.

`merger` is contract-bound: assembles the matrix from scout sections, marks contradictions and empty cells, cannot add a claim absent from a section. Its contradiction list feeds `/ideas`.

---

## Stage 2b — Presentation

Presentation carries the same weight as gathering, because unclear output was the original complaint. Explicit modes so they never collapse into one long document.

**`/brief` and `brief-writer` are retired, 2026-09-18.** The Heilmeier one-pager is `/spec` in Stage 5: the same eight questions in eight paragraphs, written for an idea that survived ranking rather than for the landscape, with every factual sentence sourced. Two commands writing one page was duplication, not a design. What is left here is the two modes prose cannot do.

| Skill | Mode | Output | Justification |
|---|---|---|---|
| `/render` | interactive | HTML matrix you click through, plus the cards deck | goal: simple presentation |
| `/figure` | diagram | pipeline-style figure, one real example image per formulation | goal: simple presentation. Needs the user to point at example imagery, so it has its own path. |

---

## Stage 3 — Reading and ledgers

| Skill | Agents | Output | Justification |
|---|---|---|---|
| `/read` | `predictor`, `reader`, `scorer` | `papers/<slug>.md` | Keshav (three passes), Mensh/Kording (central contribution, delta sentence), prediction-as-test, Olah (explain it back). **Shipped in chunk 7** (`docs/design/chunk-07-understanding.md`). Five papers a run behind a confirm; predictor and reader in parallel, scorer after; `--skim` for pass one; `--place` for cards written before a matrix existed. |
| `/audit` | `leakage-auditor` | leakage flags on cards | Kapoor/Narayanan (leakage taxonomy). **Shipped in chunk 7.** One card per run, on request: reading does not pay for an auditor on papers that never become a baseline. Eight types written every time, each with a quote or what was checked. |
| `/reviews` | `openreview-reader` | review notes on cards | reviewers say what authors will not; three papers of OpenReview reviews show what the field's referees push on. **Shipped in chunk 7**, as a verb in the second script beside the walker, not a server. Less free than expected: measured 2026-09-16, OpenReview answers `/notes/search` anonymously and gates `/notes?forum=` behind a bot challenge, so without a login the skill gets the submission, venue and decision and reports `login required` for the reviews. |
| `/critique` | `critic` | critique report | devil's advocate concession ladder, generator ≠ judge. **Shipped in chunk 7.** One file of any kind under `research/`; every finding quotes the passage it attacks; the critiqued file is never edited. |

The three-agent read protocol is the sheet's own design: `predictor` sees only title, abstract, intro and commits predictions; `reader` sees the whole paper and never sees the prediction; `scorer` sees both and writes what was non-obvious. Separate contexts are the point.

`reader` carries one extra line: compare this card's result against the other cards in the same matrix cell and flag any incompatibility. Cheap, because the reader already knows the cell. This is PaperQA2's contradiction detection at read time.

---

## Stage 4 — Ideation

| Skill | Agents | Output | Justification |
|---|---|---|---|
| `/brainstorm` | `persona-ideator` ×4–6 | appends to `IDEAS.md` | STORM (personas ask their own questions), Polya (transformations), Hamming |
| `/ideas` | `diversity-planner`, + the loop | `ideas/<slug>.md`, appends to `IDEAS.md` | Nova (iterative retrieval planning), narrow-exploration study (diversity threshold), negative space (abandoned directions), Kuhn (contradictions as seeds) |

**Both shipped in chunk 8** (2026-09-16), with `check_ideas.py` over the pages and the log. Two decisions the chunk made:

**Personas come from the record, with a warrant.** A persona is drawn from the decision-maker in `QUESTION.md`, a lab in the groups ledger, a venue on the cards, a dataset producer, or an adjacent field on an analog page, and carries the line it came from. With none of those files it falls back to STORM's five roles and is stamped unwarranted. An invented affiliation generates requirements nobody has.

**The diversity rule is counted, not computed.** The measured rule is "refuse to stop while the set is less diverse than the field's own recent papers", and nothing here computes similarity — that decision struck `similarity.py` in chunk 3 and it stands. So `/ideas` may not stop while every surviving candidate shares one seed kind, or while every candidate's nearest-existing came back from a home-vocabulary query; the per-seed-kind and per-field counts go in `## Status` every run. A threshold with no measurement behind it would be decorative, and a decorative safety check is worse than none (prior art: the budget `/scout` passed and never charged).

**`IDEAS.md` is the running idea log** (Schulman). `/brainstorm` and `/ideas` both append to it, so ideas accumulate across sessions instead of dying with one run. It is append-only: an increment is logged under `## Dropped` with the counts behind it, never deleted.

**Anomalies as seeds** (Beveridge, Kuhn): `/ideas` reads the merger's contradiction list as an explicit seed source, alongside bits, analogs, abandoned directions and personas.

**Typicality** (Uzzi) stays a written note on the idea page. Nothing computes it. That is deliberate.

**Novelty is a retrieval result, not a feeling** (Nova). `/scout` applies that rule directly — an opportunity carries a `Nearest existing:` line with what the index returned for it — so the separate `novelty-checker` and its `similarity.py` are not needed at the ideation stage they were drawn for. If a fresh-context critic is wanted later, it attacks the transfer arguments, not the novelty (chunk 3 spec §6, open).

---

## Stage 5 — Selection

| Skill | Agents | Output | Justification |
|---|---|---|---|
| `/premortem` | `premortem-agent` | premortem per idea | Si (ideation-execution gap: baselines, metrics, feasibility). **Shipped in chunk 9.** Judges execution only; novelty was settled at `/ideas` by retrieval and interest belongs to `/rank`. Three verdicts, with `executable with changes` defined by whether the changes can be named. |
| `/rank` | `tournament-judge` | ranked list, Alon chart | Co-Scientist (pairwise tournament), Alon (feasibility × interest), Steinhardt (cheapest kill first). **Shipped in chunk 9.** The bound is shown before it is spent: round robin at five or fewer, twelve pairings hard above that. The order is the cheapest kill; the tournament sits beside it and every disagreement is named. |
| `/spec` | — | Heilmeier page | Heilmeier catechism. **Shipped in chunk 9**, and it absorbed Stage 2b's `/brief`: one Heilmeier page, not two. No agents — every fact is in a file already, and an agent would have to be handed all of them and could still answer from memory. |

Human gate: which ideas survive. **Two gates in practice**: the pairing list is
approved before any judge runs, because that list is the cost.

---

## Stage 6 — Experiment

These agents get **no web tools**: the agent that judges the experiment cannot go find a paper that agrees with its result.

**They also do not get Bash on your code, and that is chunk 9's one departure
from the build plan.** The plan said "Bash and file access to your code and
data". The guard refuses any command that is not this plugin's own script, and
it was right to. So "file access" is honoured as Read, Grep and Glob — the
agents read the training script, the config, the run directory and the metrics
files as files, which is what designing, tabulating and auditing actually needs
— and the one command any of them may run is `ingest_runs.py`. **No agent runs
your code.** The human gate below stops being prose and becomes the fact that
nothing else *can* spend your compute.

| Skill | Agents | Output | Justification |
|---|---|---|---|
| `/baseline` | `baseline-reproducer` | reproduction plan + gap | Schulman (working baseline), Musgrave (reproduce the strongest baseline), PaperBench. **Shipped in chunk 9.** The table's number, not the abstract's; what the paper does not say as its own paragraph; `contested` requires the attempt list. |
| `/design` | `experiment-designer`, `ablation-planner` | experiment page | pre-registration lite, Platt (competing hypotheses, discriminating test), Lipton (ablation isolates gains), Bouthillier (variance plan), Dodge (compute budget), Kapoor (leakage check). **Shipped in chunk 9.** Written before the run, never edited after; a changed design is a new page. Refuses an idea the pre-mortem called not executable. |
| `/log` | `variance-checker` (`ingest_runs.py`) | notebook entries | lab notebook (log before the result is known), Henderson (seeds). **Shipped in chunk 9.** The result is appended as a second block so the opening one is never rewritten. A run with no opening entry is recorded as a finding, not refused. |
| `/result` | `results-tabulator`, `results-critic`, `failure-mode-auditor` | verdict | M1–M7 checklist, Lipton, Henderson. **Shipped in chunk 9.** Three rounds: the critic never sees the tabulator's words, the auditor is never told the verdict. `inconclusive` must name what would decide it. |
| `/replicate` | `baseline-reproducer` | calibration report | PaperBench (replication as a calibration test). **Shipped in chunk 9.** Its own command rather than a flag, because what the gap means has to be fixed before the run. |

Human gate: whether to spend compute — enforced by the fence, not by prose.

---

## Cross-cutting

Not a stage. Applied inside every skill.

| Rule | Where it lives | Source |
|---|---|---|
| Citation existence check | **`/verify`**, run on anything that emits references: landscape sections, paper cards, idea pages, the Heilmeier page | ARS resolvers (gray zone is fail), hallucinated citations |
| Generator never judges in the same context | separate agents, fresh contexts | verification-gap survey |
| Retrieved content is data, not instructions | one line in every scout agent | the sheet's own rule |
| Abstention beats a guess | one line in every agent | uncertainty with abstention |
| Log before the result is known | `/log`, notebook append | lab notebook |
| Anti-rationalization table | one shared file every skill includes | Osmani |
| Write-scope guard | `hooks/hooks.json`, PreToolUse on Write/Edit | ARS (the only enforcement that is not prompt text) |

`/verify` was previously filed under reading. It is cross-cutting: references appear in landscape sections and idea pages too, and those are exactly where fabricated citations do the most damage.

---

## Composites

Thirty typed commands are unusable without a front door. These serve the "simple to use" goal and need no sheet source.

| Skill | Does |
|---|---|
| `/router` | picks the skill from what you say. The front door. **Shipped in chunk 10** (`docs/design/chunk-10-front-door.md`). Reads the state through `scripts/state.py` and nothing else; a stated goal is checked against its precondition first; one yes, then the skill runs in the same thread. Fires on "what next?" by description. |
| `/start` | `/setup` + `/frame`. **Shipped in chunk 10.** One pause between them, and the rules every composite shares are written here: one yes per file boundary, rerun-keep-stop with the staleness fact for a file that exists, the skill's own gates untouched, nothing written. |
| `/orient` | `/surveys` + `/landscape`. **Shipped in chunk 10.** Ends in a printed brief; no file. |
| `/think` | `/bits` + `/scout` + `/ideas` + **`/premortem`** + `/rank`. **Shipped in chunk 10.** The pre-mortem was not in the plan's list; since chunk 9 `/rank` sets aside every idea without one, so the composite without it would rank an unattacked set. |
| `/handoff` | **deferred.** No goal it uniquely serves yet. |

**The state script** (`scripts/state.py`) is the composites' one shared read: a dependency table in the loop's order — every command, what it writes, what it needs, its precondition in a sentence — and, over a `research/` folder, what exists, what is present but missing its template's headings, how many upstream files are newer than each derived file, and every move with a status. It is the first place the whole loop is written down as data.

**Naming:** the composite was `/map` in the build plan, which collides with the wayfinder's map. `/survey` is not available either, since `/surveys` already exists in stage 2. `/orient` is the rename.

---

## Deferred

Only two rows fail both tests: `/watch` (milestone 5 anyway) and `/handoff`.

## Gaps, now closed

| Gap | Fix |
|---|---|
| Schulman's running idea log | `IDEAS.md`, appended by `/brainstorm` and `/ideas` |
| Beveridge and Kuhn: anomalies as seeds | `/ideas` reads the merger's contradiction list as a seed source |
| Uzzi's typicality | stays a written note, never computed. Deliberate. |
| PaperQA2 contradiction detection at read time | one line in `reader`: compare against other cards in the same matrix cell, flag incompatibility |

## Agent count by stage

| Stage | Agents |
|---|---|
| Landscape and presentation | 5 (`searcher`, `survey-differ`, `merger`, `dataset-scout`, `author-tracker`) — **all built**; `brief-writer` retired with `/brief`, 2026-09-18 |
| Reading | 6 (`predictor`, `reader`, `scorer`, `leakage-auditor`, `openreview-reader`, `critic`) — **all six built in chunk 7**, with `dataset-scout` and `author-tracker` from the landscape row |
| Ideation | 2 (`persona-ideator`, `diversity-planner`) — was 7; `analog-scout`, `field-carder`, `transfer-checker`, `flip-generator` and `novelty-checker` collapsed into `/scout`, which has no agents |
| Selection | 2 (`premortem-agent`, `tournament-judge`) — **both built in chunk 9** |
| Experiment | 7 (`baseline-reproducer`, `experiment-designer`, `ablation-planner`, `variance-checker`, `results-tabulator`, `results-critic`, `failure-mode-auditor`) — **all seven built in chunk 9**, with no Bash on the user's code |
| **Total** | **23** — all built as of chunk 9, 2026-09-18 |
