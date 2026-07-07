---
author: Galyarder Labs
description: Use when evaluating messy, cross-domain Galyarder company matters to
  select active profiles, tasks pipeline setups, or strategy-to-tactics transitions.
license: MIT
metadata:
  hermes:
    category: galyarder-company
    tags:
    - galyarder-company
    - seneth-council-router
name: seneth-council-router
version: 1.0.0
---

# Seneth Council Router

Seneth is the routing layer for the Galyarder skill universe. It does not replace specialist skills; it chooses the smallest effective path through them.

Use Seneth when the situation spans multiple domains, when Galih asks “pake skill apa dulu?”, or when the next move could belong to Keiya, Galyarder, a named internal mode, a Galyarder Framework specialist, or a native Hermes tool.

Seneth is now the **fallback council router**. The canonical first entrypoint for skill/category/agent selection is `galyarder-framework-router`. If the router selects a Galyarder Labs/product/company route, use `galyarder-specialist` next. Use Seneth only when the route remains cross-domain, ambiguous, politically/strategically messy, or needs a council-style synthesis.

## Routing Laws

1. **State before structure.** If Galih is fragile, sick, emotionally flooded, or relationally exposed, route through Keiya first before hard analysis.
2. **Exact trigger beats council.** If one skill clearly matches, load that skill directly; do not over-orchestrate.
3. **Minimal council.** Choose one primary skill and at most two secondary skills unless the user asks for a full council.
4. **Separate profile from skill.** Keiya/Galyarder are profiles/personas; skills are modes/specialists inside the runtime. Keiya/default skills may be practical assistant capabilities; Galyarder skills should be business/product-native.
5. **Skills route through agent behavior, not magic function calls.** A router skill should explicitly name which `skill_view(name)` calls to load next; it cannot assume a deterministic call chain unless an actual tool/script implements one.
6. **Operational tools are part of routing.** If the job is Gmail, Calendar, Docs, files, MCP, Context7, terminal, cron, Obsidian, GitHub, or browser, route to the relevant tool/skill pair.
7. **Verify before claiming.** For config, code, files, cron, or external side effects, include a verification step.

## Output Contract

When invoked, answer in this shape:

- **problem type:** what kind of situation this is
- **recommended profile/posture:** Keiya, Galyarder, or both in sequence
- **primary route:** the first skill/tool to load or action to take
- **secondary route:** optional support skills/tools
- **why:** short reason for the route
- **input needed:** only what is truly missing
- **next move:** one concrete next action

## Canonical Orchestrator Shape

When Galih asks for a Galyarder Specialist, a main Galyarder router, or whether the framework is enough, route as follows:

```text
SOUL/profile posture -> galyarder-framework-router -> Seneth only if ambiguous/cross-domain; `galyarder-specialist` is legacy support, not the first router -> execution doctrine -> domain specialist -> native tools -> artifact + verification
```

Use this output shape for routing-architecture answers:

- current playwright-pro: which skills already cover the job
- missing orchestration: whether a canonical main router/specialist is absent or only partially covered
- canonical entrypoint: the skill that should be loaded first today
- next skills to load: exact `skill_view` names, not vague categories
- whether to create/patch: prefer patching Seneth or an umbrella skill before adding a narrow new skill
- verification: how to confirm the routed skill/library shape works

Important distinction:

- **Keiya/default skills**: practical assistant/partner capabilities for everyday execution, research, docs, finance modeling, media, comfort, and flexible help.
- **Galyarder skills**: Galyarder Labs/business/product-native capabilities: strategy, Ledger/HQ, company ops, approval gates, state transitions, evidence, audit trails, and specialist workforce routing.

## Core Routing Map

### Personal / Self Layer

- `saryn-archive` — raw intake, notes, threads, videos, conversations → structured second brain.
- `draith-doctrine-check` — evaluate a non-trivial decision against Galih’s doctrine.
- `keiya-presence-memory` — relationships, neglected bonds, caring moves, relational repair.
- `draith-doctrine-check` — gap between current self and intended self, habits, experiments.
- `draith-doctrine-check` — downside, fear, fragility, worst-case, resilience moves.

### Company / Empire Layer

- `business-strategy-operator` — too many ideas/projects; choose 1–3 priorities and kill/park the rest.
- `business-strategy-operator` — chosen objective → implementation writing-plans, milestones, risks, next actions.
- `business-strategy-operator` — meaningful decision already made; record reasoning and review trigger.
- `seneth-council-router` — unclear which route to take first.

### Galyarder Skill Taxonomy

Galyarder Framework is now a routing/doctrine layer, not a jumbo bucket for every specialist. Use `galyarder-execution-doctrine` for shared standards, then route to the smallest specialist category.

Common routes:

- Software factory / repo delivery: `gstack-workflow` first for `investigate`, `qa`, `qa-only`, `review`, `ship`, `land-and-deploy`, `canary`, `design-review`, `devex-review`, `benchmark`, and context save/restore.
- Engineering doctrine: `software-development` for `architect`, `architect`, `elite-developer`, `systematic-debugging`, `systematic-debugging`, `writing-writing-planss`, `writing-writing-planss`, `github-pr-workflow`, `verification-before-completion`.
- Product / writing-plansning: `product-management` for `product-manager`, `product-manager`, `prd-to-writing-plans`, `product-manager`, `writing-plansner`, `product-manager`, `brainstorming`, `experiment`, `deploy`, `brainstorming`.
- Company / strategy / fundraising: `galyarder-company` for `galyarder-ceo`, `galyarder-cto`, `galyarder-ceo`, `galyarder-cfo-coo`, `galyarder-cfo-coo`, `founder-context`, `galyarder-cfo-coo`, `investor-research`, `pitch-deck`, `data-room`, `board-update`, `accelerator-application`.
- Design references: `design-systems` for `design-system-*` style libraries. Use gstack design workflows for live UI execution/review.
- QA / testing: `qa-testing` for Playwright and test-specific helpers not covered by gstack.
- DevOps / reliability: `devops` for `devops-engineer`, `deploy`, `sre`, `deploy`, `finops`, `saas-finops-optimization`.
- Security: `security` for `security-guardian`, `security-guardian`, `cloud-security`, `cybersecurity`, `perseus`, MITRE / phishing / ransomware / malware skills.
- Growth / marketing / sales: `growth` for `growth-strategist`, `growth-strategist`, `marketing`, `copywriting`, `copywriting`, `seo`, `cro`, `sales-engineer`, `growth-strategist`, `growth-strategist`.
- Finance / legal: `finance-legal` for `accounting`, `financial-analyst`, `legal`, `legal-counsel`, `legal-counsel`, `legal-counsel`, GDPR, licensing, and compliance.
- Notes / knowledge: `note-taking` for Obsidian, Bases, markdown, and JSON Canvas.

### Tool / Platform Layer

- Hermes config, profiles, MCP, gateway, cron, model/tool issues: `hermes`, `native-mcp`, `hermes`
- Google Workspace: `google-workspace`
- Email IMAP/SMTP: `himalaya`
- Obsidian notes/vault: `obsidian`, `obsidian`, `obsidian`, `obsidian`, `obsidian`
- GitHub: `github-auth`, `github-repo-management`, `github-issues`, `github-pr-workflow`, `github-code-review`, `codegraph-codebase-analysis`
- Context7 docs: use native Context7 MCP tools directly after resolving library ID.
- Autonomous coding agents: `claude-code`, `codex`, `opencode`, `pi-cli`, plus `writing-writing-planss` for current-session delegation.

## References

- Full expanded routing map: `references/galyarder-multi-agent-routing.md`
- Current enabled skill family index: `references/current-enabled-skill-index.md`
- Galyarder Specialist / Orchestrator session notes: `references/galyarder-specialist-orchestration.md`

## Common Mistakes

- Routing every strategic issue to only `draith` or `noctis`; many problems are product, finance, legal, growth, or engineering problems.
- Treating Keiya and Galyarder as skills. They are profile/posture layers.
- Running all skills in sequence. Pick the smallest useful path.
- Forgetting native tools. Some requests are solved by Google Workspace, Context7, GitHub, terminal, file tools, cron, or browser before any specialist reasoning.
- Giving a writing-plans when the first move should be emotional stabilization.
