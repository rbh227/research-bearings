# 11: the docs and the chunk note

Type: task
Status: done
Blocked by: 10

## What to build

- **`CONTEXT.md`**: a selection-and-experiments section — pre-mortem, the three
  verdicts, pairing, cheapest kill, the Alon quadrant, Heilmeier page, baseline,
  reproduction status, pre-registration, competing hypotheses, stop rule,
  variance plan, notebook entry, run directory, config hash, the M1–M7 audit,
  contested. One meaning each, in the voice of the existing sections.
- **`README.md`**: the eight skills move from planned to built, one sentence
  each in the voice of the existing entries. `/brief` leaves the planned list,
  with `/spec` named as the Heilmeier page. The built and planned counts near
  the top are corrected.
- **`docs/design/skills-and-agents.md`** §§ Stage 5–6: the built marks and this
  chunk's decisions, including the guard's departure from the plan.
- **`research_plugin_build_plan.md`**: Milestone 5's status rewritten, and the
  Milestone 2 line that promised `/brief` amended to point at `/spec`.
- **Manifest** to `0.9.0`.
- **`docs/design/chunk-09-selection.md`**, last, in the shape of the earlier
  chunk notes: the decision record, what was found in review, and what was left
  open.

## Acceptance

- [x] Every count in the README matches the files on disk.
- [x] Every skill and agent this chunk added appears in the design doc's Stage 5–6 tables with a built mark.
- [x] The build plan no longer promises an agent running the user's code, and says why.
- [x] `/brief` appears nowhere as planned work.
- [x] The chunk note records the decisions settled at planning and anything the build changed.
- [x] Every checker and selftest in the repo is green.

## Resolution

2026-09-18. `CONTEXT.md`, `README.md`, `docs/design/skills-and-agents.md`,
`research_plugin_build_plan.md`, manifest `0.9.0`,
`docs/design/chunk-09-selection.md`. Everything green.

**The counts on disk are 23 skills, 23 agents, 28 templates, 10 scripts**, and
the README and design doc now say so. Six skills remain planned: `/render`,
`/figure`, `/router`, `/start`, `/orient`, `/think`. **No agent remains
planned** — the design doc's agent list is complete for the first time.

**`/brief` is retired in four places, not one.** The build plan's Milestone 2
paragraph and its skill list, the design doc's Stage 2b table and its agent
count row, the `/orient` composite in both documents, and the cross-cutting
`/verify` row that named "the brief". A retirement recorded in one file and left
standing in three is how a plan starts lying.

**The build plan's own promise is corrected where it was made.** The Milestone 5
paragraph said the experiment agents get Bash on the user's code. That paragraph
now says they do not, and why — the guard refuses it and was right to. The
correction sits where the claim was, not in a separate ledger, which is this
repo's amendment rule.

**The glossary got 25 terms**, and the ones that carry a rule rather than a
definition are the point: `executable with changes` defined by nameability,
`inconclusive` defined by what it must name, `contested` defined by the attempt
list. Three states, named, in all three places.

**The chunk note records two things the build found that the spec did not
anticipate**: `ingest_runs.py` has no `best` field, because best needs a
direction the script cannot know and a `best` that meant `max` would put a
loss's worst value in a table; and the experiment-page classifier was wrong on
its first version, in the specific way that made the page most worth failing
loudly the one page it could not recognise.
