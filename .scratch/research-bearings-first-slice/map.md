# Map: research-bearings, first slice

Label: wayfinder:map

## Destination

A spec for the first buildable slice of research-bearings, ready for `/to-spec`: the skill and agent set chosen from `academic.md`, their contracts, the schemas they share, and the retrieval plumbing. Done when nothing is left to decide before someone scaffolds it.

## Notes

- **Domain**: a Claude Code plugin that runs the research loop with typed skills and contract-bound agents. Glossary in `CONTEXT.md`: **map** is this artifact only; **landscape** is the plugin's literature deliverable; an **acceptance run** is the user's post-handoff trial.
- **Inputs**: `academic.md` is "the big sheet", the source rules every skill derives from. `research_plugin_build_plan.md` is one candidate proposal for the loop and its milestones, not the plan.
- **Standing decisions** (from the build plan, reaffirmed 2026-09-12): Claude Code plugin; this repo is its own marketplace (`marketplace.json` with `source: "./"`, like the Matt-Raphs-Skills fork), retiring `raph-cc`; v1 is eventually the full loop including experiment agents; Claude-only with the judge's `model:` field left open for a second provider; Python for the few scripts; local paper cache is the reference manager; one spec covers schemas and their first consumers together.
- **Retrieval plumbing**: two MCP servers, `paper-search-mcp` (arXiv, Semantic Scholar, OpenAlex, Crossref, and more) and `openreview-mcp`. Both are 1.x-SDK servers and need `uvx --with 'mcp<2'`. A third server, `s2-snowball`, is the plugin's own single-file server for the references/citations/batch hop (ticket 10). OpenReview is registered at user scope on this machine; paper-search is ticket 04. Neither server exposes references or citations (ticket 02), so the snowball hop needs its own mechanism (ticket 10). A Semantic Scholar API key is effectively required.
- **Acceptance-run topic** (the user's real question, used for smoke runs, never a deliverable): post-disaster building damage assessment from aerial and satellite imagery, plus computer vision and AI in wildfires generally, including fire-spread prediction.
- **Skills to consult per session**: `grilling` and `domain-modeling` for every grilling ticket; `research` for research tickets; `prototype` for ticket 09. Plugin authoring follows `writing-for-agents`.
- **Repo**: https://github.com/rbh227/research-bearings. Tracker is local markdown under `.scratch/`.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->
- [Plugin manifest facts](issues/01-plugin-manifest-facts.md): default layout needs no component fields; agents are dispatched as `plugin:agent`; bundled MCP tools are `mcp__plugin_<plugin>_<server>__<tool>`; guards go in `hooks.json` keyed on `agent_type`, not agent frontmatter; fan-out skills must stay inline; Python scripts need a SessionStart install. Contradicts the build plan on the `mcp` field name and manifest listing.
- [Write-scope guard mechanics](issues/03-write-scope-guard-mechanics.md): a plugin `PreToolUse` hook on `Write|Edit` that reads `agent_type` from stdin and denies paths outside `landscape/`; exit 2 or a `permissionDecision: deny` JSON blocks; per-agent scoping only via that stdin field; drop `Bash` from landscape agents with `disallowedTools`; Python guard, not `jq`.
- [Retrieval tool inventory](issues/02-retrieval-tool-inventory.md): no references or citations tool in either MCP; seed search via `search_semantic`, hops must hit the Semantic Scholar Graph API directly; the S2 key is effectively required (429 after two or three unauthenticated calls); Unpaywall email mandatory; arXiv-only papers snowball via `ARXIV:<id>`; pass `use_scihub=False`.
- [Snowball mechanism](issues/10-snowball-mechanism.md): the plugin owns a single-file MCP server, `servers/s2_snowball.py`, PEP 723 pinning `mcp>=2,<3`, run by `uv run --script`; three tools for references, citations, and batch; prototyped and verified live with an on-disk cache. Chosen over `uvx semantic-scholar-fastmcp` (runner-up) and over a Bash script (rejected: scouts must be denied Bash).
- [The research loop end to end](issues/05-research-loop-end-to-end.md): six stages plus presentation and a cross-cutting honesty layer; 27 typed skills, 5 composites, 28 agents; three human gates (question, idea selection, compute spend); a row earns its place by implementing the sheet *or* serving one of four goals, so only `/watch` and `/handoff` defer. Outline in `docs/design/skills-and-agents.md`.

## Not yet specified

- Per-skill and per-agent contracts (inputs, dispatched agents, output file and headings, stop condition, anti-rationalization rows), once ticket 06 names the skills and agents.
- Which `academic.md` rules each skill inlines versus references from a shared file.
- Hooks: the write-scope guard and session announce, and the shared anti-rationalization file. Sharpens after ticket 03 and ticket 06.
- The `model:` policy for judge agents and where the second-provider hook lives.
- Skill eval prompts per skill, two or three each, and how they run.

## Out of scope

- Everything past the first slice: later milestones, ideation, experiments, the living map, composites like `/map`.
- Executing the wildfire research itself. The plugin is the deliverable; the acceptance run is the user's.
- Zotero or any external reference manager.
- The `raph-cc` marketplace beyond retiring it.
