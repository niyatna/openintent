# Discord agent-to-agent relay: raw mentions and verification (2026-06-17)

## Trigger

Galih asked Galyarder to mention Keiya, ask who Galih is for Keiya and Galyarder, and make sure Keiya mentioned Galyarder in her response.

## Durable lesson

For Discord agent-to-agent relay, display-name mentions like `@Keiya` / `@Galyarder` may post as plain text and may not wake the target bot. Use raw Discord mention IDs from verified recent messages or member lookup:

- Keiya: `<@1502245129153679390>`
- Galyarder: `<@1499427878708842637>`

After sending, verify by fetching recent messages from the channel and checking:

1. the relay message exists,
2. the target bot authored a new response after it,
3. the response contains the required raw mention if the user asked for cross-mention.

## Tool pattern

1. If the user names a specific channel/person, list targets first when practical.
2. If a `send_message` target copied from the long display list returns Discord `404 Unknown Channel`, do not keep retrying the same long display target. Use a stable target shape instead:
   - `discord:#general` for the general channel, or
   - `discord:<channel_id>` for a verified channel ID.
3. Prefer raw mentions in the message body:
   - `<@1502245129153679390>` for Keiya
   - `<@1499427878708842637>` for Galyarder
4. Verify via Discord message fetch before reporting completion.

## Pitfall

Do not treat `send_message(action=list)` display rows as guaranteed send targets when they include long guild/category/topic descriptions. Some rows are human-readable inventory, not stable send addresses. If Discord returns `Unknown Channel`, switch to a verified channel ID or simple channel target and continue.