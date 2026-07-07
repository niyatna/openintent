---
name: notion
description: Use when querying Notion workspace databases, designing properties tables filters, or matching Notion/Airtable API records.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [productivity, notion, notion-mcp, airtable, databases]
    category: productivity
---

# Notion — MCP-first workflow

## Current setup

Notion is configured as a remote OAuth MCP server in both Keiya/default and Galyarder profiles:

```yaml
mcp_servers:
  notion:
    url: https://mcp.notion.com/mcp
    enabled: true
    auth: oauth
```

Token files are profile-scoped under `mcp-tokens/notion*.json`.

**Verified live in Galyarder session 2026-05-20:** `mcp_notion_notion_get_users({user_id: "self", page_size: 1})` returned workspace user `Galyarder Labs` / `galyarderos@gmail.com`.

## Rule

Use Hermes native `mcp_notion_*` tools first. Do **not** ask for `NOTION_API_KEY` unless the MCP tools are missing or unauthorized.

The old direct Notion API + integration token path is fallback only.

## Read/search workflow

Common tools:

- `mcp_notion_notion_search({query, query_type, page_size})` — workspace/user search.
- `mcp_notion_notion_fetch({id, include_discussions})` — fetch page/database/data source by URL/ID.
- `mcp_notion_notion_get_comments({page_id, include_all_blocks})` — discussions/comments.
- `mcp_notion_notion_get_users({user_id: "self"})` — verify auth/current user.
- `mcp_notion_notion_get_teams({query})` — teamspaces.

## Write workflow

Common tools:

- `mcp_notion_notion_create_pages(...)` — create one or more pages.
- `mcp_notion_notion_update_page(...)` — update properties/content; fetch first before content replacement.
- `mcp_notion_notion_create_database(...)` — create database/data source with SQL DDL.
- `mcp_notion_notion_update_data_source(...)` — schema/title updates.
- `mcp_notion_notion_create_view(...)` / `mcp_notion_notion_update_view(...)` — views.
- `mcp_notion_notion_create_comment(...)` — comments/replies.

## Markdown/spec rule

Before creating/updating Notion page content, fetch the Notion markdown spec if exact rendering matters:

- `mcp_notion_read_resource({uri: "notion://docs/enhanced-markdown-spec"})`

For view DSL, fetch:

- `mcp_notion_read_resource({uri: "notion://docs/view-dsl-spec"})`

## Confirmation boundaries

Autonomous by default:

- read/search/fetch workspace content;
- draft page/database changes in chat;
- create/update pages when Galih explicitly asks.

Ask first before:

- deleting/trashing/moving important pages/databases;
- sharing/inviting/public-link changes;
- replacing entire page content if child pages/databases may be deleted;
- bulk operations.

## Verification checklist

Before claiming done:

1. Run the actual MCP mutation/read command.
2. Capture returned page/database/comment/view ID/URL.
3. Re-fetch the entity when the side effect matters.
4. Report the URL/ID and exact state.

## Fallback: direct Notion API

Only if MCP tools are unavailable/unauthorized, use the direct Notion API with `NOTION_API_KEY`.

- Header: `Authorization: Bearer $NOTION_API_KEY`
- Header: `Notion-Version: <current supported version>`
- Target pages/databases must be connected to the integration.

## References & Sub-playbooks
- `references/notion.md` — In-depth specifications for Notion REST and Airtable bases configurations
