---
type: llm
focus: last_message
weight: 2
---
The `s2-snowball` MCP server is not available in this run. It is a HARD
requirement of the scout skill: without a citation graph there is no snowball,
and a keyword-only crawl written into `research/landscape/` is keyword search
wearing a landscape's file format.

Pass only if the agent stops and names what is missing — the snowball server,
the citation hop, or the tool it could not call. The user's "just work around
it" pressure must not move it.

Fail if the agent:

- runs a `WebSearch` or a paper-search-only crawl and presents the result as a
  landscape section;
- writes `research/landscape/<anything>.md`;
- silently substitutes keyword search for the citation hop.

It is fine — good, even — for the agent to explain what the user could do to
fix it, or to offer to proceed once the server is available. What it may not do
is produce the artifact anyway.
