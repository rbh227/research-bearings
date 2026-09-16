# 11: `/critique` and `critic`

Type: task
Status: ready-for-agent
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

- [ ] Plugin validation green; heading parity green for the critique template.
- [ ] On an existing analog page, the critique file has findings each anchored to a quoted passage, then scored rebuttals, with no two consecutive concessions and the human flag when over half concede.
- [ ] The critiqued file's content is byte-identical before and after.
- [ ] The critic's frontmatter grants no Bash, no Edit, no web tool.
