# `verify` verb on the retrieval script

Type: task
Status: ready-for-agent
Blocked by:

## What

`snowball.py verify [--title "<t>"]... [--id <S2|ARXIV:|DOI:>]...` — spec §4.
Titles resolve through `search` with the title as the query and a normalised
title comparison (case, punctuation, whitespace folded; stdlib only); ids
through `batch`. One JSON object: `results[]` of `{query, kind, resolved,
paperId, title, year, match}`, plus `resolved_count` and `unresolved_count`.
Does not charge the ledger. Writes records like any other call.

## Acceptance

- [ ] Selftest cases, offline, on captured responses: exact title; a
      punctuation-variant title that still resolves; a title that does not
      exist; a good id; a bad id; a mixed batch. Each asserts the `match`
      field says why.
- [ ] `--help` lists it; the docstring's command list includes it.
- [ ] `health` unchanged. `--selftest` count in the README and the chunk 2 spec
      updated to the new number.
- [ ] Static checks green.
