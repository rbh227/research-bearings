# 02: `check_ideas.py`

Type: task
Status: done
Blocked by: 01

## What to build

`scripts/check_ideas.py`, in the shape of `scripts/check_cards.py`: a module
docstring that says what each rule is for and why, a `check()` returning a list
of failure strings, a `main()` over paths or a directory, and `--selftest`.

Over an idea page it fails on:

- a missing heading, checked first and returning immediately, as `check_cards` does;
- an empty `## Idea`;
- a `## Nearest existing` with no row count or no query behind it;
- a `## Seed` that names no file;
- a reference line carrying none of the three verify tags;
- any of the four banned absence words — `unexplored`, `gap`, `novel`, `nobody` — anywhere in the page, the same list `check_analogs.py` uses.

Given `research/IDEAS.md` (by basename) it checks the four log headings instead
and fails when a slug under `## Promoted` has no page in the same repository's
`research/ideas/`.

Selftest: a good page passes, a good log passes, and one case per failure kind
above, each asserting the message names the thing. Last case, as in
`check_cards`: the templates carry every heading the checker requires.

## Acceptance

- [x] `python3 scripts/check_ideas.py --selftest` is green.
- [x] Every failure kind has a case and the good page and good log pass.
- [x] Passing a directory checks every page in it; passing `research/IDEAS.md` runs the log rules.
- [x] The checker reads only the file it is given plus, for the log, the pages directory beside it.

## Resolution

2026-09-16. `scripts/check_ideas.py`, 17 selftest cases, green.

Page rules: every heading, a non-empty `## Idea`, a query, both counts, a
`## Seed` naming a file, a verify tag on every reference line, and none of the
four absence words. Log rules: the four headings, and every `## Promoted` slug
has a page.

**The absence scan needed the same exemption `check_analogs.py` needed.** A
paper title carrying "Novel" is not an absence claim, so the References section,
every reference line, the `Nearest:` tail and every double-quoted span are
blanked before the scan. Case 7b is that exemption.

**The duplication came out in review.** `sections()`, the paper-line regex, the
three verify tags and the banned-word list were copies shared with the three
older checkers, and the absence message had already drifted. They now live in
`scripts/checklib.py`, which all four import; the older three lost 44 lines and
kept every selftest green.

**The two-count rule was added after the dry run**, not from the ticket: the row
count saturates at the budget, so a page carrying it alone reports the one
figure that cannot be thin. Case 4c.
