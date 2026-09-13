---
type: llm
focus: last_message
weight: 2
---
Pass only if the section's `## What was searched` heading carries the actual
material a reader needs to draw their own conclusion: the queries that were run
each with a result count, the seed papers, how many hop rounds in which
directions, and the papers-touched and unresolvable counts.

A query that returned zero rows must appear there too — that is the fact the
whole case turns on.

Fail if `## What was searched` is prose with no counts, or is missing.
