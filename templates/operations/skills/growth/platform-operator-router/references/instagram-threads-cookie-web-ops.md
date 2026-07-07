# Reference: platform-operator-router

# Instagram / Threads Cookie Web Ops

## Role boundary

This skill is a **shared Meta account/session helper**, not the main social operator.

Use it only after the platform route is chosen:

| Need | Primary skill | This skill's role |
|---|---|---|
| Threads post/read/update/delete/interact | `platform-operator-router` | Meta SSO/cookie/session/TOTP support |
| Instagram post/read/update/delete/interact | `platform-operator-router` | Meta login/account-picker/cookie/TOTP support |
| Generic credential/TOTP/session contract | `agent-accounts` | Meta-specific quirks and paths |
| Browser runtime/service issue | `camofox-browser` / `browser-routing` | Meta-specific verification cues |

If the task says Threads, load `platform-operator-router` first. If it says Instagram, load `platform-operator-router` first.
Do not duplicate platform CRUD here.

## Known owned Meta surfaces

- Galyarder Instagram: `https://www.instagram.com/galyarderlabs.ai/`
- Galyarder Threads: `https://www.threads.com/@galyarderlabs.ai`
- Galyarder username: `galyarderlabs.ai`
- Keiya Instagram: `https://www.instagram.com/keiyazeyniputri/`
- Keiya Threads: `https://www.threads.com/@keiyazeyniputri`
- Keiya username: `keiyazeyniputri`

Credential pair is shared per Meta identity; session cookies are **surface-specific** and must not be copied between Instagram and Threads.

## Private paths

Never print secret values. Read them only inside local scripts/processes and report sanitized state.

```text
/home/galyarder/.hermes/private/credentials/agents/<agent>/instagram/account.txt
/home/galyarder/.hermes/private/credentials/agents/<agent>/instagram/cookies.json
/home/galyarder/.hermes/private/credentials/agents/<agent>/instagram/backup-codes.txt

/home/galyarder/.hermes/private/credentials/agents/<agent>/threads/account.txt
/home/galyarder/.hermes/private/credentials/agents/<agent>/threads/cookies.json
/home/galyarder/.hermes/private/credentials/agents/<agent>/threads/backup-codes.txt

/home/galyarder/.hermes/private/browser-profiles/agents/<agent>/instagram-camofox/
/home/galyarder/.hermes/private/browser-profiles/agents/<agent>/threads-camofox/
```

Expected modes:

- private dirs: `0o700`
- `account.txt`, `cookies.json`, `backup-codes.txt`: `0o600`

## Session proof rules

Cookie file existence is not proof. A reusable session is proven only by owner-state on a fresh browser context after importing cookies or opening the persistent profile.

Threads owner-state examples:

- `New thread`
- `Edit profile`
- `Insights`
- `Saved`
- `Profile`
- composer text like `What's new?`

Instagram owner-state examples:

- `Create`
- `Messages`
- `Edit profile`
- `View archive`
- account picker / logged-in navigation controls

Login-gate examples:

- `Continue with Instagram`
- `Log in with your Instagram account`
- username/email/password fields
- checkpoint/CAPTCHA/phone/email verification

## Meta SSO/login fallback

Only use this after platform session reuse fails.

1. Open the platform entrypoint in Camofox:
   - Threads: `https://www.threads.com/login`
   - Instagram: `https://www.instagram.com/accounts/login/`
2. For Threads, click `Continue with Instagram` when shown.
3. If Instagram interstitial says `Open Instagram`, click the small web `Log in` link instead of app-open.
4. Prefer selector fill; if fields stay empty, use focus-order fallback: username/email → Tab → password → Enter.
5. If account picker shows the correct account (`galyarderlabs.ai` / `keiyazeyniputri`), click `Continue` before falling back to password.
6. If TOTP appears, generate locally from private account file. Never print the secret or code in chat.
7. Backup code only after explicit approval; mark used locally.
8. Stop on checkpoint/CAPTCHA/phone/email gates.
9. Save/update the surface-specific `cookies.json`, then rerun the platform operator's session proof.

## Threads smoke compatibility

Canonical Threads smoke script lives in `platform-operator-router`:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent keiya
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent galyarder
```

This helper may keep a compatibility wrapper, but the operator-owned script is the source of truth.

## Meta 2FA / TOTP setup

Use when Galih asks to harden Instagram/Threads with authenticator app, `pyotp`, and backup codes.

1. Verify login/session first; do not start from credential existence.
2. Direct URL when possible: `https://accountscenter.instagram.com/password_and_security/two_factor/`
3. Select the correct Meta account explicitly; do not click by position.
4. If Meta sends a verification code to a masked email/phone, report the exact mask and pause.
5. Save `TOTP_SECRET` only after Meta shows the authenticator setup secret/QR.
6. Mark TOTP registered only after Meta accepts a fresh generated code.
7. Capture backup/recovery codes immediately; zero-byte backup-code files mean not captured.
8. Final report: booleans/counts/modes only, never secret values.

## Public action boundary

Public actions belong to `platform-operator-router` or `platform-operator-router`, not this helper:

- post, reply, repost/rethread, like, follow/unfollow
- DM/reply to a human
- profile/bio/avatar/privacy changes
- deleting content or sessions
- paid subscription, ad spend, boost, Meta business settings

Those require exact approval unless Galih gives the exact action in the current turn.

## Verification language

- `credential-stored-pending-login-session`: username/password exists locally, but no verified session.
- `login-active`: authenticated page verified in a live browser context.
- `cookies-active`: fresh context with saved cookies verified authenticated access.
- `checkpoint-blocked`: Meta verification/checkpoint stopped login.
- `posted`: public profile/permalink verified by the platform operator.

## References

- `references/meta-2fa-totp-session-gates.md`
- `references/keiya-instagram-cookie-capture-2026-05-17.md`
- `platform-operator-router/references/speed-first-frontend-crud-2026-05-18.md` — current fastest Threads CRUD flow; this helper only supports Meta auth/session pieces.
- `references/threads-camofox-media-posting-2026-05-17.md` — historical Threads media-posting lesson; current CRUD entrypoint is `platform-operator-router`.
- `references/threads-cookie-reuse-smoke-2026-05-18.md` — historical cookie-reuse proof; current canonical script lives in `platform-operator-router`.

## Common mistakes

- Starting Meta social tasks from this helper instead of `platform-operator-router` / `platform-operator-router`.
- Treating Instagram credentials as Threads cookies.
- Treating a public profile view as authenticated proof.
- Treating login footer/header text as failure after owner-state controls are visible.
- Printing password/cookies/TOTP while debugging.
- Deleting or posting from the wrong menu/context.