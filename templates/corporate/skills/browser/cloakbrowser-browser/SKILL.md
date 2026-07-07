---
name: cloakbrowser-browser
description: Use when installing, verifying, launching, or operating CloakBrowser on Galih's workstation, especially dedicated Keiya/Galyarder persistent browser profiles, Google login/session capture, cookies, HAR/CDP work, or browser-profile-manager-style workflows.
version: 1.0.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    category: browser
    tags: [cloakbrowser, browser, google, login, cookies, profile-manager, cdp, automation]
    related_skills: [browser-routing, agent-accounts, google-workspace, har-capture]
---
# CloakBrowser Browser

## Core rule

Galih's workstation has one shared OS home: `/home/galyarder/`. CloakBrowser binaries, Python venv, wrappers, and cache live only under OS home. Never recreate `/home/galyarder/.hermes/profiles/galyarder/home` and never install a second CloakBrowser under a profile home.

CloakBrowser is now the primary browser route for dedicated Keiya/Galyarder owned-agent browser sessions. Use each agent's own persistent profile directory and cookie file. Camofox is legacy/fallback unless a platform skill has a still-verified Camofox-only frontend flow and CloakBrowser is blocked.

## Installed layers

```text
Python venv:      /home/galyarder/.local/share/cloakbrowser-venv
CLI wrapper:      /home/galyarder/.local/bin/cloakbrowser-galyarder
Python wrapper:   /home/galyarder/.local/bin/cloakbrowser-python
Binary cache:     /home/galyarder/.cache/cloakbrowser/chromium-<version>/chrome
```

Verify all layers separately:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/cloakbrowser-galyarder info
find /home/galyarder/.cache/cloakbrowser -maxdepth 3 -type f -name chrome -perm -111 -print
```

`Installed: False` means the Chromium binary cache is missing even if the Python package/wrapper is installed.

Repair binary only in OS home (required after every `pip install --upgrade cloakbrowser` because the python package update does not automatically pull the chromium binary):

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/cloakbrowser-galyarder install
```

For long downloads, run as a tracked background process; do not silently block Discord for minutes.

## Browser Profile Manager interpretation

CloakBrowser README's Browser Profile Manager is the self-hosted `cloakhq/cloakbrowser-manager` app:

```bash
docker run -p 8080:8080 -v cloakprofiles:/data cloakhq/cloakbrowser-manager
```

For Hermes agent-owned accounts, use the same primitive directly through `launch_persistent_context(...)`: persistent profile directories with unique sessions, cookies, localStorage, and browser state. The manager UI is useful for many profiles/noVNC, but not required for two local Keiya/Galyarder profiles.

## Canonical local profiles

```text
Keiya Google profile:
/home/galyarder/.hermes/private/browser-profiles/agents/keiya/google-cloakbrowser

Galyarder Google profile:
/home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser

Keiya Google cookies:
/home/galyarder/.hermes/private/credentials/agents/keiya/google/cookies.json

Galyarder Google cookies:
/home/galyarder/.hermes/private/credentials/agents/galyarder/google/cookies.json
```

Profile dirs must be mode `700`; cookie/storage files mode `600`. Never print cookie values, passwords, TOTP secrets, backup codes, localStorage, or token JSON.

## Google login/session workflow

Primary helper:

```bash
/home/galyarder/.hermes/scripts/cloak_google_profile.py --owner keiya --timeout-ms 120000
/home/galyarder/.hermes/scripts/cloak_google_profile.py --owner galyarder --timeout-ms 90000
```

The helper:

1. reads `/home/galyarder/.hermes/private/credentials/agents/<owner>/google/account.txt` without printing secrets;
2. launches `launch_persistent_context(...)` with `locale="id-ID"`, `timezone="Asia/Jakarta"`, persistent profile dir, and careful human settings where useful;
3. logs into Google if needed;
4. handles the common Google phone-prompt path by clicking `Coba cara lain` / `Try another way`, selecting Authenticator/code, then submitting local TOTP;
5. verifies `https://myaccount.google.com/` owner-state;
6. saves cookies to the account's normal `COOKIES_FILE` and a `storage-state.cloakbrowser.json` next to it;
7. closes the browser context.

Strict owner-state proof:

- final host `myaccount.google.com`;
- title `Akun Google` / Google Account;
- expected account email or account label visible;
- private sections such as `Info pribadi`, `Keamanan & login`, `Data & privasi`, `Wallet & langganan` visible;
- no login form visible;
- cookie count > 0 and cookie file mode `600`.

Do not treat `https://www.google.com/account/about/` as login proof. It is public marketing/login copy.

## Launch pattern for new profile-backed tasks

```python
from cloakbrowser import launch_persistent_context

ctx = launch_persistent_context(
    "/home/galyarder/.hermes/private/browser-profiles/agents/<owner>/<service>-cloakbrowser",
    headless=True,
    locale="id-ID",
    timezone="Asia/Jakarta",
    viewport={"width": 1365, "height": 900},
    humanize=True,
    human_preset="careful",
    args=["--no-first-run", "--no-default-browser-check"],
)
page = ctx.new_page()
# operate...
ctx.close()
```

If a profile reports `SingletonLock` / `ProcessSingleton` errors, another Chromium is using that profile. Close the stale process first; only remove `Singleton*` files after verifying no matching process remains.

## Common mistakes

- Calling Python's default interpreter and concluding `cloakbrowser` is missing; use `/home/galyarder/.local/share/cloakbrowser-venv/bin/python` or wrapper.
- Treating `~/.cache/cloakbrowser` as disposable language cache. It contains the load-bearing Chromium binary when that cache path is active.
- Treating one `Installed: False` result as proof that the binary is absent. Before reinstall/redownload, check both active cache conventions: `CLOAKBROWSER_CACHE_DIR=/home/galyarder/.cache/cloakbrowser` and the package default `/home/galyarder/.cloakbrowser`; look for `chromium-*/chrome` in both. If `/home/galyarder/.cloakbrowser/chromium-*/chrome` exists, run CloakBrowser with `CLOAKBROWSER_CACHE_DIR=/home/galyarder/.cloakbrowser` or fix the wrapper instead of starting a new install.
- Reinstalling under profile home after seeing an empty cache.
- Ignoring Galih's explicit browser route. If he says to use CloakBrowser/headless, do not silently fall back to controlling his real Brave/desktop browser or `computer-use-linux`; use CloakBrowser headless or state the exact CloakBrowser gate.
- For high-friction checkout/login flows, first try the requested headless CloakBrowser route with valid persistent/session cookies before asking Galih to solve a human gate. Do not claim “CloakBrowser cannot” from a single fresh-profile captcha. If the gate persists, report `blocked: captcha` with evidence and no lecture.
- For Name.com specifically, see `references/namecom-headless-checkout-2026-06-11.md`: check the package-default CloakBrowser cache, use `browser_cookie3.brave(...)` only when Galih explicitly asks to operate Galih's existing Name.com/Brave session. If Galih says “pake akun lu sendiri”, use the agent-owned Google CloakBrowser profile (`/home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser`) and Google OAuth (`galyarderlabs@gmail.com`) instead of asking for Name.com credentials or importing Brave cookies. Avoid cart reset unless necessary, and verify total/domain/promo before final order.
- Counting public Google account pages as authenticated owner-state.
- Updating only Galyarder's skill/SOUL while Keiya/default still routes to Camofox-only.
- Leaving headed/debug browsers open after login; follow start → use → stop.

## Verification checklist

For full Camofox-first → CloakBrowser-primary migration across SOUL/router/platform skills, use `references/cloakbrowser-primary-route-migration-2026-05-28.md`.

- [ ] `HOME=/home/galyarder cloakbrowser-galyarder info` shows `Installed: True`.
- [ ] Profile home `/home/galyarder/.hermes/profiles/galyarder/home` does not exist.
- [ ] Keiya + Galyarder profile dirs exist with mode `700`.
- [ ] Keiya + Galyarder Google cookies exist with mode `600` and nonzero cookie counts.
- [ ] Owner-state proof is from `myaccount.google.com`, not `google.com/account/about`.
- [ ] No stale Cloak/Chromium process is left unless intentionally kept open.
