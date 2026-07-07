# OpenIntent Kit (Niyatna OS Bootstrap)

OpenIntent Kit is an open-source bootstrap installer to provision, link, and orchestrate a multi-agent organizational company infrastructure. It pulls and operates official containers for Niyatna's core modules in Docker with dynamic isolation lanes, standard profile distributions, and host-bound data persistence.

---

## Architecture Components

The kit bootstraps and provisions the Niyatna architecture consisting of five core layers:

1. **Niyatna Route (`9router`)**: Port `20128`. Next.js OpenAI-compatible proxy gateway with auto-fallback and token cost optimizations (internal port maps handle headroom at `8787`).
2. **Niyatna HQ (`paperclip`)**: Port `3100`. TypeScript React dashboard for task orchestration, runtimes, and status checks (linked to an isolated PostgreSQL/PGLite database).
3. **Niyatna Memory (`hindsight` / Vector DB)**: Port `9177` (mapped from container port `8888`). Self-hosted long-term memory engine utilizing SQLite storage and local CPU embeddings.
4. **Niyatna Agents (`hermes-agent` workforce lanes)**:
   * **Operations Profile**: Port `8001` (primary coordinator, task manager, codebase/db operations).
   * **Corporate Profile**: Port `8002` (Executive lane, strategy, CMO/CFO/CEO context).
   * **Public Profile**: Port `8003` (Public interface, competitor analyst, customer support).
5. **Niyatna OS (Operating / Channel Layer)**: Direct Discord-mapped workspace linking human intent to agent executions. Orchestrated via the auto-provisioner script to build structural channels for announcements, approvals, and departments.

---

## Infrastructure Requirements

* **Minimum Host Specs**: 2 vCPU cores, 4 GB RAM.
* **Recommended Specs (VPS / Local)**: 2 vCPU cores, 12 GB RAM (Oracle Cloud Free Tier VM / standard cloud VPS).
* **System OS**: Debian 11/12 or Ubuntu 20.04/22.04 LTS.
* **Core Dependencies**: Docker Engine, Docker Compose (v2.x+), Python 3.x, and Curl.

---

## One-Command Installation (Fast Deploy)

To deploy the entire multi-agent stack on your target server instantiating Niyatna OS, execute the single command below. It performs dependency audits, extracts configurations, prompts for keys, populates databases, and prepares Docker:

```bash
curl -fsSL https://raw.githubusercontent.com/niyatna/openintent/main/install.sh | bash
```

*(Note: Replace the URL placeholder with your actual repository distribution raw endpoint once pushed.)*

After the installer completes, cd into the selected directory and run:
`docker compose up -d && ./scripts/verify.sh && ./scripts/discord_setup.py`

---

## Cascading Deployment & Provisioning Workflow

If you prefer to manually execute or review target phases:

### Step 2: Orchestrate Containers
Pull official images and start the Docker services:
```bash
docker compose pull
```
```bash
docker compose up -d
```

### Step 3: Cascading System Verification
Execute the verify utility to run multi-level network handshakes, HTTP backend response checks, and Hindsight SQLite write tests:
```bash
./scripts/verify.sh
```

### Step 4: Niyatna OS Provisioning (Discord Workspace)
Build the real-time runtime channels environment. Running this zero-dependency Python script auto-provisions categories and text channel configurations directly on your Discord server using your `DISCORD_BOT_TOKEN`:

```bash
./scripts/discord_setup.py
```

This generates the structured Niyatna OS categories layout:
* **GENERAL**: `#announcements`, `#general-discussion` (general human communications)
* **OPERATIONS**: `#hq-pulse` (hq logs), `#active-tasks` (running jobs), `#approval-gates` (secure approval gates for agent delegation), `#proof-of-intent` (evidence audit trails)
* **DEPARTMENTS**: `#operations-room` (Operations Lane), `#corporate-room` (Corporate Lane), `#public-room` (Public Lane)
* **SYSTEM MONITORING**: `#agent-status`, `#system-logs`, `#integration-feeds` (telemetry and logs)

---

## Profile Customization & Distribution

Profile data rests directly in the unified `HERMES_HOME` directory. You can adjust config files under `data/hermes/profiles/`:
* **Operations**: `data/hermes/profiles/operations/config.yaml` & `data/hermes/profiles/operations/distribution.yaml`
* **Corporate**: `data/hermes/profiles/corporate/config.yaml` & `data/hermes/profiles/corporate/distribution.yaml`
* **Public**: `data/hermes/profiles/public/config.yaml` & `data/hermes/profiles/public/distribution.yaml`

---

## Data Volumes & Log Persistence

The following host directories preserve SQLite databases and server states across containers restarts:
* `./data/postgres`: PostgreSQL data directory for Paperclip HQ records.
* `./data/paperclip`: Paperclip UI config files.
* `./data/9router`: Routing credentials, cached stats, and providers (Sqlite at `db/data.sqlite`).
* `./data/hindsight`: Embedded database vector indices and schemas.
* `./data/hermes/profiles`: Persistent multi-profile state, memories, sessions, and logs for Hermes agent lanes.
