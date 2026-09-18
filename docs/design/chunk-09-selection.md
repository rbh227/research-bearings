# Chunk 9: selection and experiments

2026-09-18. The plugin learns to choose, and then to be honest about what
happened. Eight skills and nine agents in two halves: a pile of idea pages
becomes a ranked list with a Heilmeier page on top of it, and a chosen idea
becomes a pre-registration, a notebook, and a result that something other than
its author has judged.

The spec is `.scratch/chunk-09-selection/spec.md`, with eleven tickets in
`issues/`. **Grilled at the shape level** — one round, nine questions, answered
as one chunk — and the answers are recorded in the spec's own
`## Decisions settled at planning`. Build only: no `evals/` cases and no live
run. The milestone's own test — take a top idea, reproduce a real
damage-assessment baseline, design the smallest killing experiment, log it and
read the result — is the acceptance run, and it belongs to the user.

## 1. Decision record

- **No agent runs the user's code, and that is the chunk's one departure from
  the build plan.** The plan said the experiment agents get "Bash and file
  access to your code and data". `hooks/guard.py` refuses any command that is
  not this plugin's own script, and it was right to. So file access is honoured
  as Read, Grep and Glob — the agents read the training script, the config, the
  run directory and the metrics files *as files*, which is what designing,
  tabulating and auditing actually needs — and the one command any of them may
  run is `ingest_runs.py`. The human gate the plan already named, "whether to
  spend compute", stops being prose and becomes the fact that nothing else
  *can* spend it. `SCRIPT_ROOT` widened from `("scripts", "retrieval")` to
  `("scripts",)` so the ingester could live beside the checkers rather than be
  smuggled into the retrieval directory; every guarantee that mattered is
  asserted rather than assumed, including that `python3 train.py` is still
  denied.

- **The order is the cheapest kill, and the tournament sits beside it.** Two
  rules compete. A pairwise tournament measures interest, which is what a model
  can actually judge — asked to score one idea it returns four every time,
  asked to pick between two it has to find a difference and name it.
  Steinhardt's rule says run the experiment most likely to end the project
  first, because the next month buys information. `RANKING.md` writes both
  orders and **names every place they disagree**, and the disagreement is the
  point: an idea the judges loved whose kill costs three months is exactly the
  trap. When they agree, the line says they agree — its absence and its
  emptiness are different findings.

- **The bound is shown before it is spent.** Twelve ideas compared every way is
  sixty-six judge calls. Round robin at five ideas or fewer, three pairings each
  above that, twelve total and hard, with the list and the count approved before
  the first judge runs. A ranking nobody can afford should be refused before it
  is paid for, not after.

- **The pre-mortem judges execution and nothing else.** Novelty was settled at
  `/ideas` by retrieval and interest belongs to `/rank`, so `premortem-agent`'s
  refusals table has three separate entries for the ways a novelty opinion
  sneaks back in — "done before", "incremental", and judging whether the work is
  worth doing. It has read no literature beyond the cards it was handed, which
  is precisely why an opinion about what exists would be the hallucinated claim
  this plugin is built against. The measured reason: when 43 researchers
  executed randomly assigned ideas over three months, the LLM-generated ideas
  dropped 1.88 of 10 on effectiveness while human ideas barely moved, for
  missing baselines, inappropriate metrics, and evaluation plans nobody could
  run. All three are checkable in an afternoon and none is what a reviewer looks
  at.

- **`executable with changes` is defined by nameability.** If the changes cannot
  be named, the state is `not executable as written`. Without that rule the
  middle state is where every uncertain idea lands and the three states collapse
  into one. The same shape recurs twice more: `inconclusive` must name what
  would decide it, and `contested` must carry the attempt list. **Three states,
  named, in all three places**, so a downstream skill reads a value rather than
  prose.

- **`/spec` absorbed `/brief`, and `brief-writer` is retired.** Milestone 2
  deferred "the Heilmeier one-pager" under that name; this is that page. Two
  commands writing one page was the plan's duplication, not a design. `/render`
  and `/figure` remain planned.

- **An unsourced sentence may exist; it may not be invisible.** Both alternative
  rules fail. Forbidding unsourced sentences produces a Heilmeier page that
  omits what is true but uncited; allowing them silently produces a
  hallucination with eight headings. So they are written in place as `not
  established in the cards I read` and listed under `## Sources` as
  `unsourced:`.

- **The notebook's result is a second block, not a filled-in field.** The spec
  said the ingest "attaches results to that entry", and the obvious reading —
  filling in a `- Result:` line — is an edit. So the opening block carries only
  what is known before the run and has no result field at all, and the ingest
  appends beneath it. The append-only claim then survives contact with the
  second mode, and a planned seed count that disagrees with the actual one stays
  visible as a disagreement rather than being corrected away.

- **The refusal is written down, not omitted.** A single-seed number that
  quietly never reaches a table looks identical to a number nobody produced, so
  `variance-checker`'s refusal lands in the notebook entry and in the table row.
  `short of plan` is deliberately **not** a refusal: three seeds where five were
  planned is a real measurement with three seeds behind it, and the count
  travels with the number. One seed is different in kind, because there is no
  variance estimate at all.

- **`/result` runs in three rounds and the separation is the design.** The
  tabulator builds the table and writes no judgement; the critic gets the
  pre-registration and the table and **not** the tabulator's words; the auditor
  walks M1–M7 and is **not told the verdict**, because an auditor that knows the
  result was a win looks for reasons it is fine and one that knows it was a loss
  stops looking. The three write notes under `research/results/notes/` and the
  skill assembles the page, so the critic never reads a file carrying the
  tabulator's commentary. Precedent: chunk 7's read protocol.

- **The experiment page is never edited after a run.** Not to correct a metric
  name, not to record what actually happened. If the result disagrees with the
  pre-registration, that disagreement is the most useful thing in the record and
  it survives only while the pre-registration is left alone. A changed design is
  a new page with a new slug and the old one stays.

- **`/replicate` is its own command rather than a flag.** What the gap means has
  to be fixed before the run. A gap discovered on a paper you have no stake in
  is a gap you will read as the paper's fault, so the skill refuses a paper the
  researcher is building on and writes the sentence that keeps the file readable
  a year later. Its output is the comparison against every other gap under
  `research/baselines/`, not the gap itself.

- **No scores, again.** The tournament's one-to-five numbers are written
  judgements with evidence lines beside them, the grid is integers, and
  `failure-mode-auditor` returns no score at all — one number cannot carry seven
  kinds of doubt, and it invites the reader to check the number instead of the
  findings. The decision that struck `similarity.py` in chunk 3 still stands.

## 2. What the build found

- **`ingest_runs.py` has no `best` field, and refusing to add one is the point.**
  The spec asked for "final and best values". Best needs a direction — up for
  accuracy, down for loss — and the script cannot know which. A field named
  `best` that silently meant `max` would put a loss's worst value in a results
  table, which is exactly the class of number this chunk exists to catch. Each
  metric carries `final`, `min`, `max` and `count`; the caller picks the end it
  wanted. A selftest case asserts `best` is absent.

- **The experiment-page classifier was wrong on its first version, and the
  selftest caught it.** `check_experiments.py` decided which rule set to apply
  by keying on `## Stop rule` against `## Verdict`. So an experiment page whose
  stop-rule heading was misspelled — the page most worth failing loudly — was
  the one page the classifier could not recognise, and it reported "cannot tell
  whether this is an experiment page or a result page" instead of "missing
  heading: ## Stop rule". Both statements are true and only one is useful. It
  now counts how many of each set's headings are present and takes the better
  match.

- **Ticket 10 said seven agents have no Bash; it is six.** Nine agents, three
  granted Bash — `baseline-reproducer`, `results-tabulator`,
  `failure-mode-auditor` — and six without. Corrected in the ticket rather than
  left to be read later as a missing case.

- **What actually stops the six is their frontmatter, not the fence.** The
  guard's Bash rule admits any agent this plugin ships to the plugin's own
  scripts, so a `results-critic` granted Bash could run the ingester. It is not
  granted Bash, and the selftest reads that out of the file rather than assuming
  it — the same mechanism chunk 8 used for `predictor`. The guard is at 133
  cases.

- **Table columns are found by header name, not by position.** A result page is
  written by an agent, and fixing the column order would fail a correct table
  that put the run directory second. One selftest case reorders every column and
  still passes; another removes the run-directory column entirely and fails on
  the header before any row is read.

- **The notebook template has two headings, which is the fewest in the repo.**
  `## The rule` and `## Entries`. The rule is copied into every notebook so that
  anyone opening the file a year later knows what it promises without having to
  find the skill that wrote it.

## 3. What is open

- **Nothing has been run.** Every file in this chunk is a contract, and no
  pre-mortem, ranking, Heilmeier page, baseline, experiment, notebook entry or
  result has been produced by an actual dispatch. The static layer is green:
  `ingest_runs.py` at 17 cases, `check_experiments.py` at 26, the guard at 133,
  heading parity across 28 templates.

- **`ingest_runs.py` has met no real run directory.** Its fixtures are five
  shapes built in a temp dir. The first contact with a directory somebody else's
  training script wrote will find something, and the honest expectation is that
  it will be a classification rule, not a crash — the script reports what it
  cannot parse rather than failing on it.

- **Run directories are read on this machine only.** The user's experiments run
  on a remote GPU box; they sync directories down and the plugin never touches
  the remote. If that becomes the friction point, the answer is a sync step in
  `/log`, not an agent with ssh.

- **`/rank` re-runs the whole tournament after a result.** Only `## Order` is
  preserved, into `## Previous orders`. That is defensible — a judge's opinion
  formed before a result landed is an opinion about a different world — and it
  is also the most expensive thing in the selection half. If it bites, the cheap
  fix is to re-run only the pairings involving ideas the result touched.

- **`/spec`'s 800-word threshold is a guess.** Heilmeier's rule is "one page",
  and one page is not a word count. The skill reports rather than enforces, so a
  wrong threshold costs a sentence in `## Status` and nothing else.

- **The `## Ablations` handoff is the one place two agents write one section.**
  `experiment-designer` leaves the heading and `ablation-planner` fills it
  through the skill. It is the only such seam in the chunk, and it exists
  because the thing that designed the method is the last thing that should
  decide which part of it to doubt.
