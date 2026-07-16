# Discord Agent-to-Agent Relay Protocols

# Reference: discord-agent2agent-relay

# Discord Agent2Agent Relay

## Overview

Use this skill when multiple Hermes agents share a Discord server or thread and need to communicate through visible Discord messages.

The safe pattern is a controlled relay: a human asks one agent to contact another agent, the first agent explicitly mentions the target agent, the target replies back to the requesting agent, and the requesting agent summarizes to the human. Agents should not freely respond to every bot message in a shared channel.

**Origin-first routing rule:** when the human asks for an agent2agent mention from inside a Discord channel/thread, Agent A's handoff to Agent B is the next visible reply in that same origin conversation with Agent B's raw mention at the start. Do not use `send_message`, do not manually pick a channel, and do not fall back to `#general`. The gateway/platform delivery layer already posts the final answer back to the origin. Use `send_message` only when the human explicitly asks to send somewhere else, or when the current task did not originate from Discord and a destination must be selected.

This skill assumes the Discord gateway is configured so bot messages are admitted only when they explicitly mention the receiving bot, for example with `DISCORD_ALLOW_BOTS=mentions`.

## Core Rule

Only treat a bot-authored Discord message as agent2agent input when the message contains your explicit raw bot mention, such as `<@1234567890>` or `<@!1234567890>`.

Do not treat reply pings, thread context, channel presence, or a bot message merely appearing nearby as permission to respond.

## Relay Protocol

### Human to Agent A

The human starts the workflow by mentioning Agent A and asking it to contact Agent B.

Example:

```text
@AgentA ask @AgentB for their take on this plan, then summarize it back to me.
```

Agent A should:

- decide whether Agent B actually needs to be contacted
- send a clear handoff to Agent B using Agent B's raw mention
- tell Agent B whether it should reply back to Agent A
- wait for Agent B's answer before summarizing to the human

### Agent A to Agent B

Every visible handoff message to Agent B must include Agent B's raw mention.

Good:

```text
<@AGENT_B_ID>
The human asked for your perspective on this plan. Please answer with your view and mention <@AGENT_A_ID> so I can summarize it back to them.
```

Bad:

```text
The human asked for your perspective on this plan. What do you think?
```

The bad version may be ignored by Agent B because it lacks an explicit target mention.

### Agent B to Agent A

If Agent B wants Agent A to read the answer, Agent B must mention Agent A explicitly.

Good:

```text
<@AGENT_A_ID>
My view: the plan is workable, but the risk is unclear ownership. I would tighten the next action and success metric.
```

Bad:

```text
My view: the plan is workable, but the risk is unclear ownership.
```

The bad version may be visible in Discord but should not start Agent A unless Agent A is explicitly mentioned.

### Agent A to Human

When Agent A summarizes back to the human, Agent A should not mention Agent B again unless the human explicitly asks for another round.

Good:

```text
Here is the summary from Agent B: the plan is workable, but ownership and the success metric need to be sharper.
```

Bad:

```text
@AgentB summary for the human: ...
```

The bad version may start a new relay cycle.

## Long Messages

Discord may split long outputs. When a handoff to another agent spans multiple visible messages, every message must repeat the target agent's raw mention.

Good:

```text
<@AGENT_B_ID>
Part 1/2: context...
```

```text
<@AGENT_B_ID>
Part 2/2: more context...
```

Bad:

```text
<@AGENT_B_ID>
Part 1/2: context...
```

```text
Part 2/2: more context...
```

The bad version can cause Agent B to receive only the first part.

## Streaming Outputs

When composing a streamed handoff, put the target mention as early as possible. If the message starts with a preface and later turns into a handoff, the handoff portion must still include the target mention.

Good:

```text
<@AGENT_B_ID>
I need your review on this specific question: ...
```

Acceptable:

```text
I will ask Agent B.

<@AGENT_B_ID>
Please review this specific question: ...
```

Avoid streaming long handoffs where only an early chunk contains the target mention.

## Loop Prevention

- Do not reply to a bot unless it explicitly mentions you.
- Do not mention the peer agent in the final human-facing summary unless another relay round is intended.
- Do not keep asking open-ended follow-ups between agents without human instruction.
- Do not rely on Discord reply metadata as a relay signal.
- Prefer one request, one answer, one summary unless the human explicitly authorizes iterative relay/tektok.
- If the human says `minimal N`, treat N as a lower bound, not a cap. Continue beyond N until the direction is mature or the human stops it; never convert the minimum into a hard maximum.
- Iterative relay still stays sequential: send one packet, wait for the peer's explicit raw-mention reply or human-quoted relay answer, then send the next packet. Do not batch future rounds.
- When a user quotes or forwards the peer agent's reply in the current chat, treat that as the peer response for sequencing purposes and continue the next round if the task remains open.
- Do not paste a relay packet as a normal human-facing summary. If the human asked to mention another agent in the current Discord conversation, the relay packet itself should be the origin reply with the target raw mention at the start. Only use `send_message` after explicit instruction to send somewhere else; never resolve a different concrete Discord target as fallback for an origin-thread mention.

## Configuration Hints

For Hermes Discord gateways that support these options, this protocol works best with:

```env
DISCORD_REQUIRE_MENTION=true
DISCORD_IGNORE_NO_MENTION=true
DISCORD_ALLOW_BOTS=mentions
DISCORD_ALLOW_MENTION_REPLIED_USER=false
DISCORD_REPEAT_MENTIONS_ON_SPLIT=true
HERMES_DISCORD_BOT_TEXT_BATCH_DELAY_SECONDS=2.5
```

Use direct bot user mentions for relay routing. Role mentions may notify humans or groups, but they are not a reliable substitute for a receiving bot's raw user mention unless the gateway explicitly supports role-based bot admission.

## Session references

- `references/iterative-relay-minimum-rounds-2026-05-17.md` — Owner correction: `minimal N` is a lower bound, not a cap; iterative tektok must be sequential but continue until mature/approved.

## Quick Template

Agent A handoff to Agent B:

```text
<@AGENT_B_ID>
The human asked me to get your perspective on: [question].

Please answer with your concise view and mention <@AGENT_A_ID> so I can summarize it back to the human.
```

Agent B reply to Agent A:

```text
<@AGENT_A_ID>
My answer: [answer].

Key point for the human: [summary-ready takeaway].
```

Agent A summary to human:

```text
Here is the summary from the other agent: [summary].
```

## Iterative Handoff & Round Limits

# Iterative relay: minimum rounds are not a cap

Session lesson from a Default ↔ Co-Founder social-launch tektok.

## Correction

When Owner says something like `tektokan minimal 10 kali`, the number is a **lower bound**, not a fixed script length. Do not stop because the counter reached 10. Continue until the direction is mature, the user stops it, or the task reaches a natural approval/render/review gate.

## Correct pattern

1. Send exactly one packet to the peer agent with the peer raw mention at the start.
2. Ask the peer to answer with your raw mention at the start.
3. Wait for the peer reply.
4. If Owner quotes/forwards the peer reply into the current chat, treat that as the peer reply for sequencing and proceed.
5. Process the answer, update the working spec, then send the next packet.
6. Continue beyond the minimum count when the work is not mature.

## Failure modes from the session

- Sending multiple future rounds before the peer replies. That is batching, not tektok.
- Treating `minimal 10` as exactly 10.
- Waiting unnecessarily when Owner already forwarded Co-Founder's reply in the chat.
- Writing the next relay packet in the human-facing final answer instead of actually sending it through Discord.

## Practical operating rule

For creative relay, keep a live spec and a round counter, but the counter is only progress tracking. The actual stop condition is quality/approval, not the round number.

## Local Reply Pitfalls

# Relay message vs local reply pitfall — 2026-05-17

Session lesson from a failed Co-Founder ↔ Default relay during social first-post content-generator.

## Failure

The user asked Default to tektok/discuss with Co-Founder and mention her. The first attempt used `send_message` with an unresolved target, then the assistant accidentally emitted the intended Co-Founder relay packet as the visible final response to Owner instead of sending it to a resolvable Discord target.

User correction: `kamu ga nyambung oi ditanya apa bales apa`.

## Rule

When the human asks to consult/mention another Discord agent:

1. Load this skill.
2. Resolve target with `send_message(action='list')` if the exact channel/target is not already known.
3. Actually call `send_message(action='send', target=resolved_target, message=packet)`.
4. Do **not** put the relay packet in the final answer as if it were sent.
5. After the peer replies, summarize the peer's answer to the human and continue the requested work.

## Safe fallback

If the first target fails with `Unknown Channel`, do not guess silently. **Never fall back to `#general` or another broad channel when the human initiated the request from a specific channel/thread.** The default target is the current/origin conversation (`di sini`), not a convenient resolvable channel.

If a tool cannot resolve the origin thread/channel, post the raw-mention relay packet as the visible reply in the current conversation so it lands exactly where the human is talking. Only choose another explicit Co-Founder target when the human asked to route there or the origin is unavailable and the user accepts the reroute. If all sends fail, report the routing block in one line and continue with local draft work clearly labeled as not peer-reviewed.

## Social-content tektok shape

For creative persona social posts, a valid peer packet should ask for:

- critique of the current angle;
- alternate caption candidates;
- visual direction;
- explicit reminder: no publish until Owner approves;
- raw mention back to Default at start of reply.