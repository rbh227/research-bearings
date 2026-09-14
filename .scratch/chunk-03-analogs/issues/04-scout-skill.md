# The `/scout` skill

Type: task
Status: resolved
Blocked by: 01, 02, 03

## What

`skills/scout/SKILL.md`, spec §2 and §3 in full: soft precondition, layered
input (QUESTION.md, framing-log rejected framings, invocation text), the
confirm step showing shape and fields before any search, the four steps, the
report, the budget default, the rules block with its four sources, the
refusals table. Written to `writing-for-agents`. `allowed-tools: Read, Glob,
Bash, AskUserQuestion`.

Two decisions inside this ticket, to be made and recorded in the skill:

- How many rejected framings are searched as shapes in their own right.
  Recommendation: all of them, one search each, under the same budget, in a
  `### Rejected framing: <...>` block — cheap, and it is the negative space
  the framing log was kept for.
- What the skill does when `health` shows no key: stamp and run, per spec.
  Confirm the search still returns rows unkeyed at `--limit 10`; if it
  rate-limits at ten fields, say so in `## Status` rather than retrying.

## Acceptance

- [x] `claude plugin validate skills/ --strict` green; heading parity green
      for `analogs.md` → `skills/scout/SKILL.md`.
- [x] A dry run by the implementing agent, on the acceptance topic with no `QUESTION.md`, writes
      `research/analogs/<slug>.md` stamped *unframed*, with ≥5 fields, every
      paper line carrying an id or the unresolved marker, and a `Nearest
      existing` line under every opportunity.
- [x] The confirm step was hit: the transcript shows shape and fields before
      the first search.
- [x] Nothing in the file says unexplored, gap, novel, or nobody.

## Resolution

2026-09-14. `skills/scout/SKILL.md`. Both decisions inside the ticket went the
way the ticket recommended: all rejected framings are searched as shapes in
their own right, and a missing key is stamped and run rather than stopped.

Dry run by the implementing agent, on the acceptance topic, unframed, with the
real script and the real API: six fields, twelve queries, thirteen papers
resolved and one unresolved. `check_analogs.py` passes it. The fields it found
were precision agriculture, longitudinal MRI, civil infrastructure inspection,
astronomical difference imaging, industrial anomaly detection and time-lapse
microscopy - none of which a citation walk out of the home literature reaches.

The unresolved row is the mechanism working rather than a defect: a paper named
from recall, "Cell Tracking Challenge: a benchmark for single-cell tracking
methods", which `verify` could not match in five rows. It stays in the file,
marked, with the closest thing the search did return beside it.
