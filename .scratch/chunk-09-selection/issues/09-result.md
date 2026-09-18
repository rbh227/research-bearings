# 09: `/result` and its three agents

Type: task
Status: done
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

- [x] The critic's prompt contains the pre-registration and the table and no tabulator commentary.
- [x] The verdict is exactly one of the three, with the deciding stop-rule clause quoted.
- [x] `inconclusive` names what additional evidence would decide.
- [x] Every table row carries a run directory, a seed count and a variance.
- [x] A number with no run behind it is under `## Not sourced` with what was looked for.
- [x] Every M1–M7 question is answered with a file path or `unchecked:` and what was looked at.
- [x] The result file passes `check_experiments.py`, and the experiment page is byte-identical after the run.
- [x] A second run writes a second dated file and overwrites nothing.

## Resolution

2026-09-18. `agents/results-tabulator.md`, `agents/results-critic.md`,
`agents/failure-mode-auditor.md`, `skills/result/SKILL.md`. Heading parity green
against the template ticket 05 shipped.

**The three agents write notes and the skill assembles the page.** The spec said
"the three write into one dated result file", and the obvious implementation has
the critic writing into a file that already carries the tabulator's words. So
each agent writes under `research/results/notes/` and the skill assembles
`research/results/<slug>-<date>.md`. The critic then never reads a page carrying
the tabulator's commentary, which is the separation the round structure was for.
Precedent: chunk 7's read protocol, where the predictor and reader write notes.

**The auditor is not told the verdict, and that is why it is round 3 rather than
round 2.** An auditor that knows the result was a win looks for reasons it is
fine; one that knows it was a loss stops looking. Both its contract and the
skill's dispatch step say what is withheld.

**`inconclusive` has to name two things or it is not accepted.** Which clause
could not be applied, and what specific obtainable evidence would decide it.
"More seeds" is explicitly refused; "three more seeds on the baseline condition,
because the abandon clause needs five and the table has two" is the shape. The
skill reports an `inconclusive` carrying neither as the critic declining to
answer rather than accepting it as a result.

**A close margin does not soften a verdict.** The rule was written before the
number existed precisely so that 0.2 points would not be argued about
afterwards. The critic may state that it is close; it may not move the verdict.

**M1 to M7 are Lu et al.'s seven, with one detection question each**, taken from
`academic.md`. All seven are answered every run, including the clean ones,
because a clean audit means something only when the `unchecked:` ones are
visible beside it. Every `unchecked:` names what was looked at, so "M4 is fine"
and "nobody could tell about M4" cannot be confused.

**No score, deliberately.** The same contract `leakage-auditor` lives under: one
number cannot carry seven kinds of doubt, and it invites the reader to check the
number instead of the findings.

**M7 is answered from the record, not from the researcher's mind.** Frame-lock
is checked by asking whether the competing hypotheses name a real alternative
and whether any file considered a different framing. Where the record shows
none, the answer is that the record shows none.
