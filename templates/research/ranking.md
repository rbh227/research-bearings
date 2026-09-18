# Ranking

<!-- One ranked list, at research/RANKING.md. Eight headings, fixed. Written by
     /research-bearings:rank.

     This is the ONE file under research/ that is overwritten, and it keeps its
     own history inside itself under ## Previous orders. Everything else in this
     plugin is dated and appended, because a notebook entry and a result cite
     their sources by path. A ranking is a current state, and two ranking files
     would let the older one be quietly forgotten.

     It reads idea pages and pre-mortems side by side. It never edits either. -->

## Pairings

<!-- The bound, and the list, as it was shown to the researcher BEFORE any
     judge ran:

     - Ideas ranked: <n>. Set aside: <n>. Pairings: <n> of a 12 cap.
     - Rule applied: round robin (5 or fewer) | three each, spanning seed kinds

     Then one line per pairing:

     - <slug-a> vs <slug-b> — <why this pair: different seed kinds, or the
       round robin>

     The count is here because it is the cost. Twelve ideas compared every way
     is sixty-six judge calls, and a ranking nobody can afford does not get
     run. If any idea got fewer pairings than the rule asks, say which and how
     many. -->

## Tournament

<!-- What the judges returned. One line per pairing:

     - <slug-a> vs <slug-b> → <winner> · <the one sentence that decided it> ·
       `research/rankings/<a>-vs-<b>-<date>.md`

     Then the tally: wins per idea, and any idea that lost every pairing or won
     every pairing.

     A tally is not the order. It measures which ideas a judge found more
     interesting, which is one input to ## Order and not the rule. -->

## Feasibility against interest

<!-- Alon's chart as a five-by-five text grid, drawn from the judges' scores.
     Interest up the left, feasibility across the bottom, both one to five,
     averaged across each idea's pairings and rounded.

     The hard-but-feasible region — high interest, feasible but not easy — is
     marked. Alon's point is that it is the quadrant students avoid: they take
     the easy-and-interesting problems, which are already taken, or the
     fascinating-and-impossible ones, which produce nothing.

           5 |  .    .   [X]  [ ]   .
           4 |  .    .   [ ]  [ ]   .
     interest 3 |  .    .    .    .   .
           2 |  .    .    .    .   .
           1 |  .    .    .    .   .
             +------------------------
                1    2    3    4    5
                     feasibility

     [ ] marks the region. X is an idea in it. A dot is an empty cell; a letter
     or number placed in a cell is an idea, keyed below the grid.

     Scores are judges' written judgements with evidence lines behind them, not
     computed quantities. Nothing here is a measurement. -->

## Order

<!-- The ranked list, ordered by CHEAPEST KILL FIRST. One line per idea:

     1. <slug> — kill: <the experiment, from the idea page's ## Cheapest kill>
        · costs: <the cost line> · tournament: <n> wins · premortem: <verdict>

     Steinhardt's rule: run the experiment most likely to end the project,
     first. Not the idea that sounds best — the one whose failure you would
     learn most cheaply, because the point of the next month is information and
     the cheapest information comes first.

     Then, and this heading is not complete without it:

     **Where the two orders disagree:** <one line per idea whose tournament
     rank and cheapest-kill rank differ by more than two places, saying which
     is which>

     The disagreement is the interesting part. An idea the judges loved whose
     kill costs three months is exactly the trap this ordering exists to make
     visible. -->

## Set aside

<!-- Ideas whose pre-mortem said `not executable as written`. NOT ranked, and
     not deleted. One line each:

     - <slug> — blocker: <the blocker, from the pre-mortem's ## Verdict> ·
       `research/premortems/<slug>-<date>.md`

     They are set aside rather than ranked because a broken idea scored on
     interest outranks a working one, and then somebody runs it. What would
     change the verdict is in the pre-mortem; if it changes, the idea comes
     back on the next run. -->

## Surviving

<!-- The human gate, and the only heading written from what the researcher
     said, in their words:

     - <slug> — <why, quoted from the researcher>

     The skill proposes; the researcher decides. Nothing proceeds to /spec or
     /design on a judge's say-so. If the researcher overruled the order, that
     is recorded here and not argued with. -->

## Status

<!-- Date. How many ideas were read, how many pre-mortems were found, how many
     ideas had none. How many pairings ran and how many judges returned.
     Anything the run could not do.

     If this is a re-run after a result landed: what moved, and why — naming
     the result file that caused it.

     Written 2026-09-20 by /rank. 7 ideas, 7 pre-mortems, 2 set aside, 9
     pairings. Re-run after research/results/<slug>-2026-09-19.md: <slug> moved
     from 1 to 4, its kill is no longer the cheapest because the baseline
     turned out not to run. -->

## Previous orders

<!-- Every earlier order, newest first, each with its date and one line on what
     it was. Appended to on every re-run, never trimmed.

     ### 2026-09-12
     1. <slug> 2. <slug> 3. <slug> — before the baseline result.

     This is why one overwritten file is safe. The current state is at the top
     of the file and the history is at the bottom of it. -->
