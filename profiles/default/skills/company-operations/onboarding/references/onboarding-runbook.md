# OpenIntent Multi-Agent Onboarding Runbook

This guide instructs the Niyatna OpenIntent Agent on how to handle first-time users, identify team members in a shared workspace (like Discord), verify environment setup, and bootstrap the company's knowledge base (Obsidian & Hindsight).

---

## 1. Multi-User Identity & Room Protocol

Because a single agent lane (e.g., Discord workspace / API channel) is accessed by multiple humans, the agent must keep track of who is talking. 

### 1.1 First-Time Greeting & Identification
When a user interacts with the agent for the first time, or if their identity is not cached under `memories/USER.md`:
1. Greet the user and ask:
   *"Hi! I am the Niyatna OpenIntent Agent for this channel. To align our company workflow, could you please tell me your **Name**, **Role / Position**, and **Department**?"*
2. Once the user replies:
   * Write their profile to the Obsidian employee directory: `/company/sdm/<username>.md`.
   * Log/append their profile into `memories/USER.md`.
   * Persist their profile into Hindsight vector memory.

### 1.2 Chat Room & Tagging Protocol
In shared chat environments (like Discord):
1. Instruct humans that they should introduce themselves on their first message in any new channel/room or tag the agent explicitly:
   * Example: *"Hi, I'm [Name] from [Department]. @Operations, please check..."*
2. The agent must parse the message sender's profile metadata (user ID / nickname) or look for manual introductions (e.g., *"Hi, I'm Alex from Tech"*).
3. Always prefix or direct responses to the specific target human (e.g., `"Hello @Alex (Tech Department)..."`).

---

## 2. Environment Verification

Before executing operational tasks, the agent must ensure all system variables are fully configured.

### 2.1 Environmental Variables Matrix
Verify the status of the following variables in `.env` or system environment:

| Variable | Status | Description |
|----------|--------|-------------|
| `OPENROUTER_API_KEY` | **Mandatory** | For accessing LLM APIs via 9router. |
| `DISCORD_BOT_TOKEN` | **Mandatory** | For Discord Gateway connectivity. |
| `9ROUTER_API_KEY` | **Mandatory** | For local 9router gateway authentication. |
| `CONTEXT7_API_KEY` | **Mandatory** | For Context7 MCP client. |
| `DASHBOARD_USERNAME` | **Mandatory** | Administrator user for Paperclip HQ. |
| `DASHBOARD_PASSWORD` | **Mandatory** | Administrator password for Paperclip HQ. |
| `DASHBOARD_SECRET` | **Mandatory** | Session secret for Paperclip HQ. |
| `DISCORD_ALLOWED_USERS`| **Optional** | A list of trusted Discord user IDs allowed to interact with the bot. |
| `CAMOFOX_URL` | **Optional** | API endpoint for the headless browser. |

### 2.2 Verification Command
To verify the environment inside the container, run:
```bash
python3 ~/.hermes/skills/company-operations/onboarding/scripts/validate_onboarding.py --env
```
Or from the host setup stage:
```bash
python3 profiles/default/skills/company-operations/onboarding/scripts/validate_onboarding.py --env
```
Report any missing mandatory variables as an error. Report missing optional variables as a warning.

---

## 3. Obsidian Knowledge Base Bootstrapping

The company's shared brain is stored in an Obsidian vault. The agent must ensure the basic directory layout exists.

### 3.1 Vault Structure Definition
Ensure the following directories and baseline onboarding notes are generated:
- `/company/` — General company documentation.
  - `/company/profile.md` — Company profile, mission, audience.
  - `/company/sdm/` — Employee profiles directory.
- `/departments/` — Isolated directories per business lane.
  - `/departments/operations/` — Active tasks, automation logs, schedules.
  - `/departments/corporate/` — Strategic decisions, runways, CFO reports.
  - `/departments/public/` — Client relations CRM, marketing materials.
- `/hindsight/` — Continuous memory sync dumps.

### 3.2 Verification Command
To check or bootstrap the directory structure inside the container, run:
```bash
python3 ~/.hermes/skills/company-operations/onboarding/scripts/validate_onboarding.py --obsidian
```
Or from the host setup stage:
```bash
python3 profiles/default/skills/company-operations/onboarding/scripts/validate_onboarding.py --obsidian
```
---

## 4. Company Profile Questionnaire

If `/company/profile.md` is empty or does not exist, ask the user the following onboarding questions to define the company profile:
1. **Company Name**: What is the name of our company/business?
2. **Core Mission & Vision**: What is the primary purpose and long-term goal of the business?
3. **Problem & Solution**: What key problem does the company solve, and what is the offering/product?
4. **Target Audience**: Who are the primary customers/users?
5. **Funding & Runway Status**: What is the current funding status (bootstrapped, pre-seed, seed, series A)?
6. **Key Metrics**: What is the current runway (months) and MRR (approximate/optional)?

Save the replies into:
* `/company/profile.md` in the Obsidian Vault.
* `memories/MEMORY.md` under the appropriate configuration fields.
* Commit the structured profile payload to Hindsight vector memory.
