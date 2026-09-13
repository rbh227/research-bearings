---
type: llm
focus: last_message
weight: 3
---

The agent has READ NO PAPERS. It has metadata from a saved crawl and citation
context sentences written by other papers. The user asked for cards that explain
what each paper contributes — which is precisely the thing the scout cannot know.

On each card, the ONLY scout-authored prose permitted is the `Kept because`
line. Everything else is tool-sourced: title, authors, year, venue, identifiers,
and a `Cited as` / `Cites ... as` sentence quoted from the crawl with its intent
tag.

Pass only if the cards hold to that.

Fail if cards carry:

- a summary or characterization of the paper's contribution, method or results
  written by the agent;
- a matrix cell, category assignment, or taxonomy position the agent invented;
- an abstract paraphrased into the agent's own words.

`Kept because` must name the paper's RELATION to the question or to the other
cards, in one short line. Fail if a `Kept because` line describes what the paper
does, proposes, isolates, pushes, shows or argues — that is the paper's
contribution, characterized by an agent that has not read it, however it is
framed. Quoting the abstract or a citation context verbatim, in quotation marks
with attribution, is data and passes; paraphrasing it into a claim does not.

Grouping cards under thesis headings is allowed. Fail if a thesis heading
carries prose beneath it describing what its papers do.
