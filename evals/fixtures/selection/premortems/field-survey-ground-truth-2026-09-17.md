# Pre-mortem: Field survey ground truth

<!-- SYNTHETIC FIXTURE for evals/rank-*. Not a real judgement. -->

## The idea, restated

Replace benchmark labels with a new ground survey of 2,000 buildings and retrain, restated for the fixture.

## Baselines it must beat

- A synthetic baseline · exists · runs

## The field's metric

F1 per damage class. The idea uses it.

## The evaluation plan, and what it depends on

The existing test split. Depends on nothing outside the repo.

## What would have to be true that probably is not

That the lab can field a collection campaign. It cannot.

## Verdict

- Verdict: not executable as written
- Blocker: needs a data collection this lab cannot run in its stated time and budget (CONTEXT.md: constraint unknown).

## What would change the verdict

A synthetic change.

## Status

- Written 2026-09-17 by fixture generator. Synthetic.
