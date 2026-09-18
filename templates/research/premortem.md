# Pre-mortem: <the idea's title>

<!-- One pre-mortem, at research/premortems/<slug>-<date>.md. Eight headings,
     fixed. Written by research-bearings:premortem-agent, one per idea, in a
     fresh context that did not generate the idea.

     It is its own file and not a section of the idea page. A judge does not
     rewrite what it judges, and chunk 8's nine idea headings are a shipped
     contract three skills read.

     This is what /rank reads to set an idea aside, and what /design reads to
     refuse one. They read it by heading, so a missing heading is a downstream
     skill reading nothing and believing it found nothing.

     It judges EXECUTION. Not novelty — that was settled at /ideas by
     retrieval. Not interest — that is the tournament's job. The measured
     failure this exists to catch is the one from the 43-researcher study:
     ideas that lost 1.88 of 10 on effectiveness once executed, for missing
     baselines, inappropriate metrics, and evaluation plans nobody could
     run. -->

## The idea, restated

<!-- The idea in the agent's own words, in two or three sentences, without
     looking back at the page's phrasing while writing them.

     This heading exists so a misreading is visible. If the restatement is not
     the idea, nothing below it is about the idea, and the researcher can see
     that in ten seconds. Do not improve the idea here. Restate it. -->

## Baselines it must beat

<!-- One line per baseline, each with its state:

     - <baseline> — exists and runs: <the card or repo that says so>
     - <baseline> — exists, unknown whether it runs: <what was checked>
     - <baseline> — named in no file I was given: <what was checked>

     "Missing baselines" is the first of the three measured causes. A baseline
     nobody can run is the same as no baseline, three months later.

     The strongest published number in the area belongs here even when the idea
     does not mention it, because that is what a reviewer will compare against.
     Where the cards give a number, quote it with the card and the table. -->

## The field's metric

<!-- What this field actually reports, taken from the cards and QUESTION.md,
     and whether the idea's evaluation uses it:

     - The field reports: <metric>, from <file> (<how many cards report it>)
     - The idea evaluates on: <metric, from the idea page>
     - They agree / they do not agree, because: <one line>

     "Inappropriate metrics" is the second measured cause. An idea scored on a
     metric nobody in the field reports cannot be compared to anything, and
     that is discovered at submission. -->

## The evaluation plan, and what it depends on

<!-- What would have to happen for this idea's results to exist, and what each
     step needs. One line per dependency, and any of these is a BLOCKER, named
     as one:

     - a human evaluation or annotation campaign the researcher will not run
     - hardware, data or access they do not have
     - a dataset whose licence or split protocol forbids the use
     - a number that only exists if somebody else's code runs

     "Evaluation plans nobody could run" is the third measured cause.

     Where CONTEXT.md states the compute and the time, judge against those and
     say so. Where it does not, write `constraint unknown` and name what was
     assumed. Never assume a cluster. -->

## What would have to be true that probably is not

<!-- The load-bearing assumptions, one per line, each with why it is doubted
     and what it would cost to check:

     - <assumption> — doubted because <the line, from the file it is in>;
       checkable by <how>, roughly <cost>

     The idea page has its own assumptions section written by the generator.
     This one is written by something that did not want the idea to work.
     Overlap is fine; agreement is not required. -->

## Verdict

<!-- Exactly three states. The first line is read by /rank and /design, so it
     is this shape and nothing else:

     - Verdict: executable
     - Verdict: executable with changes
     - Verdict: not executable as written

     Then, below it:

     For `executable with changes`: the changes, numbered, each one a thing the
     researcher would do differently — not a wish for more information.
     For `not executable as written`: the single blocker, named, and which
     heading above it came from.

     Judged as if this will be EXECUTED, not reviewed. The question is not
     "would this be accepted" but "would three months of this produce a
     number". -->

## What would change the verdict

<!-- One or two lines. What fact, if learned, moves this idea between states —
     a baseline's code turning out to run, a dataset turning out to be
     licensed, a metric turning out to be reported after all.

     This is the heading that keeps the verdict arguable. A verdict with
     nothing that could change it is a judgement nobody can check. -->

## Status

<!-- Date. Which files were read, by path. What was NOT available and what was
     concluded without it. Any `constraint unknown` from the evaluation
     heading, repeated here so the researcher sees it without reading the whole
     file.

     Written 2026-09-20 by premortem-agent. Read: research/ideas/<slug>.md,
     research/QUESTION.md, research/CONTEXT.md, 3 cards. No datasets ledger:
     licence state unchecked for 1 dataset. -->
