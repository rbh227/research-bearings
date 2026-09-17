# 06: `diversity-planner`

Type: task
Status: done
Blocked by: 03

## What to build

`agents/diversity-planner.md`, same shape as the other agents. Tools: **Read,
Write only.** No Bash, no web tools.

Receives: the candidate set with each candidate's seed and `Nearest existing`
line, the fields already searched (the analog pages and the landscape
sections), and the home vocabulary. Writes `research/ideas/diversity-<date>.md`
from `templates/research/diversity.md`.

Contract: says what the set has in common before proposing anything — the
honest reading of why it is self-similar; proposes three to six fields, ranked,
each with a query in that field's words and the blocked home vocabulary beside
it; **names fields and does not generate ideas**, because a planner that also
proposed the ideas would be planning toward its own answer; a field that shares
the home citation graph is not a field, the same test `/scout` applies.

## Acceptance

- [x] The agent file names every heading of `templates/research/diversity.md`.
- [x] Frontmatter grants exactly Read and Write.
- [x] Refusals table covers at least: proposing ideas, proposing the home field with a wider collar, using a blocked word in a query, and ranking the candidates.
- [x] Plugin validation green.

## Resolution

2026-09-16. `agents/diversity-planner.md`, 101 lines, Read and
Write only.

Heading parity green. The contract puts the commonality before the proposal —
the planner says what the set shares, naming the tight axis, before it names a
field — and states in three separate places that it does not generate ideas,
because that is the one failure that would make the retrieval round
confirmation.
