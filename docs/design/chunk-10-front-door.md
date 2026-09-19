# Chunk 10: the front door

2026-09-18. The last milestone. Twenty-three skills become usable by somebody
who did not build them: a router that reads what exists and names the
next move with its evidence, three composites that walk a stage in one sitting
without taking a step nobody said yes to, and the loop written down once, as
data, so that the router, the composites and a grader all read the same facts.

The spec is `.scratch/chunk-10-front-door/spec.md`, with eight tickets in
`issues/`. **Grilled one question at a time** — twelve questions, mostly "what
does this skill look like from your chair" — and the answers are in the spec's
`## Decisions settled at planning`. Unlike chunks 7 to 9 this one has eval
cases (written, parsed, not run) and two live runs, recorded in §3. Version
1.0.0.

## 1. Decision record

- **The router is the doorman, not the signpost and not the chauffeur.** It
  reads the state, prints a one-screen brief, names the next command with the
  precondition it checked, asks once, and on yes invokes the skill in the same
  thread. A router that only points is one more name to remember; one that
  runs unasked removes the gate the plugin is built around. At a fork it
  offers two or three moves with a reason each. Given a goal it can see will be
  refused — "rank my ideas" with no pre-mortems — it says what is missing,
  which command writes it, walks back until it finds one that can run, and
  offers that. It never previews what a blocked skill would have asked; that
  is the rule `/frame` already applies to `/setup`.

- **The state script is the one seam.** The composites and the router had to
  agree about what exists, and a grader had to be able to hold the router's
  words against something. So `scripts/state.py` is a dependency table in the
  loop's order — every command, what it writes, what it needs, its precondition
  in a sentence — and a read of a `research/` folder against it. It is the
  first place the whole loop is written down as data, and the README's loop
  table and the design doc's stage tables were checked against it on first
  contact (§3).

- **`/think` gained `/premortem`.** The plan's list — bits, scout, ideas, rank
  — predates chunk 9, where `/rank` began setting aside every idea without a
  pre-mortem. A composite without it would rank an unattacked set. And the
  pre-mortem is the step nobody runs when it is a separate command, which is
  the step the measured ideation–execution gap is about.

- **One yes per file boundary, and a file that exists gets a question with
  the fact in it.** Rerun, keep or stop — with the file's date, how many
  upstream files are newer than it, and (after §3) how many upstream pages it
  never names. Never a silent skip, which hides that the bits are three weeks
  old; never an unasked rerun, which burns a tournament. Keep is not skip, and
  nothing cascades. The composite states the fact and does not decide it.

- **The brief is printed, never saved.** `/orient` ends in five lines —
  surveys found, cells filled, cells whose query returned nothing, the three
  uncarded papers in `/read`'s own proposal order, the next move — each read
  from a file or the state script. A saved brief would be a fifth landscape
  file with a heading to keep true and a checker to write.

- **The front door opens on natural language.** The router's description
  names the phrases; typing still works. No session-start hook: a hook that
  talks every time you open a project is the kind people disable.

- **"Hooks finalized" means the guard is the final hook set.** The front door
  runs in the main thread, which the guard never sees, so nothing here needed
  a fence change and the guard is untouched — a case added during the build
  was removed at review, because the spec put the guard out of scope. No
  stop-time checker hook — the checkers run in
  seconds and the toolchain says to run them before every commit, and a hook
  on every skill exit would be a second place the rules live. The evidence
  that would justify one is the checkers being forgotten in practice, and
  there is none.

- **Evals for the front door and the loop's typed commands; written, not
  run.** Two or more cases each for router, start, orient, think and the nine
  loop commands: 33 in the suite after the review pass. Each is a full Claude child, so the cost is
  the user's to choose. Every gate case counts `Agent` calls at zero beside
  its rubric, so "waits" is a number. The experiments half has no cases; its
  acceptance is a script.

- **One synthetic fixture, and the reason.** `/rank`'s bound and set-aside
  rule need idea pages and pre-mortems, and no live run produced any.
  `evals/fixtures/selection/` holds six template-shaped ideas and six
  pre-mortems, two `not executable as written`; every file says in its first
  comment that it is invented. Every other shape the assembler builds is a
  copy of a live run's output.

- **Dates on fixtures are set, not inherited.** Git keeps no modification
  times and `cp` gives every file the same minute, so the assembler stamps
  each file in the order it was made, with `BITS.md` before the two newest
  cards. The header of the script says so, and the graders' expected numbers
  cite the state script's output on the assembled folder.

- **`/render` and `/figure` stay planned**; 1.0.0 ships without them, because
  neither gates anyone from walking the loop.

## 2. What the build found

- **The table needed six statuses, not four.** `ready`, `stale`, `done`,
  `blocked` were planned. **`repeat`** appeared on the first fixture: `read`
  with three cards is not done, it adds, and calling it done would have hidden
  the loop's most common move. **`skipped`** appeared on the second: the
  damage fixtures have no `CONTEXT.md` and a full processing stage, and
  without it the recommended move on a folder three stages in was `setup`.
  Skipped required files are repairs, beside the malformed ones.

- **A malformed file satisfies presence.** A hand-written `QUESTION.md` with
  two of eleven headings lets `surveys` run and is listed as a repair with the
  skill that writes it. Treating it as absent would have routed to a rerun of
  `frame` over a file somebody wrote on purpose.

- **Pre-mortems are pending per idea.** A `premortems/` directory with some
  files is not a finished step; `pending.premortem` names the idea slugs
  without one, and `/think`'s boundary question carries that count.

- **The wildfire folder is a fork, not `/read`.** The ticket said it routes to
  `/read`; the script reported `scout` ready at the stage reached and `read`
  ready at the next. The router's rule became: recommended moves at the stage
  reached, stale first, the rest in loop order, cap three, then the first
  ready move of the next stage if there is room.

- **"I want ideas" is not blocked on a folder with a landscape.** The
  matrix's contradictions are a seed source. The precondition-first case is
  "rank my ideas": `rank` blocked on pre-mortems, `premortem` blocked on idea
  pages, walk back to `ideas`. That walk-back is one added line in the
  router's first rule.

- **Two of the loop skills do not refuse where the ticket assumed they
  would.** `/brainstorm` runs unframed by design; `/ideas` reports missing
  seed kinds and never refuses on them. Their cases grade what the skills
  actually promise: saying which mode it is in; and, offline with no index to
  put a candidate to, promoting nothing to a page.

- **The composite cases can only reach the first boundary.** The harness
  answers no questions, so `/start` on an empty folder ends inside setup's
  interview. Its case grades what is reachable — setup ran as the skill,
  frame never did, nothing was framed or previewed — and the pause itself is
  seen live in §3 and at `/think`'s first boundary.

- **The harness drops a case whose `name` carries its directory prefix,
  silently.** Two cases vanished from the listing until the names were fixed.
  And a directory count taken with a filter meant to exclude the `read/` and
  `landscape/` run folders excluded the `read-*` and `landscape-*` cases too:
  the documents said 27 for a while; the harness's 32 was right.

## 3. What the live runs found

Both runs are on a project folder the assembler built from the damage
fixtures: question, landscape, three cards, datasets, groups, `BITS.md`, one
critique, no `CONTEXT.md`. As in the landscape and read evals, the skills were
run from the repo rather than from an installed plugin, so the router and
`/think` were followed as written in the main thread; the state read, the
brief and the questions are the real ones.

**`/router`.** The state script reported `stage_reached: processing`; nine
present files; three cards, newest 2026-09-16 11:45; `BITS.md` dated 11:30
with `upstream_newer: 2`; one repair, `CONTEXT.md` missing upstream, setup
writes it. Moves at the stage reached: read `repeat`, datasets `done`, groups
`done`, bits `stale`, brainstorm `ready`, ideas `ready`. `recommended` in
full: scout, read, bits, brainstorm, ideas, baseline. The router's rule —
stale first, then loop order, cap three — offered **bits, read, brainstorm**,
each with its status and reason, and asked once. That matches what the script
printed. Two things it hid:

- **`ideas` was cut by the cap, `brainstorm` kept**, because the table lists
  brainstorm first. Defensible — bits is stale, so ideas should wait — and
  noted as the first thing to change if it reads wrong in use.
- **`scout` and `baseline`, ready at other stages, appeared nowhere.** Fixed
  in the run: the brief gained an **Also open** line carrying every
  recommended move the offer did not, with its status, so an unrun `/scout`
  is visible without being the next move.

**`/think` to its first pause.** The first step is `bits`; its move was
`stale`, so the first thing the composite did was ask:

> `BITS.md` exists, dated 2026-09-16 11:30. Two cards are newer than it by
> date — `gupta-2020-rescuenet`, `shen-2021-bdanet`, newest 11:45. Rerun,
> keep, or stop?

The count was right by construction: the scaffold set those dates. And it was
**misleading**, which is the finding. That `BITS.md` names all three cards
under `## Groups` — it was written after reading them, and the critique that
found it wrong was about its wording, not its coverage. A date is a proxy for
"drew on", and here the proxy said stale about a file that was current. Fixed
in the run: the state script now reports **`not_named`** beside the date
count — the upstream pages the derived file never mentions — and the shared
rules, `/think` and the router's brief carry both, saying they can disagree.
On the live folder: two newer by date, zero not named. The selftest gained the
case where the two disagree the other way. The answer given was stop; the
brief printed with `/bits` and `/ideas` as the moves the router would offer,
and nothing past the first pause ran.

**The three tables agree.** The README's loop table (with `/read` as its own
step before `/think`), the design doc's stage tables, and the state script's
dependency table name the same commands in the same order. The one divergence
is deliberate and written down: `/think` carries `/premortem`, and the design
doc's Composites row says why.

## 4. What the review found

Two axes, standards and spec, over the nine commits. Standards found no hard
breach and six smells; spec found thirteen. What was fixed:

- **`/datasets` and `/groups` were loop rows.** The spec's story 11 names
  them on-demand, and the table's first draft had them as steps, so with one
  card and no ledger the router would have offered a ledger as the next move.
  They are on-demand rows now, in the table, the router's list and the
  glossary. A ledger is asked for; it is never the next step.
- **`skipped` was a stage rule and needed to be a row rule.** A question page
  beside a missing context file sits in one stage, so setup was `ready` there
  rather than a repair. It is now "absent while any later step has output".
  The router case the spec asked for and the build skipped — framed, no
  landscape — exists on the `question-only` shape and names `/surveys`.
- **The graders' numbers had nothing holding them.** The harness cannot run
  the state script inside a grader, so the numbers were copied by hand. A
  mechanical check, `evals/fixtures/check_cases.py`, assembles every shape,
  reads it with the state script and asserts each fact a grader quotes; it
  runs in the static-checks verb, so a table change that drifts a rubric fails
  before commit.
- **The guard case was out of scope** and is removed; the note's decision
  record said the opposite and now does not.
- **Bash was scoped to any `python3`**, not to the plugin script. All four
  skills now allow `python3 *scripts/state.py*` and nothing else.
- Counts corrected where they drifted (the router said thirty commands; the
  toolchain's prose omitted the state selftest), two ticket resolutions
  written that were missing, three small duplications in the state script
  removed.

What was left as it stands, and why: the router's three-candidate rule
(disclosed in §3; the cap is a guess the next live run tests); the composite
cases grading the reachable half of the pause (the harness answers nothing);
`/orient`'s five lines layered on the router's brief rather than one routine
(the router has no landscape to summarise on most folders); the synthetic
selection fixture (the spec said copy, `/rank` cannot be graded without idea
pages, and every file says it is invented); the `checklib` import beside
"standard library only" (the checkers' own precedent).

## 5. What is open

- **No case has been run.** Thirty-three are written and parse at a zero cost
  ceiling. The first real run will find grader wording that does not survive
  contact with a transcript; the fixtures README says where each expected
  number came from so the graders can be corrected rather than argued with.

- **The router and the composites have not been run from an installed
  plugin.** The live runs followed the skills as written from the repo. The
  Skill tool invocation of a plugin skill from inside another plugin skill —
  `research-bearings:setup` called from `/start` — is the mechanism this
  chunk rests on, and it has been read, not exercised.

- **The state script's date proxy.** `not_named` fixes it for files that name
  their sources by slug. `QUESTION.md` against `CONTEXT.md`, or the matrix
  against the surveys file, have no slug to look for, and there the date is
  all there is.

- **The cap that cut `ideas`.** Three at the stage reached is a guess about
  how many options a person reads. If it reads wrong, the cheap change is to
  rank `ready` moves that follow a `stale` one below it rather than by loop
  order.

- **`/render` and `/figure`.** Planned, the next point release, and the only
  rows in the design doc not built.
