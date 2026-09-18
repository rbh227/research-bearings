# Baseline: <the paper, as a short title>

<!-- One baseline, at research/baselines/<card-slug>.md. Seven headings, fixed.
     Written by research-bearings:baseline-reproducer from a paper card, the
     fetched full text, the datasets ledger row, and the researcher's own code
     and data description.

     Two skills write this file and they mean different things by it:

     /baseline    a number you intend to BEAT. The gap is a fact about your
                  reproduction of somebody else's work.
     /replicate   a paper you are NOT building on, run as a calibration test.
                  The gap is a fact about YOUR PIPELINE, and the file says so.

     Nothing here is executed by an agent. The plan is written, the researcher
     runs it, and the skill records what came back. That is not a limitation
     working around the guard — it is the reason "whether to spend compute" is
     a human gate. -->

## The published number

<!-- The exact number this is trying to hit, with where it came from:

     - Number: <value> <metric>, on <dataset and split>
     - From: research/papers/<slug>.md § <heading>, Table <n>
     - Conditions the paper states: <the ones that change the number —
       backbone, resolution, training budget, evaluation protocol>

     The card and the table, not the abstract. An abstract's headline number is
     often the best of several conditions, and reproducing it means reproducing
     that condition rather than the one in the table.

     If the card does not carry the number, say so: `not in the card, checked
     § <headings>` — and then whether the fetched full text has it. A target
     nobody can name is not a target. -->

## What the paper says about its setup

<!-- Everything the paper states that a reproduction needs, quoted or cited by
     section: data and split protocol, preprocessing, architecture, optimiser
     and schedule, hardware, training length, evaluation protocol, and the code
     release if there is one.

     And, separately and explicitly: **what the paper does not say.** One line
     per missing piece. Musgrave's finding is that the unstated pieces are
     where reproductions go, and a reproduction plan that does not name them
     is guessing in the places that matter. -->

## What my setup differs in

<!-- Line by line against the section above, from the researcher's own code and
     data description:

     - <dimension> — paper: <theirs> · mine: <mine> · matters because <why>
     - <dimension> — paper: <theirs> · mine: unknown, <what was checked>

     A difference that is known and written down is a condition on the
     comparison. A difference nobody noticed is the reason the numbers
     disagree three weeks later. -->

## Reproduction plan

<!-- Numbered steps the RESEARCHER can run. Not pseudocode, not a description
     of an approach: the commands, the configs, and the order.

     1. <step> — <what it produces, and how you know it worked>
     2. ...

     Each step says what success looks like, so a failure is located at a step
     rather than discovered at the end. The last step produces the number that
     goes under ## The gap.

     No agent runs any of this. -->

## The gap

<!-- Filled in AFTER the researcher runs the plan. Empty until then, and the
     status below says `not attempted`.

     - Published: <value> <metric>, <conditions>
     - Achieved: <value> <metric>, <conditions> · <run directory>
     - Gap: <difference>, over <n> seeds
     - Conditions that differ: <the ones from ## What my setup differs in that
       were still true at run time>

     Both numbers and both sets of conditions, always. "Close enough" is a
     judgement the researcher makes against data, and it needs the data. -->

## Reproduction status

<!-- Exactly three states. The first line is this shape and nothing else:

     - Reproduction status: not attempted
     - Reproduction status: attempted, gap recorded
     - Reproduction status: contested

     `contested` is Musgrave's state: a published number that would not
     reproduce. It is not an accusation and it is not a failure of the
     reproduction — it is a recorded disagreement, and it requires WHAT WAS
     TRIED:

     - Tried: <each attempt, with the conditions varied and the number reached>
     - Author contact: <asked / not asked / no response>

     A number recorded as contested with no attempt list is a complaint. -->

## Status

<!-- Date. Which skill wrote this — /baseline or /replicate — and for
     /replicate, the sentence that makes it a calibration test:

     **This paper is not one I am building on. The gap below is a fact about my
     pipeline, not about this paper.**

     Then: the files read, what could not be fetched, and what the datasets
     ledger did or did not say about the split.

     Written 2026-09-20 by /baseline from research/papers/<slug>.md. Full text
     fetched. Datasets ledger row found: split protocol by event. -->
