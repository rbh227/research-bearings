# Chunk 7: understanding and the ledgers

**Status:** ready-for-agent
**Milestone:** 3 of the build plan (`research_plugin_build_plan.md` § Milestone 3)
**Date:** 2026-09-16
**Layer under this one:** `docs/design/chunk-05-gathering.md` (the landscape) and
`docs/design/chunk-04-connections.md` (the sources, the cache, the guard).

Grilled 2026-09-16, eighteen questions. Build only: no `evals/` cases and no
live run in this chunk. The chunk note `docs/design/chunk-07-understanding.md`
is written by the last ticket, in the shape of the earlier chunk notes.

## Problem Statement

The plugin can find papers and cannot understand them. `/landscape` and
`/scout` produce a matrix, a time slice and analog pages full of verified
paper lines, and nothing downstream reads a single one of those papers. The
build plan says it plainly: `/read` is the next thing that matters, because
`/scout` produces directions and nothing reads them.

Without this chunk the user reads every paper by hand, writes no card the
later skills can consume, has no way to check whether a number on a card came
from a leaky split, no way to see what the field's referees keep objecting to,
no ledger of the datasets and groups in play, and no written list of the
assumptions each part of the field shares. Milestone 4 (ideation) needs all of
those as inputs, and today none of them exist.

## Solution

Eight skills and eight agents that turn landscape lines into paper cards and
the ledgers built on them, plus the plumbing they need: a `fetch` verb that
turns a paper into text the agents can read, and three more small verbs for
OpenReview, dataset hosts, and author histories.

The centrepiece is `/read`: a three-agent protocol in which a `predictor` sees
only the abstract and introduction and commits predictions, a `reader` sees the
whole paper and never the predictions, and a `scorer` sees both and writes the
card, including the one line that says what was not obvious. The fence between
predictor and the rest of the paper is a file boundary, not a prompt
instruction: the predictor is handed a text file that ends where the
introduction ends.

Around `/read`: `/verify` tags every reference in any research file as
verified, candidate, or not found, in place. `/reviews` puts OpenReview's
objections on the card. `/datasets` and `/groups` fill two ledgers. `/audit`
flags leakage on a card. `/bits` writes the assumption each group of cards
shares. `/critique` attacks any one file with the concession ladder that
`question-critic` already uses.

## User Stories

### Fetching text

1. As a researcher, I want the plugin to download a paper and turn it into plain text from an arXiv id, a DOI, a Semantic Scholar id, or an exact title, so that no agent has to parse a PDF inside its own context.
2. As a researcher, I want the fetched text split into an intro file and a full file, so that the predictor can be given the intro file and physically cannot read further.
3. As a researcher, I want the split to happen at the first section heading after the introduction, with a page cut as the fallback, and the file to say which happened, so that I know when the predictor saw slightly too much or too little.
4. As a researcher, I want fetched text cached for 30 days under the same cache root as every other verb, so that re-reading, auditing and dataset lookups do not download the PDF again.
5. As a researcher, I want fetch to try every open-access location the indexes know (Semantic Scholar, OpenAlex, arXiv, and Unpaywall when an email is set), so that a paper without an arXiv version can still be read.
6. As a researcher, I want fetch to report "no open-access text" or "no PDF extractor installed" as a state with what was checked, not as an error, so that `/read` can fall back to a skim from the abstract and say so.

### Reading

7. As a researcher, I want `/read` with no arguments to propose the top unread papers from the landscape, show me the list, and wait for my yes, so that the most expensive step in the plugin never starts on a guess.
8. As a researcher, I want to pass my own list of titles, ids or landscape slugs to `/read`, so that I can read a paper the landscape did not rank.
9. As a researcher, I want `/read` to read at most five papers per run, so that one run stays inside a session's budget and I can run it again for the next five.
10. As a researcher, I want the predictor and the reader to run at the same time and the scorer after both, so that a full read takes two agent rounds, not three.
11. As a researcher, I want the predictor to commit predictions for the method, the main result and the weakest point before seeing anything past the introduction, so that where it was wrong tells me what was not obvious.
12. As a researcher, I want the reader to write the delta sentence, "compared to nearest prior work, this changes X and gets Y", or state that it cannot, so that a card that does not contain that sentence is visibly not understood.
13. As a researcher, I want the reader to compare the paper's result against the other cards in its matrix cell and flag any incompatibility, so that contradictions surface at read time.
14. As a researcher, I want the scorer to score each prediction against the reading and write the "what was non-obvious" line, so that the card records what a first reading would have missed.
15. As a researcher, I want every card to record which Keshav pass it stopped at, so that a skim is never mistaken for a full read.
16. As a researcher, I want `/read --skim` to produce a pass-one card from the intro text with one agent and no prediction, so that the tenth competitor can sit on the matrix without a full read.
17. As a researcher, I want `/read` to work when no matrix exists, marking the card's matrix position as unplaced and skipping the same-cell comparison, so that I can card a paper I have in hand before the landscape exists.
18. As a researcher, I want `/read --place` to fill the matrix position of unplaced cards from the current matrix without dispatching any agent, so that cards written early catch up once the landscape exists.
19. As a researcher, I want every card to carry the fields the build plan fixed for the paper card, as fixed headings, so that `/bits`, `/audit`, `/reviews` and later `/ideas` read the same shape from every card.
20. As a researcher, I want every reference a card names to have gone through `verify`, so that a fabricated citation cannot enter the papers folder through a card.
21. As a researcher, I want `/read` to tell me at the end which papers were read fully, which were skimmed, which could not be fetched, and which cards are unplaced, so that I know what the next run should do.
22. As a researcher, I want the predictor's and reader's working notes kept beside the cards, so that I can see what was predicted and what was read when a card looks wrong.

### Verifying

23. As a researcher, I want `/verify <file>` to check every reference in a landscape section, a card, an analog page, or a brief, so that fabricated citations are caught wherever they appear.
24. As a researcher, I want each reference line tagged in place as verified, candidate, or not found, so that the next skill can read the tag without a separate report.
25. As a researcher, I want a not-found reference to stay in the file with what was checked, never deleted, so that the places where recall outran the record stay visible.
26. As a researcher, I want a candidate to stay a candidate until I promote it by hand, so that a prefix match never carries the wrong paper's id.
27. As a researcher, I want `/verify` to say how many lines it tagged in each state, so that I can see at a glance whether a file is trustworthy.

### Reviews

28. As a researcher, I want `/reviews` to find a paper's OpenReview record by title or arXiv id through a script verb, so that no agent talks to OpenReview directly.
29. As a researcher, I want the review notes on the card to hold the scores, the main objections, what the authors conceded, and the decision, so that what the reviewers said sits next to the delta sentence.
30. As a researcher, I want a paper with no OpenReview record to get a dated "no record" line on its card, so that absence is recorded, not silent.
31. As a researcher, I want a field-level reviews file written once three or more cards carry review notes, saying what this field's referees keep pushing on, so that `/premortem` later knows what a reviewer would say.

### Datasets

32. As a researcher, I want `/datasets` to collect every dataset named on a card or in that paper's fetched text, so that the ledger covers what the field actually trains on.
33. As a researcher, I want each dataset looked up on the Hugging Face hub and on GitHub through a script verb, so that size, license, split files and the hosting link come from the host, not from memory.
34. As a researcher, I want each dataset row to carry the fields the build plan fixed for the dataset row, including who uses it and known flaws, so that `/audit` and `/baseline` can read it.
35. As a researcher, I want a dataset that no host returns to get a row that says what was checked, so that the ledger never pretends to a fact it does not have.
36. As a researcher, I want `/datasets` to never use web search, so that the web rule from chunk 4 holds.

### Groups

37. As a researcher, I want `/groups` to take the authors on the cards and pull their papers from the last three years through a script verb, so that the competitive landscape is built from the papers I actually understood.
38. As a researcher, I want authors grouped by lab or affiliation, with people, venues, direction, and most recent paper per group, so that I can see who is publishing on my question and where they are heading.
39. As a researcher, I want the groups ledger to name the sources and the date behind every row, so that I know when it went stale.

### Auditing

40. As a researcher, I want `/audit <slug>` to apply the Kapoor and Narayanan leakage taxonomy to one card, reading the card, the fetched text and the dataset row, so that a number I plan to build on has been checked for a leaky split.
41. As a researcher, I want every leakage flag to quote the passage that supports it or say "could not determine, checked X and Y", so that a flag is evidence, not a guess.
42. As a researcher, I want spatial and temporal overlap between splits treated as first-class leakage types, so that the remote-sensing case the wildfire work lives in is covered.
43. As a researcher, I want `/audit` to run only when I ask, per card, so that reading does not pay for an auditor on papers that never become a baseline.

### Bits

44. As a researcher, I want `/bits` to read the matrix, the time slice and the cards and write one assumption per group of cards that share a thesis, so that I can see what the field takes for granted.
45. As a researcher, I want each bit to name the cards behind it and the matrix cells those cards sit in, so that a bit is traceable to papers.
46. As a researcher, I want the grouping recorded in the bits file and kept across runs, so that `/ideas` reads a stable file and a rerun adds to it rather than reshuffling it.
47. As a researcher, I want evaluation and dataset assumptions listed as bits alongside method assumptions, so that "everyone reports on the standard split" is as visible as "everyone uses a U-Net".
48. As a researcher, I want a group with only one card marked as too thin to name a bit, so that `/bits` does not invent a shared assumption from a single paper.

### Critique

49. As a researcher, I want `/critique <file>` to dispatch a fresh-context critic against one file of any kind, so that the analog transfer arguments, a card, a section or the bits file can each be attacked by a judge that did not write them.
50. As a researcher, I want the critic to follow the concession ladder: score every rebuttal one to five, concede only at four or above, never concede twice in a row, and flag for a human if more than half of its findings are conceded, so that a same-model critic does not fold.
51. As a researcher, I want the critique written to its own file next to the research folder's other outputs, so that it does not edit the file it judged.
52. As a researcher, I want the critic to stay on Claude, so that the plugin does not grow a second-provider dependency I did not ask for.

### Plumbing and honesty

53. As a researcher, I want every new agent fenced by the guard exactly like the existing ones, writing only under the research folder, running only the retrieval scripts, and never using web tools, so that the fence is enforcement, not prose.
54. As a researcher, I want every new template registered with the heading checker, so that a skill cannot claim to write a heading that does not exist.
55. As a researcher, I want a card checker that fails on a card missing a heading, a delta sentence, a pass field, or a reference tag, so that a malformed card is caught before `/bits` reads it.
56. As a researcher, I want `/setup` to list the two new optional keys, a GitHub token and an OpenReview login, in the connections step, so that a missing key is a reported state.
57. As a researcher, I want the README and the skills-and-agents design doc updated with the eight new skills and agents, so that a new person can find them in five minutes.
58. As a researcher, I want the glossary extended with the reading terms, so that "card", "pass", "unplaced", "tag", "bit" and "group" have one meaning each.

## Implementation Decisions

### One new retrieval script beside the walker

- The new verbs live in a second retrieval script in the same directory as the walker, importing the walker's shared HTTP, cache, pacing and record helpers rather than copying them. The guard's Bash fence already admits any script in that directory, so no guard change is needed for agents to call it.
- Standard library only, like the walker. The one exception is text extraction, which needs a PDF tool the standard library does not have: the verb tries the `pdftotext` command if it is on the path, then the `pypdf` module if it imports, and otherwise reports the state `no extractor` with the two install hints. Never an error.
- Every verb answers JSON on stdout, caches under its own resolver name for 30 days, honours the cache root override, and reports missing keys and failed sources as states, exactly as chunk 4 defined them.
- New environment variables: `GITHUB_TOKEN` (optional; raises the GitHub search rate) and `OPENREVIEW_USERNAME` with `OPENREVIEW_PASSWORD` (optional; OpenReview's public API answers anonymously for public venues). Both join `health`, `status`, and the APIs reference. Neither is ever required.

### Verbs

- **`fetch`**: input is an id (arXiv, DOI, Semantic Scholar, OpenAlex) or an exact title. Resolves the record through the existing resolvers, collects every PDF location they return (Semantic Scholar open-access PDF, OpenAlex locations, arXiv, Unpaywall when the email is set), tries them in that order, downloads, extracts text, splits, and writes three files under the fetch cache: the intro text, the full text, and a metadata record naming the source URL, page count, character count, the split method, and the date. Output names the three paths and the states.
- **Splitting** looks for the first top-level section heading after the introduction (related work, background, preliminaries, method, approach, and the numbered forms of those). If none is found within the first quarter of the text, it cuts after the second page and records `split: page-cut`. Title, abstract and introduction always go in the intro file; nothing else does.
- **`reviews`**: input is a title or arXiv id. Searches OpenReview's public API for the submission, and returns the venue, decision, each official review's ratings and text, and each author response, in order. A paper with no record returns a `no record` state with the query that was run.
- **`datasets`**: input is a dataset name. Queries the Hugging Face hub datasets search and the GitHub REST search, and returns per host: name, link, license, size or file count, split files found, stars or downloads, last update. A host that returns nothing is named as such. GitHub is queried through the REST API from the script, not through the `gh` command, because the guard's Bash fence admits only the retrieval scripts and widening it for one agent is the wrong trade.
- **`authors`**: input is an author name or Semantic Scholar author id, with a year floor defaulting to three years back. Returns the author's affiliation as the indexes have it, their papers since the floor with venue and year, and their frequent co-authors within that set. Semantic Scholar first, OpenAlex when it fails or is keyless-throttled, states reported.

### The card and its template

- A paper card is one file per paper under the research folder's papers directory, from a new card template with fixed headings carrying exactly the build plan's paper-card fields: identity (slug, title, authors, year, venue, arXiv or DOI, code link and whether it runs), matrix position (formulation, data regime, or `unplaced`), the delta sentence, the bit it flips if any, what it did not compare against, the kill experiment and whether it was run, dataset and split, leakage flags, reimplementable in an afternoon, what to steal, reproduction status, prediction score, pass stopped at, plus three sections filled by later skills: reviews, leakage, and same-cell comparison. Sections a skill has not run yet hold a fixed `not run` marker, so the heading is always present.
- Reference lines on a card use the same line shape as landscape sections and end in the same tags: `verified`, `candidate`, or the new `not found`. `check_cards` enforces it.
- The slug is derived from the first author, year and first title word, deduplicated by suffix, and recorded on the card. Landscape slugs are not reused, because a landscape line has no slug.
- Working notes for a full read live in a notes directory beside the cards: one prediction file and one reading file per slug, each from its own small template. They are inputs to the scorer and are kept after the card is written.

### `/read`

- Skill in the main thread with Read, Glob, Bash, Write, Edit, AskUserQuestion and Agent. One job: cards from papers.
- With no arguments: reads the matrix and time slice, lists every paper line that has no card slug, ranks by cell density then centrality as the landscape ranked them, proposes the top five, and shows the proposal with what would remain. Waits for approval through the question tool. With arguments: resolves each to a record via `verify`, refuses a candidate, and proposes those. The cap of five per run is enforced by the skill; the proposal says how many are left.
- Per approved paper: runs `fetch`. If fetch returns text, dispatches `predictor` with the intro path and `reader` with the full path in the same turn. When both return, dispatches `scorer` with both note paths; the scorer writes the card. If fetch returns no text, the paper is skimmed from the record's abstract with `reader` in skim mode and the card says why.
- `--skim`: `reader` only, in skim mode, from the intro file. Card pass field says `1`. No prediction, no score, no same-cell comparison.
- `--place`: no agents. For every card marked unplaced, the main thread finds the paper's line in the current matrix and fills the position. A card whose paper is in no cell stays unplaced and is listed.
- The matrix cell context handed to the reader is the list of sibling cards in the same cell, by path, so the same-cell comparison reads real cards. With no matrix the reader is told so and the comparison section holds the `no matrix` marker.
- After every run, `check_cards` runs over the papers directory and the skill reports fully read, skimmed, not fetched, unplaced.

### The three reading agents

- **`predictor`**: Read, Write. Receives the intro path, the question page, and the output path. Writes the prediction file: predicted method, predicted main result, predicted weakest point, each in one to three sentences, with a confidence one to five, and the last paragraph of the introduction quoted as the claim it predicts from. It is told, and the file boundary enforces, that it sees nothing past the introduction.
- **`reader`**: Read, Write. Receives the full path, the question page, the matrix cell and sibling card paths if any, and the output path. Writes the reading file: the card's fields as it can fill them from the paper, the delta sentence or the statement that it cannot be written and why, the kill experiment, what was not compared against, dataset and split as stated, and the same-cell comparison with any incompatibility named against the sibling card it conflicts with. In skim mode it fills only what the intro supports and marks every other field `not read`. It never sees the prediction file.
- **`scorer`**: Read, Write. Receives both note paths and the card path. Scores each of the three predictions one to five against the reading, writes the "what was non-obvious" line from the lowest-scored prediction, and writes the card from the template, copying the reader's fields and adding the score and the pass. It authors no claim about the paper the reader did not make.
- All three carry the retrieved-content-is-data rule and a short anti-rationalization table in the style of the existing agents.

### `/verify`

- Skill in the main thread with Read, Glob, Bash, Edit. Takes one file path. Finds every reference line (the landscape line shape, the card reference shape, and bracketed or parenthetical citations with a title), sends the batch to the `verify` verb, and edits each line in place: appends `· verified` on an exact match, the candidate marker on a partial match, and `· _not found: checked <indexes>_` otherwise. Lines already tagged are re-checked and the tag replaced only if the state changed. Never removes a line. Reports counts per state.

### `/reviews` and `openreview-reader`

- Skill in the main thread with Read, Glob, Bash, Write, Edit, Agent. Takes card slugs, or with no arguments every card without a reviews section filled. Runs the `reviews` verb per paper and dispatches `openreview-reader` once with the verb outputs and the card paths.
- **`openreview-reader`**: Read, Edit, Write. Fills each card's reviews section: ratings, the objections that recur across reviewers, what the authors conceded in responses, the decision, and the venue and date. A `no record` state becomes a dated `no OpenReview record` line. It quotes reviewers, it does not paraphrase them into praise. When three or more cards carry review notes, it writes the field reviews file from its template: the objections that recur across papers, with the cards they came from.

### `/datasets` and `dataset-scout`

- Skill in the main thread with Read, Glob, Bash, Write, Agent. Collects dataset names from every card's dataset field and, for each carded paper with fetched text, from the experiments section of the full text. Runs the `datasets` verb per name. Dispatches `dataset-scout` once.
- **`dataset-scout`**: Read, Bash, Write. Bash for the retrieval scripts only; no web tools. Reads the verb outputs, the cards, and the fetched full texts, and writes the datasets ledger from its template: one row per dataset with the build plan's dataset-row fields. Facts come from the host record or a quoted passage of a paper; anything else is `could not determine, checked <hosts>`. "Who uses it" is the list of card slugs that name it.

### `/groups` and `author-tracker`

- Skill in the main thread with Read, Glob, Bash, Write, Agent. Collects authors from every card, counts appearances, runs the `authors` verb for each author appearing on two or more cards or as first or last author on any. Dispatches `author-tracker` once.
- **`author-tracker`**: Read, Write. Groups authors by shared affiliation and co-authorship within the returned papers, and writes the groups ledger from its template: one row per group with people, affiliation, venues, direction in one sentence grounded in their last three years' titles, most recent paper, and the cards of theirs in the papers folder. Names the sources and date per row.

### `/audit` and `leakage-auditor`

- Skill in the main thread with Read, Glob, Bash, Agent. Takes exactly one card slug. Runs `fetch` to ensure the text is present, finds the dataset row if the ledger exists, and dispatches `leakage-auditor`.
- **`leakage-auditor`**: Read, Edit. Fills the card's leakage section with the Kapoor and Narayanan taxonomy: no held-out test set, preprocessing or feature selection fitted on the union, duplicates across splits, temporal leakage, spatial leakage (tile or scene overlap), group leakage, illegitimate features, and test set not representative of deployment. Each flag carries a quoted passage or a `could not determine, checked <sections>` line. No score, no verdict: flags and evidence.

### `/bits`

- Skill in the main thread with Read, Glob, Write, Edit. No agents. Reads the matrix, the time slice, and every card. Writes the bits file from its template with two parts: the groups, and the bits.
- **Grouping.** On the first run the skill groups the cards by shared thesis, using the delta sentences and the matrix positions, and records the grouping in the bits file with the card slugs per group. On later runs it reads the recorded groups first, assigns new cards to existing groups where they fit, and proposes a new group only for cards that fit none, marked as new in that run. A group is never dissolved by the skill. This is the one place the chunk departs from the grilling: the landscape does not carry thesis groups, so `/bits` has to make them, and recording them is what keeps the file stable for `/ideas`.
- **Bits.** One per group with two or more cards: the assumption, stated in one sentence; the cards behind it; the matrix cells those cards sit in; and whether it is a method, evaluation, or dataset assumption. A group with one card is listed as too thin. Evaluation and dataset bits are drawn from the dataset and split fields and the datasets ledger when it exists.

### `/critique` and `critic`

- Skill in the main thread with Read, Glob, Write, Agent. Takes one file path under the research folder. Dispatches `critic` with that path, the context page, and the question page. Then runs the ladder: reads the critique, writes a rebuttal per finding as the author, sends the rebuttals back to the same critic, and records the scored outcome.
- **`critic`**: Read, Write. Fresh context, sees the file and nothing of the reasoning behind it. Writes the critique file: findings, each with the passage it attacks, the objection, and the ask. Second pass: scores each rebuttal one to five, concedes only at four or above, never concedes two findings in a row, and flags for a human when more than half are conceded. Repeated pushback, appeals to authority, and bare requests to soften score one. Model field inherits; no second-provider hook.
- The critique lives in a critiques directory under the research folder, one file per critiqued file per run, dated. The critiqued file is never edited by `/critique`.

### Guard, setup, docs

- The guard's write scope, Bash fence and web rule cover the eight new agents without change: they write under the research folder, run only the retrieval scripts, and hold no web tool. The guard selftest gains cases for `dataset-scout` (Bash allowed for the script, denied for `gh`), `predictor` (no Bash), and `critic` (no Write outside the research folder).
- `/setup`'s connections step reports the two new optional keys through `status`, which gains a probe for GitHub and for OpenReview. Neither enters the "keys that would help most" list; that list stays the chunk 4 three.
- New templates: card, prediction note, reading note, reviews (field level), datasets ledger, groups ledger, bits, critique. All registered with the heading checker, each naming the skill or agent that writes it.
- `check_cards`: a structural checker over the papers directory in the shape of the landscape and analogs checkers. Fails on a missing heading, an empty delta section that is not the explicit cannot-write statement, a missing pass value, a matrix position that is neither a cell nor `unplaced`, and a reference line with no tag.
- The glossary gains a reading section: card, pass, intro text, full text, unplaced, tag, review notes, leakage flag, group, thesis group, bit, critique.
- The README's skill list, the skills-and-agents design doc's Stage 3 table, the APIs reference, and the plugin manifest version are updated by the last ticket, which also writes the chunk note.

## Testing Decisions

Build only. No `evals/` cases and no live run against the wildfire question in this chunk. The user runs the milestone's live test by hand afterwards and that produces the next chunk's loose idea, as the glossary's acceptance run.

What ships is the repo's static layer, the same four seams every chunk since 3 has used:

- **Script selftests.** Every new verb ships offline cases against saved fixtures in the existing fixtures directory, in the style of the walker's 44 cases: `fetch` (a two-column arXiv PDF text with a numbered related-work heading; one with no heading, page cut; one with no PDF location, state reported; one with no extractor available), `reviews` (a record with two reviews and a response; a `no record`), `datasets` (a Hugging Face hit and a GitHub hit; both empty), `authors` (a Semantic Scholar answer; a keyless fallback to OpenAlex). Fixtures are recorded API responses, not live calls. A good case asserts the JSON shape and the state names and nothing about internals.
- **Heading parity.** The eight new templates registered with the heading checker, with the writing skill or agent named. Prior art: every template since chunk 1.
- **Guard selftest.** The new agent cases listed above, in the guard's existing selftest. Prior art: the 35 cases from chunk 5.
- **Card checker.** `check_cards` with its own cases: a good card passes; each of its five failure kinds is caught. Prior art: the landscape and analogs checkers.

A good test here observes the file the verb or checker produced, or the JSON it printed, from outside. It never reaches into a function.

## Out of Scope

- Evals under `evals/` for any of the eight skills, and the live wildfire test (DA-SegFormer plus two competitors, `/bits` on the wildfire matrix). Deferred to the acceptance run.
- Milestone 4 (`/brainstorm`, `/ideas`) and anything after it. `/bits` writes the file `/ideas` will read; it does not read it.
- A `/read` fan-out wider than five papers or more than two agents at a time.
- An `/audit` sweep with no argument. Per card only.
- Computing typicality, similarity, or any score over cards. Prediction scores are the scorer's judgment, one to five, written as a number the way the ladder writes rebuttal scores.
- Zotero: the probe exists, no verb uses it. "Which of these do I already have" waits.
- The Hugging Face daily-papers index. The hub is used for datasets only.
- Copying paper text into the research folder. Text lives in the cache.
- A second-provider model for the critic.
- Widening the guard's Bash fence to `gh` or any other command.

## Further Notes

- **The Q15 correction.** The grilling settled `/bits` on "the landscape's thesis groups." On inspection the landscape has no such thing: sections are per landscape question, the matrix is formulation by data regime, and the merger records contradictions, not theses. The spec keeps both halves of what was chosen, Ré's thesis grouping and a file that does not reshuffle between runs, by having `/bits` make the groups once and record them. If a cell-based grouping is preferred instead, that is a one-line change to the `/bits` decision and the bits template.
- **`gh` became a REST call.** Q12 was worded with `dataset-scout` using the `gh` command. The guard admits only the retrieval scripts in Bash, so GitHub is reached from the `datasets` verb over the REST API. Same source, same facts, no guard change.
- **Build order for `/to-tickets`.** Second retrieval script with `fetch` and its cases; card template, note templates, `check_cards`; the three reading agents; `/read`; `/verify`; `reviews` verb, `openreview-reader`, `/reviews`; `datasets` verb, `dataset-scout`, `/datasets`; `authors` verb, `author-tracker`, `/groups`; `leakage-auditor`, `/audit`; `/bits`; `critic`, `/critique`; guard cases, `status` probes, setup step, docs, glossary, README, manifest version, chunk note.
- **Rate limits worth knowing.** GitHub search unauthenticated is 10 requests a minute; the verb paces to that. OpenReview's public API is unpaced in its terms; the verb uses the 1-per-second pace as a courtesy. Hugging Face hub search is generous; the existing token raises it.
- **Card slugs versus landscape lines.** Landscape lines carry ids, not slugs. `/read` resolves a line to a record by id, and the record's id goes on the card, so a card is joinable back to its section line by id.
