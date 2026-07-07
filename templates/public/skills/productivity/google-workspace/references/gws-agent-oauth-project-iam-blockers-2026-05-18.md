# GWS agent OAuth project / IAM blockers — 2026-05-18

Use this when an agent-owned Google Workspace setup has valid OAuth but real API calls still fail.

## Sanitized symptoms

- Isolated config exists and `gws auth status` returns `token_valid=true` for the intended account.
- `client_config_error` is absent.
- A real Workspace API call fails with HTTP 403 similar to:

```text
Caller does not have required permission to use project <project-id>.
Grant the caller the roles/serviceusage.serviceUsageConsumer role,
or a custom role with the serviceusage.services.use permission.
```

This is not a normal refresh-token failure. It is an OAuth/GCP quota-project execution blocker.

A second possible blocker appears when switching OAuth clients/projects:

```text
Access blocked: <app> has not completed the Google verification process.
The app is currently being tested, and can only be accessed by developer-approved testers.
Error 403: access_denied
```

That means the account is not allowed by the OAuth app's consent-screen/test-user settings, even if the username/password is correct.

## Fast fix route

1. Keep the agent config isolated:

```bash
export HOME=/home/galyarder
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/home/galyarder/.config/gws-<agent>
export GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file
unset GOOGLE_WORKSPACE_CLI_TOKEN GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE
```

2. If `gws auth status` is valid but API calls fail with `serviceusage.services.use`, fix the GCP project behind the OAuth client:
   - grant `roles/serviceusage.serviceUsageConsumer` to the authenticated Google user on that project; or
   - switch to an OAuth client/project where that user already has Service Usage Consumer and the consent screen allows the account.

3. If OAuth consent says the app is still in testing, do one of:
   - add the account as a test user for that OAuth app;
   - publish/verify the OAuth app if appropriate;
   - switch to an allowed OAuth project.

4. Rerun OAuth after changing project/client/role.

5. Smoke-test with at least one cheap real API call. `auth status` alone is not enough:

```bash
gws auth status
gws gmail users getProfile --params '{"userId":"me"}'
gws drive about get --params '{"fields":"user,storageQuota"}'
gws calendar calendarList list --params '{"maxResults":1}'
```

6. If the smoke suite includes People/Contacts, ensure the OAuth flow requested the required People/Contacts scope before blaming the API.

## Reporting rule

Report the exact gate, not a fake completion:

- `auth ready; API blocked by Service Usage Consumer on <project-id>`
- `OAuth blocked; account not approved as test user for <app>`
- `done; Gmail/Drive/Calendar smoke passed`

Never paste passwords, OAuth client secrets, refresh tokens, access tokens, cookies, or full `account.txt` contents.
