# OpenIntent Kit — Context & Developer Blueprint

This file outlines the background, objectives, architectural decisions, and rules of engagement for any AI coding agent working on the OpenIntent Kit.

---

## 0. Repository Layout (what lives where)

This is a **configuration & template repository, not a compiled codebase** — there is no build, typecheck, lint, or test step. Edits are YAML manifests, shell scripts, and Python stdlib provisioners. Treat `docker-compose.yml`, the three profile trees, and `scripts/` as the sources of truth.

Top-level sources (tracked):
- `docker-compose.yml` — orchestration manifest. Services: `db` (postgres:17), `headroom`, `9router`, `bootstrap`, `hindsight-api`, `paperclip-hq`, three agent lanes (`agent-operations`, `agent-corporate`, `agent-public`), and `camoufox-browser`. **The agent lanes are gated behind the `agents` compose profile** — without `--profile agents` only core infra starts.
- `profiles/` — three **near-identical Hermes Profile Distributions** (see §0.1):
  - `profiles/default/` = Operations lane (maps to `agent-operations`, container `openintent-default`, port `8001`).
  - `profiles/corporate-agent/` = Corporate lane (`agent-corporate`, `openintent-corporate-agent`, port `8002`).
  - `profiles/public-agent/` = Public lane (`agent-public`, `openintent-public-agent`, port `8003`).
  Each profile contains: `config.yaml`, `distribution.yaml`, `SOUL.md`, `mcp.json`, `.env.EXAMPLE`, plus subdirs `scripts/`, `skills/`, `skill-bundles/`, `hooks/`, `cron/`, `memories/`, `behavior-tests/`, `hindsight/`.
- `scripts/` — runtime provisioners (all zero-dependency): `verify.sh` (cascading health checks), `discord_setup.py` (stdlib Discord channel provisioning), `init_9router_db.py` (runs inside the `bootstrap` container; creates the 9router API key via HTTP).
- `setup.sh` — interactive provisioner: prompts for keys, auto-generates cryptographic secrets, writes `.env`, and stages the three profiles into `data/hermes/`.
- `install.sh` — large self-extracting one-command installer for the **remote** target VPS.
- `docs/niyatna-growth-blueprint.md` — long-term architecture/roadmap doc.
- `AGENTS.md`, `README.md`, `.gitignore`.

Runtime state (gitignored — created by `setup.sh`, **never commit**): `.env`, `data/` (`data/postgres`, `data/9router`, `data/hindsight`, `data/paperclip`, `data/hermes`, `data/camoufox`), `*.log`, `__pycache__/`, `*.pyc`, `.agent.env`, `.niyatna-9router-key`.

### 0.1 The three-profile rule (most important edit gotcha)
The three profile trees are **deliberately near-identical**. `diff profiles/default/config.yaml profiles/{corporate-agent,public-agent}/config.yaml` differs only in:
- `agent.system_prompt` (per-lane identity),
- `platforms.discord.enabled` (default `true`; corporate/public `false`),
- `streaming.cursor`, and
- `terminal.cwd` (`/opt/data/workspace` for default; `/opt/data/profiles/<lane>/workspace` for the others).

When changing a **shared** config key, replicate the edit across all three profiles unless the intent is lane-specific. Always re-diff the three `config.yaml` files after editing to confirm only the intended per-lane fields diverge.

### 0.2 Config & distribution conventions
- `config.yaml` top key `_config_version` is a **schema version** — bump deliberately, never delete blindly. Secrets are injected via `${VAR}` env-substitution (e.g. `${9ROUTER_API_KEY}`, `${DASHBOARD_PASSWORD}`); never hardcode real values.
- `distribution.yaml` declares `env_requires` (env vars each lane needs at runtime), `distribution_owned` (paths the distribution owns), and `memory_policy` (what memory is included/excluded from the distribution).
- `SOUL.md` defines agent posture/identity; `behavior-tests/` is a docs-first QA suite (see its `README.md` for the promotion rule: one-off→fix, repeated→SOUL/skill, stable fact→memory, procedure→skill, long protocol→docs).
- The canonical model/route target across all lanes is `oc/deepseek-v4-flash-free` via the internal `http://9router:20128/v1` endpoint.

---

## 1. Project Background ("Apa & Kenapa")

### What is OpenIntent Kit?
OpenIntent Kit is an automated Multi-Agent System (MAS) orchestrator designed to instantiate a fully functioning **"Agentic Company"** structure for businesses. It bootstraps a unified gateway (9router), a command dashboard (Paperclip HQ), a memory daemon (Hindsight), and specialized agent workforce lanes (Hermes containers) mapped to Discord.

### Rationale of the Architectural Choices:
1. **Official Registry Images vs Local Build Contexts**:
   - *Problem*: Compiling Next.js, TypeScript, and Python codebases from local Dockerfiles requires huge CPU and RAM overloads at build-time. Initiating compilation on a target VPS with limited resources (4GB-12GB RAM) causes Out-of-Memory (OOM) failures or hangs.
   - *Solution*: Pull pre-built base images directly from remote container registries (`ghcr.io` and Docker Hub). The target VM only orchestrates runs and binds databases/configs.
2. **Unified HERMES_HOME Path with Isolated Profiles**:
   - *Problem*: Spawning separate workspace volumes or hard-coded paths for each agent lane causes network clutter and database file collisions.
   - *Solution*: Mount a shared directory `./data/hermes` to `/opt/data` (which is designated as `$HERMES_HOME` inside all agent containers). Each agent lane is then isolated through the `$HERMES_PROFILE` environment variable (e.g. `operations`, `corporate`, `public`). The runtime automatically maps configs and logs to `profiles/<profile_name>/`.
3. **Zero-Dependency Host Processing**:
   - *Problem*: Installing third-party python packages (like `discord.py` or vector libraries) on the target host requires pip management and system-level configuration before setup.
   - *Solution*: All provisioning scripts (`discord_setup.py`, `init_9router_db.py`, etc.) are written in raw Python utilizing only standard library packages (`sqlite3`, `urllib.request`, `json`, `uuid`).
4. **Agent Profile Distributions**:
   - *Problem*: Defining agent lane configurations using custom setup files deviates from standard Hermes conventions, making them difficult to share, back up, or reuse.
   - *Solution*: Package each agent lane template as a proper **Hermes Profile Distribution** containing a `distribution.yaml` manifest, `SOUL.md` (defining agent posture), and `config.yaml` (defining settings).

---

## 2. Ultimate Goals ("Goal Akhir")

Upon completing the bootstrap deployment, the target infrastructure should present:
1. **Orchestrator Landing Panel**: Paperclip UI running on port `3100` linked to a Postgres database, reflecting active tasks, jobs schedules, and agent coordination trees.
2. **Gateway Router API**: 9router gateway on port `20128` successfully balancing LLM load and translating cost boundaries securely.
3. **Continuous Corporate Memory**: Hindsight vector indexing on port `9177` automatically synchronizing agent context queries across sessions.
4. **Discord-Mapped Command Room (Clean & Professional Layout)**:
   A corporate workspace in Discord containing structural channels (not developer-specific names):
   - `GENERAL`: `#announcements`, `#general-discussion`.
   - `OPERATIONS`: `#hq-pulse`, `#active-tasks`, `#approval-gates`, `#proof-of-intent`.
   - `DEPARTMENTS`: `#operations-room`, `#corporate-room`, `#public-room`.
   - `SYSTEM MONITORING`: `#agent-status`, `#system-logs`, `#integration-feeds`.

---

## 3. Rules of Engagement for Coding Agents

When editing or updating this codebase, you must adhere to the following principles:
- **Absolute Paths**: Utilize absolute paths or paths resolved relative to the target project directory (`/home/galyarder/projects/openintent/`) for all host validations.
 - **Do Not Run Local Containers or Local Setup Scripts**: Never run `docker compose up`, `docker compose up -d`, `install.sh`, `setup.sh`, `scripts/discord_setup.py`, or trigger any target service locally. This project is configured only for remote staging (fresh VPS / target production environment deployment). Your job is exclusively to prepare configuration matrices, configuration templates, and installer files.
- **Port Parity**: Keep port maps aligned containing:
  - `9router` -> `20128`
  - `Paperclip HQ` -> `3100`
  - `Hindsight Slim API` -> `9177` (internal `8888`)
  - `Operations Agent` -> `8001`
  - `Corporate Agent` -> `8002`
  - `Public Agent` -> `8003`
- **Zero Secrets Commits**: Never write real API keys or tokens into code templates. All secrets flow through `${VAR}` env-substitution in YAML and are generated/prompted by `setup.sh`. The `_replace_me` / `_random_replace_me` strings in `docker-compose.yml` (JWT, DB password, dashboard secret, initial password) are intentional placeholders — keep them templated, do not "fix" them with real values. Never commit `.env`, `data/`, `.agent.env`, or `.niyatna-9router-key`.
- **Replicate shared edits across all three profiles**: see §0.1. After editing any `config.yaml`, re-diff the three to confirm only the intended per-lane fields (`system_prompt`, `discord.enabled`, `cursor`, `terminal.cwd`) diverge. Keep `_config_version` and `distribution.yaml.hermes_requires` aligned unless deliberately versioning a single lane.
- **Compose profile gating**: the three agent lanes require `--profile agents` to start. When editing `docker-compose.yml`, preserve the `profiles: [agents]` marker on `agent-operations/corporate/public` and the `bootstrap`/`hindsight-api` `depends_on` conditions (agents depend on `bootstrap` completing successfully).
- **Verify on the target host only**: `scripts/verify.sh` is a cascading **runtime** check (TCP ports, HTTP endpoints, Hindsight DB write, `docker compose ps`) — it does not lint structure and will report every port CLOSED on a clean dev machine because no services run here. Do not run it locally to "prove structure normality"; instead validate structure by re-diffing profiles, `git ls-files`, and `python3 -c "import yaml,sys; [yaml.safe_load(open(f)) for f in sys.argv[1:]]"` on edited YAML files.

---

## 4. Network & Security Architecture Patterns

Depending on the environment requirements, the Niyatna multi-agent stack utilizes two distinct network access and hardening patterns:

### 4.1 Staging / Developer Overlay (Our Active Reference Host)
For isolated development sandbox testing (e.g. testing setups where only 1-2 key stakeholders access the environment), we utilize a **Cloudflare Zero Trust Mesh Network** overlay. This pattern enforces Zero public open ports.

- **Organization Domain**: `galyarderlabs`
- **VPS Staging Server (`prod-niyatna`)**: Registered headless via `cloudflare-warp`. Assigned **Private Mesh IP**: `100.96.0.1` (`CloudflareWARP` virtual interface).
- **Client Laptop (`GalyarderOS`)**: Registered via WARP client with authenticated user email (`muhamadgalihsaputraa@gmail.com`). Assigned **Private Mesh IP**: `100.96.0.2`.
- **Hardened Port Binding Rules**: All services exposed in `docker-compose.yml` (e.g. Paperclip HQ on `3100`, 9router on `20128`, Hindsight on `9177`) must strictly bind to the VPS Mesh IP `100.96.0.1`:
  ```yaml
  ports:
    - "100.96.0.1:3100:3100"
    - "100.96.0.1:20128:20128"
    - "100.96.0.1:9177:8888"
  ```
- **Troubleshooting Step**: If ping or SSH over mesh is failing, ensure the `100.64.0.0/10` CGNAT range is removed from the Split Tunnel **Exclude List** in the Zero Trust dashboard (Devices > Device settings > Split Tunnels) on the client profile.

### 4.2 Production / Multi-User Client Deployments
For production environments accessed by entire teams/companies, requiring every user to install and enroll in a client WARP mesh is impractical. We utilize **Clientless Ingress Routing**:

1. **Localhost Binding**: In the client-vps `docker-compose.yml`, services are bound only to localhost:
   ```yaml
   ports:
     - "127.0.0.1:3100:3100"   # Paperclip HQ
     - "127.0.0.1:20128:20128" # 9router
   ```
2. **Cloudflare Tunnel (`cloudflared` daemon)**: A standard outbound-only daemon runs on the host VPS (no client-side software required for users). It connects the localhost ports directly to the company subdomains (e.g., `hq.clientcompany.com`).
3. **Application Control (Edge Auth)**: Access is secured at the Cloudflare Edge using **Cloudflare Access (Zero Trust)**. When employees open the subdomain, they sign in via standard browser SSO (Google Workspace, Microsoft Entra, or email OTP). No client app, keys, or VPN configuration is required on the employee's machine.
4. **App Auth Backup**: Internal dashboard actions rely on Paperclip's built-in session authentication and 9router's `API_KEY_SECRET` token gates.
