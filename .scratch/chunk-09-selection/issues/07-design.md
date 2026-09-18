# 07: `/design`, `experiment-designer` and `ablation-planner`

Type: task
Status: ready-for-agent
Blocked by: 02, 05

## What to build

The page written **before** the run, so that a post-hoc change is visible as a
change.

**`agents/experiment-designer.md`** — Read, Grep, Glob, Write. Writes
`research/experiments/<slug>.md` from the template: the seven pre-registration
fields, plus two or three competing hypotheses and the one experiment that
discriminates between them. The leakage check reuses chunk 7's taxonomy, applied
to the user's own split rather than to a paper's, and cites the dataset ledger
row where one exists.

**`agents/ablation-planner.md`** — Read, Write. Dispatched only for a method
idea. Writes the `## Ablations` content: per claimed source of gain, the
ablation that removes exactly that and nothing else, and what result would show
the gain came from somewhere else.

**`skills/design/SKILL.md`** — Read, Glob, Grep, Write, AskUserQuestion, Agent.
Takes one idea slug. **Refuses to write an experiment page for an idea whose
pre-mortem says `not executable as written`**, and says which blocker.
`check_experiments.py` runs before the skill reports, and the skill fixes what
it names.

An experiment page, once written, is never edited after a run.

## Acceptance

- [ ] An idea with a `not executable as written` pre-mortem is refused, with the blocker named.
- [ ] The page carries all seven pre-registration fields and passes `check_experiments.py`.
- [ ] Two or three competing hypotheses are stated with the experiment that separates them.
- [ ] The stop rule says what result means abandon, before any number exists.
- [ ] `ablation-planner` runs only for a method idea, and the skill says when it did not.
- [ ] The leakage check is applied to the user's split and cites the dataset row where one exists.
