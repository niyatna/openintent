# CloakBrowser Google headless login probe — 2026-05-18

## Scope

Session-specific reference for agent-owned Google login via CloakBrowser. Keep this under `agent-owned-account-login`; do not create a narrow one-off skill.

Use when Galih explicitly asks to test or use CloakBrowser for high-friction owned-agent login, or when Camofox/Playwright gets challenged and the task is still authorized account access.

## Verified outcome

- Account class: dedicated Galyarder-owned Google account.
- Browser: `cloakbrowser 0.3.28`, Chromium `146.0.7680.177.3`.
- Route: `launch_persistent_context_async(..., headless=True)`.
- Profile dir: `/home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser`.
- Profile dir mode: `700`.
- First real headless login: about `57.54s`.
- Rerun with persistent profile/session: about `18.41s`.
- Final proof URL: `https://myaccount.google.com/`.
- Owner-state proof: page title `Akun Google`; visible account-management sidebar (`Beranda`, `Info pribadi`, `Keamanan & login`, `Data & privasi`, etc.); profile/avatar; signed-in controls; sign-out control present; no login prompt.
- Process cleanup: after `context.close()`, remaining Cloak/Chromium process count was `0`.

## Fast execution pattern

1. Validate `account.txt` with `account_check.py` and required `EMAIL`, `PASSWORD`, `TOTP_SECRET`; never print secrets.
2. Launch persistent CloakBrowser context:

```python
ctx = await cloakbrowser.launch_persistent_context_async(
    str(profile_dir),
    headless=True,
    locale="id-ID",
    timezone="Asia/Jakarta",
    viewport={"width": 1365, "height": 900},
    humanize=True,
    human_preset="careful",
    args=["--disable-blink-features=AutomationControlled"],
)
```

3. Use direct login URL with MyAccount continue target:

```text
https://accounts.google.com/ServiceLogin?service=accountsettings&continue=https%3A%2F%2Fmyaccount.google.com%2F
```

4. Fill email, submit; fill password, submit.
5. If Google asks for Authenticator/TOTP, generate locally from `TOTP_SECRET` and submit. In the verified run, TOTP was not required.
6. If a non-security optional prompt appears (`Lewati`, `Skip`, `Not now`, `Nanti saja`), click it once only after password auth succeeds.
7. Navigate to `https://myaccount.google.com/` and verify strict owner-state:
   - host is `myaccount.google.com`, not only public `google.com/account/about`;
   - title is Google Account / `Akun Google`;
   - at least two private account sections are visible (`Info pribadi`, `Keamanan & login`, `Data & privasi`, `Wallet & langganan`, etc.);
   - sign-out/account avatar control visible;
   - no active login form visible.
8. Save screenshot to `/tmp` if needed for evidence, then `await ctx.close()` and verify no leftover Cloak/Chromium process.

## Pitfalls

- Do not treat `https://www.google.com/account/about` as owner-state. That public marketing page can show `Login dengan Google` and is not proof.
- Screenshot proof is useful but not sufficient alone; pair it with URL/title/DOM tokens and process cleanup.
- `TOTP_SECRET` may exist but may not be invoked every login. Do not force TOTP unless Google shows a 2FA/code gate.
- Keep CloakBrowser as high-friction/fallback route until each platform operator has a verified CRUD flow for it.
- Never print password, TOTP secret, backup codes, cookies, localStorage, or token JSON.
