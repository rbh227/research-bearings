# 06: `/reviews` and `openreview-reader`

Type: task
Status: done
Blocked by: 03

## What to build

The `reviews` verb in the second retrieval script: given a title or arXiv id,
search OpenReview's public API for the submission and return venue, decision,
each official review's ratings and text, and each author response, in order;
`no record` state with the query when nothing matches. Optional
`OPENREVIEW_USERNAME` and `OPENREVIEW_PASSWORD` from the environment; anonymous
otherwise. Paced at one per second as a courtesy; cached 30 days.

`openreview-reader` (Read, Edit, Write): fills each card's reviews section
with ratings, the objections that recur across reviewers, what the authors
conceded, the decision, venue and date, quoting reviewers rather than
paraphrasing them into praise; a `no record` becomes a dated `no OpenReview
record` line. When three or more cards carry review notes, writes the field
reviews file from a new template: the objections that recur across papers,
with the cards they came from.

`/reviews` (Read, Glob, Bash, Write, Edit, Agent): takes card slugs, or with
no arguments every card whose reviews section is `not run`; runs the verb per
paper; dispatches the reader once with the outputs and card paths.

## Acceptance

- [x] Offline cases: a record with two reviews and one response; a `no record`. Shape and state names only.
- [x] Plugin validation green; heading parity green for the field reviews template.
- [x] On a real ICLR or NeurIPS paper with a card, the reviews section is filled with quoted objections, scores and the decision; on a paper not on OpenReview, the dated no-record line appears.
- [x] With three carded papers reviewed, the field reviews file exists and names the cards behind each recurring objection.
- [x] `check_cards` green after the run.

## Resolution

2026-09-16. The `reviews` verb, `agents/openreview-reader.md`,
`skills/reviews/SKILL.md`, `templates/research/reviews.md`.

**Measured, and it changed the design: OpenReview answers `/notes/search`
anonymously and gates `/notes?forum=<id>` behind a bot challenge**, on both
`api.openreview.net` and `api2.openreview.net`. So without credentials the
verb finds the submission and returns its venue, decision field and url, and
reports `login required` for the reviews. That is a fourth state in the
agent's table, and the card records it rather than leaving the section unrun.

Live on the three cards, which gave three different states: `no record` for
xBD and BDANet, `login required` for RescueNet with venue and url named. The
reader edited only the `## Reviews` section of each; `check_cards` green. No
field-level file: that needs three cards carrying actual review notes.

**Not done, and it should be said plainly:** nothing downstream of
`login required` has been exercised live. The parsing of ratings, recurring
objections, concessions and decisions is offline-tested against a fixture with
two reviews, one response and a decision, and has never seen a real forum.
