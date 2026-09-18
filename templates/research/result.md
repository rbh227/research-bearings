# Result: <the experiment, as a title of three or four words>

<!-- One result, at research/results/<slug>-<date>.md. Seven headings, fixed.
     Written by /research-bearings:result in three rounds: the tabulator builds
     the table, then a fresh critic reads the outcome against the
     pre-registration without seeing the tabulator's commentary, then the
     auditor walks M1 to M7 against the run directory.

     Dated, because a second run is a second result and neither overwrites the
     other. The experiment page is NEVER edited — if this result disagrees with
     what was pre-registered, that disagreement is the most useful thing in the
     record and it survives here. -->

## Table

<!-- Built from the ingest output only, never retyped from memory or from a
     terminal that has scrolled away. One row per number, and every row carries
     where it came from:

     | metric | value | seeds | variance | run directory |
     |---|---|---|---|---|
     | val F1 | 0.612 | 3 | ±0.008 | runs/exp-14/ |
     | val F1 (baseline) | 0.588 | 3 | ±0.011 | runs/base-03/ |

     The columns are read by check_experiments.py, which finds them by header
     name: one column naming the run directory, one naming seeds, one naming
     variance. A row with an empty run directory fails.

     A SINGLE-SEED NUMBER MAY NOT ENTER THIS TABLE. Henderson. If one is here
     anyway, its row says `refused: single seed` and the number is not to be
     compared against anything. That is the only shape in which a one-seed
     number may appear. -->

## Not sourced

<!-- Every number that was wanted and could not be traced to a run directory,
     with what was looked for:

     - <metric> — looked for <the key> in <the directories>, found <what>

     This heading is why the table can be trusted. A number with no run behind
     it does not get quietly dropped and it does not get quietly included; it
     lands here, named. If nothing is missing, say `nothing`. -->

## Verdict

<!-- The fresh critic's answer, applying the pre-registered stop rule
     literally. The first line is this shape and nothing else, because it is
     read mechanically:

     - Verdict: survived
     - Verdict: killed
     - Verdict: inconclusive

     Then, always:

     - The clause that decided it: "<quoted from the experiment page's
       ## Stop rule>"
     - Against: <the rows of the table that clause applies to>

     `inconclusive` MUST BE ARGUED. It names what additional evidence would
     decide, and that evidence is a thing that could actually be obtained.
     "More seeds" is not an argument unless it says how many and why that
     number. An inconclusive with no such line is the critic declining to
     apply the rule it was given. -->

## Failure mode audit

<!-- M1 to M7 against the run directory. Every detection question answered
     with a FILE PATH or with `unchecked:` and what was looked at:

     ### M<n> <name>
     - Detection question: <the question>
     - Answer: <what was found> · <path/to/the/file/that/says/so>
     - or: `unchecked: <what was looked at, and why it did not settle it>`

     No score and no verdict — findings and evidence, the same contract
     leakage-auditor lives under. A clean audit means something only if the
     unchecked ones are visible, so an auditor that cannot check M4 says so
     rather than passing it. -->

## What the pre-registration said

<!-- The experiment page's hypothesis, metric, baseline and stop rule, quoted,
     with the page's path.

     Quoted here so the result is readable on its own and so a later change to
     the experiment page — which is forbidden, and would be visible — could be
     caught. Anything the run did differently from the pre-registration goes
     here as a named deviation with the reason.

     A deviation is not a failure. An invisible deviation is. -->

## Status

<!-- Date. The run directories ingested and what the script could not parse.
     Which of the three agents ran and which did not. The variance checker's
     refusals. What check_experiments.py said. And the next step:

     `/rank` should be re-run: this result changes what is cheapest to kill
     next.

     Written 2026-09-22 by /result from research/experiments/<slug>.md. Ingested
     4 run directories, 1 config unparseable (runs/exp-11/config.yaml). 1 metric
     refused for a single seed. check_experiments.py: clean. -->
