# Chunk 10: the front door

**Status:** ready-for-agent
**Milestone:** 6 of the build plan (`research_plugin_build_plan.md` § Milestone 6), the last one.
**Date:** 2026-09-18
**Layer under this one:** every chunk. The front door reads the files the other
27 skills write and invokes those skills; it writes nothing under `research/`
itself. `docs/design/chunk-09-selection.md` is the layer immediately beneath,
because `/think` ends in the selection half it shipped.

Grilled one question at a time on 2026-09-18, twelve questions, and approved
as one chunk. The milestone was planned in the build plan and in
`docs/design/skills-and-agents.md` § Composites; this spec follows that plan
except for `/think`'s composition, which predates chunk 9 and had to change.
The chunk note `docs/design/chunk-10-front-door.md` is written by the last
ticket.

## Decisions settled at planning

Each can be reopened by editing this section before `/to-tickets`.

1. **`/router` is the doorman.** It reads the state of `research/`, names the
   one command that comes next and the precondition it checked, asks once,
   and on yes invokes that skill in the same thread. Never a signpost that
   only points; never a chauffeur that drives without asking.
2. **At a fork it offers the fork.** When more than one command is valid it
   lists two or three, each with its one-line reason, and the user picks.
3. **A stated goal is routed to, but the precondition comes first.** "I want
   ideas" with two cards and no `BITS.md` gets the precondition, the nearest
   step, and the offer to run that instead. The router never sends the user
   to a skill it can see will refuse them.
4. **`/start` is `/setup` then `/frame`. `/orient` is `/surveys` then
   `/landscape`. `/think` is `/bits`, `/scout`, `/ideas`, `/premortem`,
   `/rank`.** The plan's `/think` list lacked `/premortem`; since chunk 9
   `/rank` sets aside any idea without one, so a composite that skipped it
   would rank an unattacked set. Added.
5. **A composite pauses at every file boundary with one yes**, and adds no
   pause inside a skill beyond the ones the skill already has. After `/setup`
   writes `CONTEXT.md` the composite shows the file's summary and asks whether
   to frame now. The user can stop at any boundary and come back.
6. **An output that already exists is asked about, and the question carries
   the staleness fact.** "`BITS.md` exists, dated the 11th, six cards read
   since. Rerun, keep, or stop?" One question per existing file. Never a
   silent skip and never an unasked rerun.
7. **`/orient` ends in a one-screen printed brief**, not a file: surveys
   found, matrix cells filled, cells whose query came back empty, the three
   papers the matrix ranked highest, and the next move. The router prints the
   same brief. One routine serves both.
8. **The front door opens on natural language.** The router's description is
   written so that Claude reaches for it on "what next", "where am I", "what
   should I do with this project" in a project with a `research/` folder.
   Typing `/research-bearings:router` still works. No session-start hook.
9. **"Hooks finalized" means the guard is declared final.** No stop-time
   checker hook, no session-start brief. The chunk note records why, and the
   build plan's line is closed.
10. **Evals: the four new skills, plus two cases each for the nine typed loop
    commands.** Written in this chunk, run by hand when the user chooses. Not
    the experiments half, whose acceptance is a script, and not the on-demand
    skills.
11. **README: front door first.** After the install block, one line says to
    type the router. The loop table carries `/start`, `/orient`, `/think` as
    the one command per stage with the typed commands under each. Every count
    is corrected. The document keeps its shape; nothing moves to `docs/`.
12. **Version 1.0.0.** `/render` and `/figure` stay planned and come as a
    point release.
13. **Acceptance is static plus two live runs**: `/router` against a populated
    research folder, and `/think` on the same folder to its first pause. Both
    recorded in the chunk note.
14. **One new seam: a state script.** The read of `research/` that the router
    and the composites need — what exists, how stale it is, what comes next —
    is a plugin script with a selftest, so the numbers come from one place
    and a grader can check the router's words against them. (Settled at the
    seam check, after the grill.)

**A fact found while writing this spec, which changes where decision 13
runs.** This repo's own `research/` folder holds only the paper cache; every
markdown file a live run produced lives under the eval run folders. The damage
topic is the only one with a question page, a landscape, three cards and a
`BITS.md`. The two live runs therefore go against a project folder assembled
from those fixtures, which is also what the eval scaffold builds. On that
folder `/think`'s first pause is the `BITS.md` question from decision 6, which
is the behaviour the run exists to see.

## Problem Statement

The plugin has 23 skills and every one of them has to be known by name. A new
person installs it, reads a README that lists nine typed commands and 23
skills, and has to work out from the file layout which command is next, what
that command needs to exist first, and whether the file it would build on is
stale. The loop's three stages each take two to five commands in an order the
README describes in prose. The step people skip when it is a separate command,
the pre-mortem, is the step the measured ideation-execution gap is about.

Under that: the README's counts are wrong, the front door it promises is marked
planned, the behavioural evals cover three skills, and the build plan's last
milestone is the only unbuilt one.

## Solution

Four skills in the main thread, one script, no agents.

**`/router`** reads the state of `research/` through the state script, prints
the one-screen brief, and names the next command with the precondition it
checked. At a fork it offers the options. Given a goal it cannot yet meet, it
names what is missing and the nearest step. It asks once and invokes on yes.
It fires on natural language as well as by name.

**`/start`, `/orient`, `/think`** each run a fixed sequence of existing skills
in this thread, pausing at every file boundary with one yes, asking rerun,
keep or stop at any output that already exists with the staleness fact in the
question, and ending with the brief and the next move. They add nothing to any
skill they run and write nothing themselves.

**The state script** is a pure function of a directory: which contract files
exist, their dates, counts (cards, ideas, pre-mortems, results), which
upstream files are newer than each derived file, and the ordered list of
commands whose preconditions are met, each with the precondition named. JSON
on stdout, standard library only, selftest over fixture folders.

Around them: the guard declared final; eval cases for the four skills and the
nine loop commands; a README with the front door first and its counts
corrected; the design doc, glossary, build plan and manifest brought current;
version 1.0.0; a chunk note carrying the two live runs.

## User Stories

### The router

1. As a new user, I want to type one command and be told what to do next, so that I do not have to learn 27 names before the plugin is useful.
2. As a user, I want the router to name the precondition it checked alongside the command, so that I can see why it chose what it chose and disagree with the evidence rather than the conclusion.
3. As a user, I want the router to ask once before it runs anything, so that a look at where I am never turns into a run I did not ask for.
4. As a user, I want the router to run the skill in this same thread when I say yes, so that I do not retype the command it just named.
5. As a user, I want the router to offer two or three options when more than one command is valid, each with its reason, so that a genuine fork is mine to take.
6. As a user, I want to state a goal in my own words and have the router route to it, so that "I want ideas" works without my knowing `/ideas` exists.
7. As a user, I want the router to tell me when my stated goal's skill would refuse me, and name the nearest step instead, so that I never get sent to a skill that stops on its first line.
8. As a user, I want the router to reach for itself when I say "what next" or "where am I" in a project with a `research/` folder, so that the front door is a sentence rather than a name.
9. As a user, I want the router to print a one-screen brief of what exists before naming the next move, so that the recommendation lands with its context.
10. As a user with no `research/` folder at all, I want the router to name `/start`, so that the empty state has one obvious move.
11. As a user, I want the router to name the on-demand skills (`/verify`, `/audit`, `/critique`, `/reviews`, `/datasets`, `/groups`, `/replicate`) only when my stated goal calls for one, so that the loop's next step is never buried under seven side doors.
12. As a user, I want a router that writes nothing under `research/`, so that asking where I am never changes where I am.

### The composites

13. As a new user, I want `/start` to take me from an empty folder to a framed question in one sitting, so that day one is one command.
14. As a user, I want `/start` to show me the context file's summary after setup and ask before framing, so that what setup found about my compute and data can change what I frame.
15. As a user, I want `/orient` to run surveys then the landscape and end with a brief, so that the gathering stage is one command and I know what it found.
16. As a user, I want `/think` to run bits, scout, ideas, pre-mortem and rank, so that the path from assumptions to a ranked shortlist is one command.
17. As a user, I want `/think` to include the pre-mortem, so that the step I would skip when it is separate is the step I cannot skip by accident.
18. As a user, I want every composite to pause at each file boundary with one yes, so that I can stop after any step and come back, and no step runs that I did not agree to.
19. As a user, I want composites to add no pause inside a skill beyond the ones the skill already has, so that a composite is exactly the skills it names and nothing else.
20. As a user re-entering, I want a composite to ask rerun, keep or stop at every output that already exists, so that a stale file is neither silently reused nor silently rebuilt.
21. As a user re-entering, I want that question to carry the staleness fact, such as how many cards were read since the file's date, so that the decision is easy and the evidence is in front of me.
22. As a user, I want a composite to stop when a skill it runs stops, so that a precondition failure inside `/frame` ends `/start` with that skill's message rather than with a half-run.
23. As a user, I want the composite to end by printing the brief and naming the next move, so that each stage hands me to the next one.
24. As a user, I want `/orient` to write no file of its own, so that there is no fifth landscape file to maintain and check.
25. As a user, I want to pass a slug or a flag through a composite to the skill that takes it, so that `/think` on a named problem behaves like `/scout` on that problem.
26. As a user, I want a composite that finishes to say which files it made and which it kept, so that the run's effect on `research/` is one list.

### The state read

27. As a user, I want one script that says what exists under `research/`, so that the router, the composites and I are all reading the same facts.
28. As a user, I want the script to report which upstream files are newer than each derived file, so that staleness is a count and a date rather than a feeling.
29. As a user, I want the script to list every command whose preconditions are met, in the loop's order, with each precondition named, so that the router's recommendation is a lookup and not an opinion.
30. As a user, I want the script to report a file that exists but has a missing required heading as present-but-malformed rather than absent, so that a half-written file is routed to as a repair, not overwritten by a rerun.
31. As a user, I want the script to never write anywhere, so that asking about the state cannot change it.
32. As a user, I want the script to run on a folder I name, not only the current project, so that the eval scaffold and the chunk's live run can point it at fixtures.
33. As a developer, I want the script to have a selftest over fixture folders, so that a change to the routing table is caught in seconds.

### Evals

34. As a developer, I want eval cases for the router in at least three states — empty, framed with no landscape, and cards with a stale bits file — so that the routing table is tested at the seam where a person meets it.
35. As a developer, I want a router case where the stated goal cannot be met, so that the precondition-first behaviour is graded.
36. As a developer, I want a case per composite that proves it pauses at the first file boundary, so that the one-yes rule is graded rather than assumed.
37. As a developer, I want a case where a composite meets an existing output and asks with the staleness fact, so that the re-entry rule is graded.
38. As a developer, I want two cases each for the nine typed loop commands, so that a reader of the README finds a case for every command it names.
39. As a developer, I want the router graders to check the router's words against the state script's output for the same folder, so that a router that invents a state fails.
40. As a developer, I want a scaffold that assembles the damage fixtures into a temp project, so that cases needing a populated folder run against a real one.
41. As a user, I want the cases written but not run in the build, so that the chunk's cost is mine to choose.

### Docs, hooks, release

42. As a new user, I want the README to tell me, right after install, to type the router, so that the first thing I read is the first thing I do.
43. As a new user, I want the loop table to show one command per stage with the typed commands under it, so that the composites and the parts they run are visible together.
44. As a reader, I want every count in the README, the design doc and the glossary to be correct, so that the documents are trustworthy about the plugin they describe.
45. As a developer, I want the chunk note to say why the guard is the final hook set, so that the build plan's line is closed with a reason and not a shrug.
46. As a user, I want the plugin at 1.0.0 when the front door lands, so that the version says what the README says: a person who did not build it can use it.
47. As a developer, I want the two live runs recorded in the chunk note with what the router said and whether it was right, so that the first contact with real files is on the record.

## Implementation Decisions

### What the front door is not

- **No agents.** All four skills run in the main thread. The design doc says
  the composites serve the "simple to use" goal and need no sheet source;
  they also need no fresh context, because they judge nothing.
- **Nothing written under `research/`.** The router and the composites write
  no file. The brief is printed. No new template, no registry entry, no new
  checker for a file that does not exist.
- **The guard does not move.** The main thread is not an agent and passes
  through the guard untouched; the composites and the router run there. The
  guard selftest gains no cases for this chunk, and the chunk note says so.

### The state script

- Standard library only, JSON on stdout, in the shape of the other plugin
  scripts: a module docstring saying what each field is for, a `main()` over
  one directory path (default: the project's `research/`), and `--selftest`.
- **A dependency table is the whole program.** One table, in the loop's
  order, from contract file to the skill that writes it, the files it reads,
  and the precondition in one sentence. The router's recommendation is the
  first row whose inputs exist and whose output does not, and the fork is
  every such row at the same stage. The table is the single source of truth
  and the skills quote it, never restate it.
- Reports, per contract file: present or absent; date; for a present file,
  whether its template's required headings are all there (present-but-
  malformed otherwise); for a derived file, the count and newest date of
  upstream files newer than it. Counts for the directory-shaped outputs:
  cards, analog pages, idea pages, pre-mortems, experiment pages, results.
- Reports the next moves: every command whose preconditions are met, in
  order, each with the precondition named and whether its output already
  exists. The router and the composites read this list and nothing else.
- **Never writes.** The selftest snapshots the fixture tree before and after,
  as the run ingester's does.
- **Never guesses.** A file whose date cannot be read reports `unknown`, and
  a folder with no `research/` reports the empty state, which routes to
  `/start`.

### `/router`

- Skill in the main thread: Read, Glob, Bash scoped to the plugin script,
  AskUserQuestion, Skill.
- Description written for the natural-language trigger: it names the phrases
  ("what next", "where am I", "what should I do") and the condition (a
  `research/` folder in the project). Typed invocation unchanged.
- Runs the state script, prints the brief, then applies three rules in order:
  a stated goal is matched to a skill and its precondition checked; a single
  next move is named with its precondition; a fork is offered as two or three
  options with one reason each. One AskUserQuestion. On yes, invokes the
  chosen skill through the Skill tool, passing through any argument the user
  gave.
- **A goal that cannot be met gets the precondition first.** The message
  names the missing file, the skill that writes it, and offers that skill.
  It does not list what the refusing skill would have asked, which is the
  same rule `/frame` applies to `/setup`.
- The on-demand skills are reachable only by stated goal. The loop's next
  move never names them.
- Reports nothing under `research/`; its whole output is what it prints.

### The composites

- Three skills in the main thread: Read, Glob, Bash scoped to the plugin
  script, AskUserQuestion, Skill. Each is a sequence and a set of rules,
  under 150 lines, and the rules are the same in all three.
- **The sequence is fixed and written in the skill**: `/start` = setup,
  frame; `/orient` = surveys, landscape; `/think` = bits, scout, ideas,
  premortem, rank.
- **Before each step, the state script is run**, and:
  - if the step's output does not exist, the composite asks the one-yes
    question at the boundary (the first step needs no yes: typing the
    composite was it);
  - if the output exists, the composite asks rerun, keep or stop, and the
    question carries the file's date and the upstream-newer count from the
    script;
  - if the step's precondition is not met, the composite says so in the
    skill's own words and stops, as that skill would have.
- **A step is the skill, invoked through the Skill tool**, with any argument
  the user gave the composite passed to the step that takes it. The composite
  adds no interview, no summary and no pause inside the step.
- **Stop means stop.** A skill that refuses, a user who says stop, or a keep
  on a file that a later step needs — all end the composite with the brief
  and the next move named. Keep is not skip: a kept file is read by the next
  step as it stands.
- **The brief at the end** is the router's brief, printed by the same
  routine: what exists, what was made or kept this run, and the next move.
- `/start`'s boundary after setup shows the context file's summary — the
  headings and one line each — before asking whether to frame.

### Evals

- Cases live beside the existing ones, one directory each, prompt plus
  graders, in the existing case shape. Router cases and composite cases
  declare a scaffold that copies the damage fixtures into the temp project's
  `research/` folder; the scaffold is a short shell script the case names,
  run only with the harness's scaffold flag, which is why the cases are
  written and not run.
- Router cases: empty project; framed with no landscape; the damage folder
  (cards, landscape, stale bits) where the answer is a fork; a stated goal
  that cannot be met. Composite cases: `/start` on an empty project pauses
  after setup; `/orient` on a framed project pauses after surveys; `/think`
  on the damage folder asks about the existing bits file with the staleness
  fact.
- Loop-command cases: two each for setup, frame, surveys, landscape, scout,
  read, brainstorm, ideas, rank. Where a case already exists for the skill,
  it counts; new cases fill to two. Each grades one behaviour the skill's
  description promises, at the transcript level, and never an implementation
  detail.
- Router graders compare the transcript's named command against the state
  script's next-moves list for the same fixture, so the check is against a
  fact, not a grader's opinion of what should come next.

### Docs, manifest, version

- README: the front-door line after install; the loop table rewritten with
  the composites as the one command per stage; the skills list gains the four
  as built; the layout block lists every skill, agent and script; the counts
  everywhere match the tree. The design doc's Composites section gets the
  built marks and the `/think` change; its count line is corrected. The
  glossary gains a front-door section: router, composite, file boundary,
  staleness fact, brief, state script. The build plan's Milestone 6 status is
  rewritten. Manifest to 1.0.0. Chunk note last, carrying the two live runs.

## Testing Decisions

Static plus two live runs. What ships:

- **The state script's selftest** against fixture folders built in a temp
  dir: empty; context only; framed; framed with a landscape; the damage shape
  (cards, landscape, bits older than the cards); a present-but-malformed file;
  a folder with an unreadable date. Asserts the JSON shape, the next-moves
  list and the staleness counts, never internals. Asserts no write.
- **The headings check** is unchanged: no new template, and the check must
  still pass with four skills that name no template.
- **The plugin validator** over the four new skill files, because the
  natural-language description and the Skill tool in the allowlist are the
  two things a validator can reject.
- **The eval cases exist and parse** — the harness lists them — and are not
  run in the build.
- **Two live runs**, by the last ticket, against a project folder assembled
  from the damage fixtures: `/router`, and `/think` to its first pause. What
  each printed goes in the chunk note beside whether it was right.

A good test here reads the printed words or the JSON and never the prose of a
skill file. Prior art: the run ingester's selftest for fixture trees and the
no-write snapshot; the frame cases for graders that check a skill stopped where
it should.

## Out of Scope

- `/render` and `/figure`. Planned, and the next point release.
- Any new hook: no stop-time checker, no session-start brief.
- Running the eval cases. Written, listed, left to the user.
- Any change to a skill the composites run, or to a template, a checker or
  the guard. A composite that needs one is a finding for the chunk note, not
  a change.
- A file under `research/` for the brief. Printed only.
- Re-running a composite's later steps automatically after a rerun of an
  earlier one. Each boundary asks; nothing cascades.
- The experiments-half commands in the router's loop order beyond naming
  `/spec`, `/baseline`, `/design`, `/log`, `/result` when their preconditions
  are met. No composite covers them; the human gates there are the point.

## Further Notes

- The dependency table in the state script is the first place the plugin's
  whole loop is written down as data. The README's loop table and the design
  doc's stage tables should agree with it, and the chunk note should say
  whether they did on first contact.
- `/think` on the damage fixtures will ask about a `BITS.md` that a critique
  already found wrong (see the chunk 8 note). That is the right first pause:
  the staleness fact and the critique are both reasons to rerun, and the
  composite should be seen to offer the choice rather than make it.
- The wildfire fixtures have a question and a landscape and no cards, which
  makes them the "framed with a landscape" router case, and the damage
  fixtures the fork case. Both fixture sets already exist; the scaffold copies
  and does not invent.
