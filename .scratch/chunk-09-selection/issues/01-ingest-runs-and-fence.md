# 01: `ingest_runs.py` and the widened Bash fence

Type: task
Status: done
Blocked by: —

## What to build

The one script an agent in this chunk may run, and the fence change that lets it
live where it belongs.

**`scripts/ingest_runs.py`** — standard library only, JSON on stdout, in the
shape of the retrieval scripts: a module docstring saying what each reported
field is for, a `main()` over one directory path, and `--selftest`.

Walks a directory for run-shaped subdirectories. A subdirectory is run-shaped if
it holds a config (`.json`, `.yaml`, `.yml`, `.toml`, `.ini`), a metrics file
(`.json`, `.jsonl`, `.csv`), or a log. Per run it reports: the path, the config
file and a hash of its bytes, any seed found in the config, the metric keys with
their final and best values, the mtime range, and an exit code if a log carries
one.

**States, not errors.** A file it cannot parse is reported per file with the
reason and the walk continues. A run with no seed reports `seed_state: "not found"` —
never a guess, never an inference. A directory that is not run-shaped is
reported as such rather than skipped silently.

**It never writes to the run directory**, and it never follows symlinks out of
the tree it was given.

**The fence.** `hooks/guard.py` `SCRIPT_ROOT` widens from
`("scripts", "retrieval")` to `("scripts",)`, so this script lives in
`scripts/` rather than being smuggled into the retrieval directory. The deny
message is reworded to "this plugin's own scripts". Nothing else about the fence
moves: no shell syntax, no chaining, no other binary, nothing outside the plugin.

## Acceptance

- [x] `python3 scripts/ingest_runs.py --selftest` is green, against fixture run directories built in a temp dir: a run with JSON config and CSV metrics; one with JSONL metrics; one with no seed; one with an unparseable config; one directory that is not a run at all.
- [x] The selftest asserts the JSON shape and the state names, never internals.
- [x] A run with no seed reports `seed_state: "not found"`; an unparseable file names the file and the reason.
- [x] The script makes no writes anywhere under the directory it is given.
- [x] `python3 hooks/guard.py --selftest` is green with the widened root, and gains cases: `ingest_runs.py` allowed; `python train.py` denied; `python3 <plugin>/scripts/ingest_runs.py x && rm -rf y` denied; a script outside the plugin denied.
- [x] Every retrieval script that was reachable before is still reachable.

## Resolution

2026-09-18. `scripts/ingest_runs.py`, 17 selftest cases green; `hooks/guard.py`
widened, 79 cases green.

**There is no `best` field, and that is deliberate.** The spec asked for "the
metric keys and their final and best values". Best needs a direction — up for
accuracy, down for loss — and the script has no way to know which. A field named
`best` that silently meant `max` would put a loss's worst value in a results
table, which is precisely the kind of number this chunk exists to catch. Each
metric carries `final`, `min`, `max` and `count`, and the caller picks the end
it wanted. Case 4 asserts `best` is absent.

**A `.json` is classified by name, never by content.** It can be a config or a
metrics file, so the stem decides: `config`/`hparams`/`args` and friends are a
config, `metrics`/`results`/`history` and friends are metrics, and anything else
is reported under `unclassified` with the reason. A directory holding only an
unclassified `.json` is not run-shaped. Case 12.

**YAML and INI are flattened, and say so.** There is no YAML parser in the
standard library and this script has no dependencies, so every `key: value` line
is read and nesting is discarded; `config_parse` reports `flattened` rather than
`parsed`, and a key appearing twice with two values lands in `ambiguous_keys`
instead of one value winning quietly. This is what finds a seed nested under
`trainer:` — case 7. JSON and TOML are parsed properly.

**A run's subdirectories are not descended into.** `checkpoints/` and `wandb/`
belong to the run above them, not beside it, so the walk stops at the first
run-shaped directory on each path. Depth is capped at 6 and runs at 200, with
`truncated` reported when the cap is hit.

**The read-only claim is asserted, not stated.** Case 14 snapshots the fixture
tree before and after the walk and compares. Symlinked directories and files are
skipped so the walk cannot leave the tree it was given.

**The fence's guarantees are unchanged by the widening.** `SCRIPT_ROOT` went
from `("scripts", "retrieval")` to `("scripts",)`; the six new cases prove the
ingester is allowed, the retrieval scripts still are, `python train.py` is not,
a chained `&& rm -rf` is not, a script outside the plugin is not, and a sibling
directory whose name merely starts with `scripts` is not.

**Adversarial review, 2026-09-18.** Two findings against this ticket, both
reproduced and fixed. A `README.txt` beside the runs made the parent the run and
hid its children — `.txt` is now a log only by name, every directory is
descended into, and skipped artifact subtrees are reported under `excluded`. And
the raw config hash could not group runs that differ only in seed, so the
ingester now reports `condition_hash` (the canonical config with seed keys
removed) beside it. 27 cases.
