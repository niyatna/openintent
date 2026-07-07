# Reference: native-mcp

# native-mcp

Use `native-mcp` to discover, call, and manage [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) servers and tools directly from the terminal.

## Prerequisites

Requires Node.js:
```bash
# No install needed (runs via npx)
npx native-mcp list

# Or install globally
npm install -g native-mcp
```

## Quick Start

```bash
# List MCP servers already configured on this machine
native-mcp list

# List tools for a specific server with schema details
native-mcp list <server> --schema

# Call a tool
native-mcp call <server.tool> key=value
```

## Discovering MCP Servers

native-mcp auto-discovers servers configured by other MCP clients (Claude Desktop, Cursor, etc.) on the machine. To find new servers to use, browse registries like [mcpfinder.dev](https://mcpfinder.dev) or [mcp.so](https://mcp.so), then connect ad-hoc:

```bash
# Connect to any MCP server by URL (no config needed)
native-mcp list --http-url https://some-mcp-server.com --name my_server

# Or run a stdio server on the fly
native-mcp list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

## Calling Tools

```bash
# Key=value syntax
native-mcp call linear.list_issues team=ENG limit:5

# Function syntax
native-mcp call "linear.create_issue(title: \"Bug fix needed\")"

# Ad-hoc HTTP server (no config needed)
native-mcp call https://api.example.com/mcp.fetch url=https://example.com

# Ad-hoc stdio server
native-mcp call --stdio "bun run ./server.ts" scrape url=https://example.com

# JSON payload
native-mcp call <server.tool> --args '{"limit": 5}'

# Machine-readable output (recommended for Hermes)
native-mcp call <server.tool> key=value --output json
```

## Auth and Config

```bash
# OAuth login for a server
native-mcp auth <server | url> [--reset]

# Manage config
native-mcp config list
native-mcp config get <key>
native-mcp config add <server>
native-mcp config remove <server>
native-mcp config import <path>
```

Config file location: `./config/native-mcp.json` (override with `--config`).

## Daemon

For persistent server connections:
```bash
native-mcp daemon start
native-mcp daemon status
native-mcp daemon stop
native-mcp daemon restart
```

## Code Generation

```bash
# Generate a CLI wrapper for an MCP server
native-mcp generate-cli --server <name>
native-mcp generate-cli --command <url>

# Inspect a generated CLI
native-mcp inspect-cli <path> [--json]

# Generate TypeScript types/client
native-mcp emit-ts <server> --mode client
native-mcp emit-ts <server> --mode types
```

## Notes

- Use `--output json` for structured output that's easier to parse
- Ad-hoc servers (HTTP URL or `--stdio` command) work without any config — useful for one-off calls
- OAuth auth may require interactive browser flow — use `terminal(command="native-mcp auth <server>", pty=true)` if needed