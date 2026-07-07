# Dedicated agent GitHub PAT automation notes

Use this when promoting a dedicated agent-owned GitHub browser account into CLI/API access for Hermes profiles such as Keiya or Galyarder.

## Durable lesson

A successful GitHub browser login is not enough for `gh`, Git HTTPS, or REST API work. GitHub treats personal access token creation as a separate security-sensitive action and may require sudo-mode verification even when the session is already authenticated.

## Recommended design

- Keep Galih's main `gh` auth separate from agent-owned GitHub identities.
- Use one fine-grained PAT per dedicated agent account/profile.
- Store the PAT only in a local private token file such as:
  - `/home/galyarder/.hermes/private/credentials/agents/<owner>/github/token.env`
- Run `gh` through a wrapper that injects token environment variables and a per-agent config directory.
- Verify identity before any repo mutation: expected login must equal the dedicated account, not the human owner account.

## Permission baseline

Prefer fine-grained PATs over classic PATs.

Baseline repository permissions:

- Metadata: read
- Contents: read/write
- Pull requests: read/write
- Issues: read/write
- Actions: read, or write only if the agent must trigger/manage workflow runs
- Workflows: write only if the agent must edit `.github/workflows/*`

Avoid by default:

- repository deletion permission
- organization admin permissions
- broad all-repository access
- classic PATs, unless a GitHub limitation forces them

## GitHub web PAT creation pitfalls

Observed during dedicated Keiya/Galyarder token setup:

- Opening the fine-grained PAT creation page from an active browser session can still redirect to **Confirm access** / sudo mode.
- Keiya reached sudo email verification as the dedicated account; automated Gmail code retrieval submitted a stale or wrong code once and GitHub returned `Sudo authentication failed`.
- Galyarder reached the fine-grained PAT form as the dedicated account; URL query parameters prefilled the intended permissions, but form submission did not return a token in the headless automation attempt.
- Do **not** try to get a dedicated-account token via `gh auth login --web` when the OS/user browser is logged into Galih's human GitHub account; GitHub CLI device/web OAuth will authorize the currently active browser account and can silently produce a token for the wrong login. If a wrong-account token is captured, delete it immediately and verify no token remains.
- If fine-grained PAT automation fails, use the dedicated account's GitHub web settings page for a classic PAT (`https://github.com/settings/tokens/new`) as the direct fallback, scoped minimally (e.g. `repo`, `workflow`, `read:user`) and then verify with the per-agent wrapper. Classic PAT worked for Keiya/Galyarder when fine-grained PAT form automation redirected to `/repos` without exposing a token.
- Therefore: do not claim token creation from web login alone. Only claim success after capturing a PAT and verifying it through the per-agent wrapper.

See `references/dedicated-agent-profile-backup-repos-2026-05-16.md` for the session pattern that created dedicated-account profile backup repos and pushed clean profile distributions using per-agent tokens without leaking secrets.

## Safe automation stance

It is acceptable to automate the owned-account flow, but keep the boundary strict:

1. Browser login/session check proves web login only.
2. PAT creation may require user-visible sudo/email verification.
3. If automation hits sudo/email/form validation friction, switch to a one-time visible human-in-loop flow instead of thrashing.
4. Save only the resulting PAT to the local private token file.
5. Report sanitized state only: token missing/present, expected login, actual login, wrapper verification status.

## Verification

Run the per-agent wrapper check after saving the token. Expected sanitized success:

```json
{
  "ok": true,
  "status": "github-token-valid",
  "expected_login": "<dedicated-account>",
  "actual_login": "<dedicated-account>"
}
```

Never print PATs, OTPs, backup codes, or raw cookies in chat, logs, Obsidian, memory, or skill files.
