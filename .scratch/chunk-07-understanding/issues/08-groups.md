# 08: `/groups` and `author-tracker`

Type: task
Status: done
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

- [x] Offline cases: a Semantic Scholar answer; a keyless fallback to OpenAlex. Shape and state names only.
- [x] Plugin validation green; heading parity green for the groups template.
- [x] On the existing cards, the ledger has at least one group per distinct affiliation among frequent authors, every direction sentence traceable to titles in the verb output, and a sources-and-date line per row.

## Resolution

2026-09-16. The `authors` verb, `agents/author-tracker.md`,
`skills/groups/SKILL.md`, `templates/research/groups.md`.

Live on the three cards: six authors queried (two or more cards, or first or
last author on one), fourteen middle authors named as not queried and why.
Two groups written.

**Two corrections the run forced into the verb.** A name search for "Yu Shen"
returned a profile with fifty papers since the floor, because the name belongs
to several people; resolving the author through the paper the card already
names cut it to eight, so the verb takes `--paper` and the skill always passes
it. And the author-papers endpoint pages at 100 with no promised ordering, so
filtering one page by year under-reported a prolific author badly — it pages
to 500 now and sets `complete: false` when the cap stops it.

**The output is honest in the three places it could have bluffed.** Every
affiliation but one is `not stated by either index`, which is a fact about the
index and not about the group. One group's Heading line reads `no clear
direction from three years of titles`, with the mixed titles listed beside it.
And Mubarak Shah's row says his three titles are a partial slice because his
lookup hit the cap, rather than presenting three papers as a senior author's
whole recent record.

The one real direction it did find is checkable: Yu Shen and Qian Du moved
from building-damage assessment to hyperspectral and multispectral
classification, with no title since 2023 touching damage assessment.
