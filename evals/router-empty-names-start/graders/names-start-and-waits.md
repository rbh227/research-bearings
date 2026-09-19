---
type: llm
weight: 2
---
The workspace has no `research/` folder. The state script reports the empty
state, and its `recommended` list is exactly `["setup"]`.

Pass only if ALL hold:

1. The reply says there is no `research/` folder (or nothing under it) and
   names `/start` — or `/setup` — as the move. Naming both, with `/start`
   described as setup then frame, is correct.
2. It asks whether to run it, or ends at the question. It does not begin the
   setup interview and does not ask the user any setup question (lab,
   compute, data, deadline).
3. It does not describe what setup will ask. Naming the file setup writes
   (`research/CONTEXT.md`) is fine; listing setup's questions fails.
