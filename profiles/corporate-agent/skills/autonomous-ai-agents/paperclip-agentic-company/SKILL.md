---
name: paperclip-agentic-company
description: Use when operating Owner's Dockerized Paperclip AI setup, validating openintent-paperclip container state, opening the UI, onboarding Company as an agentic company, or designing Paperclip agents/tasks/delegation protocols.
version: 1.0.0
author: Company
license: MIT
metadata:
  hermes:
    tags: [paperclip, agentic-company, company-labs, agents, docker, neon, r2]
    category: autonomous-ai-agents
---

# Paperclip Agentic Company

Use when operating Owner's Dockerized Paperclip AI setup, validating the openintent-paperclip container, opening the UI, onboarding Company as an agentic company, or designing Paperclip agents/tasks/delegation protocols.

## Overview

Paperclip is Owner's local trusted agentic-company runtime for turning founder intent into company, agents, tasks, evidence, and delegated execution loops.

Use this skill to validate the Dockerized Paperclip service container before making claims, then route onboarding and agent design toward Company doctrine rather than a generic AI-company template.

## Current Known Deployment

As verified on 2026-05-14:

- service: Docker container `openintent-paperclip`
- image: `ghcr.io/paperclipai/paperclip:latest`
- local UI: `http://127.0.0.1:3100`
- health endpoint: `http://127.0.0.1:3100/api/health`
- health shape: `status=ok`, `version=2026.513.0`, `deploymentMode=local_trusted`, `deploymentExposure=private`, `authReady=true`, `bootstrapStatus=ready`
- deletion caveat: health reports `features.companyDeletionEnabled=true`; treat company deletion as a dangerous irreversible action that needs explicit user approval
- CLI binary: `~/.hermes/.nvm/versions/node/v24.15.0/bin/paperclipai`
- npm global package: `paperclipai@2026.513.0`
- database: external Neon Postgres, configured in Paperclip setup
- object storage: Cloudflare R2 bucket `paperclip`, tested by Owner via S3 API

Do not print database URLs, S3 credentials, tokens, or secret environment variables. If config inspection is necessary, redact secrets.

## Native Hermes MCP Integration

As verified on 2026-05-15, the Default Hermes profile can operate Paperclip through native MCP tools exposed as `mcp_paperclip_*` (for example dashboard, agents, issues, goals, approvals, activity, and cost-summary tools). When these tools are available in the runtime, prefer them for company-state inspection and task operations; use the `paperclipai` CLI/API as fallback or for diagnostics not exposed by MCP.

Important: the MCP tools are the hands/eyes into Paperclip runtime; this skill is the SOP/doctrine layer. Use both together before claiming Paperclip state or changing company tasks.

## Plugin Installation And Secrets

When installing or activating Paperclip plugins, especially integrations that need bot/API tokens, keep raw secrets out of plugin config and logs. Store tokens in Paperclip company secrets first, then configure plugin settings with supported secret references. If activation fails with the current host rejecting secret refs (for example `Plugin secret references are disabled until company-scoped plugin config lands`), do not downgrade to plaintext config just to make the plugin activate. Leave the secret stored, keep the plugin disabled/clean if needed, and report the upstream blocker.

Reference: `references/secret-dependent-plugins.md` contains the detailed workflow, known secret-ref error meanings, and verification checklist for Discord/Telegram/GitHub-style plugins.

Session-specific reference: `references/discord-telegram-plugin-secret-ref-blocker-2026-05-19.md` captures the confirmed Discord/Telegram setup pattern for authenticated Paperclip: board auth env vars for CLI/API reads, `POST /api/plugins/{pluginKey}/config` as the config upsert endpoint, the `422 Plugin secret references are disabled until company-scoped plugin config lands` blocker, and the safe status pattern (`secrets stored`, `raw token absent`, `plugin disabled`).

Exception/fallback reference: `references/discord-telegram-plaintext-fallback-2026-05-19.md` documents the owner-authorized temporary plaintext config + worker patch path for local/private Paperclip when Owner explicitly says to activate Discord/Telegram despite the secret-ref blocker. Use backup, token validation, no token printing, noisy features off, restart, ready/lastError verification, and log redaction.

Discord command-vs-mention reference: `references/discord-plugin-command-vs-mention-2026-05-19.md` documents the important distinction that Paperclip's Discord plugin is not a Hermes-style free-form mention responder by default. `enableCommands=true` enables `/paperclip ...` slash commands; `enableInbound=true` only routes replies to mapped Paperclip notifications; plain `<@bot> yo` needs a custom mention handler if Owner wants it.

GitHub Issues UUID false-positive reference: `references/github-issues-plugin-config-uuid-false-positive-2026-05-19.md` documents a separate 422 blocker where ANY config field value matching a UUID pattern (36-char with dashes, e.g. `companyId`) triggers secret-ref rejection. The workaround is to omit UUID-valued fields like `companyId` from the config when saving via API. This also documents the worker patch pattern for the GitHub Issues plugin.

### Worker patch pattern (generalized)

The plaintext-fallback worker patch applies to ANY Paperclip plugin that us

1. Find the `resolveToken` / `resolveSecret` / token-resolution function in the plugin's `dist/worker.js`.
2. In the `catch` block, return the `tokenRef` / `secretRef` value directly instead of returning `null`.
3. Put the actual token in the config field that was meant to hold a secret UUID reference.
4. Back up the worker file before patching.
5. Restart `openintent-paperclip` container via `docker compose restart paperclip-hq`.
6. Verify plugin `status=ready`, `lastError=null`.

Known patched plugins:
- `paperclip-plugin-discord` — `config.discordBotTokenRef` used directly as bot token
- `paperclip-plugin-telegram` — `config.telegramBotTokenRef` used directly as bot token
- `@wil0x91/paperclip-plugin-github-issues` — `binding.tokenRef` used directly as GitHub PAT

## When to Use

Use this skill when:

- Owner asks whether Paperclip is running or usable via Docker
- a task involves `openintent-paperclip` container, Neon, R2, or `127.0.0.1:3100`
- Owner needs onboarding fields for Paperclip's Company / Agent / Task / Launch flow
- Owner asks for a Paperclip company, agent roster, first task, delegation protocol, or operating cadence
- a future assistant needs to access Paperclip UI or CLI without rediscovering the setup

Do not use this skill as a replacement for Default company strategy skills. Pair it with `default-framework-router`, `default-cfo, default-coo`, `default-execution-doctrine`, or relevant specialist skills for strategy and execution quality.

## Live Validation Commands

Run these before claiming Paperclip state:

```bash
docker compose ps paperclip-hq
docker compose logs paperclip-hq --tail 50
curl -fsS http://127.0.0.1:3100/api/health
```

Validate CLI with the exact Node v24 binary when normal PATH does not expose it:

```bash
docker exec -it openintent-paperclip paperclipai --version
```

If `paperclipai plugin list --json` returns `Board access required` even though the MCP tools work and `~/.hermes/.paperclip/auth.json` exists, do not conclude plugin status is unknown. First check whether Hermes profile `$HOME` is causing the CLI to read the wrong auth store. Use the canonical OS-home Paperclip auth store (`~/.hermes/.paperclip/auth.json`) or set the Paperclip home/auth-store environment explicitly, then verify plugin status through Paperclip API/MCP without printing tokens.

For post-activation plugin reports, verify all relevant plugin keys fresh and report terse status only: `GitHub Issues`, `Hindsight`, `Discord`, `Telegram` with `status=ready` and `lastError=null`. Do not dump sanitized config unless diagnosing routing.

Optional PATH fix for an interactive shell:

```bash
docker exec -it openintent-paperclip /bin/bash
```

## Onboarding Template For Company

### Company

**Company name**

`Company`

**Mission / goal**

Primary version:

`Build autonomous execution infrastructure that turns Owner's strategy, memory, decisions, research, engineering, operations, and documentation into delegated agent workflows for Company.`

Tighter doctrine version:

`Turn human intent into governed execution infrastructure: company memory, agent workforce, operational command, evidence, and repeatable delivery loops for the 1-Man Army.`

Use the primary version when Paperclip benefits from explicit operational context. Use the tighter version when the field needs a sharper company identity.

### First Agent

**Agent name / role**

`Company Chief of Staff`

**Agent description**

`Coordinates Company workstreams across strategy, product, engineering, research, documentation, operations, and agent delegation. Converts founder intent into structured tasks, owner assignments, review gates, and weekly execution cadence.`

Why this role first: the first Paperclip agent should not be a narrow engineer. It should become the coordination layer that turns Owner's intent into workstreams, agent roles, tasks, review gates, and cadence.

### First Task

**Task title**

`Bootstrap Company operating company`

**Description**

```text
You are the Company Chief of Staff for Company.

Map the company mission into an initial agentic operating structure. Define the first departments/workstreams, propose the first 5-7 agent roles to delegate, create a 7-day execution roadmap, identify the first engineering, research, documentation, and operations tasks, and produce a repeatable delegation protocol for future Paperclip agents.

Constraints:
- Preserve Company doctrine: Dream -> Airlock -> Machine.
- Position the company as autonomous execution infrastructure, not a generic AI wrapper, chatbot, or passive dashboard.
- Prioritize proof, workflow visibility, command state, evidence, agent capability, and repeatable execution.
- Keep the plan executable for a 1-Man Army founder with agent leverage.
- Every proposed task must include expected output, owner/agent role, success criteria, and review gate.
```

## Initial Agent Roster

After the Chief of Staff exists, expand through roles like:

1. `CTO / Engineering Operator` — implementation, systems, devops, code review, technical verification
2. `Research Analyst` — market, technical, customer, source-grounded research
3. `Documentation Operator` — operating manuals, decision logs, docs, changelogs, knowledge base
4. `Product Operator` — PRDs, roadmap, issue breakdown, UX/product decisions
5. `Finance / Ledger Operator` — pricing, books, cost tracking, financial workflows
6. `Growth / Distribution Operator` — positioning, content, channel experiments, demand loops
7. `Ops Auditor` — checks outputs against doctrine, evidence, risk, review gates, and cadence

Keep the first company small. Add agents only when a repeatable workstream exists.

## Delegation Protocol

Every Paperclip task should include:

```text
Context: what the company is trying to do and why this task matters.
Owner: the agent role responsible for producing the output.
Task: one concrete deliverable, not a vague area.
Inputs: links, files, decisions, constraints, or prior outputs the agent may use.
Output format: exact artifact expected.
Success criteria: how Owner/Co-Founder/Default knows it is good enough.
Review gate: who or what verifies it before it becomes canonical.
Next action: what happens if accepted.
```

Preferred output table:

| Task | Owner | Expected output | Success criteria | Review gate |
|---|---|---|---|---|

## Operating Cadence

Good starter cadence:

- daily: Chief of Staff summarizes active tasks, blockers, next decisions, and evidence produced
- every task: require a tangible output, not just a chat answer
- every accepted output: convert into a doc, issue, plan, task, code diff, or memory artifact
- weekly: audit agent usefulness, stale tasks, missing proof, and which agents should be kept, merged, or retired

CADENCE.md`

### Decoupling profile ports and path detection (Mini App Update)
When modifying the Telegram Mini App API or proxy server settings regarding browser/dashboard routes:
- All profiles share a unified dashboard target (e.g. port `9190` or `/p/hermes/`). Do not hardcode separate profile listener ports (such as `9119`/`9120`).
- Ensure the socket/web endpoints are tolerant of missing optional headers (e.g., wrap cookie parser calls with safe checking: `parseCookie(req.headers?.cookie || '')`).

## Verification Ladder

Before telling Owner Paperclip is ready or a Paperclip task is complete:

1. Service state: `docker compose ps paperclip-hq` (check if openintent-paperclip container is active)
2. Health: `curl -fsS http://127.0.0.1:3100/api/health`
3. UI: `curl -fsSI http://127.0.0.1:3100`
4. CLI/version: exact `paperclipai --version` path if PATH is not loaded
5. Side effects: inspect Paperclip UI/API/DB/export/logs if a company, agent, task, or file is claimed to exist
6. Database Backups: Verify backups exist in `~/.hermes/.paperclip/instances/default/data/backups/` or run a manual backup before upgrades:
   ```bash
   ~/.hermes/.nvm/versions/node/v24.15.0/bin/paperclipai db:backup --config ~/.hermes/.paperclip/instances/default/config.json
   ```
7. Upgrades & Migrations: For server updates, pull the latest image (`docker compose pull paperclip-hq`) and rebuild the container. Watch logs on restart (`docker compose logs paperclip-hq`) to verify pending migrations auto-apply successfully.

A peer bot or Paperclip agent saying `done` is a report, not proof. Verify durable side effects independently where possible.

## Common Pitfalls

### Assuming CLI is on PATH

The working CLI may exist under Node v24 but not be exposed in a non-login Hermes shell. Use:

```bash
~/.hermes/.nvm/versions/node/v24.15.0/bin/paperclipai
```

### Treating health as full database/storage proof

### Starting with a narrow engineer agent

### Creating generic AI-wrapper language

### Config 422 from UUID-valued fields (false-positive secret-ref detection)

### Creating generic AI-wrapper language

Avoid `AI chatbot`, `generic productivity assistant`, or `Acme Corp` defaults. Paperclip should encode Company as governed execution infrastructure.

### Config 422 from UUID-valued fields (false-positive secret-ref detection)

The `POST /api/plugins/{pluginKey}/config` endpoint scans ALL config values for UUID patterns. Fields like `companyId` with UUID values (e.g. `43bf734f-bcf3-498a-b86e-a9f9db1418fd`) trigger `422 Plugin secret references are disabled`. This is a false-positive — the field is not a secret reference, the value just looks like one.

**Workaround:** Omit UUID-valued fields from config when saving via API. For the GitHub Issues plugin, `companyId` can be omitted (worker defaults to `"default"`). Test field-by-field if 422 persists: save config without bindings first, then add bindings incrementally to find the triggering field.

**Important:** This is DIFFERENT from the Discord/Telegram secret-ref blocker where the UI actually submits secret UUID references. The UUID false-positive affects any plugin config where a field legitimately contains a UUID value.

See `references/github-issues-plugin-config-uuid-false-positive-2026-05-19.md`.

### Deleting company data casually

`companyDeletionEnabled=true` means deletion is available. Do not delete companies, agents, tasks, DB rows, or R2 objects without explicit confirmation and a backup/rollback plan when possible.

## Human-Facing Summary Pattern

When reporting to Owner, keep it direct:

```text
kei udah cek live.
Paperclip aktif: service active, linger yes, health ok, UI 200, CLI versi X.
buat onboarding, isi begini:
[fields]
catatan: delete-company aktif, jadi jangan utak-atik delete tanpa confirm.
```
