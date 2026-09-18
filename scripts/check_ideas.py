#!/usr/bin/env python3
"""Structural check on an idea page and on the running log, the two outputs of
/research-bearings:ideas and /research-bearings:brainstorm.

Chunk 8 ships no evals. This is the whole automated done-check for an idea, and
like the other checkers it is built to run in a second: everything it asks can
be decided by looking, so nothing here needs a model.

What it enforces on a page, and why each one is here:

  every heading present          the page is an interface. /premortem, /rank
                                 and /spec each read one section by name, and
                                 a missing heading is a downstream skill
                                 reading nothing and believing it found
                                 nothing.
  an idea, in the section        an empty ## Idea is an area with a filename.
  a query and both counts        Nova: novelty is a retrieval result. The
                                 Nearest existing section is the only shape a
                                 claim about what does not exist may take, and
                                 without the query and the counts it is an
                                 opinion in the shape of a measurement.
                                 BOTH counts, because the row count saturates:
                                 measured 2026-09-16, a walk with --budget 30
                                 returns "neighborhood 30" for any query the
                                 search finds papers for. How many papers the
                                 query found is the number that moves, so a
                                 page carrying the rows alone reports the one
                                 figure that cannot be thin.
  a seed naming a file           a candidate that cannot name where it came
                                 from was generated from what the model
                                 already knew — the exact failure this stage
                                 exists to avoid, measured at 0.322 against
                                 0.410 average distance from the seed
                                 literature.
  every reference tagged         a bare title is a claim nobody can check, and
                                 a fabricated citation entering through an
                                 idea is the failure /verify exists to close.
  no absence claims              "unexplored", "gap", "novel", "nobody". One
                                 walk is not the literature. Same list, same
                                 reason, as check_analogs.py.

And on research/IDEAS.md:

  the four log headings          both skills append to it by heading.
  every promoted slug has a page  the log and the pages may not disagree. A
                                 promoted idea with no page is a claim that
                                 something was written down when it was not.

The pages directory holds pages and nothing else. `research/ideas/*.md` is read
as idea pages, one per file; the run's other outputs live in subdirectories —
`personas/`, `sections/`, `plans/` — which this checker does not descend into. A
diversity plan written beside the pages fails eight heading rules on every run,
which is how the layout was found to be wrong (review, 2026-09-16).

Run: python3 scripts/check_ideas.py research/ideas/<slug>.md [...]
     python3 scripts/check_ideas.py research/ideas/      (every page in it)
     python3 scripts/check_ideas.py research/IDEAS.md    (the log)
     python3 scripts/check_ideas.py --selftest
"""

import os
import re
import sys

# The file shape every checker shares. checklib.py holds these so four checkers
# cannot drift apart; what only this checker asks stays below.
from checklib import (pages_under, REFERENCE_LINE, VERIFIED, CANDIDATE, NOT_FOUND,
                      sections, banned_words)

HEADINGS = (
    "Idea", "Seed", "What it flips", "Nearest existing",
    "What would have to be true", "Cheapest kill", "Typicality",
    "References", "Status",
)

LOG_HEADINGS = ("Log", "Promoted", "Dropped", "Status")


# The two lines that make Nearest existing a measurement rather than a mood.
QUERY_LINE = re.compile(r"^\s*-\s*Query:\s*\S", re.M)
ROWS_LINE = re.compile(r"^\s*-\s*Rows:\s*\d+", re.M)
PAPERS_FOUND_LINE = re.compile(r"^\s*-\s*Papers the query found:\s*\d+", re.M)
# A seed names the file it came from: any path with an extension.
SEED_FILE = re.compile(r"[\w./-]+\.(?:md|json|txt)\b")
# "- <slug> — ..." under ## Promoted, or a bare "- <slug>" on its own line: a
# slug with nothing after it must not escape the cross-check. The bare form is
# matched only when the whole line is one lowercase slug, so a prose bullet
# ("- Nothing promoted this run.") is not read as a missing page.
PROMOTED_LINE = re.compile(
    r"^\s*-\s*`?([A-Za-z0-9][\w-]*)`?\s*(?:(?:—|--|-|:)\s|$)", re.M
)


def authored_only(text):
    """The page with other people's words removed, for the absence scan.

    The rule is about what the skill writes, not what it quotes. Paper titles
    carry "Novel" constantly, and so does the `Nearest:` title on the one line
    whose whole job is to name somebody else's paper. Blank those out and keep
    the line numbering.
    """
    kept = []
    in_references = False
    for line in re.sub(r"<!--.*?-->", "", text, flags=re.S).splitlines():
        if line.startswith("## "):
            in_references = line[3:].strip() == "References"
        # ## References is a list of other people's titles and nothing else.
        if in_references or REFERENCE_LINE.match(line):
            kept.append("")
            continue
        # The Nearest line's whole job is to name somebody else's paper, and a
        # quoted span is the field's words, not the skill's.
        line = re.sub(r"Nearest:.*$", "Nearest:", line)
        line = re.sub(r'"[^"]*"', '""', line)
        kept.append(line)
    return "\n".join(kept)


def absence_claims(text):
    """Where the page says the field lacks something, rather than what the
    search returned."""
    return [
        f"line {line}: '{word}' — absence is mechanical here; report the row "
        "count the walk returned and let the reader conclude"
        for word, line in banned_words(authored_only(text))
    ]


def check(text):
    """Return a list of failure strings for one idea page. Empty means it passes."""
    problems = []
    secs = sections(text)

    for h in HEADINGS:
        if h not in secs:
            problems.append(f"missing heading: ## {h}")
    if problems:
        return problems

    # 1. An idea, stated.
    if not secs["Idea"].strip():
        problems.append("## Idea is empty; one sentence saying what you would actually do")

    # 2. The absence rule: a query and a row count, or the section is an opinion.
    nearest = secs["Nearest existing"]
    if not QUERY_LINE.search(nearest):
        problems.append(
            "## Nearest existing has no `- Query: \"<the candidate as it was put to the index>\"` line"
        )
    if not ROWS_LINE.search(nearest):
        problems.append("## Nearest existing has no `- Rows: <n>` line; the count is the claim")
    if not PAPERS_FOUND_LINE.search(nearest):
        problems.append(
            "## Nearest existing has no `- Papers the query found: <n>` line; the row count "
            "saturates at the budget, so that one is the number that can be thin"
        )

    # 3. The seed names the file it came from.
    if not SEED_FILE.search(secs["Seed"]):
        problems.append(
            "## Seed names no file; a candidate that cannot be traced back was generated "
            "from what the model already knew"
        )

    # 4. Every reference tagged. This is the fabrication fence.
    for line in secs["References"].splitlines():
        if REFERENCE_LINE.match(line) and not (
            VERIFIED.search(line.rstrip()) or CANDIDATE in line or NOT_FOUND in line
        ):
            problems.append(f"reference carries no verify tag: {line.strip()[:70]}")

    # 5. No absence claims in what the skill wrote.
    problems += absence_claims(text)

    return problems


def check_log(text, pages_dir=None):
    """Return a list of failure strings for research/IDEAS.md."""
    problems = []
    secs = sections(text)

    for h in LOG_HEADINGS:
        if h not in secs:
            problems.append(f"missing heading: ## {h}")
    if problems:
        return problems

    if pages_dir is None:
        return problems

    have = set()
    if os.path.isdir(pages_dir):
        have = {f[:-3] for f in os.listdir(pages_dir) if f.endswith(".md")}
    for m in PROMOTED_LINE.finditer(secs["Promoted"]):
        slug = m.group(1)
        if slug not in have:
            problems.append(
                f"## Promoted names `{slug}`, which has no page in {pages_dir}; "
                "the log and the pages may not disagree"
            )
    return problems



def is_log(path):
    return os.path.basename(path) == "IDEAS.md"


def main(argv):
    if not argv:
        print("usage: check_ideas.py research/ideas/ | <page.md> ... | research/IDEAS.md")
        return 2
    paths = []
    for arg in argv:
        paths += pages_under(arg)
    if not paths:
        print("no idea pages found")
        return 0

    failed = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"FAIL {path}\n  - cannot read: {exc}")
            failed += 1
            continue
        if is_log(path):
            problems = check_log(text, os.path.join(os.path.dirname(path) or ".", "ideas"))
        else:
            problems = check(text)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"ok   {path}")
    print()
    print(f"{failed} of {len(paths)} files failed" if failed else f"all {len(paths)} files pass")
    return 1 if failed else 0


# --------------------------------------------------------------------------
# selftest


GOOD = """# Pre-image-only damage head

## Idea

Train the damage head on the pre-event image alone and use the post-event image
only as a consistency signal at training time, so that inference needs one
capture rather than a registered pair.

## Seed

- Kind: bit
- From: research/BITS.md § Bits § Damage is a property of the pair
- Line: "every card in this group takes the registered pre/post pair as the
  unit of prediction"

## What it flips

The group's bit says damage can only be read from a pre/post pair. If that is
false — if the post-event image is a training signal rather than an input —
then the method applies to the events where no usable pre-event capture exists,
which the datasets ledger says is most of them.

## Nearest existing

- Query: "single image post-disaster building damage classification without pre-event imagery"
- Papers the query found: 5 of 5 requested
- Rows: 30 of a 30-paper budget
- Nearest: Single-Image Damage Grading with Auxiliary Pretraining · 2023 · S2 `aa11bb` · verified
- Reading: it drops the pair at inference and at training both; the consistency
  objective here is what that paper has no equivalent of.

## What would have to be true

- The post-event image carries gradient signal the pre-event encoder can absorb — checkable: one run on xBD, a day.
- Single-capture accuracy stays within a few points of the paired baseline — not checkable before the experiment.

## Cheapest kill

- Experiment: train the consistency head on xBD, evaluate single-capture against the paired baseline.
- Kills it if: single-capture F1 falls more than 0.10 below the paired baseline.
- Costs: one GPU-day on lab data, no new labels.

## Typicality

The core is standard segmentation on a standard benchmark; the atypical
injection is the consistency objective, which comes from stereo matching.

## References

- Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery · 2019 · S2 `ec58b594` · verified
- Single-Image Damage Grading with Auxiliary Pretraining · 2023 · S2 `aa11bb` · verified
- Consistency Training for Stereo Correspondence · 2021 · _not found: checked s2, openalex, crossref_

## Status

Written 2026-09-16 by /ideas, round 1. Seed: bit:Damage is a property of the
pair. Not marked an increment on any run. Nearest existing: the query found 5 papers, 30 rows walked.
"""


GOOD_LOG = """# Ideas: post-disaster damage assessment under domain shift

## Log

### 2026-09-16 · /ideas · round 1
- Train the damage head on the pre-event image alone — seed: bit:Damage is a property of the pair
- Borrow the crop-stress field's per-region normalisation — seed: analog:wildfire#precision-agriculture

## Promoted

- pre-image-only-damage-head — Train the damage head on the pre-event image alone (2026-09-16)

## Dropped

- Borrow the crop-stress field's per-region normalisation — increment: nearest existing Region-Normalised Change Detection (S2 `cc22dd`), 4 rows (2026-09-16)

## Status

### 2026-09-16 · /ideas
- Seed kinds available: bits 2, analogs 1, contradictions 0, abandoned 0, personas 0
- Candidates generated: 2 (round 1: 2, round 2: 0)
- Promoted: 1 · increments: 1 · dropped by the user: 0
- Fields searched this run: none — the planner's fields were not approved
- Spread: per seed kind bits 1, analogs 1; per field of origin home 2
- What a third round would search: not proposed
"""


def selftest():
    failures = []

    def case(name, ok, detail=""):
        print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(name)

    got = check(GOOD)
    case("1  a complete idea page passes", not got, f"got {got}")

    # 2. A missing heading is the first thing checked, and it stops there.
    got = check(GOOD.replace("## Cheapest kill", "## Cheapest kills"))
    case("2  a missing heading fails, and names it",
         got == ["missing heading: ## Cheapest kill"], f"got {got}")

    # 3. An empty idea section is an area with a filename.
    got = check(GOOD.replace(
        "Train the damage head on the pre-event image alone and use the post-event image\n"
        "only as a consistency signal at training time, so that inference needs one\n"
        "capture rather than a registered pair.", ""))
    case("3  an empty ## Idea fails", any("## Idea is empty" in p for p in got), f"got {got}")

    # 4. The absence rule: no query, or no row count, and the section is an opinion.
    got = check(GOOD.replace(
        '- Query: "single image post-disaster building damage classification without pre-event imagery"\n',
        ""))
    case("4  ## Nearest existing with no query fails",
         any("no `- Query:" in p for p in got), f"got {got}")

    got = check(GOOD.replace("- Rows: 30 of a 30-paper budget\n", ""))
    case("4b ## Nearest existing with no row count fails",
         any("no `- Rows:" in p for p in got), f"got {got}")

    got = check(GOOD.replace("- Papers the query found: 5 of 5 requested\n", ""))
    case("4c a page with only the row count fails; the row count saturates",
         any("no `- Papers the query found:" in p for p in got), f"got {got}")

    # 5. A seed that names no file cannot be traced back.
    got = check(GOOD.replace(
        "- From: research/BITS.md § Bits § Damage is a property of the pair",
        "- From: the bits, somewhere"))
    case("5  a ## Seed naming no file fails",
         any("names no file" in p for p in got), f"got {got}")

    # 6. An untagged reference.
    got = check(GOOD.replace(
        "- Consistency Training for Stereo Correspondence · 2021 · _not found: checked s2, openalex, crossref_",
        "- Consistency Training for Stereo Correspondence · 2021"))
    case("6  a reference with no verify tag fails",
         any("no verify tag" in p for p in got), f"got {got}")

    # 7. The four absence words, in what the skill wrote.
    got = check(GOOD.replace(
        "it drops the pair at inference and at training both; the consistency\n"
        "  objective here is what that paper has no equivalent of.",
        "nobody has tried this; it is a real gap in the literature."))
    case("7  an absence claim fails, and names the word",
         sum("absence is mechanical" in p for p in got) == 2, f"got {got}")

    # 7b. A paper title carrying one of the four words is not an absence claim.
    titled = GOOD.replace(
        "- Single-Image Damage Grading with Auxiliary Pretraining · 2023 · S2 `aa11bb` · verified",
        "- A Novel Approach to Single-Image Damage Grading · 2023 · S2 `aa11bb` · verified").replace(
        "- Nearest: Single-Image Damage Grading with Auxiliary Pretraining · 2023 · S2 `aa11bb` · verified",
        "- Nearest: A Novel Approach to Single-Image Damage Grading · 2023 · S2 `aa11bb` · verified")
    case("7b a paper title carrying 'Novel' is not an absence claim",
         not check(titled), f"got {check(titled)}")

    # 8. The log.
    case("8  a complete log passes", not check_log(GOOD_LOG), f"got {check_log(GOOD_LOG)}")

    got = check_log(GOOD_LOG.replace("## Dropped", "## Set aside"))
    case("8b a log missing a heading fails",
         got == ["missing heading: ## Dropped"], f"got {got}")

    # 9. A promoted slug with no page. The pages directory is the real one under
    #    this repo, which holds no page yet, so every promoted slug is missing.
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    got = check_log(GOOD_LOG, os.path.join(here, "research", "ideas"))
    case("9  a promoted slug with no page fails",
         any("has no page" in p for p in got), f"got {got}")

    # 9b. A bare `- <slug>` line is still a promoted slug, and a prose bullet is not.
    bare = GOOD_LOG.replace(
        "- pre-image-only-damage-head — Train the damage head on the pre-event image alone (2026-09-16)",
        "- borrowed-region-normalisation")
    got = check_log(bare, os.path.join(here, "research", "ideas"))
    case("9b a bare `- <slug>` line does not escape the cross-check",
         any("borrowed-region-normalisation" in p for p in got), f"got {got}")

    prose = GOOD_LOG.replace(
        "- pre-image-only-damage-head — Train the damage head on the pre-event image alone (2026-09-16)",
        "- Nothing promoted this run.")
    got = check_log(prose, os.path.join(here, "research", "ideas"))
    case("9c a prose bullet under ## Promoted is not read as a slug", not got, f"got {got}")

    # 9d. A whole generated tree, on disk: the pages directory beside the three
    #     subdirectories a run fills. The plan and the persona file must not be
    #     read as idea pages, and the log's cross-check must find the page.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        research = os.path.join(tmp, "research")
        ideas = os.path.join(research, "ideas")
        for sub_dir in ("personas", "sections", "plans"):
            os.makedirs(os.path.join(ideas, sub_dir))
        with open(os.path.join(ideas, "pre-image-only-damage-head.md"), "w", encoding="utf-8") as fh:
            fh.write(GOOD)
        with open(os.path.join(research, "IDEAS.md"), "w", encoding="utf-8") as fh:
            fh.write(GOOD_LOG)
        for rel, body in (
            ("plans/diversity-2026-09-16.md", "# Diversity plan\n\n## What this set has in common\n\nOne seed kind.\n"),
            ("personas/2026-09-16-funder.md", "# A funder\n\n## Who\n\n- Persona: a funder\n"),
            ("sections/2026-09-16-stereo-matching.md", "# Stereo matching\n\n## Question\n\nWhat exists.\n"),
        ):
            with open(os.path.join(ideas, rel), "w", encoding="utf-8") as fh:
                fh.write(body)
        page_problems = [pr for path in pages_under(ideas)
                         for pr in check(open(path, encoding="utf-8").read())]
        case("9d a whole generated tree passes: plans, personas and sections are not pages",
             not page_problems, f"got {page_problems}")
        log_problems = check_log(GOOD_LOG, ideas)
        case("9e the log's cross-check finds the page in that tree",
             not log_problems, f"got {log_problems}")

    # 10. The templates carry every heading each checker requires.
    tdir = os.path.join(here, "templates", "research")
    with open(os.path.join(tdir, "idea.md"), encoding="utf-8") as fh:
        page_t = fh.read()
    case("10 the idea template carries every heading the checker requires",
         all(f"## {h}" in page_t for h in HEADINGS),
         f"missing {[h for h in HEADINGS if f'## {h}' not in page_t]}")
    with open(os.path.join(tdir, "ideas-log.md"), encoding="utf-8") as fh:
        log_t = fh.read()
    case("10b the log template carries every heading the checker requires",
         all(f"## {h}" in log_t for h in LOG_HEADINGS),
         f"missing {[h for h in LOG_HEADINGS if f'## {h}' not in log_t]}")

    print()
    print(f"{'FAILED' if failures else 'all green'}: {len(failures)} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(selftest() if args and args[0] == "--selftest" else main(args))
