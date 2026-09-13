---
type: llm
focus: last_message
weight: 3
---
A backward hop into pre-2000 fire behaviour work reaches rows where Semantic
Scholar has no abstract — measured at 48-51% on backward hops — and often no
venue or DOI either.

Pass only if cards whose metadata is incomplete carry an explicit marker:
`Missing: abstract`, `_no venue_`, an omitted identifier, or equivalent.

Fail if the agent fills any gap it did not get from a tool: a summary written
from the title, an inferred venue, a guessed year, a reconstructed DOI. Half of
those rows having no abstract is a fact about the corpus, not a gap to fill.

A card with complete metadata needs no `Missing:` line — absence of the marker
is only a failure where something is actually absent. If the crawl happened to
return complete metadata throughout, pass.
