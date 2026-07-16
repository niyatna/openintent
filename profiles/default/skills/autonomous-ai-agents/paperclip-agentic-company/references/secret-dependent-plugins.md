# Secret-dependent Paperclip plugins

Use this when installing/configuring Paperclip plugins that need bot/API tokens (Discord, Telegram, GitHub Issues, Slack, Hindsight-like integrations, etc.).

## Principle

Never persist raw tokens in `plugin_config.config_json`, plugin logs, notes, chat summaries, or Obsidian. Store tokens as Paperclip company secrets first, then configure plugin fields with secret references only if the current Paperclip host supports resolving them.

## Safe workflow

1. **Backup first**
   - Use Paperclip DB/config backup before editing plugin settings or DB rows.
   - If plugin config files exist under the instance data dir, copy them too.

2. **Extract secrets without printing**
   - If Owner pasted tokens in Discord/Telegram, read them through the platform API or current message context only long enough to create the Paperclip secret.
   - Do not echo them to stdout. Print only booleans, hashes/fingerprints, lengths, or secret keys.

3. **Create/update company secrets**
   - Use the Paperclip company secrets API/CLI for keys such as:
     - `paperclip_discord_bot_token`
     - `paperclip_telegram_bot_token`
     - `paperclip_board_api_token`
     - `default_github_pat` / plugin-specific GitHub token keys
   - Verify secret metadata exists via `/api/companies/{companyId}/secrets`; do not retrieve or print secret values.

4. **Configure routing safely**
   - Route all noisy notifications to one explicit test channel/chat first.
   - Disable digests/media/intelligence/proactive loops unless intentionally requested.
   - For Telegram/Discord inbound commands, restrict allowed chat/channel/user IDs where the plugin supports it.

5. **Try activation with secret refs**
   - Plugin fields marked as secret refs usually expect UUID-shaped secret IDs, not raw token strings and not `{type: "secret_ref"}` objects unless the plugin docs explicitly say otherwise.
   - In the current Paperclip build, plugin config upsert uses `POST /api/plugins/{pluginKey}/config` with `{ "configJson": { ... } }`; `PATCH`/`PUT` may 404 even though `GET /config` works.
   - For non-interactive CLI/API checks, set `HOME=~/.hermes`, `PAPERCLIP_AUTH_STORE=~/.hermes/.paperclip/auth.json`, and `PAPERCLIP_API_URL=http://127.0.0.1:3100` so `paperclipai` uses the actual board auth store.
   - If activation fails, read the exact error and plugin/host code path before changing config.

## Known host blocker: instance/company secret-ref mismatch

On Paperclip versions around `2026.513.0`, secret-dependent plugin activation can fail even after valid company secrets are created:

```text
Worker initialize failed ... Plugin secret references are disabled until company-scoped plugin config lands
```

or related secret errors such as:

```text
Invalid secret reference: [object Object]
Secret not found: <uuid>
```

Interpretation:

- `Invalid secret reference` usually means the persisted value is not a UUID-shaped ref (often a raw token or object was written where the host expects a string).
- `Secret not found` means lookup failed for the supplied UUID/ref.
- `Plugin secret references are disabled until company-scoped plugin config lands` is an upstream host capability gap, not a bad bot token.

Safe handling when this blocker appears:

1. Leave the token stored as a Paperclip secret.
2. Remove raw token strings from plugin config if they were ever written.
3. Set/keep the plugin disabled with `last_error=null` if possible, so the system is clean and not spam-looping.
4. Report: “secrets stored, plugin configured as far as safe, activation blocked by upstream Paperclip secret-ref support.”
5. Do not bypass by storing raw bot/API tokens in `plugin_config.config_json` just to make activation pass unless Owner explicitly authorizes activation-now over ideal secret hygiene.

## Owner-authorized local fallback

If Owner explicitly provides the bot tokens and says to turn the integration on now, do not stop at the safe-disabled state. Use the backed-up temporary plaintext fallback documented in `references/discord-telegram-plaintext-fallback-2026-05-19.md`:

- validate tokens live without printing values;
- patch/upsert config and plugin worker only enough to bypass the host secret-ref blocker;
- keep commands/inbound/digest/noisy features off unless requested;
- restart Paperclip if needed;
- verify `ready` + `lastError=null` for Discord and Telegram;
- sanitize logs if a previous attempt logged raw tokens.

Treat this as a local/private Paperclip workaround, not a general credential policy.

## Verification checklist

Before reporting status:

- `/api/health` returns `status=ok`.
- Secret metadata contains the expected keys; no raw values printed.
- `plugin_config.config_json` does not match obvious Discord/Telegram/GitHub token regexes.
- Plugin status and `last_error` are inspected fresh.
- Recent logs are checked for repeating plugin error spam.
- Temporary token/secret-ID files under `/tmp` are removed.

## Human-facing report pattern

```text
stored aman:
- Discord bot token -> Paperclip secret key X
- Telegram bot token -> Paperclip secret key Y

plugin status:
- Discord: disabled/active, last_error: ...
- Telegram: disabled/active, last_error: ...

catatan: aktivasi official plugin keblokir upstream secret-ref support; gua nggak naruh raw token di config.
```
