#!/usr/bin/env python3
"""Do the facts the eval graders quote still hold for the fixture they name?

Every `llm` grader for a router, composite or loop case carries numbers read
from `python3 scripts/state.py <assembled folder>` on the day it was written:
which move is stale and by how many files, what is skipped, what is
recommended first. The harness cannot run the state script inside a grader, so
those numbers would drift silently the day the dependency table or a fixture
changes. This check is the mechanical half of that promise: it assembles every
shape the cases use, reads it with the state script, and asserts the facts the
graders state.

Add an assertion here whenever a grader quotes a fact. A failure means a grader
is now lying about its fixture — fix the grader or the table, never this file
alone.

Run: python3 evals/fixtures/check_cases.py            (exit 1 on any failure)
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import state  # noqa: E402


def status(out, command):
    return next(m["status"] for m in out["moves"] if m["command"] == command)


def missing(out, command):
    return next(m.get("missing", []) for m in out["moves"] if m["command"] == command)


def on_demand_met(out, command):
    return next(m["precondition_met"] for m in out["on_demand"] if m["command"] == command)


# shape -> [(case that quotes it, sentence the grader states, predicate)]
FACTS = {
    "empty": [
        ("router-empty-names-start", "recommended is exactly setup", lambda o: o["recommended"] == ["setup"] and o["empty"]),
    ],
    "question-only": [
        ("router-framed-names-surveys", "stage reached is questions", lambda o: o["stage_reached"] == "questions"),
        ("router-framed-names-surveys", "setup is skipped and a repair", lambda o: status(o, "setup") == "skipped"
         and any(r["file"] == "CONTEXT.md" and r["kind"] == "missing upstream" for r in o["repairs"])),
        ("router-framed-names-surveys", "frame is done", lambda o: status(o, "frame") == "done"),
        ("router-framed-names-surveys", "recommended begins with surveys", lambda o: o["recommended"][:1] == ["surveys"]),
        ("surveys-shows-one-review-query", "QUESTION.md present, surveys absent", lambda o: o["files"]["QUESTION.md"]["state"] == "present"
         and o["files"]["landscape/surveys.md"]["state"] == "absent"),
    ],
    "wildfire-surveyed": [
        ("orient-asks-about-existing-surveys", "surveys is done, landscape is ready", lambda o: status(o, "surveys") == "done" and status(o, "landscape") == "ready"),
        ("orient-asks-about-existing-surveys", "nothing upstream is newer than surveys.md", lambda o: o["staleness"]["landscape/surveys.md"]["upstream_newer"] == 0),
        ("landscape-shows-seven-queries-and-waits", "QUESTION.md and surveys.md present", lambda o: o["files"]["QUESTION.md"]["state"] == "present"
         and o["files"]["landscape/surveys.md"]["state"] == "present"),
    ],
    "wildfire": [
        ("router-wildfire-offers-scout-or-read", "stage reached is gathering", lambda o: o["stage_reached"] == "gathering"),
        ("router-wildfire-offers-scout-or-read", "scout is the only non-done move at that stage, ready",
         lambda o: [m["command"] for m in o["moves"] if m["stage"] == "gathering" and m["status"] != "done"] == ["scout"]
         and status(o, "scout") == "ready"),
        ("router-wildfire-offers-scout-or-read", "read is the first ready move of the next stage",
         lambda o: [m["command"] for m in o["moves"] if m["stage"] == "processing" and m["status"] == "ready"][0] == "read"),
        ("router-wildfire-offers-scout-or-read", "one repair: CONTEXT.md missing upstream",
         lambda o: [(r["file"], r["kind"]) for r in o["repairs"]] == [("CONTEXT.md", "missing upstream")]),
        ("router-goal-precondition-first", "rank blocked on premortems/", lambda o: status(o, "rank") == "blocked" and any("premortems/" in m for m in missing(o, "rank"))),
        ("router-goal-precondition-first", "premortem blocked on ideas/", lambda o: status(o, "premortem") == "blocked" and any("ideas/" in m for m in missing(o, "premortem"))),
        ("router-goal-precondition-first", "ideas is ready", lambda o: status(o, "ideas") == "ready"),
        ("read-proposes-five-and-waits", "matrix present, no cards", lambda o: o["files"]["landscape/matrix.md"]["state"] == "present" and o["counts"]["cards"] == 0),
        ("ideas-reports-missing-seed-kinds", "no BITS.md, no analogs, no IDEAS.md, matrix present",
         lambda o: o["files"]["BITS.md"]["state"] == "absent" and o["counts"]["analog_pages"] == 0
         and o["files"]["IDEAS.md"]["state"] == "absent" and o["files"]["landscape/matrix.md"]["state"] == "present"),
        ("scout-fingerprint-has-no-home-nouns", "scout is ready", lambda o: status(o, "scout") == "ready"),
        ("brainstorm-asks-problems-before-feasibility", "brainstorm is ready", lambda o: status(o, "brainstorm") == "ready"),
    ],
    "damage": [
        ("router-damage-offers-fork", "stage reached is processing", lambda o: o["stage_reached"] == "processing"),
        ("router-damage-offers-fork", "bits is stale with two newer by date and none not named",
         lambda o: status(o, "bits") == "stale" and o["staleness"]["BITS.md"]["upstream_newer"] == 2 and o["staleness"]["BITS.md"]["not_named"] == []),
        ("router-damage-offers-fork", "read repeats; brainstorm and ideas are ready",
         lambda o: status(o, "read") == "repeat" and status(o, "brainstorm") == "ready" and status(o, "ideas") == "ready"),
        ("router-damage-offers-fork", "datasets and groups are on-demand and not recommended",
         lambda o: {"datasets", "groups"} <= {m["command"] for m in o["on_demand"]} and not ({"datasets", "groups"} & set(o["recommended"]))),
        ("router-damage-offers-fork", "the rule yields bits, read, brainstorm",
         lambda o: ([m["command"] for m in o["moves"] if m["stage"] == "processing" and m["status"] == "stale"]
                    + [m["command"] for m in o["moves"] if m["stage"] == "processing" and m["status"] in ("ready", "repeat")])[:3] == ["bits", "read", "brainstorm"]),
        ("router-damage-offers-fork", "one repair: CONTEXT.md missing upstream",
         lambda o: [(r["file"], r["kind"]) for r in o["repairs"]] == [("CONTEXT.md", "missing upstream")]),
        ("think-asks-about-stale-bits", "BITS.md dated 11:30, newest upstream 11:45, the two newer cards named",
         lambda o: o["files"]["BITS.md"]["date"] == "2026-09-16T11:30:00"
         and o["staleness"]["BITS.md"]["newest_upstream"] == "2026-09-16T11:45:00"
         and o["staleness"]["BITS.md"]["newer_files"] == ["papers/gupta-2020-rescuenet.md", "papers/shen-2021-bdanet.md"]),
        ("read-drops-carded-papers", "three cards, the three named",
         lambda o: o["files"]["papers/"]["pages"] == ["gupta-2019-xbd", "gupta-2020-rescuenet", "shen-2021-bdanet"]),
        ("rank-requires-idea-pages", "no idea pages", lambda o: o["counts"]["idea_pages"] == 0),
        ("ideas-refuses-to-promote-without-the-index", "BITS.md present, three cards", lambda o: o["files"]["BITS.md"]["state"] == "present" and o["counts"]["cards"] == 3),
    ],
    "selection": [
        ("rank-shows-bound-and-sets-aside", "six ideas, six pre-mortems, none pending",
         lambda o: o["counts"]["idea_pages"] == 6 and o["counts"]["premortems"] == 6 and o["pending"]["premortem"] == []),
        ("rank-shows-bound-and-sets-aside", "rank is ready", lambda o: status(o, "rank") == "ready"),
    ],
}


def main():
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        for shape, facts in FACTS.items():
            target = os.path.join(tmp, shape, "research")
            subprocess.run([os.path.join(HERE, "assemble.sh"), shape, target], check=True, capture_output=True)
            out = state.read(target)
            for case, sentence, ok in facts:
                try:
                    good = bool(ok(out))
                except Exception as exc:  # a fact that cannot even be evaluated is a failure
                    good = False
                    sentence += " — raised {}".format(exc)
                print("{} {:<44} {}".format("ok  " if good else "FAIL", case, sentence))
                failures += 0 if good else 1
    total = sum(len(v) for v in FACTS.values())
    print("{} facts over {} shapes, {} failed".format(total, len(FACTS), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
