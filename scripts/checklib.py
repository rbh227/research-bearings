#!/usr/bin/env python3
"""What every structural checker in this repo needs, in one place.

There are four checkers — cards, analogs, landscape, ideas — and each one asks
different questions of a different file. What they share is not the questions
but the *shape of the files*: `##` headings with comments that are guidance and
not content, paper lines in one fixed form, three verify tags, and four words
that may not be used to claim an absence.

Those shared pieces lived as copies in each checker until 2026-09-16, when a
review found `sections()` byte-identical in four files and the duplicated
message in two of them already drifted apart. The precedent for fixing it is
chunk 7's: `papers.py` imports the walker's helpers rather than copying them.

Import it by name — every checker sits next to this file, and Python puts a
script's own directory first on `sys.path`, so `import checklib` works from any
working directory and needs no package.

Not here: anything one checker alone asks. A rule with one caller belongs to its
caller, where it can be read beside the reason it exists.
"""

import re

# The four words an absence claim hides behind. One walk is not the literature:
# report what the search returned and let the reader conclude.
BANNED = ("unexplored", "gap", "novel", "nobody")

# "- <title> · <year> · ..." — one paper, in the form every file uses. The
# landscape and analog files call it a paper line; cards and idea pages call
# the same shape a reference line.
PAPER_LINE = re.compile(r"^\s*-\s+.+\s·\s")
REFERENCE_LINE = PAPER_LINE

# The three tags /verify writes. A paper line carrying none of them is unchecked.
VERIFIED = re.compile(r"·\s*verified\s*$")
CANDIDATE = "_candidate:"
NOT_FOUND = "_not found:"


def sections(text):
    """Split on ## headings; returns {name: body}.

    Comments are stripped first, so a template's own guidance never counts as
    content — a freshly copied template fails every content rule rather than
    passing as a filled file.
    """
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def banned_words(body):
    """Yield (word, line number) for every banned word in `body`.

    The caller masks what it must first — other people's titles are not absence
    claims — and writes its own message, because what a reader should do instead
    differs per file: an analog page reports what the search returned, an idea
    page reports the row count the walk came back with.
    """
    lowered = body.lower()
    for word in BANNED:
        for m in re.finditer(rf"\b{word}\b", lowered):
            yield word, lowered[: m.start()].count("\n") + 1
