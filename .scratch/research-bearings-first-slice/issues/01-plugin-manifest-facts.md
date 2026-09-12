# Plugin manifest facts

Type: research
Status: resolved
Blocked by: 

## Question

What do Claude Code's `plugin.json` and `marketplace.json` accept for skills, agents, hooks, and MCP servers? What frontmatter fields does an agent file support, specifically tool allowlists and `model`? How are env vars expanded in a plugin's `.mcp.json`? How does a skill dispatch a named agent bundled by the plugin? Cite the official docs; note anything the build plan assumes that the docs contradict.

## Answer

Full findings: `docs/research/plugin-manifest-facts.md` on branch `research/plugin-manifest-facts` (commit ba8bf86).

- `plugin.json` requires only `name`. Component fields are `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`, paths relative to the plugin root and starting `./`. Default locations (`skills/`, `agents/`, `hooks/hooks.json`, `.mcp.json`) are auto-discovered, so a default-layout plugin needs no component fields. Listing `agents` *replaces* the default scan.
- `marketplace.json` needs `name`, `owner`, and `plugins[]` with `name` and `source`. A relative `source: "./"` works for git and local marketplaces. `version` in `plugin.json` wins over the marketplace entry.
- Agent frontmatter: `name` and `description` required; `tools` / `disallowedTools` accept patterns like `Bash(git push *)`, `mcp__server__*`, `Agent(a, b)`; `model` accepts `sonnet|opus|haiku|fable|<full id>|inherit`; also `effort`, `maxTurns`, `skills`, `memory`, `background`, `isolation: worktree`.
- Plugin-shipped agents ignore `hooks`, `mcpServers`, and `permissionMode` in frontmatter. The write-scope guard must live in `hooks/hooks.json`, keyed on `agent_type` from the hook's stdin.
- `.mcp.json` expands `${VAR}` and `${VAR:-default}` in `command`, `args`, `env`, `url`, `headers`, plus `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.KEY}`.
- Bundled MCP servers register as `plugin:<plugin>:<server>`; their tools are named `mcp__plugin_<plugin>_<server>__<tool>`. Agent allowlists must use these scoped names.
- A skill dispatches a bundled agent by calling the `Agent` tool with `subagent_type: "plugin-name:agent-name"` from an inline skill.
- **Contradicts the build plan**: the manifest field is `mcpServers`, not `mcp`; listing `skills, agents, hooks` in `plugin.json` is unnecessary and `agents` would force every file to be listed.
- **Gaps the plan misses**: fan-out skills must stay inline, since forked or background subagents lose the `Agent` tool. Python `scripts/` get no auto-install; `similarity.py` and friends need a `SessionStart` install into `${CLAUDE_PLUGIN_DATA}` or a `uvx`-style zero-install path.
