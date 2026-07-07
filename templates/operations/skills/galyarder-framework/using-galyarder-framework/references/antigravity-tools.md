# Antigravity CLI Tool Mapping

Skills use Claude Code tool names. When you encounter these in a skill, use your platform equivalent:

| Skill references | Antigravity CLI equivalent |
|-----------------|----------------------|
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search file content) | `grep_search` |
| `Glob` (search files by name) | `glob` |
| `TodoWrite` (task tracking) | `write_todos` |
| `Skill` tool (invoke a skill) | `activate_skill` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `Task` tool (dispatch subagent) | No equivalent  Antigravity CLI does not support subagents |

## No subagent support

Antigravity CLI has no equivalent to Claude Code's `Task` tool. Skills that rely on subagent dispatch (`writing-writing-planss`, `dispatching-parallel-agents`) will fall back to single-session execution via `executing-writing-planss`.

## Additional Antigravity CLI tools

These tools are available in Antigravity CLI but have no Claude Code equivalent:

| Tool | Purpose |
|------|---------|
| `list_directory` | List files and subdirectories |
| `save_memory` | Persist facts to GEMINI.md across sessions |
| `ask_user` | Request structured input from the user |
| `tracker_create_task` | Rich task management (create, update, list, visualize) |
| `enter_writing-plans_mode` / `exit_writing-plans_mode` | Switch to read-only research mode before making changes |

## Founder Expansion Routing

For founder-facing tasks in Antigravity, the founder / fundraising stack is an optional expansion path, not a mandatory default.

Use the `galyarder-cfo-coo` role plus the founder-oriented skills when the task involves:
- fundraising or investor pipeline work
- deck narrative, investor outreach, or board updates
- accelerator applications
- market narrative or founder-led sales qualification
- founder thought leadership and founder-brand distribution

Do not inject this layer into ordinary coding, debugging, or architecture work unless the user is clearly working on startup-building tasks.

---
 2026 Galyarder Labs. Galyarder Framework.
