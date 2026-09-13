#!/usr/bin/env python3
"""Write-scope guard for research-bearings agents.

A PreToolUse hook on Write|Edit. Agents shipped by this plugin may only write
under <project>/research/. Everything else — the main thread, other plugins'
agents, Claude Code's built-in agents — passes through untouched.

Per-agent scoping is only possible this way: plugin-shipped agent frontmatter
ignores `hooks`, and PreToolUse has no agent-type matcher, so the script reads
`agent_type` from stdin and scopes itself.

Standard library only, so there is no install story. Run --selftest to check it.
"""

import json
import os
import sys

PLUGIN_PREFIX = "research-bearings:"
WRITE_ROOT = "research"


def _roots(payload, env):
    """Directories a research/ folder may hang off, most authoritative first.

    CLAUDE_PROJECT_DIR stays at the project root even inside a worktree, where
    cwd follows Claude. Both are accepted so neither case is a false denial.
    """
    candidates = [env.get("CLAUDE_PROJECT_DIR"), payload.get("cwd")]
    seen, out = set(), []
    for c in candidates:
        if not c:
            continue
        r = os.path.realpath(c)
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def decide(payload, env):
    """Return a denial reason, or None to allow.

    Allowing is the default for everything this guard does not understand. A
    guard that fails closed would block the user's own edits on a malformed
    payload, which is a worse failure than the one it prevents.
    """
    agent = payload.get("agent_type") or ""
    if not agent.startswith(PLUGIN_PREFIX):
        return None

    path = (payload.get("tool_input") or {}).get("file_path")
    if not path:
        return None

    target = os.path.realpath(path)
    for root in _roots(payload, env):
        allowed = os.path.realpath(os.path.join(root, WRITE_ROOT))
        if target == allowed or target.startswith(allowed + os.sep):
            return None

    return (
        "research-bearings agents may only write under {}/. Refused: {}. "
        "If this agent genuinely needs to write elsewhere, that is a contract "
        "change, not a path change.".format(WRITE_ROOT, target)
    )


def run(stdin_text, env):
    """Return (exit_code, stdout). Used by main and by the selftest."""
    try:
        payload = json.loads(stdin_text)
        if not isinstance(payload, dict):
            return 0, ""
    except (ValueError, TypeError):
        return 0, ""

    reason = decide(payload, env)
    if reason is None:
        return 0, ""

    return 0, json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------


def selftest():
    import tempfile

    failures = []

    def check(name, stdin_text, env, want_deny):
        code, out = run(stdin_text, env)
        got_deny = bool(out) and '"deny"' in out
        ok = code == 0 and got_deny == want_deny
        print("  {} {}".format("PASS" if ok else "FAIL", name))
        if not ok:
            failures.append(name)
            print("       exit={} deny={} (wanted deny={})".format(code, got_deny, want_deny))

    with tempfile.TemporaryDirectory() as project:
        project = os.path.realpath(project)
        os.makedirs(os.path.join(project, "research", "landscape"))
        env = {"CLAUDE_PROJECT_DIR": project}

        def payload(agent, path):
            return json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "agent_type": agent,
                    "cwd": project,
                    "tool_input": {"file_path": path},
                }
            )

        inside = os.path.join(project, "research", "QUESTION.md")
        nested = os.path.join(project, "research", "landscape", "matrix.md")
        at_root = os.path.join(project, "README.md")
        escape = os.path.join(project, "research", "..", "secrets.md")

        print("guard.py selftest")

        # 1. No agent_type at all: the main thread. Never touched.
        check(
            "main thread write is allowed",
            json.dumps({"tool_name": "Write", "cwd": project,
                        "tool_input": {"file_path": at_root}}),
            env, False)

        # 2. Somebody else's agent. Not our business.
        check("another plugin's agent is allowed",
              payload("Explore", at_root), env, False)

        # 3-4. Our agent, inside the write root.
        check("our agent writing inside research/ is allowed",
              payload("research-bearings:question-critic", inside), env, False)
        check("our agent writing deep inside research/ is allowed",
              payload("research-bearings:paper-scout", nested), env, False)

        # 5-7. Our agent, outside the write root.
        check("our agent writing at project root is DENIED",
              payload("research-bearings:question-critic", at_root), env, True)
        check("our agent writing to /tmp is DENIED",
              payload("research-bearings:question-critic", "/tmp/loose.md"), env, True)
        check("our agent escaping via research/.. is DENIED",
              payload("research-bearings:question-critic", escape), env, True)

        # 8. A prefix that merely looks like ours.
        check("a path like research-notes/ does not count as research/",
              payload("research-bearings:question-critic",
                      os.path.join(project, "research-notes", "x.md")), env, True)

        # 9-11. Malformed input must never block the user's own work.
        check("malformed JSON is allowed", "{not json", env, False)
        check("empty stdin is allowed", "", env, False)
        check("JSON that is not an object is allowed", "[1,2,3]", env, False)

        # 12. Our agent, but no file_path in the payload.
        check("missing file_path is allowed",
              json.dumps({"agent_type": "research-bearings:question-critic",
                          "cwd": project, "tool_input": {}}), env, False)

        # 13. No CLAUDE_PROJECT_DIR: fall back to cwd.
        check("falls back to cwd when CLAUDE_PROJECT_DIR is unset",
              payload("research-bearings:question-critic", inside), {}, False)

    print()
    if failures:
        print("{} FAILED: {}".format(len(failures), ", ".join(failures)))
        return 1
    print("all checks passed")
    return 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    code, out = run(sys.stdin.read(), os.environ)
    if out:
        print(out)
    sys.exit(code)


if __name__ == "__main__":
    main()
