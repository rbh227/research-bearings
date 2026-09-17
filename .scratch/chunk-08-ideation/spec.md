# Chunk 8: ideation

**Status:** ready-for-agent
**Milestone:** 4 of the build plan (`research_plugin_build_plan.md` § Milestone 4)
**Date:** 2026-09-16
**Layer under this one:** `docs/design/chunk-07-understanding.md` (the cards,
`BITS.md`, the two ledgers), `docs/design/chunk-05-gathering.md` (the matrix,
the time slice, the `searcher`), `docs/design/chunk-03-analogs.md` (the analog
pages and the absence rule).

Not grilled: the milestone was planned in `research_plugin_build_plan.md` and
`docs/design/skills-and-agents.md` § Stage 4, and this spec follows that plan
rather than reopening it. Build only: no `evals/` cases and no live run in this
chunk. The chunk note `docs/design/chunk-08-ideation.md` is written by the last
ticket, in the shape of the earlier chunk notes.

## Problem Statement

The plugin can find papers, understand them, and name what the field takes for
granted. It cannot propose anything. `BITS.md` lists assumptions with nothing
that flips them; the analog pages carry an opportunity per field that no file
collects; the merger marks contradictions that nothing reads; the time slice
shows directions that stopped, and nothing asks why. Chunk 7 built four inputs
for this milestone — cards, bits, the datasets and groups ledgers — and the
merger's contradiction list has been waiting since chunk 5.

Without this chunk the user carries every idea in their head between sessions,
generates from whatever they read most recently, and has no record of which
ideas were already considered and dropped. That is exactly the failure the
measured study names: AI-generated ideas sit 0.322 from their seed literature
where human follow-up work sits 0.410, because local elaboration is what
happens by default and it looks like productivity.

## Solution

Two skills and two agents.

`/brainstorm` is the dump. The user talks; the skill asks from the Polya, the
Hamming and the stakeholder banks, and spawns four to six `persona-ideator`
agents built from the field's own record — the decision-maker in
`QUESTION.md`, the labs in the groups ledger, the venues on the cards, the
producers of the datasets in the ledger — each of which asks its own questions
in its own file. Nothing is judged, nothing is ranked, nothing is killed.
Everything lands in `research/IDEAS.md`.

`/ideas` is the loop. It generates candidates from five seed kinds — bits,
analog opportunities, the merger's contradictions, abandoned directions, and
the personas' questions — puts every candidate to the index and writes what
came back, dispatches `diversity-planner` to name the fields that would make
the set less self-similar, sends one `searcher` per approved field, and
generates again from what returns. Survivors get a page at
`research/ideas/<slug>.md` with the seed it came from, the nearest existing
paper and its row count, and the written typicality note. Everything appends
to `IDEAS.md`.

## User Stories

### The running log

1. As a researcher, I want one file that accumulates every idea across every session, so that ideas do not die with the run that produced them.
2. As a researcher, I want both ideation skills to append to that file and never rewrite it, so that what I thought three weeks ago is still there to read.
3. As a researcher, I want every logged idea to name the date, the skill, and the seed it came from, so that I can tell a persona's question from a bit's flip six weeks later.
4. As a researcher, I want ideas I dropped kept in the log with why, so that my own abandoned directions are visible the same way the field's are.
5. As a researcher, I want the log to say which ideas were promoted to a page, so that the log and the pages cannot silently disagree.

### Brainstorming

6. As a researcher, I want `/brainstorm` to run as a conversation rather than a generator, so that what comes out is mine and the plugin's questions are the prompt.
7. As a researcher, I want the important-problem questions asked before any feasibility question, so that the session does not converge on what is easy before it has considered what matters.
8. As a researcher, I want each of Polya's seven transformations applied to my problem and what falls out recorded, so that the stuck directions get a systematic push rather than a vague one.
9. As a researcher, I want four to six personas generated from my field's own record rather than from a stock list, so that the perspectives are the ones that exist around this question.
10. As a researcher, I want each persona to ask its own questions in its own file, so that I can see who asked what and the union is not flattened into one voice.
11. As a researcher, I want a persona to be told which files it may read and to ground its questions in them, so that a persona is a perspective on my field and not a character.
12. As a researcher, I want `/brainstorm` to decide nothing — no ranking, no novelty claim, no killing — so that the dump stays a dump.
13. As a researcher, I want `/brainstorm` to work with no landscape and no cards, from `QUESTION.md` alone or from what I type, so that I can brainstorm before the gathering is done.
14. As a researcher, I want everything the session produced appended to `IDEAS.md` at the end with its source, so that the next `/ideas` run has it as a seed.

### Generating

15. As a researcher, I want `/ideas` to read five seed kinds — bits, analog opportunities, contradictions, abandoned directions, and persona questions — so that generation does not start from the nearest papers alone.
16. As a researcher, I want every candidate to name the seed it came from by file and line, so that I can go back to what produced it.
17. As a researcher, I want the seed inventory shown to me before generation, with how many of each kind exist, so that I can see when a seed kind is missing and say whether to go anyway.
18. As a researcher, I want a bit to be turned into a candidate by flipping it — stating what follows if the assumption is false — so that `BITS.md` is used as Ré intended rather than summarised.
19. As a researcher, I want a contradiction between two cards or two sections turned into a candidate that would settle it, so that the anomaly is a seed and not a footnote.
20. As a researcher, I want abandoned directions taken from the time slice and the sections mechanically — an early thread with no current follow-up, named with the line it came from — so that "abandoned" is a reading of the record and not a feeling.
21. As a researcher, I want every candidate put to the index and its nearest existing paper and row count written down, so that novelty is a retrieval result rather than a feeling.
22. As a researcher, I want a candidate whose nearest existing paper is plainly the same idea marked as an increment and kept, so that the log records what was considered and why it was not new.
23. As a researcher, I want `diversity-planner` to read the candidate set and name the fields that would make it less self-similar, with the query for each in that field's words, so that the second round is not the first round again.
24. As a researcher, I want to approve the field list before any searcher runs, so that the run's cost is something I saw before it was spent.
25. As a researcher, I want one searcher per approved field, capped, writing its own section, so that the retrieval round costs what a `/scout` round costs and no more.
26. As a researcher, I want a second generation round that reads the returned sections, so that the retrieval actually feeds generation rather than decorating it.
27. As a researcher, I want the loop to stop after two rounds by default and to tell me what a third would add, so that a bounded loop is bounded by a number I can see.
28. As a researcher, I want the run to refuse to stop while every surviving candidate comes from one seed kind or one field, so that the diversity rule has teeth without anything computing a similarity score.
29. As a researcher, I want each surviving candidate written as its own page with fixed headings, so that `/premortem`, `/rank` and `/spec` read the same shape from every idea.
30. As a researcher, I want each page to carry what would have to be true for the idea to work and the cheapest thing that would kill it, so that a page is a testable proposal and not a wish.
31. As a researcher, I want the typicality note written by hand as a sentence about conventional core and atypical injection, so that Uzzi's rule is applied without anything computing it.
32. As a researcher, I want "unexplored", "gap", "novel" and "nobody" to be absent from every idea page, so that the absence rule that governs the analog pages governs these too.
33. As a researcher, I want every paper an idea page names to carry a verify tag, so that a fabricated citation cannot enter through an idea.
34. As a researcher, I want `/ideas` to work with no bits file and no analogs, generating from whatever seeds exist and naming the ones that were missing, so that a thin repo still gets a run.
35. As a researcher, I want the run to report candidates generated, promoted, marked increments, seed kinds used, and fields searched, so that I know what the next run should do differently.

### Plumbing and honesty

36. As a researcher, I want both new agents fenced by the guard exactly like the existing ones — writing only under the research folder, holding no web tool — so that the fence is enforcement and not prose.
37. As a researcher, I want both new templates registered with the heading checker, so that a skill cannot claim to write a heading that does not exist.
38. As a researcher, I want a checker that fails on an idea page missing a heading, a nearest-existing line, a seed, or a verify tag, and on a log whose promoted list names a page that does not exist, so that a malformed idea is caught before `/rank` reads it.
39. As a researcher, I want the README, the skills-and-agents design doc and the glossary updated with the two new skills and agents, so that a new person can find them in five minutes.

## Implementation Decisions

### No new script, and no new verb

`/ideas` needs exactly one retrieval behaviour — put a candidate to the index
and get back the nearest existing paper and a row count — and `snowball.py`
already has it. The main thread runs it, the same call `/scout` makes:

```
... neighborhood "<the candidate, in the home vocabulary>" --seeds 5 --budget 30 --top 1
```

Consistency here is the point: an idea page's `Nearest existing:` line and an
analog page's mean the same thing because they came from the same call.

Retrieval for the diversity round is the `searcher` agent, unchanged — chunk 5
rewired every retrieving skill onto it and this one joins them. `/ideas`
dispatches it in analog mode with the planner's query and an output path under
`research/ideas/sections/`, not into `/scout`'s directory, because these
sections belong to an ideation round and `/scout` must not appear to have run.

### `research/IDEAS.md`, the running log

- One file at the research root, from a new template, four headings: `## Log`,
  `## Promoted`, `## Dropped`, `## Status`.
- **Append-only.** Both skills add; neither rewrites an existing entry, and
  nothing is deleted. An idea that turned out to be a duplicate gets a line
  under `## Dropped` saying so; it does not disappear from `## Log`.
- A log line carries: the date, the skill that wrote it, the idea in one
  sentence, and the seed — `bit:<group>`, `analog:<slug>#<field>`,
  `contradiction:<matrix cell>`, `abandoned:<line>`, `persona:<slug>`, or
  `conversation` for what the user said in `/brainstorm`.
- `## Promoted` names the ideas that have a page, by slug. `check_ideas.py`
  fails if a promoted slug has no page — the log and the pages may not
  disagree.

### `/brainstorm`

- Skill in the main thread with Read, Glob, Grep, Write, Edit, AskUserQuestion,
  Agent. No Bash: it retrieves nothing.
- **Input, in this order, each overriding the last:** `research/QUESTION.md`
  and `research/CONTEXT.md`; `research/BITS.md`, the cards, the ledgers and the
  analog pages if they exist; the invocation text. With none of them it runs
  from what the user types and says in `## Status` that it was unframed.
- **The three banks, asked in this order.** Hamming first: what are the
  important problems in this field, and why are you not working on them.
  Then Polya: the seven transformations — solve a related easier problem, drop
  a constraint, add a constraint, vary the goal, work backwards from the end
  state, generalize, specialize — applied to the user's problem one at a time,
  with what falls out of each recorded even when it is "nothing". Then the
  stakeholder bank: who is affected, who pays, who would have to change what
  they do. Feasibility is not asked here at all; `/premortem` owns it.
  The order is the rule, not a preference: importance before feasibility is
  Hamming's whole point, and a session that asks "could you do it" first
  converges on what is easy.
- **Personas are generated from the record, four to six of them.** Sources, in
  order: the decision-maker named in `QUESTION.md`, the labs in
  `research/landscape/groups.md`, the venues on the cards, the dataset
  producers in `research/landscape/datasets.md`, and the adjacent fields named
  on the analog pages. Each persona gets a one-line warrant naming where it
  came from. With no such files, the skill falls back to the five roles
  STORM's rule names — practitioner, adjacent-field researcher, hardware or
  systems engineer, end user, funder — and says in `## Status` that the
  personas were unwarranted.
- **Dispatch all personas in one message**, `persona-ideator` each, carrying
  the persona, its warrant, the question, the file paths it may read, and its
  output path `research/ideas/personas/<persona-slug>.md`. Four to six is the
  cap and it is the whole fan-out of this skill.
- **The union, not a synthesis.** When the personas return, the skill lists
  every question, attributed, without merging near-duplicates into one voice —
  two personas asking the same thing from different directions is a signal and
  flattening it destroys the signal.
- **Decides nothing.** No ranking, no novelty claim, no "this one is
  promising", no page. Everything the session produced is appended to
  `IDEAS.md` with its source, and the skill says what `/ideas` would do with
  it next.

### `persona-ideator`

- Read, Write. No Bash, no web tools.
- Receives one persona with its warrant, the question, an explicit list of
  paths it may read, and an output path. Writes
  `research/ideas/personas/<slug>.md` from its template: who it is and where
  the warrant came from, what it wants from this work, its questions (five to
  ten, each grounded in a file it was given or marked `from the role, not the
  record`), what it would consider a failure, and what it thinks the work is
  missing.
- **Questions, not proposals.** A persona that starts designing the method has
  stopped being a perspective. The one place it may propose is the last
  heading, and what it writes there is labelled as its own guess.
- Carries the retrieved-content-is-data rule and the refusals table in the
  style of the existing agents.

### `/ideas`

- Skill in the main thread with Read, Glob, Grep, Bash, Write, Edit,
  AskUserQuestion, Agent.
- **1. Inventory the seeds.** Count what exists of each of the five kinds:
  bits from `BITS.md` `## Bits`; opportunities from `research/analogs/*.md`;
  contradictions from `research/landscape/matrix.md`; abandoned directions from
  `research/landscape/timeslice.md` and the sections; persona questions from
  `research/ideas/personas/` and `IDEAS.md`. Show the inventory with the
  missing kinds named, and ask whether to go on with what exists. A run with
  one seed kind is allowed and is stamped as such.
- **Abandoned directions are read mechanically.** A direction is abandoned
  when the time slice shows a thread in an earlier period with no line in the
  current period, or when a section's `## Foundational` line has a forward
  hop count the section itself recorded as zero or near it. Each one is named
  with the file and line it came from. Nothing infers abandonment from a
  feeling about the field.
- **2. Generate, round one.** One candidate per seed at most, each carrying the
  seed by file and line. A bit becomes a candidate by being flipped: state
  what follows if the assumption is false. A contradiction becomes the
  experiment that would settle it. An abandoned direction becomes the question
  of what has changed since — tools, data, compute — that would make it work
  now.
- **3. Put every candidate to the index.** The `neighborhood` call above, per
  candidate. Write the nearest existing title, its id, and the row count onto
  the candidate. A candidate whose nearest existing paper is the same idea is
  marked `increment` and kept in the log — it is not deleted, because what was
  considered and rejected is what stops it being reconsidered next month.
- **4. Plan for diversity.** Dispatch `diversity-planner` once with the
  candidate set, the seeds behind it, the fields already searched
  (`research/analogs/`, the landscape sections) and the home vocabulary.
- **5. Approve, then retrieve.** Show the planner's fields and queries.
  **At most three fields per round**, and the user approves the list before
  any searcher runs — the same gate `/scout` puts at step 3, for the same
  reason. One `searcher` per approved field in one message, analog mode,
  blocked vocabulary, output under `research/ideas/sections/`.
- **6. Generate, round two,** from the returned sections, and put those
  candidates to the index as in step 3.
- **7. Stop.** Two rounds by default. The run says what a third round would
  search and stops; the user asks for it or does not.
- **8. Promote and write.** Candidates that are not increments get a page at
  `research/ideas/<slug>.md`. Every page runs through `check_ideas.py` and
  every paper it names through `verify` before the run reports.
- **9. Append and report.** Every candidate, promoted or not, goes to
  `IDEAS.md` with its seed and outcome. Report candidates generated,
  promoted, increments, seed kinds used, fields searched, and what a further
  round would cover.

### The diversity rule, without a number

The measured rule is "refuse to stop while the set is less diverse than the
field's own recent papers". Nothing in this plugin computes similarity — that
decision struck `similarity.py` in chunk 3 and it stands — so the rule is
enforced on what can be counted by looking:

- **A run may not stop while every surviving candidate shares one seed kind**,
  or while every candidate's nearest existing paper came from the home field's
  own vocabulary. Either state sends the run back to step 4 for one more
  planning round, and the second occurrence is reported to the user rather
  than looped on.
- The counts — candidates per seed kind, and per field of origin — are written
  in `## Status` on every run, so the spread is visible whether or not it
  triggered the rule.

This is the chunk's one departure from the milestone as written, and it is
deliberate: a threshold with no measurement behind it would be decorative, and
a decorative safety check is worse than none. Prior art, chunk 3: the budget
`/scout` passed and never charged.

### `diversity-planner`

- Read, Write. No Bash, no web tools.
- Receives the candidate set with the seed and nearest-existing line of each,
  the list of fields already searched, and the home vocabulary. Writes
  `research/ideas/diversity-<date>.md` from its template: what the set has in
  common (the honest reading of why it is self-similar), the fields it is not
  drawing on, and per proposed field a query in that field's words with the
  blocked home vocabulary beside it, plus one line on what that field would
  contribute that the set lacks.
- **Names fields, does not generate ideas.** The generation is the main
  thread's; the planner that also proposed the ideas would be planning toward
  its own answer.
- Proposes three to six fields, ranked, so the main thread's cap of three per
  round has something to cut.

### The idea page

New template, fixed headings, one file per promoted candidate at
`research/ideas/<slug>.md`:

| Heading | What goes in it |
|---|---|
| `## Idea` | One sentence. What you would do, not what area it is in. |
| `## Seed` | The kind, and the file and line it came from. |
| `## What it flips` | The assumption, contradiction or stopped direction this goes against, quoted from its file. |
| `## Nearest existing` | Title, id, row count, and the query that returned it. The only shape an absence claim may take. |
| `## What would have to be true` | The assumptions the idea rests on, one per line, each marked checkable or not. |
| `## Cheapest kill` | The smallest experiment that would end it, and what result would end it. |
| `## Typicality` | One written sentence: the conventional core and the atypical injection. Nothing computes this. |
| `## References` | Paper lines in the shared shape, each with a verify tag. |
| `## Status` | Date, skill, round, whether it was marked an increment on any earlier run, and the counts. |

The slug is the idea in three or four words, deduplicated by suffix, and is
recorded on the page and in `IDEAS.md`.

### Guard, checker, docs

- The guard needs no change: the prefix rule covers both new agents. Its
  selftest gains the frontmatter cases for `persona-ideator` and
  `diversity-planner` (neither grants Bash, WebSearch or WebFetch), their
  WebSearch and WebFetch denials, and one write case each — denied outside
  `research/`, allowed into `research/ideas/`.
- `check_ideas.py`, in the shape of `check_cards.py`: over an idea page it
  fails on a missing heading, an empty `## Idea`, a `## Nearest existing` with
  no row count or no query, a `## Seed` naming no file, an untagged reference,
  and any of the four banned absence words. Given `research/IDEAS.md` it
  checks the four log headings and fails when a promoted slug has no page.
  Ships with a selftest covering a good page, a good log, and one case per
  failure kind.
- New templates: `ideas-log.md` (`IDEAS.md`), `idea.md` (the page),
  `persona.md`, `diversity.md`. All registered in `check_headings.py` with the
  skill or agent that writes each.
- `CONTEXT.md` gains an ideation section: seed, seed kind, candidate,
  increment, promoted, abandoned direction, persona, warrant, round,
  typicality note, running log.
- README: `/brainstorm` and `/ideas` move from planned to built, the stage
  table's Processing row is unchanged (it already names `/ideas`), and the
  agent count line is updated.
- `docs/design/skills-and-agents.md` § Stage 4 gains the built marks and the
  two decisions this spec made — the mechanical diversity rule and the
  personas-from-the-record rule.
- Plugin manifest version to 0.8.0.

## Testing Decisions

Build only. No `evals/` cases and no live run in this chunk; the milestone's
test — run it on the wildfire map, and check whether the top ideas' nearest-
paper rows are actually thin — is the acceptance run and the user does it.

What ships is the repo's static layer, the same seams as every chunk since 3:

- **`check_ideas.py` with its own selftest**, a good page and a good log plus
  one case per failure kind. Prior art: `check_cards.py`'s nine cases.
- **Heading parity.** Four new templates registered with their writers.
- **Guard selftest.** The new agent cases listed above.
- **No new script cases**, because no new verb ships. That is the point of
  reusing `neighborhood`.

A good test here observes the file the checker produced or the JSON a verb
printed, from outside. It never reaches into a function.

## Out of Scope

- Evals under `evals/` for either skill, and the live wildfire run.
- Milestone 5 and everything after it: `/premortem`, `/rank`, `/spec`, and the
  experiment skills. `/ideas` writes the page they will read; it does not rank,
  score, premortem or select.
- Computing typicality, similarity, novelty or diversity as a number. The
  written note and the countable spread are the whole of it.
- A third generation round without the user asking for one, and any fan-out
  wider than six personas or three searchers.
- A new retrieval verb or a second script. `neighborhood` and `verify` are what
  this chunk calls.
- Editing `BITS.md`, the cards, the matrix or the analog pages. `/ideas` reads
  them and writes its own files.
- Deleting anything from `IDEAS.md`.
- A second-provider model for either agent.

## Further Notes

- **Why `/flip` is not here.** `docs/design/skills-and-agents.md` still names
  `/flip` in two lines about `IDEAS.md`; chunk 3 absorbed it into `/scout` and
  struck it with `flip-generator` and `novelty-checker`. Flipping a bit is a
  seed kind inside `/ideas`, per the build plan's Milestone 4. The two stale
  lines are corrected by the docs ticket.
- **Build order for `/to-tickets`.** `IDEAS.md` template and the idea page
  template; `check_ideas.py` with its selftest; `persona.md` and
  `diversity.md` templates; `persona-ideator`; `/brainstorm`;
  `diversity-planner`; `/ideas`; guard cases and heading registry; glossary,
  README, skills-and-agents, manifest version, chunk note.
- **Where the personas live.** `research/ideas/personas/` rather than
  `research/personas/`, because they are ideation inputs and nothing else
  reads them. The same reasoning puts the diversity plans and the round
  sections under `research/ideas/`.
- **The cap on candidates.** One per seed, two rounds, three fields — the run's
  size is the seed inventory the user approved at step 1 plus at most three
  searchers. That is the bound, and it is a number the user sees before
  anything runs, exactly as in `/scout`.

## Amendments after build, 2026-09-16

Recorded from the two-axis review, so the spec and the shipped files agree.

- **The stop rule's second condition carries a clause the spec did not have.**
  The spec wrote it as "every candidate's nearest existing paper came from the
  home field's own vocabulary". That is vacuously true: step 3 puts every
  candidate to the index *in the home vocabulary* by design, so the condition
  could never be false and the run could never stop. The shipped form adds
  "with no field search behind any of them", which is the condition that can
  actually clear. `skills/ideas/SKILL.md`, `CONTEXT.md` § spread, the design doc
  and the chunk note all state the shipped form.
- **`## Nearest existing` carries three required lines, not two.** The spec's
  page table said "title, id, row count, and the query", and its checker list
  stopped at "no row count or no query". The dry run found the row count
  saturates at `--budget`, so `Papers the query found: <n> of 5 requested` is
  required too, and `check_ideas.py` fails a page without it. A page written to
  the spec's original table fails the checker; that is intended.
- **`agents/searcher.md` was edited**, against "Retrieval for the diversity
  round is the `searcher` agent, unchanged". One line: its contract named two
  section directories and now names three, so an ideation round's sections live
  under `research/ideas/sections/` rather than in `/scout`'s directory. The
  agent's behaviour is unchanged; the sentence in the spec was too strong.
- **The glossary gained a twelfth term, `spread`**, beyond the eleven the spec
  listed. It is the name of the countable diversity rule, and the rule needed
  one.
- **One requirement was void.** The docs ticket asked for README's "agent count
  line" to be updated. There is no such line in README, at HEAD or now, so
  nothing was changed for it.
- **`scripts/checklib.py` was added, and the three older checkers rewired onto
  it.** Not in the spec, which scoped this chunk to one new checker. The review
  found `sections()` byte-identical in four files and the absence message
  already drifted between two; the shared shape now has one home. Every
  checker's selftest stayed green through the change.
- **The diversity plan moved to `research/ideas/plans/`.** The spec put it at
  `research/ideas/diversity-<date>.md`, beside the pages, and also had `/ideas`
  run the checker over `research/ideas/`. Those two decisions contradict:
  the checker reads every file in the pages directory as an idea page, so the
  plan fails eight heading rules on every run. Reproduced, then fixed by giving
  plans their own directory.
- **Sections, persona files and plans are dated and never overwritten.** The
  spec fixed them at `<field-slug>.md` and `<persona-slug>.md`. The retrieval
  script writes a section with `open(path, "w")`, so a second run on the same
  field replaces the evidence behind an idea already promoted and logged — an
  append-only log pointing at files that change under it. Paths now carry the
  date and deduplicate by numeric suffix.
- **The log's `analog:` seed form takes two shapes.** `analog:<slug>#<field>`
  for an analog page's field block and `analog:<field>#<section path>` for a
  section a diversity round returned. The spec listed only the first while
  `/ideas` step 6 wrote the second; both are now in the log template.
