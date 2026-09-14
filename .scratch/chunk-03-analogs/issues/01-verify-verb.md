# `verify` verb on the retrieval script

Type: task
Status: resolved
Blocked by:

## What

`snowball.py verify [--title "<t>"]... [--id <S2|ARXIV:|DOI:>]...` — spec §4.
Titles resolve through `search` with the title as the query and a normalised
title comparison (case, punctuation, whitespace folded; stdlib only); ids
through `batch`. One JSON object: `results[]` of `{query, kind, resolved,
paperId, title, year, match}`, plus `resolved_count` and `unresolved_count`.
Does not charge the ledger. Writes records like any other call.

## Acceptance

- [x] Selftest cases, offline, on captured responses: exact title; a
      punctuation-variant title that still resolves; a title that does not
      exist; a good id; a bad id; a mixed batch. Each asserts the `match`
      field says why.
- [x] `--help` lists it; the docstring's command list includes it.
- [x] `health` unchanged. `--selftest` count in the README and the chunk 2 spec
      updated to the new number.
- [x] Static checks green.

## Resolution

2026-09-14. `verify` ships with nine selftest cases, 19 to 28. Titles resolve
through `search` with case, punctuation and spacing folded; ids through `batch`.
Charges no ledger. On a miss the closest row comes back with it, so a typo reads
differently from a paper that is not there.

Case 26 exists because the first version crashed the moment it went through the
CLI rather than the function: `verify` has no `--run`/`--budget`, and the
dispatcher read `args.budget` before looking at the verb. The selftest now also
counts its own cases instead of printing a hardcoded total.
