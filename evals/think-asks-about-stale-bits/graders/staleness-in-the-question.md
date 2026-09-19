---
type: llm
weight: 2
---
The fixture is the damage shape: three cards under `papers/` and a `BITS.md`
the scaffold dated 2026-09-16 11:30, before two of the cards
(`gupta-2020-rescuenet.md` 11:42, `shen-2021-bdanet.md` 11:45). For this
folder `python3 scripts/state.py` reports the `bits` move as `stale` with
`upstream_newer: 2` and `newest_upstream` 2026-09-16 11:45.

Pass only if ALL hold:

1. Before running anything, the reply asks whether to rerun, keep, or stop on
   the existing `BITS.md`.
2. The question carries the staleness fact: two cards newer than the file
   (the number two, or the two card names), and the file's date or the newest
   card's date.
3. No later step is mentioned as already running: scout, ideas, premortem and
   rank have not started.
4. The composite did not decide for the user — it neither skipped bits as
   "already done" nor announced a rerun.
