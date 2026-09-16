# 11: `/critique` and `critic`

Type: task
Status: done
Blocked by: None (can start immediately)

## What to build

`critic` (Read, Write), fresh context, model inherits. First pass: given one
file under the research folder, the context page and the question page, writes
the critique file from a new template: findings, each with the passage it
attacks, the objection, and the ask. Second pass: given the rebuttals, scores
each one to five, concedes only at four or above, never concedes two findings
in a row, flags for a human when more than half are conceded; repeated
pushback, appeals to authority and bare requests to soften score one. The
pattern is `question-critic`'s ladder, generalised to any file.

`/critique <file>` (Read, Glob, Write, Agent): dispatches the critic; reads
the critique; writes one rebuttal per finding as the author; sends the
rebuttals back to the same critic; records the scored outcome in the critique
file. Critiques live in a critiques directory under the research folder, one
dated file per critiqued file per run. The critiqued file is never edited.

## Acceptance

- [x] Plugin validation green; heading parity green for the critique template.
- [x] On an existing analog page, the critique file has findings each anchored to a quoted passage, then scored rebuttals, with no two consecutive concessions and the human flag when over half concede.
- [x] The critiqued file's content is byte-identical before and after.
- [x] The critic's frontmatter grants no Bash, no Edit, no web tool.

## Resolution

2026-09-16. `agents/critic.md`, `skills/critique/SKILL.md`,
`templates/research/critique.md`.

Live on the bits file written earlier the same day in the main thread. The
run output was moved to `evals/read/runs/damage/` after review; the critique
is `evals/read/runs/damage/critiques/BITS-2026-09-16.md`.
Four findings, each anchored to a quoted passage, ordered worst first. All
four were correct.

The worst of them: the file grouped `shen-2021-bdanet` under a thesis of "one
network trained end to end" when that card's own Delta describes BDANet as a
two-stage framework and its Kill experiment contrasts it against
"single-stage, one-network approaches". The critic also caught a card marked
`_not read_` being used as evidence about what a paper does not state, a
two-part assumption whose second half rested on one card while the first
rested on three, and an ellipsis that lost which paper concatenates and which
subtracts.

The bits file was not touched by the critic or the skill; it was revised
afterwards, against the findings, as a separate step.

**The ladder ran twice and both rebuttals scored 1.** Both were agreements
dressed as rebuttals, and the critic said so rather than accepting them: an
admission is not evidence against a finding. On the first it went further and
found an error inside the rebuttal — `gupta-2020-rescuenet` never frames its
own contribution as fusion-by-difference; that reading exists only inside
`shen-2021-bdanet`, as BDANet's description of a rival.

**Two ladder rules did not fire, and the ticket should say so.** "Never
concede twice in a row" and the runaway-agreement flag both need the critic to
concede, and it conceded nothing. The two remaining findings were conceded by
the author before the ladder, because checking the cards first removed the
evidence the rebuttals would have rested on — in one case the drafted rebuttal
claimed `gupta-2019-xbd` never says which partition its number came from, and
the card says "on the pooled test set". Both rules are in the contract with
their conditions; neither has been exercised live.
