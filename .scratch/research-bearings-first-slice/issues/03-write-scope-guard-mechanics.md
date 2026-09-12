# Write-scope guard mechanics

Type: research
Status: resolved
Blocked by: 

## Question

How does a Claude Code PreToolUse hook receive a tool call and block it? What is the hook input schema for Write, Edit, and Bash, and what exit code or JSON blocks the call? Can a hook scope by plugin, agent, or path? How does a SessionStart hook announce itself? Cite the official hooks reference.

## Answer

Full findings: `docs/research/write-scope-guard-mechanics.md` on branch `research/write-scope-guard-mechanics` (commit e2533bd). Includes a working `hooks.json`, a Python guard script, and an announce script, exercised against six synthetic inputs.

- A `PreToolUse` command hook gets the call as JSON on stdin: `tool_name`, `tool_input`, `tool_use_id`, plus `cwd`, `agent_id`, `agent_type`. `Write` input is `{file_path, content}`; `Edit` is `{file_path, old_string, new_string, replace_all}`; `Bash` is `{command, ...}`. `file_path` arrives absolute.
- Block with exit 2 (stderr becomes the denial reason) or exit 0 printing `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}`. Allow with exit 0 and empty stdout. Exit 1 does not block, and a missing or non-executable script silently allows.
- Per-plugin scoping: yes, via `hooks/hooks.json`, active only while the plugin is enabled, scripts referenced by `${CLAUDE_PLUGIN_ROOT}`.
- Per-path scoping: `matcher` filters on tool name only. The handler `if` field is best-effort with no negation, so the script does the "outside `landscape/`" check itself. A session-wide `Edit(...)` deny permission rule is the hard alternative.
- **Per-agent scoping is possible one way only**: plugin agents cannot carry `hooks` frontmatter and `PreToolUse` has no agent-type matcher, but plugin hooks do run inside sub-agents with `agent_type` set to `<plugin>:<agent>`. The script scopes itself on that field and passes everything else through.
- `SessionStart` cannot block. It announces via `systemMessage` and injects context via stdout or `hookSpecificOutput.additionalContext`. Matchers: `startup|resume|clear|compact|fork`.
- Design recommendation: remove `Bash` from landscape-writing agents via `disallowedTools` so the guard only needs `Write|Edit`; treat the Bash-redirect branch as heuristic defence in depth. Write the guard in Python, not `jq`, since `jq` isn't installed and a script that fails to start silently allows.
