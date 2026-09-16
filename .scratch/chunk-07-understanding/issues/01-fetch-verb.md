# 01: Second retrieval script and the `fetch` verb

Type: task
Status: done
Blocked by: None (can start immediately)

## What to build

A second retrieval script beside the walker, in the same directory so the
guard's Bash fence already admits it, that imports the walker's shared HTTP,
cache, pacing and record helpers rather than copying them. Its first verb is
`fetch`: given an arXiv id, DOI, Semantic Scholar id, OpenAlex id or exact
title, resolve the record through the existing resolvers, collect every PDF
location they return (S2 open-access PDF, OpenAlex locations, arXiv, Unpaywall
when the email is set), try them in that order, download, extract text, split,
and write three files under the fetch cache: intro text, full text, and a
metadata record (source URL, page count, character count, split method, date).
Print JSON naming the three paths and every state.

Extraction: `pdftotext` on the path first, then the `pypdf` module if it
imports, else the state `no extractor` with both install hints. Split: the
first top-level section heading after the introduction (related work,
background, preliminaries, method, approach, and their numbered forms); if none
within the first quarter of the text, cut after the second page and record
`split: page-cut`. Title, abstract and introduction always go in the intro
file; nothing else does. No open-access location is the state `no text`, with
what was checked. Cache per resolver, 30 days, cache-root override honoured.
Standard library only, apart from the extractor.

## Acceptance

- [x] `fetch` on a real arXiv id writes intro, full and metadata files and prints their paths; a second call is served from the cache.
- [x] Offline selftest cases, against saved fixtures, for: a two-column PDF text with a numbered related-work heading (heading split); a text with no heading (page cut, recorded); a record with no PDF location (`no text`, checked sources named); no extractor available (`no extractor`, hints named). Cases assert the JSON shape and state names only.
- [x] The walker's own selftest still passes; `health` and `status` are unchanged.
- [x] The guard selftest still passes: an agent running the new script by its full path is allowed.

## Resolution

2026-09-16. `scripts/retrieval/papers.py`, importing the walker's transport.
Live on arXiv 2105.15203 (SegFormer): 19 pages, 78,027 characters, split at
`2   Related Work`, intro 12,731 characters ending at the end of section 1;
the second call came from the cache. Nine offline cases green.

Three things the build changed from the ticket, each measured:

- **The split window is 40 per cent, not a quarter.** A real paper's
  "2. Related Work" lands near 28 per cent of the *extracted* text, because
  the references and the running headers extract too. A ceiling of 30,000
  characters is the other half of the rule, so 40 per cent of a very long
  extraction is still not believed as an introduction.
- **A short text with no form feeds is cut in half, never handed over whole.**
  `min(9000, len)` returned the entire document for anything under nine
  thousand characters, which is the one outcome the protocol cannot survive.
- **The single-paper S2 lookup asks for fields.** Without them the endpoint
  answers with an id and a title, and a paper with a PDF looks like a paper
  with none. The id the caller passed is also stamped back onto the record,
  because an index that answers a lookup by arXiv id and then omits it from
  `externalIds` is common.

Also: one download retry per location, after an arXiv PDF that curl pulls in
two seconds timed out once at sixty.
