# V2.1 Skill Noise / Stale Audit — Galyarder Profile Normalized

## Scope

- Scanned `/home/galyarder/.hermes/profiles/galyarder/skills` recursively after non-destructive folder normalization.
- Active profile skills: **117**.
- Top-level categories: **24**.
- Exact duplicate skill names: **0**.
- Bad frontmatter: **0**.
- Archived outside active skills tree: **1**.
- Category moves applied: **124**.

## Decision

No skills were deleted. No SKILL.md `name:` values were renamed. No active skill content was edited as part of the folder move itself. One previously active `.archive` skill and curator backup artifacts were moved outside `/skills/` so the loader no longer treats archive material as active inventory.

Finalization remains non-destructive: keep broad inventory, route through Core Daily Pack, and treat noisy/reference families as opt-in. Any future delete/disable action still requires explicit Galih approval.

## Exact duplicate skill names

- None.

## Likely overlap / consolidation families

These are not errors. They are families that need router preference rules instead of deletion.

### testing / QA / TDD — 46 candidates

- `onboarding-cro` (growth) — Use when setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness.
- `benchmark` (gstack-suite) — Performance regression detection using the browse daemon. Establishes baselines for page load times, Core Web Vitals, and resource sizes. Compares before/after on every PR. Tracks 
- `browse` (gstack-suite) — Fast headless browser for QA testing and site dogfooding. Navigate any URL, interact with elements, verify page state, diff before/after actions, take annotated screenshots, check 
- `browser-routing` (browser) — Use when choosing configuring or troubleshooting which browser stack should handle a task across Brave CDP Hermes native browser Camofox gstack Playwright BrowserOS or cloud browse
- `browserstack` (qa-testing) — Use when user mentions "browserstack", "cross-browser", "cloud testing", "browser matrix", "test on safari", "test on firefox", or "browser compatibility".
- `build-fix` (software-development) — Use when a build, typecheck, test, or CI failure must be investigated and fixed with a small verified change.
- `playwright-pro` (qa-testing) — Use when user says "test playwright-pro", "what's not tested", "playwright-pro gaps", "missing tests", "playwright-pro report", or "what needs testing".
- `cso` (gstack-suite) — Chief Security Officer mode. Infrastructure-first security audit: secrets archaeology, dependency supply chain, CI/CD pipeline security, LLM/AI security, skill supply chain scannin
- `design-review` (gstack-suite) — Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. Iteratively fixes issues in source cod
- `devex-review` (gstack-suite) — Live developer experience audit. Uses the browse tool to actually TEST the developer experience: navigates docs, tries the getting started flow, times TTHW, screenshots error messa
- `dogfood` (dogfood) — Exploratory QA of web apps: find bugs, evidence, reports.
- `e2e` (qa-testing) — Use when running, debugging, or validating end-to-end tests and browser automation flows.
- `e2e-runner` (qa-testing) — Use when executing Playwright or browser E2E suites, collecting failures, and producing actionable test evidence.
- `executing-active-directory-attack-simulation` (security) — Use when running authorized Active Directory attack simulations, identity-path testing, or domain security exercises.
- `elite-developer` (software-development) — Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for m
- `fix` (qa-testing) — Use when user says "fix test", "flaky test", "test failing", "debug test", "test broken", "test passes sometimes", or "intermittent failure".
- `galyarder-browser-routing` (browser) — Use when a request involves opening websites, browser choice, Brave CDP, Camofox/Camoufox, gstack/Playwright, cloud browsers, YouTube/media, logged-in accounts, auth/session automa
- `galyarder-execution-doctrine` (galyarder-framework) — Use when applying Galyarder Framework test-driven development discipline before implementation.
- `galyarder-execution-doctrine` (galyarder-framework) — Use when writing Galyarder Framework implementation writing-planss with zero-context handoff, TDD, verification, and execution discipline.
- `generate` (qa-testing) — Use when user says "write tests", "generate tests", "add tests for", "test this component", "e2e test", "create test for", "test this page", or "test this feature".
- `gstack` (gstack-suite) — Fast headless browser for QA testing and site dogfooding. Navigate pages, interact with elements, verify state, diff before/after, take annotated screenshots, test responsive layou
- `gstack-local` (devops) — Use when maintaining or using the local Garry Tan gstack install, including gstack browser automation, generated gstack skills, Claude Code specialist workflows, QA/review/ship flo
- `gstack-upgrade` (gstack-suite) — Upgrade gstack to the latest version. Detects global vs vendored install, runs the upgrade, and shows what's new. Use when asked to "upgrade gstack", "update gstack", or "get lates
- `health` (gstack-suite) — Code quality dashboard. Wraps existing project tools (type checker, linter, test runner, dead code detector, shell linter), computes a weighted composite 0-10 score, and tracks tre
- `intercepting-mobile-traffic-with-burpsuite` (security) — Use when performing mobile application penetration testing, assessing API security, or evaluating client-server communication patterns. Activates for requests involving mobile traf
- `mapping-mitre-attack-techniques` (security) — Use when building an ATT&CK-based playwright-pro heatmap, tagging SIEM alerts with technique IDs, aligning security controls to adversary playbooks, or reporting threat exposure to execu
- `playwright-pro` (qa-testing) — Use when user mentions "cypress", "selenium", "playwright-pro tests", "convert tests", "switch to playwright", "move from cypress", or "replace selenium".
- `monitoring-darkweb-sources` (security) — Use when establishing dark web monitoring playwright-pro, investigating specific data breach claims, or enriching deploy investigations with dark web context. Activates for requests in
- `perseus` (security) — Use when performing advanced authorized offensive security review, penetration testing, exploit analysis, or adversarial validation.
- `writing-plans-eng-review` (gstack-suite) — Eng manager-mode writing-plans review. Lock in the execution writing-plans — architecture, data flow, diagrams, edge cases, test playwright-pro, performance. Walks through issues interactively with opinio
- ... 16 more omitted from this reference.

### writing-plansning / PRD / strategy — 71 candidates

- `onboarding-cro` (growth) — Use when designing, auditing, or improving analytics events, funnels, attribution, dashboards, or measurement writing-planss.
- `architect` (software-development) — Use when writing-plansning system architecture, evaluating technical tradeoffs, designing scalable components, or making architectural decisions.
- `draith-doctrine-check` (galyarder-self) — Turn the gap between current and intended self into a small set of habits, experiments, and constraints for the next cycle.
- `autowriting-plans` (gstack-suite) — Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisions using 6 decision principles. Surfaces taste de
- `brainstorming` (product-management) — Use when exploring creative options, feature ideas, product directions, UX approaches, or implementation alternatives before committing to a writing-plans.
- `galyarder-cfo-coo` (galyarder-company) — Use when coordinating cross-functional work, routing decisions, filtering founder noise, turning ambiguous priorities into operating cadence, assigning owners, sequencing workstrea
- `copywriting` (growth) — Use when a user invokes 'content creator', asks to write a blog post, article, guide, or brand voice analysis (routes to content-production), or asks to writing-plans content, build a topic
- `copywriting` (growth) — Use when deciding what to publish, what topics to prioritize, or how to structure a content program.
- `context-restore` (gstack-suite) — Restore working context saved earlier by /context-save. Loads the most recent saved state (across all branches by default) so you can pick up where you left off — even across Condu
- `design-consultation` (gstack-suite) — Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color, layout, spacing, motion), and generates fo
- `design-html` (gstack-suite) — Design finalization: generates production-quality Pretext-native HTML/CSS. Works with approved mockups from /design-shotgun, CEO writing-planss from /writing-plans-ceo-review, design review context 
- `design-review` (gstack-suite) — Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. Iteratively fixes issues in source cod
- `devex-review` (gstack-suite) — Live developer experience audit. Uses the browse tool to actually TEST the developer experience: navigates docs, tries the getting started flow, times TTHW, screenshots error messa
- `draith-doctrine-check` (galyarder-self) — Evaluate a writing-plans or decision against Galih's core doctrine (freedom, mastery, legacy, integrity, family duty).
- `platform-operator-router` (growth) — Use when reviewing email setups, building automation flows, diagnosing deliverability, writing email copy, selecting platforms, or pulling Standards. Covers strategy, flows, delive
- `executing-active-directory-attack-simulation` (security) — Use when running authorized Active Directory attack simulations, identity-path testing, or domain security exercises.
- `executing-phishing-simulation-campaign` (security) — Use when writing-plansning or executing authorized phishing simulations, awareness campaigns, or email-security exercises.
- `executing-writing-planss` (software-development) — Use when you have a written implementation writing-plans to execute in a separate session with review checkpoints
- `executing-red-team-engagement-writing-plansning` (security) — Use when writing-plansning authorized red-team engagements, scoping exercises, defining rules of engagement, or mapping objectives.
- `founder-context` (galyarder-company) — Use when creating or updating canonical founder, startup, market, product, traction, or strategy context.
- `freeze` (gstack-suite) — Restrict file edits to a specific directory for the session. Blocks Edit and Write outside the allowed path. Use when debugging to prevent accidentally "fixing" unrelated code, or 
- `galyarder-ceo` (galyarder-company) — Use when making CEO-level decisions about strategy, prioritization, company direction, markets, or execution leverage.
- `galyarder-cfo-coo` (galyarder-company) — Use when making CFO/COO decisions about cash, runway, operations, risk, process, or company stability.
- `galyarder-ceo` (galyarder-company) — Use when making CMO-level decisions about positioning, distribution, demand, campaigns, brand, or growth systems.
- `galyarder-cto` (galyarder-company) — Use when making CTO-level decisions about technical architecture, tech stack, system design, infrastructure, codebase strategy, or engineering tradeoffs.
- `galyarder-execution-doctrine` (galyarder-framework) — Use when executing Galyarder Framework implementation writing-planss through isolated subagents and two-stage review.
- `galyarder-execution-doctrine` (galyarder-framework) — Use when writing Galyarder Framework implementation writing-planss with zero-context handoff, TDD, verification, and execution discipline.
- `generating-threat-intelligence-reports` (security) — Use when producing finished intelligence products from raw collection data, creating sector threat briefings, or delivering post-deploy intelligence assessments. Activates for re
- `growth-strategist` (growth) — Use when designing growth strategy, acquisition channels, SEO writing-planss, campaign direction, or demand-generation priorities.
- `guard` (gstack-suite) — Full safety mode: destructive command warnings + directory-scoped edits. Combines /careful (warns before rm -rf, DROP TABLE, force-push, etc.) with /freeze (blocks edits outside a 
- ... 41 more omitted from this reference.

### growth / marketing / CRO — 37 candidates

- `benchmark-models` (gstack-suite) — Cross-model benchmark for gstack skills. Runs the same prompt through Claude, GPT (via Codex CLI), and Gemini side-by-side — compares latency, tokens, cost, and optionally quality 
- `browser-routing` (browser) — Use when choosing configuring or troubleshooting which browser stack should handle a task across Brave CDP Hermes native browser Camofox gstack Playwright BrowserOS or cloud browse
- `browserstack` (qa-testing) — Use when user mentions "browserstack", "cross-browser", "cloud testing", "browser matrix", "test on safari", "test on firefox", or "browser compatibility".
- `campaign-analytics` (growth) — Use when analyzing marketing campaigns, ad performance, attribution models, conversion rates, or calculating marketing ROI, ROAS, CPA, and campaign metrics across channels.
- `galyarder-cfo-coo` (galyarder-company) — Use when coordinating cross-functional work, routing decisions, filtering founder noise, turning ambiguous priorities into operating cadence, assigning owners, sequencing workstrea
- `growth-strategist` (growth) — Use when creating competitor comparison pages, alternatives pages, positioning matrices, or SEO pages for competitive search intent.
- `copywriting` (growth) — Use when a user invokes 'content creator', asks to write a blog post, article, guide, or brand voice analysis (routes to content-production), or asks to writing-plans content, build a topic
- `context-restore` (gstack-suite) — Restore working context saved earlier by /context-save. Loads the most recent saved state (across all branches by default) so you can pick up where you left off — even across Condu
- `copywriting` (growth) — Use when writing or improving landing page copy, emails, ads, positioning, or conversion-focused messaging.
- `cro` (growth) — Use when optimizing conversion rate across onboarding, paywalls, signup forms, pricing pages, or activation flows.
- `cso` (gstack-suite) — Chief Security Officer mode. Infrastructure-first security audit: secrets archaeology, dependency supply chain, CI/CD pipeline security, LLM/AI security, skill supply chain scannin
- `document-release` (gstack-suite) — Post-ship documentation update. Reads all project docs, cross-references the diff, updates README/ARCHITECTURE/CONTRIBUTING/AGENTS.md to match what shipped, polishes CHANGELOG voic
- `platform-operator-router` (growth) — Use when reviewing email setups, building automation flows, diagnosing deliverability, writing email copy, selecting platforms, or pulling Standards. Covers strategy, flows, delive
- `executing-phishing-simulation-campaign` (security) — Use when writing-plansning or executing authorized phishing simulations, awareness campaigns, or email-security exercises.
- `galyarder-ceo` (galyarder-company) — Use when making CMO-level decisions about positioning, distribution, demand, campaigns, brand, or growth systems.
- `galyarder-specialist` (galyarder-framework) — Use when a Galyarder Labs request needs canonical routing across domain folders, Galyarder Framework orchestration, profile/posture choice, specialist skill selection, tool choice,
- `growth-strategist` (growth) — Use when building engineering-led growth loops, acquisition tools, SEO surfaces, referral systems, or viral mechanics.
- `growth-strategist` (growth) — Use when designing growth strategy, acquisition channels, SEO writing-planss, campaign direction, or demand-generation priorities.
- `keiya-capability-router` (galyarder-self) — Use when a Keiya/default assistant request needs routing across everyday capabilities: emotional presence, memory, PAP/selfie/media, voice notes, research, Google Workspace, browse
- `learn` (gstack-suite) — Manage project learnings. Review, search, prune, and export what gstack has learned across sessions. Use when asked to "what have we learned", "show learnings", "prune stale learni
- `marketing` (growth) — Use when writing-plansning or improving marketing strategy, SEO, copy, campaigns, positioning, or acquisition systems.
- `growth-strategist` (growth) — Use when writing-plansning marketing strategy, growth marketing, advertising campaigns, PPC optimization, lead generation, pipeline generation, or startup marketing budgets. Covers multi-ch
- `growth-strategist` (growth) — Use when generating or evaluating practical marketing ideas, growth experiments, channel tactics, or campaign concepts.
- `growth-strategist` (growth) — Use when applying behavioral science, persuasion, mental models, or conversion psychology to marketing and revenue.
- `onboarding-cro` (growth) — Use when improving onboarding flows, activation, first-run experience, product education, or user setup completion.
- `onboarding-cro` (growth) — Use when analyzing or optimizing a single page for conversion, clarity, trust, CTA performance, or funnel fit.
- `onboarding-cro` (growth) — Use when optimizing paywalls, upgrade screens, pricing prompts, writing-plans comparison, or monetization conversion.
- `writing-plans-tune` (gstack-suite) — Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). Review which AskUserQuestion prompts fire across gstack skills, set per-question preferen
- `profiling-threat-actor-groups` (security) — Use when briefing executives on sector-specific threats, updating threat model assumptions, or prioritizing defensive controls against specific adversaries. Activates for requests 
- `seo-audit` (growth) — Use when designing programmatic SEO systems, templates, indexable page strategies, or scalable organic acquisition.
- ... 7 more omitted from this reference.

### finance / legal / risk — 20 candidates

- `board-update` (galyarder-company) — Use when drafting investor updates, board reports, stakeholder briefings, or concise operating narratives with wins, misses, risks, and asks.
- `github-pr-workflow` (software-development) — Use when reviewing code changes for correctness, security, maintainability, spec compliance, and regression risk.
- `legal-counsel` (finance-legal) — Use when starting client engagements, writing proposals, drafting partnership agreements, or needing GDPR-compliant data processing addenda.
- `legal-counsel` (finance-legal) — Use when reviewing contracts for risk, unfavorable terms, obligations, negotiation points, or compliance exposure.
- `data-room` (galyarder-company) — Use when preparing, auditing, or organizing fundraising, diligence, investor, legal, financial, or company data-room materials.
- `accounting` (finance-legal) — Use when deciding whether a pricing move should ship.
- `finops-manager` (devops) — Use when managing infrastructure spend, SaaS unit economics, cloud budgets, cost governance, or finance-ops tradeoffs.
- `galyarder-cfo-coo` (galyarder-company) — Use when making CFO/COO decisions about cash, runway, operations, risk, process, or company stability.
- `galyarder-financial-services-pack` (finance-legal) — Use when Keiya/default assistant finance work needs practical financial-services workflows: financial modeling, comps, DCF, 3-statement/LBO models, investment banking drafts, equit
- `galyarder-financial-services-workflows` (galyarder-framework) — Use when handling financial-services workflows for Galyarder Labs or Ledger/HQ: financial modeling, DCF, comps, earnings review, investment banking materials, private-equity screen
- `legal-tos-privacy` (finance-legal) — Use when auditing products, websites, analytics, cookies, or data flows for GDPR, CCPA, and privacy compliance.
- `legal-tos-privacy` (finance-legal) — Use when processing EU personal data.
- `legal-tos-privacy` (finance-legal) — Use when auditing or designing AI governance systems, ISO 42001 controls, model risk processes, or AI compliance evidence.
- `business-strategy-operator` (galyarder-company) — Turn a strategic objective into a clear implementation writing-plans with milestones, constraints, risks, and next actions.
- `keiya-capability-router` (galyarder-self) — Use when a Keiya/default assistant request needs routing across everyday capabilities: emotional presence, memory, PAP/selfie/media, voice notes, research, Google Workspace, browse
- `legal` (finance-legal) — Use when drafting, reviewing, or reasoning about legal documents, compliance, terms, privacy, contracts, or liability.
- `legal-advisor` (finance-legal) — Use when needing legal-style outlines for policies, disclaimers, terms, privacy, compliance, or risk framing.
- `legal-counsel` (finance-legal) — Use when producing legal/compliance deliverables, reviewing risk, drafting policies, or advising on contractual exposure.
- `legal-tos-privacy` (finance-legal) — Use when the user needs to draft, review, or update legal documents (ToS, Terms of Service, Privacy Policy, legal pages). Triggers on requests for legal documents, terms drafting, 
- `draith-doctrine-check` (galyarder-self) — Map worst-case scenarios and structural risks for a writing-plans, then propose resilience moves without inducing paralysis.

### Hermes / runtime / agent routing — 85 candidates

- `browser-routing` (browser) — Use when choosing configuring or troubleshooting which browser stack should handle a task across Brave CDP Hermes native browser Camofox gstack Playwright BrowserOS or cloud browse
- `camofox-browser` (browser) — Use when working with Hermes Camofox/Camoufox browser automation, headless/headful Camofox windows, hidden browser audio, Camofox service health, YouTube/media playback, or the Gal
- `galyarder-cfo-coo` (galyarder-company) — Use when coordinating cross-functional work, routing decisions, filtering founder noise, turning ambiguous priorities into operating cadence, assigning owners, sequencing workstrea
- `debugging-hermes-tui-commands` (software-development) — Debug Hermes TUI slash commands: Python, gateway, Ink UI.
- `design-html` (gstack-suite) — Design finalization: generates production-quality Pretext-native HTML/CSS. Works with approved mockups from /design-shotgun, CEO writing-planss from /writing-plans-ceo-review, design review context 
- `design-system-airbnb` (design-systems) — Use when applying, referencing, or recreating the Airbnb design system inside Hermes Agent workflows.
- `design-system-airtable` (design-systems) — Use when applying, referencing, or recreating the Airtable design system inside Hermes Agent workflows.
- `design-system-apple` (design-systems) — Use when applying, referencing, or recreating the Apple design system inside Hermes Agent workflows.
- `design-system-bmw` (design-systems) — Use when applying, referencing, or recreating the BMW design system inside Hermes Agent workflows.
- `design-system-calcom` (design-systems) — Use when applying, referencing, or recreating the Cal.com design system inside Hermes Agent workflows.
- `design-system-claude-anthropic` (design-systems) — Use when applying, referencing, or recreating the Claude (Anthropic) design system inside Hermes Agent workflows.
- `design-system-clay` (design-systems) — Use when applying, referencing, or recreating the Clay design system inside Hermes Agent workflows.
- `design-system-clickhouse` (design-systems) — Use when applying, referencing, or recreating the ClickHouse design system inside Hermes Agent workflows.
- `design-system-cohere` (design-systems) — Use when applying, referencing, or recreating the Cohere design system inside Hermes Agent workflows.
- `design-system-coinbase` (design-systems) — Use when applying, referencing, or recreating the Coinbase design system inside Hermes Agent workflows.
- `design-system-composio` (design-systems) — Use when applying, referencing, or recreating the Composio design system inside Hermes Agent workflows.
- `design-system-cursor` (design-systems) — Use when applying, referencing, or recreating the Cursor design system inside Hermes Agent workflows.
- `design-system-elevenlabs` (design-systems) — Use when applying, referencing, or recreating the ElevenLabs design system inside Hermes Agent workflows.
- `design-system-expo` (design-systems) — Use when applying, referencing, or recreating the Expo design system inside Hermes Agent workflows.
- `design-system-figma` (design-systems) — Use when applying, referencing, or recreating the Figma design system inside Hermes Agent workflows.
- `design-system-framer` (design-systems) — Use when applying, referencing, or recreating the Framer design system inside Hermes Agent workflows.
- `design-system-hashicorp` (design-systems) — Use when applying, referencing, or recreating the HashiCorp design system inside Hermes Agent workflows.
- `design-system-ibm` (design-systems) — Use when applying, referencing, or recreating the IBM design system inside Hermes Agent workflows.
- `design-system-intercom` (design-systems) — Use when applying, referencing, or recreating the Intercom design system inside Hermes Agent workflows.
- `design-system-kraken` (design-systems) — Use when applying, referencing, or recreating the Kraken design system inside Hermes Agent workflows.
- `design-system-linear` (design-systems) — Use when applying, referencing, or recreating the Linear design system inside Hermes Agent workflows.
- `design-system-lovable` (design-systems) — Use when applying, referencing, or recreating the Lovable design system inside Hermes Agent workflows.
- `design-system-minimax` (design-systems) — Use when applying, referencing, or recreating the MiniMax design system inside Hermes Agent workflows.
- `design-system-mintlify` (design-systems) — Use when applying, referencing, or recreating the Mintlify design system inside Hermes Agent workflows.
- `design-system-miro` (design-systems) — Use when applying, referencing, or recreating the Miro design system inside Hermes Agent workflows.
- ... 55 more omitted from this reference.

## Router preference rules

- Route by user intent and skill trigger text first; use folder category only as first-pass grouping.
- Prefer Galyarder umbrella skills for Galyarder Labs work, then 1–2 support skills.
- Prefer specific domain skills over broad overlapping skills once the request domain is clear.
- Preserve archive material outside active `/skills/` unless Galih explicitly asks to restore it.
