# Hermes Hot Context: No Duplicate SOUL/USER/MEMORY Reads — 2026-06-13

## Session signal

Galih corrected a grounding workflow mistake: the hot identity/user/memory context is already present in normal turns, but the agent duplicated the same hot files with `search_files`/`read_file` before a trivial reply, creating noise and latency.

## Durable rule

For Keiya/default and Galyarder profiles, hot identity/user/memory context counts as already available for ordinary replies.

Do **not** file-read or search active `SOUL.md`, `USER.md`, or `MEMORY.md` merely to satisfy the grounding packet.

File-read hot profile files only when:

1. editing or auditing those files;
2. resolving an injection/freshness failure;
3. needing exact line-level text or full-file verification;
4. comparing profile distribution copies or cross-profile drift.

## Correct sequence

1. Use the hot context already present in the turn as the baseline.
2. Load the relevant skill route/domain skill.
3. Use Hindsight/provided recalled memory context; call explicit Hindsight only when available recall is insufficient for the claim.
4. Check Obsidian only when the turn goes beyond available hot context into memory, identity, protocol, canon, strategy, company, or stored context.
5. Use live tools for current state, external facts, file/repo/runtime state, actions, and completion claims.

## Cross-profile lesson

If Galih corrects a workflow that affects both Galyarder and Keiya/default, do not patch only the active profile. Update the class-level skill and any default/Keiya-facing wording or distribution references that carry the same bad instruction.

## Bad pattern

```text
User: woi
Agent: searches for SOUL.md, USER.md, MEMORY.md; reads them again; searches Obsidian; replies.
```

This is wrong for ordinary replies when those hot layers are already present in the turn.

## Good pattern

```text
User: woi
Agent: uses hot context + loaded core skills; no duplicate file read; replies briefly.
```

Final reply should not dump grounding machinery unless Galih asks.