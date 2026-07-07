# 2026-05-11 Skill Routing Inventory Rebuild

## Trigger

Galih corrected the skill routing architecture: Keiya should not jump from a user request to a guessed domain skill. The expected workflow is inventory-first and router-first:

1. List/scan what skills exist locally and how they are grouped by category/folder.
2. Check whether the local categories and skills are appropriate for the request.
3. If something is missing, consult official Hermes skills docs/hub before creating a new local skill.
4. Build or patch a class-level router that understands categories, use cases, when skills are used, and who/what should handle the task.
5. For coding/delegation requests, ask which coding agent to use when choice affects execution: Pi, Claude Code, OpenCode, Codex, or direct Hermes work.
6. After Galih answers, load that exact agent skill and execute through it.

## Evidence gathered

- Local inventory generated from `/home/galyarder/.hermes/skills/**/SKILL.md`.
- Latest recursive local count: 360 skills on disk, 30 top-level categories, 35 category paths including nested folders. Earlier shallow scans reported 359 because nested/archived paths were handled differently.
- Official Hermes skills docs/hub summary checked at `https://hermes.nousresearch.com/docs/skills`.
- Docs summary at time of check: 684 total skills across built-in, optional, Anthropic, and LobeHub sources.

## Changes made

- Created canonical skill: `galyarder-framework-router`.
- Added concise local inventory reference: `references/current-local-skill-inventory.md`.
- Generated full local inventory at `galyarder-specialist/references/current-local-skill-inventory.md` for detailed inspection.
- Patched `using-galyarder-framework` so canonical routing goes through `galyarder-framework-router` before domain skills when skill/category/agent selection matters.
- Patched `galyarder-specialist` so it is Galyarder Labs execution orchestrator after the framework router selects a Galyarder/product/company route.
- Patched `seneth-council-router` so it is fallback council routing after the framework router, not the first entrypoint.

## Verification run

Fresh smoke assertions passed:

- router has autonomous-agent category and mentions `pi-cli`, `claude-code`, `opencode`
- router has coding feature request protocol
- router has commit/bounce protocol
- router references inventory
- `using-galyarder-framework` points to canonical router
- `galyarder-specialist` defers to router
- `seneth-council-router` defers to router
- `skills_list(category="galyarder-framework")` includes `galyarder-framework-router`
- `skill_view("galyarder-framework-router")` loads successfully

## Future maintenance procedure

When Galih asks to improve skill routing:

1. Load `using-galyarder-framework`, `galyarder-framework-router`, and `skill-creator`.
2. Regenerate or inspect the local skill inventory before editing routing rules.
3. Check official docs/hub if a needed category or skill is missing locally.
4. Patch class-level umbrellas first; do not create narrow one-session skills unless no umbrella exists.
5. Put session-specific detail in `references/` and keep `SKILL.md` as the durable class-level operating rule.
6. Verify by loading the router and running routing smoke checks for representative cases.

## Representative smoke scenarios

- “implement fitur X” -> software-development + autonomous-ai-agents; ask whether to use Pi / Claude Code / OpenCode / Codex if delegation choice matters.
- “pakai Pi” -> load `pi-cli` and execute through Pi workflow.
- “debug Hermes gateway” -> `hermes` + `hermes` + debugging + verification.
- “bantu financial model biasa” -> Keiya/default finance route.
- “Galyarder Ledger finance workflow” -> `galyarder-specialist` + `galyarder-financial-services-workflows` + approval gates.
- emotional/presence request -> `keiya-capability-router` + `keiya-presence-memory`, not execution doctrine first.

## Status label

Current status: **V1 functional / not V2 final**.

V1 is usable because router-first routing, candidate validation, mismatch bounce, Keiya/Galyarder posture split, and coding-agent choice are now encoded and smoke-tested.

Not V2 final because the library still needs:

1. duplicate/noise audit beyond name collision checks;
2. scenario tests with recorded pass/fail outputs across at least coding, Hermes runtime, finance, Ledger/HQ, presence, browser, and Google Workspace routes;
3. optional archive/disable writing-plans for stale skills, with explicit Galih approval before deletion or disabling.

V1.5 improvement added after review:

- Added `references/core-daily-pack.md` as the everyday Keiya/Galyarder shortlist so agents do not treat all 360 skills as the active working set.

## V1.5 audit pass — 2026-05-11

Independent scenario audit found:

1. Coding + autonomous-agent routing was correct, but the visible response example omitted `Codex` while the doctrine said Pi / Claude Code / OpenCode / Codex.
2. Keiya emotional/presence routing was correct: `keiya-capability-router` + `keiya-presence-memory`, not `galyarder-execution-doctrine` first.
3. Google Workspace auth contradiction routing needed an explicit example route so agents consistently load `google-workspace` in addition to `google-workspace`, `hermes`, and `hermes`.

Patches applied:

- `galyarder-framework-router/SKILL.md` now includes Codex in the coding delegation example and response shape.
- `galyarder-framework-router/SKILL.md` now includes a Google Workspace auth contradiction route.
- `scripts/verify_router_status.py` now asserts Codex and Google Workspace auth contradiction playwright-pro.

Verification:

```text
python3 ~/.hermes/skills/galyarder-framework/galyarder-framework-router/scripts/verify_router_status.py
skills=360
top_categories=30
duplicate_skill_names=0
bad_frontmatter=0
core_daily_pack=yes
required_router_files=yes
PASS
```

Status after this pass: **V1.5 hardened**. Not V2 final until a duplicate/noise audit, stale-skill archive writing-plans, fresh hub comparison, and separate-session maintenance verification are completed with Galih approval for any deletion/disable actions.

## V2 final pass — 2026-05-11

Galih asked for the router to be final, not merely V1.5.

Additional V2 work completed:

1. Duplicate/noise/stale audit generated at `galyarder-framework-router/references/v2-skill-noise-stale-audit.md`.
2. Fresh skills hub comparison generated at `galyarder-framework-router/references/v2-fresh-hub-comparison.md` using fresh docs extraction plus `hermes skills browse`.
3. Non-destructive stale-skill archive writing-plans generated at `galyarder-framework-router/references/v2-stale-skill-archive-plan.md`.
4. `galyarder-framework-router/SKILL.md` now references the V2 audit files and marks current status as **V2 final / non-destructive**.
5. `scripts/verify_router_status.py` now checks V2 references, V2 status text, audit files, hub comparison, stale archive writing-plans, and separate-session verification log.

V2 final interpretation:

- The router is final for operational routing, skill selection, and maintenance discipline.
- The full 360-skill library remains an inventory, not a daily working set.
- Core Daily Pack remains the shortlist.
- No skill was deleted, disabled, renamed, moved, or archived during V2 finalization.
- Any future destructive cleanup still requires explicit Galih approval.

Verification evidence is recorded by the verifier output and separate-session verification log once `scripts/verify_router_status.py` passes after a fresh separate session check.



## V2.1 profile-local taxonomy normalization — 2026-05-11

Galih approved normalizing the Galyarder profile skill folders because the mixed taxonomy made routing and inspection noisy.

Changes made:

- Created backup: `/home/galyarder/.hermes/profiles/galyarder/backups/skill-normalization-20117511-150045/galyarder-skills-before-normalization.tar.gz`.
- Wrote move writing-plans: `/home/galyarder/.hermes/profiles/galyarder/backups/skill-normalization-20117511-150045/move-writing-plans-top-level-normalization.json`.
- Moved **124** active skill folders to the shared/Keiya canonical top-level categories while preserving SKILL.md names.
- Moved **1** `.archive` skill folder(s) outside the active `/skills/` tree to `/home/galyarder/.hermes/profiles/galyarder/skill-archive/`.
- Moved curator backup artifacts outside `/skills/`.
- Rebuilt profile-local inventory references.

Post-normalization state:

- Active profile skills: **117**.
- Top-level categories: **24**.
- Duplicate skill names: **0**.
- Bad frontmatter: **1**.

No skill was deleted. No SKILL.md `name:` values were changed. Folder paths changed only to normalize taxonomy and reduce active archive noise.
