# Reference: notion

# Workspace Databases (Notion & Airtable)

A unified class-level guide for interacting with no-code databases and workspace tables: Notion and Airtable.

---

## 1. Notion Workspace Management

Manage tables, pages, and workspace integrations via Notion MCP.

### Setup
Notion is configured via the MCP server endpoint:
`https://mcp.notion.com/mcp`

### Key Tools
- **Search**: `mcp_notion_notion_search`
- **Read**: `mcp_notion_notion_fetch`
- **Create Page**: `mcp_notion_notion_create_page`
- **Update Page**: `mcp_notion_notion_patch_page`

For detailed parameters, OAuth configuration, and usage snippets, see [references/notion-mcp.md](references/notion-mcp.md).

---

## 2. Airtable Bases and Records

Interact with Airtable databases directly via HTTP REST API.

### Setup
- Authentication keys: Personal keys from Airtable developer dashboard, loaded as environment variables in the session.
- Base endpoint: `https://api.airtable.com/v0`

For detailed lookup parameters, filter formulas, cell types, schemas, and pagination scripts, see [references/airtable-cli.md](references/airtable-cli.md).