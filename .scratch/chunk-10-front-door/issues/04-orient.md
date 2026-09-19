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

## Resolution

2026-09-18. `skills/orient/SKILL.md` (78 lines), quoting `/start`'s shared
rules by name and adding its sequence and its five-line brief;
`evals/orient-asks-about-existing-surveys` on a new fixture shape,
`wildfire-surveyed` (question and surveys only). Validator, heading parity and
the harness's case parse green.

**The brief's five items each name their source.** Surveys found is the count
of paper lines under `## Surveys`; cells filled is `## Cells` against
`## Axes`; empty cells are the ones carrying only a query-and-count line, said
as what the search returned; the three papers are in `/read`'s own proposal
order minus those already carded; next is the state read. Nothing in the brief
comes from memory, and nothing is saved.

**The case is not the one the ticket named, and this was not said at the
time** — the review caught the omission. The ticket asked for a pause after
surveys on a framed project; that needs the harness to answer the yes at the
boundary, which it cannot. The case grades the reachable half of the same
rule: on a folder where the surveys file exists, the composite asks rerun, keep
or stop with the date before the landscape step begins, and nothing runs.

**The `case.yaml` name carried its directory prefix** and the harness dropped
the case silently. Fixed; the parse counts it.
