---
author: Galyarder Labs
description: Use when selecting which Hermes/Galyarder skill, category, specialist
  worker, or automated agent CLI should handle a request.
license: MIT
metadata:
  hermes:
    category: galyarder-framework
    references:
    - references/current-local-skill-inventory.md
    - references/core-daily-pack.md
    - references/2026-05-11-skill-routing-inventory-rebuild.md
    - references/v2-skill-noise-stale-audit.md
    - references/v2-fresh-hub-comparison.md
    - references/v2-stale-skill-archive-plan.md
    - references/router-merge-pitfalls.md
    - references/cross-profile-merge-patterns.md
    - references/cross-profile-skill-governance.md
    - references/cross-profile-taxonomy-normalization-2026-05-12.md
    - references/router-governance-after-taxonomy-2026-05-12.md
    related_skills:
    - using-galyarder-framework
    - keiya-capability-router
    - seneth-council-router
    - galyarder-execution-doctrine
    - galyarder-cfo-coo
    tags:
    - galyarder-framework
    - router
    - skills
    - orchestration
    - taxonomy
    - delegation
    - domains
name: galyarder-framework-router
status: V2.1.0 final / non-destructive
version: 2.1.0
---


# Galyarder Framework Router

## Purpose

This is the canonical router for the local Hermes/Galyarder skill library.

It exists because the library is large. Hundreds of skills are useful as an inventory, but only a small route should be active for any task. The router's job is to inspect the request, understand available categories, pick exact candidate skills, load and validate the chosen skill, and bounce back when the skill's trigger conditions do not match.

## First Principle

Do not guess a domain skill directly.

Route first, scan candidates, load the candidate, check its opening trigger/boundary lines, then commit or bounce.

```text
user request
  -> state/posture check
  -> category scan
  -> exact candidate skills
  -> load chosen skill
  -> trigger/boundary match?
      yes: use it
      no: bounce back, re-route, or ask
```

If a loaded skill is wrong, stop early and re-route.

## Direct-Command Escape Hatch

If the incoming request is a simple direct command (mention X, send Y, do Z, open A, build B for me), do not keep classifying domains.

1. Execute the command literally first.
2. Use the router only after execution confirms the command is done or if the command itself requires domain routing (e.g., "build PRD for Ledger Sales Agent").

This prevents the router from turning fast actions into unnecessary orchestration.

## Relationship to Other Router Skills

- `using-galyarder-framework` = global rule that relevant skills must be loaded.
- `keiya-capability-router` = everyday Keiya/default assistant routing, and Galyarder postures when needed.
- `galyarder-specialist` was absorbed into this router on 2026-05-18; this router remains the canonical entrypoint.
- `seneth-council-router` = persona/mode router for ambiguous situations across Keiya, Galyarder, strategic, and tactical modes.

## Selecting the Active Route

Use these rules in order.

1. If a direct command is present, execute it literally first.
2. If the request matches a known direct trigger (hermes config, gstack, obsidian, etc.), load that skill directly.
3. If the task matches Galyarder Labs routing, stay in `galyarder-framework-router`; use this router and its absorbed legacy reference for domain-map support.
4. If the request is for an autonomous coding agent, load the relevant agent skill.
5. If the request is Keiya/general/default assistant work, load `keiya-capability-router`.
6. If uncertain, load this router and use the category scan below.
7. Only load `seneth-council-router` if the request is ambiguous across Keiya/Galyarder/mode boundaries.

Never load every skill in a category. Pick 1 primary and 1-2 support.

When routing through community/LobeHub/external skills, treat them as advisory taste, design, product-thinking, or market-voice layers, not authority layers. Do not blanket-reject them as persona noise: Galih explicitly corrected this during the Skills Hub audit because skills like `gen-z`, copywriting, social, brand, design/product layers, prompt/media, and writing-polish can carry useful human-expertise value. Use them only when they add a distinct lens, and keep canonical Galyarder/company/security/finance/legal skills in command.

### Design routing hotbar

For design work, do not default to the huge `creative` category bundle. Use `galyarder-core`, then the smallest design route:

- `product-design-thinking` — Layers decision work: observed behaviour, domain, user needs, strategy, conceptual model, interaction flow, surface audit. Use when the problem/UX decision is unclear before visual polish.
- `design-taste-core` — default UI/frontend route: `design-taste`, `design-taste`, `design-taste`, `design-taste`, `design-taste`, plus verification.
- `frontend-style-variants` — push visual language: `design-styles`, `design-styles`, `design-styles`, `design-taste`, `web-widgets`, `design-styles`.
- `design-canvas-and-visual-gen` — design canvas/comps/brand boards: `superdesign`, `superdesign`, `superdesign`, `superdesign`, `superdesign`, `diagram-design`.

Load `creative` only when Galih explicitly asks for the whole creative folder/category context.

## Category Scan

Because the local skill library contains hundreds of skills across dozens of folders, do not scan every file.

Use the top-level category directories as the first classification level.

Example top-level categories after the 2026-05-12 taxonomy normalization:

- `growth`
- `software-development`
- `creative`
- `gstack-workflow`
- `mlops`
- `productivity`
- `security`
- `finance-legal`
- `research`
- `galyarder-company`
- `devops`
- `qa-testing`
- `communication`
- `autonomous-ai-agents`
- `galyarder-framework`
- `media`
- `product-management`
- `note-taking`
- `galyarder-self`
- `mcp`
- `browser`
- `dogfood`
- `gaming`
- plus small shelves when present: `blockchain`, `data-science`, `red-teaming`

For cross-profile skill governance, selective sync, disabled config cleanup, frontmatter repair, Keiya/Galyarder diff work, taxonomy normalization, or post-human skill-position review, use `references/cross-profile-skill-governance.md`, `references/router-governance-after-taxonomy-2026-05-12.md`, and run `scripts/verify_cross_profile_skill_sync.py`. Do not mass-sync profile-only skills unless Galih explicitly wants a noisy clone; selective capability sync is the default. After taxonomy normalization or Galih manual edits, both Keiya/default and Galyarder should keep clean canonical category shelves, valid disabled config, resolving hub locks, fresh router inventories, and no category metadata drift.

When a request mentions a clear domain or category, go to that category first, then pick the exact skill.

If the domain is unclear, ask one short clarifying question before loading five candidate skills.


## V2.1 Profile-Local Taxonomy Normalization

The Galyarder profile skill tree was normalized after Galih approval. Folder categories are now cleaner and closer to the shared/Keiya canonical taxonomy, while skill names remain the stable API.

Rules after normalization:

- Resolve and route by `name:` in SKILL.md, not by folder path.
- Treat folder category as a first-pass grouping only.
- Keep `galyarder-framework-router/` together with its `references/` and `scripts/`.
- Keep archived/stale material outside the active `/skills/` tree unless Galih explicitly asks to restore it.
- Rebuild `references/current-local-skill-inventory.md` after any future folder taxonomy change.

## Domain Routing Map

When a request needs domain classification, use this map to identify the primary skill and 1-2 support skills.

### strategy/operations
**Use when:** company direction, prioritization, strategic bets, operating cadence, cross-functional coordination

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `galyarder-ceo` | Strategy, direction, prioritization | `business-strategy-operator`, `business-strategy-operator`, `business-strategy-operator` |
| `galyarder-cto` | Technical architecture, tech stack, coding agent routing | `architect`, `elite-developer`, `galyarder-cfo-coo` |
| `galyarder-cfo-coo` | Cash, runway, ops, risk, compliance | `finops`, `financial-analyst`, `galyarder-cfo-coo` |
| `galyarder-ceo` | Positioning, distribution, demand | `growth-strategist`, `copywriting`, `copywriting` |
| `galyarder-cfo-coo` | Cross-functional coordination, operating cadence | `galyarder-ceo`, `business-strategy-operator`, `business-strategy-operator` |

### engineering
**Use when:** coding, debugging, architecture, testing, deployment, infrastructure

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `galyarder-cto` | Tech architecture decisions, coding agent selection | `architect`, `galyarder-ceo` |
| `elite-developer` | Production-grade implementation | `galyarder-execution-doctrine`, `verification-before-completion` |
| `galyarder-execution-doctrine` | Root cause debugging | `build-fix`, `systematic-debugging` |
| `galyarder-execution-doctrine` | New feature with TDD | `elite-developer`, `verification-before-completion` |
| `galyarder-execution-doctrine` | Implementation writing-plans writing | `galyarder-execution-doctrine`, `writing-plansner` |
| `galyarder-execution-doctrine` | Execute via subagents | `galyarder-execution-doctrine`, `verification-before-completion` |

### product
**Use when:** product strategy, requirements, PRD, conversion, onboarding, pricing

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `product-manager` | Product strategy, requirements, roadmap | `galyarder-ceo`, `growth-strategist` |
| `product-manager` | PRD authoring | `product-manager`, `prd-to-writing-plans` |
| `prd-to-writing-plans` | PRD → implementation writing-plans | `galyarder-execution-doctrine`, `galyarder-execution-doctrine` |
| `product-manager` | PRD → tickets | `product-manager`, `linear` |
| `growth-strategist` | Monetization, pricing, packaging | `accounting`, `galyarder-ceo` |
| `conversion-engineer` | Onboarding, activation, funnel | `onboarding-cro`, `onboarding-cro`, `onboarding-cro` |
| `brainstorming` | Fast PoC/MVP | `experiment`, `elite-developer` |

### finance-ledger
**Use when:** financial modeling, accounting, unit economics, Ledger/HQ finance, pricing

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `galyarder-cfo-coo` | Cash, runway, ops decisions | `financial-analyst`, `finops` |
| `galyarder-financial-services-workflows` | Ledger/HQ financial workflows | `galyarder-cfo-coo`, `galyarder-cto` |
| `financial-analyst` | Financial modeling, valuation | `galyarder-cfo-coo`, `accounting` |
| `finops` | Cloud/AI cost auditing | `finops-manager`, `saas-finops-optimization` |
| `accounting` | Bookkeeping, tax prep | `galyarder-cfo-coo` |
| `accounting` | Pricing decisions | `growth-strategist`, `galyarder-cfo-coo` |

### growth/market
**Use when:** positioning, campaigns, growth, distribution, competitors, content

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `galyarder-ceo` | CMO-level marketing decisions | `galyarder-ceo`, `growth-strategist` |
| `growth-strategist` | Acquisition, growth loops | `growth-strategist`, `growth-strategist` |
| `growth-strategist` | Market/customer research | `founder-context`, `growth-strategist` |
| `seo` | Search optimization | `copywriting`, `seo-audit` |
| `copywriting` | Content writing-plansning | `galyarder-ceo`, `galyarder-ceo` |

### docs/knowledge
**Use when:** documentation, notes, Obsidian vault, knowledge management

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `obsidian` | Obsidian vault operations | `obsidian`, `obsidian`, `obsidian` |
| `founder-context` | Canonical founder/startup context | `galyarder-ceo`, `galyarder-cto` |
| `docs` | Documentation authoring | `obsidian`, `obsidian` |
| `saryn-archive` | Raw intake → structured archive | `obsidian`, `obsidian` |

### legal-risk
**Use when:** legal, compliance, privacy, contracts, ToS

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `legal` | General legal reasoning | `legal-advisor`, `legal-counsel` |
| `legal-tos-privacy` | ToS/Privacy Policy | `legal-tos-privacy` |
| `legal-counsel` | Contract risk review | `legal-counsel`, `legal-counsel` |
| `legal-tos-privacy` | EU data processing | `legal-tos-privacy`, `legal` |

### security
**Use when:** security review, deploy response, threat intelligence

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `security-guardian` | Security posture review | `security-guardian`, `bitwarden` |
| `security-guardian` | Code/architecture security | `security-guardian`, `galyarder-cto` |
| `deploy` | Incident response | `security-guardian`, `galyarder-cto` |

### self/council
**Use when:** personal development, relationships, doctrine check, risk mapping

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `draith-doctrine-check` | Evaluate against Galih's doctrine | `galyarder-execution-doctrine` |
| `draith-doctrine-check` | Worst-case scenario mapping | `galyarder-ceo`, `galyarder-cto` |
| `draith-doctrine-check` | Self-improvement writing-planss | `keiya-presence-memory`, `draith-doctrine-check` |
| `keiya-presence-memory` | Relationship scan | `saryn-archive` |

### browser
**Use when:** browser automation, web QA, scraping, site testing

| Primary Skill | Use Case | Support Skills |
|---------------|----------|----------------|
| `galyarder-browser-routing` | Galyarder-specific browser routing | `browser-routing`, `camofox-browser` |
| `browser-routing` | General browser stack choice | `camofox-browser`, `gstack` |

## Autonomous Coding Agent Choice

When a request needs code changes, decide which coding agent to use.

Start from the desired route, then narrow down.

```text
request needs code
  -> simple/performance fix
     -> read skill, use direct simple path
  -> isolated file or issue
     -> use `pi-cli` for fast single-issue
  -> feature or PR-level change
     -> use `claude-code` or `opencode`
```

Agent decision rules:

- `claude-code`: multi-file features, deep debugging, important repo changes
- `opencode`: feature, implementation, PR review, medium complexity
- `pi-cli`: fast single-issue fixes, refactors, repo inspection, quick maintenance
- `codex`: speed-focused tasks, simple implementations, rapid prototyping

One-liner shorthand:

- "feature" → `claude-code` or `opencode`
- "fast fix" → `pi-cli`
- "deep debugging" → `claude-code` or `opencode`
- "simple implementation" → `codex`

## Posture Split: Keiya vs Galyarder

If the request affects Keiya posture, daily state, or immediate care, use `keiya-capability-router`.

If the request affects Galyarder Labs, hard standards, or company structure, use `galyarder-framework-router`; use `galyarder-specialist` only as legacy/domain-map support.

If it is a shared request, classify the dominant purpose first, then load the matching primary skill.

Never guess. If the request is mixed, split once into primary purpose.

## Curated Skill Stack (Top 34)

When scanning for relevant skills, check these first. They cover 90% of Galyarder execution needs.

### Orchestration / Routing (5)
- `using-galyarder-framework` — entrypoint, skill-scan mandate
- `galyarder-framework-router` — domain classifier + specialist picker (this skill)
- `galyarder-execution-doctrine` — shared execution standard, verification, shadow posture
- `seneth-council-router` — ambiguous/messy/cross-domain fallback
- `galyarder-cfo-coo` — operating cadence, cross-functional coordination

### Strategy / Company (5)
- `galyarder-ceo` — CEO-level strategy and company direction
- `galyarder-cto` — CTO-level technical architecture, tech stack, coding agent routing
- `business-strategy-operator` — reduce noise, choose priorities
- `business-strategy-operator` — convert objective into execution writing-plans
- `business-strategy-operator` — record meaningful decisions

### Engineering (6)
- `elite-developer` — production-grade implementation
- `galyarder-execution-doctrine` — 4-phase root cause
- `galyarder-execution-doctrine` — RED-GREEN-REFACTOR
- `galyarder-execution-doctrine` — implementation writing-planss
- `galyarder-execution-doctrine` — delegate via subagents
- `verification-before-completion` — never claim done without proof

### Autonomous AI Agents (4)
- `claude-code` — complex features, deep context, multi-file changes
- `opencode` — features, PR review, medium complexity
- `pi-cli` — quick fixes, refactors, repo inspection
- `codex` — speed-focused tasks, simple implementations

### Product / Design (7)
- `product-manager` — product strategy, requirements, roadmap
- `product-manager` — PRD authoring
- `prd-to-writing-plans` — PRD breakdown into implementation
- `product-design-thinking` / `product-design-thinking` — product-design decision diagnosis before surface work
- `design-taste` — production frontend design vocabulary, critique, polish, live/design commands
- `design-taste` — anti-slop UI/default design taste for frontend generation
- `superdesign` — external design-canvas/draft workflow when visual comps are the deliverable

### Finance (3)
- `galyarder-cfo-coo` — CFO/COO decisions
- `galyarder-financial-services-workflows` — Ledger/HQ finance workflows
- `financial-analyst` — financial modeling, valuation

### Growth / Marketing (2)
- `galyarder-ceo` — CMO-level marketing decisions
- `growth-strategist` — acquisition, growth loops

### Self / Council (5)
- `saryn-archive` — raw intake → structured archive
- `draith-doctrine-check` — evaluate against Galih's doctrine
- `draith-doctrine-check` — worst-case scenarios
- `draith-doctrine-check` — self-improvement writing-planss
- `keiya-presence-memory` — relationship scan

### Docs / Knowledge (1)
- `obsidian` — Obsidian vault work

Total: **38 route entries**. Check these first. Load only the relevant ones. Never load the whole hotbar.

## Domain vs Generic Skill Preference

When both a `galyarder-*` prefixed skill and a generic Hermes skill exist for the same task:

| Task | Preferred (Galyarder mode) | Fallback (generic) |
|------|---------------------------|-------------------|
| Debugging | `galyarder-execution-doctrine` | `systematic-debugging` |
| TDD | `galyarder-execution-doctrine` | `systematic-debugging` |
| Plans | `galyarder-execution-doctrine` | `writing-writing-planss` |
| Code review | `galyarder-execution-doctrine` | `writing-plans` |
| Subagent dev | `galyarder-execution-doctrine` | `writing-writing-planss` |
| Execution | `galyarder-execution-doctrine` | `verification-before-completion` |

Always prefer the `galyarder-*` version in Galyarder mode. The generic versions are for non-Galyarder tasks.

## Specialized Skill Direct Access

These skills are loaded directly when the trigger is clear. No routing needed.

| Trigger | Skill |
|---------|-------|
| "hermes config", "hermes setup", "hermes troubleshoot" | `hermes` |
| "gstack", "/browse", "/ship", "/qa" | `using-gstack` |
| "obsidian vault", "obsidian note" | `obsidian` |
| "write writing-plans for..." | `galyarder-execution-doctrine` |
| "brainstorm", "explore options" | `brainstorming` |
| "design decision", "UX bottleneck", "onboarding unclear", "product design layers" | `product-design-thinking` + `product-design-thinking` |
| "frontend design", "UI polish", "design-taste", "taste skill" | `design-taste` + `design-taste` |
| "Superdesign", "design canvas", "design draft/comps" | `superdesign` |
| "log decision" | `business-strategy-operator` |
| "focus on what" | `business-strategy-operator` |
| "fundraising", "investor" | `galyarder-cfo-coo` |
| "data room" | `data-room` |
| "hermes runtime", "gateway troubleshoot" | `hermes` |

## Pre-Flight Checklist

Before responding to any Galyarder request, verify:

- [ ] **Direct command?** If yes, execute literally. Stop here.
- [ ] **Known direct trigger?** If yes, load that skill directly. Stop here.
- [ ] **Domain classified?** Which domain(s) does this touch?
- [ ] **Primary skill loaded?** Load it via `skill_view(name)`.
- [ ] **Support skills loaded?** 1-2 max, not the whole folder.
- [ ] **Trigger/boundary match?** Does the loaded skill's opening actually fit the request?
- [ ] **Canon docs needed?** If touching Galyarder Labs product/brand/design/agents → load README, BRAND, DESIGN, AGENTS.
- [ ] **Implementation needed?** If yes → route to coding agent via galyarder-cto.
- [ ] **Verification defined?** How do we know it's done? What's the proof?

If a loaded skill does not match, stop early and bounce back to re-route.

## Routing Decision Flow

```text
Request in
  ↓
Is this a simple direct command? (mention X, send Y, do Z)
  → YES: execute literally. Done.
  → NO: continue ↓

Is this a known direct trigger? (hermes config, gstack, obsidian, etc.)
  → YES: load that skill directly. Done.
  → NO: continue ↓

Classify domain using map above:
  strategy/operations → galyarder-ceo / galyarder-cto / galyarder-cfo-coo / galyarder-ceo / galyarder-cfo-coo
  engineering → galyarder-cto / elite-developer / debugging / TDD / writing-planss
  product → product-manager / product-manager / prd-to-writing-plans / growth-strategist
  finance-ledger → galyarder-cfo-coo / financial-analyst / finops
  growth/market → galyarder-ceo / growth-strategist / growth-strategist
  docs/knowledge → obsidian / founder-context / docs / saryn-archive
  legal-risk → legal / legal-counsel / legal-tos-privacy
  security → security-guardian / security-guardian / deploy
  self/council → draith-doctrine-check / draith-doctrine-check / draith-doctrine-check
  browser → galyarder-browser-routing / browser-routing
  ↓
Load primary skill
  ↓
Trigger/boundary match?
  → NO: bounce back, re-route, or ask
  → YES: continue ↓
  ↓
Does it need implementation?
  → YES: route to coding agent (claude-code / opencode / pi-cli / codex)
  → NO: execute with primary + 1-2 support skills
  ↓
Apply galyarder-execution-doctrine for verification
  ↓
Deliver artifact
```

## After Delivery

Summarize what was routed, which skills were used, and whether there is a follow-up route.

Useful delivery note format:

```text
route used
loaded skill(s)
verification result
any recommended follow-up route
```

## Checklist

Use before any Galyarder Labs deliverable.

- [ ] Domain classified
- [ ] Canonical docs loaded when required
- [ ] Primary skill loaded
- [ ] Support skills loaded (1-2 max)
- [ ] Coding agent selected if implementation needed
- [ ] Artifact/output defined
- [ ] Approval/verification gates identified
- [ ] Explicit non-actions named for complex tasks
- [ ] Trigger/boundary validated for loaded skill

## Final Rule

If the request is Galyarder Labs work, load `galyarder-framework-router` first.
Choose one primary skill and at most one or two support skills.
If the loaded skill does not match, bounce back and re-route.
If uncertainty remains after loading skills, pause and clarify with the user.
Never ship output that contradicts canonical docs.

If a domain folder contains more than five skills, rely on the routing table above.
Do not attempt to load every skill in a folder because the folder name matches the request.

## Common Routing Scenarios

These are representative routing examples that demonstrate how the router handles different request types.

### Coding Feature Request
"implement fitur X" → load `galyarder-cto` → choose agent: Claude Code for complex multi-file, OpenCode for medium complexity, Pi for quick fix, Codex for speed-focused simple implementation.

### Hermes Runtime Bug
"hermes runtime error X" → load `hermes` + `hermes` → debug → verify with `verification-before-completion`.

### Google Workspace Auth Contradiction
"Google Workspace auth contradiction" or "gws not working" → load `hermes` + `hermes` + `google-workspace` → check actual gws runtime state with a tiny API call to verify, don't just check legacy token wrapper → if auth contradiction found, fix credential flow via `google-workspace` if it exists, otherwise fix inline.

### Ordinary Finance
"Ordinary finance" or company finance questions → load `galyarder-financial-services-workflows` (the canonical Galyarder financial services pack) + `financial-analyst` → use `galyarder-cfo-coo` for decisions.

### Ledger Finance
"Galyarder Ledger finance workflow" or Ledger/HQ finance → load `galyarder-financial-services-workflows` as primary → support: `galyarder-cfo-coo` + `galyarder-cto`.

### Obsidian Vault
"Obsidian vault" or vault operations → load `obsidian` → support: `obsidian`, `obsidian` as needed.

### GBrain / brain DB
"GBrain", "brain DB", "project brain", or DB-backed markdown memory → load `gbrain` as the thin Hermes route. Do not import GBrain internal skillpack into Hermes. Use canonical OS-home `/home/galyarder/gbrain` via the profile wrapper; GBrain is for DB-backed brain search/query/import, while Hindsight/session_search handle conversation memory and Obsidian handles vault files.

### Emotional State
"Emotional state" or presence/care requests → route to `keiya-capability-router` → load `keiya-presence-memory` if needed → do NOT pull `galyarder-execution-doctrine` first. Emotional requests need care, not execution gates.

## Absorbed legacy skill: `galyarder-specialist`

Unique material from `galyarder-specialist` is preserved in `references/absorbed-galyarder-specialist-2026-05-18.md`. Route future work through this skill as the canonical target.
