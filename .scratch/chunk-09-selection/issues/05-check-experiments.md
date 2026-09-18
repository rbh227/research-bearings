# 05: the experiment and result templates, and `check_experiments.py`

Type: task
Status: done
Blocked by: —

## What to build

The two pages the experiment half writes, and the checker over them.

**`templates/research/experiment.md`** — comment-only. The seven
pre-registration fields, each its own heading: hypothesis, baseline and why,
metric and why, seeds and variance plan, leakage check, compute budget and
search size, stop rule. Plus `## Competing hypotheses` (two or three, and the
one experiment that discriminates between them) and `## Ablations`.

**`templates/research/result.md`** — comment-only. The table, `## Not sourced`,
the three-state verdict with the clause of the stop rule that decided it, the
M1–M7 audit, and `## Status`.

**`scripts/check_experiments.py`** — in the shape of `check_ideas.py`: a module
docstring saying what each rule is for and why, a `check()` returning a list of
failure strings, a `main()` over paths or a directory, `--selftest`, and
**shared code from `checklib.py`** rather than a fifth copy of `sections()` and
the paper-line regex.

Over an experiment page it fails on: a missing heading; an absent stop rule; a
variance plan with no seed count; a missing leakage section; a blank compute
budget.

Over a result page it fails on: a missing verdict; a verdict that is not one of
the three; a table row with no run directory; a single-seed number in a table
without the explicit refusal note.

## Acceptance

- [x] `python3 scripts/check_experiments.py --selftest` is green.
- [x] A good experiment page and a good result page pass; there is one case per failure kind above.
- [x] Each failure message names the thing that failed.
- [x] Passing a directory checks every page in it.
- [x] The two templates carry every heading the checker requires, asserted by the last selftest case as `check_cards` does.
- [x] Nothing that already lives in `checklib.py` is copied into this file.

## Resolution

2026-09-18. `templates/research/experiment.md`, `templates/research/result.md`,
`scripts/check_experiments.py`, 26 selftest cases green. `sections()` comes from
`checklib.py`; nothing shared was copied.

**The stop rule has a fixed line shape, and that is the rule with teeth.**
`- Abandon if: <result>`. A stop rule written as prose is one `results-critic`
has to interpret, and three months later the interpretation is whoever wants the
result's. Case 4 is a page that says "we will stop if the results look bad",
which reads like a stop rule and is not one.

**The page classifier was wrong on its first version, and the selftest caught
it.** `kind()` keyed on `## Stop rule` against `## Verdict`, so an experiment
page whose stop-rule heading was misspelled — the page most worth failing loudly
— was the one page the classifier could not recognise, and it reported "cannot
tell" instead of "missing heading". It now counts how many of each set's
headings are present and takes the better match. Case 3 is that page.

**Table columns are found by header name, not by position.** A result page is
written by an agent, and fixing the column order would make the checker fail on
a correct table that happened to put the run directory second. Case 15 reorders
every column and still passes; case 14 is a table with no run-directory column
at all, which fails on the header before any row is read.

**A single-seed row may exist only carrying `refused`.** Refusing it outright
would make the number vanish, and a silent omission is what Henderson's rule
exists to prevent. Case 13 is the bare row failing, 13b the refused row passing.

**Two rules beyond the ticket, both from the spec's user stories.** An empty
hypothesis, baseline or metric fails (case 8) — a pre-registration that
pre-registers nothing is what the critic would compare the outcome against. And
a compute budget with no `- Search size:` fails (case 7b), which is Dodge's
rule: a method given a hundred configurations against a baseline given ten is a
result about the search.

**A page carrying both heading sets is refused.** An experiment page is never
edited after a run, so a result belongs in its own dated file. Case 16b.

**Adversarial review, 2026-09-18.** A seed cell of `unknown`, `0` or nothing
passed the gate, because the rule acted only on a cell beginning with 1. A row is
now comparable only with a positive integer seed count; anything else must carry
`refused`. Five regression cases; 31 total.
