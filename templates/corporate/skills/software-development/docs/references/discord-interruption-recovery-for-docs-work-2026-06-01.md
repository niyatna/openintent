# Discord interruption recovery for docs-site work (2026-06-01)

## Trigger
Use this when a docs/GitHub Pages/content-rewrite job is interrupted mid-run, the user complains that the agent is stuck, or a previous session only left a partial report.

## Problem pattern
A previous run reported `partial`, then the runtime reset or timed out while a terminal command was active. The next session showed only named sessions or resumed the wrong task, while the actual repo still had staged/generated changes.

## Recovery sequence
1. **Recover the real task from live chat/session context.** Do not ask the user to `/resume` or pick a named session when enough context is retrievable.
2. **Inspect the repo state before editing.** Run read-only git status/counts first: branch, remotes, HEAD, staged count, unstaged count, untracked count, and top path buckets.
3. **Create a real diff backup before cleanup.** When large staged changes exist, save both cached and unstaged binary diffs plus name-status snapshots before any restore/cleanup. Disable pager/delta if scripting diff output (`GIT_EXTERNAL_DIFF=` and `git --no-pager`) so captured files are plain patch text.
4. **Unstage and scope cleanup before staging.** If thousands of files are staged, unstage all, restore obvious runtime/noise paths, then stage only the intended docs/public-positioning surface.
5. **Separate generated docs from canonical source.** For MkDocs sites, generated public detail pages under `docs/agents`, `docs/skills`, `docs/commands`, or `docs/design` may be intentional generated output. Canonical runtime source under root `agents/`, `skills/`, `commands/`, `integrations/`, and `personas/` should not be bulk-mutated solely for public copy cleanup.
6. **Watch for generator bugs caused by rushed regex rewrites.** A replacement like `r'(\1)'` must remain a backreference; if it becomes an actual control character (`\x01`) in source, generated links silently corrupt. Verify generator snippets with `repr()` and compile/run the generator before trusting output.
7. **Treat recursive delete/restore prompts as approval gates.** If Hermes blocks `rm -rf`, `git restore` over many paths, or similar cleanup, report the exact gate and wait; do not bypass with an equivalent destructive command.
8. **Resume execution after approval.** Once approved, continue verification, staging, commit/push, workflow wait, and live Pages verification. Do not stop after saying `partial` if the next step is executable.

## Terse Discord report shape
When Galih interrupts with “ngestuck lagi?” or asks status in the middle:

```text
belum selesai / partial — state dulu.
- repo/state evidence: <1-2 bullets>
- what got fixed/recovered: <1-2 bullets>
- current gate: <exact approval/blocker>
- next move after approval: <verify -> stage -> commit/push -> live check>
```

No apology speech, no long process dump, no vague “I will continue.” Say the state, name evidence, and execute the next safe step if tools allow.
