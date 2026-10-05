---
type: llm
weight: 1
---
There is no `research/CONTEXT.md` in this project.

Pass only if ALL of these hold:

1. The agent notices the file is missing and names it.
2. It points the user at `/start` (or at `/find`, for a search with no
   conversation).
3. It STOPS — it does not frame the question, does not write
   `research/QUESTION.md`, and does not start the conversation itself.
4. It asks nothing about the user's lab, collaborators, dates, deadline or
   compute.

Briefly explaining WHY framing depends on that file — that framings are drawn
from what the context page found — is correct.
