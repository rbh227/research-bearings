# The `/scout` skill

Type: task
Status: ready-for-agent
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

- [ ] `claude plugin validate skills/ --strict` green; heading parity green
      for `analogs.md` → `skills/scout/SKILL.md`.
- [ ] A dry run on the acceptance topic with no `QUESTION.md` writes
      `research/analogs/<slug>.md` stamped *unframed*, with ≥5 fields, every
      paper line carrying an id or the unresolved marker, and a `Nearest
      existing` line under every opportunity.
- [ ] The confirm step was hit: the transcript shows shape and fields before
      the first search.
- [ ] Nothing in the file says unexplored, gap, novel, or nobody.
