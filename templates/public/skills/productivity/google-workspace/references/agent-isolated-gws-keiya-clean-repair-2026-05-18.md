# Agent-isolated GWS Keiya clean repair — 2026-05-18

Use this when Keiya GWS is functional but not clean: `token_valid=true` with `client_config_error`, plaintext token storage, or quick-access skill missing from the active profile path.

## Symptoms

- `/home/galyarder/.config/gws-keiya` exists with mode `700`.
- `auth status` shows `token_valid=true` but also:
  - `client_config_error` because `client_secret.json` is Web shape (`web`) instead of installed/Desktop shape (`installed`);
  - `storage: plaintext` from `credentials.json` or explicit `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`;
- Gmail/Drive/Calendar may still work if the helper points to the plaintext credential file.
- Active `skill_view('google-workspace')` may fail if the skill lives only under global `.hermes/skills`, not the profile path.

## Repair shape

1. Backup current files under `/home/galyarder/.config/gws-keiya` before editing.
2. Convert the OAuth client JSON from Web shape to installed/Desktop shape:
   - top-level key must be `installed`;
   - preserve `client_id`, `client_secret`, `project_id`, auth/token/cert URIs, and redirect URIs;
   - write both `client_secret.json` and `google_client_secret.json` with mode `600`.
3. Migrate the plaintext authorized-user JSON into `credentials.enc` using the GWS AES-256-GCM format:
   - key source: `/home/galyarder/.config/gws-keiya/.encryption_key`, base64-decoded 32-byte key;
   - encrypted file format: `12-byte nonce || AESGCM(ciphertext+tag)`;
   - write `credentials.enc` mode `600`;
   - validate `gws auth status` reports `encrypted_credentials_exists=true`, `encryption_valid=true`, `token_valid=true`;
   - only after validation, move `credentials.json` aside as a timestamped `.bak` so `plain_credentials_exists=false`.
4. Put the skill/helper in the active Galyarder profile path:
   - `/home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/SKILL.md`
   - `/home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/keiya-gws.sh`
5. Helper env must set:
   - `HOME=/home/galyarder`
   - `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=/home/galyarder/.config/gws-keiya`
   - `GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file`
   - `GOOGLE_WORKSPACE_PROJECT_ID=" "`
   - unset `GOOGLE_WORKSPACE_CLI_TOKEN` and `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`

The blank quota project is intentional for Keiya. The installed client still contains `project_id=galyarder-agent` because GWS requires it, but Keiya's consumer Gmail account is not an IAM member on that project. Without blanking `GOOGLE_WORKSPACE_PROJECT_ID`, read calls can fail with `serviceusage.services.use` / Service Usage Consumer 403.

## Verification

```bash
KWS="bash /home/galyarder/.hermes/profiles/galyarder/skills/productivity/google-workspace/scripts/keiya-gws.sh"
$KWS auth status
$KWS gmail users getProfile --params '{"userId":"me"}'
$KWS gmail users messages list --params '{"userId":"me","maxResults":1}'
$KWS drive about get --params '{"fields":"user,storageQuota"}'
$KWS calendar calendarList list --params '{"maxResults":1}'
$KWS people people connections list --params '{"resourceName":"people/me","pageSize":1,"personFields":"names,emailAddresses"}'
```

Expected:

- config dir mode `700`; credential/client/token files mode `600`;
- client files top-level `installed`;
- `auth status`: `token_valid=true`, `storage=encrypted`, `encryption_valid=true`, `plain_credentials_exists=false`, no `client_config_error`;
- Gmail profile/list, Drive about, Calendar list, and People connections all exit `0`;
- Gmail/Drive/Calendar identity is `keiyazeyniputri@gmail.com` / `Keiya Zeyni Putri`.

## Pitfalls

- Do not remove `project_id` from `client_secret.json`; GWS treats it as a required installed config field and reports `client_config_error`.
- Do not leave `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` set after migration; it forces plaintext precedence.
- `people people get --resourceName people/me` needs profile/userinfo scope; Keiya's current token uses `contacts.readonly`, so use `people people connections list` as the People smoke.
- Do not print token/client secret JSON values. Summaries must report only paths, modes, scopes count, account, and pass/block state.
