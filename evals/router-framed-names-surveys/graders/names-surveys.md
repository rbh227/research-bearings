---
type: llm
weight: 2
---
The fixture has `research/QUESTION.md` and nothing else — framed, no
landscape, and no `CONTEXT.md`. For this folder `python3 scripts/state.py`
reports `stage_reached: questions`, `setup` as `skipped` (a repair: the
context file is absent while the question exists), `frame` as `done`, and
`surveys` as the first `ready` move; `recommended` begins with surveys.

Pass only if ALL hold:

1. The brief names the stage (questions) and the question file.
2. The single next move named is `/surveys` (offering `/orient`, which runs
   surveys then landscape, alongside it is also correct), with the precondition
   it passed: the question file exists.
3. `/setup` is not the move. Naming the missing `CONTEXT.md` as a repair is
   correct; sending the user back to setup fails.
4. It asks once, or ends at the question, and runs nothing.
