# 06: Two cases for each typed loop command

Type: task
Status: done
Blocked by: 02

## What to build

The eval tier the README's loop implies. Two cases each for the nine typed
commands — setup, frame, surveys, landscape, scout, read, brainstorm, ideas,
rank — using the scaffold from ticket 02 wherever a case needs a populated
folder. The thirteen existing cases count toward their skills; new cases fill
each to two and no skill drops below the cases it already has.

Each case grades one behaviour the skill's description promises, at the
transcript level: a precondition refused, a gate shown before it is spent, a
file written with its headings, a count reported. Never an implementation
detail, never a grader's taste.

Written, listed, not run.

## Acceptance

- [x] Every one of the nine commands has at least two cases under the eval directory, in the existing prompt-plus-graders shape.
- [x] Each new case names the fixture shape it needs, or none, and the scaffold provides it.
- [x] Each grader names the one behaviour it checks and where in the skill's description that behaviour is promised.
- [x] The harness lists every case without error. None is run.

## Resolution

2026-09-18. Fourteen new cases, two each for surveys, landscape, scout, read,
brainstorm, ideas and rank; setup (3) and frame (4) already had theirs. Two
more assembler shapes, `question-only` and `selection`. The harness parses
every case at a zero cost ceiling: 32 in the suite.

**Two of the ticket's assumptions did not survive the skills' own text.**
`/brainstorm` has no precondition — an unframed run is "a normal way to use
this skill" — so its second case grades that it says it is unframed and
proceeds, not that it refuses. `/ideas` reports missing seed kinds and never
refuses on them; its two cases grade the inventory (what was found, what was
absent, each with its file) and the harder rule underneath: offline, with no
index to put a candidate to, **nothing is promoted to a page**, because a
candidate with no row count is not an idea here. That case has a
`file_exists: false` grader and a regex against the four absence words.

**One synthetic fixture, and why.** `/rank`'s bound and set-aside rule need
idea pages and pre-mortems, and no live run produced any. `fixtures/selection/`
holds six template-shaped idea pages and six pre-mortems, two `not executable
as written`, each with a first comment saying it is invented. `check_ideas.py`
passes all six. It is the only fixture that is not a copy of a run, and the
README says so.

**Every gate case has a `no-agent-before-the-gate` grader** (`Agent` called
zero times) beside its rubric, so "waits" is a count, not a judge's
impression. The `read` and `rank` cases add `file_exists: false` for the file
the skill would have written.

**Network.** The sandbox grants none by default, which makes the two
`offline` cases meaningful and the one `needs-network` case (surveys' single
searcher) gradable only on what it shows before dispatch. The fixtures README
gives the run command and says which is which.
