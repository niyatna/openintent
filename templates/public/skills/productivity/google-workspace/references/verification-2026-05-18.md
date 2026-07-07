# Galyarder GWS verification snapshot — 2026-05-18

This is the last known verified state for the dedicated Galyarder Google Workspace account. Treat it as a snapshot; rerun live smoke checks before acting on current mail/drive/calendar state.

## Account and paths

```text
account: galyarderlabs@gmail.com
config dir: /home/galyarder/.config/gws-galyarder
profile skill: /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/SKILL.md
helper: /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galyarder-gws.sh
gws binary: /home/galyarder/.local/bin/gws
project: galyarder-agent
```

## Verified permissions/state

- config directory mode: `700`
- `credentials.enc`, `token_cache.json`, `client_secret.json`, `.encryption_key`: `600`
- `auth status`: `token_valid=true`
- `auth status user`: `galyarderlabs@gmail.com`
- `client_config_error`: absent
- `plain_credentials_exists`: false
- helper executable: yes
- skill loadable from active Galyarder profile: yes

## Smoke checks that passed

Run through the helper:

```bash
GWSG="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galyarder-gws.sh"
$GWSG auth status
$GWSG gmail users getProfile --params '{"userId":"me"}'
$GWSG gmail users messages list --params '{"userId":"me","maxResults":1}'
$GWSG drive about get --params '{"fields":"user,storageQuota"}'
$GWSG calendar calendarList list --params '{"maxResults":1}'
$GWSG people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
```

Observed good outputs included:

- Gmail profile email: `galyarderlabs@gmail.com`
- Gmail metadata list returned one message id/thread id
- Drive user display name: `Galyarder Labs`
- Drive user email: `galyarderlabs@gmail.com`
- Calendar primary id/summary: `galyarderlabs@gmail.com`
- People profile email: `galyarderlabs@gmail.com`
- People display name: `Galyarder Labs`

## Important syntax note

Correct fast People proof:

```bash
$GWSG people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
```

Correct contacts-list proof:

```bash
$GWSG people people connections list --params '{"resourceName":"people/me","pageSize":1,"personFields":"names,emailAddresses"}'
```

Wrong command shape:

```bash
$GWSG people people.connections list ...
```

That wrong shape fails validation and should not be interpreted as OAuth/API failure.
