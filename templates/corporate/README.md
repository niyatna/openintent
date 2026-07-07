# niyatna Hermes Profile Distribution

Version: `0.1.0`

Niyatna Hermes profile: formation operator, secure department workflows, HQ task coordination, memory updates, automations, and Proof of Intent.

## Install / update

```bash
hermes profile install /home/galyarder/.hermes/profile-distributions/niyatna-profile --name niyatna --alias
hermes profile update niyatna
hermes profile info niyatna
```

## Secrets and memory

Real credentials are intentionally excluded. Copy `.env.EXAMPLE` to `.env` on the target machine and fill values.

Curated hot-memory files are intentionally included for profile continuity:

- `memories/USER.md`
- `memories/MEMORY.md`

These files contain stable facts only. Raw archives, sessions, runtime databases, auth files, tokens, logs, browser state, gateway state, and private disaster-recovery archives remain excluded.

## Runtime note

`mcp.json` is included for profile distribution/versioning. Hermes v0.13.0 runtime still reads MCP server config from `config.yaml` / `mcp_servers` unless patched to merge profile-local `mcp.json`.

Hermes runtime hot-memory loading uses `HERMES_HOME/memories/{USER.md,MEMORY.md}`. Root-level `USER.md`/`MEMORY.md` may exist in a live profile for compatibility, but this distribution treats `memories/` as the source of truth.

## Source copied from

`/home/galyarder/.hermes/profiles/niyatna`
