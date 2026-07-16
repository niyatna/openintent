# Reference: platform-operator-router

# Threads Operator

## Speed-first execution flow

Default target: get to a verified live artifact with the fewest safe steps. Do not spend time rediscovering frontend structure when the known direct path works.

Fast path:

```text
1. identify agent: co-founder | default
2. run cookie smoke for that agent only
3. if cookies-active -> open https://www.threads.com/
4. verify owner-state controls, not public profile only
5. execute requested CRUD through frontend
6. verify exact live result on permalink/profile feed
7. report one line: live/blocker/deleted
```

Do **not** start with login. Do **not** open the public account profile first. Do **not** run both accounts “just in case”.

Cookie smoke:

```bash
python ~/.hermes/profiles/default/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent co-founder
python ~/.hermes/profiles/default/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent default
```

Use only the target account. Output interpretation:

- `status="cookies-active"` and `needs_login=false` -> skip login; execute frontend CRUD directly.
- `status="login-required"` -> use Threads/Instagram SSO fallback, save/update cookies, rerun smoke.
- `status="probe-error"` -> fix the selected browser/script before claiming auth state.

Verified behavior from current references: Co-Founder and Default Threads cookies can open owner-state without login through this script.

## Absolute rule

For Owner's dedicated agent-owned Threads accounts, the workflow is **Camofox persistent profile first**. CloakBrowser remains a legacy/fallback route while this platform's proven frontend scripts are still CloakBrowser-based or Camofox is blocked.
No official API-first route. No Hermes native browser route. No random Brave route.

Mandatory chain:

```text
platform-operator-router -> Camofox persistent profile first -> CloakBrowser fallback only when needed -> verify owner-state -> requested CRUD -> verify live
```

Public/destructive actions require exact Owner approval unless he gave the exact action in the current turn.
Never print password, TOTP secret, backup codes, cookies, tokens, localStorage/sessionStorage, or full account files.

## Account/session paths

```text
~/.hermes/private/credentials/agents/<agent>/threads/account.txt
~/.hermes/private/credentials/agents/<agent>/threads/cookies.json
~/.hermes/private/credentials/agents/<agent>/threads/backup-codes.txt
~/.hermes/private/browser-profiles/agents/<agent>/threads-camofox/
~/.hermes/private/browser-profiles/agents/<agent>/threads-cloakbrowser/  # legacy fallback
```

Known handles:

- Co-Founder: `co-founder`
- Default: `yourcompany`

Entrypoints:

- Session/login entry: `https://www.threads.com/login`
- Logged-in home/composer: `https://www.threads.com/`
- Profile verify only after auth: `https://www.threads.com/@<username>`

## Owner-state proof

Owner-state controls beat cookie-file existence. Proof includes any of:

- `New thread`
- `Edit profile`
- `Insights`
- `Saved`
- `Profile`
- composer text such as `What's new?`

Login-gate text means reuse failed:

- `Log in with your Instagram account`
- `Username, phone or email`
- `Password`
- `Continue with Instagram`

## Frontend platform access

Use the direct frontend. Do not rediscover the site every posting run.

Observed owner-state on Co-Founder via CloakBrowser cookie probe:

- URL after cookie reuse: `https://www.threads.com/`
- visible controls: `Threads`, `For you`, `New thread`, `Search`, `Activity`, `Notifications`, `Profile`, `Insights`, `Saved`, `Edit`, `Following`
- strong owner proof: `New thread`, `What's new?`, `Post`, `Insights`, `Saved`, `Profile`

Fast UI handles:

- Home/composer: `https://www.threads.com/`
- Login/session: `https://www.threads.com/login`
- Profile: `https://www.threads.com/@<username>`
- Exact post: permalink from the created/deleted target
- Create: `New thread` visible control or composer text `What's new?`
- Attach media: file input/file chooser inside composer; use local absolute file path
- Media proof before post: visible thumbnail/preview inside composer
- Publish: `Post`
- Original post menu: `More` on the target post; correct menu includes `Insights`, `Pin to profile`, `Reply options`, `Delete`
- Wrong menu signal: reply-menu options like `Pin reply`, `Hide for everyone`; back out and click original post menu instead
- Owner profile management: `Edit profile`, `Insights`, `Saved`
- Public verification: exact permalink + authenticated/public profile feed check

Frontend selectors change. Prefer semantic text/role controls first; if that fails, inspect the live DOM visually. Do not encode brittle CSS selectors as proof.

## Frontend CRUD

### Create

1. Run smoke script; `cookies-active` means do not login.
2. Open `https://www.threads.com/`.
3. Click `New thread` or the composer (`What's new?`).
4. Paste exact caption/text into composer.
5. For media: attach via CloakBrowser frontend file input/file chooser.
6. Hard gate: wait until media preview/thumbnail is visible before `Post`.
7. Click `Post` once.
8. Verify public permalink/profile feed has exact caption and media.

No preview = no post. No exact caption = no done.

### Read

- Session read: smoke script or owner-state controls (`New thread`, `Insights`, `Saved`, `Profile`).
- Feed/profile read: open `https://www.threads.com/@<username>` after auth.
- Post read: open exact permalink.
- Evidence: handle, caption, media visibility/count, timestamp/header, URL.

### Update

Threads web edit may be missing/unreliable. Fastest correct route:

- If edit is clearly available and final state can be verified, use it.
- Otherwise for caption/media mistakes: delete wrong post + repost exact final artifact.
- Treat media update as delete + repost.
- Profile/bio/avatar/privacy changes require explicit approval; verify public/profile view after save.

### Delete

1. Open exact post permalink while authenticated.
2. Click the **original post** `More` menu, not reply menu.
3. Correct menu contains options like `Insights`, `Pin to profile`, `Reply options`, `Delete`.
4. Click `Delete`, confirm.
5. Verify profile feed absence. Deleted permalink can redirect/fallback, so feed check wins.

### Interactions

Reply, repost/rethread, like, follow/unfollow, DM, and profile changes are public actions. Execute only after exact Owner approval/scope. Verify final visible state.

## Login fallback only when reuse fails

1. Open `https://www.threads.com/login`.
2. Click `Continue with Instagram` if shown.
3. If Instagram interstitial shows `Open Instagram`, click small web `Log in` link, not app-open.
4. Fill username/email + password from `account.txt`; never print values.
5. If fields stay empty, use focus-order fallback: username -> Tab -> password -> Enter.
6. If TOTP appears, generate locally from private account file.
7. Stop on checkpoint/CAPTCHA/phone/email gate.
8. Save/update `cookies.json`, rerun smoke script, then continue CRUD.

## Reusable scripts

- `scripts/threads_cookie_reuse_smoke.py` — imports old `cookies.json` into a fresh CloakBrowser session, opens `https://www.threads.com/login`, checks owner-state vs login gate, and prints sanitized JSON.

## References

- `references/speed-first-frontend-crud-2026-05-18.md` — fastest end-to-end Threads frontend CRUD route, including create/read/update/delete/interactions and accepted concise report shape.
- `references/threads-cookie-reuse-smoke-2026-05-18.md` — cookie reuse proof and command.
- `references/threads-cloakbrowser-media-posting-2026-05-17.md` — media posting, caption correction, deletion menu trap.

## User-facing report

Keep it short:

- Success: `live: <permalink>`
- Reuse success: `cookies-active; no login needed.`
- Blocked: `blocker: <one gate>. stopped before wrong public action.`