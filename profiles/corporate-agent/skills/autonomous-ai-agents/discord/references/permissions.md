# Discord Permissions & Routing Guards

# Discord bot-to-bot routing session note

## Scenario

A Discord channel contains two Hermes-backed agents/bots. The user asked whether the `allowed` ID list, which currently contains only the user's Discord ID, should also include the Discord application IDs for the Co-Founder and Default bots so the agents can see each other's messages.

## Finding

Hermes Discord routing has a distinct bot-message filter. In `gateway/platforms/discord.py`, messages from bot authors are controlled by `DISCORD_ALLOW_BOTS` before the normal human allowlist path. The modes are:

- `none`: ignore all other bots;
- `mentions`: accept bot messages only when they mention this bot;
- `all`: accept all bot-authored messages that reach the adapter.

The regression tests around `tests/gateway/test_discord_bot_auth_bypass.py` verify that permitted Discord bot messages bypass the human allowlist, while humans remain checked against the allowlist.

## Recommended answer

Do not add other bot application IDs to `DISCORD_ALLOWED_USERS` as the main solution. Keep the human allowlist human-only and set:

```env
DISCORD_ALLOW_BOTS=mentions
```

For a safe multi-agent Discord channel, pair it with:

```env
DISCORD_REQUIRE_MENTION=true
DISCORD_IGNORE_NO_MENTION=true
```

Then each bot must explicitly mention the other bot when handing off or asking it to respond.

## Pitfalls

- `DISCORD_ALLOW_BOTS=all` can create bot-to-bot loops in free-response/shared channels.
- App/client IDs can be confused with Discord user/message author IDs.
- Changing env/config usually requires restarting the gateway/profile process.
- Shared channel visibility is still filtered per bot; it is not automatic shared memory.

## Enable Scopes & Toolsets

# Discord Toolset Enable Scope — 2026-05-17

## Session signal

Owner asked why the Hermes dashboard showed **Discord (read/participate)** as inactive. Live config showed the Discord gateway was active and token/env existed, but `platform_toolsets.discord` lacked native Discord toolsets.

The correction: when Owner says to **turn on / enable** Discord toolsets, do exactly that config action first. Do **not** bundle a gateway/service restart unless he explicitly asks for restart or the task is specifically to verify live runtime reload.

## Distinction

- Discord gateway active = bot can receive/reply to routed Discord messages.
- Discord toolset active = agent can call Discord REST tools, e.g. fetch messages, search members, create threads, and, with admin toolset, server/admin operations.

Dashboard label:

```text
Discord (read/participate)
Inactive
Fetch messages, search members, create thread
```

means the native `discord` toolset is not enabled for the current platform/profile, not necessarily that the Discord gateway is down.

## Minimal enable action

For Default Discord platform:

```bash
HOME=~/.hermes hermes -p default tools enable --platform discord discord discord_admin
```

Verification without restarting services:

```bash
python - <<'PY'
from pathlib import Path
import yaml
p = Path('~/.hermes/profiles/default/config.yaml')
conf = yaml.safe_load(p.read_text()) or {}
items = (conf.get('platform_toolsets') or {}).get('discord') or []
print('has_discord=' + str('discord' in items))
print('has_discord_admin=' + str('discord_admin' in items))
print(items)
PY
```

Expected result:

```text
has_discord=True
has_discord_admin=True
```

## Restart boundary

Restarting `hermes-gateway-default.service` can be correct when the user asks for live runtime reload, smoke testing, or immediate tool availability in a running gateway session. But it is **not part of the minimal enable step**.

Do not append this automatically to a plain enable request:

```bash
systemctl --user restart hermes-gateway-default.service
```

If restart seems necessary, state it as a separate follow-up and ask or wait for explicit permission unless the user already requested restart/live reload.

## Style lesson

For irritated or terse operator commands, reduce explanation and execute the literal requested scope. Report only what changed and what was intentionally not touched.