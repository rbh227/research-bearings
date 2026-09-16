# 08: `/groups` and `author-tracker`

Type: task
Status: ready-for-agent
Blocked by: 03

## What to build

The `authors` verb: given an author name or Semantic Scholar author id and a
year floor defaulting to three years back, return the affiliation as the
indexes have it, the papers since the floor with venue and year, and frequent
co-authors within that set. Semantic Scholar first, OpenAlex when it fails or
is keyless-throttled, states reported. Cached 30 days.

`author-tracker` (Read, Write): groups authors by shared affiliation and
co-authorship within the returned papers and writes the groups ledger from a
new template: one row per group with people, affiliation, venues, direction in
one sentence grounded in the last three years' titles, most recent paper, and
the cards of theirs in the papers folder. Sources and date per row.

`/groups` (Read, Glob, Bash, Write, Agent): collects authors from every card,
runs the verb for each author on two or more cards or first or last author on
any, dispatches the tracker once.

## Acceptance

- [ ] Offline cases: a Semantic Scholar answer; a keyless fallback to OpenAlex. Shape and state names only.
- [ ] Plugin validation green; heading parity green for the groups template.
- [ ] On the existing cards, the ledger has at least one group per distinct affiliation among frequent authors, every direction sentence traceable to titles in the verb output, and a sources-and-date line per row.
