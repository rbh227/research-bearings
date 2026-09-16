# 05: The `/verify` skill

Type: task
Status: ready-for-agent
Blocked by: 02

## What to build

`/verify <file>` (Read, Glob, Bash, Edit). Finds every reference line in one
research file: the landscape line shape, the card reference shape, and
bracketed or parenthetical citations carrying a title. Sends the batch to the
existing `verify` verb. Edits each line in place: appends `· verified` on an
exact match, the candidate marker with the near id on a partial match, and
`· _not found: checked <indexes>_` otherwise. Lines already tagged are
re-checked and the tag replaced only if the state changed. Never removes a
line. Reports counts per state. Works on a section, a card, an analog page or
a brief.

## Acceptance

- [ ] Plugin validation green.
- [ ] On a landscape section with one line altered to a fake title, the fake line gains the `not found` tag with the indexes checked, every other line keeps its tag, and no line is removed.
- [ ] On a card, the same holds and `check_cards` stays green.
- [ ] A candidate line stays a candidate on a second run; nothing promotes it.
- [ ] The run report gives counts per state.
