# 05: The `/verify` skill

Type: task
Status: done
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

- [x] Plugin validation green.
- [x] On a landscape section with one line altered to a fake title, the fake line gains the `not found` tag with the indexes checked, every other line keeps its tag, and no line is removed.
- [x] On a card, the same holds and `check_cards` stays green.
- [x] A candidate line stays a candidate on a second run; nothing promotes it.
- [x] The run report gives counts per state.

## Resolution

2026-09-16. `skills/verify/SKILL.md`.

Verified on a real landscape section with one title replaced by
"Attention Is All You Need for Wildfire Damage Assessment". 71 paper lines
before and after; the faked line moved from `verified` to `_candidate:` with
the id it nearly matched; every other line kept its tag; nothing was removed.

One correction to the ticket's wording: that particular fake earns
**candidate**, not `not found`, because "Attention Is All You Need" is a real
prefix — which is the measured chunk-3 case this rule exists for. A title with
no near match ("A Completely Made Up Paper About Nothing At All Zzz") comes
back `none` across s2, openalex and crossref and is what becomes
`_not found: checked s2, openalex, crossref_`. Both states were exercised.
