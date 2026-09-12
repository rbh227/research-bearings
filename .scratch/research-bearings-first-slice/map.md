# Map: research-bearings, first slice

Label: wayfinder:map

## Destination

A spec for the first buildable slice of research-bearings, ready for `/to-spec`: the skill and agent set chosen from `academic.md`, their contracts, the schemas they share, and the retrieval plumbing. Done when nothing is left to decide before someone scaffolds it.

## Notes

- **Domain**: a Claude Code plugin that runs the research loop with typed skills and contract-bound agents. Glossary in `CONTEXT.md`: **map** is this artifact only; **landscape** is the plugin's literature deliverable; an **acceptance run** is the user's post-handoff trial.
- **Inputs**: `academic.md` is "the big sheet", the source rules every skill derives from. `research_plugin_build_plan.md` is one candidate proposal for the loop and its milestones, not the plan.
- **Standing decisions** (from the build plan, reaffirmed 2026-09-12): Claude Code plugin; this repo is its own marketplace (`marketplace.json` with `source: "./"`, like the Matt-Raphs-Skills fork), retiring `raph-cc`; v1 is eventually the full loop including experiment agents; Claude-only with the judge's `model:` field left open for a second provider; Python for the few scripts; local paper cache is the reference manager; one spec covers schemas and their first consumers together.
- **Retrieval plumbing**: two MCP servers, `paper-search-mcp` (arXiv, Semantic Scholar, OpenAlex, Crossref, and more) and `openreview-mcp`. Both are 1.x-SDK servers and need `uvx --with 'mcp<2'`. OpenReview is registered at user scope on this machine; paper-search is ticket 04.
- **Acceptance-run topic** (the user's real question, used for smoke runs, never a deliverable): post-disaster building damage assessment from aerial and satellite imagery, plus computer vision and AI in wildfires generally, including fire-spread prediction.
- **Skills to consult per session**: `grilling` and `domain-modeling` for every grilling ticket; `research` for research tickets; `prototype` for ticket 09. Plugin authoring follows `writing-for-agents`.
- **Repo**: https://github.com/rbh227/research-bearings. Tracker is local markdown under `.scratch/`.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->

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
