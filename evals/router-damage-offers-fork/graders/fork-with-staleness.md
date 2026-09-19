---
type: llm
weight: 2
---
The fixture is the damage shape: question, landscape, three cards under
`papers/`, `landscape/datasets.md`, `landscape/groups.md`, `BITS.md`, one
critique, no `CONTEXT.md`. The scaffold dates `BITS.md` (2026-09-16 11:30)
before two of the three cards. For this folder `python3 scripts/state.py`
reports `stage_reached: processing`; at that stage `bits` is `stale` with
`upstream_newer: 2` (and `not_named` empty: the file names all three cards),
`read` is `repeat`, `brainstorm` and `ideas` are `ready`; `datasets` and
`groups` are on-demand rows and never offered; the router's rule (stale
first, then loop order, cap three) yields bits, read, brainstorm. One repair:
`CONTEXT.md`, `missing upstream`.

Pass only if ALL hold:

1. The brief names the stage (processing), the three cards, and that
   `BITS.md` has two cards newer than it by date (the number two, or the two
   card names) while naming every card (zero not named) — both facts.
2. The reply offers a fork of at most three options that includes `/bits`
   and `/read`. `/bits` is described as stale or as having newer cards, not
   as missing.
3. It does not offer `/setup` as a move. Naming the missing `CONTEXT.md` as a
   repair is correct.
4. It does not offer `/verify`, `/audit`, `/critique`, `/reviews`,
   `/replicate`, `/datasets` or `/groups` — the on-demand skills are not the
   next move.
5. It asks the user to choose, or ends at the question, and runs nothing.
