# External Repo Skill Adaptation Notes

Use this when a session adapts an external repo into Hermes/Galyarder skills.

## Lesson

Do not abstract too early. First identify what the repo actually contains and why it is valuable.

A wrong conversion pattern:

- repo contains domain workflows
- agent creates a meta architecture skill
- user has to correct that the repo was actually about finance, docs, browser, testing, etc.

Correct conversion pattern:

1. Inspect the repo inventory: README, layout, manifests, skill files, commands, scripts.
2. Name the primary payload:
   - domain workflows
   - scripts/tools
   - architecture pattern
   - deployment recipe
   - data connectors
   - examples/templates
3. Create or patch a class-level umbrella skill for that payload.
4. Adapt to the active profile:
   - Keiya/default = general assistant and relational support use case.
   - Galyarder = Galyarder Labs execution infrastructure, Ledger/HQ/Framework/Agent state, evidence, approval gates, audit trail.
5. Add architecture insights as a section inside the domain skill unless architecture is the repo's primary payload.
6. Verify frontmatter, duplicate names, directory/name match, and skill loadability.
7. If a wrong skill was created, delete it with `absorbed_into` pointing at the correct umbrella skill.

## Session Example

Anthropic `financial-services` was initially misread as mainly an agent architecture pattern. The user corrected that the repo contained actual financial-services skills.

Correct final shape:

- Keiya/default can have a general `galyarder-financial-services-pack` for standard assistant finance work product.
- Galyarder profile should have `galyarder-financial-services-workflows` mapped to Galyarder Ledger/HQ with evidence, citations, formulas, review gates, and audit/command state.

Wrong shape:

- a standalone `hermes-vertical-agent-architecture` skill as the primary artifact for a finance workflow repo.

## Check Question

Before creating the skill, ask internally:

> If the user asked "what did you actually take from the repo?", would the answer name the repo's concrete domain payload, or only a generic architecture abstraction?

If the answer is generic, inspect again before creating.
