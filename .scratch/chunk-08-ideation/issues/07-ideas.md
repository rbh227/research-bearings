# 07: `/ideas`

Type: task
Status: done
Blocked by: 01, 02, 06

## What to build

`skills/ideas/SKILL.md` (Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion,
Agent). Writes `research/ideas/<slug>.md` and appends to `research/IDEAS.md`.

The nine steps of the spec: inventory the five seed kinds and show the missing
ones before generating; generate one candidate per seed with the seed named by
file and line (a bit is **flipped**, a contradiction becomes the experiment
that settles it, an abandoned direction becomes what has changed since);
put every candidate to the index with

```
... neighborhood "<candidate, in the home vocabulary>" --seeds 5 --budget 30 --top 1
```

and write the nearest existing title, id and row count; dispatch
`diversity-planner` once; show its fields and queries and take the user's
approval before any searcher runs, **at most three fields**; one `searcher` per
approved field in one message, analog mode, blocked vocabulary, output under
`research/ideas/sections/`; generate round two from the returned sections and
index those too; stop after two rounds, saying what a third would search;
promote non-increments to pages; append everything to `IDEAS.md`; report.

**Abandoned directions are read mechanically** — a time-slice thread with no
line in the current period, or a foundational line whose section recorded a
zero or near-zero forward hop — each named with the file and line.

**The diversity rule without a number**: the run may not stop while every
surviving candidate shares one seed kind, or while every candidate's nearest
existing paper came back from the home vocabulary. Either sends it back to the
planning step once; a second occurrence is reported rather than looped on. The
per-seed-kind and per-field counts go in `## Status` every run.

An increment is kept and logged, never deleted.

## Acceptance

- [x] The skill names every heading of `templates/research/idea.md` and of the log template it appends to.
- [ ] The seed inventory is shown, and a run with one seed kind is allowed and stamped. **Not run** — build-only chunk.
- [x] The cap of three fields and the approval gate are in the skill — but **no dispatch has happened**, so the gate has never held anything back.
- [x] The checker accepts a page written to the contract by hand, and its log cross-check catches a promoted slug with no page (dry run, scratch tree). **No page has been written by the skill itself.**
- [ ] The banned absence words appear nowhere in what it writes or says. **Enforced by `check_ideas.py`, never exercised on skill output.**
- [x] Plugin validation green; heading parity green.

## Resolution

2026-09-16. `skills/ideas/SKILL.md`, ~300 lines.

Nine steps, five seed kinds, two rounds, three fields, one candidate per seed,
two user gates. The stop rule is the counted form: no run stops while every
candidate shares one seed kind or every nearest-existing came from a
home-vocabulary query, and a second occurrence is reported rather than looped
on.

**The dry run changed the page shape.** The `neighborhood` call the skill quotes
was run live: `--seeds 5 --budget 30` returned `counts.neighborhood: 30`, which
is what it returns for almost any query the search finds papers for. A bare row
count reads as a census. The page now carries `Papers the query found: <n> of 5
requested` as well, `check_ideas.py` requires both, and the skill says which
number can actually be thin.

**Also found: the walk hands back a formatted, verified line.**
`groups.current[0].line` is already in the shared paper-line shape with its id
and `· verified`. The skill says to paste it rather than retype it.

**One existing file touched.** `agents/searcher.md` named two section
directories; it now names three, so an ideation round's sections live under
`research/ideas/sections/` rather than in `/scout`'s directory.
