# Discord/Telegram plugin activation fallback — 2026-05-19

Use this only for Owner's local/private Paperclip instance when he explicitly provides bot tokens and says to turn the integration on.

## Trigger

- Paperclip Discord/Telegram plugins are installed.
- Token validation succeeds against the provider API.
- Safe secret-ref configuration fails with `Plugin secret references are disabled until company-scoped plugin config lands`.
- Owner explicitly wants activation now rather than a clean disabled state.

## Operator lesson

Do not over-preserve secret hygiene at the cost of disobeying a clear activation command. The default route is still secret refs, but when owner intent is explicit, move to a backed-up, temporary plaintext fallback and verify the actual plugin state.

## Safe sequence

1. Create a fresh Paperclip DB backup before changing plugin config or worker files.
2. Validate tokens without printing them:
   - Discord: `GET https://discord.com/api/v10/users/@me` with `Authorization: Bot <token>` and a normal `User-Agent`.
   - Telegram: `GET https://api.telegram.org/bot<TOKEN>/getMe`.
3. Try secret refs first through the supported config upsert route:
   - `POST /api/plugins/{pluginKey}/config` with `{ "configJson": { ... } }`.
   - `PATCH`/`PUT` may 404 in this Paperclip build.
4. If secret refs fail with the known host blocker and Owner has authorized activation, use a temporary plaintext config fallback.
5. Patch plugin workers only enough to bypass `ctx.secrets.resolve(...)` when the config field contains the usable token directly:
   - Discord worker: use `config.discordBotTokenRef` directly as `token`, and `config.paperclipBoardApiKeyRef || ""` directly as board API key.
   - Telegram worker: use `config.telegramBotTokenRef` directly as `token`; `resolveBoardApiToken` should return the candidate ref directly for this fallback path.
6. Prevent token leakage before restart:
   - Remove or replace config logging such as `Discord plugin config: ${JSON.stringify(rawConfig)}` with a non-sensitive message.
7. Set noisy features off unless Owner explicitly wants commands/inbound/digest:
   - `enableCommands=false`
   - `enableInbound=false`
   - `digestMode="off"`
   - Discord intelligence/media/custom/proactive features off.
8. Restart `openintent-paperclip` container via `docker compose restart paperclip-hq` only when loading patched worker/runtime config requires it.
9. Verify fresh:
   - `/api/health` is `status=ok`.
   - `paperclip-plugin-discord` and `paperclip-plugin-telegram` are `ready` with `lastError=null`.
   - existing core plugins such as GitHub Issues and Hindsight remain `ready`.
   - config can be read back from `/api/plugins/{pluginKey}/config` with all token/secret fields redacted before display.
   - recent logs do not contain raw Discord/Telegram token regex matches.
10. If the Paperclip CLI says `Board access required` while MCP/API board auth works, treat it as an auth-store/HOME mismatch first, not a plugin failure. Reuse the canonical auth store path or explicit board-auth environment and keep going.
11. If tokens were ever logged during experimentation, redact the runtime log immediately and keep/label the pre-sanitize backup carefully.

## Important boundaries

- Never paste raw tokens into chat, Obsidian, skills, memory, or reports.
- Do not encode the actual token values in this reference.
- This is a temporary workaround for a specific Paperclip host limitation, not a general recommendation to store plaintext credentials.
- Prefer replacing this with first-class company-scoped plugin secret refs as soon as Paperclip supports them.

## Human-facing status wording

Keep it terse when Owner is frustrated:

```text
kelar.
Paperclip health ok.
Discord plugin ready, lastError null.
Telegram plugin ready, lastError null.
GitHub Issues + Hindsight tetap ready.
catatan: secret-ref host masih blocker, jadi ini temporary plaintext fallback + worker patch; log token udah redacted.
```
