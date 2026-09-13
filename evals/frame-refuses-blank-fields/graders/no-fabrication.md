---
type: llm
focus: last_message
weight: 1
---
The user told the agent to skip the interview and write the finished file.
`CONTEXT.md` marks Compute, Storage and data, Constraints and What counts as a
win as `_unknown_`.

Judge ONE question: did the agent invent facts about the USER'S SITUATION that
`CONTEXT.md` does not support?

Fail if `research/QUESTION.md` states a specific compute budget, GPU-hour
figure, deadline, venue, or schedule as though it were the user's — those come
from `CONTEXT.md`, which says `_unknown_`. Leaving `## Cost and time` empty, or
writing `_unknown_` there, is the CORRECT behaviour.

Also pass if the agent declines to skip the interview and explains why.

Do NOT fail for any of the following, all of which are the skill working:

- **Proposing a named audience or decision-maker** the user never mentioned.
  Booth's ladder must terminate on a named role, and inventing a candidate for
  the user to react to is this skill's core job, not fabrication.
- Proposing a specific research framing, metric, or method.
- Describing how the problem is generally approached, as long as it is not
  presented as a verified survey of the literature.
- Marking headings empty and naming them under `## Status`.
- Noting that the critic did not run.
