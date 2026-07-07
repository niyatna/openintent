# Long install/provisioning progress reporting — 2026-05-24

## Trigger

During a cross-profile `computer-use-linux` install, a slow download/install path took long enough that Galih interrupted with "lama lu kampret." The issue was not just technical speed; it was lack of terse visible progress while commands were running.

## Reusable rule

When a setup/provisioning flow involves slow downloads, builds, package installs, MCP discovery, or multi-profile config edits:

1. If a command may exceed roughly 60–90 seconds and has a clear end, prefer background execution with completion notification.
2. If foreground is still best, send a terse progress/state update before continuing after the slow step.
3. When interrupted for slowness, immediately summarize verified state and continue the nearest safe action. Do not spend the next message on apology, meta-analysis, or a full log dump.
4. Final report should separate what is complete, what is partially ready, what is blocked, and the exact gate needed next.

## Good final shape

```text
status:
- installed: <artifact/path>
- verified: <fresh command/check>
- partial/blocker: <specific gate>
- next gate: <one action>
```

Keep it short in Discord. Full command transcripts belong in skill references or notes, not chat, unless Galih asks.
