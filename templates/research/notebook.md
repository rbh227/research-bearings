# Notebook

<!-- One notebook, at research/NOTEBOOK.md. Two headings, fixed. Written by
     /research-bearings:log and by nothing else.

     ONE file, not one per experiment. Post-hoc selection is impossible only if
     every attempt lands in the same place before its result is known. A
     notebook per experiment would let an attempt that embarrassed somebody
     quietly not exist, and the whole point of this file is that it cannot. -->

## The rule

<!-- Copied into every notebook so that anyone opening the file knows what it
     promises. Do not edit this section after /log writes it:

     This file is append-only. Lines are added; no line is ever changed or
     removed, including by the person who wrote it. An attempt that failed, was
     misconfigured, or was embarrassing stays exactly where it landed.

     Every attempt is opened BEFORE its result is known, with the date, the
     experiment page, the config hash and the seeds. Results are attached
     afterwards as a new block under the entry they belong to. The opening
     block is never rewritten to match what came back.

     An entry with no experiment page is a run with no pre-registration. It is
     recorded, not refused — that is a finding about the work, and hiding it
     would be the one thing this file exists to prevent. -->

## Entries

<!-- Oldest first, appended. Each attempt opens one `###` block before the run:

     ### 2026-09-20 14:02 · <slug> · cond 7c3e0a9d1b52
     - Experiment: research/experiments/<slug>.md
     - Opened: before the run
     - Config: runs/exp-14/config.json · sha256 4a91c2e0f31b…
     - Condition: 7c3e0a9d1b52… (the config with its seed keys removed)
     - Seeds: 17, 18, 19, 20, 21
     - Intent: <one line — what this attempt is testing, in the researcher's words>

     Two hashes, from ingest_runs.py and never retyped. The CONDITION hash is
     how a later ingest finds this entry again: a five-seed attempt is five
     config files with five config hashes and one condition hash, so the block
     title carries the condition hash's first twelve characters. The config
     hash is the provenance of the one config this entry was opened from.

     Seeds are the ones planned. If they are not known yet, `Seeds: not yet
     fixed` — never a guess, and never copied from the variance plan as though
     it were a fact about this run.

     When the run finishes, /log appends a SECOND block under the same entry
     and touches nothing above it:

     #### Ingested 2026-09-22 09:14
     - Run directory: runs/exp-14/
     - Seeds found: 5 (17, 18, 19, 20, 21)
     - Metrics: damage F1 final 0.612, min 0.588, max 0.615 over 5 runs
     - Exit code: 0 · runs/exp-14/train.log
     - Could not parse: runs/exp-14/notes.yaml — no `key: value` lines found
     - Refused: <the variance checker's refusals, or `none`>

     A refusal is written HERE, in the entry, not omitted from a table
     somewhere else. Henderson's rule works only if the refusal is visible:
     a single-seed number that quietly never appears looks identical to a
     number nobody produced.

     An ingest that finds no opening entry appends a whole entry marked:

     ### 2026-09-22 09:14 · <run-dir> · cond 8b02f11c9a44
     - Experiment: NONE — this run was not logged before its result was known
     - Opened: after the fact, by ingest

     That entry is a finding and it stays. -->
