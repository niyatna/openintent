# OpenIntent Kit — Multi-Agent Infrastructure Orchestrator

```text
  ┌──────────────────────────────────────────────────────────────┐
  │                        OPENINTENT KIT                        │
  │     Autonomous Multi-Agent Organizational Infrastructure     │
  └──────────────────────────────────────────────────────────────┘
     [Python]  ──  [Hermes Agent]  ──  [Paperclip HQ]  ──  [9router]  
             ──  [Hindsight Memory]  ──  [Camoufox Browser]
```

OpenIntent Kit is an open-source bootstrap orchestrator designed to instantiate a fully functioning **"Agentic Company"** structure for businesses. It automatically provisions a unified gateway (**9router**), a command dashboard (**Paperclip HQ**), a self-hosted vector database (**Hindsight**), a headed stealth browser (**Camoufox**), and isolated agent workspaces (**Hermes Agent**) mapped straight to Discord.

---

## 1. Architecture & Stack Components

The kit mounts, links, and operates **9 dedicated containers** orchestrated through Docker Compose:

### 🌐 1. Gateway & Router (`9router`)
- **Container**: `openintent-9router` (Service: `9router`)
- **Port**: `20128` (Internal port maps handle headroom at `8787`).
- **Role**: Next.js OpenAI-compatible proxy gateway. Automatically translates model requests, handles provider failover, optimizes prompts, enforce budget boundaries, and balances LLM loads.
- **Canonic Route**: All agents route requests through `http://9router:20128/v1` targeting `oc/deepseek-v4-flash-free` for zero-friction intelligence.

### 📊 2. Command Dashboard (`paperclip-hq`)
- **Container**: `openintent-paperclip` (Service: `paperclip-hq`)
- **Port**: `3100`
- **Role**: TypeScript React control panel linked to the Postgres database. Reflects active task backlogs, cron schedules, agent roster trees, and coordinates parallel execution loops.

### 🧠 3. Continuous Corporate Memory (`hindsight-api`)
- **Container**: `openintent-hindsight` (Service: `hindsight-api`)
- **Port**: `9177` (internal port `8888`)
- **Role**: Vector database and long-term memory engine. Employs SQLite storage and local CPU embeddings to automatically index, recall, and synchronize agent context across sessions in real-time.

### 🤖 4. Agent Workforce Lanes (`hermes-agent`)
Spawns three isolated Hermes containers, gated behind the `--profile agents` compose group for resource isolation. Each lane runs its own profile distribution, memory bank, and workspace directory:
- **Operations Profile** (`openintent-default` | Port `8001`): The primary coordinator and task backlog manager. Handles company OS, local files, config checks, and memory bank sync.
- **Corporate Profile** (`openintent-corporate-agent` | Port `8002`): CFO/COO/CEO executive lane. Handless runway runways, budget approvals, and strategic roadmap reviews.
- **Public Profile** (`openintent-public-agent` | Port `8003`): General public interface. Handless public customer support (strictly sandboxed from company secrets and source codes) and market searches.

### 🦊 5. Stealth Browser Agent (`camoufox-browser`)
- **Container**: `openintent-camoufox` (Service: `camoufox-browser`)
- **Port**: `9377`
- **Role**: Playwright stealth Chromium browser agent based on Camoufox. Handles headed/headless automation, persistent cookie reuse, and anti-bot bypass protocols for social media postings.

### ⚙️ 6. Core Support Services
- **Database (`db`)**: Runs `postgres:17` on port `5432` to serve Paperclip HQ's persistent records.
- **Database Bootstrap (`bootstrap`)**: Short-lived Python container that auto-seeds 9router's initial API credentials via secure HTTP handshakes on startup.
- **Internal Proxy (`headroom`)**: Manages routing headroom, local proxy boundaries, and SSL mesh integrations.

---

## 2. Infrastructure & System Requirements

- **Minimum Specs**: 2 vCPU cores, 4 GB RAM.
- **Recommended Specs**: 2 vCPU cores, 12 GB RAM (e.g., standard Cloud VPS or Oracle Cloud Free Tier).
- **Supported OS**: Debian 11/12 or Ubuntu 20.04/22.04 LTS.
- **Core Dependencies**: Docker Engine, Docker Compose (v2.x+), Python 3.x, and Curl.

---

## 3. Quick Start (1-Minute Remote Deployment)

⚠️ **CRITICAL DEPLOYMENT NOTICE**: Never run installer scripts (`install.sh`, `setup.sh`), verify scripts, or docker-compose services on your local development machine. This workspace is strictly for configuring and preparing deployment templates. All scripts are designed to execute only on your remote server.

To install and bootstrap the Agentic Company infrastructure on your remote VPS, run the single command below:

```bash
curl -fSsL https://raw.githubusercontent.com/niyatna/openintent/main/install.sh | bash
```

### Cascading Post-Install Setup
After the extraction completes on the remote server, cd into the folder and execute the setup sequence:

1. **Populate Environment & Profiles**:
   ```bash
   ./setup.sh
   ```
   *(This prompts for OpenRouter/Discord tokens, auto-generates JWT/DB cryptography secrets, writes `.env`, and setups profiles inside `data/hermes/`).*

2. **Orchestrate Stack**:
   ```bash
   docker compose --profile agents up -d
   ```

3. **Verify TCP Port & HTTP Handshakes**:
   ```bash
   ./scripts/verify.sh
   ```

4. **Provision Discord Channels Workspace**:
   ```bash
   ./scripts/discord_setup.py
   ```

---

## 4. Discord Command Room Structure

Running the zero-dependency Python provisioner (`./scripts/discord_setup.py`) uses your `DISCORD_BOT_TOKEN` to build a clean corporate layout on your Discord server:

- **`GENERAL`**: `#announcements` & `#general-discussion`.
- **`OPERATIONS`**: `#hq-pulse` (dashboard updates), `#active-tasks` (running job notifications), `#approval-gates` (interactive Approve/Reject buttons for wallet or code actions), `#proof-of-intent` (evidence audit trails).
- **`DEPARTMENTS`**: `#operations-room` (Operations Lane), `#corporate-room` (Corporate Lane), `#public-room` (Public Lane).
- **`SYSTEM MONITORING`**: `#agent-status`, `#system-logs`, `#integration-feeds` (telemetry and logs).

---

## 5. Host Directories & Data Persistence

To prevent data loss across container restarts, the following host volume bindings are created inside `./data/`:
- `./data/postgres`: PostgreSQL data files for Paperclip HQ.
- `./data/paperclip`: Panel configurations and session files.
- `./data/9router`: SQLite routing databases and stats (`db/data.sqlite`).
- `./data/hindsight`: Vector database indices.
- `./data/hermes/profiles`: Persistent profiles, memories, and logs for the three agent lanes.
- `./data/camoufox`: Stealth browser local profiles and caches.
