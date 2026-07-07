# V2 Stale Skill Archive Plan — 2026-05-11

## Decision

This writing-plans is non-destructive. No skill is deleted, disabled, renamed, moved, or archived unless Galih explicitly approves that specific action.

The V2 router treats noisy/stale/overlapping skills as an inventory management concern, not as a reason to break existing runtime references.

## Current State

- Active Galyarder profile inventory after V2.1 normalization: 117 skills.
- Exact duplicate skill names: 0.
- Bad frontmatter: 0.
- Archive/noise material moved outside active `/skills/` tree: 1 SKILL.md file plus curator backup artifacts.
- Heuristic stale/noise markers recorded in `v2-skill-noise-stale-audit.md`.
- Fresh hub comparison recorded in `v2-fresh-hub-comparison.md`.

## Archive Buckets

Use these buckets before proposing any destructive action:

1. **Compatibility shims**
   - Skills marked deprecated/redirect.
   - Keep installed unless their target umbrella exists, is verified, and no cron/job/profile references depend on the old name.

2. **Reference-only packs**
   - Design-system skills and other large passive reference families.
   - Keep installed, but keep out of Core Daily Pack unless explicitly requested.

3. **Overlapping specialist families**
   - TDD, debugging, writing-plansning, review, finance, legal, growth, browser/QA families.
   - Do not archive by name similarity alone. Prefer router precedence rules.

4. **Host-specific optional skills**
   - macOS/Apple, desktop, hardware, or other environment-specific skills.
   - Install/archive only when the actual host and user workflow need them.

## Proposal Procedure

Before archiving/disabling/removing a skill:

1. Search current local skill inventory and references for the skill name.
2. Check cron jobs, profile config, and any router/core-pack references when relevant.
3. Confirm replacement route exists and loads with `skill_view`.
4. Write a short proposal with:
   - skill name
   - reason
   - replacement/umbrella skill
   - references checked
   - rollback path
5. Ask Galih for explicit approval.
6. If approved, use `skill_manage(action="delete", absorbed_into=...)` only when the target umbrella exists; otherwise keep the skill and mark it as opt-in/noisy in router docs.

## Router Rule

The router must prefer selection rules over deletion:

- Core Daily Pack = active shortlist.
- Full active profile skill set = inventory; archived material remains recoverable outside active `/skills/`.
- Design-system/reference-only families = opt-in.
- Deprecated redirect skills = compatibility shims until approved cleanup.
- Galyarder-specific variants win for Galyarder product/company/framework tasks.
- Generic software-development/productivity variants win for ordinary tasks.

## V2 Final Condition

The stale-skill archive requirement is satisfied when this non-destructive writing-plans exists, the verifier checks it, and separate-session verification confirms the router can still load and enforce V2 without deleting/disabling anything.


## V2.1 normalization execution note

With Galih approval, profile-local folder normalization moved archive/noise material outside active `/skills/` without deleting it. Active skill folders were reclassified by category only; skill names and frontmatter names were preserved. Any future `skill_manage(action="delete")` remains destructive and still requires explicit approval.

Archive root used: `/home/galyarder/.hermes/profiles/galyarder/skill-archive/skill-normalization-20117511-150045`.
