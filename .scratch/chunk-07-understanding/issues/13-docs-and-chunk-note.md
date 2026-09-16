# 13: Docs, manifest, chunk note

Type: task
Status: ready-for-agent
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

- [ ] Every new skill and agent appears in the README and the design doc table.
- [ ] The chunk note exists with the three sections and names every ticket's piece in the ships table.
- [ ] All static checks green in one pass: both script selftests, guard selftest, heading parity, `check_cards`, `check_landscape`, `check_analogs`, plugin validation.
- [ ] The build plan's Milestone 3 status reads built, static-checked, live test pending.
