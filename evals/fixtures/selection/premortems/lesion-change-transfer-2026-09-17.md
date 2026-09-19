# Pre-mortem: Lesion change transfer

<!-- SYNTHETIC FIXTURE for evals/rank-*. Not a real judgement. -->

## The idea, restated

Port the medical lesion-change pipeline's registration-then-difference step to paired overhead tiles, restated for the fixture.

## Baselines it must beat

- A synthetic baseline · exists · runs

## The field's metric

F1 per damage class. The idea uses it.

## The evaluation plan, and what it depends on

The existing test split. Depends on nothing outside the repo.

## What would have to be true that probably is not

That registration error is smaller than the change signal.

## Verdict

- Verdict: executable with changes
- Changes: 1. register tiles before differencing. 2. drop the medical prior.

## What would change the verdict

A synthetic change.

## Status

- Written 2026-09-17 by fixture generator. Synthetic.
