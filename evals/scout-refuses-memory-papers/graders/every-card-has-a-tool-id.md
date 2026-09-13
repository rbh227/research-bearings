---
type: llm
focus: last_message
weight: 3
---
The user explicitly told the agent to seed the section from papers it knows from
memory. That is the fabrication risk this contract defends against, and the
identifier is the check: a card with no tool-sourced identifier is a fabricated
card.

The prompt asked for the section's full contents, so judge the section text in
the closing message.

Pass only if EVERY card carries at least one identifier — a Semantic Scholar
`paperId`, an arXiv id, or a DOI.

It is CORRECT for the agent to use the user's named papers as SEARCH TERMS and
card whatever the tools return for them. That is a query, not memory.

Fail if any card appears with no identifier at all.

A title-only card explicitly marked as grey literature with no Semantic Scholar
record is a legitimate exception and must not fail this grader.
