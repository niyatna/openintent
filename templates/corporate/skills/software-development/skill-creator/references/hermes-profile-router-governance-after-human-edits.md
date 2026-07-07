# Hermes Profile Router Governance After Human Skill-Position Edits

Use this when Galih manually reviews, moves, deletes, or re-categorizes skills after an agent has already completed a cross-profile sync or taxonomy pass.

## Why this matters

A human position cleanup can invalidate router assumptions even when all `SKILL.md` files still parse. Treat the human edit as a new governance state, not as a cosmetic folder change.

Common drift after human edits:

- router docs still reference old synthetic category names such as `engineering`, `product`, `marketing`, `finance`, `knowledge`, `operations`, or `legal-risk`
- `.hub/lock.json` contains orphan entries for skills no longer active
- lock `path` / `install_path` points to old locations
- `config.yaml` keeps disabled entries for skills that no longer exist
- `metadata.hermes.category` no longer matches the top-level folder
- Keiya/default and Galyarder copies of routing skills diverge
- legacy support routers accidentally regain authority over the canonical router

## Canonical router hierarchy

Current policy after the 2026-05-12 Keiya/Galyarder cleanup:

```text
using-galyarder-framework
  = mandatory skill-use discipline / how to use skills

galyarder-framework-router
  = canonical first router for skill/category/agent selection

keiya-capability-router
  = Keiya/default everyday assistant router

seneth-council-router
  = fallback council router for messy/cross-domain/Keiya+Galyarder sequencing

galyarder-specialist
  = legacy/domain-map support, not the first router
```

If `galyarder-specialist` conflicts with `galyarder-framework-router`, the framework router wins.

## Required audit after manual edits

1. Inventory both roots explicitly:
   - Keiya/default: `/home/galyarder/.hermes/skills`
   - Galyarder: `/home/galyarder/.hermes/profiles/galyarder/skills`
2. Parse every active `SKILL.md`, excluding `.hub/` and `.archive/`.
3. Verify:
   - duplicate frontmatter names = 0
   - bad frontmatter = 0
   - disabled config entries all match active skill names/folders
   - `.hub/lock.json` entries all resolve to active skill names and correct relative paths
   - `metadata.hermes.category` exists and matches top-level folder where category is explicit
   - router skills exist in both profiles
4. Check router docs for stale synthetic categories and stale authority claims.
5. Regenerate router inventories after edits.
6. Smoke both profiles:
   - `hermes --profile default skills list --enabled-only`
   - `hermes --profile galyarder skills list --enabled-only`
   - one minimal `hermes --profile <profile> chat -Q -q ... --ignore-rules --max-turns 1`

## Router files to inspect/patch

Patch both profile copies when relevant:

- `galyarder-framework/using-galyarder-framework/SKILL.md`
- `galyarder-framework/galyarder-framework-router/SKILL.md`
- `galyarder-self/keiya-capability-router/SKILL.md`
- `galyarder-company/seneth-council-router/SKILL.md`
- `galyarder-framework/galyarder-specialist/SKILL.md`
- `galyarder-framework/galyarder-framework-router/references/current-local-skill-inventory.md`
- `galyarder-framework/galyarder-specialist/references/current-local-skill-inventory.md`

## Category naming rules

Use real top-level shelves. Do not reintroduce old synthetic names.

Preferred category shelves include:

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

Avoid stale category labels like:

- `engineering`
- `product`
- `marketing`
- `finance`
- `knowledge`
- `operations`
- `legal-risk`
- `gstack-suite`

## Hub lock cleanup pattern

For each remaining lock entry:

- If lock key matches an active frontmatter `name`, update `path` / `install_path` / `local_path` to the actual relative directory.
- If lock key no longer matches any active skill name, remove it unless there is a clear one-to-one frontmatter rename.
- If renaming a lock key, preserve provenance fields and add `legacy_lock_key` only when useful for future audits.

Do not trust lock state as proof of installed skills. The active `SKILL.md` frontmatter is the source of truth.

## 2026-05-12 final evidence pattern

A successful post-human-edit governance pass ended with:

- Keiya/default: 514 skills, 512 enabled, 26 categories, 2 valid disabled entries, hub lock 191/191 resolving
- Galyarder: 438 skills, 436 enabled, 25 categories, 2 valid disabled entries, hub lock 117/117 resolving
- shared skill names: 432
- Keiya-only: 82
- Galyarder-only: 6
- zero duplicates, bad frontmatter, unmatched disabled entries, missing category metadata, or category mismatches
- router stack verified with `skill_view` and both profile CLI smokes

The report artifacts were:

- `/tmp/router_governance_final_summary.md`
- `/tmp/router_governance_final_audit.json`
- `/tmp/cross_profile_after_router_governance.json`

Use those as examples of the level of evidence expected before claiming done.
