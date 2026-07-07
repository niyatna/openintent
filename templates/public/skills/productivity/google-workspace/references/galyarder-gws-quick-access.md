# Reference: google-workspace

# Galyarder GWS Quick Access

## Overview

Galyarder's Google Workspace access is authenticated through an isolated `gws` config. Use this skill for fast Workspace API work without bleeding into Galih's global/default keyring or Keiya's config.

Core rule: for Galyarder account work, always use the helper script. Do not raw-call `gws` unless you manually set the same environment.

## Known Galyarder GWS State

```text
account: galyarderlabs@gmail.com
gws binary: /home/galyarder/.local/bin/gws
config dir: /home/galyarder/.config/gws-galyarder
client file: /home/galyarder/.config/gws-galyarder/client_secret.json
credentials file: /home/galyarder/.config/gws-galyarder/credentials.enc
helper: /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galyarder-gws.sh
```

The OAuth project is `galyarder-agent`. If OAuth is rerun and Google shows an unverified-app screen, expand **Advanced / Lanjutan**, continue to the app, select all requested scopes, and continue. This is expected for the local test app path; do not call it complete until live API smoke tests pass.

## Fast Route

```bash
GWSG="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galyarder-gws.sh"
$GWSG auth status
```

For read-only tasks, use the requested `gws` call through `$GWSG`. For side effects, draft first and ask Galih for approval unless Galih gave the exact action.

## Helper Environment

The helper sets:

```bash
HOME=/home/galyarder
GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/home/galyarder/.config/gws-galyarder
GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file
```

and unsets:

```bash
GOOGLE_WORKSPACE_CLI_TOKEN
GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE
```

This forces the isolated encrypted credentials under `/home/galyarder/.config/gws-galyarder`.

## Quick Verification Commands

Use one or two checks before normal work; run all checks after setup/repair.

```bash
# Token/auth shape
$GWSG auth status

# Gmail profile
$GWSG gmail users getProfile --params '{"userId":"me"}'

# Gmail metadata read
$GWSG gmail users messages list --params '{"userId":"me","maxResults":1}'

# Drive account/storage
$GWSG drive about get --params '{"fields":"user,storageQuota"}'

# Calendar primary list
$GWSG calendar calendarList list --params '{"maxResults":1}'

# People profile read (fast People API proof)
$GWSG people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'

# People contacts read (can be slower on large contact sets)
$GWSG people people connections list --params '{"resourceName":"people/me","pageSize":1,"personFields":"names,emailAddresses"}'
```

Sheets and Docs generally need real file IDs. A `404 Requested entity was not found` on a dummy ID proves the API route is alive but not the file.

## Acceptance Criteria

Galyarder GWS is considered ready only when:

- config dir exists and is private (`700`);
- OAuth credentials/token state is isolated under `/home/galyarder/.config/gws-galyarder`;
- `auth status` reports `token_valid: true` and user/account is `galyarderlabs@gmail.com`;
- Gmail profile returns `galyarderlabs@gmail.com`;
- Gmail metadata list succeeds;
- Drive about returns the Galyarder account;
- Calendar primary list succeeds;
- People profile read exits without auth/API error;
- helper script loads and uses isolated env;
- this skill is loadable in the active Galyarder profile;
- no `client_config_error` appears in `auth status`.

## Approval Boundaries

Autonomous after live auth check:

- Gmail search/list/read metadata or messages Galih asks to inspect
- Drive search/list/read metadata
- Docs/Sheets read by ID/search when non-destructive
- Calendar list/read
- People contacts/profile list/read

Requires Galih approval before execution:

- send/reply email
- create/update/delete Calendar events
- create/update/delete/share Drive/Docs/Sheets files
- public sharing or permission changes
- deleting messages/files/events
- billing/security/account setting changes

## Failure Routing

| Symptom | Meaning | Next route |
|---|---|---|
| `token_valid: true` and target API succeeds | GWS ready | Continue task |
| Account is not `galyarderlabs@gmail.com` | Wrong keyring/config bleed | Use helper; inspect env |
| `client_config_error` | Bad OAuth client file shape | Replace with Desktop/installed-format client secret |
| `accessNotConfigured` / `SERVICE_DISABLED` | API disabled on project | Enable API; do not rerun OAuth |
| `serviceusage.services.use` / Service Usage Consumer block | OAuth project IAM blocker | Grant `roles/serviceusage.serviceUsageConsumer` or use allowed project, then rerun smoke |
| `invalid_grant`, revoked, no refresh token | Token broken | Load `google-workspace` + `agent-accounts` + `camofox-browser`; redo OAuth |
| Google unverified app screen | Local OAuth app not verified | Advanced → continue only for owned account/local setup |
| `403 access_denied` test-user block | Account not in OAuth test audience or wrong OAuth project | Add account as test user or use correct OAuth client |
| `403 insufficientPermission` | Missing scope | Re-OAuth with correct scopes via Camofox |

## Common Mistakes

- Running raw `/home/galyarder/.local/bin/gws` and accidentally using Galih's global config.
- Reusing Keiya's helper/config for Galyarder.
- Treating OAuth browser success as done before API smoke tests.
- Printing token/client-secret/credential files while debugging.
- Sending email or modifying files/events without Galih's approval.
- Using `people.connections` as a top-level command; correct nested syntax is `people people connections list`.

## References

- `references/verification-2026-05-18.md` — last verified Galyarder GWS snapshot, exact smoke commands, and correct People command syntax. Rerun smoke before current-state claims.

## Report Shape

```text
galyarder gws: ready / blocker
verified: Gmail/Drive/Calendar/People/etc.
result: <id/count/link/summary>
needs approval: <only if side effect>
```