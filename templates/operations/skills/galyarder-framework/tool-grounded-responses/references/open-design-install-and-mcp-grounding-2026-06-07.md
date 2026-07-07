# Open Design install/MCP grounding lesson — 2026-06-07

## Trigger

Use this note when Galih asks whether to install or integrate a third-party local workspace that advertises a CLI, web daemon, MCP server, or one-line installer.

## Lesson

Do not answer from README marketing claims alone. Ground the recommendation in live repo/source inspection and, when relevant, inspect the actual hosted installer response before recommending a pipe-to-shell flow.

In the Open Design review, the repo did expose a local web daemon, `od` CLI, stdio MCP server, Docker setup, and manual Hermes MCP snippet path. But the advertised hosted installer endpoint returned an HTML page during inspection, not a shell script. The durable lesson is not “the installer is broken”; it is: inspect first, then choose the safer integration lane.

## Preferred answer shape for Galih

- State the role split: existing Hermes/Keiya reasoning stays in charge; the new tool is an external workspace/render/preview/export layer.
- Give install recommendation based on weight and rollback: Docker/local daemon first, source build only if needed.
- For Hermes MCP, prefer dry/manual snippet inspection before editing any profile config.
- Avoid importing large third-party skill packs into Keiya/default unless explicitly requested.
- Keep the reply short and operational: verdict, weight, route, gates.

## Verification points to check

- Repo structure and package metadata for actual CLI/MCP entrypoints.
- Docker or service config for port, data directory, memory limit, bind host, and health check.
- MCP server tool list or source definitions so the user knows what Hermes will actually gain.
- Whether the target agent installer writes config automatically or only prints a snippet.
- Local machine readiness only as current-state evidence, not as a permanent rule.
