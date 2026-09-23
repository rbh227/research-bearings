# Experiment: <the idea, as a title of three or four words>

<!-- One experiment page, at research/experiments/<slug>.md. Ten headings,
     fixed. Written by research-bearings:experiment-designer BEFORE anything
     runs, and NEVER edited afterwards.

     That is the whole point. A page written before the run makes every
     post-hoc change visible as a change: if the metric here is not the metric
     in the result, somebody moved the target, and the record says so. /result
     reads this page to judge the outcome against it, and edits nothing.

     The seven pre-registration fields are the first seven headings.
     check_experiments.py enforces them. -->

## Hypothesis

<!-- One sentence: what you believe, stated so that it could turn out false.

     "The consistency objective improves single-image damage F1" is a
     hypothesis. "We investigate the effect of the consistency objective" is a
     plan, and no result can contradict it. -->

## Baseline, and why

<!-- What this is compared against, and the reason that comparison is the
     right one. One line naming it, one or two explaining:

     - Baseline: <name> · <the card and table the published number came from,
       or the run directory of your own reproduction>
     - Why: <why this is the comparison that matters>

     Schulman: a working baseline first. Musgrave: the strongest one, not the
     most convenient. A baseline chosen because it was easy to run is a number
     with nothing behind it. -->

## Metric, and why

<!-- The metric, and why it is this one:

     - Metric: <name, with its exact definition or the paper that defines it>
     - Why: <why this measures what the hypothesis claims>
     - The field reports: <what the cards say the field reports>

     If the metric differs from what the field reports, that is a choice, and
     the reason goes here where a reviewer can find it. An idea scored on a
     metric nobody reports cannot be compared to anything. -->

## Seeds and variance plan

<!-- Written BEFORE the run, because variance discovered afterwards is a
     finding about the experiment rather than about the method:

     - Seeds: <n>
     - Sources of randomness: <initialisation, data order, augmentation,
       split, hardware non-determinism — which ones are controlled and which
       are not>
     - Reported as: <mean and standard deviation over the n seeds, or the
       interval>

     Henderson: a single-seed number is not a result. `- Seeds:` carries an
     integer and check_experiments.py reads it. -->

## Leakage check

<!-- Chunk 7's taxonomy, applied to YOUR OWN split rather than to a paper's.
     One line per type, each with what was checked and where:

     - <type> — <checked how, and what was found> · <the dataset ledger row,
       where one exists>

     Kapoor and Narayanan. The eight types are in the leakage-auditor's
     contract. This section is where your own number gets the treatment you
     gave everybody else's — it is the one that gets retracted otherwise. -->

## Compute budget

<!-- Dodge: a comparison is only fair if both sides got the same search.

     - Budget: <GPU-hours, or wall-clock on named hardware>
     - Search size: <how many hyperparameter configurations, for this method
       AND for the baseline>

     If the baseline got ten configurations and the method got a hundred, the
     result is about the search and not about the method. Both numbers go
     here, before either is spent. -->

## Stop rule

<!-- The decision, made before the number is known. At least one line of this
     exact shape, and check_experiments.py reads it:

     - Abandon if: <the result that means stop>
     - Continue if: <the result that means keep going>

     This is what results-critic applies literally. A stop rule written after
     the number exists is a rationalisation with a heading. -->

## Competing hypotheses

<!-- Platt: two or three hypotheses that could each explain the outcome, and
     the ONE experiment that discriminates between them.

     - H1: <the hypothesis above>
     - H2: <the other explanation — usually that the gain comes from somewhere
       you did not intend>
     - H3: <optional>
     - Discriminating experiment: <the one run whose outcome differs between
       them, and how>

     An experiment that can only confirm H1 has not been designed; it has been
     hoped for. If no run discriminates, say so — that is a real finding about
     the design and it belongs here. -->

## Ablations

<!-- Written by research-bearings:ablation-planner for a method idea, and
     `not a method idea: no ablation plan` otherwise.

     Lipton: a gain nobody isolated is a gain nobody can attribute. Per claimed
     source of gain:

     - Claimed source: <what you say makes it work>
     - Ablation: <what removes exactly that and nothing else>
     - If the gain survives this: <the gain came from somewhere else, and where
       to look next> -->

## Status

<!-- Date. The idea and pre-mortem this came from, by path. Whether an
     ablation plan was written and why or why not. What check_experiments.py
     said.

     THIS PAGE IS NOT EDITED AFTER THE RUN. If the design changed, that is a
     new experiment page with a new slug, and the old one stays. A result that
     disagrees with its pre-registration is the most useful thing in the
     notebook.

     Written 2026-09-20 by experiment-designer from research/ideas/<slug>.md and
     research/premortems/<slug>-2026-09-19.md. Ablation plan: written, 2 claimed
     sources. check_experiments.py: clean. -->
