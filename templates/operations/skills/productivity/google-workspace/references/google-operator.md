# Reference: google-workspace

# Google Operator

## Default first move: check existing auth/session

For Google tasks, do **not** start with login. Check the already-authorized execution layer first.

Fast route:

1. If task is Gmail/Calendar/Drive/Docs/Sheets and `gws` can do it, run a cheap live `gws auth/status` or read check first.
2. If `gws` auth is healthy, execute via `google-workspace`/`gws`.
3. If OAuth/auth is expired or missing, use CloakBrowser persistent-profile login/OAuth bootstrap.
4. After CloakBrowser OAuth/login, rerun `gws` live check before claiming ready.

## Absolute rule

For dedicated agent-owned Google login/OAuth/bootstrap, the route is **CloakBrowser persistent profile first**. Camofox/Camoufox is legacy/fallback only when CloakBrowser is blocked. No random browser, no Galih personal account, no token-file confidence without live check.

After CloakBrowser login/OAuth creates healthy auth, `gws` is the fastest execution layer for Workspace CRUD.
Never print token JSON, OAuth client secret JSON, passwords, TOTP secrets, backup codes, cookies, or localStorage/sessionStorage.

## Known local paths

```text
gws CLI: /home/galyarder/.local/bin/gws
OAuth client config: /home/galyarder/.config/gws/client_secret.json
Hermes legacy token: /home/galyarder/.hermes/google_token.json
Agent credentials: /home/galyarder/.hermes/private/credentials/agents/<agent>/google/account.txt
CloakBrowser persistent profile: /home/galyarder/.hermes/private/browser-profiles/agents/<agent>/google-cloakbrowser/
Legacy Camofox profile/cookies: only use if CloakBrowser is blocked or a still-verified fallback flow requires it.
```

## Frontend platform access

Use direct Google frontend only for login/OAuth/account-session proof. Do not rediscover account pages every run.

Observed owner-state via CloakBrowser/Camofox cookie probe:

- URL: `https://myaccount.google.com/`
- title: `Akun Google`
- visible controls: `Setelan Akun Google`, `Bantuan`, `Aplikasi Google`, account avatar (`Akun Google: <name> (<email>)`), `Menu navigasi`, `Beranda`, `Info pribadi`, `Keamanan & login`, `Sandi Google`, `Aplikasi & layanan pihak ketiga`, `Data & privasi`, `Wallet & langganan`, `Penyimpanan Google One`
- search input: `Telusuri Akun Google`

Direct frontend URLs:

- Account proof: `https://myaccount.google.com/`
- Gmail proof: `https://mail.google.com/mail/u/0/#inbox`
- OAuth/login fallback: use the exact OAuth URL or `https://accounts.google.com/`

## CloakBrowser login/OAuth bootstrap

1. Validate account file without printing secrets.
2. Launch the account's CloakBrowser persistent profile, or run `/home/galyarder/.hermes/scripts/cloak_google_profile.py --owner <keiya|galyarder> --timeout-ms 120000` for Google account proof/session refresh.
3. Open exact Google OAuth URL, or `https://accounts.google.com/` if plain login/session setup is required.
4. Fill email/password from private account file.
5. If Authenticator code requested, generate locally.
6. Backup code only with explicit approval.
7. Complete OAuth consent/redirect.
8. Save/update session/cookies if used.
9. Rerun `gws auth status` or a cheap live read.

## Camofox legacy/fallback login/OAuth

Use only when CloakBrowser is blocked or a still-verified fallback flow requires Camofox.

1. Validate account file without printing secrets.
2. Open exact Google OAuth URL, or `https://accounts.google.com/` if plain login/session setup is required.
3. Fill email/password from private account file.
4. If Authenticator code requested, generate locally.
5. Backup code only with explicit approval.
6. Complete OAuth consent/redirect.
7. Save/update session/cookies if used.
8. Rerun `gws auth status` or a cheap live read.

## CloakBrowser high-friction login proof

Use this as the normal owned-agent Google browser proof when auth/session state must be refreshed or verified.

Fast verified pattern:

1. Validate `account.txt` without printing secrets.
2. Launch `cloakbrowser.launch_persistent_context_async(profile_dir, headless=True, locale="id-ID", timezone="Asia/Jakarta", humanize=True, human_preset="careful")`.
3. Open `https://accounts.google.com/ServiceLogin?service=accountsettings&continue=https%3A%2F%2Fmyaccount.google.com%2F`.
4. Fill email/password; submit TOTP only if Google shows an Authenticator/code gate.
5. If a non-security optional prompt appears after successful auth, click `Lewati` / `Skip` / `Not now` once.
6. Strict proof is `https://myaccount.google.com/` with title `Akun Google`, private account sections visible, account/avatar/sign-out controls visible, and no login form.
7. Close the context and verify no leftover Cloak/Chromium process before reporting.

Do not count `https://www.google.com/account/about` as owner-state; it is public marketing/login copy, not account proof.

## Gmail app passwords for IMAP/SMTP

When creating or rotating a Gmail app password for an authorized agent-owned Google account, use the App Passwords frontend at `https://myaccount.google.com/apppasswords` only through an isolated browser session and never print the generated password.

Critical rule: a 16-letter DOM candidate is not proof. The page can contain 16-letter false positives/noise. Baseline candidates before clicking `Buat`, accept only a newly generated visible grouped candidate, and validate it with live Gmail IMAP + SMTP login before saving or patching config.

For the verified CloakBrowser + Himalaya/Hermes email flow, see `references/gmail-app-password-cloakbrowser-imap-smtp-2026-05-18.md`.

## Workspace CRUD after auth

Always load `google-workspace` for exact commands.

| Task | Fast route |
|---|---|
| Gmail search/read | `gws gmail search/get` |
| Gmail send/reply | draft + approval, then `gws gmail send/reply` |
| Calendar list/create/delete | `gws calendar ...` |
| Drive search/list/download/upload | `gws drive ...` or Drive API |
| Docs read/create/update | `gws docs ...` or Docs API |
| Sheets read/update/append | `gws sheets ...` |

Writes, shares, external email, delete, billing/security changes require confirmation unless Galih gave the exact action.

## Verification language

- `auth-active`: live `gws` status/read works.
- `oauth-required`: CloakBrowser OAuth/login needed.
- `blocked`: Google verification/CAPTCHA/account gate.
- `done`: output ID/link verified.

## User-facing report

- Auth reuse: `gws auth healthy; no login needed.`
- Work success: `done: <id/link>`
- Blocked: `blocker: <one gate>. next: <one move>`