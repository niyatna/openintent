# Discord Raw Mentions & Formatting

# Discord controlled relay protocol

## Session signal

In a live Discord thread, Keiya mentioned the Galyarder bot using a raw mention object and Galyarder replied. The user and both agents then aligned on a safety pattern: Discord should be a controlled relay surface, not an autonomous agent chat room.

Observed local mentions in this session:

- Keiya Putri: `<@1502245129153679390>`
- Galyarder: `<@1499427878708842637>`

These IDs are environment-specific. Re-verify them before using on another server/profile.

## Raw mention lesson

Plain text such as `@Galyarder` or `@Keiya Putri` may not become a real Discord mention when emitted by an agent. Deterministic handoff should use a raw mention object:

```text
<@BOT_USER_ID>
```

If the bot user ID is not in hot memory:

1. Search durable memory/Hindsight first.
2. Prefer Discord Developer Mode or Discord API `/users/@me` for the active bot token.
3. If local token inspection is the only path, the first token segment can often be base64url-decoded into the bot user ID candidate. Never print or store the token; print only the decoded ID/mention candidate.
4. Treat decoded IDs as candidates until verified by a live mention-response test.

## Controlled relay rules

Use this pattern for Keiya ↔ Galyarder or other Hermes-backed agents in Discord:

1. Human invokes or explicitly authorizes the handoff.
2. One purpose per handoff.
3. Use a short packet: context → question → constraint → requested output.
4. The target agent gives one reply only.
5. No autonomous ping-pong or agent-to-agent free chat.
6. Results return to the same thread/channel for the human to review; no hidden side-channel.
7. For important decisions, Keiya reads human state, Galyarder reduces to constraints/options/next move, and Galih remains final decision-maker.

## One-hop handoff rule

The stable local pattern is one-hop handoff:

1. The human tells Agent A to consult Agent B.
2. Agent A sends a message that explicitly mentions Agent B **exactly once at the start of that message**. Do not repeat the raw mention in body paragraphs, sub-headers, or mid-message — the mention is a routing header, not a bullet marker.
3. Agent B answers once and includes Agent A raw mention (once, at the start) so Agent A can read the answer. If Discord splits the answer, Hermes repeats that mention onto each continuation chunk (once per chunk).
4. Agent A summarizes the answer to the human without mentioning Agent B again.

This prevents loops because ordinary human-facing summaries contain no bot mention, and gateway filtering only accepts bot-authored messages that explicitly mention the receiving bot. For long bot-to-bot answers, Hermes repeats the first raw mention onto split chunks so the receiving bot can aggregate the full answer without accepting unrelated bot chatter. A second agent-to-agent round requires a fresh explicit human request or a fresh explicit bot mention.

## Verification pattern

A minimal safe test:

```text
<@TARGET_BOT_ID> hei, test controlled relay. jawab satu kali saja kalau kebaca.
```

Expected result: exactly one response from the target bot, no follow-up loop.

## Pitfalls

- Accepting all bot messages (`DISCORD_ALLOW_BOTS=all`) in a shared channel can turn a handoff into a loop.
- Letting agents continue discussion after the requested output violates controlled relay.
- Mentioning by display name can look correct to humans while failing as a Discord mention object.
- Hidden side-channel summaries make Galih lose command authority; return outputs to the visible thread unless explicitly asked otherwise.
- Summarizing back to the human while mentioning the peer bot again can re-trigger the peer and restart a ping-pong loop.
- If the requester mention is buried after too much text, the first chunk may be mostly preface; keep bot-to-bot prompts compact and use the raw mention early.
- Repeating the raw mention multiple times within the same message/chunk turns a routing header into notification spam. One mention per chunk is sufficient; the mention is a packet header, not a paragraph marker.

## Mention Sanitization Pitfalls

# Discord relay mention sanitization / duplicate-send pitfall — 2026-05-30

## Context

During a Keiya → Galyarder credential-migration relay, Galyarder sent a completion packet through `send_message` with what should have been Keiya's raw mention. The visible tool output showed the mention masked as `<@***>`, and a corrected resend was skipped by the Discord relay duplicate guard for the same trigger.

## Lesson

For bot-to-bot Discord relays, a successful `send_message` call is not always proof that the peer bot was deterministically pinged. Raw mentions can be masked/sanitized in tool output, and duplicate-relay prevention can block an immediate corrected resend.

## Procedure

1. Keep bot-to-bot relay packets short so they do not split.
2. Put the raw mention exactly once at the very start of the message.
3. If the tool output or mirrored message shows the mention as masked/sanitized, do **not** claim deterministic peer delivery.
4. If a corrected resend is skipped as a duplicate, report the caveat plainly and continue with verified local evidence.
5. For high-stakes peer handoffs, verify visible Discord message state if tools allow; otherwise say `sent, routing caveat: mention visibility unverified`.

## What not to do

- Do not pretend a peer was pinged if the visible packet lost the raw mention.
- Do not spam duplicate resends around the duplicate guard.
- Do not treat peer bot silence as task failure if the human-visible status was already posted and local verification proves the side effect.