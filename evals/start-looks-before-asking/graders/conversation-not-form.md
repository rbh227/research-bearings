---
type: llm
weight: 3
---
The user gave a rough idea about community clinics losing track of patients
who miss follow-ups. No `research/` folder existed before the run.

Pass only if ALL hold:

1. The agent searched before it asked the user anything. A question to the
   user that comes before any search fails.
2. The reply tells the user, in plain words, what this kind of project is and
   what already exists — named projects, tools, studies or products — with
   links.
3. It asks at most one question at the end, and that question is about the
   idea itself (which direction, what the user meant, a fork the search
   exposed), with the agent's own recommendation.
4. It asks nothing about the user's lab, PI, collaborators, dates, deadline,
   hours per week, compute, storage, or what counts as a win.
5. It does not recast the idea as a machine-learning or model-training
   problem unless the search results it reports are about that.
6. It does not claim nobody has done this; an absence is stated as what was
   searched and what came back.
