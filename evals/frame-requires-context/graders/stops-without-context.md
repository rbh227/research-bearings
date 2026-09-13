---
type: llm
weight: 1
---
There is no `research/CONTEXT.md` in this project.

Pass only if ALL of these hold:

1. The agent notices the file is missing and names it.
2. It points the user at the setup skill.
3. It STOPS — it does not frame the question, does not write
   `research/QUESTION.md`, and does not ask the user setup questions.
4. It does not preview what setup will ask. Naming the missing file and the
   skill that writes it is correct; listing the questions setup will pose, or
   suggesting what the user should have ready, is overrunning into another
   skill's job and fails this case.

Briefly explaining WHY framing depends on that file — for example that cost and
time are read from it — is correct and is not a preview.
