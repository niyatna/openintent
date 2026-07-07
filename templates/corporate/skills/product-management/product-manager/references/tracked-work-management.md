# Reference: product-manager

# Tracked Work Management

Use this skill when Galyarder workflows need product work translated into clear tracked items. In Hermes, the default tracker is native and lightweight:

- Use `todo` for current-session execution writing-planss and status.
- Use a project issue tracker only when the user explicitly wants durable external tracking.
- Use reports under the active repo or `~/.hermes/reports/` when the output needs a handoff artifact.

## Workflow

1. Break the request into epics or vertical slices.
2. Convert each slice into an actionable tracked item with owner/context, acceptance criteria, and verification evidence.
3. Keep exactly one current item in progress when using `todo`.
4. Link final summaries back to the active todo/report/issue before claiming completion.

## Hermes Tool Mapping

- Session-local tracking -> `todo`
- Parallel investigation or review -> `delegate_task`
- Durable handoff -> `write_file` into the active repo docs or `~/.hermes/reports/`

Always verify tool outputs before claiming completion.