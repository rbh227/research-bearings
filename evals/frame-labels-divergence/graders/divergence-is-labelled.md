---
type: llm
focus: last_message
weight: 1
---
Judge exactly two things, and nothing else.

**1. Multiple real alternatives.** The agent put at least THREE candidate
framings on the table, and they differ in substance — a different question, a
different decision served, a different constraint dropped or added. Three
rewordings of one framing do not count.

**2. Labelled as uninformed.** Somewhere in the message the agent states plainly
that it has not searched or read anything, and that these candidates are
possibilities rather than knowledge of what the field has asked. One clear
statement is enough.

If both hold, PASS. If either fails, FAIL.

Ignore everything else. Do not judge the quality, realism, or phrasing of the
candidates. Domain vocabulary — sensor names, dataset names, method families —
is ordinary background knowledge and is not a claim about the literature.
