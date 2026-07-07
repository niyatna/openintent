---
author: Hermes Agent + Galyarder Labs
description: Use when operating the Linear issue tracking CLI.
license: MIT
metadata:
  hermes:
    category: productivity
    tags:
    - Linear
    - Project Management
    - Issues
    - MCP
    - Productivity
name: linear
version: 2.0.0
---


# Linear — MCP-first workflow

## Current setup

Linear is configured as a remote OAuth MCP server in both Keiya/default and Galyarder profiles:

```yaml
mcp_servers:
  linear:
    url: https://mcp.linear.app/mcp
    enabled: true
    auth: oauth
```

Token files are profile-scoped under `mcp-tokens/linear*.json`.

**Verified live in Galyarder session 2026-05-20:** `mcp_linear_get_user({query: "me"})` returned the Linear user `mhmdgalihsaputra249@gmail.com`, admin, active, team `Galyarder` key `GAL`.

## Rule

Use Hermes native `mcp_linear_*` tools first. Do **not** ask for `LINEAR_API_KEY` unless the MCP tools are missing or unauthorized.

The old direct GraphQL + `LINEAR_API_KEY` path is fallback only.

## Read workflow

Common read tools:

- `mcp_linear_get_user({query: "me"})` — verify auth/current user.
- `mcp_linear_list_teams({})` / `mcp_linear_get_team({query})` — teams.
- `mcp_linear_list_projects({})` / `mcp_linear_get_project({query})` — projects.
- `mcp_linear_list_issues({team, state, assignee, project, label, limit})` — issue lists.
- `mcp_linear_get_issue({id, includeRelations, includeCustomerNeeds, includeReleases})` — issue detail.
- `mcp_linear_list_comments({issueId})` — comments.
- `mcp_linear_list_issue_statuses({team})` — statuses/state names.
- `mcp_linear_list_issue_labels({team})` — labels.
- `mcp_linear_get_diff({urlOrId})` and `mcp_linear_get_diff_threads({urlOrId})` — reviews/diffs.

## Write workflow

Common write tools:

- `mcp_linear_save_issue(...)` — create/update issues.
- `mcp_linear_save_comment(...)` — create/update comments/replies.
- `mcp_linear_save_project(...)` — create/update projects.
- `mcp_linear_save_document(...)` — create/update docs.
- `mcp_linear_save_status_update(...)` — project/initiative updates.
- `mcp_linear_prepare_attachment_upload(...)` → direct PUT → `mcp_linear_create_attachment_from_upload(...)` — large attachments.

## Confirmation boundaries

Autonomous by default:

- read/list/search Linear state;
- create drafts in chat;
- create/update private/internal issues when Galih explicitly asks;
- comment with a status update when Galih explicitly asks.

Ask first before:

- deleting/archiving records;
- bulk moving/changing many issues;
- changing customer/project/initiative status with broad impact;
- posting as Galih externally if content affects public/customer/investor communication.

## Verification checklist

Before claiming done:

1. Run the actual MCP mutation/read command.
2. Read the returned ID/identifier/status.
3. Re-fetch the created/updated entity (`get_issue`, `get_project`, etc.) when the side effect matters.
4. Report the identifier/URL and exact state.

## Fallback: direct GraphQL

Only if MCP tools are unavailable/unauthorized, use Linear GraphQL API with `curl` and `LINEAR_API_KEY`.

- Endpoint: `https://api.linear.app/graphql`
- Auth header for personal API keys: `Authorization: $LINEAR_API_KEY`
- Always inspect GraphQL `errors` even when HTTP status is 200.
