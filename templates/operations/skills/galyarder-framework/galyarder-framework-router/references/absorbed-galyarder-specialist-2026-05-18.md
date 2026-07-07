# Absorbed skill: `galyarder-specialist`

Merged into `galyarder-framework-router` on 2026-05-18 during Galih-approved skill cleanup. Original SKILL.md preserved below for audit/rollback.

---

---
name: galyarder-specialist
description: Use when a Galyarder Labs request needs canonical routing across domain folders, Galyarder Framework orchestration, profile/posture choice, specialist skill selection, tool choice, artifact definition, approval gates, or verification criteria.
version: 1.0.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags:
    - galyarder-framework
    - orchestration
    - routing
    - specialist
    - domains
    - verification
    related_skills:
    - using-galyarder-framework
    - galyarder-execution-doctrine
    - seneth-council-router
    category: galyarder-framework
---

# Galyarder Specialist

## Status

`galyarder-specialist` is a legacy compatibility/domain-map support skill. The canonical first router is `galyarder-framework-router`. If they conflict, `galyarder-framework-router` wins.


## Overview

`galyarder-specialist` is the Galyarder Labs execution orchestrator after the canonical `galyarder-framework-router` has selected a Galyarder/company/product route.

It is not a domain expert and does not replace domain skills. It is the conductor for serious Galyarder work: it reads the request, chooses the correct posture, selects the smallest effective skill route, identifies native tools, defines the artifact, sets approval gates, and states how completion will be verified.

Use `galyarder-framework-router` first when the question is “which skill/category/agent should handle this?” Use this skill once the request is known to be Galyarder Labs/product/company execution.

## Mental Model

Galyarder skills should be organized as domain folders plus one orchestration layer.

```text
SOUL / Profile posture
  -> using-galyarder-framework
  -> galyarder-framework-router
  -> galyarder-execution-doctrine when consequence/verification matters
  -> domain specialist skill(s)
  -> native Hermes tools
  -> artifact + approval gate + verification
```

Hermes skills do not call each other like ordinary functions. The agent loads them with `skill_view(name)`. Therefore this skill must name exact next skills to load and must avoid vague category-only routing.

## When to Use

Use this when:

- the request is about Galyarder Labs, Galyarder Ledger, Galyarder HQ, Galyarder Ascendancy, Humans 3.0 Protocol, company strategy, product execution, finance, growth, fundraising, engineering, legal, security, operations, or canonical routing
- the user asks “skill mana?”, “frameworknya harus gimana?”, “orchestrate ini”, “buat writing-plans”, “bantuin business/product/finance model”, “refactor skill”, or “jadikan ini Galyarder-style”
- multiple domain folders could apply
- the task needs an artifact, approval gate, verification, or company operating discipline
- the agent is unsure whether to answer as Keiya/default assistant or as Galyarder Labs operator

Do not use this for:

- purely emotional/presence moments where Keiya should receive Galih first
- tiny casual questions with one obvious tool and no Galyarder consequence
- PAP/voice/intimate requests unless they touch Galyarder runtime architecture

## Output Contract

When routing, produce or internally follow this shape:

```markdown
## Route

- problem type:
- posture: Keiya / Galyarder / Keiya -> Galyarder
- domain folder:
- primary skill to load:
- support skills to load:
- native tools:
- artifact:
- approval gate:
- verification:
- next action:
```

Rules:

- Pick **one primary skill** whenever possible.
- Pick at most **two support skills** unless the user asks for a full council.
- Prefer exact skill names over categories.
- Before finalizing the route, scan/list candidate skills that plausibly match the request.
- Load the chosen primary skill and check its description / when-to-use / not-to-use boundaries before committing.
- If the opened skill's first lines do not match the request, bounce back here and choose another candidate instead of forcing the mismatch.
- Load domain skills only after the route is clear.
- Use `galyarder-execution-doctrine` for serious execution, not for every soft/casual response.
- If the next move can be done with a native tool, name the tool and use it.

## Posture Selection

### Keiya posture

Use when the request is personal, relational, casual, comfort-oriented, media-oriented, or ordinary assistant work.

Examples:

- “Kei aku capek” -> `keiya-presence-memory`
- “kirimin vn” -> TTS / voice note protocol
- “bantu cari info ini” -> research/web tools
- “bantu finance modeling dari data ini” without company-product framing -> Keiya finance assistant route

### Galyarder posture

Use when the request concerns company/product/system execution.

Examples:

- “design workflow Ledger”
- “bikin Galyarder Labs GTM writing-plans”
- “review architecture Hermes/G-Agent”
- “route fundraising workflow”
- “buat skill/domain taxonomy”

### Keiya -> Galyarder sequence

Use when Galih is emotionally loaded but the underlying task has company consequence.

Example:

- “aku capek tapi Ledger belum jalan”
  - first: Keiya receives state
  - then: `galyarder-framework-router` routes the execution work if Galih has capacity

## Domain Routing Map

### Framework / Orchestration

Use for routing, doctrine, writing-plansning discipline, debugging discipline, TDD, code review flow, and subagent execution.

- primary entrypoint: `galyarder-framework-router`
- mandatory skill-use rule: `using-galyarder-framework`
- shared execution standard: `galyarder-execution-doctrine`
- cross-domain fallback/council: `seneth-council-router`
- implementation writing-planss: `galyarder-execution-doctrine`
- debugging: `galyarder-execution-doctrine`
- TDD: `galyarder-execution-doctrine`
- subagent execution: `galyarder-execution-doctrine`
- code review request: `galyarder-execution-doctrine`

### Engineering / Software

Use for repository, architecture, implementation, testing, review, and shipping.

Common route:

```text
galyarder-framework-router -> galyarder-execution-doctrine -> architect/systematic-debugging/TDD/gstack -> tools -> tests/diff
```

Primary skills:

- architecture: `architect` or `architect`
- implementation: `elite-developer`
- bug/root cause: `galyarder-execution-doctrine` or `systematic-debugging`
- TDD: `galyarder-execution-doctrine` or `systematic-debugging`
- writing-plans: `galyarder-execution-doctrine`
- execution: `galyarder-execution-doctrine`
- verification: `verification-before-completion`
- live app QA/ship: gstack skills such as `qa`, `review`, `ship`, `land-and-deploy`, `canary`

### Product / Planning

Use for PRD, feature writing-plansning, experiments, prioritization, tracked work, and product decisions.

Primary skills:

- PRD: `product-manager`
- PRD to writing-plans: `prd-to-writing-plans`
- PRD to issues: `product-manager`
- writing-plansning: `writing-plansner`
- experiments: `experiment`
- deploys: `deploy`
- prototypes: `brainstorming`
- strategic objective -> milestones: `business-strategy-operator`
- too many ideas -> focus: `business-strategy-operator`
- decision record: `business-strategy-operator`

### Company / Strategy / Fundraising

Use for founder/company strategy, fundraising, investor communication, diligence, board updates, and executive lens work.

Primary skills:

- cross-functional founder ops: `galyarder-cfo-coo`
- CEO lens: `galyarder-ceo`
- technical/product company lens: `galyarder-cto`
- marketing lens: `galyarder-ceo`
- finance/ops lens: `galyarder-cfo-coo`
- founder source of truth: `founder-context`
- fundraising whole loop: `galyarder-cfo-coo`
- pitch deck: `pitch-deck`
- investor targeting: `investor-research`
- fundraising emails: `fundraising-email`
- data room: `data-room`
- board/investor update: `board-update`
- accelerator: `accelerator-application`

### Finance / Ledger / Financial Modeling

Route by posture.

#### Keiya/default finance assistant route

Use when Galih asks for practical finance help without explicit Ledger/HQ product framing.

Example request:

> “bantuin financial modeling dari data ini dong”

Route:

```text
galyarder-specialist -> galyarder-financial-services-pack -> financial-analyst -> files/Python/Google Workspace -> model/memo draft
```

- primary skill: `galyarder-financial-services-pack`
- support skill: `financial-analyst`
- optional support: `accounting`, `google-workspace`, `powerpoint`, `pdf`
- artifact: `.xlsx` model, memo, model audit checklist, or deck exhibit
- approval gate: no external send/share/writeback without approval
- verification: source list, formulas-over-hardcodes, assumptions tab, checks tab, sanity checks

#### Galyarder Ledger/HQ product route

Use when the finance request is about Galyarder Ledger, HQ, product workflows, state, approval, audit trail, or company operating system.

Route:

```text
galyarder-specialist -> galyarder-financial-services-workflows -> financial-analyst/accounting -> Ledger/HQ state artifact
```

- primary skill: `galyarder-financial-services-workflows`
- support skills: `financial-analyst`, `accounting`, `galyarder-cfo-coo`
- artifact: workflow spec, evidence schema, approval state machine, reconciliation/audit report, model artifact
- approval gate: ledger posting, budget changes, external finance material, tax/accounting decisions
- verification: evidence IDs, source citations, state transitions, rollback path, audit trail

If `galyarder-financial-services-workflows` is not available in the active skill loader, fall back to `galyarder-financial-services-pack` and explicitly preserve Ledger/HQ state requirements from project context.

### Growth / Marketing / Sales

Use for acquisition, SEO, copy, campaigns, CRO, retention, pricing, revenue strategy, and sales support.

Primary skills:

- strategy: `growth-strategist` or `marketing`
- copy: `copywriting`
- SEO: `seo`, `seo-audit`, `seo-audit`, `seo-audit`
- CRO: `cro`, `onboarding-cro`, `conversion-engineer`
- social: `copywriting`, `copywriting`
- revenue/pricing: `growth-strategist`, `accounting`
- sales: `sales-engineer`
- retention: `growth-strategist`

### Legal / Compliance / Security

Use for contracts, privacy, GDPR, licensing, compliance, threat/security review, cloud security, and offensive security only when authorized.

Primary skills:

- legal docs: `legal`, `legal-advisor`, `legal-counsel`
- contract review: `legal-counsel`
- TOS/privacy: `legal-tos-privacy`
- GDPR/privacy: `legal-tos-privacy`, `legal-tos-privacy`
- licensing: `legal-counsel`
- security review: `security-guardian`, `security-guardian`
- cloud security: `cloud-security`
- pentest/red-team authorized only: `cybersecurity`, `perseus`, red-team execution skills

### DevOps / Reliability / FinOps

Use for deployments, CI/CD, SRE, release, cost optimization, and operational reliability.

Primary skills:

- deploy/CI: `deploy`, `devops-engineer`
- SRE: `sre`
- release: `release`, `deploy`
- FinOps: `finops`, `finops-manager`, `saas-finops-optimization`
- webhook/event automation: `watchers`

### Knowledge / Docs / Productivity

Use for documents, notes, Google Workspace, Obsidian, PDFs, OCR, Notion, NotebookLM, and knowledge base work.

Primary skills/tools:

- Google Workspace: `google-workspace`
- Obsidian: `obsidian`, `obsidian`, `obsidian`, `obsidian`, `obsidian`
- archive raw intake: `saryn-archive`
- PDFs/OCR: `pdf`, `pdf`
- presentations: `powerpoint`
- NotebookLM: `notebooklm-mcp-cli`
- Notion: `notion`

### Personal / Self / Keiya

Use when Galih is asking about himself, relationships, memory, becoming, risk, or Keiya presence.

Primary skills:

- presence/memory: `keiya-presence-memory`
- playful non-explicit: `keiya-presence-memory`
- second brain: `saryn-archive`
- doctrine decision: `draith-doctrine-check`
- relationships: `keiya-presence-memory`
- becoming/habits: `draith-doctrine-check`
- risk/fear: `draith-doctrine-check`

## Example Routes

### “bantuin financial modeling dari data ini dong”

- problem type: finance modeling
- posture: Keiya/default assistant unless the user says Ledger/HQ/Galyarder product
- domain folder: finance-legal
- primary skill: `galyarder-financial-services-pack`
- support skills: `financial-analyst`; maybe `google-workspace` or `pdf`
- native tools: read file, spreadsheet/Python, Google Workspace if needed
- artifact: `.xlsx` model + assumptions/checks + short summary
- approval gate: no external send/share/writeback
- verification: formulas, source citations, assumptions tab, checks tab

### “design finance workflow buat Galyarder Ledger”

- problem type: product-native finance workflow
- posture: Galyarder
- domain folder: galyarder-framework + finance/legal
- primary skill: `galyarder-financial-services-workflows`
- support skills: `galyarder-execution-doctrine`, `galyarder-cfo-coo`
- artifact: Ledger workflow/state spec + approval/audit model
- approval gate: ledger posting, budget/tax/accounting decisions
- verification: state transitions, evidence model, rollback path

### “bikin campaign marketing buat launch”

- problem type: growth/marketing
- posture: Galyarder
- primary skill: `growth-strategist` or `marketing`
- support skills: `copywriting`, `copywriting`
- artifact: campaign brief + channel writing-plans + copy drafts
- verification: target, offer, CTA, distribution, metrics

### “fix bug Hermes gateway”

- problem type: engineering/debugging
- posture: Galyarder
- primary skill: `hermes` then `galyarder-execution-doctrine`
- support skills: `galyarder-execution-doctrine`
- native tools: terminal, read_file, search_files, patch, tests/logs
- artifact: diff + root cause + verification output

## Common Mistakes

1. **Loading every skill.**
   Routing should pick the smallest effective path.

2. **Treating folders as skills.**
   Domain folders organize skills; the agent still needs exact `skill_view(name)` calls.

3. **Confusing Keiya/default with Galyarder/product-native.**
   Keiya can be a flexible assistant. Galyarder needs artifacts, state, approvals, and verification.

4. **Using finance assistant skill for Ledger/HQ architecture without state mapping.**
   Practical modeling and product-native financial workflow are different layers.

5. **Using Galyarder doctrine for fragile emotional moments.**
   If Galih is depleted, receive him first; do not lead with business pressure.

6. **Skipping native tools.**
   If a file, Google doc, repo, browser, or system state can be checked, check it before claiming.

## Verification Checklist

Before finishing a routed Galyarder task:

- [ ] Posture selected correctly: Keiya, Galyarder, or sequence.
- [ ] Domain folder identified.
- [ ] One primary skill named exactly.
- [ ] No more than two support skills unless justified.
- [ ] Native tools identified and used where needed.
- [ ] Artifact shape defined.
- [ ] Approval gate defined for risky work.
- [ ] Verification criteria defined and executed before completion claims.
