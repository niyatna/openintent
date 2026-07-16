# OpenIntent Kit — Multi-Agent Company Orchestrator

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=flat-square&logo=gnu-bash&logoColor=white)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=flat-square&logo=yaml&logoColor=151515)

OpenIntent Kit is an open-source bootstrap orchestrator designed to instantiate a fully functioning "Agentic Company" structure for businesses. Instead of serving as isolated chatbots, the multi-agent stack operates as a collaborative, digital corporate workforce, executing task backlogs, analyzing markets, managing runways, and conducting repository audits under direct human oversight.

---

## 1. Agentic Company Operations Framework

OpenIntent structures its autonomous workforce into distinct corporate divisions, executing operations through specialized agent profiles:

### 1.1 Executive & Strategy (CEO)
- **Role**: General brand strategy, market positioning, marketing campaign structures, and thought leadership.
- **Workflow**: Translates the founder's raw vision into marketing briefs and establishes public identity guidelines.

### 1.2 Financial Operations (CFO)
- **Role**: Runway calculation, burn rate audits, cost optimization (FinOps), and fundraising coordination.
- **Workflow**: Enforces capital discipline. For any wallet movements or spot asset liquidations, the CFO verifies on-chain balances, calculates quotes, and demands explicit human approval before broadcasting transfers.

### 1.3 System Operations (COO)
- **Role**: Core workstream sequencing, task lifecycle management, Chief of Staff cadences, and compliance audits (GDPR, ISO 42001).
- **Workflow**: Manages organizational cadences, schedules, and coordinates structured multi-agent handoffs.

### 1.4 Technical Architecture (CTO)
- **Role**: Codebase architecture, repository framework management, node configurations, and automated code audits.
- **Workflow**: Establishes workspace boundaries, configures test-driven-development (TDD) pipelines, and runs system validation checks.

### 1.5 Discord OS (Human-in-the-Loop Cockpit)
The company's operating system interface is mapped directly to a structured Discord server via autonomous webhook relays, enforcing strict Human-in-the-Loop (HILO) confirmation gates:
- **Announcements**: Announcements and general communications in `#announcements` and `#general-discussion`.
- **Approvals**: High-stakes operations (like code merges or cash transfers) post interactive Approve/Reject buttons directly to `#approval-gates`.
- **Evidence**: Completed tasks automatically write verification summaries and links directly to `#proof-of-intent` for audit audits.
- **Departments**: Direct department communication links (`#operations-room`, `#corporate-room`, `#public-room`).
- **Telemetry**: Infrastructure logs and agent health check summaries route to `#agent-status` and `#system-logs`.

---

## 2. Infrastructure & Stack Components

The kit mounts, links, and operates 9 dedicated containers orchestrated through Docker Compose:

### 2.1 Gateway & Router (9router)
- **Container**: `openintent-9router` (Service: `9router`)
- **Port**: `20128` (Internal port maps handle headroom at `8787`).
- **Role**: Next.js OpenAI-compatible proxy gateway. Automatically translates model requests, handles provider failover, optimizes prompts, enforces budget boundaries, and balances LLM loads.
- **Canonic Route**: All agents route requests through `http://9router:20128/v1` targeting `oc/deepseek-v4-flash-free` for zero-friction intelligence.

### 2.2 Command Dashboard (paperclip-hq)
- **Container**: `openintent-paperclip` (Service: `paperclip-hq`)
- **Port**: `3100`
- **Role**: TypeScript React control panel linked to the Postgres database. Reflects active task backlogs, cron schedules, agent roster trees, and coordinates parallel execution loops.

### 2.3 Continuous Corporate Memory (hindsight-api)
- **Container**: `openintent-hindsight` (Service: `hindsight-api`)
- **Port**: `9177` (internal port `8888`)
- **Role**: Vector database and long-term memory engine. Employs SQLite storage and local CPU embeddings to index, recall, and synchronize agent context across sessions in real-time.

### 2.4 Agent Workforce Lanes (hermes-agent)
Spawns three isolated Hermes containers, gated behind the `--profile agents` compose group for resource isolation. Each lane runs its own profile distribution, memory bank, and workspace directory:
- **Operations Profile** (`openintent-default` | Port `8001`): The primary coordinator and task backlog manager. Handles company OS, local files, config checks, and memory bank sync.
- **Corporate Profile** (`openintent-corporate-agent` | Port `8002`): CFO/COO/CEO executive lane. Handles runway, budget approvals, and strategic roadmap reviews.
- **Public Profile** (`openintent-public-agent` | Port `8003`): General public interface. Handles public customer support (strictly sandboxed from company secrets and source codes) and market searches.

### 2.5 Stealth Browser Agent (camoufox-browser)
- **Container**: `openintent-camoufox` (Service: `camoufox-browser`)
- **Port**: `9377`
- **Role**: Playwright stealth Chromium browser agent based on Camoufox. Handles headed/headless automation, persistent cookie reuse, and anti-bot bypass protocols for social media postings.

### 2.6 Core Support Services
- **Database (db)**: Runs `postgres:17` on port `5432` to serve Paperclip HQ's persistent records.
- **Database Bootstrap (bootstrap)**: Short-lived Python container that auto-seeds 9router's initial API credentials via secure HTTP handshakes on startup.
- **Internal Proxy (headroom)**: Manages routing headroom, local proxy boundaries, and SSL mesh integrations.

### 2.7 Pre-Seeded CLI & MCP Integrations
The Operations Agent container automatically bootstraps and seeds the following NPM globally-installed tools and Python PIP modules on startup:
- **Claude Code** (`@anthropic-ai/claude-code`): Global CLI tool that delegates code edits and PR reviews.
- **CodeGraph** (`@colbymchenry/codegraph`): Global repository indexing tool to query symbol definitions and dependency trees.
- **officecli** (`officecli`): CLI utility and helper script to create and alter Office documents (`.docx`, `.xlsx`, `.pptx`).
- **notebooklm-mcp-cli**: Python MCP connector that interfaces with Google's NotebookLM for source-grounded file digestion.
- **paperclip-mcp**: Python MCP connector to link tasks, budgets, and runs between Hermes and Paperclip HQ.

---

## 3. Infrastructure & System Requirements

- **Minimum Specs**: 2 vCPU cores, 4 GB RAM.
- **Recommended Specs**: 2 vCPU cores, 12 GB RAM (e.g., standard Cloud VPS or Oracle Cloud Free Tier).
- **Supported OS**: Debian 11/12 or Ubuntu 20.04/22.04 LTS.
- **Core Dependencies**: Docker Engine, Docker Compose (v2.x+), Python 3.x, and Curl.

---

## 4. Quick Start (1-Minute Remote Deployment)

WARNING: Never run installer scripts (install.sh, setup.sh), verify scripts, or docker-compose services on your local development machine. This workspace is strictly for configuring and preparing deployment templates. All scripts are designed to execute only on your remote server.

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
   *(This prompts for OpenRouter/Discord tokens, auto-generates JWT/DB cryptography secrets, writes `.env`, and sets up profiles inside `data/hermes/`).*

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

## 5. Host Directories & Data Persistence

To prevent data loss across container restarts, the following host volume bindings are created inside `./data/`:
- `./data/postgres`: PostgreSQL data files for Paperclip HQ.
- `./data/paperclip`: Panel configurations and session files.
- `./data/9router`: SQLite routing databases and stats (`db/data.sqlite`).
- `./data/hindsight`: Vector database indices.
- `./data/hermes/profiles`: Persistent profiles, memories, and logs for the three agent lanes.
- `./data/camoufox`: Stealth browser local profiles and caches.
