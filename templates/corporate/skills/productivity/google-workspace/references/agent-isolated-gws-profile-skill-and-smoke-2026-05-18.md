# Agent-isolated GWS profile skill + smoke verification — 2026-05-18

Use this when setting up or auditing a dedicated agent Google Workspace config (for example Galyarder or Keiya) rather than the default/global Hermes Google account.

## Lesson

OAuth success is not enough. A setup can have `token_valid=true` and still be incomplete if:

- the API smoke calls fail because the OAuth project lacks IAM/API enablement;
- the quick-access skill/helper was written under the global skill tree instead of the active profile tree;
- the helper does not force the isolated config/keyring env;
- the People command syntax is wrong, causing a false failure unrelated to auth.

## Active-profile placement rule

For a profile-specific quick-access skill, verify that `skill_view("<agent>-gws-quick-access")` loads it from the active profile path, not only that files exist somewhere on disk.

Expected shape for Galyarder:

```text
/home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/SKILL.md
/home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galyarder-gws.sh
/home/galyarder/.config/gws-galyarder
```

A stale/global-only path such as `/home/galyarder/.hermes/skills/productivity/<skill>` may exist, but that alone does not prove the running profile can load the skill.

## Isolated helper contract

The helper should set:

```bash
export HOME=/home/galyarder
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/home/galyarder/.config/gws-<agent>
export GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file
unset GOOGLE_WORKSPACE_CLI_TOKEN
unset GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE
```

Then `exec` the real `gws` binary.

## Minimal smoke suite before claiming ready

Run through the helper, not raw `gws`:

```bash
GWSG="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/galyarder-gws.sh"
$GWSG auth status
$GWSG gmail users getProfile --params '{"userId":"me"}'
$GWSG gmail users messages list --params '{"userId":"me","maxResults":1}'
$GWSG drive about get --params '{"fields":"user,storageQuota"}'
$GWSG calendar calendarList list --params '{"maxResults":1}'
$GWSG people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
```

Good result:

- config dir mode `700`;
- credential/token/client files mode `600`;
- `auth status` reports the intended account and `token_valid=true`;
- no `client_config_error`;
- Gmail, Drive, Calendar, and People profile smoke calls exit `0`;
- quick-access skill is loadable in the active profile.

## People command syntax

Fast People API proof:

```bash
gws people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
```

Contact-list proof, when needed:

```bash
gws people people connections list --params '{"resourceName":"people/me","pageSize":1,"personFields":"names,emailAddresses"}'
```

Wrong shape that produces a validation error:

```bash
gws people people.connections list ...
```

## Report rule

Use one of these shapes:

```text
ready: auth + Gmail/Drive/Calendar/People smoke passed via isolated helper.
```

```text
auth ready; API blocked by <IAM/API/scope gate>.
```

Do not report completion from OAuth/token state alone.
