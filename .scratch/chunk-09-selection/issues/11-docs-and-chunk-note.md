# 11: the docs and the chunk note

Type: task
Status: ready-for-agent
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

- [ ] Every count in the README matches the files on disk.
- [ ] Every skill and agent this chunk added appears in the design doc's Stage 5–6 tables with a built mark.
- [ ] The build plan no longer promises an agent running the user's code, and says why.
- [ ] `/brief` appears nowhere as planned work.
- [ ] The chunk note records the decisions settled at planning and anything the build changed.
- [ ] Every checker and selftest in the repo is green.
