# 03: the persona and diversity templates

Type: task
Status: done
Blocked by: —

## What to build

Two more templates under `templates/research/`, same comment-only style.

`persona.md` → `research/ideas/personas/<slug>.md`, written by
`persona-ideator`. Headings: `## Who` (the persona and the warrant — which file
it was drawn from), `## What they want from this work`, `## Questions` (five to
ten, each grounded in a file the agent was given, or marked `from the role, not
the record`), `## What would count as failure`, `## What they think is
missing` — the one heading where the persona may propose, and the comment says
what it writes there is labelled as its own guess.

`diversity.md` → `research/ideas/diversity-<date>.md`, written by
`diversity-planner`. Headings: `## What this set has in common` (the honest
reading of why the candidates are self-similar), `## Fields not drawn on`,
`## Proposed searches` (three to six, ranked, each with the field, a query in
that field's words, the blocked home vocabulary beside it, and one line on what
the field would contribute that the set lacks), `## Status`.

## Acceptance

- [x] Both templates exist with exactly those headings, in order.
- [x] The persona template's comments say questions not proposals, and name the one heading that is the exception.
- [x] The diversity template's comments say the planner names fields and does not generate ideas.
- [x] Headings parity green once ticket 08 registers them.

## Resolution

2026-09-16. `templates/research/persona.md`,
`templates/research/diversity.md`. Five headings and four, comment-only,
registered in ticket 08.

The persona template's comments carry the one rule that matters: a persona's
identity is its warrant and nothing else, and `## What they think is missing` is
the only heading where it may propose.
