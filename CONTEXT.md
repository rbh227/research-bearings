# CONTEXT.md

Glossary for the research plugin effort. One meaning per word.

## Terms

- **map**: The wayfinder planning artifact for an effort, under `.scratch/<effort>/map.md`, with one child ticket per decision. Never used for anything the plugin produces.
- **landscape**: The plugin's Milestone 1 deliverable for a research question: the surveys diff, the concept matrix, the time slice, and the brief. The build plan's "map chain" is the sequence of skills that produces a landscape.
- **ticket**: A wayfinder child issue holding one decision or investigation. Not a plugin concept.
- **destination**: What a map is finding its way to. For this effort: Milestones 0 and 1 specified sharply enough to hand to `/to-spec`.
- **research-bearings**: The plugin this effort is building. A Claude Code plugin whose typed skills and contract-bound agents run the research loop; Milestone 1 produces a landscape.
- **acceptance run**: A trial of the built plugin on a real research question, performed by the user after handoff. Not part of any map; it produces the next map's loose idea.

## Retrieval terms

Added with chunk 2. All of these describe one `/research-bearings:snowball` run.
The skill was called `/scout` until 2026-09-14; the name moved to the breadth
tool (chunk 3), and the depth tool took the name of what it does.

- **section**: One markdown file under `research/landscape/`, answering one question, written by one `paper-scout`. A landscape is assembled from sections; a section is never a landscape.
- **card**: One paper's entry inside a section's `## Papers`. Metadata plus one quoted citation sentence plus one `Kept because` line. Never a summary.
- **seed**: A paper found by search, from which hops start. Seeds are found, not hopped to.
- **hop**: One `references` (backward) or `citations` (forward) call of the retrieval script from one seed. A **round** is a hop in both directions across the current seed set.
- **touched** / **kept**: Touched is every paper a hop returned and counts against the budget. Kept is the 25–35 that reach `## Papers`. The design once conflated them.
- **saturation**: A stop reason: a completed round added fewer than three keepers. Not claimable if any hop in that round was truncated.
- **budget**: A stop reason, and the ceiling that causes it, denominated in papers touched. `budget` always means the section is incomplete. **Enforced by the retrieval script**, which keeps a ledger per run and refuses hops past the ceiling before spending the request; it was a line in the agent's prompt until 2026-09-13, and under that arrangement it did not hold.
- **ledger**: `research/.crawl/<slug>.touched.json` — the distinct papers the script has handed a run. The count the section must agree with; `/snowball` reads it back and reports it over the section's figure if they differ.
- **saved crawl**: A directory of the script's JSON outputs, one per call, read in filename order in place of running the script. How the evals reach the agent and how a crawl is replayed offline.
- **truncated**: A hop whose result carried a non-null `next` — the API held rows back, so the hop sampled the edge list rather than reading it. Paging is not built.
- **unresolvable**: A cited work with no Semantic Scholar record, carrying only title, venue and year. Never hopped from, never counted. Mostly grey literature.
- **anchored** / **unanchored**: Whether the run took scope and vocabulary from `research/QUESTION.md`. Unanchored runs are stamped as such in the section.
- **degradation stamp**: A line at the top of a section recording that the run was reduced — no API key, truncated hops, a question search cannot answer.
