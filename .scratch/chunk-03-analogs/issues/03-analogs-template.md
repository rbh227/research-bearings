# The analogs template and its heading-parity registration

Type: task
Status: ready-for-agent
Blocked by:

## What

`templates/research/analogs.md` with the five fixed headings and the fixed
per-field block from spec §5, as HTML-comment guidance in the template like
the others. Register it in `scripts/check_headings.py` against
`skills/scout/SKILL.md` — which does not exist until ticket 04, so this ticket
lands the template and the registration line, and parity goes green when 04
lands. If `check_headings.py` cannot express "template exists, skill pending",
make the registration part of 04's acceptance instead and say so here.

## Acceptance

- [ ] Template file with `## Question` · `## Shape` · `## Fields` ·
      `## Verification` · `## Status`, and the per-field block verbatim from
      the spec in a comment under `## Fields`.
- [ ] `/setup` does not need to know about it (it is written by `/scout`, not
      scaffolded) — confirm and note.
- [ ] Registration in `check_headings.py`, or the deferral recorded.
