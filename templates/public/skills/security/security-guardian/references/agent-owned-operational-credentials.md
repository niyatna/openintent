# Agent-owned operational credentials

Use this reference when a writing-plansned agent-owned account skeleton is promoted into a real operational identity for Keiya, Galyarder, or another Hermes profile.

## Core boundary

Operational credentials are allowed only after explicit user approval for the account class and owner. Once approved, local private credential files may contain password and TOTP material, but the same secret boundary still applies:

- keep secret values local-only;
- never print, commit, screenshot, store in Obsidian, store in memory, or write into skill files;
- report only status, presence, length, path class, and verification result;
- keep profile-distribution repos free of runtime credentials, cookies, token files, keystores, raw sessions, and backup codes.

## Skeleton vs operational account

Treat these as different states.

### Planned skeleton

A writing-plansned skeleton is a placeholder. It should contain non-secret metadata only: owner, service, account id, email/username, notes, and references to future secret paths.

Verifier expectation: no populated secret fields.

### Operational dedicated account

An operational dedicated account has been explicitly promoted by the user and may contain local-only password/TOTP recovery material.

Verifier expectation: permissions and disallowed-secret checks, not a blanket failure for `PASSWORD` or `TOTP_SECRET`.

Allowed operational secret fields in private account files:

- `PASSWORD`
- `TOTP_SECRET`

Still disallowed in plaintext generic account files unless a stronger encrypted design exists:

- API tokens
- private keys
- seed phrases
- raw backup codes
- broad OAuth refresh tokens outside the intended auth store

## Google Authenticator setup pattern

For dedicated Google accounts:

1. Store the account email/password in the local private account file.
2. Sign in through isolated browser automation or a human-controlled trusted browser session.
3. Open Google Account security / 2-Step Verification / Authenticator.
4. Prefer the manual setup key over QR extraction.
5. Extract the base32 manual key without printing it.
6. Save it as `TOTP_SECRET` only after confirming it is the active Google-provided setup key, not a local placeholder.
7. Generate the 6-digit code with `pyotp` as late as possible after the verification form is visible; early codes can expire and cause wrong-code errors.
8. Verify the success signal: authenticator listed, added, or setup complete.
9. Save cookies/session state only to the private runtime path.
10. Update the account `STATUS` to the verified state.

Never claim TOTP is operational just because a local placeholder secret exists. It must be registered with the service.

## Browser/auth automation notes

For account setup automation, favor a short local script that reads private files and prints sanitized JSON. The script may access secrets internally, but output must not include them.

Sanitized output examples:

- `password_present=true`
- `totp_len=32`
- `cookie_count=25`
- `status=login-active-totp-registered`

Avoid printing raw OTP codes. They are short-lived but still credentials.

## GitHub and X signup gates

Prepare credentials and check username availability, but do not claim an account exists until platform state verifies it.

Common gates:

- Google OAuth handoff;
- email verification;
- CAPTCHA / human verification;
- phone verification;
- X developer access or billing requirement.

When blocked, record the gate and next required human action. Do not attempt CAPTCHA bypass, phone-farm behavior, or mass signup logic.

### GitHub dedicated token pattern

A GitHub browser session/cookie proves web login only. It does **not** give `gh`, Git, or API access. Dedicated agent-owned GitHub identities need a separate token/SSH design for CLI/API work.

Preferred approach:

- one fine-grained PAT per dedicated agent account/profile;
- selected repositories only;
- baseline permissions: Metadata read, Contents read/write, Pull requests read/write, Issues read/write;
- add Actions/Workflows permissions only when the profile must trigger or edit workflows;
- avoid `delete_repo`, org-admin, all-repo, or classic broad tokens unless a GitHub limitation forces it.

Isolation rule: do not overwrite the human owner's global `gh` auth. Use token environment variables plus per-agent `GH_CONFIG_DIR`, then verify `gh api user --jq .login` equals the expected dedicated account before any repo mutation. If the login resolves to the human owner's account, stop and fix token routing.

GitHub PAT creation may require sudo mode, fresh email verification, or additional UI validation even after password login succeeds. When automating PAT creation, treat these as verification gates and never claim a token exists until the generated PAT has been saved and the per-agent wrapper verifies the expected login.

Report only sanitized token state: token missing/present, expected login, actual login, permission class, and verification result. Never print PAT values.

### GitHub TOTP setup pattern

For dedicated GitHub accounts, user-provided username/password can be stored in the private account file after approval, but 2FA is not operational until GitHub accepts the TOTP code and shows a success/recovery-code step.

Observed pitfalls:

- GitHub may request email-based sudo verification before security actions.
- Email verification codes can be stale; automated Gmail search can pick an older code unless it narrows to the newest fresh GitHub message.
- The setup page can expose a TOTP setup key before 2FA is actually enabled. Do not persist that key as active unless the verify step succeeds.
- A pyotp-generated code can fail because of timing, form-submission semantics, or session state. If GitHub returns “Two-factor code verification failed”, clear any attempted `TOTP_SECRET` and mark the state as failed/pending rather than pretending 2FA is enabled.
- Save recovery codes only after the success/recovery-code page is visible; raw backup codes remain local-only and never belong in chat, Obsidian, memory, or profile repos.

Sanitized statuses worth tracking: `credential-stored-pending-github-2fa`, `github-totp-verify-failed`, `github-2fa-enabled`, and `github-2fa-enabled-pending-recovery-save`.

### X session/cookie boundary

For X, cookies are an artifact saved **after** a successful login; they are not a substitute for the login. If Google cookies are valid but X returns to the public landing page with no X cookies/session, classify it as an auth/session-handoff block, not as missing local credentials.

Preferred order:

1. official X OAuth/API tooling when available and appropriate;
2. one human-in-loop visible-browser login/verification for a dedicated account;
3. saved browser cookies as fallback runtime state after login succeeds.

Do not build CAPTCHA bypass, phone-farm, or mass-signup logic.

## Wallet foundation boundary

Local EVM wallet foundation may create an encrypted keystore and public address, but that is not production agentic-wallet autonomy.

Default status should be read-only / no funds / no signing until there is explicit policy for:

- network;
- spend limit;
- allowlisted destination/contracts;
- recovery path;
- transaction approval threshold;
- monitoring and revocation.

### Coinbase Agentic Wallet pattern

When the user asks for a production-grade agentic wallet, prefer a managed/guardrailed agentic-wallet provider path over exposing local private keys to the agent.

For Coinbase CDP Agentic Wallet:

- **Agentic Wallet MCP / payments-mcp** is the safer first path for Hermes-style agents: wallet address, balance, x402 service discovery, payment-requirement checks, and x402 requests. User-only controls should remain user-only: adding funds/onramp, transfer-out, and spend-limit changes.
- **Agentic Wallet CLI / `awal`** is more powerful because it can send/trade/x402-pay. Treat send/trade as transaction capability requiring explicit spend limits, allowlists, confirmation thresholds, monitoring, and revocation before operational autonomy.
- Electron/companion-wallet setup can require visible UI/auth. Capture the install/auth repair steps if needed, but do not harden a transient headless startup failure into “the wallet does not work.”

Never store plaintext seed phrases or private keys in generic account files.

## Verification checklist

Before reporting operational status:

- private directories are `700`;
- credential files, cookies, and keystores are `600`;
- no secrets are in profile-distribution diffs;
- TOTP generation works from the stored secret;
- login/session claim is backed by an actual page/API/cookie/session check;
- public/social/wallet actions remain confirmation-gated unless a scoped policy exists;
- access-hardening or equivalent verifier understands skeleton vs operational account states.