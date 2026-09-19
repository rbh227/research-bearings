# 07: The README with the front door first, the guard declared final, 1.0.0

Type: task
Status: done
Blocked by: 02, 03, 04, 05

## What to build

**README.** After the install block, one line: type the router and it tells
you what comes next. The loop table rewritten with `/start`, `/orient`,
`/think` as the one command per stage and the typed commands under each. The
skills list gains the four as built. The layout block lists every skill,
agent and script that exists. Every count in the document matches the tree.
The document keeps its shape; nothing moves to `docs/`.

**Design doc.** The Composites section gets the built marks and the `/think`
change with its reason. The count line is corrected.

**Glossary.** A front-door section: router, composite, file boundary,
staleness fact, brief, state script. One meaning each.

**Build plan.** Milestone 6's status rewritten as shipped, with the hooks line
closed: the guard is the final hook set, no stop-time checker and no
session-start brief, and why.

**Manifest** to 1.0.0.

## Acceptance

- [x] The README's first instruction after install is the router.
- [x] Every count in the README, the design doc and the glossary equals what a listing of the tree gives.
- [x] The design doc's Composites table shows four built rows and the `/think` sequence with `/premortem`.
- [x] The glossary defines the six front-door terms.
- [x] The build plan's Milestone 6 reads shipped and says what "hooks finalized" resolved to.
- [x] The manifest reads 1.0.0 and the static-checks verb is green.

## Resolution

2026-09-18. README, design doc, glossary, build plan and manifest edited; the
full static-checks verb and every selftest green.

**Counts, from the tree**: 27 skills, 23 agents, 11 scripts (seven checkers
and the shared library, the ingester, the state script, two retrieval
scripts), 28 templates, **32 cases** by the harness's own rule — a directory
holding `prompt.md` or `case.yaml`. The first draft of this ticket said 27:
the directory count was taken with a filter meant to drop the `read/` and
`landscape/` run folders, and it dropped the five `read-*` and `landscape-*`
cases with them. The harness's banner said 32 and was right; the documents
now say 32, and the count is reproducible with `find`.

**The README's loop table changed shape**: a fourth column, the one command
per stage beside the commands it runs, with `/read` kept as its own step
because `/think` starts after the cards exist. The layout block now lists
every skill, agent and script rather than the chunk-7 subset it had drifted
to.

**"Hooks finalized" is closed in the build plan with the reasons**, so a
later reader can tell whether the evidence for a stop-time checker has
arrived: it arrives when the checkers turn out to be forgotten before commits,
and it has not.
