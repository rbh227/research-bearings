# 01: the running log and the idea page

Type: task
Status: done
Blocked by: —

## What to build

Two templates under `templates/research/`, in the comment-only style of the
existing ones (every heading present, every heading's contents described in a
comment, nothing that could be mistaken for content).

`ideas-log.md` → `research/IDEAS.md`. Four headings: `## Log`, `## Promoted`,
`## Dropped`, `## Status`. Append-only: the comments say that both skills add
and neither rewrites, that nothing is deleted, and that an idea that turned out
to be a duplicate gets a `## Dropped` line rather than disappearing from
`## Log`. A log line carries date, the skill, the idea in one sentence, and the
seed in the fixed form `bit:<group>`, `analog:<slug>#<field>`,
`contradiction:<cell>`, `abandoned:<line>`, `persona:<slug>`, or
`conversation`. `## Promoted` lists slugs that have a page.

`idea.md` → `research/ideas/<slug>.md`. Nine headings in this order: `## Idea`,
`## Seed`, `## What it flips`, `## Nearest existing`, `## What would have to be
true`, `## Cheapest kill`, `## Typicality`, `## References`, `## Status`. The
comments carry the contracts from the spec: `## Nearest existing` is the only
shape an absence claim may take and holds title, id, row count and the query;
`## Typicality` is one written sentence about the conventional core and the
atypical injection and nothing computes it; `## References` uses the shared
paper-line shape with a verify tag on every line.

## Acceptance

- [x] Both templates exist with exactly the headings above, in order.
- [x] Every heading's comment says who writes it and what belongs in it.
- [x] No template line would pass as content: the files are headings plus comments.
- [x] `python3 scripts/check_headings.py` still passes (registration lands in ticket 08; until then these templates are not registered).

## Resolution

2026-09-16. `templates/research/ideas-log.md`, `templates/research/idea.md`.

Both comment-only, both registered in ticket 08. The idea page came out at nine
headings as specified, and then grew two lines inside `## Nearest existing`
after the dry run in ticket 07 found the row count saturates — see that
ticket's resolution and the chunk note § 4.

**One heading name had to be defended rather than chosen.** `## Seed` means
where the idea came from; the Gathering glossary already uses `seed` for a paper
a walk starts from, and the first draft put both senses on one page. The
retrieval count is now written `Papers the query found`, and the glossary entry
names the collision.
