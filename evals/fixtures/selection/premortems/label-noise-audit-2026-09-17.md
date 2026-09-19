# Pre-mortem: Label noise audit

<!-- SYNTHETIC FIXTURE for evals/rank-*. Not a real judgement. -->

## The idea, restated

Re-label a stratified 500-tile sample of the benchmark and measure inter-annotator agreement per damage class before any modelling, restated for the fixture.

## Baselines it must beat

- A synthetic baseline · exists · runs

## The field's metric

F1 per damage class. The idea uses it.

## The evaluation plan, and what it depends on

The existing test split. Depends on nothing outside the repo.

## What would have to be true that probably is not

That the benchmark labels are consistent enough to measure this.

## Verdict

- Verdict: executable

## What would change the verdict

A synthetic change.

## Status

- Written 2026-09-17 by fixture generator. Synthetic.
