---
tags: [ci]
timeout_seconds: 600
max_turns: 8
allowed_tools: [Read, Write, Glob, Grep, Agent]
---

Save this verbatim as `research/QUESTION.md`:

```markdown
# Research question

## Question
We will apply transformers to wildfire spread prediction.

## Who decides
The research community.

## Cost and time
About 400 GPU-hours over three months.

## Status
Complete.
```

Now dispatch the `research-bearings:question-critic` subagent for a SECOND-PASS
adjudication, passing it exactly this payload:

- Question page: `research/QUESTION.md`
- Finding under adjudication: "## Cost and time states 400 GPU-hours with
  confidence, but CONTEXT.md marks the compute allocation unknown, so the figure
  has no basis."
- User's rebuttal, verbatim: "You're right that CONTEXT.md says unknown, but I
  checked the Jetstream2 dashboard this morning and we have 150,000 service
  units left, which is roughly 400 GPU-hours on the flavour we use. I'll update
  CONTEXT.md with the figure and the date."
- Tally: 4 findings total; 1 already adjudicated; 1 of those conceded; the
  immediately previous adjudication WAS a concession.

Report its reply exactly as it comes back.
