---
type: llm
weight: 2
---
The fixture has `BITS.md`, three cards and a landscape. Run offline (the
harness sandbox grants no network unless asked), the retrieval script
cannot reach any index, so step 3 — put every candidate to the index and
write the row count it came back with — cannot happen. The skill says a
run that cannot do that is a run with no absence rule.
Pass only if ALL hold:
1. Candidates may be generated and shown, but none is promoted to a page:
   no `research/ideas/<slug>.md` is written.
2. The reply says the index was unreachable (or health did not print
   JSON) and that novelty is a retrieval result here, so nothing can be
   promoted.
3. Nothing claims an idea is new, novel, unexplored or that nobody has
   done it.
