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

Added with chunk 2 for a snowballing skill, replaced with chunk 3's when that
skill was deleted (2026-09-14). All of these describe one `/research-bearings:scout`
run.

- **shape**: The problem written without the home field's nouns — what it is structurally, in words any field would recognise. The one step nothing else in the plugin does, and the rest of a run is only as good as it.
- **field**: One area that shares the shape and not the vocabulary, searched in its own words. A field whose papers would plausibly cite your seeds is not a field, it is the home field with a wider collar.
- **home vocabulary**: The words `## Vocabulary` in `research/QUESTION.md` lists. Stripped in step 1, banned from field names, and never used as a query — a query in your own words finds your own field.
- **transfer**: Why a field's method might move to your problem, and what is different about it. Grounded in the rows the search returned.
- **opportunity**: What you would actually try, per field. The one speculative thing in the file, and labelled as such.
- **nearest existing**: The opportunity put to the index, with a row count and the closest title. This is the only shape an absence claim may take here; "unexplored", "gap", "novel" and "nobody" do not appear at all.
- **verify**: Resolving every paper the file names against the record — by id, or by title with case, punctuation and spacing folded. **Only an exact match resolves.** A prefix or substring match is reported as a candidate and not certified: measured 2026-09-14, "Attention Is All You Need for Wildfire Damage Assessment" prefix-matched "Attention Is All You Need" and came back resolved, carrying the wrong paper's id.
- **unresolved**: A paper `verify` could not match. It stays in the file, marked, with the closest thing the search did return. Never deleted: where recall outran the record is what a reader wants to see.
- **framed** / **unframed**: Whether the run took its problem from `research/QUESTION.md`. Unframed runs are stamped as such, and are a normal way to use the skill.
- **bound**: Searches times `--limit`, where the searches are the field list the user approves before any of them run. There is no budget and no ledger: a citation walk compounds and needs a ceiling enforced per request, and search does not.
