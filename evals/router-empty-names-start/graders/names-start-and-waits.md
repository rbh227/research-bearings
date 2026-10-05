---
type: llm
weight: 2
---
The workspace has no `research/` folder. The state script reports the empty
state, and its `recommended` list is exactly `["start", "find"]`.

Pass only if ALL hold:

1. The reply says there is no `research/` folder (or nothing under it) and
   offers the two doors: `/start` (talk an idea through, then frame it) and `/find` (a topic or task the user already has).
2. It asks whether to run it, or ends at the question. It does not begin
   `/start`'s conversation and asks nothing about the user's lab, compute,
   data or deadline.
3. It does not describe what `/start` will ask. Naming the file it writes
   (`research/CONTEXT.md`) is fine.
