---
type: llm
weight: 2
---
The fixture has a full landscape (`matrix.md`, `timeslice.md`) and no
cards under `research/papers/`. With no arguments the skill proposes up to
five unread papers from the matrix — densest cells first, then by the
centrality on the line — and waits.
Pass only if ALL hold:
1. Up to five papers are proposed, each with title, year, the matrix cell
   it sits in, and why it is on the list.
2. The reply says how many unread lines remain after this run.
3. It waits for the user's yes before fetching or dispatching anything.
4. No card is written.
