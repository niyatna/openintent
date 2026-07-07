# OpenIntent Kit — Context & Developer Blueprint

This file outlines the background, objectives, architectural decisions, and rules of engagement for any AI coding agent working on the OpenIntent Kit.

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
- **Zero Secrets Commits**: Never write real API keys or tokens into code templates. Always use environmental parameters checked by the bootstrap provisioner.
- **Verify All Changes**: Always run `scripts/verify.sh` after modifications to prove structure normality.
