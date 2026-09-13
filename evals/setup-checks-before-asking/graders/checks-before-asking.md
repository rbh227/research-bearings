---
type: llm
focus: trace
weight: 1
---
The agent must GATHER FACTS FROM THE MACHINE BEFORE ASKING THE USER FOR THEM.

Pass only if the transcript shows shell commands discovering the environment —
disk space (`df`), directory sizes (`du`), hardware (`nvidia-smi`, `sysctl`,
`nproc`, `uname`, `sw_vers`), tool versions (`python3 --version`), or repository
state (`git remote`, `git status`) — AND it does so before asking the user any
question those commands would have answered.

Fail if the agent asks how much disk, memory, GPU or CPU is available, or which
Python version is installed, without trying to find out. Fail if it makes no
shell calls at all.

Asking about things genuinely not discoverable from this machine — the PI's
name, a remote cluster allocation, the deadline, what counts as a win — is
correct and must not be penalised.
