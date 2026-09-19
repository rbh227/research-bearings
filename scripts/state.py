#!/usr/bin/env python3
"""The state of a research/ folder: what exists, what is stale, what comes next.

The one seam chunk 10 added. `/router` and the three composites (`/start`,
`/orient`, `/think`) read this and nothing else, so the front door's
recommendation is a lookup against a table rather than an opinion, and a grader
can hold the router's words against the JSON for the same folder.

The dependency table (`TABLE`) is the whole program: every loop command in the
loop's order, the contract files it writes, the files it needs first, and its
precondition in one sentence. The on-demand skills are rows too, flagged so the
router finds them by stated goal and never names them as the next move.

Run: python3 scripts/state.py [<research-dir>]     (default: ./research)
     python3 scripts/state.py --selftest

What each reported field is for:

  verb, root, exists    "state", the absolute folder read, and whether it was there.
  stage_reached         The latest stage with any present output, or null when the
                        folder is empty. The router prefers moves at this stage.
  files                 Every contract file or directory, keyed by its path under
                        research/. `state` is one of `present`, `absent`,
                        `present-but-malformed`; a directory-shaped entry carries
                        `count`, `newest`, `oldest`, and the names of malformed pages.
                        `missing_headings` names what the template has and the file
                        does not — a half-written file is routed to as a repair, not
                        overwritten by a rerun. `date` is ISO or `unknown`.
  counts                cards, analog_pages, idea_pages, premortems, specs, baselines,
                        experiment_pages, results, critiques.
  staleness             Per derived file that exists: how many upstream files are
                        newer than it, the newest upstream date, which inputs were
                        counted, and `not_named` — the upstream pages the file never
                        mentions, because a date is a proxy and BITS.md names the
                        cards it drew on. Both facts go in a composite's
                        rerun/keep/stop question, and they can disagree.
  pending               Idea pages with no pre-mortem, so `/premortem` is ready even
                        when some pre-mortems exist.
  moves                 Every row in loop order with its status:
                          ready    preconditions met, output absent
                          stale    met, output present, upstream files newer than it
                          repeat   met, output present, and the command adds rather
                                   than rewrites (cards, analog pages, ideas, ...)
                          done     met, output present and current
                          blocked  output absent and a precondition unmet; `missing`
                                   names it. An output that exists is judged as a file.
                          skipped  output absent but a later stage has output; the
                                   file is required downstream, so it is a repair
                        Each carries `precondition` in one sentence and `writes`.
  recommended           The moves a router may offer: ready, stale and repeat rows,
                        in loop order, never on-demand rows and never skipped ones.
  repairs               Malformed files and skipped required files, each with the
                        command that writes it.
  on_demand             The on-demand skills — verify, audit, critique, reviews,
                        replicate, and the two ledgers, datasets and groups — and
                        whether each could run now.

Never writes: not to the folder it reads, not anywhere. The selftest snapshots
the fixture tree before and after and asserts it.

Standard library only, plus `checklib` beside it for the heading split.
"""

import datetime
import json
import os
import re
import sys

import checklib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates", "research")

STAGES = ("questions", "gathering", "processing", "selection", "experiments")

# path under research/ -> (template name, directory-shaped?)
FILES = {
    "CONTEXT.md": ("CONTEXT.md", False),
    "CONNECTIONS.md": ("CONNECTIONS.md", False),
    "QUESTION.md": ("QUESTION.md", False),
    "framing-log.md": ("framing-log.md", False),
    "landscape/surveys.md": ("surveys.md", False),
    "landscape/matrix.md": ("matrix.md", False),
    "landscape/timeslice.md": ("timeslice.md", False),
    "landscape/datasets.md": ("datasets.md", False),
    "landscape/groups.md": ("groups.md", False),
    "landscape/reviews.md": ("reviews.md", False),
    "analogs/": ("analogs.md", True),
    "papers/": ("card.md", True),
    "BITS.md": ("bits.md", False),
    "IDEAS.md": ("ideas-log.md", False),
    "ideas/": ("idea.md", True),
    "premortems/": ("premortem.md", True),
    "RANKING.md": ("ranking.md", False),
    "specs/": ("heilmeier.md", True),
    "baselines/": ("baseline.md", True),
    "experiments/": ("experiment.md", True),
    "NOTEBOOK.md": ("notebook.md", False),
    "results/": ("result.md", True),
    "critiques/": ("critique.md", True),
}

# What the counts block calls each directory.
COUNT_NAMES = {
    "papers/": "cards", "analogs/": "analog_pages", "ideas/": "idea_pages",
    "premortems/": "premortems", "specs/": "specs", "baselines/": "baselines",
    "experiments/": "experiment_pages", "results/": "results", "critiques/": "critiques",
}

# A precondition: ("all", [files]) every file present; ("any", [files]) at least
# one; ("count", path, n) a directory with at least n pages.
ALL, ANY, COUNT = "all", "any", "count"

# The loop, written down as data. Fields: command, stage, writes, needs,
# precondition sentence, repeatable, extra upstream for staleness, on_demand.
TABLE = [
    dict(command="setup", stage="questions", writes=["CONTEXT.md", "CONNECTIONS.md"],
         needs=[], precondition="Nothing; this is the first step."),
    dict(command="frame", stage="questions", writes=["QUESTION.md", "framing-log.md"],
         needs=[(ALL, ["CONTEXT.md"])],
         precondition="CONTEXT.md must exist; setup writes it."),
    dict(command="surveys", stage="gathering", writes=["landscape/surveys.md"],
         needs=[(ALL, ["QUESTION.md"])],
         precondition="QUESTION.md must exist; frame writes it."),
    dict(command="landscape", stage="gathering",
         writes=["landscape/matrix.md", "landscape/timeslice.md"],
         needs=[(ALL, ["QUESTION.md"])],
         precondition="QUESTION.md must exist; frame writes it. surveys.md is read if present.",
         upstream=["QUESTION.md", "landscape/surveys.md"]),
    dict(command="scout", stage="gathering", writes=["analogs/"],
         needs=[(ALL, ["QUESTION.md"])],
         precondition="QUESTION.md must exist; frame writes it.", repeatable=True),
    dict(command="read", stage="processing", writes=["papers/"],
         needs=[(ALL, ["landscape/matrix.md"])],
         precondition="landscape/matrix.md must exist; landscape writes it. Reading proposes from the matrix.",
         repeatable=True),
    dict(command="bits", stage="processing", writes=["BITS.md"],
         needs=[(COUNT, "papers/", 2)],
         precondition="At least two cards under papers/ that can share a thesis; read writes them."),
    dict(command="brainstorm", stage="processing", writes=["IDEAS.md"],
         needs=[(ALL, ["QUESTION.md"])],
         precondition="QUESTION.md must exist; frame writes it.", repeatable=True),
    dict(command="ideas", stage="processing", writes=["ideas/"],
         needs=[(ANY, ["BITS.md", "analogs/", "IDEAS.md", "landscape/matrix.md"])],
         precondition="At least one seed source: BITS.md, an analog page, IDEAS.md, or the matrix's contradictions.",
         repeatable=True),
    dict(command="premortem", stage="selection", writes=["premortems/"],
         needs=[(COUNT, "ideas/", 1)],
         precondition="At least one idea page under ideas/; ideas writes them.", repeatable=True),
    dict(command="rank", stage="selection", writes=["RANKING.md"],
         needs=[(COUNT, "premortems/", 1)],
         precondition="At least one pre-mortem under premortems/; premortem writes them.",
         upstream=["premortems/", "ideas/", "results/"]),
    dict(command="spec", stage="selection", writes=["specs/"],
         needs=[(ALL, ["RANKING.md"])],
         precondition="RANKING.md with survivors; rank writes it.", repeatable=True),
    dict(command="baseline", stage="experiments", writes=["baselines/"],
         needs=[(COUNT, "papers/", 1)],
         precondition="A card carrying the number to beat; read writes cards.", repeatable=True),
    dict(command="design", stage="experiments", writes=["experiments/"],
         needs=[(ALL, ["RANKING.md"])],
         precondition="A ranked idea whose pre-mortem did not say not executable; rank writes RANKING.md.",
         repeatable=True),
    dict(command="log", stage="experiments", writes=["NOTEBOOK.md"],
         needs=[(COUNT, "experiments/", 1)],
         precondition="An experiment page under experiments/; design writes them.", repeatable=True),
    dict(command="result", stage="experiments", writes=["results/"],
         needs=[(ALL, ["NOTEBOOK.md"])],
         precondition="NOTEBOOK.md with an ingested run; log writes it.", repeatable=True),
    # On demand: reachable by stated goal, never the next move. datasets and
    # groups are here by the spec's word (story 11), not the loop table's
    # first draft — a ledger is asked for, never the next step.
    dict(command="datasets", stage="processing", writes=["landscape/datasets.md"],
         needs=[(COUNT, "papers/", 1)],
         precondition="At least one card under papers/; read writes them.", on_demand=True),
    dict(command="groups", stage="processing", writes=["landscape/groups.md"],
         needs=[(COUNT, "papers/", 1)],
         precondition="At least one card under papers/; read writes them.", on_demand=True),
    dict(command="verify", stage="processing", writes=[], needs=[(ANY, ["QUESTION.md"])],
         precondition="Any file under research/ that names papers.", on_demand=True, repeatable=True),
    dict(command="audit", stage="processing", writes=[], needs=[(COUNT, "papers/", 1)],
         precondition="One card to audit; read writes cards.", on_demand=True, repeatable=True),
    dict(command="critique", stage="processing", writes=["critiques/"], needs=[(ANY, ["QUESTION.md"])],
         precondition="One file under research/ to attack.", on_demand=True, repeatable=True),
    dict(command="reviews", stage="processing", writes=["landscape/reviews.md"],
         needs=[(COUNT, "papers/", 1)],
         precondition="Cards to carry the notes; read writes them.", on_demand=True, repeatable=True),
    dict(command="replicate", stage="experiments", writes=["baselines/"], needs=[(COUNT, "papers/", 1)],
         precondition="A card for a paper you are not building on.", on_demand=True, repeatable=True),
]

# Files some row needs with ALL or COUNT: absent while a later stage has output,
# they are a repair rather than a fresh move.
REQUIRED = set()
for _row in TABLE:
    for _need in _row["needs"]:
        if _need[0] == ALL:
            REQUIRED.update(_need[1])
        elif _need[0] == COUNT:
            REQUIRED.add(_need[1])


def stat_fn(path):
    """Split out so the selftest can make a date unreadable."""
    return os.stat(path)


def mtime(path):
    try:
        return stat_fn(path).st_mtime
    except OSError:
        return None


def iso(ts):
    if ts is None:
        return "unknown"
    return datetime.datetime.fromtimestamp(ts).replace(microsecond=0).isoformat()


def template_headings(name):
    path = os.path.join(TEMPLATES, name)
    try:
        with open(path, encoding="utf-8") as fh:
            return [line[3:].strip() for line in fh if line.startswith("## ")], path
    except OSError:
        return None, path


def missing_headings(path, required):
    if required is None:
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            present = set(checklib.sections(fh.read()))
    except OSError:
        return list(required)
    return [h for h in required if h not in present]


def absent_entry(is_dir):
    """The one shape an absent file or directory reports, wherever it is absent."""
    if is_dir:
        return {"state": "absent", "count": 0, "pages": [], "newest": None, "oldest": None,
                "malformed": [], "dates_unknown": 0}
    return {"state": "absent", "date": None}


def inspect_file(root, rel, template):
    path = os.path.join(root, rel)
    required, tpath = template_headings(template)
    entry = {"template": os.path.relpath(tpath, ROOT) if required is not None else "not found"}
    if not os.path.isfile(path):
        entry.update(absent_entry(False))
        return entry
    missing = missing_headings(path, required)
    entry.update(state="present-but-malformed" if missing else "present",
                 date=iso(mtime(path)), missing_headings=missing)
    return entry


def inspect_dir(root, rel, template):
    path = os.path.join(root, rel.rstrip("/"))
    required, tpath = template_headings(template)
    entry = {"template": os.path.relpath(tpath, ROOT) if required is not None else "not found"}
    if not os.path.isdir(path):
        entry.update(absent_entry(True))
        return entry
    pages = [p for p in checklib.pages_under(path) if not os.path.islink(p)]
    times = [t for t in (mtime(p) for p in pages) if t is not None]
    malformed = [os.path.basename(p) for p in pages if missing_headings(p, required)]
    entry.update(
        state="present" if pages else "absent",
        count=len(pages),
        pages=sorted(os.path.splitext(os.path.basename(p))[0] for p in pages),
        newest=iso(max(times)) if times else None,
        oldest=iso(min(times)) if times else None,
        malformed=sorted(malformed),
        dates_unknown=len(pages) - len(times),
    )
    return entry


def present(files, rel):
    return files[rel]["state"] in ("present", "present-but-malformed")


def need_met(files, need):
    kind = need[0]
    if kind == ALL:
        missing = [f for f in need[1] if not present(files, f)]
        return not missing, missing
    if kind == ANY:
        ok = any(present(files, f) for f in need[1])
        return ok, [] if ok else list(need[1])
    if kind == COUNT:
        ok = files[need[1]].get("count", 0) >= need[2]
        return ok, [] if ok else ["{} (need {}, have {})".format(need[1], need[2], files[need[1]].get("count", 0))]
    raise ValueError(kind)


def upstream_times(root, files, inputs):
    """Every (path, mtime) among the inputs: a file's own, or each page under a directory."""
    out = []
    for rel in inputs:
        if rel.endswith("/"):
            path = os.path.join(root, rel.rstrip("/"))
            if os.path.isdir(path):
                for p in checklib.pages_under(path):
                    out.append((os.path.relpath(p, root), mtime(p)))
        else:
            path = os.path.join(root, rel)
            if os.path.isfile(path):
                out.append((rel, mtime(path)))
    return out


def inputs_of(row):
    seen = []
    for need in row["needs"]:
        names = need[1] if need[0] in (ALL, ANY) else [need[1]]
        for n in names:
            if n not in seen:
                seen.append(n)
    for n in row.get("upstream", []):
        if n not in seen:
            seen.append(n)
    return seen


def staleness_of(root, files, row):
    """For a single-file output that exists: upstream files newer than it."""
    target = row["writes"][0]
    own = mtime(os.path.join(root, target))
    if own is None:
        return {"upstream_newer": "unknown", "newest_upstream": "unknown", "upstream": inputs_of(row)}
    newer = [(p, t) for p, t in upstream_times(root, files, inputs_of(row)) if t is not None and t > own]
    # A date is a proxy. A derived file that names what it drew on — BITS.md
    # names its cards under ## Groups, RANKING.md names its ideas — can be
    # asked directly: which upstream pages does it never mention? Found on
    # first contact (chunk 10): the damage BITS.md was "stale" by two cards
    # it already covered.
    try:
        with open(os.path.join(root, target), encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        text = ""
    # A slug counts as named only as a whole token: `xbd` inside
    # `gupta-2019-xbd` is not a mention of a card called `xbd`.
    not_named = []
    for rel in inputs_of(row):
        if rel.endswith("/"):
            for stem in files[rel].get("pages", []):
                if not re.search(r"(?<![\w-])" + re.escape(stem) + r"(?![\w-])", text):
                    not_named.append(rel + stem + ".md")
    return {
        "upstream_newer": len(newer),
        "newest_upstream": iso(max(t for _, t in newer)) if newer else None,
        "newer_files": sorted(p for p, _ in newer),
        "not_named": sorted(not_named),
        "upstream": inputs_of(row),
    }


def read(root):
    root = os.path.abspath(root)
    out = {"verb": "state", "root": root, "exists": os.path.isdir(root)}
    files = {}
    for rel, (template, is_dir) in FILES.items():
        files[rel] = (inspect_dir if is_dir else inspect_file)(root, rel, template) if out["exists"] \
            else absent_entry(is_dir)
        files[rel]["written_by"] = next((r["command"] for r in TABLE if rel in r["writes"]), None)
    out["files"] = files
    out["counts"] = {name: files[rel]["count"] for rel, name in COUNT_NAMES.items()}

    # Stage reached: the latest stage any row's output is present in. And the
    # last loop row with output, in table order, because "skipped" is about
    # rows, not stages: a question page beside a missing context file means
    # setup was skipped even though both sit in the questions stage.
    reached, last_with_output = None, -1
    for i, row in enumerate(TABLE):
        if row.get("on_demand"):
            continue
        if any(present(files, w) for w in row["writes"]):
            last_with_output = i
            if reached is None or STAGES.index(row["stage"]) > STAGES.index(reached):
                reached = row["stage"]
    out["stage_reached"] = reached

    # Pending pre-mortems: idea slugs with no premortems/<slug>-<date>.md. The
    # date suffix is matched as a date, not as "anything after a dash": an idea
    # `pre` must not be satisfied by `pre-image-only-head-2026-09-17`.
    idea_slugs = files["ideas/"]["pages"]
    pm_pages = files["premortems/"]["pages"]
    pending = [s for s in idea_slugs
               if not any(p == s or re.fullmatch(re.escape(s) + r"-\d{4}-\d{2}-\d{2}(-\d+)?", p)
                          for p in pm_pages)]
    out["pending"] = {"premortem": pending}

    moves, staleness, repairs, on_demand = [], {}, [], []
    for i, row in enumerate(TABLE):
        met, missing = True, []
        for need in row["needs"]:
            ok, miss = need_met(files, need)
            if not ok:
                met = False
                missing.extend(miss)
        exists = any(present(files, w) for w in row["writes"])
        move = {"command": row["command"], "stage": row["stage"], "writes": row["writes"],
                "precondition": row["precondition"], "output_exists": exists}
        if row.get("on_demand"):
            move["precondition_met"] = met
            move["missing"] = missing
            on_demand.append(move)
            continue
        later_output = last_with_output > i
        required_absent = [w for w in row["writes"] if w in REQUIRED and not present(files, w)]
        # A file that exists is judged as a file — done, stale or repeat — even
        # when what it was built from is now missing; that absence is the
        # upstream row's repair, not this row's block. Blocked is for a step
        # that has not run and cannot.
        if not met and not exists:
            move["status"], move["missing"] = "blocked", missing
        elif not exists and later_output and required_absent:
            move["status"] = "skipped"
            for w in required_absent:
                repairs.append({"file": w, "command": row["command"], "kind": "missing upstream",
                                "detail": "absent while {} has output".format(TABLE[last_with_output]["command"])})
        elif not exists:
            move["status"] = "ready"
        elif row["command"] == "premortem" and pending:
            move["status"] = "ready"
            move["pending"] = pending
        elif row.get("repeatable"):
            move["status"] = "repeat"
        else:
            st = staleness_of(root, files, row)
            staleness[row["writes"][0]] = st
            move["status"] = "stale" if st["upstream_newer"] not in (0, "unknown") else "done"
            if st["upstream_newer"] != 0:
                move["staleness"] = st
        moves.append(move)

    for rel, entry in files.items():
        if entry["state"] == "present-but-malformed":
            repairs.append({"file": rel, "command": entry["written_by"], "kind": "malformed",
                            "missing_headings": entry["missing_headings"]})
        for name in entry.get("malformed", []):
            repairs.append({"file": rel + name, "command": entry["written_by"], "kind": "malformed"})

    out["moves"] = moves
    out["staleness"] = staleness
    out["recommended"] = [m["command"] for m in moves if m["status"] in ("ready", "stale", "repeat")]
    out["repairs"] = repairs
    out["on_demand"] = on_demand
    out["empty"] = not out["exists"] or not any(present(files, r) for r in files)
    if out["empty"]:
        out["recommended"] = ["setup"]
    return out


# --------------------------------------------------------------------------- selftest

def selftest():
    """Fixture folders in a temp dir, then the JSON shape, the moves and the
    staleness counts. Never internals: what is asserted is what the router reads."""
    import tempfile
    import time

    failures, total = [], [0]

    def case(name, ok, detail=""):
        total[0] += 1
        print("{} {}".format("ok  " if ok else "FAIL", name) + (" — {}".format(detail) if detail and not ok else ""))
        if not ok:
            failures.append(name)

    def filled(template):
        heads, _ = template_headings(template)
        return "".join("## {}\n\nfilled.\n\n".format(h) for h in heads)

    def status(out, command):
        return next(m["status"] for m in out["moves"] if m["command"] == command)

    with tempfile.TemporaryDirectory() as tmp:
        def write(folder, rel, body, age=0):
            path = os.path.join(tmp, folder, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
            if age:
                t = time.time() - age
                os.utime(path, (t, t))
            return path

        # 1. Empty: no folder at all.
        out = read(os.path.join(tmp, "nowhere", "research"))
        case("1  the JSON shape is the documented one",
             set(out) >= {"verb", "root", "exists", "stage_reached", "files", "counts", "staleness",
                          "pending", "moves", "recommended", "repairs", "on_demand", "empty"}
             and out["verb"] == "state", "got {}".format(sorted(out)))
        case("2  no folder is the empty state and routes to setup",
             out["exists"] is False and out["empty"] and out["recommended"] == ["setup"]
             and out["stage_reached"] is None)

        # 2. Context only.
        write("ctx", "CONTEXT.md", filled("CONTEXT.md"))
        out = read(os.path.join(tmp, "ctx"))
        case("3  context only: frame is ready, surveys is blocked on QUESTION.md",
             status(out, "frame") == "ready" and status(out, "surveys") == "blocked"
             and "QUESTION.md" in next(m["missing"] for m in out["moves"] if m["command"] == "surveys"))
        case("4  recommended is exactly frame", out["recommended"] == ["frame"], str(out["recommended"]))
        case("5  stage reached is questions", out["stage_reached"] == "questions")

        # 3. Framed.
        write("framed", "CONTEXT.md", filled("CONTEXT.md"))
        write("framed", "QUESTION.md", filled("QUESTION.md"))
        out = read(os.path.join(tmp, "framed"))
        case("6  framed: surveys, landscape, scout and brainstorm are ready, read is blocked",
             all(status(out, c) == "ready" for c in ("surveys", "landscape", "scout", "brainstorm"))
             and status(out, "read") == "blocked")
        case("7  recommended is in loop order",
             out["recommended"] == ["surveys", "landscape", "scout", "brainstorm"], str(out["recommended"]))
        case("8  frame is done, not stale, when CONTEXT.md is older",
             status(out, "frame") == "done")

        # 4. Framed with a landscape (the wildfire shape): no CONTEXT.md.
        write("wild", "QUESTION.md", filled("QUESTION.md"))
        write("wild", "landscape/surveys.md", filled("surveys.md"))
        write("wild", "landscape/matrix.md", filled("matrix.md"))
        write("wild", "landscape/timeslice.md", filled("timeslice.md"))
        out = read(os.path.join(tmp, "wild"))
        case("9  wildfire shape: read is ready with the matrix as its precondition",
             status(out, "read") == "ready"
             and "matrix.md" in next(m["precondition"] for m in out["moves"] if m["command"] == "read"))
        case("10 stage reached is gathering", out["stage_reached"] == "gathering")
        case("11 a missing CONTEXT.md with downstream output is a repair, not a move",
             status(out, "setup") == "skipped" and "setup" not in out["recommended"]
             and any(r["file"] == "CONTEXT.md" and r["kind"] == "missing upstream" for r in out["repairs"]))

        # 5. The damage shape: cards newer than BITS.md.
        write("dmg", "QUESTION.md", filled("QUESTION.md"))
        write("dmg", "landscape/surveys.md", filled("surveys.md"))
        write("dmg", "landscape/matrix.md", filled("matrix.md"))
        write("dmg", "landscape/timeslice.md", filled("timeslice.md"))
        write("dmg", "BITS.md", filled("bits.md"), age=3 * 86400)
        write("dmg", "papers/a-2019.md", filled("card.md"), age=5 * 86400)
        write("dmg", "papers/b-2020.md", filled("card.md"), age=86400)
        write("dmg", "papers/c-2021.md", filled("card.md"))
        write("dmg", "papers/notes/a-2019.reading.md", "## What was read\n")
        out = read(os.path.join(tmp, "dmg"))
        case("12 three cards counted, and the notes subdirectory is not a card",
             out["counts"]["cards"] == 3, str(out["counts"]))
        case("13 the damage shape is a fork: read repeats, bits is stale, ideas is ready",
             status(out, "read") == "repeat" and status(out, "bits") == "stale"
             and status(out, "ideas") == "ready"
             and {"read", "bits", "ideas"} <= set(out["recommended"]), str(out["recommended"]))
        st = out["staleness"].get("BITS.md", {})
        case("14 two cards are newer than BITS.md, and the newest card's date is named",
             st.get("upstream_newer") == 2 and st.get("newest_upstream") == out["files"]["papers/"]["newest"]
             and sorted(st.get("newer_files", [])) == ["papers/b-2020.md", "papers/c-2021.md"], str(st))
        case("15 stage reached is processing", out["stage_reached"] == "processing")
        case("15b a stale file also says which upstream pages it never names",
             st.get("not_named") == ["papers/a-2019.md", "papers/b-2020.md", "papers/c-2021.md"], str(st))
        # The same folder, with a bits file that names two of its three cards:
        # the date proxy still says two newer, the text says one not named.
        write("dmg2", "QUESTION.md", filled("QUESTION.md"))
        write("dmg2", "landscape/matrix.md", filled("matrix.md"))
        write("dmg2", "BITS.md", filled("bits.md") + "\n- group one: a-2019, b-2020\n", age=3 * 86400)
        write("dmg2", "papers/a-2019.md", filled("card.md"), age=5 * 86400)
        write("dmg2", "papers/b-2020.md", filled("card.md"), age=86400)
        write("dmg2", "papers/c-2021.md", filled("card.md"))
        st2 = read(os.path.join(tmp, "dmg2"))["staleness"]["BITS.md"]
        case("15c date and text are reported side by side, and can disagree",
             st2["upstream_newer"] == 2 and st2["not_named"] == ["papers/c-2021.md"], str(st2))
        case("16 premortem is blocked with no idea pages, rank is blocked with no pre-mortems",
             status(out, "premortem") == "blocked" and status(out, "rank") == "blocked")

        # 6. Present but malformed.
        write("bad", "CONTEXT.md", filled("CONTEXT.md"))
        write("bad", "QUESTION.md", "## Question\n\nx\n\n## Vocabulary\n\ny\n")
        out = read(os.path.join(tmp, "bad"))
        case("17 a file missing headings is present-but-malformed, never absent",
             out["files"]["QUESTION.md"]["state"] == "present-but-malformed"
             and "The ladder" in out["files"]["QUESTION.md"]["missing_headings"])
        case("18 a malformed file still satisfies presence: surveys is ready",
             status(out, "surveys") == "ready")
        case("19 the repair names the file and the skill that writes it",
             any(r["file"] == "QUESTION.md" and r["command"] == "frame" and r["kind"] == "malformed"
                 for r in out["repairs"]), str(out["repairs"]))
        case("20 frame is done, not ready: a repair is not a rerun",
             status(out, "frame") == "done" and "frame" not in out["recommended"])

        # 7. Pending pre-mortems.
        write("sel", "QUESTION.md", filled("QUESTION.md"))
        write("sel", "BITS.md", filled("bits.md"))
        write("sel", "ideas/one.md", filled("idea.md"))
        write("sel", "ideas/two.md", filled("idea.md"))
        write("sel", "premortems/one-2026-09-18.md", filled("premortem.md"))
        out = read(os.path.join(tmp, "sel"))
        case("21 an idea with no pre-mortem keeps premortem ready and is named",
             status(out, "premortem") == "ready" and out["pending"]["premortem"] == ["two"])
        case("22 rank is ready once one pre-mortem exists", status(out, "rank") == "ready")
        # An idea whose slug is a prefix of another's is not covered by the
        # other's pre-mortem; a slug that is a substring of a longer token is
        # not named by it.
        write("sel", "ideas/pre.md", filled("idea.md"))
        write("sel", "ideas/pre-image-head.md", filled("idea.md"))
        write("sel", "premortems/pre-image-head-2026-09-18.md", filled("premortem.md"))
        out = read(os.path.join(tmp, "sel"))
        case("22b a prefix slug is still pending when only the longer slug has a pre-mortem",
             sorted(out["pending"]["premortem"]) == ["pre", "two"], str(out["pending"]))
        write("dmg2", "papers/xbd.md", filled("card.md"))
        write("dmg2", "BITS.md", filled("bits.md") + "\n- group one: a-2019, b-2020, gupta-2019-xbd\n", age=3 * 86400)
        st3 = read(os.path.join(tmp, "dmg2"))["staleness"]["BITS.md"]
        case("22c a slug inside a longer token is not a mention",
             "papers/xbd.md" in st3["not_named"] and "papers/a-2019.md" not in st3["not_named"], str(st3))

        # 8. An unreadable date.
        global stat_fn
        real_stat = stat_fn
        target = os.path.join(tmp, "framed", "QUESTION.md")

        def flaky(path):
            if os.path.abspath(path) == target:
                raise OSError("no date")
            return real_stat(path)
        stat_fn = flaky
        try:
            out = read(os.path.join(tmp, "framed"))
        finally:
            stat_fn = real_stat
        case("23 a date that cannot be read is `unknown`, and the file is still present",
             out["files"]["QUESTION.md"]["date"] == "unknown"
             and out["files"]["QUESTION.md"]["state"] == "present")

        # 9. On demand rows are never recommended.
        out = read(os.path.join(tmp, "dmg"))
        on_demand = {"verify", "audit", "critique", "reviews", "replicate", "datasets", "groups"}
        case("24 on-demand skills are listed with their readiness and never recommended",
             {m["command"] for m in out["on_demand"]} == on_demand
             and all(m["precondition_met"] for m in out["on_demand"])
             and not (on_demand & set(out["recommended"])), str(out["recommended"]))
        case("24b a ledger is never the next move: datasets and groups are not in recommended with one card",
             not ({"datasets", "groups"} & set(out["recommended"])))

        # 12. Question only (no CONTEXT.md): setup was skipped within its own
        # stage, and the next move is surveys, not setup.
        write("qonly", "QUESTION.md", filled("QUESTION.md"))
        out = read(os.path.join(tmp, "qonly"))
        case("24c a question beside a missing context file makes setup a repair, not the next move",
             status(out, "setup") == "skipped" and out["recommended"][0] == "surveys"
             and any(r["file"] == "CONTEXT.md" and r["kind"] == "missing upstream" for r in out["repairs"]),
             str((status(out, "setup"), out["recommended"], out["repairs"])))
        case("24d a file that exists is done, not blocked, when its own input is missing",
             status(out, "frame") == "done", status(out, "frame"))

        # 10. Nothing written.
        before = sorted(os.path.relpath(os.path.join(d, n), tmp) for d, _, ns in os.walk(tmp) for n in ns)
        for folder in ("ctx", "framed", "wild", "dmg", "bad", "sel", "qonly"):
            read(os.path.join(tmp, folder))
        after = sorted(os.path.relpath(os.path.join(d, n), tmp) for d, _, ns in os.walk(tmp) for n in ns)
        case("25 nothing was written into any fixture tree", before == after,
             "added {}".format(sorted(set(after) - set(before))))
        case("26 the whole report is JSON-serialisable", isinstance(json.dumps(out), str))

        # 11. Every contract file names its writer, every template is found.
        case("27 every contract file has a writer and a template",
             all(e["written_by"] for e in out["files"].values())
             and all(e["template"] != "not found" for e in out["files"].values()),
             str({k: (e["written_by"], e["template"]) for k, e in out["files"].items()
                  if not e["written_by"] or e["template"] == "not found"}))

    print("{} cases, {} failed".format(total[0], len(failures)))
    return 1 if failures else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) > 1:
        print("usage: state.py [<research-dir>]   |   state.py --selftest", file=sys.stderr)
        return 2
    root = argv[0] if argv else os.path.join(os.getcwd(), "research")
    print(json.dumps(read(root), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
