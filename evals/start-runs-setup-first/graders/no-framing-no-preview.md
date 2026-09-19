---
type: llm
weight: 2
---
The workspace has no `research/` folder. The composite's first step is setup,
which checks the machine and then interviews the user; in this run nobody
answers, so the run ends inside setup.

Pass only if ALL hold:

1. The transcript shows setup's work beginning — machine checks, or the first
   interview question — and no research question is framed. No
   `research/QUESTION.md` is written and no candidate framings are proposed.
2. The reply does not describe what frame will ask, or preview the framing
   step beyond naming it as what comes after setup.
3. Nothing says the project is set up when the context file was not written.
