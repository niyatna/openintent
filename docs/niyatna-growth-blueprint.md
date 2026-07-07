# Niyatna OS - "Growth with Company" Data Doctrine Blueprint

## 1. Core Vision & Philosophy
Traditional AI assistants (like Keiya/default) focus on personal productivity and "growing with the user." Niyatna OS pivots this paradigm toward **"Growing with the Company."**

Instead of serving as isolated chatbots, Niyatna agents act as the **cognitive data nervous system** of an organization. The ultimate value of Niyatna OS lies in its ability to consume, digest, map, and organize every operational byte:
- **Finance & Admin**: Invoices, ledger updates, runways, purchase approvals.
- **People & HR (SDM)**: Worker profiles, habits, tasks, roles, capabilities, performance logs.
- **Operations & Systems (SDA)**: Local code checkouts, server logs, API integrations, tool states.
- **Knowledge Base (Obsidian Brain)**: Project requirements, SOPs, documentation.

By feeding this continuous, unified context into a structured local memory daemon (Hindsight + local vector databases), the agent's strategic value scales non-linearly. It maps out organizational habits, detects workflow bottlenecks, flags security risks, and enforces strict "Proof of Intent" for all actions.

---

## 2. Profile Access boundaries (Early Phase Mapping)
When a user (employee, investor, stakeholder) first interacts with Niyatna OS, they encounter a structured greeting protocol:
1. **Identification**: *"Hi, who are you? What is your full name and position within the department? What do you need to access today?"*
2. **Dynamic Contextual Alignment**: The agent matches the user's role against the target profile's permission matrix.

### The Profile Hierarchy:
- **Default Profile (Operations Agent - Port 8001)**:
  - **Access**: Open to all internal employees, department leaders, and investors.
  - **Capabilities**: Managing internal files, task directories, local automations, code verify scopes, and Hindsight indexing. (Prohibited from public-facing CS channels).
- **Corporate Profile (Corporate Agent - Port 8002)**:
  - **Access**: Strict authorization boundary. Restricted only to founders, C-level executives (CEO, CMO, CFO, COO), and primary investors.
  - **Capabilities**: Accessing strategic models, investment ROI datasets, Obsidian corporate vaults, and budget/runway approval gates.
- **Public Profile (Public Agent - Port 8003)**:
  - **Access**: Publicly accessible by external clients, competitors, and general users (e.g., embedded on websites, external support chats).
  - **Capabilities**: Competitor scraping, public market data monitoring, and customer support (strictly sandboxed from internal company databases, secrets, and code paths).

---

## 3. Mapping Context into the Obsidian Brain
To materialize the "Grow with Company" value, the agent uses the local Obsidian Vault as its persistent, human-readable semantic structure:
- **People Directory**: `/Obsidian/company/sdm/<user_id>.md` (storing user habits, tasks, values, and organizational history).
- **Asset/Systems Logs**: `/Obsidian/company/sda/<system_id>.md` (tracking hardware, API health, tool endpoints).
- **Task Backlog**: `/Obsidian/company/tasks/` maps directly to Paperclip command logs.
- **Finance Ledger**: `/Obsidian/company/finance/` runs basic transaction verifications.

---

## 4. Starter Blueprint Templates (`USER.md` & `MEMORY.md`)
To package Niyatna OS as a portable, distributable starter kit, `USER.md` and `MEMORY.md` must be stripped of Muhamad Galih Saputra's personal settings and converted into generic, plug-and-play templates.
- **`USER.md`** template: Guides the agent on how to interview the first user who starts the session, log their organization info, and store it.
- **`MEMORY.md`** template: Sets up the structural placeholders for departments, company goals, and Hindsight memory bank references.
