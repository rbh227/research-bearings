---
name: frame
description: Turn a research topic into a question worth answering. Diverges into candidate framings, converges with Booth's ladder and the Heilmeier eight, then has a fresh-context critic attack whatever survives. Use when starting a new research direction, when a question feels vague or unfalsifiable, or when re-entering after a survey has changed what you know. Writes research/QUESTION.md.
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, Agent
---

# frame

One job: produce a research question worth answering. Two output files, because
the answer and the wreckage are different things.

This is **not** an interrogation of a question the user already has. A framing
session's most valuable possible output is *you are asking the wrong question*,
and a skill that only sharpens can never say it. So the loop diverges before it
converges, every time, including on re-entry.

## Precondition

`research/CONTEXT.md` must exist. If it does not: name the missing file, say
`/research-bearings:setup` writes it, and **stop there**.

That is a hard phase fence. Do not interview the user for setup content, and do
not be helpful about it either — no list of what setup will ask, no "meanwhile,
worth thinking about", no preview of the questions. Setup opens by checking the
machine, and a preview written here is guesswork that pre-loads answers before
anything has been measured. Two sentences and stop.

## The loop

**1. Read, then make sure the log exists.** Read `research/CONTEXT.md` in full.
If `research/QUESTION.md` and `research/framing-log.md` exist, read those too —
this is a re-entry, and the rejected framings tell you what has already been
ruled out. **Never ask for anything `CONTEXT.md` already answers.**

If `research/framing-log.md` does **not** exist, copy
`${CLAUDE_PLUGIN_ROOT}/templates/research/framing-log.md` to it now, before
anything writes to it. Step 2 appends to that file, and an append to a file that
was never created produces a log without its three headings — which breaks
re-entry, because the next run reads those headings to learn what has already
been ruled out. If the file does exist, append only; never overwrite it.

**2. Diverge.** Put three to six candidate framings on the table. Generate them
by applying Polya's transformations to the user's topic:

- solve a related easier problem
- drop a constraint
- add a constraint
- vary the goal
- work backwards from the desired end state
- generalize
- specialize

Then ask Hamming's question of the area: what are the important problems here,
and why is the user not working on one of them?

**Mark every candidate as an uninformed guess.** Say it plainly in the message:
you have searched nothing, read nothing, and these are shapes a question could
take, not knowledge of what the field has asked. On a re-entry after `/surveys`,
say instead which surveyed material each candidate came from.

Append all candidates to `research/framing-log.md` before going further.

**3. Converge.** Take each candidate down Booth's ladder:

- **Topic → question → problem.** A topic statable in four or five words is
  still a topic. Narrow it by adding words, especially nouns made from verbs.
- **Condition and consequence.** What is true now, and what does it cost that
  nobody knows the answer?
- **The so-what recursion.** Ask "so what?" of that consequence. Then of the
  answer. Keep going until you reach a named person or role making a decision,
  or until you run out — which means it was a topic all along.

Kill any candidate whose ladder terminates on "advances the field", "is
interesting", or an unnamed audience. Record each death in `framing-log.md`
under `## Rejected framings` with the round and the cause.

**4. Repeat 2 and 3** from what survived, until exactly one framing stands. If
everything dies, say so and diverge again from a different transformation —
that is a successful round, not a failure.

**5. Fill.** Copy `${CLAUDE_PLUGIN_ROOT}/templates/research/QUESTION.md` to
`research/QUESTION.md` if it does not exist, then fill the headings. Cost and
time come from `CONTEXT.md`'s Compute and Constraints sections — if the
allocation there is `_unknown_`, so is the cost. Any heading you cannot fill is
left empty and named under `## Status`.

**6. Critique.** Dispatch `research-bearings:question-critic` through the
`Agent` tool with `subagent_type: "research-bearings:question-critic"`. Give it
the paths to `research/QUESTION.md` and `research/CONTEXT.md` and nothing else.
**Do not send it this loop's reasoning, the rejected candidates, or which parts
you found hard.** The separation is the mechanism.

**7. Adjudicate, one finding at a time.** Worst first. Put the finding to the
user and take their response. Then **dispatch `question-critic` a second time**
— a separate call, not a continuation — carrying exactly:

- the path to `research/QUESTION.md`
- the finding, quoted as the critic wrote it
- the user's rebuttal, **verbatim**
- the tally so far: how many findings there are in total, how many you have
  already adjudicated, how many of those were conceded, and whether the
  immediately previous one was a concession

The critic runs in a fresh context and remembers nothing between calls, so
anything you leave out of that payload it cannot use. The tally is the only
reason it can apply "never concede twice in a row" and "flag if more than half
were conceded" — omit it and both rules silently stop working.

**Take the score and the verdict from the critic's reply. Never assign either
yourself.** You wrote the page; scoring the defence of it is precisely the
judgement the separation of contexts exists to prevent. Do not tidy, shorten or
strengthen the user's rebuttal on its way to the critic — send what they said.

Record under `## Critique` in `framing-log.md`: the finding, the rebuttal, the
score, and whether it stood. Where a finding stood, revise `QUESTION.md` and log
the change under `## Revisions` with the date.

If the critic's last reply reports that it conceded on more than half the
findings, pass that on to the user. It means the question has not actually been
tested.

## Outputs

`research/QUESTION.md` is the deliverable and the only file downstream skills
read. Eleven fixed headings, in this order:

`## Question` · `## The ladder` · `## Who decides` · `## Today` ·
`## What's new` · `## Risks` · `## Cost and time` · `## Checkpoints` ·
`## Why you` · `## Vocabulary` · `## Status`

`research/framing-log.md` is the working record. Three headings:

`## Rejected framings` · `## Critique` · `## Revisions`

It grows across re-entries. Nothing reads it automatically; it exists for the
user, and for later ideation work that mines abandoned directions.

## Stop condition

Exactly one framing stands. Every heading in `QUESTION.md` is filled or named
under `## Status`. The so-what ladder terminates on a named person or role
making a named decision. The critic has run, and every finding is either
addressed or recorded with its rebuttal and score.

This file is never sealed. When `/surveys` later shows what the field actually
asks, run this skill again.

## Rules this skill applies

**Booth's ladder.** Topic → question → problem; the X/Y/Z sentence; the
recursive so-what, terminating on a named audience.
— `academic.md` § How research actually works

**The Heilmeier eight** are the fixed headings, not a checklist to recite.
— same

**Hamming.** What are the important problems, and why are you not working on
one? — same

**Wagstaff.** The metric ties to a decision someone makes. — same

**Polya.** The transformation bank is what divergence runs on. — same

**Abstention beats a guess.** An empty heading named under `## Status` is
better than plausible filler. — `academic.md` § Keeping agents honest

**The generator never judges.** The critic runs in a separate context and never
sees how the page was made. — same

## Refusals

| The shortcut | Why you don't |
|---|---|
| "This question is basically fine already." | Then walk the ladder. The rung where it stops *is* the finding. |
| "The audience is the research community." | Not an audience. Name a person or a role who makes a call. |
| "I'll fill the thin headings with plausible text." | A blank heading is a blank heading. Name it under `## Status`. |
| "I know this area well enough to call that novel." | You have searched nothing. Divergence is labelled uninformed, always. |
| "The critic agreed, so we're done." | Check the scores. Conceding on more than half is a flag, not a pass. |
| "One good framing is enough, skip divergence." | The point of diverging is discovering the first framing was wrong. Three minimum. |
| "Cost and time — I'll estimate from experience." | Read `CONTEXT.md`. If the allocation is `_unknown_`, so is the cost. |
| "The user seems attached to this framing." | Attachment is not evidence. Run the ladder on it like any other candidate. |
| "I'll send the critic my reasoning so it has context." | That reasoning is precisely what it must not see. |
| "That rebuttal was obviously weak, I'll score it a 2 myself." | You are the generator. Re-dispatch the critic and use its score. |
| "The critic already saw this finding, no need to resend it." | Fresh context every call. It remembers nothing. Quote the finding back. |
| "I'll clean up the user's rebuttal before passing it on." | Send it verbatim. Tidying it is arguing on their behalf. |
| "The log doesn't exist yet, I'll just start writing to it." | Copy the template first, or it ends up with no headings and re-entry breaks. |
| "No CONTEXT.md, but I'll list what setup will ask so they're prepared." | No. Name the file, name the skill, stop. That list is setup's job and your guesswork. |
