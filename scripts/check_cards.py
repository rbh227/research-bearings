#!/usr/bin/env python3
"""Structural check on a paper card, the output of /research-bearings:read.

Chunk 7 ships no evals. This is the whole automated done-check for a card, and
like the other checkers it is built to run in a second: everything it asks
can be decided by looking, so nothing here needs a model.

What it enforces, and why each one is here:

  every heading present          the card is an interface. /bits, /audit,
                                 /reviews and later /ideas each read one
                                 section by name, and a missing heading is a
                                 downstream skill reading nothing and
                                 believing it found nothing.
  a delta, or the admission      Mensh and Kording: if "compared to X, this
                                 changes Y and gets Z" cannot be written, the
                                 paper is not understood. The card may say so
                                 — `_cannot be written_` — but it may not be
                                 silent, because silence reads as understood.
  a pass value                   Keshav: record which pass you stopped at. A
                                 skim that does not say it is a skim is a full
                                 read to everything downstream.
  a matrix position or _unplaced_  a card that invents its own cell disagrees
                                 with the landscape later. Unplaced is honest
                                 and /read --place fixes it.
  every reference tagged         a bare title is a claim nobody can check,
                                 and a fabricated citation entering through a
                                 card is the failure /verify exists to close.

Run: python3 scripts/check_cards.py research/papers/<slug>.md [...]
     python3 scripts/check_cards.py research/papers/     (every card in it)
     python3 scripts/check_cards.py --selftest
"""

import os
import re
import sys

# The file shape every checker shares: ## sections, the paper-line form, and the
# three tags /verify writes. checklib.py holds them so four checkers cannot
# drift apart; what only this checker asks stays below.
from checklib import REFERENCE_LINE, VERIFIED, CANDIDATE, NOT_FOUND, pages_under, sections

HEADINGS = (
    "Identity", "Matrix position", "Delta", "Bit flipped", "Not compared against",
    "Kill experiment", "Data and split", "Reproduction", "What to steal",
    "Same-cell comparison", "Prediction score", "What was non-obvious",
    "Reviews", "Leakage", "References", "Status",
)

# A section a later skill fills, and has not yet. Present and honest, not empty.
NOT_RUN = "_not run_"
CANNOT = "_cannot be written_"
UNPLACED = "_unplaced_"

PASS_LINE = re.compile(r"^\s*-\s*Read:.*\bpass\s+(1|full)\b", re.I | re.M)
CELL_LINE = re.compile(r"^\s*-\s*Cell:\s*`[^`]+`", re.M)


def check(text):
    """Return a list of failure strings. Empty means the card passes."""
    problems = []
    secs = sections(text)

    for h in HEADINGS:
        if h not in secs:
            problems.append(f"missing heading: ## {h}")
    if problems:
        return problems

    # 1. The delta sentence, or the explicit admission that it cannot be written.
    delta = secs["Delta"].strip()
    if not delta:
        problems.append("## Delta is empty; write the delta sentence or `_cannot be written_` and what is missing")
    elif CANNOT not in delta and not re.search(r"compared to\b", delta, re.I):
        problems.append(
            "## Delta has no 'Compared to <prior work>, this changes X and gets Y' sentence "
            f"and does not say `_cannot be written_`: {delta.splitlines()[0][:70]}"
        )

    # 2. The pass. A skim that does not announce itself is a full read downstream.
    if not PASS_LINE.search(secs["Identity"]):
        problems.append("## Identity has no `- Read: <date> · pass 1|full` line")

    # 3. The matrix position: a real cell, or unplaced. Never invented, never blank.
    position = secs["Matrix position"].strip()
    if not position:
        problems.append("## Matrix position is empty; name the cell or write `_unplaced_`")
    elif UNPLACED not in position and not CELL_LINE.search(position):
        problems.append(
            "## Matrix position names no `- Cell: \\`<formulation> × <regime>\\`` line "
            "and does not say `_unplaced_`"
        )

    # 4. Every reference tagged. This is the fabrication fence.
    refs = [ln for ln in secs["References"].splitlines() if REFERENCE_LINE.match(ln)]
    for line in refs:
        if not (VERIFIED.search(line.rstrip()) or CANDIDATE in line or NOT_FOUND in line):
            problems.append(f"reference carries no verify tag: {line.strip()[:70]}")

    # 5. A section a later skill owns is either filled or says it has not run.
    for heading in ("Reviews", "Leakage"):
        if not secs[heading].strip():
            problems.append(f"## {heading} is empty; it should say `{NOT_RUN}` until its skill runs")

    # A full read commits predictions; a skim does not, and says so.
    pass_at = PASS_LINE.search(secs["Identity"])
    if pass_at and pass_at.group(1).lower() == "full":
        for heading in ("Prediction score", "What was non-obvious"):
            body = secs[heading].strip()
            if not body or NOT_RUN in body:
                problems.append(
                    f"## {heading} says `{NOT_RUN}` on a full read; the protocol produces it, "
                    "so either the scorer did not run or the pass is really 1"
                )

    return problems



def main(argv):
    if not argv:
        print(__doc__.strip().splitlines()[-3].strip())
        return 2
    paths = []
    for arg in argv:
        paths += pages_under(arg)
    if not paths:
        print("no cards found")
        return 0

    failed = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                problems = check(fh.read())
        except OSError as exc:
            print(f"FAIL {path}\n  - cannot read: {exc}")
            failed += 1
            continue
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"ok   {path}")
    print()
    print(f"{failed} of {len(paths)} cards failed" if failed else f"all {len(paths)} cards pass")
    return 1 if failed else 0


# --------------------------------------------------------------------------
# selftest


GOOD = """# DA-SegFormer: Domain-Adaptive Transformers for Building Damage Assessment

## Identity

- Slug: researcher-2024-da
- Authors: Jane Q. Researcher, Alex B. Coauthor, Sam C. Lastauthor
- Year: 2024
- Venue: CVPR
- Ids: arXiv `2401.00001` · S2 `abc123`
- Code: https://example.org/code — runs: not tried
- Read: 2026-09-16 · pass full · text: fetched
- Fetched from: https://arxiv.org/pdf/2401.00001

## Matrix position

- Formulation: paired-image segmentation
- Data regime: multi-event VHR optical
- Cell: `paired-image segmentation × multi-event VHR optical` — research/landscape/matrix.md

## Delta

Compared to the xView2 challenge winner, this changes the fusion point from
channel stacking to a shared attention bottleneck with a domain discriminator,
and gets 0.61 harmonic mean F1 on a held-out wildfire split against 0.44.

## Bit flipped

That the architecture is the lever: the ablation shows the alignment term, not
the backbone, carries the transfer gain.

## Not compared against

- Self-training domain adaptation, which is the other dominant family and is
  cheaper to run than adversarial alignment.

## Kill experiment

- Experiment: remove the domain discriminator, keep the backbone.
- Run: yes — transfer drops 0.61 to 0.48, which is the paper's own ablation.

## Data and split

- Dataset: xBD
- Split: leave-one-disaster-type-out for the transfer numbers; the standard
  tile split for in-domain.
- Seeds and variance: five seeds, standard deviation 0.03.
- Metric: harmonic mean of per-class F1 over four damage grades.

## Reproduction

- Status: self-reported
- Evidence: authors release code and weights; no third-party reproduction found.
- Reimplementable in an afternoon: no — the adversarial schedule needs tuning.

## What to steal

The leave-one-disaster-type-out protocol. It is a better transfer test than
the standard split and costs nothing extra to run.

## Same-cell comparison

- gupta-2019-creating — compatible: reports the benchmark, not a competing number.

## Prediction score

- Method: 4 — predicted adversarial alignment, missed the shared bottleneck.
- Main result: 2 — predicted a small in-domain gain, missed that the claim is transfer.
- Weakest point: 5 — predicted the tile-overlap split issue, which the paper concedes.
- Pass stopped at: full

## What was non-obvious

That the contribution is a transfer result rather than a benchmark result: the
in-domain gain is 0.02 and the paper does not claim it.

## Reviews

_not run_

## Leakage

_not run_

## References

- Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery · 2019 · S2 `ec58b594` · verified
- SegFormer: Simple and Efficient Design for Semantic Segmentation · 2021 · arXiv `2105.15203` · verified
- Unsupervised Domain Adaptation by Backpropagation · 2015 · _candidate: prefix match only, Domain-Adversarial Training of Neural Networks (S2 `xyz`)_

## Status

Read 2026-09-16 by /read (pass full). Reviews: not run. Leakage: not run.
"""


def selftest():
    failures = []

    def check_case(name, ok, detail=""):
        print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(name)

    got = check(GOOD)
    check_case("1  a complete card passes", not got, f"got {got}")

    # 2. A missing heading is the first thing checked, and it stops there.
    cut = GOOD.replace("## Kill experiment", "## Kill experiments")
    got = check(cut)
    check_case("2  a missing heading fails, and names it",
               any("missing heading: ## Kill experiment" == p for p in got), f"got {got}")

    # 3. A delta that is neither the sentence nor the admission.
    vague = GOOD.replace(
        "Compared to the xView2 challenge winner, this changes the fusion point from\n"
        "channel stacking to a shared attention bottleneck with a domain discriminator,\n"
        "and gets 0.61 harmonic mean F1 on a held-out wildfire split against 0.44.",
        "This paper is about domain adaptation for damage assessment.")
    got = check(vague)
    check_case("3  a delta with no 'compared to' and no admission fails",
               any("## Delta has no" in p for p in got), f"got {got}")

    admits = GOOD.replace(
        "Compared to the xView2 challenge winner, this changes the fusion point from\n"
        "channel stacking to a shared attention bottleneck with a domain discriminator,\n"
        "and gets 0.61 harmonic mean F1 on a held-out wildfire split against 0.44.",
        "_cannot be written_ — the paper never names a nearest prior work.")
    check_case("3b `_cannot be written_` passes; it is a finding, not a gap",
               not check(admits), f"got {check(admits)}")

    # 4. No pass value.
    nopass = GOOD.replace("- Read: 2026-09-16 · pass full · text: fetched", "- Read: 2026-09-16")
    got = check(nopass)
    check_case("4  a card with no pass value fails",
               any("no `- Read:" in p for p in got), f"got {got}")

    # 5. A matrix position that is neither a cell nor unplaced.
    bad_cell = GOOD.replace(
        "- Cell: `paired-image segmentation × multi-event VHR optical` — research/landscape/matrix.md",
        "- Cell: somewhere in the segmentation area")
    got = check(bad_cell)
    check_case("5  a matrix position with no cell line and no `_unplaced_` fails",
               any("names no" in p for p in got), f"got {got}")

    unplaced = GOOD.replace(
        "- Formulation: paired-image segmentation\n"
        "- Data regime: multi-event VHR optical\n"
        "- Cell: `paired-image segmentation × multi-event VHR optical` — research/landscape/matrix.md",
        "_unplaced_ — no matrix existed when this was read.")
    check_case("5b `_unplaced_` passes", not check(unplaced), f"got {check(unplaced)}")

    # 6. An untagged reference.
    untagged = GOOD.replace(
        "- Unsupervised Domain Adaptation by Backpropagation · 2015 · _candidate: prefix match only, Domain-Adversarial Training of Neural Networks (S2 `xyz`)_",
        "- Unsupervised Domain Adaptation by Backpropagation · 2015")
    got = check(untagged)
    check_case("6  a reference with no verify tag fails",
               any("no verify tag" in p for p in got), f"got {got}")

    # 6b. The not-found tag is a tag: a paper the record does not hold stays, marked.
    notfound = GOOD.replace(
        "· _candidate: prefix match only, Domain-Adversarial Training of Neural Networks (S2 `xyz`)_",
        "· _not found: checked s2, openalex, crossref_")
    check_case("6b `_not found:` is a tag; the line stays in the file",
               not check(notfound), f"got {check(notfound)}")

    # 7. A full read with no prediction score did not run the protocol it claims.
    noscore = GOOD.replace(
        "- Method: 4 — predicted adversarial alignment, missed the shared bottleneck.\n"
        "- Main result: 2 — predicted a small in-domain gain, missed that the claim is transfer.\n"
        "- Weakest point: 5 — predicted the tile-overlap split issue, which the paper concedes.\n"
        "- Pass stopped at: full",
        "_not run_")
    got = check(noscore)
    check_case("7  a full read with no prediction score fails",
               any("Prediction score" in p and "_not run_" in p for p in got), f"got {got}")

    # 7b. A skim legitimately has neither.
    skim = noscore.replace("· pass full ·", "· pass 1 ·").replace(
        "That the contribution is a transfer result rather than a benchmark result: the\n"
        "in-domain gain is 0.02 and the paper does not claim it.", "_not run_")
    check_case("7b a skim with no prediction score passes", not check(skim), f"got {check(skim)}")

    # 8. A section a later skill owns may not be silently empty.
    empty_reviews = GOOD.replace("## Reviews\n\n_not run_", "## Reviews\n")
    got = check(empty_reviews)
    check_case("8  an empty ## Reviews fails; `_not run_` is the honest form",
               any("## Reviews is empty" in p for p in got), f"got {got}")

    # 9. The template itself is all comments, so it is not mistaken for a card.
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(here, "templates", "research", "card.md"), encoding="utf-8") as fh:
        template = fh.read()
    check_case("9  the template carries every heading the checker requires",
               all(f"## {h}" in template for h in HEADINGS),
               f"missing {[h for h in HEADINGS if f'## {h}' not in template]}")

    print()
    print(f"{'FAILED' if failures else 'all green'}: {len(failures)} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(selftest() if args and args[0] == "--selftest" else main(args))
