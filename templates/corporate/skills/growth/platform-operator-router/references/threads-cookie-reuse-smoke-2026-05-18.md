# Threads cookie reuse smoke — 2026-05-18

## Lesson

For the fastest Threads workflow, testing `browser_navigate("https://www.threads.com/login")` alone is not the skill flow. A plain/native browser context without the saved account cookies can still show the login page.

The correct reusable-access probe is:

1. load the matching private `cookies.json`;
2. import it into a fresh Camofox REST session with `POST /sessions/:userId/cookies`;
3. open `https://www.threads.com/login` through `POST /tabs`;
4. evaluate the page for owner-state controls;
5. close the Camofox session.

Owner-state controls observed as proof:

- `New thread`
- `Insights`
- `Saved`
- `Profile`
- sometimes `Edit profile`

Login-gate text that means reuse failed:

- `Log in with your Instagram account`
- `Username, phone or email`
- `Password`
- `Continue with Instagram`

## Session result

Using the cookie-import Camofox flow, both current cookie files opened Threads without login:

- Keiya Threads: 17 cookies imported; redirected/opened to `https://www.threads.com/`; owner-state included `New thread`, `Insights`, `Saved`, `Profile`; `needs_login=false`.
- Galyarder Threads: 9 cookies imported; redirected/opened to `https://www.threads.com/`; owner-state included `New thread`, `Insights`, `Saved`, `Profile`; `needs_login=false`.

Do not report from cookie file existence alone. The reusable proof is the cookie-import smoke test plus owner-state controls.

## Reusable script

Use `scripts/threads_cookie_reuse_smoke.py` from this skill:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent keiya
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent galyarder
```

The script prints sanitized JSON only: cookie count, owner hits, login hits, `needs_login`, and status. It never prints cookie values or account secrets.
