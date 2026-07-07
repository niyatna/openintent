---
author: Galyarder Labs
description: Use when auditing, setting up, or authenticating automated agent logins
  via CloakBrowser profiles, session cookies, or TOTP keys.
license: MIT
metadata:
  hermes:
    category: autonomous-ai-agents
    related_skills:
    - cloakbrowser-browser
    - hermes-camofox-browser
    - camofox-browser
    - 1password
    - platform-operator-router
    tags:
    - account-login
    - cloakbrowser
    - browser-profiles
    - camofox
    - totp
    - cookies
    - google
    - github
    - twitter
    - x
    - oauth
    - secrets
name: agent-accounts
version: 1.0.0
---


# Agent-Owned Account Login

## Role boundary

This is a **support skill**, not the entrypoint for social posting.

- `platform-operator-router` chooses the platform route.
- `platform-operator-router`, `platform-operator-router`, `platform-operator-router`, and `google-workspace` own platform-specific frontend CRUD.
- `agent-owned-account-login` owns the shared credential/session primitives: private account file contract, TOTP/backup-code handling, cookie/session hygiene, and safe CloakBrowser persistent-profile login bootstrap.
- Browser skills own CloakBrowser/Camofox runtime mechanics, not platform semantics.

Do not duplicate platform posting/deletion/interactions here. If a frontend label changes, patch the platform operator skill.

Session-specific supported flows are collected under `references/`. Current notable references:

- `references/xiaomi-mimo-cloakbrowser-invite-code-2026-06-05.md` — Xiaomi MiMo dedicated account OAuth, invite-code/token-credit redemption, API-key creation boundaries, and verification pitfalls.
- `references/github-agent-pat-regeneration-and-2fa-checkup-2026-06-16.md` — GitHub Personal Access Token headless regeneration and settings 2FA checkup bypass flow.

## Overview

This skill is for **dedicated agent-owned accounts**, not Galih's primary personal accounts.

Core rule: login automation is allowed only after the account has an access contract, safe credential storage, confirmation thresholds, and a read-only/safe-write test. CloakBrowser persistent profiles are the primary isolated auth/session route. Camofox/Camoufox is legacy/fallback only when CloakBrowser is blocked or the platform skill still has a verified Camofox-only CRUD flow. Secrets stay in private credential files or an encrypted manager, never in chat, SOUL, memory, Obsidian, skills, profile repos, or logs.

## When to Use

Use this when Galih asks to:

- prepare Keiya/Galyarder-owned Google, GitHub, X/Twitter, Notion/Linear OAuth, or similar accounts;
- sign in through CloakBrowser persistent profiles using account credentials or cookies;
- generate a TOTP code from a saved TOTP secret;
- validate an `account.txt` without printing credentials;
- design autonomous login recovery for dedicated accounts;
- decide whether to use browser login, cookies, OAuth, platform-operator-router, or an API/token flow.

Do not use this for mass signup, CAPTCHA bypass, OTP/email farm automation, quota evasion, scraping behind access controls, or accounts Galih does not own/control.

## Account File Contract

Private credential root:

```text
/home/galyarder/.hermes/private/credentials/agents/
  keiya/
    google/account.txt
    github/account.txt
    x/account.txt
    wallet/account.txt
  galyarder/
    google/account.txt
    github/account.txt
    x/account.txt
    wallet/account.txt
```

`account.txt` is `.env`-style and must be `chmod 600`. Directories should be `chmod 700`.

Recommended fields:

```dotenv
ACCOUNT_ID=keiya-google
OWNER=keiya
SERVICE=google
EMAIL=example@gmail.com
USERNAME=
PASSWORD=never_commit_or_print
TOTP_SECRET=BASE32SECRETWITHOUTSPACES
BACKUP_CODES_FILE=/home/galyarder/.hermes/private/credentials/agents/keiya/google/backup-codes.txt
COOKIES_FILE=/home/galyarder/.hermes/private/credentials/agents/keiya/google/cookies.json
RECOVERY_EMAIL=
PHONE_LAST4=
NOTES=dedicated agent-owned account
```

Rules:

- Never commit `account.txt`, `backup-codes.txt`, `cookies.json`, tokens, or session stores.
- Do not paste the password/TOTP secret into chat.
- If using 1Password later, replace secret fields with `op://...` references and use `op run` / `op read`.
- Wallet account files should store public address and metadata only by default. Never store seed phrase/private key in plaintext.

## TOTP

TOTP is generated locally from the base32 `TOTP_SECRET`. The code is time-based; a fresh code is usually valid for 30 seconds.

Use the helper:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/autonomous-ai-agents/agent-owned-account-login/scripts/account_totp.py \
  --account-file /home/galyarder/.hermes/private/credentials/agents/keiya/google/account.txt
```

This prints only the OTP and timing metadata, not the secret.

If `pyotp` is unavailable, the helper uses Python stdlib HMAC/SHA1 and base32 decoding.

## Account Skeleton Creation

Create private directories and placeholder-only `account.txt` files with:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/autonomous-ai-agents/agent-owned-account-login/scripts/account_init.py \
  --owner keiya \
  --service google \
  --email keiya.example@gmail.com
```

The initializer writes no secret values. It creates:

- `account.txt` with empty `PASSWORD=` and `TOTP_SECRET=` placeholders;
- `backup-codes.txt` placeholder;
- `cookies.json` placeholder;
- directory mode `700`, file mode `600`.

Validator/audit scripts should check the fields the initializer actually emits: `ACCOUNT_ID=`, `OWNER=`, `SERVICE=`, empty secret placeholders, and `NOTES=dedicated agent-owned account`. Do not require a synthetic `STATUS=writing-plansned-placeholder` unless the initializer is changed to write it; that causes false-positive hardening failures.

Only fill real credentials locally after the account is approved and the access contract exists in `/home/galyarder/.hermes/private/credentials/access-registry.yaml`.

## Validation


---
**Warning:** Detailed setup and developer instructions have been moved out of this main playbook to prevent token footprint expansion. Please refer to: `references/agent-owned-account-login.md` for the full reference guidelines.

## References & Sub-playbooks
Detailed guidelines for operations and troubleshooting are stored as modular reference documents under references/:
- `references/agent-os-account-lifecycle.md` — Guidelines for execution of Agent Os Account Lifecycle
