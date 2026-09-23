---
type: llm
weight: 2
---
This is a fresh project: `research/framing-log.md` did not exist before this run.

The agent must have created it from the plugin's template BEFORE appending
candidate framings to it, so that it carries all three of its required headings:
`## Rejected framings`, `## Critique`, and `## Revisions`.

Pass only if the file contents shown in the reply contain all three headings.

Fail if the file contains only the appended candidates with no heading structure,
or is missing any of the three headings. Those headings are what a later
re-entry reads to learn what has already been ruled out, so a log without them
is not recoverable.
