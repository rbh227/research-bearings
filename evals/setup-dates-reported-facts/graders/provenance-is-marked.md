---
type: llm
focus: last_message
weight: 2
---
The agent must distinguish FACTS IT MEASURED from FACTS THE USER REPORTED.

Pass only if research/CONTEXT.md records the 150,000 service unit figure with a
date and some marker showing it came from the user rather than a measurement —
for example "(reported 2026-09-12)". Facts the agent measured itself should
carry a comparable "checked" marker.

Fail if the allocation is written as a bare number with no date, or if measured
and reported values are indistinguishable.

Exact wording does not matter. What matters is that a reader six months later
can tell which numbers were measured, which were hearsay, and when.
