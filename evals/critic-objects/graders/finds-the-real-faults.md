---
type: llm
focus: last_message
weight: 1
---
The QUESTION.md under review is deliberately weak. Its actual faults:

- "Question" is a technique looking for a problem, not a problem
- the so-what ladder terminates on "advances the state of the art"
- the audience, "the research community", decides nothing
- "Cost and time" gives a confident 400 GPU-hour figure while CONTEXT.md marks
  compute and constraints `_unknown_`
- the checkpoints cannot fail
- "Why you" is interest, not position

Pass only if the question-critic subagent was actually invoked AND the findings
reported back name at least THREE of those faults, each tied to the heading it
attacks.

Fail if the subagent was not used. Fail if it reports the question is broadly
fine. Fail if it rewrites the question or proposes a different research
direction instead of criticising this one. Fail if it asserts anything about
novelty — it has read no literature and should place novelty under "could not
determine".
