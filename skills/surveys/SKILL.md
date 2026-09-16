---
name: surveys
description: Find the surveys and reviews of a framed research question, extract each one's own taxonomy and open-challenges list, diff them, and harvest the field's vocabulary into QUESTION.md. One searcher restricted to surveys, then a survey-differ agent. Use after /frame and before /landscape, or whenever the question's vocabulary is still guesses. Writes research/landscape/surveys.md.
allowed-tools: Read, Glob, Bash, Agent
---

# surveys

One job: let the field's own reviewers tell you how the field is carved up,
before you carve it yourself. `/research-bearings:landscape` takes its axes
from what this writes.

## Preconditions

- **`research/QUESTION.md` must exist.** This skill appends to its
  `## Vocabulary`. If it does not: name the file, say `/research-bearings:frame`
  writes it, stop.
- **`research/CONNECTIONS.md`** is read first; missing, run
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieval/snowball.py" status --md`
  once and carry on.

## Steps

**1. One query**, from `## Question` and `## Vocabulary`, in the home
vocabulary, asking for the problem itself — not for "survey": the searcher's
`survey` mode restricts the seeds to reviews at the index (`publicationTypes=Review`
on Semantic Scholar, `type:review` on OpenAlex). Show it. Do not wait.

**2. Dispatch one searcher**, `subagent_type: "research-bearings:searcher"`,
with the question, the field, the query, `mode: survey`, no blocked words, and
the output path `research/landscape/sections/surveys.md`.

**3. Dispatch the differ**, `subagent_type: "research-bearings:survey-differ"`,
with the section path and the output path `research/landscape/surveys.md`.
Nothing else: it reads the section and the paper records, and it knows where
`QUESTION.md` is.

**4. Report.** Surveys found, surveys with abstracts, vocabulary lines
appended. Then say: run `/research-bearings:frame` again if the harvested
vocabulary changes the question, and `/research-bearings:landscape` when it
does not.

## Outputs

`research/landscape/sections/surveys.md` (the searcher's six headings) and
`research/landscape/surveys.md`: `## Surveys` · `## Taxonomy diff` ·
`## Open challenges across surveys` · `## Vocabulary harvested` ·
`## What was searched` · `## Status`. And an appended, dated block under
`## Vocabulary` in `research/QUESTION.md`.

## Stop condition

Both files exist; every survey block says what it was read from; the
vocabulary block in `QUESTION.md` carries the date; the counts have been said.

## Rules this skill applies

**Mapping studies before primary studies.** — Petersen; `academic.md`
§ Reading and mapping a literature. **Vocabulary harvest**: the question is
re-framed in the field's words, not yours. — same. **Abstention beats a
guess:** a survey whose record has no abstract is named, not summarised from
memory. — § Keeping agents honest.

## Refusals

| The shortcut | Why you don't |
|---|---|
| "I'll add 'survey' to the query." | The mode already restricts the seeds at the index. Adding the word finds papers *about* surveys. |
| "Only two surveys came back; I'll list the ones I know." | Two is the finding. The differ says a diff needs two, and `/landscape` runs either way. |
| "The differ should read the PDFs for a real taxonomy." | It reads records, by contract. Full text is `/read`'s, when it exists, and it says "abstract only" so nobody mistakes the one for the other. |
