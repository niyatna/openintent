# Threads agent-owned login and cookie capture

Session lesson from adding Keiya's dedicated Threads account.

## Scope

Use this for dedicated agent-owned Threads/Instagram identity login. It is not for Galih's personal accounts, mass signup, CAPTCHA bypass, or platform abuse.

## Credential layout

Store Threads credentials local-only under the same agent-owned account tree:

```text
/home/galyarder/.hermes/private/credentials/agents/<owner>/threads/
  account.txt
  backup-codes.txt
  cookies.json
```

`account.txt` can follow the standard dotenv contract with Threads-specific fields:

```dotenv
ACCOUNT_ID=<owner>-threads
OWNER=<owner>
SERVICE=threads
PROFILE_URL=https://www.threads.com/@<username>
EMAIL=
USERNAME=<username>
PASSWORD=...
TOTP_SECRET=
BACKUP_CODES_FILE=/home/galyarder/.hermes/private/credentials/agents/<owner>/threads/backup-codes.txt
COOKIES_FILE=/home/galyarder/.hermes/private/credentials/agents/<owner>/threads/cookies.json
NOTES=dedicated agent-owned Threads account; public actions require confirmation
```

Directory mode should be `700`; files should be `600`. Never print password, cookies, tokens, or backup codes in chat/log summaries.

## Access registry entry

Add a non-secret access-registry block for the account, e.g. `agent_owned_threads_keiya`, with these semantics:

- owner status: credential stored / pending or active login session
- capabilities: profile/session read; drafts only until confirmation
- autonomous: validate account shape; open login/session bootstrap when explicitly requested
- confirmation-gated: post, reply, DM, follow, repost, profile/privacy change, paid spend, deleting content or sessions
- verification: account_check, cookie file mode/non-empty, read-only profile/session check

## Login workflow

1. Load `agent-accounts` plus the browser-routing/Camofox skill.
2. Ensure the account file exists and passes `account_check.py --require PASSWORD --require USERNAME`.
3. Patch/verify `scripts/camofox_session.py` supports provider `threads` with login URL `https://www.threads.com/login`.
4. Use Camofox or Hermes browser tools to open `https://www.threads.com/login`.
5. Fill username/password and submit.
6. Verify login by navigating to `https://www.threads.com/@<username>` and checking for logged-in UI, e.g. `New thread`, `Edit profile`, `Insights`, or compose controls.
7. Capture cookies/session metadata into the private `cookies.json` path and `chmod 600`.
8. Do not perform any public action unless Galih explicitly confirms that specific action.

## Cookie capture caveat

Hermes `browser_console` can capture document-accessible state:

```js
(() => ({
  url: location.href,
  title: document.title,
  cookie: document.cookie,
  localStorage: Object.fromEntries(Object.entries(localStorage)),
  sessionStorage: Object.fromEntries(Object.entries(sessionStorage))
}))()
```

This is useful evidence and can preserve non-HttpOnly state, but it is not guaranteed to contain all login cookies. Browser context may hold HttpOnly session cookies that are invisible to `document.cookie`. For stronger persistence after restart, add/use a Playwright context cookie/storage-state exporter rather than claiming the document-cookie snapshot is complete.

## Verification output pattern

In final user-facing report, avoid exposing secret values. Report only:

- skill name used/updated
- credential directory path
- cookies/session file path
- file mode (`600`)
- read-only login verification (profile title/username or UI markers)
- explicit caveat if only document-accessible cookies were captured
