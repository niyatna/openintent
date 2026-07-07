# enowX AI BYOA Proxy Notes

Source reviewed: `https://enowxlabs.com/apps/enowx-ai`
Date: 2026-05-07

## What the page describes

The page describes `enowX AI` as a self-hosted AI proxy / BYOA system exposing local OpenAI/Anthropic-compatible endpoints:

```text
API/Chat: http://localhost:1430
Dashboard: http://localhost:1431
```

Claimed features:

- unified API for many model IDs
- image generation endpoint via Canva AI
- MITM proxy for tools like Cursor, Trae, and Antigravity
- sticky account rotation
- automatic error recovery
- multi-step fallback
- LAN exposure and IP whitelist
- account batch import

Account management excerpts from the page:

```text
Dashboard: localhost:1431/accounts
batch import in email:password format
CLI: enowxai accounts add accounts.txt
```

Critical requirement quoted by the page:

```text
Use fresh Google accounts with no 2FA or phone verification.
Any security prompts will cause automated login to fail.
```

Auth engines described:

```text
Rod: fast, may trigger captchas
Camoufox: anti-detect browser that bypasses captchas
```

Troubleshooting note:

```text
Account Hangs: Try disabling Headless Mode in Dashboard Settings to see the login process.
```

## Architecture lessons worth extracting

Useful control-writing-planse ideas:

- local OpenAI-compatible facade
- dashboard for account/provider status
- provider/account inventory
- sticky routing by account/session
- health checks and automatic recovery
- fallback routing
- LAN exposure with whitelist
- headless/headful browser auth debugging
- model alias layer

These map well onto a clean 9Router-style system when using owned/paid provider access.

## Abuse-sensitive patterns to avoid

Do not copy:

- fresh-account farming
- no-2FA/no-phone account requirements as an operating dependency
- CAPTCHA/anti-bot bypass claims
- `email:password` plaintext account files as a primary secret store
- account rotation to multiply free-trial quota
- content filters meant to evade upstream blocking

## Galyarder-compatible interpretation

A clean Galyarder version should be:

```text
owned/paid accounts and keys
  -> provider adapters
  -> encrypted/permission-locked secret store
  -> account/key health checker
  -> quota/cost/rate-limit tracker
  -> OpenAI-compatible router endpoint
  -> Hermes and internal agents
```

Camofox can be used for owned-account assisted login or session refresh, not for mass signup or CAPTCHA evasion.

If the user asks whether such systems are technically possible, answer yes at the architecture level, then keep implementation outlines on the owned-account/provider-manager path.
