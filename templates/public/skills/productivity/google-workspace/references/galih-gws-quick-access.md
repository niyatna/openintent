# Reference: google-workspace

# Galih GWS Quick Access

## Overview

Galih's own Google Workspace access uses the default/native `gws` config, not Keiya or Galyarder isolated configs.

Core rule: **use `gws` first. Do not open browser unless the token is actually broken.**

This skill exists for fast access to Galih's Google Workspace account and to prevent routing confusion with:

- Keiya: `google-workspace` → `/home/galyarder/.config/gws-keiya`
- Galyarder Labs: `google-workspace` → `/home/galyarder/.config/gws-galyarder`
- Galih: `google-workspace` → `/home/galyarder/.config/gws`

## Known Galih GWS State

```text
account: mhmdgalihsaputra249@gmail.com
primary delivery email outside GWS: muhamadgalihsaputra@proton.me
gws binary: /home/galyarder/.local/bin/gws
config dir: /home/galyarder/.config/gws
client file: /home/galyarder/.config/gws/client_secret.json
credentials file: /home/galyarder/.config/gws/credentials.enc
project id: galih-org
helper: /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galih-gws.sh
```

Do not treat Proton as Google Workspace identity. Proton is the home/delivery email; Galih's current GWS account is the Gmail above unless reconfigured later.

## Fast Route

```bash
GWSU="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galih-gws.sh"
$GWSU auth status
```

For read-only tasks, use the requested `gws` call through `$GWSU`.

For side effects, draft first and ask Galih for approval unless Galih already gave the exact action/content.

## Helper Environment

The helper sets:

```bash
HOME=/home/galyarder
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/home/galyarder/.config/gws
```

and unsets:

```bash
GOOGLE_WORKSPACE_CLI_TOKEN
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE
```

It intentionally does **not** force `GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file` because Galih's default/native setup currently uses the normal keyring-backed encrypted credentials. Let `gws` choose its native backend.

## Quick Verification Commands

Use one or two checks before normal work; run all checks after setup/repair.

```bash
# Token/auth shape
$GWSU auth status

# Gmail profile
$GWSU gmail users getProfile --params '{"userId":"me"}'

# Gmail metadata read
$GWSU gmail users messages list --params '{"userId":"me","maxResults":1}'

# Drive account/storage
$GWSU drive about get --params '{"fields":"user,storageQuota"}'

# Calendar primary list
$GWSU calendar calendarList list --params '{"maxResults":1}'

# People profile read
$GWSU people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
```

Sheets and Docs need real file IDs. A dummy-ID 404 means the API route is alive, not that a file exists.

```bash
$GWSU sheets spreadsheets get --params '{"spreadsheetId":"SHEET_ID"}'
$GWSU docs documents get --params '{"documentId":"DOC_ID"}'
```

## Normal CRUD Map

Always prefer the API/CLI route when token is healthy.

| Need | Fast route |
|---|---|
| Gmail search/list/read | `$GWSU gmail users messages ...` or `google-workspace` syntax |
| Gmail send/reply | draft + approval → `$GWSU gmail ...` |
| Calendar list/read | `$GWSU calendar calendarList/events ...` |
| Calendar create/update/delete | draft + approval → `$GWSU calendar ...` |
| Drive search/list/read metadata | `$GWSU drive ...` |
| Drive/Docs/Sheets create/update/share/delete | draft + approval → `$GWSU ...` |
| Docs/Sheets read by ID | `$GWSU docs ...` / `$GWSU sheets ...` |
| People/profile | `$GWSU people people get ...` |

Load `google-workspace` only when exact command syntax is needed.

## Acceptance Criteria

Galih GWS is ready only when:

- config dir exists and is private (`700`);
- `credentials.enc` exists and decrypts (`encryption_valid: true` in `auth status`);
- plaintext `credentials.json` does not exist;
- `auth status` reports `token_valid: true`;
- `auth status` user/account is `mhmdgalihsaputra249@gmail.com`;
- Gmail profile returns the same account;
- Gmail metadata list succeeds;
- Drive about succeeds;
- Calendar list succeeds;
- helper uses `/home/galyarder/.config/gws`, not Keiya/Galyarder configs;
- this skill loads from the active Galyarder profile.

## Browser/Reauth Rule

Do **not** open browser for normal access.

Open Brave CDP only when live `gws` proof fails with one of these auth signals:

- `token_valid: false`
- `invalid_grant`
- refresh token revoked/expired
- `NOT_AUTHENTICATED`
- OAuth scope mismatch that requires re-consent
- repeated API calls fail specifically because auth is broken, not because an API is disabled or a file ID is wrong

When browser reauth is needed, route through Brave CDP because this is Galih's own account and Brave is the human-facing cockpit.

Required support route:

1. Load `browser-routing`.
2. Verify Brave CDP: `curl -s http://127.0.0.1:9222/json/version`.
3. Run `gws auth login` with the needed service/scope set.
4. Let it open or paste the OAuth URL into Brave CDP / real Brave.
5. Complete Google consent in Brave as Galih.
6. Return redirected URL/code if `gws` asks for it.
7. Rerun `$GWSU auth status`.
8. Rerun at least Gmail profile + one Drive or Calendar smoke check.

If CDP is down but Brave is already usable, use the real Brave fallback from `browser-routing` rather than Camofox. Do not use Camofox/CloakBrowser for Galih's personal GWS unless Galih explicitly overrides this skill.

## Failure Routing

| Symptom | Meaning | Next route |
|---|---|---|
| `token_valid: true` and target API succeeds | GWS ready | Continue task |
| Account is not `mhmdgalihsaputra249@gmail.com` | Wrong config/env bleed | Use helper; inspect env |
| `client_config_error` | Bad OAuth client file shape | Repair client file through `google-workspace` |
| `accessNotConfigured` / `SERVICE_DISABLED` | API disabled on project | Enable API; do not rerun OAuth first |
| `403 insufficientPermission` | Missing scope | Brave CDP reauth with correct scopes |
| `serviceusage.services.use` | OAuth project/IAM/quota blocker | Fix project/IAM/quota; do not assume token broken |
| `invalid_grant`, revoked, no refresh token | Token broken | Brave CDP reauth |
| Google verification/CAPTCHA/account gate | Human account gate | Stop, report blocker, ask Galih to complete gate if needed |

## Approval Boundaries

Autonomous after live auth check:

- Gmail search/list/read metadata or messages Galih asks to inspect;
- Drive search/list/read metadata;
- Docs/Sheets read by ID/search when non-destructive;
- Calendar list/read;
- People profile/contact read.

Requires Galih approval before execution:

- send/reply email;
- create/update/delete Calendar events;
- create/update/delete/share Drive/Docs/Sheets files;
- public sharing or permission changes;
- deleting messages/files/events;
- billing/security/account setting changes;
- browser reauth if it requires entering sensitive personal gates beyond ordinary OAuth consent.

## Common Mistakes

- Opening browser before checking `gws auth status`.
- Using Keiya/Galyarder helper for Galih's own account.
- Treating a dummy Docs/Sheets 404 as auth failure.
- Treating API disabled/IAM/quota errors as token failure.
- Forcing file keyring backend and breaking the native default setup.
- Printing OAuth token/client secret/credential files.
- Sending email or modifying Calendar/Drive without approval.
- Confusing Proton delivery identity with Google Workspace account identity.

## Report Shape

Keep it short:

```text
galih gws: ready / auth-required / blocker
verified: Gmail/Drive/Calendar/etc.
result: <id/count/link/summary>
needs approval: <only if side effect or reauth gate>
```