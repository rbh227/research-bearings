---
name: landscape
description: Map the literature around a framed research question — derive the seven landscape questions from QUESTION.md and surveys.md, show the seven queries, fan out seven searcher agents in parallel over the citation indexes, then have a contract-bound merger lay their sections side by side as a formulation-by-data-regime matrix and a time slice. Use after /frame and ideally after /surveys, when you want to know what exists on your question in your own field. Writes research/landscape/matrix.md and timeslice.md.
allowed-tools: Read, Glob, Bash, Write, AskUserQuestion, Agent
---

# landscape

One job: the depth artifact. What your own field has done on your question,
laid out so an empty cell is visible and every filled one is checkable.
`/research-bearings:scout` does the other thing, the fields that never cite
yours.

Retrieval is one script, run by the searchers and by this skill for the cell
probes:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieval/snowball.py" <command> ...
```

## Preconditions

- **`research/QUESTION.md` must exist.** The seven questions are derived from
  it. If it does not: name the file, say `/research-bearings:frame` writes it,
  stop.
- **`research/landscape/surveys.md`** is read if it exists. Its taxonomy is the
  best source of formulations. Without it, say so and derive the axes from the
  sections alone.
- **`research/CONNECTIONS.md`** is read first. A source marked `not connected`
  is expected to fail and the sections will say so; that is stamped, not fixed.
  If the file is missing, run `... status --md` once and carry on.

## Steps

**1. Derive the seven questions.** From `## Question`, `## Today`, `## What's
new` and `## Vocabulary` in `QUESTION.md`, and `## Taxonomy diff` in
`surveys.md` when present. One query each, **in the home vocabulary** — this
is the one skill where your own words are right:

| # | Question | The query asks for |
|---|---|---|
| 1 | formulations | how the problem is posed: the task, the output, the unit of prediction |
| 2 | data regimes | the data conditions: labels, supervision, resolution, domain shift |
| 3 | methods | the method families applied to the problem |
| 4 | reproduction | benchmarks, baselines, comparisons, re-evaluations |
| 5 | abandoned | early approaches to the same problem, before the current family |
| 6 | adjacent | the same problem one field over, in that field's words |
| 7 | time slice | the problem in the last two years' vocabulary |

Question 5 is not retrieval-shaped: the record does not publish retractions of
interest. Its section will show what an early-vocabulary query returns, and
the merger's time slice does the rest. Say that in the query list.

**2. Show the seven queries** and the slug the files will carry, and ask. This
is the run's bound and its one human gate: seven walks at 30 seeds and 400
papers each is up to 2,800 papers. Strike, rewrite, or approve.

**3. Dispatch seven searchers, in parallel** — seven `Agent` calls in one
message, each `subagent_type: "research-bearings:searcher"`, each carrying:
the question, the field (the home field, named), the query, `mode: landscape`,
no blocked words, and the output path
`research/landscape/sections/<n>-<question>.md`. Nothing else: no reasoning,
no other section's path.

**4. Read the seven sections.** From their `## Foundational` and `## Current`
lines and `surveys.md`'s taxonomy, name the axes: three to six formulations,
three to five data regimes, each with the section or survey it came from. Show
them; do not wait.

**5. Probe every cell.** For each formulation × regime pair, one
`search "<formulation> <regime>" --limit 10`. Write
`research/landscape/sections/cells.md`: one `### <formulation> × <regime>`
block per pair, with `- Searched: \`<q>\` → <N> rows` and one line per row as
`- <title> · <year> · <venue> · S2 \`<id>\` · verified` (or the OpenAlex id).
This is an eighth section, written by the script's output, so that the merger
can name the query behind every empty cell without ever running one.

**6. Dispatch the merger**, once, `subagent_type: "research-bearings:merger"`,
with the sections directory, the axes with their provenance, and the two output
paths. Nothing else.

**7. Check and report.** Run
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_landscape.py" research/landscape`.
Then say: cells filled / empty / total, contradictions, sections that reported
a degraded index, and what to run next (`/research-bearings:scout` for the
fields that never cite yours; `/read` when it exists, for the cells that
matter).

## Outputs

`research/landscape/sections/1-formulations.md` … `7-time-slice.md` and
`cells.md`, written by the searchers and step 5. `research/landscape/matrix.md`
(`## Axes` · `## Matrix` · `## Cells` · `## Contradictions` · `## Sources` ·
`## Status`) and `research/landscape/timeslice.md` (`## Periods` ·
`## Per section` · `## Surveys by year` · `## Status`), written by the merger.

## Stop condition

Seven sections exist with six headings each; `cells.md` covers every axis
pair; `matrix.md` and `timeslice.md` exist; `check_landscape.py` passes; the
counts have been said out loud.

## Rules this skill applies

**Snowball from seeds and stop at the asymptote.** — Ré, Wohlin;
`academic.md` § Reading and mapping a literature. **The merger cannot add a
claim.** — ARS; § Skill and agent design patterns. **Absence is mechanical:**
an empty cell is a query and a count. — § Keeping agents honest.
**Contradictions are idea seeds, not noise to resolve.** — Kuhn; § Ideation.

## Refusals

| The shortcut | Why you don't |
|---|---|
| "No QUESTION.md, but they told me the topic." | Then it is `/scout`, unframed. This skill derives seven questions from a framed one. |
| "Seven searchers is a lot; I'll run three." | Seven is the contract, and the matrix has seven sources. Strike questions at the gate with the user, not silently. |
| "I'll pass the searchers each other's paths so they don't overlap." | Overlap is information: the merger reads it as agreement. Each searcher sees its own question only. |
| "I'll fill the obvious empty cells from what I know." | An empty cell is a query and a count. Filling it from memory is the fabrication this plugin exists to catch. |
| "The merger's matrix looks thin, I'll add a few rows." | The skill does not edit what the merger wrote. Rerun with different queries. |
