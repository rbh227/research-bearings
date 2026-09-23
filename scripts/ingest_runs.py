#!/usr/bin/env python3
"""Read a directory of experiment runs and report what is in it, as JSON.

This is the one command an agent in this plugin may run against the user's own
files, and the only thing it does is look. It never writes anywhere under the
directory it is given, never follows a symlink out of that tree, and never runs
anything the user wrote. `/log` calls it to attach a result to a notebook entry;
`results-tabulator` calls it to build a table from run directories rather than
from a model's memory; `failure-mode-auditor` calls it to answer M1-M7 against
files instead of prose.

**It works on run directories nobody formatted for it.** There is no layout to
adopt. A subdirectory is run-shaped if it holds a config, a metrics file, or a
log, and the classification is by filename because a `.json` can be either.

**How a file is classified, by name.** `.yaml`, `.yml`, `.toml`, `.ini` and
`.cfg` are configs. `.jsonl`, `.csv` and `.tsv` are metrics. `.log`, `.out`,
`.err` and `.txt` are logs, as are extensionless `stdout`, `stderr`, `log` and
`output`. A `.json` is the ambiguous case: its stem decides — `config`, `cfg`,
`params`, `hparams`, `args`, `settings`, `options`, `flags` and the like make it
a config; `metrics`, `results`, `scores`, `history`, `scalars`, `eval` and
`summary` make it metrics; anything else (`best_model.json`, `log.json`) is
reported under `unclassified` and not read.

**States, not errors.** Every file it cannot read is reported with the reason
and the walk continues. A directory that is not run-shaped is reported as such
rather than skipped silently, because "I found nothing here" and "I did not
look here" are different findings. The only non-zero exit is a root that does
not exist.

**Nothing is inferred.** A run with no seed reports `"seeds": []` and
`"seed_state": "not found"` — never a guess, and never a default of 0. A metric
key carries `final`, `min`, `max` and `count` and **no "best"**: best depends on
whether the metric goes up or down, this script cannot know which, and a field
named `best` that silently means `max` would put a loss's worst value in a
results table. The caller picks the direction; the script reports the numbers.

Two parsers are shallower than the format and say so in `config_parse`:

  yaml   there is no YAML parser in the standard library, so every `key: value`
         line is read and nesting is discarded (`"flattened"`). A key that
         appears twice with different values lands in `ambiguous_keys` rather
         than one value winning quietly.
  ini    configparser's sections are flattened to `section.key`, same reason.

JSON and TOML are parsed properly (`"parsed"`).

Output is one JSON object on stdout:

  root           the directory that was walked, resolved
  runs[]         path, config file and hash, condition hash, seeds, metrics,
                 mtime range, exit code, per-file unparsed reasons, and how
                 many runs sit beneath it
  not_runs[]     directories that held none of the three, with what was seen
  excluded[]     subtrees the walk did not look at, each with the reason:
                 an artifact directory, the depth limit, or the run cap
  truncated      true if the run cap was hit, with the cap

Two hashes per run, and they answer different questions. `config_hash` is the
sha256 of the config file's bytes: provenance, and how a notebook entry is
found again. `condition_hash` is the sha256 of the canonical parsed config
with every seed key removed: two runs that differ only in seed share one, and
that is the key on which runs may be grouped and averaged. The raw hash alone
cannot say which runs are one condition, because the seed is in the bytes.

Run: python3 scripts/ingest_runs.py <directory>
     python3 scripts/ingest_runs.py --selftest
"""

import csv
import hashlib
import io
import json
import os
import re
import sys
from datetime import datetime, timezone

# How a file gets classified. A `.json` is a config or a metrics file depending
# on its name, and one that matches neither is reported under `unclassified`
# rather than guessed at.
CONFIG_STEMS = ("config", "cfg", "params", "hparams", "hyperparams", "args",
                "settings", "options", "opts", "flags", "run_config", "train_config")
METRIC_STEMS = ("metric", "metrics", "result", "results", "score", "scores",
                "history", "scalars", "eval", "evaluation", "summary")
CONFIG_EXT = (".json", ".yaml", ".yml", ".toml", ".ini", ".cfg")
METRIC_EXT = (".json", ".jsonl", ".csv", ".tsv")
LOG_EXT = (".log", ".out", ".err")
# A .txt is a log only when its name says so. `README.txt`, `notes.txt` and
# `requirements.txt` are not logs, and a first version that treated every .txt
# as one made `runs/` itself run-shaped and hid every run beneath it (review,
# 2026-09-18).
TXT_LOG_STEMS = ("log", "logs", "stdout", "stderr", "output", "train", "console", "nohup")
# Subtrees that belong to the run above them and are never runs themselves.
# They are skipped AND REPORTED, so a reader can see what the walk did not look at.
ARTIFACT_DIRS = ("checkpoints", "checkpoint", "ckpt", "ckpts", "weights", "models",
                 "wandb", "tensorboard", "tb", "tb_logs", "lightning_logs", "mlruns",
                 "__pycache__", ".git", ".hydra", "cache", ".cache", "tmp", "samples",
                 "predictions", "outputs_images", "figures", "media")

# Keys that carry a seed. Checked at every depth of a parsed config.
SEED_KEYS = ("seed", "seeds", "random_seed", "rng_seed", "torch_seed",
             "numpy_seed", "np_seed", "data_seed", "manual_seed", "global_seed")

# An exit code, in the spellings a training script, a scheduler and subprocess
# use. Every pattern names the word "exit" or "returncode": a first version
# also matched bare `return`, and "query returned 5 results" came back as exit
# code 5 (review, 2026-09-18). A false exit code is a false file fact, and M1
# is answered from this field.
EXIT_PATTERNS = (
    re.compile(r"\bexit(?:ed)?\s+(?:with\s+)?(?:code|status)[:=\s]+(-?\d+)", re.I),
    re.compile(r"\bexit[_ ]?(?:code|status)[:=\s]+(-?\d+)", re.I),
    re.compile(r"\breturn[_ ]?code[:=\s]+(-?\d+)", re.I),
    re.compile(r"\bProcess finished with exit code\s+(-?\d+)", re.I),
)

MAX_PARSE_BYTES = 5 * 1024 * 1024   # a file larger than this is reported, not read
MAX_RUNS = 200                       # a cap, reported when it is hit
MAX_DEPTH = 6                        # how far below the root to look
LOG_TAIL_BYTES = 64 * 1024           # an exit code is at the end of a log


# --------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------


def classify(name):
    """Return 'config', 'metrics', 'log', 'unclassified' or None for one filename.

    None means the extension is not one this script reads at all — a
    checkpoint, an image, a .py. `unclassified` is the narrower finding: the
    extension could be either a config or a metrics file and the name says
    neither, so it is reported and not read.
    """
    stem, ext = os.path.splitext(name)
    ext = ext.lower()
    stem_l = stem.lower()

    def matches(stems):
        return any(s == stem_l or s in re.split(r"[^a-z0-9]+", stem_l) for s in stems)

    is_config_name = matches(CONFIG_STEMS)
    is_metric_name = matches(METRIC_STEMS)

    if ext in (".yaml", ".yml", ".toml", ".ini", ".cfg"):
        return "config"
    if ext in (".jsonl", ".csv", ".tsv"):
        return "metrics"
    if ext == ".json":
        if is_config_name:
            return "config"
        if is_metric_name:
            return "metrics"
        return "unclassified"
    if ext in LOG_EXT:
        return "log"
    if ext == ".txt":
        return "log" if matches(TXT_LOG_STEMS) else None
    if ext == "" and stem_l in ("stdout", "stderr", "log", "output"):
        return "log"
    return None


# --------------------------------------------------------------------------
# config parsing
# --------------------------------------------------------------------------


def _scalar(token):
    """Parse one YAML/INI scalar. Returns the string unchanged if it is one."""
    t = token.strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'":
        return t[1:-1]
    low = t.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "none", "~", ""):
        return None
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        pass
    return t


def flatten_yaml(text):
    """Read every `key: value` line, discard nesting, report duplicate keys.

    There is no YAML parser in the standard library and this script has no
    dependencies. Flattening finds the thing that is actually wanted — a seed,
    a learning rate, a model name — at whatever depth it sits, and says in
    `config_parse` that it is not a real parse. A key that appears twice with
    two different values is ambiguous after flattening, so it is named rather
    than resolved.
    """
    out, ambiguous = {}, []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip() or line.lstrip().startswith("-"):
            continue
        m = re.match(r"^\s*([A-Za-z_][\w.\-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest == "":          # a nested block opens here; the key itself holds nothing
            continue
        value = _scalar(rest)
        if key in out and out[key] != value and key not in ambiguous:
            ambiguous.append(key)
        out.setdefault(key, value)
    return out, ambiguous


def flatten_ini(text):
    import configparser
    parser = configparser.ConfigParser()
    parser.read_string(text)
    out = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            out["{}.{}".format(section, key)] = _scalar(value)
            out.setdefault(key, _scalar(value))
    for key, value in parser.defaults().items():
        out.setdefault(key, _scalar(value))
    return out


def parse_config(path):
    """Return (data, parse_state, ambiguous_keys, reason).

    `data` is None when the file could not be read at all, and `reason` says
    why. Every caller reports the reason rather than dropping the file.
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        return None, "unreadable", [], str(exc)
    if size > MAX_PARSE_BYTES:
        return None, "unreadable", [], "larger than {} bytes".format(MAX_PARSE_BYTES)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return None, "unreadable", [], str(exc)

    if ext == ".json":
        try:
            return json.loads(text), "parsed", [], None
        except ValueError as exc:
            return None, "unparsed", [], "not valid JSON: {}".format(exc)
    if ext == ".toml":
        try:
            import tomllib
        except ImportError:
            return None, "unparsed", [], "no tomllib in this Python (needs 3.11+)"
        try:
            return tomllib.loads(text), "parsed", [], None
        except Exception as exc:                      # tomllib raises its own type
            return None, "unparsed", [], "not valid TOML: {}".format(exc)
    if ext in (".ini", ".cfg"):
        try:
            return flatten_ini(text), "flattened", [], None
        except Exception as exc:
            return None, "unparsed", [], "not valid INI: {}".format(exc)
    if ext in (".yaml", ".yml"):
        data, ambiguous = flatten_yaml(text)
        if not data:
            return None, "unparsed", [], "no `key: value` lines found"
        return data, "flattened", ambiguous, None
    return None, "unparsed", [], "unhandled config extension {}".format(ext or "(none)")


def strip_seeds(node):
    """A copy of a parsed config with every seed key removed, at any depth."""
    if isinstance(node, dict):
        return {k: strip_seeds(v) for k, v in node.items()
                if str(k).lower().split(".")[-1] not in SEED_KEYS}
    if isinstance(node, list):
        return [strip_seeds(v) for v in node]
    return node


def condition_hash(data):
    """sha256 of the canonical config with the seed keys removed.

    Two runs that differ only in seed are one condition, and the raw config
    hash cannot say so: the seed is in the bytes, so five seeds are five
    hashes. This is the key `variance-checker` and `results-tabulator` group
    on. The raw hash stays beside it for provenance — it is how a notebook
    entry is found again — and this one says which runs may be averaged.

    Canonical means sorted keys and JSON, so key order in the file does not
    change the answer. A config that would not parse has no condition hash,
    and the report says `null` rather than guessing.
    """
    canonical = json.dumps(strip_seeds(data), sort_keys=True, default=str,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def find_seeds(data):
    """Every seed in a parsed config, with the key path each came from.

    Returns a list of {"key": path, "value": v}. Nothing is inferred: a config
    with no seed key returns an empty list, and the caller reports `not found`.
    """
    found = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                here = "{}.{}".format(path, key) if path else str(key)
                base = str(key).lower().split(".")[-1]
                if base in SEED_KEYS:
                    if isinstance(value, bool):
                        pass                       # `seed: true` is a flag, not a seed
                    elif isinstance(value, int):
                        found.append({"key": here, "value": value})
                    elif isinstance(value, list) and all(
                            isinstance(v, int) and not isinstance(v, bool) for v in value) and value:
                        for v in value:
                            found.append({"key": here, "value": v})
                if isinstance(value, (dict, list)):
                    walk(value, here)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                if isinstance(value, (dict, list)):
                    walk(value, "{}[{}]".format(path, i))

    walk(data, "")
    return found


# --------------------------------------------------------------------------
# metrics parsing
# --------------------------------------------------------------------------


def _numeric(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def summarise(series):
    """final / min / max / count for one metric key.

    No `best`. Best needs a direction — up for accuracy, down for loss — and
    this script has no way to know which, so it reports the numbers and lets
    the caller say which end it wanted.
    """
    return {
        "final": series[-1],
        "min": min(series),
        "max": max(series),
        "count": len(series),
    }


def parse_metrics(path):
    """Return (metrics, non_numeric, reason).

    `metrics` maps key -> {final, min, max, count}. `non_numeric` names the
    columns or keys that were present and held nothing this could read as a
    number, so a missing metric is visibly a type problem and not an absence.
    """
    ext = os.path.splitext(path)[1].lower()
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        return {}, [], str(exc)
    if size > MAX_PARSE_BYTES:
        return {}, [], "larger than {} bytes".format(MAX_PARSE_BYTES)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        return {}, [], str(exc)

    series, non_numeric = {}, []

    def add(key, value):
        number = _numeric(value)
        if number is None:
            if key not in non_numeric:
                non_numeric.append(key)
            return
        series.setdefault(key, []).append(number)

    if ext == ".jsonl":
        bad = 0
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                bad += 1
                continue
            if isinstance(row, dict):
                for key, value in row.items():
                    add(key, value)
        if not series and bad:
            return {}, non_numeric, "{} lines are not valid JSON".format(bad)
        if bad:
            non_numeric.append("{} unparseable lines".format(bad))
    elif ext in (".csv", ".tsv"):
        delimiter = "\t" if ext == ".tsv" else ","
        try:
            rows = list(csv.DictReader(io.StringIO(text), delimiter=delimiter))
        except csv.Error as exc:
            return {}, [], "not valid CSV: {}".format(exc)
        if not rows:
            return {}, [], "no rows"
        for row in rows:
            for key, value in row.items():
                if key is None:
                    continue
                add(key, value)
    elif ext == ".json":
        try:
            data = json.loads(text)
        except ValueError as exc:
            return {}, [], "not valid JSON: {}".format(exc)
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        add(key, item)
                elif isinstance(value, dict):
                    for sub, item in value.items():
                        add("{}.{}".format(key, sub), item)
                else:
                    add(key, value)
        elif isinstance(data, list):
            for row in data:
                if isinstance(row, dict):
                    for key, value in row.items():
                        add(key, value)
        else:
            return {}, [], "top level is neither an object nor an array"
    else:
        return {}, [], "unhandled metrics extension {}".format(ext or "(none)")

    return {k: summarise(v) for k, v in sorted(series.items())}, non_numeric, None


def find_exit_code(path):
    """The exit code a log carries, or None. Reads the tail only."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as fh:
            if size > LOG_TAIL_BYTES:
                fh.seek(size - LOG_TAIL_BYTES)
            tail = fh.read().decode("utf-8", errors="replace")
    except OSError:
        return None
    # The LAST exit line in the log, whichever spelling it uses — not the last
    # match of the first pattern that hits, which would let an early
    # "exit code 0" outrank a later "exited with status 137".
    last = None
    for pattern in EXIT_PATTERNS:
        for m in pattern.finditer(tail):
            if last is None or m.start() > last.start():
                last = m
    if last is None:
        return None
    try:
        return int(last.group(1))
    except ValueError:
        return None


# --------------------------------------------------------------------------
# the walk
# --------------------------------------------------------------------------


def iso(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat(timespec="seconds")


def inspect(directory, root):
    """Everything this script can say about one candidate run directory."""
    rel = os.path.relpath(directory, root)
    report = {
        "path": rel if rel != "." else os.path.basename(root) or root,
        "abs_path": directory,
        "config_file": None,
        "config_hash": None,
        "condition_hash": None,
        "config_parse": None,
        "seeds": [],
        "seed_state": "not found",
        "metrics_file": None,
        "metrics": {},
        "mtime_range": None,
        "exit_code": None,
        "unparsed": [],
        "unclassified": [],
        "non_numeric": [],
    }

    configs, metrics, logs, mtimes = [], [], [], []
    try:
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
    except OSError as exc:
        report["unparsed"].append({"file": rel, "reason": str(exc)})
        return report, False

    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            continue
        kind = classify(entry.name)
        if kind is None:
            continue
        try:
            mtimes.append(entry.stat().st_mtime)
        except OSError:
            pass
        if kind == "config":
            configs.append(entry.path)
        elif kind == "metrics":
            metrics.append(entry.path)
        elif kind == "log":
            logs.append(entry.path)
        else:
            report["unclassified"].append({
                "file": os.path.relpath(entry.path, root),
                "reason": "a .json whose name says neither config nor metrics",
            })

    if not (configs or metrics or logs):
        return report, False

    if configs:
        path = configs[0]
        report["config_file"] = os.path.relpath(path, root)
        try:
            with open(path, "rb") as fh:
                report["config_hash"] = hashlib.sha256(fh.read()).hexdigest()
        except OSError as exc:
            report["unparsed"].append({"file": report["config_file"], "reason": str(exc)})
        data, state, ambiguous, reason = parse_config(path)
        report["config_parse"] = state
        if ambiguous:
            report["ambiguous_keys"] = ambiguous
        if data is None:
            report["unparsed"].append({"file": report["config_file"], "reason": reason})
        else:
            seeds = find_seeds(data)
            report["seeds"] = seeds
            report["seed_state"] = "found" if seeds else "not found"
            report["condition_hash"] = condition_hash(data)
        if len(configs) > 1:
            report["other_configs"] = [os.path.relpath(p, root) for p in configs[1:]]

    if metrics:
        path = metrics[0]
        report["metrics_file"] = os.path.relpath(path, root)
        parsed, non_numeric, reason = parse_metrics(path)
        report["metrics"] = parsed
        report["non_numeric"] = non_numeric
        if reason:
            report["unparsed"].append({"file": report["metrics_file"], "reason": reason})
        if len(metrics) > 1:
            report["other_metrics"] = [os.path.relpath(p, root) for p in metrics[1:]]

    for path in logs:
        code = find_exit_code(path)
        if code is not None:
            report["exit_code"] = code
            report["exit_code_file"] = os.path.relpath(path, root)
            break
    if logs:
        report["log_files"] = [os.path.relpath(p, root) for p in logs]

    if mtimes:
        report["mtime_range"] = [iso(min(mtimes)), iso(max(mtimes))]

    return report, True


def walk(root):
    """Find every run-shaped directory at or below `root`.

    Every directory is descended into, whether or not it is itself a run. The
    first version stopped at the first run-shaped directory on each path, on
    the theory that `checkpoints/` belongs to the run above it — and a
    `README.txt` in `runs/` then made `runs/` the run and hid every experiment
    beneath it, with nothing reported (review, 2026-09-18). So artifact
    subtrees are now named explicitly in ARTIFACT_DIRS, skipped, and REPORTED
    under `excluded`, and everything else is looked at. A run that contains
    runs says so in `contains_runs`, so a collection directory that happens to
    hold a stray config is visible as a collection.
    """
    root = os.path.realpath(root)
    runs, not_runs, excluded = [], [], []
    truncated = False

    stack = [(root, 0)]
    while stack:
        directory, depth = stack.pop(0)
        report, is_run = inspect(directory, root)
        if is_run:
            if len(runs) >= MAX_RUNS:
                truncated = True
                excluded.append({"path": report["path"], "reason": "run cap of {} reached".format(MAX_RUNS)})
                continue
            report["contains_runs"] = 0
            runs.append(report)
        else:
            # A directory that could not be read is not a directory that held
            # nothing. inspect() put the OSError under `unparsed`; say so here,
            # because "found nothing" and "could not look" are different findings.
            if report["unparsed"]:
                reason = "could not read: " + report["unparsed"][0]["reason"]
            else:
                reason = "holds no config, metrics file or log"
            not_runs.append({
                "path": report["path"],
                "reason": reason,
                "unclassified": report["unclassified"],
            })
        try:
            children = sorted(os.scandir(directory), key=lambda e: e.name)
        except OSError:
            continue
        for entry in children:
            if not entry.is_dir() or entry.is_symlink():
                continue
            rel = os.path.relpath(entry.path, root)
            if entry.name.lower() in ARTIFACT_DIRS:
                excluded.append({"path": rel, "reason": "artifact directory, belongs to the run above it"})
                continue
            if depth + 1 > MAX_DEPTH:
                excluded.append({"path": rel, "reason": "deeper than {} levels".format(MAX_DEPTH)})
                continue
            stack.append((entry.path, depth + 1))

    # A run beneath another run: count it on the parent, so a collection
    # directory that holds a stray config is visible as what it is.
    by_path = {r["abs_path"]: r for r in runs}
    for r in runs:
        parent = os.path.dirname(r["abs_path"])
        while parent.startswith(root) and parent != r["abs_path"]:
            if parent in by_path:
                by_path[parent]["contains_runs"] += 1
                break
            if parent == root:
                break
            parent = os.path.dirname(parent)

    return {
        "verb": "ingest",
        "root": root,
        "runs": runs,
        "not_runs": not_runs,
        "excluded": excluded,
        "truncated": truncated,
        "run_cap": MAX_RUNS,
        "counts": {
            "runs": len(runs),
            "not_runs": len(not_runs),
            "excluded": len(excluded),
            "runs_with_no_seed": sum(1 for r in runs if r["seed_state"] == "not found"),
            "runs_with_unparsed_files": sum(1 for r in runs if r["unparsed"]),
            "conditions": len({r["condition_hash"] for r in runs if r["condition_hash"]}),
        },
    }


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------


def selftest():
    """Fixture run directories in a temp dir, then the JSON shape and the state
    names. Never internals: what is asserted is what an agent reads."""
    import tempfile

    failures = []

    def case(name, ok, detail=""):
        print("{} {}".format("ok  " if ok else "FAIL", name) + (" — {}".format(detail) if detail and not ok else ""))
        if not ok:
            failures.append(name)

    with tempfile.TemporaryDirectory() as tmp:
        def write(*parts, body=""):
            path = os.path.join(tmp, *parts)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
            return path

        # 1. JSON config + CSV metrics. The ordinary case.
        write("runs", "a", "config.json",
              body=json.dumps({"seed": 17, "lr": 0.01, "model": {"name": "unet"}}))
        write("runs", "a", "metrics.csv",
              body="step,val_acc,train_loss\n1,0.50,2.0\n2,0.70,1.0\n3,0.65,1.2\n")
        write("runs", "a", "train.log", body="epoch 3 done\nProcess finished with exit code 0\n")

        # 2. JSONL metrics, seed nested in a YAML config.
        write("runs", "b", "config.yaml",
              body="trainer:\n  max_epochs: 10\n  seed: 99\nname: 'run b'\n")
        write("runs", "b", "metrics.jsonl",
              body='{"val_acc": 0.1}\n{"val_acc": 0.4}\nnot json\n{"val_acc": 0.3}\n')

        # 3. No seed anywhere.
        write("runs", "c", "hparams.json", body=json.dumps({"lr": 0.1, "batch": 32}))
        write("runs", "c", "results.json", body=json.dumps({"f1": [0.2, 0.9]}))

        # 4. A config that will not parse.
        write("runs", "d", "config.json", body="{this is not json")
        write("runs", "d", "metrics.csv", body="step,loss\n1,0.5\n")

        # 5. Not a run at all.
        os.makedirs(os.path.join(tmp, "runs", "notes", "deeper"))
        write("runs", "notes", "README.md", body="just notes\n")

        # 6. A .json whose name says neither.
        write("runs", "e", "blob.json", body=json.dumps({"x": 1}))

        before = sorted(os.path.relpath(os.path.join(dirpath, name), tmp)
                        for dirpath, _, names in os.walk(tmp) for name in names)

        out = walk(os.path.join(tmp, "runs"))
        runs = {r["path"]: r for r in out["runs"]}

        case("1  the JSON shape is the documented one",
             set(out) >= {"verb", "root", "runs", "not_runs", "truncated", "counts"}
             and out["verb"] == "ingest", "got keys {}".format(sorted(out)))

        case("2  four run-shaped directories are found, and the non-run is not one",
             sorted(runs) == ["a", "b", "c", "d"], "got {}".format(sorted(runs)))

        a = runs.get("a", {})
        case("3  a JSON config yields its seed and a hash",
             [s["value"] for s in a.get("seeds", [])] == [17]
             and a.get("seed_state") == "found"
             and len(a.get("config_hash") or "") == 64
             and a.get("config_parse") == "parsed",
             "got {}".format({k: a.get(k) for k in ("seeds", "config_hash", "config_parse")}))

        case("4  CSV metrics carry final, min, max and count, and no best",
             a.get("metrics", {}).get("val_acc") == {"final": 0.65, "min": 0.5, "max": 0.7, "count": 3}
             and "best" not in a.get("metrics", {}).get("val_acc", {}),
             "got {}".format(a.get("metrics")))

        case("5  an exit code in a log is read",
             a.get("exit_code") == 0, "got {}".format(a.get("exit_code")))

        case("6  an mtime range is reported as two timestamps",
             isinstance(a.get("mtime_range"), list) and len(a["mtime_range"]) == 2,
             "got {}".format(a.get("mtime_range")))

        b = runs.get("b", {})
        case("7  a nested YAML seed is found, and the parse says it was flattened",
             [s["value"] for s in b.get("seeds", [])] == [99]
             and b.get("config_parse") == "flattened",
             "got {} {}".format(b.get("seeds"), b.get("config_parse")))

        case("8  JSONL metrics parse, and the bad lines are reported not dropped silently",
             b.get("metrics", {}).get("val_acc", {}).get("count") == 3
             and any("unparseable" in str(x) for x in b.get("non_numeric", [])),
             "got {} {}".format(b.get("metrics"), b.get("non_numeric")))

        c = runs.get("c", {})
        case("9  a run with no seed says `not found` and guesses nothing",
             c.get("seeds") == [] and c.get("seed_state") == "not found",
             "got {} {}".format(c.get("seeds"), c.get("seed_state")))

        d = runs.get("d", {})
        case("10 an unparseable config is reported per file with the reason, and the run survives",
             any(u["file"].endswith("config.json") and "JSON" in u["reason"]
                 for u in d.get("unparsed", []))
             and d.get("metrics", {}).get("loss", {}).get("count") == 1,
             "got {}".format(d.get("unparsed")))

        case("11 a directory that is not a run is reported, not skipped",
             any(n["path"].endswith("notes") for n in out["not_runs"]),
             "got {}".format([n["path"] for n in out["not_runs"]]))

        e = [r for r in out["runs"] if r["path"] == "e"]
        case("12 a .json whose name says neither is unclassified, not guessed",
             not e and any(n["path"] == "e" and n["unclassified"] for n in out["not_runs"]),
             "got runs={} not_runs={}".format([r['path'] for r in out['runs']],
                                              [(n['path'], n['unclassified']) for n in out['not_runs']]))

        case("13 the counts agree with the lists",
             out["counts"]["runs"] == len(out["runs"])
             and out["counts"]["runs_with_no_seed"] == 2,
             "got {}".format(out["counts"]))

        after = sorted(os.path.relpath(os.path.join(dirpath, name), tmp)
                       for dirpath, _, names in os.walk(tmp) for name in names)
        case("14 nothing was written into the run tree", before == after,
             "added {}".format(sorted(set(after) - set(before))))

        case("15 the whole report is JSON-serialisable",
             isinstance(json.dumps(out), str))

        # 16. A single run directory passed directly, which is what /log does.
        one = walk(os.path.join(tmp, "runs", "a"))
        case("16 one run directory passed directly is that one run",
             one["counts"]["runs"] == 1 and one["runs"][0]["seed_state"] == "found",
             "got {}".format(one["counts"]))

        # 18. Exit codes: prose is not an exit code, and the last exit line wins.
        write("runs", "f", "config.json", body=json.dumps({"seed": 1}))
        write("runs", "f", "train.log",
              body="query returned 5 results\nexit code 0\nepoch 2\nexited with status 137\n")
        f = {r["path"]: r for r in walk(os.path.join(tmp, "runs"))["runs"]}.get("f", {})
        case("18 `returned 5 results` is not an exit code, and the last exit line wins",
             f.get("exit_code") == 137, "got {}".format(f.get("exit_code")))
        write("runs", "g", "config.json", body=json.dumps({"seed": 1}))
        write("runs", "g", "train.log", body="the model returned 3 boxes\nall done\n")
        g = {r["path"]: r for r in walk(os.path.join(tmp, "runs"))["runs"]}.get("g", {})
        case("18b a log with prose and no exit line reports no exit code",
             g.get("exit_code") is None, "got {}".format(g.get("exit_code")))

        # 19. A directory that cannot be read is reported as unreadable, not empty.
        locked = os.path.join(tmp, "runs", "locked")
        os.makedirs(locked)
        write("runs", "locked", "config.json", body="{}")
        os.chmod(locked, 0)
        try:
            out2 = walk(os.path.join(tmp, "runs"))
            row = [n for n in out2["not_runs"] if n["path"].endswith("locked")]
            unreadable = bool(row) and row[0]["reason"].startswith("could not read")
            root_user = os.geteuid() == 0 if hasattr(os, "geteuid") else False
            case("19 an unreadable directory says `could not read`, never `holds no config`",
                 unreadable or root_user,
                 "got {}".format(row[0]["reason"] if row else "no row"))
        finally:
            os.chmod(locked, 0o700)

        # 20. A README.txt in the parent does not hide the runs beneath it, and
        # artifact directories are excluded by name and reported.
        write("coll", "README.txt", body="these are my runs\n")
        write("coll", "seed1", "config.json", body=json.dumps({"seed": 1, "lr": 0.1}))
        write("coll", "seed1", "metrics.csv", body="step,acc\n1,0.5\n")
        write("coll", "seed2", "config.json", body=json.dumps({"seed": 2, "lr": 0.1}))
        write("coll", "seed2", "metrics.csv", body="step,acc\n1,0.6\n")
        write("coll", "seed1", "checkpoints", "epoch1.pt", body="")
        write("coll", "seed1", "checkpoints", "config.json", body=json.dumps({"seed": 1}))
        write("coll", "other", "config.json", body=json.dumps({"seed": 3, "lr": 0.2}))
        coll = walk(os.path.join(tmp, "coll"))
        found = sorted(r["path"] for r in coll["runs"])
        case("20 a README.txt beside the runs does not make the parent the run",
             found == ["other", "seed1", "seed2"], "got {}".format(found))
        case("20b an artifact directory is excluded by name and reported",
             any(e["path"].endswith(os.path.join("seed1", "checkpoints")) and "artifact" in e["reason"]
                 for e in coll["excluded"]),
             "got {}".format(coll["excluded"]))
        case("20c a .txt that is not a log is not a log", classify("README.txt") is None
             and classify("requirements.txt") is None and classify("train_log.txt") == "log")

        # 21. Two runs that differ only in seed share a condition hash; a run
        # that differs in anything else does not.
        by = {r["path"]: r for r in coll["runs"]}
        case("21 runs differing only in seed share a condition hash and not a config hash",
             by["seed1"]["condition_hash"] == by["seed2"]["condition_hash"]
             and by["seed1"]["config_hash"] != by["seed2"]["config_hash"],
             "got {} / {}".format(by["seed1"]["condition_hash"][:8], by["seed2"]["condition_hash"][:8]))
        case("21b a run differing in a setting has a different condition hash",
             by["other"]["condition_hash"] != by["seed1"]["condition_hash"])
        case("21c the condition count is reported", coll["counts"]["conditions"] == 2,
             "got {}".format(coll["counts"]))
        case("21d key order does not change the condition hash",
             condition_hash({"a": 1, "seed": 4, "b": {"c": 2}}) == condition_hash({"b": {"c": 2}, "a": 1, "seed": 9}))
        case("21e an unparseable config has no condition hash",
             d.get("condition_hash") is None)

        # 22. A run that contains runs says so.
        write("nest", "config.json", body=json.dumps({"lr": 1}))
        write("nest", "inner", "config.json", body=json.dumps({"seed": 1}))
        write("nest", "inner", "metrics.csv", body="s,a\n1,1\n")
        nest = {r["path"]: r for r in walk(os.path.join(tmp, "nest"))["runs"]}
        case("22 a run that contains runs reports the count rather than hiding them",
             nest.get("nest", {}).get("contains_runs") == 1 and "inner" in nest,
             "got {}".format({k: v.get("contains_runs") for k, v in nest.items()}))

        # 17. A missing root is the one error.
        case("17 a root that does not exist exits non-zero",
             main([os.path.join(tmp, "nope")]) != 0)

    print()
    if failures:
        print("{} FAILED: {}".format(len(failures), ", ".join(failures)))
        return 1
    print("all checks passed")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) != 1:
        print("usage: ingest_runs.py <directory>   |   ingest_runs.py --selftest",
              file=sys.stderr)
        return 2
    root = argv[0]
    if not os.path.isdir(root):
        print(json.dumps({"verb": "ingest", "root": os.path.abspath(root),
                          "state": "no such directory"}))
        return 1
    print(json.dumps(walk(root), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
