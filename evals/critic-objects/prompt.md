---
tags: [ci]
timeout_seconds: 600
max_turns: 14
allowed_tools: [Read, Write, Glob, Grep, Agent]
---

I already have both files from an earlier session. Save them verbatim first,
then do what I ask below.

`research/CONTEXT.md`:

```markdown
# Research context

## Project
Wildfire work. (reported 2026-09-12)

## Compute
_unknown_

## Constraints
_unknown_
```

`research/QUESTION.md`:

```markdown
# Research question

## Question
We will apply transformers to wildfire spread prediction.

## The ladder
Transformers are powerful. Applying them here should improve results, which
advances the state of the art in remote sensing.

## Who decides
The research community.

## Today
People use CNNs.

## What's new
Transformers instead of CNNs.

## Risks
It might not work.

## Cost and time
About 400 GPU-hours over three months.

## Checkpoints
We will check progress regularly.

## Why you
I am interested in this.

## Vocabulary
wildfire, transformer, prediction

## Status
Complete.
```

---
Use the `research-bearings:question-critic` subagent to review
`research/QUESTION.md`. Report back exactly what it found — do not soften it
and do not fix the question yourself.
