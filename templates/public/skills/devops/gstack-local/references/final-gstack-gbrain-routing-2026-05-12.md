# Final gstack / GBrain / routing state — 2026-05-12

Use this as the post-cleanup reference after the Keiya/default and Galyarder skill-system review.

## Final verified skill state

| Profile | Unique skills | Duplicate names | Bad frontmatter | `gstack-workflow` dirs | Hermes `gbrain` skill |
|---|---:|---:|---:|---:|---:|
| Keiya/default | 507 | 0 | 0 | 45 | yes |
| Galyarder | 477 | 0 | 0 | 45 | yes |

Verification artifacts from the cleanup run:

- `/tmp/final_skill_system_gstack_gbrain_verify.md`
- `/tmp/final_skill_system_gstack_gbrain_verify.json`
- `/tmp/gstack_workflow_duplicate_cleanup.json`

## gstack decision

Keep two gstack repos for profile isolation:

```text
/home/galyarder/.claude/skills/gstack
/home/galyarder/.hermes/profiles/galyarder/home/gstack
```

Reason: gstack carries browser/cache/session/runtime state. Keiya/default and Galyarder can use isolated browser/cache state without splitting a single DB truth.

Do **not** keep duplicate generated Hermes skill directories. Each profile should have exactly 45 active `gstack-workflow` skill dirs with unprefixed names such as:

```text
autowriting-plans
browse
qa
ship
review
office-hours
setup-gbrain
```

If old prefixed dirs reappear, archive/remove them:

```text
gstack-autowriting-plans
gstack-browse
gstack-qa
gstack-ship
...
```

During cleanup, 45 stale prefixed dirs in Galyarder were archived to:

```text
/home/galyarder/.hermes/backups/gstack-workflow-duplicate-clean-20260512-233349
```

## GBrain decision

GBrain is the opposite: use one canonical OS-home instance because it owns DB/memory truth.

Canonical paths:

```text
repo: /home/galyarder/gbrain
data: /home/galyarder/brain
DB:   /home/galyarder/.gbrain/brain.pglite
CLI:  /home/galyarder/.bun/bin/gbrain
```

The Galyarder profile-local duplicate was archived earlier and the profile-local `gbrain` command is a wrapper that forces the canonical OS-home instance.

Use the thin Hermes `gbrain` skill under `research/gbrain`. Do not import GBrain's internal skillpack into Hermes.

## When GBrain is actually useful

Use GBrain for DB-backed markdown brain operations:

- import/search/query `/home/galyarder/brain`
- embedding health/backfill
- brain stats/doctor/skillpack-check
- minions/autopilot experiments after approval

Do **not** use GBrain as the default for every memory task:

- conversation recall → `session_search` / Hindsight
- durable small facts → Hermes memory / Hindsight retain
- long-form vault edits → Obsidian skills
- software factory QA/review/ship/browser workflow → gstack

## Routing stack after cleanup

```text
using-galyarder-framework
  -> galyarder-framework-router
     -> exact domain/tool skill

Keiya/default everyday route:
  -> keiya-capability-router

Ambiguous/cross-domain route:
  -> seneth-council-router

Legacy support:
  -> galyarder-specialist

Software factory:
  -> gstack-local / using-gstack / gstack-workflow/<skill>

DB-backed brain:
  -> gbrain
```

Router patches made:

- `galyarder-framework-router` now routes "GBrain / brain DB" to `gbrain`.
- `keiya-capability-router` now includes "GBrain / personal brain" route.
- `gstack-local` now distinguishes gstack, GBrain, and Hermes cron and uses normalized `gstack-workflow` names.
