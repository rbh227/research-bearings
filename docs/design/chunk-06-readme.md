# Chunk 6: the README

2026-09-16. The README is rewritten for a new person with five minutes, and
four diagrams are drawn for the four things prose explains badly.

## 1. Decision record

- **Order.** What it is in three sentences, install, the loop with its three
  gates, the eight commands, every skill and agent in one line marked built or
  planned, the four rules, sources and keys, evals, layout. A reader who stops
  after any section has something whole.
- **Built or planned, on every line.** The old README described three skills
  and pointed at a plan. This one lists all twenty-nine skill rows and
  twenty-three agents so the shape of the whole is visible, and marks the
  five skills and four agents that exist. Planned rows are one clause each.
- **Diagrams as SVG, drawn with the diagram-design skill.** GitHub renders
  an SVG referenced from markdown; it does not render an HTML page. So each
  diagram is authored as the skill's HTML deliverable in `docs/diagrams/` and
  the SVG is extracted from it by the skill's own export procedure, with the
  font import injected. Default skin, minimal variant, no dot pattern, no
  accent colour except the guard's boundary treatment: the user asked for no
  decoration, and the skill's first-run style gate was answered with the
  default rather than a brand pull.
- **Four diagrams, four types.** The loop is the skill's Loop type, six
  stations on one circle with dashed write-backs into one hub, `research/`;
  the three gates are tagged, not coloured, because the type allows one focal
  station and there are three gates. The fan-out, the read trio and the tool
  split are Architecture type, orthogonal connectors, nine nodes or fewer,
  legend as a bottom strip.
- **Nothing in the README that the repo contradicts.** Every command named
  exists or is marked planned; every path in the layout block exists; the
  install lines are the ones that worked.

## 2. What ships

| Piece | Change |
|---|---|
| `README.md` | rewritten |
| `docs/diagrams/loop.{html,svg}` | the loop with its three human gates |
| `docs/diagrams/gathering-fan-out.{html,svg}` | question → seven searchers → script → indexes → merger → matrix |
| `docs/diagrams/read-trio.{html,svg}` | predictor sees the abstract only, reader the full text, scorer both |
| `docs/diagrams/tool-split.{html,svg}` | research agents read the world and cannot run code; experiment agents run code and cannot read the world |

Nothing deleted. The old README's "The idea" section, the shape-of-a-problem
argument, is now one clause in the `/scout` line and the analogs file itself.

## 3. Done-check

- Every `/research-bearings:<name>` the README marks built has a
  `skills/<name>/SKILL.md`; every agent marked built has `agents/<name>.md`.
- Every path in the layout block exists.
- The four SVGs parse as XML and reference the fonts the HTML does.
- Static checks green.

## Addendum, 2026-09-18

The README was restructured after chunk 10 shipped 1.0.0: a wordmark banner
(`docs/diagrams/banner.svg`) and a monospace pipeline block at the top, then
commands, quick start, the 27 skills in tables by stage, the 23 agents in one
table, how it works, sources, checks, and the project structure. The three
remaining diagrams were redrawn simpler — five nodes, four nodes, three nodes,
no tags and no legend strips — in the same palette. The loop diagram was
retired; the pipeline block at the top of the README carries the six stations
and the three gates.
