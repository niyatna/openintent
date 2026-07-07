# Bitwarden agent account bootstrap + readiness check (2026-05-29)

Use this when bootstrapping a Keiya/Galyarder-owned Bitwarden account from a private `account.txt`, verifying organization access, and preparing for later Bitwarden Secrets Manager (`bws`) setup without migrating secrets yet.

## Scope

This is **login/session bootstrap + readiness proof only**:

- validate the private `account.txt` shape and permissions;
- log in / prove Bitwarden account usability;
- save browser storage/cookies private-only where possible;
- verify organization visibility for the agent account;
- do **not** create/playwright-pro/sync Secrets Manager secrets unless Galih explicitly approves.

Never print passwords, master passwords, access tokens, refresh tokens, keys, cookies, invite links, recovery codes, or raw storage.

## Private paths

```text
/home/galyarder/.hermes/private/credentials/agents/<owner>/bitwarden/account.txt
/home/galyarder/.hermes/private/credentials/agents/<owner>/bitwarden/cookies.json
/home/galyarder/.hermes/private/credentials/agents/<owner>/bitwarden/storage-state.cloakbrowser.json
/home/galyarder/.hermes/private/browser-profiles/agents/<owner>/bitwarden-cloakbrowser
```

Directory mode should be `700`; credential/session files mode should be `600`.

## Account validation

Use the normal account checker, requiring at least email + password/master password presence:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/autonomous-ai-agents/agent-accounts/scripts/account_check.py \
  --account-file /home/galyarder/.hermes/private/credentials/agents/<owner>/bitwarden/account.txt \
  --require EMAIL --require PASSWORD
```

The checker masks public fields; do not dump the raw file.

## API-first readiness proof

Bitwarden web vault can be slow or headless-fragile. For readiness, the most reliable proof is direct web-vault API login using the account's private master password hash flow:

1. `POST https://vault.bitwarden.com/identity/accounts/prelogin/password` with the account email.
2. Read `kdf`, `kdfIterations`.
3. For PBKDF2_SHA256 (`kdf=0`):
   - `masterKey = PBKDF2-HMAC-SHA256(password, lower(email), kdfIterations, 32)`
   - `masterPasswordHash = PBKDF2-HMAC-SHA256(masterKey, password, 1, 32)`
   - base64-encode `masterPasswordHash`.
4. `POST https://vault.bitwarden.com/identity/connect/token` with:
   - `grant_type=password`
   - `username=<email>`
   - `password=<base64 masterPasswordHash>`
   - `scope=api offline_access`
   - `client_id=web`
   - `deviceType=10`
   - owner-specific `deviceIdentifier` / `deviceName`.
5. Use the bearer token only in-process to check:
   - `GET /api/accounts/profile`
   - `GET /api/sync?excludeDomains=true`
   - `GET /api/organizations`
6. Redact all token/key/privateKey fields from output.

Readiness evidence for agent account:

```text
prelogin=200
identity/connect/token=200
/api/accounts/profile=200
/api/sync=200
/api/organizations=200
org_visible=true for galyarder-labs
```

This proves the **account + org access** are usable for the next Secrets Manager setup. It does not by itself playwright-pro secrets or prove `bws` token/project wiring.

## Browser storage proof caveat

Bitwarden Web Vault commonly persists usable web state in `localStorage`, not ordinary cookies. It is valid to see:

```text
cookies.json: []
storage-state.cloakbrowser.json: cookies=0, origins=1, origin=https://vault.bitwarden.com, localStorage keys present
```

Do not report cookie count `0` as failure if API login works and `storage-state.cloakbrowser.json` has Bitwarden localStorage. Say: `browser session saved via storage-state/localStorage; cookies may be empty`.

## Invite/admin-status pitfall

Do not infer `admin approval needed` from generic Bitwarden email text alone. Verify live admin/member state:

- row status `Diundang` / `Invited` means the invite acceptance/email flow is still incomplete;
- an empty `Needs confirmation` tab means the real blocker is **not** admin confirmation;
- next action is resend/fresh invite + accept from the invited account side, not telling Galih to search for a missing approval button.

If direct invite acceptance returns `Invalid token`, ask Galih/admin to resend the invitation, then accept the newest invite. Treat old invite links as invalidated by account creation/reinvite churn.

## CloakBrowser profile pitfall

If an interrupted headless run leaves `SingletonLock` / `SingletonSocket` / `SingletonCookie` under a persistent Bitwarden profile, do not delete the files casually during an account task. First verify no matching Chromium process is using the profile. If deletion would be considered destructive in the current interaction, use a fresh owner-scoped profile suffix (for example `bitwarden-cloakbrowser-active`) and document the old stale profile for later cleanup.

## Status field convention

For `account.txt`, useful non-secret statuses:

```text
invited-email-accepted-account-created-not-confirmed
api-login-active-org-visible
api-login-active-org-visible-browser-session-localstorage-saved
blocked-invalid-credentials
needs-2fa
needs-email-verification
blocked-login-error
```

Keep `STATUS` factual and current. Do not store one-off logs or raw API responses in the credential file.

## BWS boundary

After account/org readiness is proven, the next setup still needs explicit Galih approval for Secrets Manager wiring:

- Bitwarden Secrets Manager project/scope;
- machine account (`keiya-hermes` / `galyarder-hermes`);
- access token stored in the profile-specific env var (`KEIYA_BWS_ACCESS_TOKEN` or `GALYARDER_BWS_ACCESS_TOKEN`);
- `hermes secrets bitwarden setup` / `sync` only after approval.

Until then, keep Hermes Bitwarden integration disabled or dry-run only.