#!/usr/bin/env python3
"""Structural check on a landscape: the merger's matrix against the sections
it was built from. Seconds, no model.

What it enforces, and why each one is here:

  every cell says something checkable   a paper line, or the query that was
                                         run for it and what it returned. A
                                         blank cell is an absence claim with
                                         no query behind it.
  every paper line is checked            it ends in `verified` or carries the
                                         candidate marker. A bare title is a
                                         claim nobody can check.
  no absence words                       "unexplored", "gap", "novel",
                                         "nobody", outside paper titles.
  no title from nowhere                  every title in the matrix's cells
                                         appears in some section. The merger
                                         copies; it does not compose.

Run: python3 scripts/check_landscape.py research/landscape
     python3 scripts/check_landscape.py --selftest
"""

import os
import re
import sys

MATRIX_HEADINGS = ("Axes", "Matrix", "Cells", "Contradictions", "Sources", "Status")
SECTION_HEADINGS = ("Question", "Foundational", "Current", "Surveys", "What was searched", "What returned nothing")
BANNED = ("unexplored", "gap", "novel", "nobody")
PAPER_LINE = re.compile(r"^\s*-\s+.+\s·\s")
ZERO_LINE = re.compile(r"^\s*-\s+query\s+`[^`]+`\s+returned\s+.*\brows\b", re.I)
CHECKED = re.compile(r"·\s*verified\b|_candidate:")


def sections(text):
    """{heading: body}, comments stripped so template guidance never counts."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def title_of(line):
    """The title on a paper line: everything before the first ` · `."""
    body = re.sub(r"^\s*-\s+", "", line)
    return body.split(" · ", 1)[0].strip().lower()


def cells(body):
    """{cell name: [lines]} from a ## Cells body."""
    out, current = {}, None
    for line in body.splitlines():
        if line.startswith("### "):
            current = line[4:].strip()
            out[current] = []
        elif current is not None and line.strip():
            out[current].append(line)
    return out


def authored_only(text):
    """The matrix with copied material removed, for the absence scan: paper
    lines and the closest-title fragments carry other people's words."""
    kept = []
    for line in re.sub(r"<!--.*?-->", "", text, flags=re.S).splitlines():
        kept.append("" if PAPER_LINE.match(line) or ZERO_LINE.match(line) else line)
    return "\n".join(kept)


def absence_claims(text, where):
    out = []
    body = authored_only(text).lower()
    for word in BANNED:
        for m in re.finditer(rf"\b{word}\b", body):
            line = body[:m.start()].count("\n") + 1
            out.append(f"{where} line {line}: '{word}' — absence is mechanical here; a cell is a query and a count")
    return out


def check(matrix_text, section_texts):
    """Return a list of failure strings. `section_texts` is {name: text}."""
    problems = []
    secs = sections(matrix_text)
    for h in MATRIX_HEADINGS:
        if h not in secs:
            problems.append(f"matrix: missing heading ## {h}")
    if problems:
        return problems

    known_titles = set()
    for name, text in section_texts.items():
        ss = sections(text)
        for h in SECTION_HEADINGS:
            if h not in ss:
                problems.append(f"{name}: missing heading ## {h}")
        for h in ("Foundational", "Current", "Surveys"):
            for ln in ss.get(h, "").splitlines():
                if PAPER_LINE.match(ln):
                    known_titles.add(title_of(ln))
                    if not CHECKED.search(ln):
                        problems.append(f"{name}: paper line is neither verified nor a candidate: {ln.strip()[:70]}")
        # cells.md, and any section, may carry plain `- <title> · … · verified` lines elsewhere
        for ln in text.splitlines():
            if PAPER_LINE.match(ln) and CHECKED.search(ln):
                known_titles.add(title_of(ln))

    for cell, lines in cells(secs["Cells"]).items():
        papers = [ln for ln in lines if PAPER_LINE.match(ln) and not ZERO_LINE.match(ln)]
        zero = [ln for ln in lines if ZERO_LINE.match(ln)]
        if not papers and not zero:
            problems.append(f"matrix cell '{cell}' has neither a paper nor a 'query … returned … rows' line")
        for ln in papers:
            if not CHECKED.search(ln):
                problems.append(f"matrix cell '{cell}': paper line is neither verified nor a candidate: {ln.strip()[:70]}")
            if known_titles and title_of(ln) not in known_titles:
                problems.append(f"matrix cell '{cell}': title appears in no section: {title_of(ln)[:70]}")

    problems += absence_claims(matrix_text, "matrix")
    for name, text in section_texts.items():
        problems += absence_claims(text, name)
    return problems


SECTION_A = """# Formulations

## Question
How is the problem posed. field: home. mode: landscape
Query: `building damage assessment formulation` (blocked: none)

## Foundational
- Creating xBD: A Dataset for Assessing Building Damage · 2019 · CVPRW · centrality 4 · influential 37 · 19.5 cites/yr · both indexes · S2 `ec58` · verified

## Current
- Semi-Supervised Federated Learning for Assessing Building Damage · 2024 · ICC · centrality 1 · influential 0 · 2.0 cites/yr · s2 · S2 `e000` · verified
- A Paper I Remembered · 2023 · _no venue_ · _candidate: prefix match only, A Paper I Remembered Well (S2 `abc`)_

## Surveys
- A comprehensive review of earthquake-induced building damage detection · 2013 · ISPRS · centrality 2 · influential 20 · 9.0 cites/yr · both indexes · S2 `d308` · verified

## What was searched
- Query: `building damage assessment formulation`
- Stop: complete

## What returned nothing
every query and hop returned rows
"""

CELLS = """# Cells

## Question
cell probes

## Foundational

## Current

## Surveys

## What was searched
- Searched by /landscape

## What returned nothing
- `pixel classification weak labels` → 0 rows

### pixel classification × weak labels
- Searched: `pixel classification weak labels` → 0 rows

### pixel classification × full labels
- Searched: `pixel classification full labels` → 3 rows
- Creating xBD: A Dataset for Assessing Building Damage · 2019 · CVPRW · S2 `ec58` · verified
"""

PASSING = """# Landscape matrix: damage

## Axes
- Formulation: pixel classification — from sections/1-formulations.md
- Data regime: weak labels — from sections/2-data-regimes.md
- Data regime: full labels — from sections/2-data-regimes.md

## Matrix
| formulation \\ regime | weak labels | full labels |
|---|---|---|
| pixel classification | query `pixel classification weak labels` returned zero rows | 1 paper |

## Cells

### pixel classification × weak labels
- query `pixel classification weak labels` returned zero rows — sections/cells.md

### pixel classification × full labels
- Creating xBD: A Dataset for Assessing Building Damage · 2019 · CVPRW · centrality 4 · influential 37 · 19.5 cites/yr · both indexes · S2 `ec58` · verified — sections/1-formulations.md

## Contradictions
none found across 2 sections

## Sources
- sections/1-formulations.md — 4 papers
- sections/cells.md — 1 paper

## Status
2026-09-15. Cells 1 filled / 1 empty / 2 total. Contradictions 0. Degraded: none.
"""


def selftest():
    failures = []

    def case(name, ok, detail=""):
        print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(name)

    secs = {"sections/1-formulations.md": SECTION_A, "sections/cells.md": CELLS}
    problems = check(PASSING, secs)
    case("1  a well-formed matrix over well-formed sections passes", problems == [], f"got {problems}")

    blank = PASSING.replace(
        "- query `pixel classification weak labels` returned zero rows — sections/cells.md",
        "- nothing here yet")
    problems = check(blank, secs)
    case("2  a cell with neither a paper nor a zero-rows line fails",
         any("neither a paper nor" in p for p in problems), f"got {problems}")

    bare = PASSING.replace(" · S2 `ec58` · verified — sections/1-formulations.md", " · S2 `ec58` — sections/1-formulations.md")
    problems = check(bare, secs)
    case("3  a paper line without verified or candidate fails",
         any("neither verified nor a candidate" in p for p in problems), f"got {problems}")

    claim = PASSING.replace("none found across 2 sections", "none found; this cell is an unexplored gap")
    problems = check(claim, secs)
    case("4  a banned word in authored text fails, twice for two words",
         sum("absence is mechanical" in p for p in problems) == 2, f"got {problems}")

    stranger = PASSING.replace(
        "- Creating xBD: A Dataset for Assessing Building Damage · 2019 · CVPRW · centrality 4",
        "- A Novel Approach Nobody Wrote · 2019 · CVPRW · centrality 4")
    problems = check(stranger, secs)
    case("5  a matrix title absent from every section fails, and its own banned words do not count",
         any("appears in no section" in p for p in problems) and not any("absence is mechanical" in p for p in problems),
         f"got {problems}")

    thin = SECTION_A.replace("## What returned nothing\nevery query and hop returned rows\n", "")
    problems = check(PASSING, {"sections/1-formulations.md": thin, "sections/cells.md": CELLS})
    case("6  a section missing a heading fails", any("missing heading ## What returned nothing" in p for p in problems),
         f"got {problems}")

    problems = check(PASSING.replace("## Sources\n", "## Sourcez\n"), secs)
    case("7  a matrix missing a heading fails", any("missing heading ## Sources" in p for p in problems), f"got {problems}")

    print()
    if failures:
        print(f"{len(failures)} of 7 cases failed: {', '.join(failures)}")
        return 1
    print("7 of 7 cases passed")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if not argv:
        print("usage: check_landscape.py research/landscape | --selftest", file=sys.stderr)
        return 2
    root = argv[0]
    matrix = os.path.join(root, "matrix.md")
    sec_dir = os.path.join(root, "sections")
    if not os.path.exists(matrix):
        print(f"no matrix at {matrix}", file=sys.stderr)
        return 2
    section_texts = {}
    if os.path.isdir(sec_dir):
        for name in sorted(os.listdir(sec_dir)):
            if name.endswith(".md"):
                section_texts["sections/" + name] = open(os.path.join(sec_dir, name), encoding="utf-8").read()
    problems = check(open(matrix, encoding="utf-8").read(), section_texts)
    for p in problems:
        print(f"FAIL  {p}")
    if problems:
        print(f"\n{len(problems)} problem(s) in {root}")
        return 1
    print(f"ok  {root}: matrix and {len(section_texts)} sections agree")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
