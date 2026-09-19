# Fixtures for the front-door and loop cases

`assemble.sh <shape> [target]` builds a `research/` folder from the files the
live runs left under `landscape/runs/` and `read/runs/`. Six shapes:

| Shape | Holds |
|---|---|
| `empty` | nothing; no `research/` folder |
| `question-only` | the wildfire `QUESTION.md` alone |
| `wildfire-surveyed` | the wildfire question and its surveys file |
| `wildfire` | the wildfire question and its full landscape, no cards |
| `damage` | the damage question, landscape, three cards, datasets, groups, a bits file dated before two of the cards, one critique |
| `selection` | `damage` plus six **synthetic** idea pages and six pre-mortems from `selection/`, two of them not executable |

Every shape but `selection` copies and never invents. `selection/` is the one
synthetic fixture: template-shaped pages whose first comment says they are
invented, so that `/rank`'s pairing bound and set-aside rule have something to
run on. They are not research.

The dates the assembler sets are explained at the top of the script: git keeps
none, so they are stamped in the order the files were made, with `BITS.md`
before the two newest cards.

## Running the cases

Each case that needs a folder carries a `case.yaml` naming a `scaffold.sh`
that calls the assembler into the run's workspace. Scaffolds run only when
asked; the router, the composites and most loop skills need Bash for the
plugin's own scripts; the skills that dispatch agents need `Agent`, which is
in the read-only allowlist. A run is:

```bash
claude plugin eval . --scaffold --allow-tools "Bash(python3 *)"
```

Bash under the harness is sandboxed with no network unless a domain is
granted. That is deliberate for the cases tagged `offline`: they grade what a
skill does when the index cannot be reached. The cases tagged `needs-network`
grade a dispatch that will fail offline; run them with the domains in
`docs/APIS.md` granted, or read their transcripts knowing the searcher could
not search.

The expected facts in each `llm` grader were read from
`python3 scripts/state.py <assembled folder>` on the day the case was written,
and `check_cases.py` holds them to it: it assembles every shape, reads it with
the state script and asserts each fact a grader quotes. It runs in the
toolchain's static-checks verb. When the table or a fixture changes, it fails,
and the grader or the table is corrected — never this check alone.

```bash
python3 evals/fixtures/check_cases.py
```

To look at a shape by hand:

```bash
evals/fixtures/assemble.sh damage /tmp/dmg/research && python3 scripts/state.py /tmp/dmg/research
```
