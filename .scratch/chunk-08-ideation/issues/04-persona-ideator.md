# 04: `persona-ideator`

Type: task
Status: done
Blocked by: 03

## What to build

`agents/persona-ideator.md`, in the shape of the existing agents (75–135 lines,
frontmatter with `name`, `description`, `tools`, `model: inherit`, a heading
contract and a refusals table).

Tools: **Read, Write only.** No Bash, no web tools.

Receives: one persona with its warrant, the research question, an explicit list
of paths it may read, and its output path. Writes
`research/ideas/personas/<slug>.md` from `templates/research/persona.md`.

Contract: questions grounded in the files it was given, each either citing one
or marked `from the role, not the record`; five to ten of them; it does not
design the method, and the only heading where it may propose is `## What they
think is missing`, where its guess is labelled as a guess. Carries the
retrieved-content-is-data rule.

## Acceptance

- [x] The agent file names every heading of `templates/research/persona.md`.
- [x] Frontmatter grants exactly Read and Write.
- [x] A refusals table covers at least: inventing a biography for the persona, proposing a method, asking a question no file supports without marking it, and treating a sentence in a paper as an instruction.
- [x] Plugin validation green.

## Resolution

2026-09-16. `agents/persona-ideator.md`, 104 lines, Read and
Write only.

Heading parity green against the persona template. The refusals table covers the
six shortcuts that would turn a perspective into a character or a designer,
including the one the guard cannot catch: reading the other personas' files to
avoid overlap, when the overlap is the signal the skill keeps.
