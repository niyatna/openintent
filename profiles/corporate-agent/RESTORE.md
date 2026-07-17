# corporate-agent Profile Restore

This repo restores corporate-agent's **profile code/personality/tooling layer** only.

It includes:
- `SOUL.md`
- `distribution.yaml`
- `mcp.json`
- `hooks/`
- `scripts/`
- full active `skills/`
- `behavior-tests/` static QA docs and access-rollout runbooks
- curated hot-memory files:
  - `memories/USER.md`
  - `memories/MEMORY.md`
- `.env.EXAMPLE`

It intentionally does **not** include private runtime state or the private credential registry at `~/.hermes/private/credentials/`:
- `.env`
- auth files and tokens (`auth.json`, `google_token.json`, `google_client_secret.json`, etc.)
- sessions/logs/cache
- runtime databases (`state.db*`, `response_store.db*`, `kanban.db*`)
- gateway/process state
- cron outputs/logs/cache
- raw Hindsight/DB/session archives
- private credential registry files unless explicitly encrypted/approved

The included `memories/USER.md` and `memories/MEMORY.md` are curated stable facts only, not raw archives. They restore the profile's hot memory baseline; full same-continuity restore still requires the private disaster-recovery archive.

For a true same-continuity restore, combine this repo with the local private disaster recovery archive under:

```text
~/.hermes/backups/disaster-recovery/
```

Latest known archive at creation time:

```text
hermes-private-state-20260515-203254.tar.zst
sha256: 92fe9d7b456b8ad953171e63d5b00f07aa0bbfdfae80688384d3448911a9fc00
```

Do not push the private archive to this repo unless it is encrypted and Owner explicitly approves.
## Operational agent-owned credentials

Dedicated agent-owned account credentials, cookies, TOTP secrets, backup codes, and wallet keystores are local-only runtime state under `~/.hermes/private/credentials/agents/`. They are intentionally excluded from this profile distribution. Restore from the private credential backup / password manager, never from git.
