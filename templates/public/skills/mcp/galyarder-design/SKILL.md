---
author: Galyarder Labs
description: Use when operating the local Galyarder Design canvas, starting gd CLI
  watch deamons, or loading the gd MCP wrapper.
license: Apache-2.0
metadata:
  hermes:
    category: mcp
    tags:
    - galyarder-design
    - design
    - mcp
    - cli
    - local-first
name: galyarder-design
version: 1.0.0
---


# Galyarder Design

## Purpose

Use this skill when Galih asks about **Galyarder Design**, `gd`, design prototypes, local design preview/export, Galyarder Design MCP tools, or whether to use upstream Open Design.

Galyarder Design is Galih's OSS local-first design engine at:

```text
/home/galyarder/projects/galyarder-design
https://github.com/galyarderlabs/galyarder-design
```

It is a fork/variant of Open Design, but it is the primary local engine for Galih's workflow. It uses the `gd` CLI, not `od`.

## Current Local Route

Primary service:

```bash
systemctl --user status galyarder-design.service --no-pager -l
systemctl --user start galyarder-design.service
systemctl --user enable galyarder-design.service
systemctl --user restart galyarder-design.service
```

Service unit:

```text
~/.config/systemd/user/galyarder-design.service
```

It runs:

```bash
pnpm tools-dev run web --daemon-port 7456 --web-port 7457
```

Expected URLs:

```text
Daemon/API: http://127.0.0.1:7456
Web UI:     http://127.0.0.1:7457
Health:     http://127.0.0.1:7456/api/health
```

Verification:

```bash
curl -s http://127.0.0.1:7456/api/health
curl -sI http://127.0.0.1:7457/ | head
PATH=/home/galyarder/.nvm/versions/node/v24.15.0/bin:$PATH \
  pnpm tools-dev status --json
```

## CLI

Use the wrapper instead of relying on `pnpm exec gd`:

```bash
/home/galyarder/.local/bin/gd --help
```

The wrapper sets:

```text
GD_DATA_DIR=/home/galyarder/projects/galyarder-design/.gd
```

Common commands:

```bash
gd --help
gd mcp --help
gd diagnostics export /tmp/gd-diagnostics.zip
gd plugin list
gd tools live-artifacts list
gd artifacts create --name demo/index.html --input /tmp/index.html
gd research search --query "design systems" --max-sources 5
```

When a command is project-context dependent, first inspect the web UI active project or use MCP `list_projects` / `get_active_context`.

## MCP Bridge For Hermes And Keiya

Galyarder Design exposes a local stdio MCP server:

```bash
gd mcp --daemon-url http://127.0.0.1:7456
```

Use this wrapper for Hermes MCP registration:

```bash
/home/galyarder/.local/bin/gd-mcp
```

Manual Hermes config shape:

```yaml
mcp_servers:
  galyarder-design:
    command: /home/galyarder/.local/bin/gd-mcp
    enabled: true
    timeout: 180
    connect_timeout: 60
```

Install/register into both profiles:

```bash
printf 'Y\n' | hermes --profile galyarder mcp add galyarder-design \
  --command /home/galyarder/.local/bin/gd-mcp

printf 'Y\n' | hermes --profile default mcp add galyarder-design \
  --command /home/galyarder/.local/bin/gd-mcp
```

Test:

```bash
hermes --profile galyarder mcp test galyarder-design
hermes --profile default mcp test galyarder-design
```

After config changes, start a new Hermes session or restart gateways if Galih wants the live Discord/Telegram agents to see the MCP tools immediately:

```bash
systemctl --user restart hermes-gateway-galyarder.service
systemctl --user restart hermes-gateway.service
```

## MCP Tools Currently Exposed

Current fork exposes 8 MCP tools:

- `list_projects` — list Galyarder Design projects.
- `get_active_context` — project/file currently open in the UI; active context expires after idle time.
- `get_artifact` — preferred way to pull an artifact bundle with referenced sibling files.
- `get_project` — project metadata, active skill/design system, entry file, preview URL.
- `get_file` — read one text file from a project.
- `search_files` — literal substring search across project text files.
- `list_files` — file metadata and artifact manifests.
- `create_artifact` — create one HTML/Markdown/SVG artifact entry file.

Use MCP when Hermes/Keiya needs to inspect, retrieve, create, or hand off Galyarder Design artifacts without zip export/manual file copy.

## When To Use Galyarder Design

Use it for:

- local web/mobile/desktop prototype previews;
- design-system based artifacts;
- design handoff HTML/CSS/source inspection;
- project-scoped design artifact creation;
- letting Hermes/Keiya pull the active design context;
- public OSS workflow around `galyarderlabs/galyarder-design`.

Use Keiya/Galyarder design skills for thinking and review, then use Galyarder Design as the local preview/render/workspace layer.

Recommended stack:

```text
Keiya/Galyarder reasoning -> Galyarder Design artifact workspace -> MCP pull/review/refine
```

## Upstream Open Design Policy

Do **not** install/run upstream `open-design` as the primary live service unless Galih explicitly asks. Upstream is useful as a patch source, but Galyarder Design is the local product.

Use upstream selectively for:

- MCP tool additions;
- `mcp install` writing-plansner ideas;
- daemon/CLI bugfixes;
- Docker/service hardening;
- export/runtime fixes.

Avoid pulling upstream wholesale when it would reintroduce:

- Chinese/i18n UI noise Galih removed;
- SaaS/API/public product baggage not needed locally;
- release automation noise;
- route ambiguity between `od` and `gd`.

## Pitfalls

- `pnpm exec gd` can fail from stale package/symlink resolution such as `ERR_MODULE_NOT_FOUND` for `@modelcontextprotocol/sdk`. Prefer `/home/galyarder/.local/bin/gd`.
- `gd mcp install hermes` does not exist in the current fork. Register with Hermes using `/home/galyarder/.local/bin/gd-mcp`.
- MCP requires the daemon to be running on `127.0.0.1:7456`.
- The web UI is on `7457`, not `7456`; daemon/API is on `7456`.
- Do not start upstream `open-design` on the same ports while Galyarder Design is active.
- Before upstream sync or public OSS release work, inspect local git state; the repo may have uncommitted landing-page changes.

## Verification Before Reporting Done

Minimum proof:

```bash
systemctl --user is-active galyarder-design.service
curl -s http://127.0.0.1:7456/api/health
curl -sI http://127.0.0.1:7457/ | head
/home/galyarder/.local/bin/gd mcp --help
hermes --profile galyarder mcp list | grep -i galyarder-design
hermes --profile default mcp list | grep -i galyarder-design
```

For MCP functionality, run:

```bash
hermes --profile galyarder mcp test galyarder-design
hermes --profile default mcp test galyarder-design
```
