# Paperclip Discord plugin: slash commands vs mention chat — 2026-05-19

## Trigger

Use this reference when Paperclip Discord plugin is `ready` / Gateway is connected but Owner says mentioning the bot gets no response.

## Finding

`paperclip-plugin-discord` is not a Hermes-style free-form mention responder by default.

There are three separate surfaces:

1. **Notifications** — Paperclip posts issue/approval/error/escalation messages to the configured channel.
2. **Slash commands** — Discord interactions such as `/stable-diffusion-image-generation status`, `/stable-diffusion-image-generation agents`, `/stable-diffusion-image-generation issues`, `/stable-diffusion-image-generation help`, `/acp ...`. These require `enableCommands=true` and slash command registration after restart/reload.
3. **Inbound reply routing** — user replies to a Paperclip notification message that has stored mapping state. This requires `enableInbound=true`, but it only routes replies to mapped issue/escalation messages. It is not a free chat handler.

A plain message like `<@bot> yo` does not trigger a default reply unless a custom message/mention handler is added.

## Source-level mechanics (verified from `dist/` source)

- **Slash commands are registered at startup** whenever `defaultGuildId` is set, regardless of the `enableCommands` config value. `enableCommands` only gates the runtime interaction *handler* inside `handleInteraction()`. If you enable commands in config but they don't respond, restart Paperclip to re-register with Discord.
- **`gatewayNeedsMessages`** controls whether the Gateway opens with `GUILD_MESSAGES_INTENT | MESSAGE_CONTENT_INTENT`. It is `true` when **any** of: `enableInbound`, `enableMediaPipeline`, `enableCustomCommands`, `enableProactiveSuggestions`, or `enableIntelligence` is true. If all five are false, the Gateway connects with `GUILD_INTENT` only — it will handle `INTERACTION_CREATE` (slash commands, buttons) but will **not** receive `MESSAGE_CREATE` events at all. This means even reply routing won't fire if `enableInbound=false` and all other message-scanning features are off.
- **Inbound reply routing** (`handleMessageCreate`) ignores bot-authored messages (`message.author.bot`) and only processes messages with `message_reference.message_id` pointing to a previously mapped Paperclip notification. It is not a free chat handler.

## Safe initial interactive config

When Owner expects the bot to be usable from Discord but does not want chaos:

```json
{
  "enableCommands": true,
  "enableInbound": false,
  "digestMode": "off",
  "enableIntelligence": false,
  "enableMediaPipeline": false,
  "enableCustomCommands": false,
  "enableProactiveSuggestions": false
}
```

Then restart/reload Paperclip if required and verify logs include:

```text
Slash commands registered with Discord
Gateway WebSocket connected
Gateway ready
```

Verify plugin/API state:

```text
Paperclip health: ok
paperclip-plugin-discord: status=ready, lastError=null
enableCommands=true
enableInbound=false
```

## User-facing answer pattern

If Owner asks why mention got no response, be direct:

```text
karena plugin Paperclip Discord bukan mention bot. yang tadi masih notif-only.
sekarang command path udah gua nyalain: /stable-diffusion-image-generation status, /stable-diffusion-image-generation agents, /stable-diffusion-image-generation issues, /stable-diffusion-image-generation help.
mention bebas tetap gak akan dibales kecuali kita patch custom handler.
```

## If free-form mention response is required

That is a separate feature/patch, not default plugin behavior. Design it deliberately:

- gate by allowed Discord user/channel;
- avoid bot-to-bot loops;
- define whether mention creates Paperclip issue, asks a chosen Paperclip agent, or invokes Hermes;
- log/audit the resulting action;
- keep token redaction and secret-ref/plaintext fallback boundaries intact.
