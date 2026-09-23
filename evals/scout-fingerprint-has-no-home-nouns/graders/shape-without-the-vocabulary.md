---
type: llm
weight: 2
---
The fixture's `research/QUESTION.md` is about wildfire detection and
spread from satellite and aerial imagery, and its `## Vocabulary` lists
the home field's words. The skill's first step writes the problem as its
structure with those nouns removed, then shows it.
Pass only if ALL hold:
1. A shape (fingerprint) is shown: the problem as structure — data shape,
   label regime, shift — without the words "wildfire", "fire", "burn",
   "satellite" or any term from the question's vocabulary section.
2. The blocked list (the home vocabulary) is shown beside the plan.
3. The reply waits for the user before any searcher runs.
