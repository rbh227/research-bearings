---
type: llm
weight: 2
---
The fixture is the wildfire shape: `QUESTION.md` and a full `landscape/`
(surveys, matrix, timeslice), no `CONTEXT.md`, no cards. For this folder
`python3 scripts/state.py` reports `stage_reached: gathering`, `scout` as
the only non-done move at that stage (status `ready`), `read` as the first
`ready` move of the next stage with the precondition "landscape/matrix.md
must exist", and one repair: `CONTEXT.md`, `missing upstream`.

Pass only if ALL hold:

1. The reply prints a brief that names the stage reached (gathering) and the
   files that exist, with the matrix among them.
2. It offers `/scout` and `/read` as the moves — both, as a choice — and no
   more than three options in total. `/read`'s line names the matrix as what
   makes it possible.
3. It does NOT recommend `/setup` as the next move. Mentioning that
   `CONTEXT.md` is missing, as a repair, is correct; sending the user back to
   setup fails.
4. It asks the user to choose, or ends at the question, and runs nothing.
