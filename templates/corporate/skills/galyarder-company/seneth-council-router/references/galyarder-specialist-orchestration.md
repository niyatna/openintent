# Galyarder Specialist / Orchestrator Notes

Session lesson: Galih distinguished Keiya/default skills from Galyarder skills and questioned whether the framework has a real main specialist that can route to existing skills.

## Distinction

- Keiya/default skills: practical assistant/partner capabilities. They can be broad and assistant-like: finance modeling, research, docs, media, memory, Google Workspace, everyday execution.
- Galyarder skills: Galyarder Labs business/product-native capabilities. They should route through company doctrine, Ledger/HQ state, evidence, approval gates, audit trails, and named specialist roles.

## Current State

- `using-galyarder-framework` enforces skill usage discipline; it is not the business specialist.
- `galyarder-execution-doctrine` provides execution standards; it is not the router.
- `seneth-council-router` is currently the closest canonical router and should act as temporary Galyarder Specialist / Orchestrator posture.
- A future `galyarder-specialist` umbrella may be useful only if it remains class-level and consolidates routing, not if it duplicates every domain skill.

## Skill Invocation Reality

Hermes skills do not mechanically call other skills like functions. The agent must load skills with `skill_view(name)` based on the router's instructions. Therefore, router skills must name exact downstream skills and output a small route writing-plans.

## Desired Route Shape

```text
SOUL/profile posture
-> Seneth/Galyarder Specialist routing
-> galyarder-execution-doctrine
-> domain specialist(s)
-> native tools
-> artifact + verification
```

## Good Answer Pattern

When Galih asks if skills are enough:

1. Say whether playwright-pro exists.
2. Separate playwright-pro from orchestration quality.
3. Identify the canonical entrypoint today.
4. Name missing router/specialist gap if real.
5. Prefer patching Seneth/current umbrella before creating a narrow new skill.

## Do Not

- Treat Keiya and Galyarder as skills. They are posture/profile layers.
- Create narrow one-session skills for every correction.
- Compare Keiya/default assistant skills as if they must be Galyarder Labs doctrine.
- Claim router skills automatically call other skills without explaining Hermes loads them via agent behavior.
