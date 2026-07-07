# CodeGraph MCP + Hermes Verification Pattern

Session-derived pattern for verifying CodeGraph or any project-scoped MCP integration in Hermes without mistaking launch context for capability absence.

## Trigger

Use this when the user says CodeGraph/MCP was installed, asks whether an MCP is active, or you are about to claim a project-scoped MCP server is unavailable.

## Durable Lessons

1. **Verify the intended Hermes profile explicitly.**
   Use `hermes --profile <profile> config path`, `hermes --profile <profile> mcp list`, and `hermes --profile <profile> mcp test <server>` rather than bare `hermes ...` when Keiya/default and Galyarder both exist.

2. **CodeGraph tools are project-scoped.**
   CodeGraph exposes tools only when the MCP process can resolve an initialized `.codegraph/` root. Testing from an unindexed cwd can return `Tools discovered: 0` even when the server is correctly installed. Test from the indexed project root or configure/launch the server with an explicit path.

3. **Do not conclude absence from the current chat registry.**
   MCP config changes require a fresh Hermes session/gateway restart before newly added tools appear in the active tool list. Current-session `tool_search` can lag behind config writes.

4. **Hide option-looking stdio args behind a wrapper when CLI parsing fights you.**
   If `hermes mcp add ... --args serve --mcp` is parsed incorrectly because `--mcp` looks like a Hermes option, create a stable wrapper script such as:

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   exec /absolute/path/to/codegraph serve --mcp "$@"
   ```

   Then register the wrapper as the MCP command:

   ```bash
   hermes --profile galyarder mcp add codegraph --command /home/galyarder/.local/bin/codegraph-mcp
   ```

5. **Prefer stable launch paths over shell-session PATH assumptions.**
   If CodeGraph was installed under NVM or another user-local Node prefix, either use the absolute binary path in the wrapper or ensure the gateway/service environment actually includes that PATH.

## Verification Ladder

```bash
# 1. Confirm project index
codegraph status /path/to/project

# 2. Confirm profile-specific MCP registration
hermes --profile galyarder mcp list

# 3. Test from the indexed project root
cd /path/to/project
hermes --profile galyarder mcp test codegraph

# Expected: tools discovered (e.g. codegraph_search, codegraph_callers,
# codegraph_node, codegraph_explore). If testing outside the indexed root,
# zero tools can be a context issue, not a broken install.
```

## Reporting Pattern

Keep the user-facing status short:

- `installed + indexed: <files/nodes/edges>`
- `registered for profile: <profile>`
- `MCP test from indexed root: <tool count>`
- `needs restart: yes/no`
