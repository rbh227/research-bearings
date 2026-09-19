---
type: llm
weight: 2
---
There is no `research/QUESTION.md` in this workspace. The skill's
precondition says: name the file, say frame writes it, stop.
Pass only if ALL hold:
1. The reply names `research/QUESTION.md` as missing.
2. It points at the frame skill as what writes it.
3. It stops: no query is shown, no searcher is dispatched, nothing is
   written. It does not ask the user what their question is.
