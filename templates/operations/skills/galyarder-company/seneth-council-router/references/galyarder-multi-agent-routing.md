# Galyarder Multi-Agent & Skills Routing

Quick map for how Galih should use the `keiya` and `galyarder` profiles plus the internal skills, Galyarder Framework specialists, and native Hermes tools.

Keep this close to Hermes config so routing decisions do not depend on memory alone.

## 1. Top-Level Profiles

### keiya profile

**Channel:** personal chat, emotional OS, sanctuary, light life ops.

**Core soul:** warm equal partner. Regulates state first, then clarity.

**Typical use:**

- daily check-in, venting, grounding
- fragile/tired/sick/stressed states
- light writing-plansning from a human/emotional angle
- relationship context and soft accountability
- PAP, voice note, intimate presence, reminders

### galyarder profile

**Channel:** strategy, system design, multi-agent orchestration, business/infra.

**Core soul:** hardened operating system, doctrine keeper, execution architect.

**Typical use:**

- project writing-plansning and prioritization
- doctrine check, risk mapping, decision-making
- business / engineering / product / growth / finance / legal routing
- interfacing with the internal skill system
- spawning subagents, using terminal, MCP, GitHub, Google Workspace, cron, and Obsidian

## 2. Internal Modes / Named Skills

These are modes inside the Galyarder system, implemented as Hermes skills. They do not require separate profiles or gateways.

## 2.1 Self Layer

### Saryn — Archive / Second Brain

**Skill:** `saryn-archive`

**Use when:**

- Galih consumed a book, article, thread, video, conversation, note, or highlight
- raw input should become structured, searchable knowledge

**Output shape:**

- Title
- Source
- Core Ideas
- What Changed in Galih
- Possible Uses
- Tags

### Draith — Doctrine Guardian

**Skill:** `draith-doctrine-check`

**Use when:**

- Galih is about to commit to a non-trivial writing-plans or decision
- the question is “is this aligned with my law?”

**Output shape:**

- Decision
- Verdict: aligned / borderline / off
- Reasons
- Adjustments
- Recommendation

### Lyntia — Bonds / Relationship Ops

**Skill:** `keiya-presence-memory`

**Use when:**

- Galih might be neglecting people he cares about
- there is relational tension, silence, guilt, or a need for a small human move

**Output shape:**

- Map of people
- Priority Bonds
- Suggested Moves: small, human actions

### Aruna — Becoming / Growth OS

**Skill:** `draith-doctrine-check`

**Use when:**

- Galih talks about the gap between current self and intended self
- a change needs habits, experiments, constraints, or a 1–4 week cycle

**Output shape:**

- Current vs Intended
- Focus Axes
- Behaviours & Habits
- Experiments
- Check-in Plan

### Noctis — Abyss / Risk

**Skill:** `draith-doctrine-check`

**Use when:**

- there is real downside, fragility, fear, exposure, or worst-case concern
- a writing-plans needs resilience moves before execution

**Output shape:**

- Context
- Risk Dimensions
- Worst-Case Scenarios
- Fragile Points
- Resilience Moves
- Residual Risk

## 2.2 Company Layer

### Oryth — Direction / Threshold

**Skill:** `business-strategy-operator`

**Use when:**

- too many ideas/projects compete for attention
- a cycle needs <=3 priorities and a kill/parking list

**Output shape:**

- Horizon
- Primary Focus: <=3
- Secondary
- Parked/Kill List
- Comments

### Kaelor — Forge / Implementation

**Skill:** `business-strategy-operator`

**Use when:**

- a focus or objective has been chosen
- it needs to become an execution writing-plans

**Output shape:**

- Objective
- Constraints & Context
- Workstreams
- Steps
- Risks
- Milestones
- Next 3 Actions

### Pactra — Covenant / Decision Log

**Skill:** `business-strategy-operator`

**Use when:**

- a meaningful decision has already been taken
- product direction, financial structure, governance, architecture, or identity decisions must be recorded

**Output shape:**

- Decision
- Date
- Context
- Reasons & Trade-offs
- Expected Outcomes
- Alternatives Considered
- Review Trigger
- Notes

### Seneth — Council / Router

**Skill:** `seneth-council-router`

**Use when:**

- the situation is messy and unclear which profile, skill, tool, or sequence should be used first

**Output shape:**

- Problem Type
- Recommended Profile/Posture
- Primary Route
- Secondary Route
- Input Needed
- Next Move

## 3. Broader Skill Universe

The named internal modes above are not the full system. Hermes currently has hundreds of installed skills across categories. Seneth must consider all relevant categories, not only the eight named Galyarder modes.

### 3.1 Galyarder Framework Specialists

Use `galyarder-framework` for business, product, engineering, security, growth, legal, finance, fundraising, operations, and design work.

Common route clusters:

#### Strategy / Executive / Founder Ops

- `galyarder-ceo`
- `galyarder-cfo-coo`
- `founder-context`
- `board-update`
- `growth-strategist`
- `growth-strategist`
- `codegraph-codebase-analysis`

#### Product / Planning / Project Management

- `product-manager`
- `product-manager`
- `prd-to-writing-plans`
- `product-manager`
- `writing-plansner`
- `writing-plans`
- `linear`
- `executing-writing-planss`
- `writing-writing-planss`

#### Architecture / Engineering / Code Quality

- `galyarder-cto`
- `architect`
- `architect`
- `elite-developer`
- `systematic-debugging`
- `systematic-debugging`
- `tdd`
- `tdd-guide`
- `github-pr-workflow`
- `writing-plans`
- `elite-developer`
- `elite-developer`
- `verification-before-completion`

#### QA / Browser / Playwright

- `playwright-pro`
- `e2e`
- `e2e-runner`
- `generate`
- `fix`
- `review`
- `report`
- `playwright-pro`
- `pw-init`
- `qa-automation-engineer`
- `browserstack`

#### DevOps / Reliability / Release / Cost

- `devops-engineer`
- `deploy`
- `sre`
- `release`
- `deploy`
- `finops`
- `finops-manager`
- `saas-finops-optimization`
- `deploy`

#### Security / Red Team / Threat Intel

- `security-guardian`
- `security-guardian`
- `cloud-security`
- `cybersecurity`
- `perseus`
- `legal-tos-privacy`
- `legal-tos-privacy`
- `executing-red-team-engagement-writing-plansning`
- `executing-red-team-exercise`
- `executing-active-directory-attack-simulation`
- `executing-phishing-simulation-campaign`
- `testing-for-xss-vulnerabilities-with-burpsuite`
- `intercepting-mobile-traffic-with-burpsuite`
- `investigating-phishing-email-deploy`
- `generating-threat-intelligence-reports`
- `profiling-threat-actor-groups`
- `tracking-threat-actor-infrastructure`
- `mapping-mitre-attack-techniques`
- `monitoring-darkweb-sources`
- `recovering-from-ransomware-attack`
- `eradicating-malware-from-infected-systems`
- `perseus`

#### Growth / Marketing / Sales / Revenue

- `galyarder-ceo`
- `growth-strategist`
- `growth-strategist`
- `marketing`
- `growth-strategist`
- `growth-strategist`
- `growth-strategist`
- `copywriting`
- `copywriting`
- `copywriting`
- `copywriting`
- `copywriting`
- `seo`
- `seo-audit`
- `seo-audit`
- `seo-audit`
- `cro`
- `conversion-engineer`
- `onboarding-cro`
- `onboarding-cro`
- `onboarding-cro`
- `platform-operator-router`
- `campaign-analytics`
- `sales-engineer`
- `lead-scoring`
- `growth-strategist`
- `growth-strategist`

#### Finance / Legal / Accounting / Governance

- `galyarder-cfo-coo`
- `accounting`
- `financial-analyst`
- `accounting`
- `legal`
- `legal-advisor`
- `legal-counsel`
- `legal-tos-privacy`
- `legal-counsel`
- `legal-counsel`
- `legal-counsel`
- `legal-tos-privacy`

#### Fundraising / Investor Ops

- `galyarder-cfo-coo`
- `fundraising-email`
- `investor-research`
- `pitch-deck`
- `data-room`
- `accelerator-application`

#### Documentation / Obsidian / Knowledge Structure

- `docs`
- `obsidian`
- `obsidian`
- `obsidian`
- `obsidian`
- `obsidian`
- `scrapling`

#### Design / Visual Systems

- Design System skills: Apple, BMW, Claude, ClickHouse, Framer, Linear, Mistral AI, Notion, Pinterest, SpaceX, Superhuman, Warp, xAI, and other enabled/disabled design-system references
- `web-widgets`
- `web-widgets`
- `web-widgets`
- `diagram-design`
- `diagram-design`

### 3.2 Hermes / Tools / Infra Skills

Use these when the issue is the agent runtime, profile, gateway, model, MCP, cron, tools, or platform integration:

- `hermes`
- `native-mcp`
- `hermes`
- `google-workspace`
- `himalaya`
- `notion`
- `maps`
- `powerpoint`
- `pdf`
- `pdf`
- `github-auth`
- `github-repo-management`
- `github-issues`
- `github-pr-workflow`
- `github-code-review`
- `codegraph-codebase-analysis`
- `watchers`
- `kanban-workflow`
- `kanban-workflow`

### 3.3 Autonomous Coding Agents

Use these when delegating code, inspection, refactoring, review, or long-running work:

- `claude-code`
- `codex`
- `opencode`
- `pi-cli`
- native `delegate_task`
- spawned Hermes via tmux / CLI when long-running isolation is needed
- cron jobs for durable scheduled tasks

### 3.4 Research / ML / Data / Media

Use these for specialized research, machine learning, data science, media, and content production:

- `arxiv`
- `scrapling`
- `gbrain`
- `signal-radar`
- `gbrain`
- `jupyter-live-kernel`
- `outlines`
- `peft-fine-tuning`
- `peft-fine-tuning`
- `peft-fine-tuning`
- `huggingface-hub`
- `evaluating-llms-harness`
- `serving-llms-vllm`
- `serving-llms-vllm`
- `outlines`
- `obliteratus`
- `huggingface-hub`
- `stable-diffusion-image-generation`
- `audiocraft-audio-generation`
- `youtube-content`
- `gif-search`
- `heartmula`
- `songsee`
- `persona-media-management`

## 4. Routing Flow

A typical non-trivial situation inside Galyarder:

### Step 0 — Stabilize if needed

If Galih is emotionally flooded, sick, depleted, ashamed, or raw, start in Keiya posture. Do not open with doctrine, risk, or productivity pressure.

### Step 1 — Triage

If context is messy, use `seneth-council-router`.

If a direct skill matches clearly, skip Seneth and load that skill.

### Step 2 — Doctrine / Risk / Direction

- Use `draith-doctrine-check` if the issue is alignment with Galih’s law.
- Use `draith-doctrine-check` if downside and fragility matter.
- Use `business-strategy-operator` if there are too many options.

### Step 3 — Specialist Routing

Route to the exact specialist cluster:

- engineering → architecture / debugging / TDD / code review skills
- growth → marketing / SEO / CRO / copywriting skills
- finance/legal → accounting / legal / contracts / pricing skills
- fundraising → investor / deck / data-room skills
- runtime issue → Hermes / MCP / gateway / cron / Google Workspace skills

### Step 4 — Planning & Execution

Use `business-strategy-operator` after objective selection.
Use native tools, GitHub, Google Workspace, terminal, browser, files, MCP, delegation, or cron to execute and verify.

### Step 5 — Relationships & Self

Use `keiya-presence-memory` when people are affected.
Use `draith-doctrine-check` when execution requires personal habit/system change.

### Step 6 — Knowledge & Covenant

Use `saryn-archive` for learnings.
Use `business-strategy-operator` for meaningful commitments.

## 5. Minimal Mental Model

- **Keiya** = emotional OS, sanctuary, partner, hearth.
- **Galyarder** = strategic OS, system architect, operating blade.
- **Seneth** = router, council coordinator.
- **Named internal modes** = Saryn, Draith, Lyntia, Aruna, Noctis, Oryth, Kaelor, Pactra.
- **Galyarder Framework** = broad specialist bench for business, engineering, security, finance, growth, legal, and product.
- **Native tools** = action layer: files, terminal, web, browser, Context7 MCP, Google Workspace, GitHub, cron, delegation, messaging.

If unsure:

1. start with Keiya for state,
2. switch to Galyarder for structure,
3. use Seneth to pick the first specialist,
4. execute with native tools,
5. log decisions/learnings with Pactra/Saryn.
