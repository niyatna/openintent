# Router Governance After Taxonomy — 2026-05-12

This note records the post-taxonomy routing cleanup after Galih manually reviewed/improved skill positions.

## Current policy

- `using-galyarder-framework` = mandatory skill-use discipline: load relevant skills before substantive answers, verify with tools, and do not guess from memory.
- `galyarder-framework-router` = canonical first router for Galyarder/company/product/framework/skill-taxonomy/coding-agent selection.
- `keiya-capability-router` = default/Keiya practical assistant router for everyday help, comfort/presence, media, research, docs, scheduling, and personal execution.
- `seneth-council-router` = fallback council router only when the route is messy/cross-domain/ambiguous or needs Keiya + Galyarder sequencing.
- `galyarder-specialist` = legacy/domain-map support skill. It is not the first router anymore. If it conflicts with `galyarder-framework-router`, the framework router wins.

## Canonical flow

```text
incoming request
  -> using-galyarder-framework discipline
  -> direct command? execute literal first
  -> profile/posture split
      -> Keiya/default everyday task: keiya-capability-router
      -> Galyarder/company/product/framework/task routing: galyarder-framework-router
      -> ambiguous cross-domain/council: seneth-council-router
  -> load one primary domain skill + at most 1-2 support skills
  -> use native tools
  -> verify before completion claim
```

## Category names after normalization

Use these real top-level shelves, not older synthetic names like `engineering`, `product`, `marketing`, `finance`, `knowledge`, `operations`, or `legal-risk`:

- `software-development`
- `product-management`
- `growth`
- `finance-legal`
- `galyarder-company`
- `galyarder-framework`
- `galyarder-self`
- `devops`
- `qa-testing`
- `security`
- `research`
- `note-taking`
- `creative`
- `productivity`
- `communication`
- `autonomous-ai-agents`
- `gstack-workflow`
- `mlops`
- `browser`
- `mcp`

## Post-review cleanup performed

- Synced newer router/how-to-use docs from Galyarder to Keiya/default where Keiya was stale.
- Reasserted `galyarder-framework-router` as canonical first router.
- Reframed `galyarder-specialist` as legacy/domain-map support.
- Updated `keiya-capability-router` escalation paths to `galyarder-framework-router`.
- Removed stale disabled config entries for design-system skills that no longer exist after Galih's manual review.
- Removed `.hub/lock.json` orphan entries for skills no longer active and fixed stale lock paths.
- Fixed category metadata on moved/manual-review skills such as `photography-critic`, `fitness-nutrition`, and `kpi-hero`.

## Verification gates

Before claiming future router/taxonomy work is done:

1. Parse all active `SKILL.md` files in both profile roots.
2. Verify duplicate names = 0 and bad frontmatter = 0.
3. Verify disabled config entries all match active skill names/folders.
4. Verify `.hub/lock.json` entries resolve to active skill names and correct relative paths.
5. Verify router skill paths exist in both profiles:
   - `using-galyarder-framework`
   - `galyarder-framework-router`
   - `keiya-capability-router`
   - `seneth-council-router`
   - `galyarder-specialist`
6. Smoke `hermes --profile default skills list --enabled-only` and `hermes --profile galyarder skills list --enabled-only`.
