# Galih personal GWS quick access (2026-05-18)

## What changed

Galih asked for a dedicated quick-access route for his own Google Workspace account, but with a strict boundary:

- normal operation must use `gws` only;
- do not open browser for routine Gmail/Drive/Calendar/Docs/Sheets access;
- if token/auth fails, reauth through Brave CDP / real Brave because this is Galih's own human account;
- do not use Camofox/CloakBrowser for this personal account unless Galih explicitly overrides.

## Skill/helper layout

Two copies were needed because Galyarder and Keiya/default read different skill roots:

```text
Galyarder profile:
/home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/

Keiya/default root:
/home/galyarder/.hermes/skills/productivity/google-workspace/
```

Each copy has its own helper path inside that skill root:

```text
scripts/galih-gws.sh
```

Important: when mirroring the skill across profiles, update absolute helper paths inside `SKILL.md`. Do not leave the default/Keiya skill pointing at the Galyarder-profile helper.

## Helper contract

The helper should force the native/default Galih GWS config and remove stale overrides:

```bash
export HOME="/home/galyarder"
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR="/home/galyarder/.config/gws"
unset GOOGLE_WORKSPACE_CLI_TOKEN
unset GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE
```

Do not force `GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file` for Galih's personal default setup; let native `gws` use its normal keyring-backed encrypted credentials.

## Fast verification ladder

Use the target-profile helper path and verify live API, not only file presence.

```bash
GWSU="bash /home/galyarder/.hermes/skills/productivity/google-workspace/scripts/galih-gws.sh"
$GWSU auth status
$GWSU gmail users getProfile --params '{"userId":"me"}'
$GWSU gmail users messages list --params '{"userId":"me","maxResults":1}'
$GWSU drive about get --params '{"fields":"user"}'
$GWSU calendar calendarList list --params '{"maxResults":1}'
```

Expected healthy signals:

- `token_valid: true`
- `storage: encrypted`
- `encryption_valid: true`
- `plain_credentials_exists: false`
- user/profile email: `mhmdgalihsaputra249@gmail.com`
- Gmail/Drive/Calendar smoke calls exit successfully

## Keiya/default skill verification

`hermes skills inspect <name>` may resolve registries and report not found even when the local skill is enabled. For profile-local/default local skill proof, prefer:

```bash
HOME=/home/galyarder hermes --profile default skills list --source local --enabled-only
HOME=/home/galyarder hermes --profile default -z 'cek skill google-workspace ada? jawab satu baris saja'
```

The first proves local skill registration; the second proves the target profile can actually see/use the skill in conversation context.

## Reauth route

Only after an actual auth failure (`token_valid: false`, `invalid_grant`, `NOT_AUTHENTICATED`, revoked refresh token, or missing scope requiring consent):

1. Load `browser-routing`.
2. Verify Brave CDP at `http://127.0.0.1:9222/json/version`.
3. Run the appropriate `gws auth login` command.
4. Complete Google consent in Brave / Brave CDP.
5. Rerun `auth status` and at least Gmail profile + Drive or Calendar smoke.

Do not treat API disabled, IAM/quota, dummy Docs/Sheets 404, or wrong file ID as token failure.

## Overlap note

`google-workspace`, `google-workspace`, and `google-workspace` overlap as account-specific quick-access skills. They may later be consolidated into one class-level GWS quick-access umbrella with per-account helpers/references, but the current user-approved operational shape keeps account-specific entrypoints for speed and identity separation.
