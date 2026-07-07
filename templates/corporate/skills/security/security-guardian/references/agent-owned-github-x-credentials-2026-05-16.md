# Agent-owned GitHub/X credential rollout — 2026-05-16

Session-specific lessons from promoting Keiya/Galyarder GitHub and X accounts from placeholders to credentialed local identities.

## What changed

- User provided updated username/email/password credentials for two GitHub accounts and two X accounts.
- Credentials were saved only to private local account files under `/home/galyarder/.hermes/private/credentials/agents/.../account.txt` with `0600` file mode.
- No secrets were stored in Obsidian, memory, profile repos, or final chat output. Status reporting used only presence booleans and sanitized state strings.

## Durable patterns

### GitHub web login is not enough

A GitHub browser session can prove the account is logged in, but it does not give CLI/API access. PAT generation still triggers separate security gates such as sudo mode and email verification.

Recommended reporting distinction:

- `github-login-active`: browser/web session active.
- `token-missing`: no local PAT for CLI/API access.
- `github-token-valid`: wrapper verified PAT identity with expected login.

### Per-agent GitHub wrappers

Use per-agent token files plus per-agent `GH_CONFIG_DIR` so the human owner's global `gh` auth is not overwritten.

Verification shape:

```bash
/home/galyarder/.hermes/scripts/keiya-gh --check
/home/galyarder/.hermes/scripts/galyarder-gh --check
```

Expected sanitized proof: actual login equals the dedicated account username.

### GitHub 2FA setup

GitHub authenticator setup can expose a setup key before the account has actually enabled 2FA. That key must not be persisted as operational until GitHub accepts a TOTP code and shows the success/recovery-code step.

If GitHub returns `Two-factor code verification failed`, clear any attempted `TOTP_SECRET`, mark the account pending/failed, and do not claim 2FA is enabled.

### X credentials

A stored X username/email/password is not the same as an X browser session or API access. Use statuses like `credential-stored-x-login-pending` until login/session is verified. Cookies should be saved only after successful login.

## Audit implication

Credential audits for operational GitHub/X accounts should require:

- private directories `0700`;
- account/token/cookie files `0600`;
- no disallowed secret fields such as private keys, seed phrases, raw backup codes, or broad tokens in generic account files;
- password present for credentialed login;
- TOTP state explicitly tracked as configured, pending, not configured, or verify failed.

Do not blanket-fail GitHub/X operational accounts just because `TOTP_SECRET` is empty during a pending 2FA rollout; require explicit tracked state instead.
