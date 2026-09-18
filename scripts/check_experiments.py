#!/usr/bin/env python3
"""Structural check on an experiment page and on a result page, the two outputs
of /research-bearings:design and /research-bearings:result.

Chunk 9 ships no evals. This is the whole automated done-check for both pages,
and like the other checkers it is built to run in a second: everything it asks
can be decided by looking, so nothing here needs a model.

What it enforces on an experiment page, and why each one is here:

  every heading present          the page is an interface. /result reads the
                                 stop rule, the metric and the baseline by
                                 name, and a missing heading is a downstream
                                 skill reading nothing and believing it found
                                 nothing.
  a hypothesis, a baseline and   an empty section is a pre-registration that
  a metric, non-empty            pre-registers nothing. These three are what
                                 the critic compares the outcome against.
  a stop rule in its own shape   `- Abandon if: <result>`. results-critic
                                 applies this literally, and a stop rule
                                 written as prose is one the critic has to
                                 interpret — which is the interpretation the
                                 author wanted, three months later. A rule
                                 with no `Abandon if:` line is not a rule.
  a seed count                   Henderson: a single-seed number is not a
                                 result. `- Seeds: <n>` is written before the
                                 run so that variance is planned rather than
                                 discovered, and an integer is the only form
                                 the plan can take that means anything.
  a leakage section with content Kapoor and Narayanan, applied to your own
                                 split rather than to a paper's. This is the
                                 one that gets retracted.
  a compute budget and a         Dodge: a comparison is fair only if both
  search size                    sides got the same search. A method with a
                                 hundred configurations against a baseline
                                 with ten is a result about the search.

And on a result page:

  every heading present          same reason.
  a verdict, and one of three    survived / killed / inconclusive. /rank reads
                                 it to re-order, and a fourth state is a
                                 downstream skill reading prose.
  a run directory per table row  a number with no run behind it is the thing
                                 the whole experiment half exists to prevent.
                                 The columns are found by header name, so the
                                 order can change; a table with no run-directory
                                 column at all fails on the header.
  no single-seed number without  Henderson again, enforced rather than stated.
  its refusal                    A one-seed row may appear ONLY carrying
                                 `refused`, which is how the refusal stays
                                 visible instead of becoming a silent omission.

Which rules run is decided by the page itself: a page with a stop rule is an
experiment, a page with a verdict is a result. A page with neither is reported
as such rather than passed.

Run: python3 scripts/check_experiments.py research/experiments/<slug>.md [...]
     python3 scripts/check_experiments.py research/experiments/
     python3 scripts/check_experiments.py research/results/
     python3 scripts/check_experiments.py --selftest
"""

import os
import re
import sys

# The file shape every checker shares. checklib.py holds these so five checkers
# cannot drift apart; what only this checker asks stays below.
from checklib import sections

EXPERIMENT_HEADINGS = (
    "Hypothesis",
    "Baseline, and why",
    "Metric, and why",
    "Seeds and variance plan",
    "Leakage check",
    "Compute budget",
    "Stop rule",
    "Competing hypotheses",
    "Ablations",
    "Status",
)

RESULT_HEADINGS = (
    "Table",
    "Not sourced",
    "Verdict",
    "Failure mode audit",
    "What the pre-registration said",
    "Status",
)

VERDICTS = ("survived", "killed", "inconclusive")

# `- Abandon if: <something>`. The one shape results-critic can apply without
# interpreting, which is the point: an interpreted stop rule is interpreted by
# whoever wants the result.
ABANDON = re.compile(r"^\s*-\s*Abandon if\s*:\s*(\S.*)$", re.M | re.I)
SEEDS = re.compile(r"^\s*-\s*Seeds\s*:\s*(\d+)\b", re.M | re.I)
BUDGET = re.compile(r"^\s*-\s*Budget\s*:\s*(\S.*)$", re.M | re.I)
SEARCH_SIZE = re.compile(r"^\s*-\s*Search size\s*:\s*(\S.*)$", re.M | re.I)
VERDICT_LINE = re.compile(r"^\s*-\s*Verdict\s*:\s*(\S.*?)\s*$", re.M | re.I)

# A cell holding nothing a reader could follow. An em dash and a question mark
# are how "I did not find one" gets written when nobody is checking.
EMPTY_CELL = re.compile(r"^(|-+|—|–|n/?a|none|\?+|tbd)$", re.I)


def is_blank(body):
    """True if a section holds no content once its guidance comment is gone.

    checklib.sections() has already stripped comments, so a freshly copied
    template fails every content rule rather than passing as a filled file.
    """
    return not body.strip()


def table_rows(body):
    """Return (header_cells, [(line_number, cells)]) for the first table found.

    A markdown table is any run of lines starting with `|`. The separator row
    is dropped. Returns (None, []) when there is no table.
    """
    lines = body.splitlines()
    header, rows, started = None, [], False
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            if started:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            started = True
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append((i, cells))
    return header, rows


def column_index(header, *words):
    """The index of the first column whose name contains all of `words`."""
    for i, name in enumerate(header):
        lowered = name.lower()
        if all(w in lowered for w in words):
            return i
    return None


def check_experiment(text):
    problems = []
    found = sections(text)

    for name in EXPERIMENT_HEADINGS:
        if name not in found:
            problems.append("missing heading: ## {}".format(name))
    if problems:
        # Same rule as check_cards: a page missing a heading is not a page this
        # checker can say anything else useful about.
        return problems

    for name in ("Hypothesis", "Baseline, and why", "Metric, and why"):
        if is_blank(found[name]):
            problems.append(
                "## {} is empty: a pre-registration that pre-registers nothing "
                "is what the critic will compare the outcome against".format(name)
            )

    stop = found["Stop rule"]
    if is_blank(stop):
        problems.append("## Stop rule is empty: the decision has to be made before the number is known")
    elif not ABANDON.search(stop):
        problems.append(
            "## Stop rule has no `- Abandon if: <result>` line: results-critic "
            "applies the rule literally, and prose is interpreted by whoever wants the result"
        )

    variance = found["Seeds and variance plan"]
    if is_blank(variance):
        problems.append("## Seeds and variance plan is empty: variance discovered after the run is a finding about the experiment")
    elif not SEEDS.search(variance):
        problems.append(
            "## Seeds and variance plan has no `- Seeds: <n>` count: Henderson, "
            "a single-seed number is not a result and the plan has to say how many"
        )
    else:
        n = int(SEEDS.search(variance).group(1))
        if n < 1:
            problems.append("## Seeds and variance plan gives `- Seeds: {}`, which is not a run".format(n))

    if is_blank(found["Leakage check"]):
        problems.append(
            "## Leakage check is empty: this is where your own split gets the "
            "treatment you gave every paper's, and it is the one that gets retracted"
        )

    budget = found["Compute budget"]
    if is_blank(budget):
        problems.append("## Compute budget is empty: a comparison is fair only if both sides got the same search")
    else:
        if not BUDGET.search(budget):
            problems.append("## Compute budget has no `- Budget: <compute>` line")
        if not SEARCH_SIZE.search(budget):
            problems.append(
                "## Compute budget has no `- Search size: <n>` line: Dodge, a method "
                "given a hundred configurations against a baseline given ten is a result about the search"
            )

    return problems


def check_result(text):
    problems = []
    found = sections(text)

    for name in RESULT_HEADINGS:
        if name not in found:
            problems.append("missing heading: ## {}".format(name))
    if problems:
        return problems

    verdict_body = found["Verdict"]
    match = VERDICT_LINE.search(verdict_body)
    if not match:
        problems.append(
            "## Verdict has no `- Verdict: <state>` line: /rank reads it to re-order, "
            "and a verdict in prose is a downstream skill guessing"
        )
    else:
        state = match.group(1).strip().rstrip(".").lower()
        if state not in VERDICTS:
            problems.append(
                "## Verdict is `{}`, which is not one of {}: a fourth state is a "
                "downstream skill reading prose".format(match.group(1).strip(), ", ".join(VERDICTS))
            )

    header, rows = table_rows(found["Table"])
    if header is None:
        problems.append("## Table holds no table: the numbers are built from the ingest output, not retyped")
        return problems

    run_col = column_index(header, "run")
    seed_col = column_index(header, "seed")
    if run_col is None:
        problems.append(
            "## Table has no run-directory column: every number carries where it "
            "came from, or the table and the runs can disagree"
        )
    if seed_col is None:
        problems.append("## Table has no seeds column: a number with no seed count cannot be checked against the variance plan")
    if not rows:
        problems.append("## Table has a header and no rows")

    for line_no, cells in rows:
        label = cells[0] if cells else "(row {})".format(line_no)
        if run_col is not None:
            cell = cells[run_col] if run_col < len(cells) else ""
            if EMPTY_CELL.fullmatch(cell.strip()):
                problems.append(
                    "## Table row '{}' names no run directory: a number with no run "
                    "behind it belongs under ## Not sourced".format(label)
                )
        if seed_col is not None:
            cell = cells[seed_col] if seed_col < len(cells) else ""
            seeds = re.match(r"^\s*(\d+)", cell)
            if seeds and int(seeds.group(1)) == 1:
                if "refused" not in " ".join(cells).lower():
                    problems.append(
                        "## Table row '{}' is a single-seed number with no refusal: "
                        "Henderson — a one-seed row may appear only carrying "
                        "`refused`, so the refusal stays visible".format(label)
                    )

    return problems


def kind(text):
    """Which page this is, decided by the page rather than by its path.

    By how many of each set's headings are present, not by one marker heading.
    The first version keyed on `## Stop rule` against `## Verdict`, and the
    selftest caught what that costs: an experiment page whose stop-rule heading
    is misspelled is exactly the page most worth failing loudly, and it was the
    one page the classifier could not recognise. It reported "cannot tell"
    instead of "missing heading: ## Stop rule", which is the less useful of the
    two true statements.
    """
    found = sections(text)
    e = sum(1 for n in EXPERIMENT_HEADINGS if n in found)
    r = sum(1 for n in RESULT_HEADINGS if n in found)
    if e >= 3 and r >= 3:
        return "both"
    if e == 0 and r == 0 or e == r:
        return None
    return "experiment" if e > r else "result"


def check(text):
    what = kind(text)
    if what == "experiment":
        return check_experiment(text)
    if what == "result":
        return check_result(text)
    if what == "both":
        return ["this page has both ## Stop rule and ## Verdict: an experiment page is "
                "never edited after a run, so a result belongs in its own dated file"]
    return ["cannot tell whether this is an experiment page or a result page: "
            "it has neither ## Stop rule nor ## Verdict"]


def pages_under(arg):
    if os.path.isdir(arg):
        return sorted(
            os.path.join(arg, n) for n in os.listdir(arg)
            if n.endswith(".md") and os.path.isfile(os.path.join(arg, n))
        )
    return [arg]


def main(argv):
    if not argv:
        print("usage: check_experiments.py research/experiments/ | research/results/ | <page.md> ...")
        return 2
    paths = []
    for arg in argv:
        paths += pages_under(arg)
    if not paths:
        print("no pages found")
        return 0

    failed = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print("FAIL {}\n  - cannot read: {}".format(path, exc))
            failed += 1
            continue
        problems = check(text)
        if problems:
            failed += 1
            print("FAIL {}".format(path))
            for p in problems:
                print("  - {}".format(p))
        else:
            print("ok   {}".format(path))

    print()
    print("{} of {} pages failed".format(failed, len(paths)) if failed
          else "all {} pages pass".format(len(paths)))
    return 1 if failed else 0


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

GOOD_EXPERIMENT = """# Experiment: single-capture damage head

## Hypothesis

Training the damage head on the pre-event image alone, with the post-event image
used only as a consistency signal, matches paired-input F1 on xBD within 2 points.

## Baseline, and why

- Baseline: xView2 baseline, paired input · research/papers/gupta-2019-xbd.md § Table 4, 0.741 localisation F1
- Why: it is the strongest published number on this split, and its code runs.

## Metric, and why

- Metric: per-class damage F1 on the xBD held-out split, as defined in Gupta 2019 § 5.2
- Why: the hypothesis is about damage classification, not localisation.
- The field reports: damage F1 in 6 of the 7 cards under research/papers/.

## Seeds and variance plan

- Seeds: 5
- Sources of randomness: initialisation and data order are controlled by the seed;
  cuDNN non-determinism is not, and is left uncontrolled.
- Reported as: mean and standard deviation over the 5 seeds.

## Leakage check

- Temporal leakage — the split is by event, checked against research/landscape/datasets.md § xBD
- Preprocessing on the full set — normalisation statistics are computed on train only, scripts/prep.py:41

## Compute budget

- Budget: 40 GPU-hours on one A100, which is what research/CONTEXT.md states is available
- Search size: 12 configurations for the method and 12 for the baseline

## Stop rule

- Abandon if: single-capture F1 is more than 5 points below the paired baseline at 5 seeds
- Continue if: the gap is under 2 points, or under 5 with the ablation isolating the cause

## Competing hypotheses

- H1: the consistency objective carries the pre-event signal.
- H2: the gain is the extra augmentation the consistency pass introduces.
- Discriminating experiment: run the augmentation without the consistency loss;
  under H2 the gain survives, under H1 it does not.

## Ablations

- Claimed source: the consistency loss
- Ablation: remove the loss term, keep the second forward pass and its augmentation
- If the gain survives this: the gain came from augmentation, and H2 is the story

## Status

Written 2026-09-20 by experiment-designer from research/ideas/single-capture.md.
"""

GOOD_RESULT = """# Result: single-capture damage head

## Table

| metric | value | seeds | variance | run directory |
|---|---|---|---|---|
| damage F1 | 0.612 | 5 | ±0.008 | runs/exp-14/ |
| damage F1 (baseline) | 0.588 | 5 | ±0.011 | runs/base-03/ |

## Not sourced

- localisation F1 — looked for `loc_f1` in runs/exp-14/ and runs/base-03/, found neither

## Verdict

- Verdict: survived
- The clause that decided it: "Abandon if: single-capture F1 is more than 5 points below the paired baseline at 5 seeds"
- Against: rows 1 and 2, a gap of +2.4 points in favour of the method

## Failure mode audit

### M1 fabricated number
- Detection question: does every number in the table appear in a metrics file?
- Answer: yes · runs/exp-14/metrics.csv, runs/base-03/metrics.csv

### M4 silent test-set reuse
- Answer: `unchecked: read runs/exp-14/config.json, which names no split file`

## What the pre-registration said

Hypothesis, metric, baseline and stop rule quoted from
research/experiments/single-capture.md. No deviations.

## Status

Written 2026-09-22 by /result. Ingested 2 run directories, nothing unparseable.
"""


def selftest():
    failures = []

    def case(name, ok, detail=""):
        print("{} {}".format("ok  " if ok else "FAIL", name)
              + (" — {}".format(detail) if detail and not ok else ""))
        if not ok:
            failures.append(name)

    got = check(GOOD_EXPERIMENT)
    case("1  a complete experiment page passes", not got, "got {}".format(got))

    got = check(GOOD_RESULT)
    case("2  a complete result page passes", not got, "got {}".format(got))

    # 3. A missing heading is checked first and stops there.
    got = check(GOOD_EXPERIMENT.replace("## Stop rule", "## Stopping rule"))
    case("3  an experiment page missing a heading fails, and names it",
         any("missing heading: ## Stop rule" in p for p in got), "got {}".format(got))

    # 4. A stop rule with no Abandon line is prose the critic has to interpret.
    got = check(GOOD_EXPERIMENT.replace(
        "- Abandon if: single-capture F1 is more than 5 points below the paired baseline at 5 seeds\n",
        "We will stop if the results look bad.\n"))
    case("4  a stop rule with no `- Abandon if:` line fails",
         any("no `- Abandon if:" in p for p in got), "got {}".format(got))

    got = check(GOOD_EXPERIMENT.replace(
        "- Abandon if: single-capture F1 is more than 5 points below the paired baseline at 5 seeds\n"
        "- Continue if: the gap is under 2 points, or under 5 with the ablation isolating the cause\n", ""))
    case("4b an empty stop rule fails",
         any("## Stop rule is empty" in p for p in got), "got {}".format(got))

    # 5. A variance plan with no seed count.
    got = check(GOOD_EXPERIMENT.replace("- Seeds: 5\n", "- Seeds: as many as time allows\n"))
    case("5  a variance plan with no seed count fails",
         any("no `- Seeds: <n>` count" in p for p in got), "got {}".format(got))

    # 6. A missing leakage section.
    got = check(GOOD_EXPERIMENT.replace(
        "- Temporal leakage — the split is by event, checked against research/landscape/datasets.md § xBD\n"
        "- Preprocessing on the full set — normalisation statistics are computed on train only, scripts/prep.py:41\n",
        ""))
    case("6  an empty leakage check fails",
         any("## Leakage check is empty" in p for p in got), "got {}".format(got))

    # 7. A blank compute budget, and a budget with no search size.
    got = check(GOOD_EXPERIMENT.replace(
        "- Budget: 40 GPU-hours on one A100, which is what research/CONTEXT.md states is available\n"
        "- Search size: 12 configurations for the method and 12 for the baseline\n", ""))
    case("7  a blank compute budget fails",
         any("## Compute budget is empty" in p for p in got), "got {}".format(got))

    got = check(GOOD_EXPERIMENT.replace(
        "- Search size: 12 configurations for the method and 12 for the baseline\n", ""))
    case("7b a compute budget with no search size fails, which is Dodge's rule",
         any("no `- Search size:" in p for p in got), "got {}".format(got))

    # 8. An empty hypothesis.
    got = check(GOOD_EXPERIMENT.replace(
        "Training the damage head on the pre-event image alone, with the post-event image\n"
        "used only as a consistency signal, matches paired-input F1 on xBD within 2 points.\n", ""))
    case("8  an empty ## Hypothesis fails",
         any("## Hypothesis is empty" in p for p in got), "got {}".format(got))

    # 9. A result page missing a heading.
    got = check(GOOD_RESULT.replace("## Not sourced", "## Missing"))
    case("9  a result page missing a heading fails, and names it",
         any("missing heading: ## Not sourced" in p for p in got), "got {}".format(got))

    # 10. No verdict line at all.
    got = check(GOOD_RESULT.replace("- Verdict: survived\n", "The experiment worked.\n"))
    case("10 a result with no `- Verdict:` line fails",
         any("no `- Verdict: <state>` line" in p for p in got), "got {}".format(got))

    # 11. A verdict outside the three.
    got = check(GOOD_RESULT.replace("- Verdict: survived", "- Verdict: promising"))
    case("11 a verdict that is not one of the three fails, and names the three",
         any("not one of survived, killed, inconclusive" in p for p in got), "got {}".format(got))

    for state in VERDICTS:
        got = check(GOOD_RESULT.replace("- Verdict: survived", "- Verdict: " + state))
        case("11{} `{}` is accepted".format("abc"[VERDICTS.index(state)], state),
             not got, "got {}".format(got))

    # 12. A table row with no run directory.
    got = check(GOOD_RESULT.replace("| damage F1 | 0.612 | 5 | ±0.008 | runs/exp-14/ |",
                                    "| damage F1 | 0.612 | 5 | ±0.008 |  |"))
    case("12 a table row with no run directory fails, and names the row",
         any("row 'damage F1' names no run directory" in p for p in got), "got {}".format(got))

    got = check(GOOD_RESULT.replace("| damage F1 | 0.612 | 5 | ±0.008 | runs/exp-14/ |",
                                    "| damage F1 | 0.612 | 5 | ±0.008 | — |"))
    case("12b an em dash is not a run directory",
         any("names no run directory" in p for p in got), "got {}".format(got))

    # 13. A single-seed number, with and without its refusal.
    got = check(GOOD_RESULT.replace("| damage F1 | 0.612 | 5 | ±0.008 | runs/exp-14/ |",
                                    "| damage F1 | 0.612 | 1 | n/a | runs/exp-14/ |"))
    case("13 a single-seed number with no refusal fails",
         any("single-seed number with no refusal" in p for p in got), "got {}".format(got))

    got = check(GOOD_RESULT.replace(
        "| damage F1 | 0.612 | 5 | ±0.008 | runs/exp-14/ |",
        "| damage F1 | 0.612 | 1 | refused: single seed | runs/exp-14/ |"))
    case("13b a single-seed number carrying `refused` passes", not got, "got {}".format(got))

    # 14. A table with no run-directory column at all.
    got = check(GOOD_RESULT.replace("| metric | value | seeds | variance | run directory |",
                                    "| metric | value | seeds | variance | source |"))
    case("14 a table with no run-directory column fails on the header",
         any("no run-directory column" in p for p in got), "got {}".format(got))

    # 15. Column order is not fixed: the columns are found by name.
    reordered = GOOD_RESULT.replace(
        "| metric | value | seeds | variance | run directory |\n"
        "|---|---|---|---|---|\n"
        "| damage F1 | 0.612 | 5 | ±0.008 | runs/exp-14/ |\n"
        "| damage F1 (baseline) | 0.588 | 5 | ±0.011 | runs/base-03/ |",
        "| metric | run directory | value | variance | seed count |\n"
        "|---|---|---|---|---|\n"
        "| damage F1 | runs/exp-14/ | 0.612 | ±0.008 | 5 |\n"
        "| damage F1 (baseline) | runs/base-03/ | 0.588 | ±0.011 | 5 |")
    case("15 the columns are found by header name, not by position",
         not check(reordered), "got {}".format(check(reordered)))

    # 16. Neither kind, and both kinds.
    case("16 a page that is neither is reported rather than passed",
         any("neither ## Stop rule nor ## Verdict" in p for p in check("# x\n\n## Notes\n\nhi\n")))
    case("16b a page carrying both is refused: a result is its own dated file",
         any("never edited after a run" in p for p in check(GOOD_EXPERIMENT + GOOD_RESULT)))

    # 17. As check_cards does: the templates carry every heading this checker requires.
    here = os.path.dirname(os.path.abspath(__file__))
    for template, required in (("experiment.md", EXPERIMENT_HEADINGS),
                               ("result.md", RESULT_HEADINGS)):
        path = os.path.join(here, "..", "templates", "research", template)
        try:
            with open(path, encoding="utf-8") as fh:
                names = [l.strip()[3:].strip() for l in fh if l.startswith("## ")]
        except OSError as exc:
            names = []
            print("     (cannot read {}: {})".format(template, exc))
        missing = [h for h in required if h not in names]
        case("17 templates/research/{} carries every heading the checker requires".format(template),
             not missing, "missing {}".format(missing))

    print()
    if failures:
        print("{} FAILED: {}".format(len(failures), ", ".join(failures)))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
