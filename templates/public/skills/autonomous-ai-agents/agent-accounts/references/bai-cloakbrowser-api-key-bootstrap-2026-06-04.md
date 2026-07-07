# B.AI CloakBrowser API-key bootstrap (2026-06-04)

Use this reference when Galih asks to create/verify an agent-owned B.AI (`chat.b.ai`) account/API key using the owner’s existing Google account through CloakBrowser. Keep this under the `agent-accounts` umbrella because it is an account/session/API-secret bootstrap pattern, not a one-off B.AI skill.

## Scope

- Owner-scoped browser profile: `/home/galyarder/.hermes/private/browser-profiles/agents/<owner>/bai-cloakbrowser`
- Owner Google credential/session source: `/home/galyarder/.hermes/private/credentials/agents/<owner>/google/`
- Owner B.AI credential target: `/home/galyarder/.hermes/private/credentials/agents/<owner>/bai/`
- B.AI UI: `https://chat.b.ai/chat` and API-key page `https://chat.b.ai/key`
- B.AI API base: `https://api.b.ai` (`https://api.b.ai/v1` for OpenAI-compatible clients)

Never print the raw API key. Use masked form only, e.g. `sk-6w…abe4`.

## Durable flow

1. Verify the owner Google session first with the normal CloakBrowser Google helper or existing cookies. Owner-state proof must come from `myaccount.google.com`, not a public Google marketing/login page.
2. Launch owner-scoped CloakBrowser persistent context for B.AI and import current Google cookies into the context when needed.
3. Open `https://chat.b.ai/chat`, click `Log in`, then click `Continue with Google`.
4. Use `expect_popup` for the Google OAuth popup. B.AI’s Google button opens a popup, not just same-page navigation.
5. In the popup, select the owner account row (for Galyarder: `Galyarder Labs / galyarderlabs@gmail.com`). If the chooser does not have a live session, fall back to the standard Google email/password/TOTP flow.
6. On the Google consent screen, click `Lanjutkan` / `Continue`. The popup may close immediately after consent; do not call screenshot/body methods on the popup after that without checking `pop.is_closed()`.
7. Return to the main B.AI page, reload if needed, and verify logged-in state by absence of login modal plus owner/user controls, credits, and B.AI cookies.
8. Navigate to `https://chat.b.ai/key`.
9. Click `Create API key`, enter an owner-scoped descriptive name (example: `galyarder-test`), then click the modal `Create API key` button.
10. Capture the full key immediately from the creation modal DOM or from the `apiKey.createApiKey` response body. The table later only shows masked key. Store raw key only in the private credential directory.
11. Save:
    - `api-key.txt` — raw key, mode `600`
    - `api-key.env` — `BAI_API_KEY=<raw key>`, mode `600`
    - `metadata.json` — owner, service, account, masked key, base URL, file refs, mode `600`
    - `cookies.json` and `storage-state.cloakbrowser.json` — mode `600`
    - parent directory mode `700`
12. Test in two layers:
    - `GET https://api.b.ai/v1/models` with `Authorization: Bearer <key>`; this proves auth/key validity even before credits are available.
    - `POST https://api.b.ai/v1/chat/completions` with a tiny prompt; this proves spend/quota path.
13. If chat completion returns `insufficient_user_quota` and the page shows `Claim Free Credits`, click it, verify `usage.points` / visible balance updates, then retry the chat completion.

## Verification evidence to report

Report only secret-safe evidence:

- logged-in account identifier / B.AI user handle, not cookies
- key name and masked key only
- private credential directory path
- file modes (`700` dir, `600` secret files)
- `/v1/models` status and model count
- chat completion status and a harmless response like `BAI key ok`
- if credits were claimed: visible balance or `usage.points` result, without exposing session tokens

## Pitfalls

- B.AI’s Google OAuth uses a popup; if you click the button without `expect_popup`, the main page may look unchanged and you can falsely think the click failed.
- Google consent may be localized (`Lanjutkan`) because CloakBrowser uses `id-ID` locale.
- After clicking consent, the popup can close while Playwright still holds the page object. Guard with `pop.is_closed()` before reading text or taking screenshots; otherwise `TargetClosedError` is expected noise, not proof of failure.
- A successful `/v1/models` check can pass while chat completion fails with `insufficient_user_quota`; treat these as separate gates.
- Do not capture the key only from the key table after modal close. The table masks the key; capture raw key immediately from the modal or create API response.
- Do not write B.AI raw keys into memory, chat, SOUL, Obsidian, skills, or profile distributions. Only private credential files may hold the raw value.
