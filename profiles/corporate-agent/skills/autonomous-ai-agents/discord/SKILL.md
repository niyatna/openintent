---
author: Company
description: Use when configuring or troubleshooting Hermes Discord gateway routing, bot relay protocols, raw mentions, or allowed-user permissions.
license: MIT
metadata:
  hermes:
    category: autonomous-ai-agents
    tags:
    - hermes
    - discord
    - gateway
    - multi-agent
    - bot-routing
    - allowed-users
name: discord
version: 1.0.0
---

# Discord Gateway & Multi-Agent Relay

## Overview

Use this for Hermes Agent Discord gateway behavior: who is authorized, when the bot responds in a server channel, and how multiple Discord bots/agents can talk without creating loops.

Core principle: **human authorization and bot-message acceptance are separate gates.** Do not solve bot-to-bot visibility by treating other bots as human users.

## When to Use

Load this when:

- multiple Hermes-backed Discord bots/agents share one server channel;
- one bot cannot “see” or respond to another bot’s message;
- a user asks whether bot app IDs should be added to an allowed-user list;
- Discord mention behavior is confusing in shared channels;
- free-response channels, auto-threading, or multi-agent loops are involved;
- troubleshooting “bot ignores message” on Discord.

## Core Decision Table

| Situation | Setting pattern | Reason |
|---|---|---|
| One trusted human controls the agent | allow only that human in the human allowlist | Keeps tool access locked to the operator |
| Other bots should be heard only when they call this bot | set bot acceptance to `mentions` | Enables bot-to-bot handoff without accepting all bot chatter |
| Other bots should never trigger this bot | set bot acceptance to `none` | Safest default |
| All bot messages should be accepted | set bot acceptance to `all` only in isolated channels | High loop risk |
| Multiple bots share a public channel | require explicit mentions | Prevents agents from jumping into each other’s conversations |

## Recommended Multi-Agent Discord Pattern

For a channel where Co-Founder, Default, or other Hermes agents need to call each other:

```env
DISCORD_ALLOWED_USERS=<trusted-human-user-id>
DISCORD_ALLOW_BOTS=mentions
DISCORD_REQUIRE_MENTION=true
DISCORD_IGNORE_NO_MENTION=true
DISCORD_REPEAT_MENTIONS_ON_SPLIT=true
```

Meaning:

1. the trusted human remains authorized;
2. bot-authored messages are accepted only when they mention this bot;
3. general server chatter is ignored unless directed at this bot;
4. a message mentioning another bot but not this bot is ignored.

### Controlled relay protocol

In multi-agent Discord spaces, treat bot-to-bot communication as a **controlled relay**, not an agent chat room:

1. Human invokes or explicitly authorizes the handoff.
2. One purpose per handoff.
3. Use a short packet: `context → question → constraint → requested output`.
4. The target agent gives one reply only.
5. No autonomous ping-pong or agent-to-agent free chat.
6. Results return to the same thread/channel for the human to review.
7. For important decisions, Co-Founder reads human state, Default reduces to constraints/options/next move, and Owner remains final decision-maker.

Use raw Discord mention objects such as `<@BOT_USER_ID>` for deterministic bot pings; display-name text like `@Default` may not resolve from gateway-authored messages. See `references/discord-controlled-relay-protocol.md` for session details and verification pattern.

### Agent-facing relay behavior

When the user asks you to consult another Discord agent from a Discord thread/channel, **the origin conversation is the route**. If the human says “mention Co-Founder/Default” while already chatting in a channel/thread, do not use `send_message` or manually pick a different target. Reply in the current/origin conversation with the raw bot mention at the start; the gateway/platform delivery layer will post the final response back to the same place. Use `send_message` only when the human explicitly asks to send/relay somewhere else, or when you are outside a Discord-origin turn and must choose a destination.

1. Mention the target bot explicitly with its raw Discord mention (`<@BOT_USER_ID>`) **exactly once per outbound Discord message/chunk**, ideally at the very start of the origin reply.
2. Do **not** repeat the same target raw mention in every paragraph, section header, bullet, or body sentence within the same chunk. Treat the mention as a routing header, not punctuation.
3. Tell the target exactly what to answer and explicitly ask it to mention you back at the very start of its answer so your gateway accepts the answer.
4. Ask for one reply only unless the human explicitly requested a multi-step exchange; long replies may split, and Hermes repeats/injects the first raw mention across split continuation chunks. Each continuation chunk should contain the target mention once at the start, not repeatedly in the body.
5. If the target claims persistent side effects (file writes, memory updates, config changes, cron jobs, external sends, or profile sync), do **not** treat the bot reply alone as proof. Use available read-only tools to verify: check files, run verifier/tests, inspect status/logs, or compare expected artifacts. If verification is unavailable, label the result as "target reported" instead of "verified done".
6. After any needed verification, summarize the result back to the human without mentioning the target bot again.
7. Do not continue the agent-to-agent thread unless the human asks for another handoff.

### Iterative creative relay

If the human explicitly asks for `tektok`, `diskusi`, or iterative drafting with another agent, bounded multi-round relay is allowed. Keep each round scoped:

1. summarize the latest human correction in one packet;
2. ask the peer for specific alternatives or critique;
3. return the result to the human before continuing;
4. do not publish/send external output until the human explicitly approves the final wording.

This is still controlled relay, not autonomous agent chatter.

When another bot mentions you for a handoff:

1. Answer the requested question once.
2. Include the requester bot raw mention, preferably at the start. Hermes repeats the first raw mention onto split continuation chunks.
3. Do not mention unrelated bots or roles.
4. Do not keep asking follow-up questions to the requester unless the human explicitly authorized a follow-up loop.

Safe packet example:

```text
<@TARGET_BOT_ID> konteks: Owner minta satu sudut pandang dari kamu.
pertanyaan: apa hal penting yang perlu aku sampaikan balik ke Owner?
constraint: jawab sekali saja. mention aku balik dengan raw mention; kalau jawaban kepanjangan dan ke-split, Hermes akan repeat mention itu ke tiap chunk.
output diminta: 3 bullet singkat, tanpa ngajak agent lain.
```

Human-facing summary after the target replies should not contain the target bot mention unless Owner explicitly asks you to ping it again.

## Troubleshooting Workflow

1. **Identify sender type.** Is the incoming message from a human user or another Discord bot?
2. **Check the correct gate.**
   - Human sender: inspect the human allowlist / role allowlist.
   - Bot sender: inspect bot-message acceptance (`none`, `mentions`, or `all`).
3. **Check mention routing.** In server channels, require or expect direct `@mention` unless the channel is deliberately configured for free response.
4. **Check channel controls.** Allowed/ignored/free-response/no-thread channel settings can override what looks like a normal mention issue.
5. **Check the same profile's platform toolsets.** For Discord-side inspection or admin actions, the gateway profile needs the relevant Discord toolsets exposed on the `discord` platform (for example `discord`, and only when explicitly needed `discord_admin`). Env gates can be correct while platform toolsets still hide Discord-native tools.
6. **Restart the running gateway/profile after config changes.** Runtime processes do not necessarily reread environment values live.
7. **Verify with a directed test.** Bot A posts a message that explicitly mentions Bot B. Bot B should respond when bot acceptance is `mentions`.

## Source-Level Anchors

When confirming behavior in the Hermes Agent repo:

- Discord adapter: `gateway/platforms/discord.py`
- Gateway authorization: ***
- Bot-auth regression tests: `tests/gateway/test_discord_bot_auth_bypass.py`
- Discord user guide: `website/docs/user-guide/messaging/discord.md`

These anchors are useful because Discord routing is split between adapter-side filtering and gateway-level authorization.

## Common Mistakes

### Adding bot app IDs to the human allowlist

This usually does not fix bot-to-bot routing. Hermes has a separate bot-message gate; if bot acceptance is `none`, messages from other bots are ignored before the human allowlist matters.

### Confusing app/client ID with Discord user ID

If an ID is needed, copy the bot/user ID from Discord Developer Mode in the server context. Do not assume the application/client ID is the same thing the message author exposes.

### Setting bot acceptance to `all` in a shared channel

This can create bot loops: Bot A responds to Bot B, Bot B responds to Bot A, and the channel floods. Prefer `mentions` unless the channel is tightly isolated.

### Treating a shared Discord thread as an agent chat room

Even when raw mentions work, do not let agents freely discuss or continue pinging each other. Keep the human in control with a single-purpose relay packet, one target reply, and a visible return to the thread.

### Turning relay grounding into visible skill/tool theatre

For a simple human-authorized agent-to-agent relay (for example `mention Co-Founder, saling sapa`), skill loading is internal routing discipline, not the visible deliverable. Do not answer Owner with raw relay packets, tool logs, or a lecture about which skill was loaded unless he explicitly asks for an audit trail. Execute the controlled relay once, then report tersely: sent / blocked / peer replied.

### Forgetting profile-specific runtime state

Hermes can run profiles with separate config/environment. Always check the same profile that owns the Discord gateway process.

### Channel skill config key mismatch

When troubleshooting Discord auto-loaded skills, verify the live adapter actually receives the configured key. Some configs use the legacy dict form `discord.channel_skills`, while the gateway resolver historically looked only for list-form `channel_skill_bindings`. Check `gateway.config.load_gateway_config()` output for `config.platforms[Platform.DISCORD].extra`, then test `resolve_channel_skills(extra, channel_id, parent_id)`. If `channel_skills` is present in `config.yaml` but missing from `extra`, bridge it in `gateway/config.py`; if it reaches `extra` but resolves to `None`, patch `gateway/platforms/base.py` to support the dict alias and parent-thread fallback. Also check `gateway/run.py` auto-skill injection: channel bindings are injected only on new sessions, so if SOUL requires a profile core bundle every fresh gateway session, the runner must prepend the active profile's core bundle (`/co-founder-core` or `/default-core`) and treat bundle names as bundles, not ordinary skills. `skill_view('co-founder-core')` / `skill_view('default-core')` is expected to fail because they are bundles, not skills; use `/co-founder-core`, `/default-core`, or `agent.skill_bundles.build_bundle_invocation_message()`.

See `references/discord-channel-skills-bundles-pr-2026-06-11.md` for the upstream PR pattern, tests, and pitfalls from the 2026-06-11 fix.

### Local patch must become upstream PR

If the fix is in Hermes source code, do not leave it as a local-only patch. Local patches are update hazards: `hermes update`, `git pull`, rebase, or reinstall can drop them or create hidden divergence. Before declaring the runtime fixed, create an upstream-ready branch from `upstream/main`, isolate only the intended diff, add regression tests, push to the fork, and open a PR. Prefer a clean worktree for PR prep instead of committing from the live patched checkout.

Pitfalls:
- Do not copy whole files from a long-lived local checkout into a fresh worktree; it may drag unrelated local changes. Reapply minimal patches or inspect diff carefully.
- Use `--body-file` for `gh pr create/edit` when the PR body contains backticks or shell snippets; inline shell strings can execute command substitutions and corrupt the PR body.
- Run targeted tests after commit and after push if possible; report exact command + pass count.

### Discord speaker/register grounding

Do not infer the voice/register from the Discord server/channel label alone. Ground it from the active profile/speaker. Co-Founder/default uses Indonesian `aku-kamu` even when the channel is named Company or the topic is technical/runtime. Default/blade mode uses `lu-gua` with `gua` (never `gua`, wait, let me check the instruction: "Default/blade mode uses lu-gua with gua (never gue)"). If Co-Founder relays or quotes Default, lu-gua may appear only as quoted/relayed Default text, not Co-Founder's own voice.

### Assuming shared channel means shared context

Bots can read only messages delivered to their own gateway process and accepted by their filters. A shared Discord channel is not automatically shared agent memory.

### Assuming one raw mention covers all Discord split chunks

A raw mention at the start of chunk 1 does not guarantee later visible chunks reach the requester. If a relay answer may split, keep it short or deliberately structure each visible outbound chunk/message so it starts with the requester raw mention exactly once. Treat every visible Discord message as its own routed packet.

### Sending raw mentions through the wrong tool path

Some send/relay paths can sanitize or mask raw mention strings (for example turning `<@123...>` into `<@***>`) or skip a corrective resend as a duplicate for the same triggering message. When a bot-to-bot reply must route, prefer the native Discord/channel path that preserves raw mentions, and verify the actual sent message content when possible. If the mention was masked after a successful substantive status post, do not spam retries blindly; report the status to the human and name the routing caveat.

### Treating a peer bot's completion report as verified proof

A peer bot can report `DONE`, but the receiving agent should still verify persistent side effects with direct evidence before telling the human the work is complete. For example, after a profile sync, run the verifier from the target profile/root and check expected files/backups exist. If you cannot verify, say "reported done" and name what remains unverified.

## Reference

- `references/discord-bot-to-bot-routing.md` — original routing finding: human allowlist and bot-message acceptance are separate gates.
- `references/discord-controlled-relay-protocol.md` — live Co-Founder ↔ Default mention test, raw mention lesson, and controlled relay protocol.
- `references/discord-peer-side-effect-verification.md` — session-specific pattern for verifying a peer bot's claimed persistent changes before reporting completion.
- `references/discord-relay-mention-sanitization-pitfall-2026-05-30.md` — mention masking/duplicate-send pitfall: successful send is not always deterministic peer ping proof.
