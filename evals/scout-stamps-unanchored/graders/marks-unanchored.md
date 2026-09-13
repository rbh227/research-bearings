---
type: llm
focus: last_message
weight: 2
---
There is no `research/QUESTION.md` in this project, so the run is UNANCHORED:
it has no scope boundaries and no vocabulary from a question file.

Pass only if the section's `## Question` heading says so — "unanchored", "no
QUESTION.md", "run on the question as typed", or equivalent plain wording.

Fail if:

- the section presents itself as anchored, or says nothing about its mode;
- the agent interviewed the user for question-stage content (audience, so-what
  ladder, success criteria) before scouting. That is the `frame` skill's job,
  and a scout that frames its own question answers the question it preferred.

Asking the user to confirm the question wording, the budget, or the output slug
is CORRECT and must not fail this grader. The line is between confirming what
it was given and interviewing for what it was not.
