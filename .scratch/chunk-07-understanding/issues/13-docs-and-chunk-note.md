# 13: Docs, manifest, chunk note

Type: task
Status: done
Blocked by: 01 through 12

## What to build

The README's skill list and any diagram text that names the skills; the
skills-and-agents design doc's Stage 3 table and agent counts; the plugin
manifest version bump; the build plan's Milestone 3 status line; and the chunk
note in the shape of chunks 3 to 6: decision record, what ships (one row per
piece), done-check (static only; the live test is deferred to the acceptance
run and said so). The chunk note's decision record carries the two departures
from the grilling recorded in the spec's further notes.

## Acceptance

- [x] Every new skill and agent appears in the README and the design doc table.
- [x] The chunk note exists with the three sections and names every ticket's piece in the ships table.
- [x] All static checks green in one pass: both script selftests, guard selftest, heading parity, `check_cards`, `check_landscape`, `check_analogs`, plugin validation.
- [x] The build plan's Milestone 3 status reads built, static-checked, live test pending.

## Resolution

2026-09-16. `docs/design/chunk-07-understanding.md`, README, the Stage 3 table
in `docs/design/skills-and-agents.md`, `docs/APIS.md` (nine sources),
`CONTEXT.md` (eleven reading terms), the build plan's Milestone 3 status, and
the manifest at 0.7.0.

Full static suite green in one pass: 45 walker cases, 27 reading cases, the
guard selftest including eight new agents and a frontmatter check, heading
parity over fourteen templates, `check_cards` (13 cases and 3 real cards),
`check_analogs`, `check_landscape`, and plugin validation.

The chunk note carries a §5 "What is not done", which is the part a reader
needs most: no evals for any of the eight skills, the milestone's live test
left to the acceptance run, `/reviews` never having read an actual review, and
`--place` unable to fill a same-cell comparison.
