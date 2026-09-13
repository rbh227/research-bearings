# Shared contracts

Type: grilling
Status: resolved
Blocked by: 01, 06

## Question

What schemas and project folder template do the chosen skills share? Fields per schema, on-disk format, fixed headings, and how the one deterministic validation check works.

## Resolution

Chunk 1 fixes three schemas and no more; the rest are written with their first consumer.

Output root is `research/` — one directory, one guard rule, no collision with the Pocock-convention root `CONTEXT.md`.

- `research/CONTEXT.md`: nine fixed headings (Project, People, Compute, Storage and data, Code, Calibration, Constraints, What counts as a win, History). Local facts verified via Bash; every user-reported number carries the date it was reported; every section carries content or an explicit `_unknown_`.
- `research/QUESTION.md`: eleven fixed headings, the deliverable only. Booth's sentence, the ladder, who decides, the Heilmeier fields, why you, vocabulary, status.
- `research/framing-log.md`: the working record. Rejected framings with cause of death, critique with concession scores, dated revisions.

Deliverable and working record are separate files so `QUESTION.md` stays short and quotable and downstream skills read only it.

Methodology rules are **inlined per skill** rather than referenced from a shared file: a skill's rules are the skill, a reference file needs a `Read` the model can decline, and per-skill anti-rationalization tables are more accurate than a generic one. `academic.md` stays a repo document, not shipped.

The one deterministic check is `hooks/guard.py --selftest`, seven cases over the write-scope guard's stdin contract.

Spec: `docs/design/chunk-01-question-stage.md` §4-5.
