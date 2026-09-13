---
type: llm
focus: last_message
weight: 2
---

There is no `research/QUESTION.md` in this project, so the run is UNANCHORED:
it has no scope boundaries and no vocabulary from a question file.

Pass only if the section's `## Question` heading says so — "unanchored", "no
QUESTION.md", "run on the question as typed", or equivalent plain wording.

Fail if the section presents itself as anchored, or says nothing about its mode,
or if the agent interviewed the user for question-stage content (audience,
so-what ladder, success criteria) before writing.
