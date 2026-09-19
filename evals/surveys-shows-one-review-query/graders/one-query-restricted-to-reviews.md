---
type: llm
weight: 2
---
The fixture has `research/QUESTION.md` with `## Question` and
`## Vocabulary` filled, and nothing else. The skill builds ONE query from
those two sections, restricted to surveys and reviews, shows it, and does
not wait before dispatching one searcher.
Pass only if ALL hold:
1. Exactly one query is shown, built from the question's own words or its
   vocabulary section, and it is visibly restricted to reviews/surveys
   (a review filter, or "survey"/"review" in the query).
2. The reply does not ask the user to approve the query before going on —
   this skill has no gate there.
3. At most one searcher is dispatched (a network failure inside it, in an
   offline run, is reported and is not a failure of this case).
