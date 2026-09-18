# Chunk 9: selection and experiments

**Status:** ready-for-agent
**Milestone:** 5 of the build plan (`research_plugin_build_plan.md` § Milestone 5)
**Date:** 2026-09-18
**Layer under this one:** `docs/design/chunk-08-ideation.md` (the idea pages this
reads), `chunk-07-understanding.md` (the cards `/baseline` reproduces from), and
`chunk-04-connections.md` (the guard, whose Bash fence decides this chunk's shape).

Grilled at the shape level on 2026-09-18, one round, and approved as one chunk.
The milestone was planned in the build plan and in
`docs/design/skills-and-agents.md` §§ Stage 5–6; this spec follows that plan
except where the guard forbids it (see "The guard decides this chunk's shape").
Build only: no `evals/` cases and no live run. The chunk note
`docs/design/chunk-09-selection.md` is written by the last ticket.

## Decisions settled at planning

The user approved the design as one chunk. The open items were settled as
follows; each can be reopened by editing this section before `/to-tickets`.

1. **One chunk, both halves.** Selection and experiments ship together. The
   experiments half cannot be exercised on a live run until the user has one,
   so its acceptance is the static layer named under Testing Decisions.
2. **No agent ever runs the user's code.** The build plan's "Bash and file
   access to your code" is honoured as Read, Grep and Glob. The plugin designs
   before and audits after; the user presses run.
3. **Selection ends in a Heilmeier page.** The ranking exists to choose which
   idea earns one. `/spec` is that page, and it absorbs the Heilmeier one-pager
   Milestone 2 deferred as `/brief`. `/brief` and `brief-writer` leave the
   planned list; `/render` and `/figure` stay planned.
4. **The pre-mortem judges execution only.** Novelty was settled by retrieval
   at `/ideas`; interest is the tournament's job.
5. **Pairwise judging, bounded, with the pairing list approved first.** No
   absolute scores and no single judge over the whole set.
6. **The order is cheapest kill first.** Tournament wins and the Alon plot are
   written beside it so the user can overrule.
7. **Two human gates in selection**: approve the pairing list, then choose
   survivors. Every idea without a pre-mortem gets one, capped at five per run,
   with no stop to choose which.
8. **`/replicate` stays its own skill** and is `/baseline` with the
   calibration flag; the design doc lists it separately and the file it writes
   says what it is for.
9. **Run directories are read on this machine only.** The user's experiments
   run on a remote GPU box; the user syncs run directories down, and the plugin
   never touches the remote. `ingest_runs.py` walks local paths.

## Problem Statement

The plugin can now produce ideas and cannot choose between them, and it has no
idea what happens after one is chosen. `/ideas` writes pages with a cheapest
kill on each and nothing runs it, nothing attacks the idea before it is
believed, nothing orders the set, and nothing turns a survivor into a page a
professor could read. Past that: no experiment is designed before it is run, no
attempt is logged before its result is known, no result is read against what was
pre-registered, and no number is checked for the seven ways a language model
fakes one.

Measured, and the reason this milestone is not optional: when 43 researchers
executed randomly assigned ideas over three months, LLM-generated ideas dropped
1.88 of 10 on effectiveness while human ideas barely moved, and the causes were
missing baselines, inappropriate metrics, and evaluation plans nobody could
run. Those are exactly the things a pre-mortem catches and a pre-registration
prevents.

## Solution

Eight skills and nine agents in two halves, plus one script.

**Selection** turns idea pages into a ranked, attacked, specified shortlist:
`/premortem` sends a fresh-context agent at each idea to find how it fails in
execution; `/rank` runs a bounded pairwise tournament, plots Alon's feasibility
against interest and orders by cheapest kill; `/spec` writes the Heilmeier page
for a survivor. Human gate: which ideas survive.

**Experiments** is what happens after that gate: `/baseline` reproduces the
strongest existing result and reports the gap; `/design` writes the experiment
page before anything runs, with competing hypotheses and the test that
separates them; `/log` appends every attempt to an immutable notebook *before*
its result is known; `/result` tabulates, has a fresh critic read the outcome
against the pre-registration, and walks the M1–M7 checklist over the run
directory; `/replicate` reproduces a published result as a calibration test on
your own pipeline. Human gate: whether to spend compute.

## User Stories

### Pre-mortem

1. As a researcher, I want each idea attacked in a fresh context by an agent that did not generate it, so that the generator never judges its own work.
2. As a researcher, I want the pre-mortem to name the baselines the idea must beat and say whether they exist and run, so that "missing baselines" is caught before three months are spent.
3. As a researcher, I want it to name the field's own metric and say whether the idea's evaluation uses it, so that an idea is not scored on a metric nobody in the field reports.
4. As a researcher, I want feasibility judged as if the idea will be executed rather than reviewed, in my actual time and compute, so that the judgement matches the measured failure it exists to prevent.
5. As a researcher, I want any dependency on a study I will not run — a human evaluation, an annotation campaign, hardware I do not have — named as a blocker, so that an infeasible evaluation plan is visible at ranking time.
6. As a researcher, I want the pre-mortem written as its own file rather than edited into the idea page, so that the thing being judged is not rewritten by its judge.
7. As a researcher, I want each pre-mortem to end in one of three states — executable, executable with changes, or not executable as written — so that `/rank` has something to read.

### Ranking

8. As a researcher, I want ideas compared in pairs by a judge that sees both and neither's author, so that ranking is comparative rather than a set of absolute scores.
9. As a researcher, I want the number of pairings bounded and the bound visible before anything runs, so that ranking twelve ideas does not cost sixty-six judge calls.
10. As a researcher, I want every pairing to name a winner and the one sentence that decided it, so that the ranking can be argued with.
11. As a researcher, I want the result plotted on feasibility against interest with the hard-but-feasible region marked, so that I can see the quadrant Alon says students avoid.
12. As a researcher, I want the final order to be by cheapest kill first, not by score, so that the next thing I run is the one most likely to end the project early.
13. As a researcher, I want ideas whose pre-mortem said "not executable as written" listed separately rather than ranked, so that a broken idea does not outrank a working one on interest.
14. As a researcher, I want `/rank` to re-run after a result lands and say what moved, so that the order reflects what was learned.
15. As a researcher, I want the ranking to be a human gate — it proposes, I choose — so that nothing proceeds to compute on a judge's say-so.

### The Heilmeier page

16. As a researcher, I want a surviving idea written as the eight Heilmeier answers in eight paragraphs on one page, so that I can hand it to somebody who has ten minutes.
17. As a researcher, I want the page to draw its facts from the idea page, the pre-mortem and the cards rather than from memory, and to name where each came from, so that it is checkable.
18. As a researcher, I want the page to state the midterm and final checks as dated, testable things, so that "how will you know" has an answer before the work starts.
19. As a researcher, I want a page that does not fit on one page to be reported as still a brainstorm, so that the catechism's own test is applied.

### Baselines

20. As a researcher, I want `/baseline` to read a paper card and my data description and write the reproduction plan before anything runs, so that reproducing is a plan and not an afternoon of guessing.
21. As a researcher, I want the plan to name the exact published number it is trying to hit, with the card and the table it came from, so that the comparison has a target.
22. As a researcher, I want the gap between the published number and mine recorded with both numbers and the conditions, so that "close enough" is a judgement I make against data.
23. As a researcher, I want a baseline that cannot be reproduced to be recorded as contested, with what was tried, so that Musgrave's rule has a place to land.
24. As a researcher, I want `/replicate` to run the same machinery against a paper I am not building on, as a calibration test of my own pipeline, so that I know whether my reproduction gaps mean anything.

### Designing an experiment

25. As a researcher, I want the experiment page written before the run, so that post-hoc changes are visible as changes.
26. As a researcher, I want two or three competing hypotheses and the experiment that discriminates between them, so that confirming one hypothesis is not the outcome.
27. As a researcher, I want the metric, the baseline and why each was chosen written down, so that the choice can be attacked later.
28. As a researcher, I want a variance plan — which sources of randomness, how many seeds — written before the run, so that variance is not discovered after the fact.
29. As a researcher, I want the leakage checklist applied to my own split before the run, so that my number is not the one that gets retracted.
30. As a researcher, I want the compute budget and the hyperparameter search size stated, so that the comparison is fair by Dodge's rule.
31. As a researcher, I want an explicit stop rule — if X I abandon, if Y I continue — so that the decision is made before the number is known.
32. As a researcher, I want a method idea to get an ablation plan that isolates the source of any gain, so that Lipton's failure is designed out rather than reviewed for.
33. As a researcher, I want the experiment page checked mechanically for the seven pre-registration fields, so that an incomplete pre-registration cannot be run from.

### The notebook

34. As a researcher, I want every attempt appended to one notebook before its result is known, with the date, the config hash and the seeds, so that post-hoc selection is impossible rather than discouraged.
35. As a researcher, I want the notebook to be append-only, so that an attempt that embarrassed me is still there.
36. As a researcher, I want `/log` to read my run directories through a script and tell me what it found and what it could not parse, so that ingestion is a reported state and not a guess.
37. As a researcher, I want the script to work on run directories I did not format for it, so that I do not have to adopt a layout to use the plugin.
38. As a researcher, I want a single-seed number refused entry to any results table, with the refusal recorded, so that Henderson's rule is enforced and not merely stated.
39. As a researcher, I want every notebook entry to name the experiment page it belongs to, so that a run with no pre-registration is visible.

### Results

40. As a researcher, I want the results tabulated from the run directories rather than retyped, so that the table and the runs cannot disagree.
41. As a researcher, I want every number in a table to carry its run directory, its seed count and its variance, so that a number with no run behind it is obvious.
42. As a researcher, I want a fresh-context critic to read the outcome against the pre-registration and return survived, killed, or inconclusive, so that the person who wanted it to work is not the one deciding whether it did.
43. As a researcher, I want the critic to be given the pre-registered stop rule and to apply it literally, so that "inconclusive" has to be argued for rather than defaulted to.
44. As a researcher, I want the M1–M7 checklist walked against the run directory with each detection question answered from a file, so that a hallucinated result has seven chances to be caught.
45. As a researcher, I want any failure mode the auditor cannot check to be named as unchecked with what it looked at, so that a clean audit means something.
46. As a researcher, I want `/result` to leave the experiment page alone and write its own file, so that the pre-registration is never edited to match the outcome.

### Plumbing and honesty

47. As a researcher, I want every new agent fenced exactly like the existing ones — writing only under the research folder, no web tools — so that the fence is enforcement and not prose.
48. As a researcher, I want no agent able to run my training code, so that the thing that spends my compute is me.
49. As a researcher, I want every new template registered with the heading checker, so that a skill cannot claim a heading that does not exist.
50. As a researcher, I want a checker over experiment pages and result pages, so that an incomplete pre-registration or a number with no run behind it is caught mechanically.
51. As a researcher, I want the README, the design doc and the glossary updated, so that a new person can find the eight new skills in five minutes.

## Implementation Decisions

### The guard decides this chunk's shape

The build plan says "the experiment agents get Bash and file access to your code
and data, and no web tools. That's enforced in the agent frontmatter and by the
guard." **Half of that is impossible as written.** `hooks/guard.py` sets
`SCRIPT_ROOT = ("scripts", "retrieval")` and refuses any Bash that is not
`python3 <plugin>/scripts/**.py`, with no shell syntax and nothing chained. An
agent cannot run `python train.py`, and it should not be able to.

So:

- **No agent runs the user's code. Ever.** "File access to your code and data"
  is honoured as Read, Grep and Glob: the agents read the training script, the
  config, the run directory and the metrics files as files. That is what they
  need to design, tabulate and audit.
- **The one command an agent may run is this plugin's own.** `SCRIPT_ROOT`
  widens from `("scripts", "retrieval")` to `("scripts",)` so `ingest_runs.py`
  can live in `scripts/` where it belongs rather than being smuggled into the
  retrieval directory. The fence's actual guarantees — this plugin's own
  reviewed code, no shell syntax, no chaining, no other binary — are unchanged,
  and the guard selftest gains the cases that prove it.
- **Running the experiment is the main thread's, behind the human gate the plan
  already names.** `/design` writes the page; the user runs the run; `/log`
  ingests it. "Whether to spend compute" stops being prose and becomes the fact
  that nothing else *can* spend it.

This is the chunk's one departure from the milestone as written, and it is the
guard doing its job.

### Where things live

| File | Written by | Why its own file |
|---|---|---|
| `research/premortems/<slug>-<date>.md` | `premortem-agent` | a judge does not edit what it judges |
| `research/RANKING.md` | `/rank` | one ranked list, rewritten per run, with its history in `## Previous orders` |
| `research/specs/<slug>.md` | `/spec` | the Heilmeier page, one per surviving idea |
| `research/baselines/<card-slug>.md` | `baseline-reproducer` | one per baseline, reused by `/replicate` |
| `research/experiments/<slug>.md` | `experiment-designer` | the pre-registration; never edited after a run |
| `research/NOTEBOOK.md` | `/log` | one append-only notebook, the whole point of which is that it is one |
| `research/results/<slug>-<date>.md` | `results-tabulator`, then the critic and auditor | dated, because a second run is a second result and neither overwrites the other |

**The idea page's nine headings do not change.** Chunk 8 shipped them and three
skills read them; a pre-mortem section added now would break a shipped contract
for no gain. `/rank` reads the page and the pre-mortem file side by side.

**Nothing under `research/` is overwritten except `RANKING.md`**, which is a
current-state file and keeps its own history inside itself. The chunk-8 rule
holds everywhere else: dated paths, deduplicated by numeric suffix, because a
notebook entry and a result cite their sources by path.

### `/premortem`

- Skill in the main thread: Read, Glob, Grep, Write, AskUserQuestion, Agent.
- With no arguments, proposes every idea page with no pre-mortem, newest first,
  and waits. With slugs, takes those. **Cap: five per run**, the same cap
  `/read` uses and for the same reason.
- One `premortem-agent` per idea, dispatched in one message, each in a fresh
  context with only the idea page, `QUESTION.md`, `CONTEXT.md`, and the card
  paths the idea names.
- Reports: pre-mortems written, and the count in each of the three states.

### `premortem-agent`

- Read, Write. No Bash, no web.
- Writes `research/premortems/<slug>-<date>.md` from its template. Seven
  headings: the idea restated in its own words (so a misreading is visible),
  baselines it must beat and whether each exists and runs, the field's metric
  and whether the idea uses it, the evaluation plan and what it depends on,
  what would have to be true that probably is not, the three-state verdict, and
  what would change the verdict.
- **Judges execution, not novelty.** Novelty was settled at `/ideas` by
  retrieval; re-litigating it here is the failure mode. Its refusals table says
  so.
- **Feasibility is judged in the user's stated compute and time**, taken from
  `CONTEXT.md`. Where `CONTEXT.md` does not say, it writes `constraint unknown`
  and names what it assumed — never a silent assumption of a cluster.

### `/rank` and `tournament-judge`

- Skill in the main thread: Read, Glob, Write, Edit, AskUserQuestion, Agent.
- **The bound, shown before anything runs.** Ideas with a pre-mortem verdict of
  `not executable as written` are set aside, not ranked. Of the rest: five or
  fewer ideas get a full round-robin (at most ten pairings); more than five, each
  idea meets three others chosen to span different seed kinds, capped at
  **twelve pairings total**. The pairing list is shown with the count and the
  user approves it.
- Judges dispatched at most six per message.
- **`tournament-judge`**: Read, Write. One pairing per dispatch. Sees both idea
  pages and both pre-mortems and nothing about who wrote them or how they were
  generated. Writes one comparison file: the winner, the single sentence that
  decided it, each idea's feasibility and interest scored one to five with the
  evidence line behind each, and what would flip the result.
- **The order is by cheapest kill, not by wins.** Wins and the Alon plot are
  both written; the ordering rule is Steinhardt's — the experiment most likely
  to end the project, first. `RANKING.md` states the cost of each kill and
  orders on it, with the tournament result beside it, and says plainly where the
  two disagree.
- The Alon plot is a five-by-five text grid, feasibility against interest, with
  the hard-but-feasible region marked, drawn from the judges' scores.
- **A human gate.** The skill proposes an order and asks which ideas survive;
  what the user says goes in `## Surviving`, in their words.
- Re-running after a result: the previous order moves to `## Previous orders`
  with its date, and `## Status` says what moved and why.

### `/spec`

- Skill in the main thread: Read, Glob, Write. No agents — this is a page
  written from files that already exist.
- Reads the idea page, its pre-mortem, `RANKING.md`, `QUESTION.md`, and any
  card the idea names. Writes `research/specs/<slug>.md`: the eight Heilmeier
  questions as eight paragraphs, each sourced.
- **Every factual sentence names where it came from.** A Heilmeier page that
  cannot source its "how is it done today" is answering from memory.
- **The one-page test is applied and reported.** Over about 800 words, the skill
  says so: by the catechism's own rule it is still a brainstorm.

### `/baseline`, `/replicate` and `baseline-reproducer`

- Skill in the main thread: Read, Glob, Grep, Bash, Write, AskUserQuestion,
  Agent. Takes one card slug (`/baseline`) or one card slug plus
  `--calibration` (`/replicate`).
- **`baseline-reproducer`**: Read, Grep, Glob, Write, Bash (plugin scripts
  only). Reads the card, the fetched full text, the datasets ledger row, and
  the user's own code and data description, and writes
  `research/baselines/<card-slug>.md`: the exact published number with the card
  and table it came from, what the paper says about its setup, what the user's
  setup differs in, the reproduction plan as numbered steps the user can run,
  and — after a run — the achieved number, the gap, and the conditions.
- **It does not run anything.** The plan is written, the user runs it, and the
  skill records what came back. `## Reproduction status` is one of: `not
  attempted`, `attempted, gap recorded`, or `contested` — the last being
  Musgrave's state, for a published number that would not reproduce, with what
  was tried.
- `/replicate` is the same machinery pointed at a paper the user is *not*
  building on, and its file says so: the gap is a fact about the pipeline, not
  about the paper.

### `/design`, `experiment-designer` and `ablation-planner`

- Skill in the main thread: Read, Glob, Grep, Write, AskUserQuestion, Agent.
  Takes one idea slug. Refuses to write an experiment page for an idea whose
  pre-mortem says `not executable as written`, and says which blocker.
- **`experiment-designer`**: Read, Grep, Glob, Write. Writes
  `research/experiments/<slug>.md` from the template: the seven
  pre-registration fields (hypothesis, baseline and why, metric and why, seeds
  and variance plan, leakage check, compute budget and search size, stop rule),
  plus Platt's two or three competing hypotheses and the one experiment that
  discriminates between them.
- **`ablation-planner`**: Read, Write. Dispatched only for a method idea.
  Writes the `## Ablations` section content: per claimed source of gain, the
  ablation that removes exactly that and nothing else, and what result would
  show the gain came from somewhere else.
- **The leakage check reuses chunk 7's taxonomy**, applied to the user's own
  split rather than to a paper's, and cites the dataset row where one exists.
- `check_experiments.py` runs before the skill reports, and the skill fixes what
  it names.

### `/log`, `ingest_runs.py` and `variance-checker`

- Skill in the main thread: Read, Glob, Bash, Write, Edit, AskUserQuestion,
  Agent.
- **Two modes, and the first is the point.** `/log --start <slug>` appends the
  attempt to `research/NOTEBOOK.md` **before the run**, with the date, the
  experiment page, the config hash and the seeds. `/log <run-dir>` ingests
  afterwards and attaches results to that entry by config hash. An ingest that
  finds no opening entry says so: a run with no pre-registration is a finding,
  not an error.
- **`ingest_runs.py`** (standard library only, JSON on stdout, states not
  errors): walks a directory for run-shaped subdirectories — anything holding a
  config (`.json`, `.yaml`, `.yml`, `.toml`, `.ini`), a metrics file (`.json`,
  `.jsonl`, `.csv`), or a log. Per run it reports the path, the config file and
  a hash of its bytes, any seed it can find in the config, the metric keys and
  their final and best values, the mtime range, and an exit code if a log
  carries one. **What it cannot parse is reported per file with the reason**,
  and nothing is inferred: a run with no seed reports `seed: not found`, never
  a guess. It never writes to the run directory.
- **`variance-checker`**: Read, Write. Reads the ingest output and the
  experiment page's variance plan, and returns per metric whether the seed count
  meets the plan. **A single-seed number is refused entry to a results table**,
  and the refusal is written into the notebook entry rather than being a silent
  omission.

### `/result`, `results-tabulator`, `results-critic`, `failure-mode-auditor`

- Skill in the main thread: Read, Glob, Bash, Write, AskUserQuestion, Agent.
  Takes one experiment slug. Runs in three rounds, because two of the three
  agents must not see what the others concluded.
- **`results-tabulator`**: Read, Write, Bash (`ingest_runs.py`). Builds the
  table from the ingest output only. Every row carries its run directory, seed
  count and variance. A number it cannot source from a run directory does not
  enter the table; it goes under `## Not sourced` with what was looked for.
- **`results-critic`**: Read, Write. Fresh context. Given the experiment page's
  pre-registration and the table, and *not* the tabulator's commentary. Applies
  the pre-registered stop rule literally and returns `survived`, `killed` or
  `inconclusive`, with the clause of the stop rule that decided it.
  `inconclusive` must be argued: it names what additional evidence would
  decide.
- **`failure-mode-auditor`**: Read, Grep, Glob, Write, Bash (`ingest_runs.py`).
  Walks M1 to M7 against the run directory, answering each detection question
  with a file path or `unchecked: <what was looked at>`. No score, no verdict —
  findings and evidence, the same contract `leakage-auditor` lives under.
- The three write into one dated result file; the experiment page is never
  edited. The skill then says `/rank` should be re-run.

### Guard, checker, docs

- `SCRIPT_ROOT` widens to `("scripts",)`. The deny message is reworded to "this
  plugin's own scripts". Selftest gains: `ingest_runs.py` allowed for
  `results-tabulator`; `python train.py` denied; a chained
  `python3 <plugin>/scripts/ingest_runs.py x && rm -rf y` denied; a script
  outside the plugin denied; plus the frontmatter and web cases for all nine new
  agents, and write-scope cases for the four new directories.
- **`check_experiments.py`**, in the shape of `check_ideas.py`: over an
  experiment page it fails on a missing heading, an absent stop rule, a variance
  plan with no seed count, a missing leakage section, and a compute budget that
  is blank; over a result page it fails on a missing verdict, a verdict that is
  not one of the three, a table row with no run directory, and a single-seed
  number in a table without the explicit refusal note. Ships with its own
  selftest and shares `checklib.py`.
- Seven new templates, all registered: premortem, ranking, heilmeier, baseline,
  experiment, notebook, result.
- `CONTEXT.md` gains a selection-and-experiments section. README moves eight
  skills from planned to built and drops `/brief` from the planned list, with
  `/spec` named as the Heilmeier page. `docs/design/skills-and-agents.md` §§ Stage 5–6
  get the built marks and this chunk's decisions. Manifest to `0.9.0`. The build
  plan's Milestone 5 status is rewritten. Chunk note last.

## Testing Decisions

Build only, as with chunks 7 and 8. What ships is the static layer:

- **`ingest_runs.py` selftest** against fixture run directories built in a temp
  dir: a run with JSON config and CSV metrics; one with JSONL metrics; one with
  no seed; one with an unparseable config; one directory that is not a run at
  all. Asserts the JSON shape and the state names, never internals.
- **`check_experiments.py` selftest**: a good experiment page, a good result
  page, and one case per failure kind.
- **Heading parity** for seven templates.
- **Guard selftest** for the widened fence and the nine new agents.

## Out of Scope

- Evals under `evals/`, and any live run.
- Milestone 6: `/router`, `/start`, `/orient`, `/think`, hooks finalized.
- `/render` and `/figure` — Milestone 2's deferred presentation pair. `/brief`
  is not deferred any longer: `/spec` is that page (decision 3).
- Any agent running the user's training code, and any widening of the Bash fence
  beyond this plugin's own `scripts/` directory.
- Writing into the user's run directories. `ingest_runs.py` reads only.
- Any access to the remote GPU box. The user syncs run directories down first.
- Editing the idea page's nine headings, an experiment page after a run, or any
  line of `NOTEBOOK.md`.
- Computing a score for novelty, typicality, diversity or idea quality. The
  tournament's one-to-five scores are a judge's written judgement with evidence
  beside them, like the concession ladder's.
- A second-provider model for any judge. `model: inherit`, as everywhere.

## Further Notes

- **Build order for `/to-tickets`.** Templates (premortem, ranking, heilmeier);
  `premortem-agent`; `/premortem`; `tournament-judge`; `/rank`; `/spec`;
  `ingest_runs.py` with its selftest and the guard widening; templates
  (baseline, experiment, notebook, result); `check_experiments.py`;
  `baseline-reproducer`; `/baseline` and `/replicate`; `experiment-designer` and
  `ablation-planner`; `/design`; `variance-checker`; `/log`;
  `results-tabulator`, `results-critic`, `failure-mode-auditor`; `/result`;
  guard cases and heading registry; docs, glossary, README, manifest, chunk note.
- **Why the notebook is one file.** Post-hoc selection is impossible only if
  every attempt lands in the same place before its result is known. A notebook
  per experiment would let an embarrassing one quietly not exist.
- **The three-state verdict everywhere.** Pre-mortem returns executable /
  executable with changes / not executable; the results critic returns survived
  / killed / inconclusive; reproduction returns not attempted / gap recorded /
  contested. Three states, named, in all three places, so that a downstream
  skill reads a value rather than prose.
