# 04: `/orient` — surveys, landscape, and the brief at the end

Type: task
Status: ready-for-agent
Blocked by: 03

## What to build

The gathering composite. `/surveys` then `/landscape`, under the shared rules
from ticket 03, quoted not restated. Ends with the router's brief, which for
this composite must carry: surveys found, matrix cells filled, cells whose
query came back empty, the three papers the matrix ranked highest, and the
next move, which is `/read` when the matrix has lines nobody has read.

Writes no file of its own. The brief is printed.

**One case**: `/orient` on the wildfire shape with its landscape removed and
its surveys present asks rerun/keep/stop about the existing surveys file with
the staleness fact, and does not begin the landscape before an answer.

## Acceptance

- [ ] The skill validates, is under 150 lines, quotes the shared rules by name and adds only its sequence and its brief.
- [ ] The brief's five items are named and each is derivable from the state script's output or the landscape files, never from memory.
- [ ] No file under `research/` is written by the composite; the headings check passes with a skill that names no template.
- [ ] The case exists and the harness lists it. Not run.
