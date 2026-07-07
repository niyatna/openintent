# X cookie web operations for agent-owned accounts

Use this when operating Keiya/Galyarder agent-owned X accounts with saved web cookies instead of OAuth/API tokens.

## Scope

This is for account-owned actions explicitly authorized by Galih, such as public posts, profile checks, and follow-back actions. Never print cookie values, auth tokens, CSRF values, or raw credential contents.

## Session pattern

- Load cookies from the agent's private `COOKIES_FILE` in `/home/galyarder/.hermes/private/credentials/agents/<owner>/x/account.txt`.
- Use a fresh browser context and inject cookies.
- Prefer headless Brave/Chromium via Playwright for X web UI actions when API auth is unavailable.
- Use existing cookies/session only when Galih asks to avoid login retry.

## Posting pattern

1. Navigate to `https://x.com/compose/post` with cookies injected.
2. Fill `[data-testid="tweetTextarea_0"]`.
3. X may leave multiple `tweetButton*` buttons in DOM. Pick the visible enabled button, not `.last()` blindly.
4. Click post.
5. Verify by opening the profile and checking visible post text and/or `/status/<id>` links.
6. If X shows transient `Something went wrong` after post-click, do not assume failure. Re-open the profile and verify status links; the post may have succeeded.

## Follow-back pattern

1. Navigate to `https://x.com/<target_handle>`.
2. Wait for the profile body to load; sometimes first read is partial/blank.
3. Handle both `Follow` and `Follow back` buttons. For Galih's account the visible button can be exactly `Follow back`, with aria label `Follow back @mhmdgalihsptraa`.
4. Click the follow/follow-back button.
5. Verify by reloading the target profile from the actor account and checking both:
   - `Following`
   - `Follows you`

## Verification language

- `posted`: profile/status link verified.
- `followed`: target profile shows `Following` and `Follows you` from actor account.
- `post-clicked-unverified`: click happened, but no profile/status proof yet; must re-check before telling Galih it worked.
- `unknown` with blank body: likely page-load timing; retry a profile debug/read before concluding failure.

## Pitfalls observed

- Generic follow automation missed `Follow back`; include that exact button text.
- X can return blank/partial body on first profile read even when the session is fine; retry once with longer wait.
- Button locator `.last()` can pick a disabled compose button; inspect all tweet buttons and click the enabled visible one.
- X profile may show transient error content while status links already exist; profile re-check is the source of truth.
