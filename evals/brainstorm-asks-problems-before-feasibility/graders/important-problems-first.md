---
type: llm
weight: 2
---
The fixture has `research/QUESTION.md`. The skill's first bank asks the
user what the important problems are — Hamming's question — before
anything about feasibility, and only later pushes the problem through
Polya's transformations and spawns personas.
Pass only if ALL hold:
1. The first thing asked of the user is about the important problems in
   the area, or what they would work on if resources did not matter.
2. Nothing about feasibility, cost, compute or "can we do this" is asked
   first.
3. No persona agent is dispatched before the user answers.
4. Nothing is ranked and no idea page is written.
