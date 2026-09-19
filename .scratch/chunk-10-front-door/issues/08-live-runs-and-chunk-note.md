# 08: Two live runs, and the chunk note

Type: task
Status: done
Blocked by: 06, 07

## What to build

The first contact with real files, and the record of it.

**Assemble the folder.** Run the scaffold from ticket 02 to build a project
folder from the damage fixtures, outside the repo's own `research/`.

**Run `/router` there.** Record what the brief said, which moves it offered,
which preconditions it named, and whether the fork it offered matches what
the state script printed for the same folder.

**Run `/think` there to its first pause.** It should ask about the existing
bits file with the count of cards newer than it and the newest card's date.
Record the question verbatim and whether the count was right. Answer stop.
Nothing beyond the first pause runs.

**The chunk note**, in the shape of the chunk 9 note: what was decided and
why, what the live runs said, what the first contact corrected, and what is
open. Say plainly that the eval cases are written and unrun, that the guard is
final and why, and whether the README's loop table, the design doc's stage
tables and the state script's dependency table agreed on first contact.

## Acceptance

- [x] The router's brief and offered moves are recorded beside the state script's output for the same folder, and any disagreement is named.
- [x] `/think`'s first question is recorded verbatim with whether its staleness count was right, and nothing past the first pause ran.
- [x] Anything the runs corrected is fixed in the skill or the script, with the selftest extended where the script changed.
- [x] The chunk note exists with the four sections and closes the hooks line.
- [x] Every ticket in this chunk is closed with its resolution and SHA.

## Resolution

2026-09-18. Two live runs on the assembled damage folder, recorded in
`docs/design/chunk-10-front-door.md` § 3; the note written with its four
sections; the hooks line closed in § 1.

**`/router`** offered bits (stale), read (repeat), brainstorm (ready) — in
agreement with the state script — and hid `scout` and `baseline`, ready at
other stages. Fixed: the brief carries an **Also open** line with every
recommended move the offer did not.

**`/think`** asked, first thing, rerun/keep/stop on `BITS.md` with the file's
date and two cards newer than it. The count was right and misleading: the file
names all three cards. Fixed in the state script: `not_named` beside the date
count, in the shared rules, `/think` and the router's brief, with the selftest
case where the two disagree (33 cases after the review pass). Answer given: stop. Nothing past the
first pause ran.

**Emulated, as chunks 5 and 7 were.** The skills were followed as written
from the repo, not invoked from an installed plugin; the note's § 4 says the
Skill-tool call between plugin skills is the untested mechanism.
