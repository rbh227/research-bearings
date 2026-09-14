---
name: setup
description: Record a research project's resources and constraints before any research work begins — lab, compute allocation, data access, code, your calibration, deadline, and what counts as a win. Use when starting a research project, when picking up an inherited one, or when compute or data access changes. Writes research/CONTEXT.md.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(df:*), Bash(du:*), Bash(ls:*), Bash(uname:*), Bash(sw_vers:*), Bash(nvidia-smi:*), Bash(python3:*), Bash(pip:*), Bash(uv:*), Bash(git status:*), Bash(git log:*), Bash(git remote:*), Bash(free:*), Bash(sysctl:*), Bash(nproc:*), Bash(test:*), Bash(find:*), Bash(wc:*)
---

# setup

One job: fill `research/CONTEXT.md`. Nothing else. You do not frame a question
here — that is `/research-bearings:frame`, and it reads what you write.

## The rule that shapes this skill

**Check first, then ask.** Anything true of this machine is a fact you can go
and get. Asking the user for it wastes their attention and gets a worse answer,
because people misremember their own disk space. Anything you cannot check, you
ask — and you write the answer with **the date they told you**, so a stale
figure is visibly stale instead of quietly wrong.

## Steps

**1. Check what you can.** Before asking anything, run the checks below and keep
the results. Do this in one batch; it takes seconds.

| What | How |
|---|---|
| Disk free, per volume | `df -h` |
| Sizes of candidate data directories | `du -sh` on plausible ones found via `ls` / `find` |
| GPU presence and model | `nvidia-smi` (absent on most Macs — that is itself the answer) |
| CPU and memory | `sysctl -n hw.ncpu hw.memsize` on macOS, `nproc` and `free -h` on Linux |
| OS | `sw_vers` or `uname -a` |
| Python and env | `python3 --version`, `uv --version`, `pip list` if a venv is obvious |
| Repo state | `git remote -v`, `git status --short`, `git log --oneline -5` |
| What is already here | `ls` the project root; look for data, notebooks, papers, a README |
| Retrieval | `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieval/snowball.py" health` — reports key presence without spending a request. Nothing to connect to: retrieval is one script, run on demand. `/research-bearings:scout` probes the API itself at the start of every crawl. |

**2. Read anything that answers a question for you.** A README, a proposal, a
grant blurb, an existing notes file. Do not ask what a file already says.

**3. Copy the template.** `${CLAUDE_PLUGIN_ROOT}/templates/research/CONTEXT.md`
to `research/CONTEXT.md`, creating `research/` if needed. If the project has a
`.gitignore`, add `research/.papers/` and `research/.crawl/` to it — the paper cache is regenerable and
runs to thousands of files. If the file already
exists, read it and update in place — never clobber a section that has content
without showing the user what you are replacing.

**4. Interview, one section at a time.** Work down the ten headings in order.
For each: state what you already know from step 1, ask only what is missing,
then write that section before moving on. A session that dies halfway leaves a
half-filled file, not nothing.

Ask in plain prose. Most of these answers are numbers, names and sentences, not
choices, so multiple choice is the wrong instrument here.

**5. Mark the unknowns.** Any section the user cannot or will not answer gets
`_unknown_` or `_not applicable_`. Never omit a heading. Never invent content.

## Output

`research/CONTEXT.md`, ten fixed headings, in this order:

| Heading | What goes in it | Where it comes from |
|---|---|---|
| `## Project` | What this project is in one line; new, inherited or continuing; the deliverable and its deadline; who it is for | ask |
| `## People` | Lab, PI, collaborators and who owns what, who nearby works on adjacent things, who you ask when stuck | ask |
| `## Compute` | Where it lives; the allocation in units that bind (service units, GPU-hours, node flavours, wall-clock caps); what is contended; what is already burned | local checked, remote asked and dated |
| `## Storage and data` | Volumes and sizes; datasets held now; licence or IRB access; what is behind a request form and how long it takes | sizes checked, access asked |
| `## Code` | Repos owned or inherited; what runs today; what is known-broken; the environment; **whether a working baseline exists** | repo state checked, rest asked |
| `## Calibration` | What they know cold, what they are shaky on, what they could reimplement in an afternoon | ask |
| `## Constraints` | Hours per week actually available; teaching load; publication obligations or embargoes; hardware they cannot get | ask |
| `## What counts as a win` | Which venue or artefact, by when, and who has to accept it | ask |
| `## History` | What this project already tried, and why it stopped | ask |
| `## Retrieval` | Whether the retrieval script runs, whether a Semantic Scholar key is present, the date probed | checked |

Mark every checked number `(checked YYYY-MM-DD)` and every reported number
`(reported YYYY-MM-DD)`. The distinction is the point.

## Stop condition

All ten headings present. Each has content or an explicit `_unknown_`. Every
number carries a date and says whether it was checked or reported.

Then tell the user what to run next: `/research-bearings:frame`.

## Rules this skill applies

**Ask whether a working baseline exists.** Most progress comes from having one
you can modify, so its absence is the single most useful thing in the file.
— Schulman; `academic.md` § How research actually works

**A win condition names a decision, not a number.** "Better mAP" is not a win.
"Accepted at the CVPR workshop, which my funding renewal depends on" is.
— Wagstaff; `academic.md` § How research actually works

**Abstention beats a guess.** `_unknown_` is a valid and preferred answer.
— `academic.md` § Keeping agents honest

## Refusals

| The shortcut | Why you don't |
|---|---|
| "I'll ask how much disk they have." | You have Bash. Run `df -h`, then report it. |
| "Close enough on the allocation." | Write the figure and the date you were told it, or write `_unknown_`. |
| "They're a CS grad student, they know Python." | Calibration is what they tell you, never what you infer from their role. |
| "The win is a good paper." | Which venue, by when, and who has to accept it. |
| "New project, so no History section." | Ask anyway. New projects usually inherit something, and what was abandoned is worth knowing. |
| "I'll fill the thin sections with reasonable defaults." | There are no default labs, deadlines or allocations. `_unknown_`. |
| "I'll ask all thirty questions at once so it's efficient." | Ten sections, one at a time, writing as you go. Efficiency that loses the whole session on an interruption is not efficiency. |
| "I'll ask whether they set up a Semantic Scholar key." | Call `health`. It answers without a network request, and the user's memory of what they configured is worse than the script's. |
