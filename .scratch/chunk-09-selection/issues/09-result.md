# 09: `/result` and its three agents

Type: task
Status: ready-for-agent
Blocked by: 01, 05, 08

## What to build

Reading the outcome against what was pre-registered, in three rounds, because
two of the three agents must not see what the others concluded.

**`agents/results-tabulator.md`** — Read, Write, Bash (`ingest_runs.py` only).
Builds the table from the ingest output only. Every row carries its run
directory, seed count and variance. **A number it cannot source from a run
directory does not enter the table**; it goes under `## Not sourced` with what
was looked for.

**`agents/results-critic.md`** — Read, Write. Fresh context. Given the
experiment page's pre-registration and the table, and **not** the tabulator's
commentary. Applies the pre-registered stop rule literally and returns
`survived`, `killed` or `inconclusive`, with the clause of the stop rule that
decided it. **`inconclusive` must be argued**: it names what additional evidence
would decide.

**`agents/failure-mode-auditor.md`** — Read, Grep, Glob, Write, Bash
(`ingest_runs.py` only). Walks M1 to M7 against the run directory, answering
each detection question with a file path or `unchecked: <what was looked at>`.
No score and no verdict — findings and evidence, the same contract
`leakage-auditor` lives under.

**`skills/result/SKILL.md`** — Read, Glob, Bash, Write, AskUserQuestion, Agent.
Takes one experiment slug, runs the three rounds, and writes one dated file at
`research/results/<slug>-<date>.md`. **The experiment page is never edited.**
Then it says `/rank` should be re-run.

## Acceptance

- [ ] The critic's prompt contains the pre-registration and the table and no tabulator commentary.
- [ ] The verdict is exactly one of the three, with the deciding stop-rule clause quoted.
- [ ] `inconclusive` names what additional evidence would decide.
- [ ] Every table row carries a run directory, a seed count and a variance.
- [ ] A number with no run behind it is under `## Not sourced` with what was looked for.
- [ ] Every M1–M7 question is answered with a file path or `unchecked:` and what was looked at.
- [ ] The result file passes `check_experiments.py`, and the experiment page is byte-identical after the run.
- [ ] A second run writes a second dated file and overwrites nothing.
