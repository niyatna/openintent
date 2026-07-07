# Gmail app password via CloakBrowser for IMAP/SMTP (2026-05-18)

## Use case

When Galih asks to create/rotate an app password for an authorized agent-owned Google account and wire it into IMAP/SMTP tooling such as Himalaya or the Hermes email gateway.

This is credential/security work. Do not print the app password, account password, TOTP secret, cookies, token JSON, or raw DOM containing the generated app password.

## Verified route

Account: Galyarder-owned Google (`galyarderlabs@gmail.com`) using the existing CloakBrowser persistent profile.

1. Use the authorized account file under the private credentials root and validate field presence without printing secrets.
2. Launch CloakBrowser with the existing persistent profile:
   - profile example: `/home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser`
   - `headless=True`, locale `id-ID`, timezone `Asia/Jakarta`, `humanize=True`, `human_preset="careful"`.
3. Open `https://myaccount.google.com/apppasswords`.
4. If Google asks to verify, fill password from the private account file. Use TOTP only if Google asks for an Authenticator/code gate.
5. On the Indonesian app-password page, fill the app-name field (`Nama aplikasi`) and click `Buat`.
6. Extract only the new generated app-password candidate, store it privately, and validate it with live IMAP + SMTP before accepting it.

## Critical pitfall: DOM noise can look like an app password

Do not trust the first 16-letter candidate extracted from the page. During the session, a candidate was captured from DOM/page noise and looked structurally valid but failed both Gmail IMAP and SMTP auth.

Required guard:

- Take a baseline set of grouped 4x4-letter candidates before clicking `Buat`.
- After creation, extract only candidates that are new relative to the baseline.
- Prefer the visible grouped pattern `xxxx xxxx xxxx xxxx`; avoid accepting continuous 16-letter strings from arbitrary page text.
- Validate the chosen candidate before saving:
  - IMAP: `imap.gmail.com:993`, login OK, `INBOX` select OK.
  - SMTP: `smtp.gmail.com:587`, STARTTLS login OK.
- If validation fails, discard the candidate, do not write config, and create a fresh app password.

## Storage/config pattern used

- Private app password file: `/home/galyarder/.hermes/private/credentials/agents/galyarder/google/app-password-himalaya-imap-smtp.txt`
- Secret file mode: `600`
- Himalaya helper: `/home/galyarder/.config/himalaya/galyarder-password.py`
- Himalaya config: `/home/galyarder/.config/himalaya/config.toml`
- Hermes email envs patched when replacing the active profile email route:
  - `/home/galyarder/.hermes/.env`
  - `/home/galyarder/.hermes/profiles/galyarder/.env`

Keep backups before replacing configs. Keep helper files non-world-readable/executable as needed. Never put the app password in memory, chat, skill body, profile repo, or Obsidian.

## Minimal success proof

Report only non-secret proof:

- app password file exists with mode `600` and length `16`
- Himalaya `account list` shows the expected account name
- Himalaya `folder list` reads Gmail folders
- direct IMAP login/select succeeds
- direct SMTP login succeeds
- Cloak/Chromium leftover process count is `0`

Do not report the app password or any raw page text that may contain it.
