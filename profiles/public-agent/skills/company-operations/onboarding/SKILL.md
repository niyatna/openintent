---
name: onboarding
description: Use when guiding first-time users, identifying chat users, checking environment setup, or bootstrapping the company Obsidian directory structure.
version: 1.0.0
author: Company Operations
license: MIT
metadata:
  hermes:
    tags: [onboarding, setup, multi-user, identity, env, obsidian]
    category: company-operations
---

# OpenIntent Onboarding Specialist

## When to Use
Use when:
- Greet a human for the first time in a chat session.
- Staging or verifying a new OpenIntent MAS deployment.
- A user wants to confirm if all required `.env` configurations are valid.
- Bootstrapping or verifying the Obsidian database folders (`/company`, `/departments`).
- Populating the startup company profile (mission, runway, target audience).

Do not use for:
- Regular coding, task management, or production deployments.

## Core Directives

### 1. Multi-User Identification
- Greet the user and check if their identity (name, role, department) exists in `memories/USER.md`.
- If missing, request their **Name**, **Role**, and **Department**.
- Save the details to `memories/USER.md` and log their employee file in the Obsidian vault at `/company/sdm/<username>.md`.
- In shared chat rooms (like Discord), ask users to identify themselves or tag the agent, and match responses to their username.

### 2. Environment Verification
- Run `python3 ~/.hermes/skills/company-operations/onboarding/scripts/validate_onboarding.py --env` to check if all mandatory and optional variables are properly configured.
- Report the results to the user. Explain any missing variables.

### 3. Obsidian Bootstrapping
- Run `python3 ~/.hermes/skills/company-operations/onboarding/scripts/validate_onboarding.py --obsidian` to verify or create the company directory structure inside the Obsidian vault.
- Ensure folders exist for: `/company`, `/company/sdm`, `/departments/operations`, `/departments/corporate`, and `/departments/public`.

### 4. Company Profile Questionnaire
- If `/company/profile.md` is empty or missing, ask the user the onboarding questions:
  1. Company Name
  2. Core Mission & Vision
  3. Problem & Solution
  4. Target Audience
  5. Funding & Runway Status
  6. Key Metrics
- Populate `/company/profile.md` and `memories/MEMORY.md`, and sync to Hindsight vector memory.

## References
- `references/onboarding-runbook.md` — detailed fields, environment variables lists, and directories map.
