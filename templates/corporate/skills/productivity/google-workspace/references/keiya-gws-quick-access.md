# Reference: google-workspace

# Keiya GWS Quick Access

## Overview

Keiya's Google Workspace access is authenticated through an isolated encrypted `gws` config. Use this skill to avoid repeating OAuth/debugging and to prevent `gws` from accidentally using Galih/default or Galyarder keyrings.

Core rule: for Keiya account work, always use the helper script. Do not raw-call `gws` unless you manually set the same environment.

## Known Keiya GWS State

```text
account: keiyazeyniputri@gmail.com
gws binary: /home/galyarder/.local/bin/gws
config dir: /home/galyarder/.config/gws-keiya
client file: /home/galyarder/.config/gws-keiya/client_secret.json
credentials file: /home/galyarder/.config/gws-keiya/credentials.enc
helper: /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/keiya-gws.sh
```

The OAuth project is `galyarder-agent`. The client secret is stored in installed/Desktop shape and `auth status` should have no `client_config_error`.

## Fast Route

```bash
KWS="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/keiya-gws.sh"
$KWS auth status
```

For read-only tasks, use the requested `gws` call through `$KWS`. For side effects, draft first and ask Galih for approval unless Galih gave the exact action.

## Helper Environment

The helper sets:

```bash
HOME=/home/galyarder
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/home/galyarder/.config/gws-keiya
GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file
GOOGLE_WORKSPACE_PROJECT_ID=" "
```

and unsets:

```bash
GOOGLE_WORKSPACE_CLI_TOKEN
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE
```

This forces the isolated encrypted credentials under `/home/galyarder/.config/gws-keiya`, prevents plaintext/export-token precedence, and suppresses the quota-project header that otherwise triggers `serviceusage.services.use` for Keiya's consumer account.

## Quick Verification Commands

Use one or two checks before normal work; run all checks after setup/repair.

```bash
# Token/auth shape
$KWS auth status

# Gmail profile
$KWS gmail users getProfile --params '{"userId":"me"}'

# Gmail metadata read
$KWS gmail users messages list --params '{"userId":"me","maxResults":1}'

# Drive account/storage
$KWS drive about get --params '{"fields":"user,storageQuota"}'

# Calendar primary list
$KWS calendar calendarList list --params '{"maxResults":1}'

# People contacts read (Keiya token currently has contacts.readonly; empty `{}` is valid if no contacts)
$KWS people people connections list --params '{"resourceName":"people/me","pageSize":1,"personFields":"names,emailAddresses"}'
```

People `people/me` profile read requires `profile` scope; Keiya's current token is contacts-focused, so use `people people connections list` as the People smoke unless OAuth is rerun with profile/userinfo scopes.

Sheets and Docs usually need real file IDs. A `404 Requested entity was not found` on a dummy ID means the API route is alive, not that a document exists.

```bash
$KWS sheets spreadsheets get --params '{"spreadsheetId":"SHEET_ID"}'
$KWS docs documents get --params '{"documentId":"DOC_ID"}'
```

## Acceptance Criteria

Keiya GWS is considered ready only when:

- config dir exists and is private (`700`);
- OAuth credentials/token state is isolated under `/home/galyarder/.config/gws-keiya`;
- client secret is installed/Desktop shape;
- `credentials.enc` exists and is decryptable (`encryption_valid: true`);
- plaintext `credentials.json` does not exist;
- `auth status` reports `token_valid: true`, encrypted storage, and no `client_config_error`;
- Gmail profile returns `keiyazeyniputri@gmail.com`;
- Gmail metadata list succeeds;
- Drive about returns the Keiya account;
- Calendar primary list succeeds;
- People connections exits without auth/API error;
- helper script loads and uses isolated env;
- this skill is loadable in the active Galyarder profile.

## Approval Boundaries

Autonomous after live auth check:

- Gmail search/list/read metadata or messages Galih asks to inspect
- Drive search/list/read file metadata
- Docs/Sheets read by ID or search when non-destructive
- Calendar list/read
- People contacts list/read

Requires Galih approval before executing:

- send/reply email
- create/update/delete Calendar events
- create/update/delete/share Drive/Docs/Sheets files
- public sharing or permission changes
- deleting messages/files/events
- billing/security/account setting changes

For approval-required work, draft the exact action/content first, then ask.

## Failure Routing

| Symptom | Meaning | Next route |
|---|---|---|
| `token_valid: true` and target API succeeds | GWS ready | Continue task |
| Account is not `keiyazeyniputri@gmail.com` | Wrong keyring/config bleed | Use helper; inspect env |
| `client_config_error` | Bad OAuth client file shape | Replace with Desktop/installed-format client secret |
| `storage: plaintext` or `plain_credentials_exists: true` | Not clean encrypted setup | Migrate to `credentials.enc`, then remove/disable plaintext file |
| `accessNotConfigured` / `SERVICE_DISABLED` | API disabled on OAuth project | Enable API; do not rerun OAuth |
| `serviceusage.services.use` / Service Usage Consumer block | OAuth project IAM blocker | Grant `roles/serviceusage.serviceUsageConsumer` or use allowed project, then rerun smoke |
| `invalid_grant`, revoked, no refresh token | Token broken | Load `google-workspace` + `agent-accounts` + `camofox-browser`; redo OAuth |
| Google unverified app screen | Local OAuth app not verified | Advanced → continue only for owned account/local setup |
| `403 access_denied` test-user block | Account not in OAuth test audience or wrong OAuth project | Add account as test user or use correct OAuth client |
| `403 insufficientPermission` | Missing scope | Re-OAuth with correct scopes via Camofox |

## Common Mistakes

- Running raw `/home/galyarder/.local/bin/gws ...` and accidentally using Galih/default or Galyarder config.
- Trusting `setup.py --check` for Keiya isolated auth; it may prefer native global `gws` state.
- Rerunning OAuth when the token is valid but an API/project readiness error appears.
- Printing token/client-secret files while debugging.
- Sending email or changing files/events without Galih's approval.
- Using `people.connections` as a top-level command; correct nested syntax is `people people connections list`.
- Using `people people get people/me` as the People smoke without profile/userinfo scopes.

## Report Shape

Keep reports short:

```text
keiya gws: ready / blocker
verified: Gmail/Drive/Calendar/People/etc.
result: <id/count/link/summary>
needs approval: <only if side effect>
```