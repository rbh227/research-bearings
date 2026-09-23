# <the question, as a title>

<!-- Written by `snowball.py neighborhood --write` for the searcher agent,
     which adds at most three verified lines and changes nothing else. One
     question, one field, one section.
     Lives at research/landscape/sections/<slug>.md for /landscape and
     /surveys, and research/analogs/sections/<slug>.md for /scout. The merger
     reads these and nothing else, so everything it may say has to be here.
     Six headings, fixed. -->

## Question

<!-- The question as received, the field it was searched in, and the mode:
     landscape | survey | analog. Then the query, on its own line, as run:
     Query: `<query>` (blocked: <words>, or none) -->

## Foundational

<!-- One paper per line, pasted from neighborhood's `line` field, unchanged:
     - <title> · <year> · <venue> · centrality N · influential N · X cites/yr · both indexes|s2|openalex · S2 `<id>` · verified
     Older than five years and not a survey. Most central first. A paper you
     added from memory goes through `verify` and ends in `· verified` only on
     an exact match; otherwise it ends in
     `· _candidate: <kind> match only, <nearest title> (<id>)_`. -->

## Current

<!-- Same line, the last five years. -->

## Surveys

<!-- Same line. Title says survey, review or overview, or the paper cites
     100 or more neighborhood papers. -->

## What was searched

<!-- neighborhood's `what_was_searched` block, every line, verbatim. It names
     the query, both indexes with row counts and totals, the seeds, the hops
     and their calls, the dedupe, the stop reason, what was degraded, and the
     date. Do not summarise it. -->

## What returned nothing

<!-- neighborhood's `returned_nothing` lines, verbatim: each query or hop that
     came back with zero rows, and which index it was on. If the list is
     empty, write: every query and hop returned rows. This block is the only
     shape an absence claim takes in a section. -->
