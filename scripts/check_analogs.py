#!/usr/bin/env python3
"""Structural check on an analogs file, the output of /research-bearings:scout.

Chunk 3 has no judge tier. This is the whole automated done-check, and it is
built to run in a second: everything it asks can be decided by looking, so
nothing here needs a model.

What it enforces, and why each one is here:

  every paper line is checkable   an id, or the marker saying it would not
                                  resolve. A bare title is a claim nobody can
                                  check, which is the failure mode the verify
                                  step exists to close.
  the counts agree                ## Verification is a summary of ## Fields; if
                                  they disagree, one of them was written from
                                  memory.
  no home-field names             a field that shares your vocabulary shares
                                  your citation graph, and /snowball already
                                  covers it.
  five fields minimum             breadth is the deliverable.
  no absence claims               "unexplored", "gap", "novel", "nobody". Ten
                                  queries are not a census, and an absence
                                  claim becomes an empty cell in somebody's
                                  matrix.

Run: python3 scripts/check_analogs.py research/analogs/<slug>.md
     python3 scripts/check_analogs.py --selftest
"""

import os
import re
import sys

HEADINGS = ("Question", "Shape", "Fields", "Verification", "Status")
MIN_FIELDS = 5
UNRESOLVED = "_unresolved: not found by title_"
BANNED = ("unexplored", "gap", "novel", "nobody")
# "- <title> · <year> · ..." — the shape of a paper line under ## Fields.
PAPER_LINE = re.compile(r"^\s*-\s+.+\s·\s")
ID_ON_LINE = re.compile(r"S2 `[^`]+`|arXiv `[^`]+`|DOI `[^`]+`")


def sections(text):
    """Split on ## headings; returns {name: body}. Comments are stripped, so a
    template's own guidance never counts as content."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def vocabulary(project):
    """The home field's words, from research/QUESTION.md's ## Vocabulary.

    Absent is not a failure: an unframed run is a normal way to use the skill,
    and this check simply has less to say about it.
    """
    path = os.path.join(project, "research", "QUESTION.md")
    if not os.path.exists(path):
        return None
    body = sections(open(path, encoding="utf-8").read()).get("Vocabulary", "")
    words = set()
    for line in body.splitlines():
        line = line.strip().lstrip("-*").strip()
        # Take the term, not its gloss: "**bitemporal** — two captures" -> bitemporal
        term = re.split(r"[—:–-]", line, 1)[0]
        for w in re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}", term):
            words.add(w.lower())
    return words


def check(text, vocab=None):
    """Return a list of failure strings. Empty means the file passes."""
    problems = []
    secs = sections(text)

    for h in HEADINGS:
        if h not in secs:
            problems.append(f"missing heading: ## {h}")
    if problems:
        return problems

    fields = re.findall(r"^### +(.+)$", secs["Fields"], re.M)
    if len(fields) < MIN_FIELDS:
        problems.append(f"{len(fields)} fields; at least {MIN_FIELDS} are required")

    if vocab:
        for name in fields:
            hits = sorted({w for w in re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}", name) if w.lower() in vocab})
            if hits:
                problems.append(
                    f"field '{name}' uses the home vocabulary ({', '.join(hits)}); "
                    "a field that shares your words shares your citation graph"
                )

    papers = [ln for ln in secs["Fields"].splitlines() if PAPER_LINE.match(ln)]
    unchecked = [ln.strip() for ln in papers if not ID_ON_LINE.search(ln) and UNRESOLVED not in ln]
    for ln in unchecked:
        problems.append(f"paper line carries no id and no unresolved marker: {ln[:70]}")

    # ## Verification's own counts must match what ## Fields actually contains.
    stated = re.search(r"resolved\s+(\d+).*?unresolved\s+(\d+)", secs["Verification"], re.S | re.I)
    if not stated:
        problems.append("## Verification does not state 'resolved N ... unresolved M'")
    else:
        want_unresolved = sum(1 for ln in papers if UNRESOLVED in ln)
        want_resolved = len(papers) - want_unresolved - len(unchecked)
        got_resolved, got_unresolved = int(stated.group(1)), int(stated.group(2))
        if (got_resolved, got_unresolved) != (want_resolved, want_unresolved):
            problems.append(
                f"## Verification says resolved {got_resolved} / unresolved {got_unresolved}; "
                f"## Fields has {want_resolved} / {want_unresolved}"
            )

    problems += absence_claims(text)
    return problems


def authored_only(text):
    """The file with other people's words removed, for the absence scan.

    The rule is about what the scout writes, not what it quotes. Paper titles
    carry "Novel" constantly — "A Novel Approach to Crop Stress" is a title,
    not a claim about the field — and so does the `closest:` title on a
    Nearest existing line. Blank those out, keep the line numbering.
    """
    kept = []
    in_verification = False
    for line in re.sub(r"<!--.*?-->", "", text, flags=re.S).splitlines():
        if line.startswith("## "):
            in_verification = line[3:].strip() == "Verification"
        # ## Verification is a list of titles and nothing else.
        if in_verification or PAPER_LINE.match(line):
            kept.append("")
            continue
        kept.append(re.sub(r"closest:.*$", "closest:", line))
    return "\n".join(kept)


def absence_claims(text):
    """Where the file says the field lacks something, rather than what the
    search returned."""
    out = []
    body = authored_only(text).lower()
    for word in BANNED:
        for m in re.finditer(rf"\b{word}\b", body):
            line = body[:m.start()].count("\n") + 1
            out.append(
                f"line {line}: '{word}' — absence is mechanical here; "
                "report what the search returned and let the reader conclude"
            )
    return out


PASSING = """# Per-region change on paired overhead imagery

## Question
What else has solved this. Unframed — run on the invocation text as typed.

## Shape
Per-region change classification on paired captures, sparse labels.
Stripped: damage, disaster, satellite.

## Fields

### precision agriculture, crop stress from UAV flights
- Shares: paired captures of one scene over time
- Searched: `crop stress detection UAV multitemporal` → 10 rows
- Papers:
  - A Multitemporal UAV Pipeline for Crop Stress · 2021 · S2 `aaa111`
  - Field-Scale Change Detection in Orchards · 2019 · _unresolved: not found by title_
- Transfer: the labelling regime matches.
- Opportunity (speculative): borrow their weak-label scheme.
- Nearest existing: `weak labels paired overhead change` → 4 rows; closest: Some Paper (S2 `bbb222`)

### longitudinal medical imaging, lesion change
- Shares: two captures, per-region verdict
- Searched: `longitudinal lesion change segmentation` → 10 rows
- Papers:
  - Registration-Free Longitudinal Lesion Tracking · 2022 · S2 `ccc333`
- Transfer: registration-free comparison.
- Opportunity (speculative): drop the alignment step.
- Nearest existing: `registration free change overhead` → 2 rows; closest: Another (S2 `ddd444`)

### infrastructure inspection, crack progression
- Shares: sparse labels on repeat captures
- Searched: `crack progression inspection repeat imaging` → 8 rows
- Papers:
  - Crack Growth Monitoring From Repeat Photos · 2020 · S2 `eee555`
- Transfer: progression modelling.
- Opportunity (speculative): model severity as progression.
- Nearest existing: `progression severity overhead pairs` → 1 rows; closest: Third (S2 `fff666`)

### forestry, burn severity mapping
- Shares: per-region severity classes
- Searched: `burn severity mapping classes` → 9 rows
- Papers:
  - Burn Severity Classes From Repeat Survey · 2018 · S2 `ggg777`
- Transfer: ordinal severity.
- Opportunity (speculative): ordinal loss instead of categorical.
- Nearest existing: `ordinal severity overhead` → 3 rows; closest: Fourth (S2 `hhh888`)

### astronomy, transient detection in image subtraction
- Shares: difference imaging on aligned pairs
- Searched: `transient detection image subtraction survey` → 10 rows
- Papers:
  - Difference Imaging For Transient Surveys · 2017 · S2 `iii999`
- Transfer: subtraction artefact handling.
- Opportunity (speculative): treat artefacts as a class.
- Nearest existing: `subtraction artefacts overhead pairs` → 0 rows; closest: none returned

## Verification
- A Multitemporal UAV Pipeline for Crop Stress — resolved, S2 `aaa111`
- Field-Scale Change Detection in Orchards — unresolved
resolved 5, unresolved 1, checked 6

## Status
2026-09-14. Slug: shape-test. Touched 47. Unframed. Key present.
"""


def selftest():
    failures = []

    def case(name, ok, detail=""):
        print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))
        if not ok:
            failures.append(name)

    problems = check(PASSING)
    case("1  a well-formed file passes", problems == [], f"got {problems}")

    bare = PASSING.replace(
        "  - Field-Scale Change Detection in Orchards · 2019 · _unresolved: not found by title_",
        "  - Field-Scale Change Detection in Orchards · 2019",
    )
    problems = check(bare)
    case(
        "2  a paper line with no id and no marker fails",
        any("no id and no unresolved marker" in p for p in problems),
        f"got {problems}",
    )

    home = PASSING.replace(
        "### forestry, burn severity mapping",
        "### satellite damage assessment, another corner of it",
    )
    problems = check(home, vocab={"satellite", "damage"})
    case(
        "3  a field in the home vocabulary fails",
        any("home vocabulary" in p for p in problems),
        f"got {problems}",
    )

    claim = PASSING.replace(
        "- Transfer: ordinal severity.",
        "- Transfer: ordinal severity. Nobody has tried this on overhead imagery.",
    )
    problems = check(claim)
    case(
        "4  an absence claim fails",
        any("absence is mechanical" in p for p in problems),
        f"got {problems}",
    )

    titled = PASSING.replace(
        "  - Crack Growth Monitoring From Repeat Photos · 2020 · S2 `eee555`",
        "  - A Novel Approach to Crack Growth, and the Gap It Closes · 2020 · S2 `eee555`",
    ).replace(
        "closest: Fourth (S2 `hhh888`)", "closest: A Novel Ordinal Model (S2 `hhh888`)")
    problems = check(titled)
    case(
        "7  a paper title containing a banned word is not an absence claim",
        problems == [],
        f"got {problems}",
    )

    thin = PASSING.split("### infrastructure inspection")[0] + "\n## Verification\nresolved 3, unresolved 1\n\n## Status\nx\n"
    problems = check(thin)
    case(
        "5  fewer than five fields fails",
        any("at least 5 are required" in p for p in problems),
        f"got {problems}",
    )

    miscount = PASSING.replace("resolved 5, unresolved 1, checked 6", "resolved 9, unresolved 0, checked 9")
    problems = check(miscount)
    case(
        "6  verification counts that disagree with the fields fail",
        any("## Verification says" in p for p in problems),
        f"got {problems}",
    )

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
        print(__doc__.strip().splitlines()[-2].strip(), file=sys.stderr)
        return 2
    path = argv[0]
    if not os.path.exists(path):
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    text = open(path, encoding="utf-8").read()
    # The project root is two levels up from research/analogs/<file>.
    project = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(path))))
    problems = check(text, vocabulary(project))
    for p in problems:
        print(f"FAIL  {p}")
    if problems:
        print(f"\n{len(problems)} problem(s) in {path}")
        return 1
    print(f"ok  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
