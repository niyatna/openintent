# Agent Accounts & Credentials Reference Guide

This reference provides a consolidated, generic guide for managing, bootstrapping, and verifying dedicated agent-owned accounts and credentials (such as GitHub personal access tokens, Bitwarden Secrets Manager integrations, and persistent browser session states).

---

## 1. Directory Structure & Security Invariants

All private credentials, cookies, and local session states must reside in gitignored directory structures outside the codebase. 

### Local Credential Storage Patterns
```text
~/.hermes/private/credentials/agents/<profile>/
  bitwarden/
    account.txt                 # Master emails and password hashes (mode 600)
    cookies.json                # Saved session cookies (mode 600)
    storage-state.camofox.json  # Browser localStorage state (mode 600)
  github/
    token.env                   # Github PAT tokens and scopes (mode 600)
```

### System Security Guidelines
- **Directory Mode**: `700` (restricted to the operating user).
- **File Mode**: `600` (restricted read/write).
- **Secret Hygiene**: Never print passwords, master keys, tokens, or raw cookies to stdout, logs, or chat interfaces. Filter out authorization headers in logs.

---

## 2. Bitwarden Agent Account Bootstrap & Verification

Use this workflow to bootstrap a dedicated agent Bitwarden account and verify API-level organization access before Secrets Manager deployment.

### API-First Verification Flow
Because headless browser interaction with the Bitwarden vault is fragile under headless environments, verify credential readiness directly via the identity API:

1. **Prelogin Check**: `POST https://vault.bitwarden.com/identity/accounts/prelogin/password` with the account email.
2. **KDF Derivation** (PBKDF2_SHA256):
   - `masterKey = PBKDF2-HMAC-SHA256(password, lower(email), kdfIterations, 32)`
   - `masterPasswordHash = PBKDF2-HMAC-SHA256(masterKey, password, 1, 32)`
3. **Token Request**: `POST https://vault.bitwarden.com/identity/connect/token` using the derived `masterPasswordHash`, requesting scope `api offline_access`.
4. **Validation Check**: With the retrieved bearer token, verify access via:
   - `GET /api/accounts/profile`
   - `GET /api/sync?excludeDomains=true`
   - `GET /api/organizations` (Confirms organization mapping is active).

### Local Session Persistence
Bitwarden commonly uses `localStorage` rather than regular cookies. A successful session state save may output an empty `cookies.json` but must have origin-specific localStorage keys in `storage-state.camofox.json`.

---

## 3. GitHub Agent PAT Regeneration & 2FA Checkup

When headless GitHub actions fail with `410 Bad credentials`, the Personal Access Token (PAT) needs manual regeneration through the agent's persistent browser context.

### Handling 2FA Checkup Redirects
1. If GitHub redirects setting paths to `/settings/two_factor_checkup`, click **"Verify 2FA now"**.
2. Retrieve the base32 `TOTP_SECRET` from local credentials, generate the one-time code, and submit it into the `input[name="app_otp"]` field.
3. **Critical**: Always click **"Done"** after successful verification to save the session state on the lock page.

### Token Regeneration Flow
1. Navigate directly to the token URL: `https://github.com/settings/tokens/<token_id>/regenerate?index_page=1`.
2. Autofill the password verification (`#sudo_password`) from credentials if prompted.
3. Click the `Regenerate token` submission button.
4. Extract the newly minted token matching `/^ghp_[A-Za-z0-9]+$/` from `.token-value` or custom selectors. Save immediately to `token.env`.
5. Verify using the CLI:
   ```bash
   GH_TOKEN=<token> gh api user --jq '.login'
   ```

### Membership Acceptance
Accept pending organization invitations programmatically:
```bash
GH_TOKEN=<token> gh api --method PATCH /user/memberships/orgs/<org_name> -f state=active
```
