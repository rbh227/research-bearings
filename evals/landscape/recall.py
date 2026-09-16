#!/usr/bin/env python3
"""Recall of a landscape run against the gold list, reported by gold heading.

    python3 evals/landscape/recall.py evals/landscape/runs/<topic> [--headings "A,B"] [--show-matches]

Reads every paper line under research/landscape/sections/*.md, surveys.md,
matrix.md and timeslice.md in the run, and every `- Author — fragment — year`
entry under the gold file's `## Papers — …` headings. A gold entry counts as
found when one found title carries enough of the fragment's content words:
at least 60 percent of them, or at least three when the fragment is long, and
never on the surname alone. The threshold is a choice, stated here and not
tuned against a run; the matches are printed so a human can audit them.

It never edits the gold file. Read evals/gold/wildfire-cv.md's Provenance
before reading the number: the gold list is a memory list, so a shared blind
spot passes.
"""

import os
import re
import sys

STOP = set("""a an the of for and or in on to from with by via using based towards toward
its their over under between across after before new large scale deep learning approach method
methods model models data dataset datasets study analysis assessment detection mapping prediction
imagery image images remote sensing satellite aerial network networks neural machine us""".split())
PAPER_LINE = re.compile(r"^\s*-\s+.+\s·\s")


def words(text):
    text = re.sub(r"\(.*?\)", " ", text)
    out = []
    for w in re.findall(r"[A-Za-z][A-Za-z0-9\-]+", text.lower()):
        w = w.strip("-")
        if len(w) > 2 and w not in STOP:
            out.append(w)
    return out


def gold_entries(path):
    """{heading: [(author, fragment, year, raw)]} for every ## Papers heading."""
    out, current = {}, None
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            h = line[3:].strip()
            current = h if h.lower().startswith("papers") else None
            if current:
                out[current] = []
        elif current and line.strip().startswith("- "):
            raw = line.strip()[2:]
            parts = [p.strip() for p in raw.split(" — ")]
            if len(parts) >= 2:
                out[current].append((parts[0], parts[1], parts[2] if len(parts) > 2 else "", raw))
    return out


def found_titles(run):
    titles = set()
    root = os.path.join(run, "research", "landscape")
    files = []
    sec = os.path.join(root, "sections")
    if os.path.isdir(sec):
        files += [os.path.join(sec, f) for f in os.listdir(sec) if f.endswith(".md")]
    files += [os.path.join(root, f) for f in ("surveys.md", "matrix.md", "timeslice.md")]
    for f in files:
        if not os.path.exists(f):
            continue
        for line in open(f, encoding="utf-8"):
            if PAPER_LINE.match(line):
                body = re.sub(r"^\s*-\s+", "", line)
                titles.add(body.split(" · ", 1)[0].strip())
    return titles


def matches(fragment, titles):
    want = words(fragment)
    if not want:
        return None
    need = max(2, min(3, int(round(0.6 * len(want)))))
    best, best_hit = None, 0
    for t in titles:
        have = set(words(t))
        hit = sum(1 for w in want if w in have)
        if hit > best_hit:
            best, best_hit = t, hit
    return best if best_hit >= need else None


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    run = argv[0]
    only = None
    show = "--show-matches" in argv
    if "--headings" in argv:
        only = [h.strip() for h in argv[argv.index("--headings") + 1].split(",")]
    gold = gold_entries(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gold", "wildfire-cv.md"))
    titles = found_titles(run)
    print(f"run: {run}\nfound titles: {len(titles)}\n")
    total_hit = total = 0
    for heading, entries in gold.items():
        if only and not any(o.lower() in heading.lower() for o in only):
            continue
        hits, misses = [], []
        for author, fragment, year, raw in entries:
            m = matches(fragment, titles)
            (hits if m else misses).append((raw, m))
        total_hit += len(hits)
        total += len(entries)
        print(f"## {heading}: {len(hits)}/{len(entries)}")
        if show:
            for raw, m in hits:
                print(f"  found  {raw}\n         ↳ {m}")
        for raw, m in misses:
            print(f"  MISS   {raw}")
        print()
    if total:
        print(f"recall over the headings scored: {total_hit}/{total} = {total_hit / total:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
