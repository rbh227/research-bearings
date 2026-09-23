#!/usr/bin/env python3
"""Structural check: every heading in a template is named by the skill that
writes it, and every heading a skill claims to write exists in the template.

Templates are the single source of truth for the plugin's file interfaces. If
these drift, a downstream skill reads a heading that is never written.

Run: python3 scripts/check_headings.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# template -> the files that must name every one of its headings
CONTRACTS = {
    "templates/research/CONTEXT.md": ["skills/setup/SKILL.md"],
    "templates/research/CONNECTIONS.md": ["skills/setup/SKILL.md"],
    "templates/research/QUESTION.md": ["skills/frame/SKILL.md"],
    "templates/research/framing-log.md": ["skills/frame/SKILL.md"],
    "templates/research/analogs.md": ["skills/scout/SKILL.md"],
    "templates/research/section.md": ["agents/searcher.md"],
    "templates/research/matrix.md": ["agents/merger.md", "skills/landscape/SKILL.md"],
    "templates/research/timeslice.md": ["agents/merger.md", "skills/landscape/SKILL.md"],
    "templates/research/surveys.md": ["agents/survey-differ.md", "skills/surveys/SKILL.md"],
    "templates/research/card.md": ["agents/scorer.md", "skills/read/SKILL.md"],
    "templates/research/prediction.md": ["agents/predictor.md"],
    "templates/research/reading.md": ["agents/reader.md"],
    "templates/research/reviews.md": ["agents/openreview-reader.md", "skills/reviews/SKILL.md"],
    "templates/research/datasets.md": ["agents/dataset-scout.md", "skills/datasets/SKILL.md"],
    "templates/research/groups.md": ["agents/author-tracker.md", "skills/groups/SKILL.md"],
    "templates/research/bits.md": ["skills/bits/SKILL.md"],
    "templates/research/critique.md": ["agents/critic.md", "skills/critique/SKILL.md"],
    "templates/research/ideas-log.md": ["skills/brainstorm/SKILL.md", "skills/ideas/SKILL.md"],
    "templates/research/idea.md": ["skills/ideas/SKILL.md"],
    "templates/research/persona.md": ["agents/persona-ideator.md"],
    "templates/research/diversity.md": ["agents/diversity-planner.md"],
    "templates/research/premortem.md": ["agents/premortem-agent.md"],
    "templates/research/ranking.md": ["skills/rank/SKILL.md"],
    "templates/research/heilmeier.md": ["skills/spec/SKILL.md"],
    "templates/research/baseline.md": ["agents/baseline-reproducer.md", "skills/baseline/SKILL.md"],
    "templates/research/experiment.md": ["agents/experiment-designer.md", "skills/design/SKILL.md"],
    "templates/research/notebook.md": ["skills/log/SKILL.md"],
    "templates/research/result.md": ["agents/results-tabulator.md", "skills/result/SKILL.md"],
}

# agent -> the output headings its contract must define
AGENT_OUTPUTS = {
    "agents/question-critic.md": ["Findings", "Concessions", "Could not determine"],
    "agents/critic.md": ["Findings", "Concessions", "Could not determine"],
    # tournament-judge writes a comparison file rather than a template's page:
    # one pairing, four headings, and no template of its own because the file
    # is read by /rank and by nobody else.
    "agents/tournament-judge.md": ["Winner", "What decided it", "Scores",
                                   "What would flip it"],
}


def norm(text):
    """Collapse whitespace so a heading name that line-wraps still matches."""
    return re.sub(r"\s+", " ", text)


def headings(path):
    return [
        line.strip()[3:].strip()
        for line in (ROOT / path).read_text().splitlines()
        if line.startswith("## ")
    ]


def main():
    failures = []

    for template, consumers in CONTRACTS.items():
        names = headings(template)
        # A registered consumer that does not exist is a failure with a name,
        # not a traceback: it happens whenever a template lands a ticket ahead
        # of the skill that writes it.
        absent = [c for c in consumers if not (ROOT / c).exists()]
        if absent:
            failures.append(
                "{}: registered consumer {} does not exist".format(template, ", ".join(absent))
            )
            print("  {:2d} headings  {} -> {} (MISSING)".format(len(names), template, ", ".join(absent)))
            continue
        blob = norm(" ".join((ROOT / c).read_text() for c in consumers))
        missing = [n for n in names if norm(n) not in blob]
        for n in missing:
            failures.append(
                "{}: heading '{}' is in the template but named nowhere in {}".format(
                    template, n, ", ".join(consumers)
                )
            )
        print("  {:2d} headings  {} -> {}".format(len(names), template, ", ".join(consumers)))

    for agent, outputs in AGENT_OUTPUTS.items():
        blob = norm((ROOT / agent).read_text())
        for o in outputs:
            if norm("## " + o) not in blob:
                failures.append("{}: output heading '{}' is not defined".format(agent, o))
        print("  {:2d} outputs   {}".format(len(outputs), agent))

    print()
    if failures:
        for f in failures:
            print("FAIL  " + f)
        return 1
    print("heading parity: all templates and contracts agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
