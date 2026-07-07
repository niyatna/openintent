# Reference: google-workspace

# Google Workspace Auth Troubleshooting

## When to use

Use when Google Workspace status is contradictory:

- direct `gws ...` works but Hermes helper scripts fail
- `gws auth status` shows `token_valid: true` but `setup.py --check` reports `REFRESH_FAILED` or `invalid_grant`
- Google Workspace appears unavailable in Hermes despite live Gmail/Calendar/Drive API calls working
- a wrapper sets `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` or `GOOGLE_WORKSPACE_CLI_TOKEN` and may bypass native `gws` keyring auth

## Core rule

For Galih's host and any modern `gws` install, **native `gws auth status` plus a tiny real API call is the source of truth**. Do not declare GWS broken from a legacy Hermes token check alone.

## Known credential split

Modern `gws` can store credentials in encrypted/keyring-backed files under:

```text
~/.config/gws/credentials.enc
~/.config/gws/token_cache.json
~/.config/gws/client_secret.json
```

Older Hermes Google Workspace helpers may still use:

```text
~/.hermes/google_token.json
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=~/.hermes/google_token.json
GOOGLE_WORKSPACE_CLI_TOKEN=<legacy access token>
```

That legacy token can be expired/revoked while native `gws` remains healthy.

## Diagnostic sequence

```bash
gws auth status
gws gmail users getProfile --params '{"userId":"me"}'
python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail search 'newer_than:1d' --max 1
```

Interpretation:

- If `gws auth status` has `token_valid: true` and direct `gws` API call succeeds, native GWS is healthy.
- If helper scripts fail with `invalid_grant`/`REFRESH_FAILED`, the failure is likely the legacy token path, not Google Workspace itself.

## Fix pattern

Patch helper wrappers to prefer native `gws` auth:

1. Probe `gws auth status` with `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` and `GOOGLE_WORKSPACE_CLI_TOKEN` removed from the probe environment.
2. If `token_valid: true`, do **not** set `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=~/.hermes/google_token.json`.
3. Run `gws` normally so it can use encrypted/keyring credentials.
4. Fall back to `~/.hermes/google_token.json` only when native `gws` is unavailable or invalid.
5. Parse JSON defensively because `gws` may print `Using keyring backend: keyring` before the JSON body.

## Verification before claiming fixed

For ordinary/global Hermes Google Workspace, use the legacy/helper checks:

```bash
python -m py_compile \
  ~/.hermes/skills/productivity/google-workspace/scripts/setup.py \
  ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py \
  ~/.hermes/skills/productivity/google-workspace/scripts/gws_bridge.py

python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail search 'newer_than:1d' --max 1
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py calendar list --calendar primary
python ~/.hermes/skills/productivity/google-workspace/scripts/gws_bridge.py gmail users getProfile --params '{"userId":"me"}'
```

For agent-isolated GWS accounts, verify through the agent helper and active profile skill, not raw/global `gws`:

```bash
GWSA="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/<agent>-gws-quick-access/scripts/<agent>-gws.sh"
$GWSA auth status
$GWSA gmail users getProfile --params '{"userId":"me"}'
$GWSA gmail users messages list --params '{"userId":"me","maxResults":1}'
$GWSA drive about get --params '{"fields":"user,storageQuota"}'
$GWSA calendar calendarList list --params '{"maxResults":1}'
# For Galyarder token with profile scope:
$GWSA people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
# For Keiya token with contacts.readonly but no profile scope:
$GWSA people people connections list --params '{"resourceName":"people/me","pageSize":1,"personFields":"names,emailAddresses"}'
```

Good signals:

- `setup.py --check` reports `AUTHENTICATED: gws token valid ...` for global helper flows
- Galih personal/default helper `google-workspace` reports intended account `mhmdgalihsaputra249@gmail.com`, encrypted storage, and `token_valid: true`
- isolated helper `auth status` reports intended account and `token_valid: true`
- Gmail/Drive/Calendar/People smoke calls succeed
- active profile `skill_view("<agent>-gws-quick-access")` loads the quick-access skill from the profile path
- for Keiya/default local skill proof, `hermes --profile default skills list --source local --enabled-only` is stronger than `skills inspect`, which may resolve registry sources instead of local skills

## Reference cases

- `references/gws-native-vs-legacy-token.md` — session case note with symptoms, root cause, applied fix shape, and verification commands.
- `references/gws-agent-oauth-project-iam-blockers-2026-05-18.md` — OAuth project/IAM blockers where token is valid but API calls fail.
- `references/agent-isolated-gws-profile-skill-and-smoke-2026-05-18.md` — agent-specific isolated config/helper/skill placement and smoke suite; includes active-profile skill loadability and People command syntax.
- `references/agent-isolated-gws-keiya-clean-repair-2026-05-18.md` — Keiya-specific cleanup from Web client/ plaintext token to installed client + encrypted credentials + quota-project suppression.
- `references/galih-personal-gws-quick-access-2026-05-18.md` — Galih personal/default GWS quick-access route, account-specific helper mirroring across Galyarder and Keiya/default skill roots, verification ladder, and Brave CDP-only reauth boundary.

## Pitfalls

- Do not trust `setup.py --check` alone if direct `gws` works.
- Do not overwrite or revoke native `gws` keyring credentials while trying to fix a stale legacy token.
- Do not send test emails or create/delete Calendar events without explicit user confirmation.
- Avoid leaking OAuth tokens/client secrets in logs or summaries; redact credential contents.