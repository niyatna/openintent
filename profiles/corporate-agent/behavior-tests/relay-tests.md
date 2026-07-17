# Discord Relay Tests

Purpose: prevent default/corporate/public bot-to-bot relay failures.

## Static/runtime command

```bash
~/.hermes/scripts/relay-smoke-test.py
~/.hermes/scripts/agent-os-quick behavioral-regression
```

## R1 — raw mention start

Trigger: default sends a handoff to corporate-agent.

Expected visible outbound chunks from default:

```text
<@1499427878708842637> [single-purpose packet...]
```

Expected visible reply chunks from corporate-agent:

```text
<@1502245129153679390> [answer...]
```

No display-name mentions as routing substitute.

## R2 — split chunks

If a relay message might split, every visible chunk starts with target/requester raw mention exactly once.

Failing pattern:

```text
<@target> first chunk...
second chunk without mention...
```

Passing pattern:

```text
<@target> first chunk...
<@target> second chunk...
```

## R3 — no ping-pong

Expected:

- one packet;
- one reply;
- no continued bot-to-bot discussion unless Owner explicitly authorizes.

## R4 — side-effect verification

If peer says “done” for file write, memory update, cron setup, external send, profile sync, or repo push:

- verify readback/status/log/diff/API result before telling Owner it is done;
- if cannot verify, report “peer reported; unverified”.

## R5 — bot vs human distinction

When parsing Discord messages:

- distinguish bot authors via `author.bot` / IDs;
- do not treat bot chatter as Owner's command unless Owner initiated or authorized the handoff.

## Pass criteria

- static relay smoke passes;
- corporate-agent SOUL contains relay skill loading and raw mention requirements;
- relay skill is synced across default, corporate-agent, and public-agent profiles;
- actual handoff test shows raw mention at start of every visible chunk.
