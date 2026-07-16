---
author: Company
description: Use when installing, retrieving credentials secrets, or unlocking key
  vaults via the Bitwarden CLI (bw).
license: MIT
metadata:
  hermes:
    category: security
    tags:
    - security
    - secrets
    - bitwarden
    - bw
    - cli
name: bitwarden
setup:
  collect_secrets:
  - env_var: BW_CLIENTID
    prompt: Bitwarden Access Client ID
    secret: true
  - env_var: BW_CLIENTSECRET
    prompt: Bitwarden Access Client Secret
    secret: true
  help: Uses Bitwarden CLI. Set BW_CLIENTID and BW_CLIENTSECRET env vars or use personal
    master password via console environment.
version: 1.0.0
---


# Bitwarden CLI

Use this skill when managing secrets, passwords, SSH keys, or API tokens via Bitwarden rather than plaintext configurations.

## Setup & CLI Installation

Bitwarden CLI (`bw`) can be run via npx or installed locally.

```bash
# Verify CLI via npx (default fallback)
npx @bitwarden/cli --version

# Or install globally via npm
npm install -g @bitwarden/cli
```

## Authentication & Unlock Protocol

### 1. API Key Authentication (Recommended for scripts)
Configure the following variables in `~/.hermes/.env` (or environment):
* `BW_CLIENTID`
* `BW_CLIENTSECRET`

```bash
# Log in with API Key
export BW_CLIENTID="user.your-id"
export BW_CLIENTSECRET="your-secret"
npx @bitwarden/cli login --apikey
```

### 2. Unlocking and Session Handling
Logging in or unlocking returns a **Session Key**. To execute subsequent CLI commands, this session key MUST be exported as `BW_SESSION` or passed with `--session <session_key>`.

```bash
# Unlock the vault (prompts for Master Password if client ID is set)
export BW_SESSION=$(npx @bitwarden/cli unlock --raw)
```

## Retrieval Workflows

Always filter or clean stdout. Bitwarden CLI outputs JSON.

```bash
# Search for an item
npx @bitwarden/cli list items --search "github" --session "$BW_SESSION" | jq

# Get exact password field of an item by UID
npx @bitwarden/cli get password "<item-uuid>" --session "$BW_SESSION"

# Get custom field value by name
npx @bitwarden/cli get item "<item-uuid>" --session "$BW_SESSION" | jq '.fields[] | select(.name=="api_key") | .value'
```

## Operational Safety Rules
* **Never echo or log** `$BW_SESSION` or raw password output.
* Keep `BW_CLIENTSECRET` out of version control and session transcripts.
* Wipe/lock the vault immediately when authentication tasks are done:
  ```bash
  npx @bitwarden/cli lock
  ```
