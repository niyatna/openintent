# Xiaomi MiMo CloakBrowser invite-code flow (2026-06-05)

Use when Galih asks to log into `platform.xiaomimimo.com` with the dedicated agent-owned Google account and enter an invite/referral code.

## Proven flow

- Use the Galyarder dedicated Google CloakBrowser profile:
  `/home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser`
- Verify Google owner-state first with `/home/galyarder/.hermes/scripts/cloak_google_profile.py --owner galyarder` if uncertain.
- Open `https://platform.xiaomimimo.com?ref=<CODE>`.
- If Xiaomi account does not yet exist, Google OAuth may create a Xiaomi account and then require setting a Xiaomi password (8-16 chars, at least 2 character classes). Generate/store it only in the private account file, e.g. `/home/galyarder/.hermes/private/credentials/agents/galyarder/xiaomi/account.txt` mode `600`; never print it.
- Console URL: `https://platform.xiaomimimo.com/console/balance`.
- First console visit may show an Open Platform agreement modal; tick the visible checkbox then click `Confirm`.
- The sidebar item is `Enter invite code +$2`, near the bottom-left sidebar. Do not confuse it with the top navbar `Refer & earn` button, which opens the account's own referral-code modal.
- Clicking `Enter invite code +$2` opens an `Invite code` modal with six Ant Design OTP-style inputs (`input.ant-otp-input`, labels `OTP Input 1` through `OTP Input 6`). Fill the invite code one character per input; keyboard typing the full six-character code into the first input works.
- Click `Redeem & get $2 credits`. Success modal text observed: `Invite more friends` and `View Recharge Details`.

## Verification

- Reopen `/console/balance` and read `Balance`, `Cash Balance`, and `Bonus Balance` snippets.
- For code `W85Q58`, balance verification after redeem showed `Balance $ 2.72`, `Cash Balance: $ 0.00`, `Bonus Balance: $ 2.72`.

## Pitfalls

- Do not refuse this as “agent cannot use its own Google account” when the request is for the dedicated agent-owned Galyarder/Keiya Google account and is within allowed scope.
- Do not classify Xiaomi MiMo `Enter invite code +$2` as real-money transfer/spend. It is platform bonus credit/token UI for API usage; treat it as a low-risk service-credit/referral action on the dedicated agent-owned account, while still verifying the final balance and avoiding secret leakage.
- Galih expects approved dedicated agent-owned account flows (Galyarder/Keiya Google via CloakBrowser, platform token-credit/referral flows, API-key creation) to be executed rather than refused as if they were personal-human logins or real-money transfers. Load the relevant account/login skill first when uncertain, then act with secret hygiene and proof.
- Headless clicks can hit nested wrapper elements; for the sidebar item, prefer Playwright locator: `page.locator('button').filter(has_text=re.compile('Enter invite code', re.I)).first.scroll_into_view_if_needed(); ...click(force=True)`.
- Cookie settings drawers/modals can block clicks; close only cookie-related overlays, not the required Open Platform agreement modal.
