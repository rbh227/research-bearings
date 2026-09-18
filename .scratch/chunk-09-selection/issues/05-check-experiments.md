# 05: the experiment and result templates, and `check_experiments.py`

Type: task
Status: ready-for-agent
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

- [ ] `python3 scripts/check_experiments.py --selftest` is green.
- [ ] A good experiment page and a good result page pass; there is one case per failure kind above.
- [ ] Each failure message names the thing that failed.
- [ ] Passing a directory checks every page in it.
- [ ] The two templates carry every heading the checker requires, asserted by the last selftest case as `check_cards` does.
- [ ] Nothing that already lives in `checklib.py` is copied into this file.
