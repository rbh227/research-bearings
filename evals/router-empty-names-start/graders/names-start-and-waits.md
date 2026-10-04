---
type: llm
weight: 2
---
The workspace has no `research/` folder. The state script reports the empty
state, and its `recommended` list is exactly `["setup", "find"]`.

Pass only if ALL hold:

1. The reply says there is no `research/` folder (or nothing under it) and
   offers the two doors: `/start` (setup then frame, for an interest to
   sharpen) and `/find` (a topic or task the user already has).
2. It asks whether to run it, or ends at the question. It does not begin the
   setup interview and does not ask the user any setup question (lab,
   compute, data, deadline).
3. It does not describe what setup will ask. Naming the file setup writes
   (`research/CONTEXT.md`) is fine; listing setup's questions fails.
