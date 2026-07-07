# Agent-owned OAuth and social-login boundaries

Use this reference when promoting dedicated agent-owned accounts (Keiya/Galyarder/Hermes identities) from stored credentials/browser sessions into API tokens, CLI auth, or social-login sessions.

## Core rule

Never treat "a token was produced" or "a cookie file exists" as success. Success is identity-verified operational access for the intended dedicated account.

## GitHub dedicated-account token lessons

- A GitHub browser session plus 2FA proves web access only; it does not prove CLI/API access.
- Fine-grained PAT web automation can submit the form and redirect to `/repos` without ever exposing a `github_pat_...` value. Classify this as `token-not-found-after-submit`; do not save anything.
- `gh auth login --web` can use the currently active browser/GitHub session even when `GH_CONFIG_DIR` is isolated. In practice it may mint/return a token for the human owner account rather than the dedicated account.
- `gh auth token` may print a token even when the interactive `gh auth login --web` process is still waiting or timed out. Token stdout is not proof.
- If a token validates as the wrong account, immediately scrub it from the dedicated account `token.env`; do not keep it as a fallback or report it as partial progress.

## Required GitHub verification

After any token capture attempt:

```bash
/home/galyarder/.hermes/scripts/keiya-gh --check
/home/galyarder/.hermes/scripts/galyarder-gh --check
```

Only accept:

```json
{
  "ok": true,
  "status": "github-token-valid",
  "expected_login": "<dedicated-account>",
  "actual_login": "<same-dedicated-account>"
}
```

If `actual_login` is the human owner or any unexpected account, scrub the token file and report `github-token-invalid-or-wrong-account` / `token-missing` after cleanup.

Sanitized token-file cleanup shape:

```text
GITHUB_TOKEN=
TOKEN_STATUS=removed-wrong-account-token
```

Then re-run wrapper checks.

## X login lessons

- `https://x.com/i/flow/login` may initially render a signup-heavy page with only a `Sign in` link. Click `a[href="/login"]` or `a[href="https://x.com/login"]` first to expose the actual sign-in modal.
- A stored X username/email/password is still only credential state, not an active login/session.
- X may return `Suspicious login prevented` immediately after identifier submission, before the password step. This is a hard observed boundary for that moment; repeated headless retries can worsen the block.
- Save X cookies only after verifying an authenticated surface such as `/home`, `/notifications`, or `/messages` with logged-in UI text.

Recommended status strings:

- `x-login-active`
- `x-login-not-authenticated`
- `x-login-blocked-suspicious-login-prevented`
- `x-login-blocked-verification`
- `credential-stored-x-login-pending`

## Reporting style for urgent credential work

When the user is pressing for speed, do not repeat old blockers first. Execute the next safe attempt, then report a terse state table: attempted, observed, cleaned up, current blocker, next executable move.

Never print PATs, OAuth tokens, passwords, TOTP secrets, backup codes, device codes, or raw cookies in chat, notes, memory, or skill files.
