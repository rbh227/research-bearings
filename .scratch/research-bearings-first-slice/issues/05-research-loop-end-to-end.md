# The research loop end to end

Type: grilling
Status: resolved
Blocked by: 

## Question

Reading from `academic.md`, what stages does the research loop have, what does each stage produce, and where does a human decide rather than an agent? The build plan's six milestones are one candidate answer, to be challenged, not assumed.

## Answer

Outline: `docs/design/skills-and-agents.md`.

Six stages plus presentation and a cross-cutting honesty layer: question, landscape, presentation, reading, ideation, selection, experiment. 27 typed skills, 5 composites, 28 agents, 4 scripts.

Three human gates: the question, which ideas survive, whether to spend compute.

**Two tests for whether a row earns its place**, not one: it implements an entry in `academic.md`, *or* it serves one of the four goals (parallel gathering, simple presentation, planning directions, simple to use). The sheet is silent on usability, so a goal-backed row is fully justified. Under both tests only `/watch` and `/handoff` defer.

Changes from the first draft: presentation split into three explicit modes (`/brief` prose, `/render` interactive, `/figure` diagram) sharing `brief-writer`; `/verify` moved to cross-cutting since references appear in landscape sections and idea pages too; the composite `/map` renamed `/orient` (collides with the wayfinder, and `/survey` collides with `/surveys`).

Four gaps closed: `IDEAS.md` as the running idea log appended by three skills; `/ideas` reads the merger's contradiction list as a seed source; typicality stays an uncomputed note; `reader` gains one line comparing its card against others in the same matrix cell.
