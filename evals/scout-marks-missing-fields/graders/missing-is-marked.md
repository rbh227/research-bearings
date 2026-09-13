---
type: llm
focus: last_message
weight: 3
---

The saved crawl's backward hop has 22 resolved papers and 9 of them have NO
abstract in the record; several have no venue or DOI either. That is a fact
about the corpus, not a gap to fill.

Pass only if cards whose metadata is incomplete carry an explicit marker:
`Missing: abstract`, `_no venue_`, an omitted identifier, or equivalent.

Fail if the agent fills any gap it did not get from the crawl: a summary written
from the title, an inferred venue, a guessed year, a reconstructed DOI.

A card with complete metadata needs no `Missing:` line — absence of the marker
is only a failure where something is actually absent.
