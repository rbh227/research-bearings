# The first slice

Type: grilling
Status: resolved
Blocked by: 05

## Question

Which skills and agents ship in the first buildable slice of research-bearings, and what does that slice deliberately leave out? Each chosen skill gets one job and one output file.

## Resolution

Chunk 1 is the plugin skeleton plus the question stage: `/setup` (writes `research/CONTEXT.md`) and `/frame` (writes `research/QUESTION.md` and `research/framing-log.md`), with one agent, `question-critic`. Chosen over a paper-scout-first slice and over the whole landscape chain because it is the only chunk with no dependency on the pending Semantic Scholar key, and because it proves the install-and-run machinery before any retrieval exists.

Left out deliberately: all retrieval, the landscape chain, every schema without a consumer, the shared anti-rationalization file (rejected outright), and any cross-model review stage (the user runs `/codex-review` by hand).

`/frame` is a diverge-converge loop, not an interrogation: it generates candidate framings (Polya transformations, Hamming's bank), kills them on Booth's ladder and the recursive so-what, and repeats. Divergence is labelled uninformed; the stage is re-entrant after `/surveys`.

Spec: `docs/design/chunk-01-question-stage.md`.
