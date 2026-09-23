---
type: llm
weight: 2
---
The fixture is the wildfire shape: question and landscape, no cards, no
idea pages, no pre-mortems. For this folder `python3 scripts/state.py`
reports `rank` as `blocked` (missing: `premortems/`), `premortem` as
`blocked` (missing: `ideas/`), and `ideas` as `ready`.

Pass only if ALL hold:

1. The reply does not rank anything and does not run `/rank`.
2. It says why: there are no pre-mortems (and/or no idea pages) for `/rank`
   to read, and it names the command that writes them.
3. It walks back to a step that can run now — `/ideas` (or another `ready`
   move such as `/scout` or `/read` if it argues ideas need seeds) — and
   offers that.
4. It does not list what `/rank` or `/premortem` would ask or do beyond
   what they need. Naming the missing files and their writers is the whole
   message.
5. It asks once, or ends at the question, and invokes nothing.
