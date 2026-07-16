# Discord/Telegram Paperclip plugin secret-ref blocker — 2026-05-19

## When this applies

Use for Paperclip Discord/Telegram plugin setup on authenticated local Paperclip where bot tokens have already been received and should be stored safely.

## Durable lesson

The safe target state is **secrets stored, raw token absent from plugin config, plugin disabled if host cannot resolve secret refs**. Do not “finish” activation by copying raw Discord/Telegram tokens into `plugin_config.config_json`.

## Observed state

- Paperclip health: `status=ok`, `deploymentMode=authenticated`, `bootstrapStatus=ready`.
- Installed plugins:
  - `local.github-issues`: `ready`
  - `paperclip-plugin-hindsight`: `ready`
  - `paperclip-plugin-discord`: installed but `disabled`
  - `paperclip-plugin-telegram`: installed but `disabled`
- Paperclip company secrets existed and were active for:
  - `paperclip_discord_bot_token`
  - `paperclip_telegram_bot_token`
  - `paperclip_board_api_token`
- Discord/Telegram plugin config had safe routing/default channel/chat values and no raw token regex match.

## API/CLI patterns that worked

Set these env/path controls when using Paperclip CLI non-interactively so it finds the real board auth store:

```bash
HOME=~/.hermes \
PAPERCLIP_AUTH_STORE=~/.hermes/.paperclip/auth.json \
PAPERCLIP_API_URL=http://127.0.0.1:3100 \
~/.hermes/.nvm/versions/node/v24.15.0/bin/paperclipai plugin list --json
```

Useful read endpoints with board bearer auth:

```text
GET /api/plugins/{pluginKey}
GET /api/plugins/{pluginKey}/config
GET /api/companies/{companyId}/secrets
```

Config write endpoint shape discovered in this session:

```text
POST /api/plugins/{pluginKey}/config
body: {"configJson": {...}}
```

`PATCH`/`PUT /api/plugins/{pluginKey}/config` returned `404`; `POST` is the supported upsert path in this build.

## Blocker behavior

Attempting to POST Discord/Telegram config with UUID secret refs in fields such as:

```text
discordBotTokenRef
paperclipBoardApiKeyRef
telegramBotTokenRef
paperclipBoardApiTokenRef
```

returned:

```text
422 {"error":"Plugin secret references are disabled until company-scoped plugin config lands"}
```

Interpretation: this is a Paperclip host capability gap, not invalid Discord/Telegram bot tokens.

## Safe verification checklist

Before reporting status:

1. Confirm health is ok.
2. Confirm secret metadata exists and is active; never print values.
3. Confirm plugin status/lastError fresh via `paperclipai plugin list --json` or `/api/plugins`.
4. Fetch `/api/plugins/{pluginKey}/config` and scan serialized config for obvious token regexes:
   - Discord-like: long three-part `a.b.c`
   - Telegram-like: `digits:long-token`
5. Check recent server log for repeating worker initialize failures / secret-ref errors.
6. If secret refs are blocked, keep Discord/Telegram disabled with clean `lastError=null` and report the upstream blocker tersely.

## Human-facing status pattern

```text
belum full active.

udah:
- token Discord/Telegram stored as Paperclip Secrets
- plugin installed
- raw token gak ada di config

blocked:
- aktivasi official plugin gagal karena Paperclip host belum support secret refs untuk instance plugin config:
  `Plugin secret references are disabled until company-scoped plugin config lands`

jadi status aman: secret stored, plugin disabled, nunggu upstream/company-scoped plugin config. gua gak bypass pake raw token.
```
