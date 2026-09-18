# 07: `/design`, `experiment-designer` and `ablation-planner`

Type: task
Status: done
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

- [x] An idea with a `not executable as written` pre-mortem is refused, with the blocker named.
- [x] The page carries all seven pre-registration fields and passes `check_experiments.py`.
- [x] Two or three competing hypotheses are stated with the experiment that separates them.
- [x] The stop rule says what result means abandon, before any number exists.
- [x] `ablation-planner` runs only for a method idea, and the skill says when it did not.
- [x] The leakage check is applied to the user's split and cites the dataset row where one exists.

## Resolution

2026-09-18. `agents/experiment-designer.md`, `agents/ablation-planner.md`,
`skills/design/SKILL.md`. Heading parity green against the template ticket 05
shipped.

**Three outcomes on the pre-mortem, not two.** `not executable as written`
refuses with the blocker quoted and the line that would change the verdict. No
pre-mortem at all also refuses, because this page's baselines and metric come
from that judgement and without it they come from the person who wants the idea
to work. `executable with changes` proceeds and **the changes are named in the
report**, so they are not quietly dropped between the two skills.

**Whether this is a method idea is asked, not inferred.** The idea page does not
reliably say, and guessing wrong drops the section that identifies where a gain
came from. One `AskUserQuestion`, and the heading reads `not a method idea: no
ablation plan` when the answer is no — an absent section and a section saying
the question was asked are different findings.

**`ablation-planner` is separate from `experiment-designer` for the reason every
agent here is separate from its neighbour**: the thing that designed the method
is the last thing that should decide which part of it to doubt.

**The hardest line in the ablation contract is "exactly that and nothing else."**
Removing a loss term usually also removes a second forward pass, its
augmentation and a third of the compute, and then the ablation measures four
things and attributes the result to one. So each ablation states what it holds
fixed, and two changes that cannot be separated are **named as inseparable**
rather than given an ablation that silently conflates them.

**`If the gain survives this:` is required on every ablation.** It names the
outcome under which the method's story is wrong. A section where every line
predicts the story holding was written to agree.

**A missing discriminating experiment is a finding, not a blank.** Platt's
section may say that no run discriminates; what it may not do is contain an
invented one, which makes the page worse than empty.

**The checker runs before the skill reports.** A blank budget, a stop rule with
no `- Abandon if:` line and a variance plan with no seed count all make the page
unusable to `/result`, and all three are caught mechanically rather than by
review.
