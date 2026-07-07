# Meta 2FA/TOTP session gates — Instagram/Threads

## When this applies

Use when setting up authenticator-app 2FA for the Galyarder-owned Meta handle `galyarderlabs.ai` after login/cookie bootstrap.

## Durable lesson from the Camofox session

Meta Accounts Center can be reachable and show the correct account while still blocking 2FA setup behind an email verification gate. In the observed flow:

- Direct URL worked: `https://accountscenter.instagram.com/password_and_security/two_factor/`
- Correct account row appeared as `galyarderlabs.ai Instagram`.
- Selecting it opened a gate: `Check your email`.
- The code was sent to a masked address like `m*******9@gmail.com`, not necessarily the currently open `galyarderlabs@gmail.com` inbox.

Do not infer the target inbox from the agent account label. Trust the UI mask.

## Operational sequence

1. Verify Camofox/server state and authenticated Meta/Instagram page state.
2. Open Accounts Center 2FA direct URL.
3. Select the account by visible label, not by row index alone.
4. If email-code gate appears:
   - record only the masked destination and status;
   - search the exact available inbox if it matches the mask;
   - if not available, ask Galih for the code or access to that inbox;
   - do not claim 2FA/TOTP is configured.
5. After the gate clears, capture authenticator setup secret/QR.
6. Save `TOTP_SECRET` in the private account file only; never print it.
7. Confirm with `pyotp.TOTP(secret).now()` and submit the generated code.
8. Save backup codes to `backup-codes.txt` with mode `0o600`.
9. Final verification must be sanitized:
   - account status field;
   - cookie file exists + cookie count, not cookie values;
   - backup code file non-empty + count, not codes;
   - `TOTP_SECRET` present + pyotp code has expected six-digit shape, not the secret/code;
   - file modes `0o600` and private dirs `0o700`;
   - access-hardening pass if available.

## Status vocabulary

- `credential-stored-pending-login-session`: credentials exist but no verified login/cookie session.
- `login-active`: authenticated browser context proved access.
- `cookies-active`: fresh cookie-only context proved access.
- `email-verification-gated`: Meta requires code from masked email before setup can continue.
- `meta-totp-registered`: Meta accepted a pyotp-generated authenticator code.
- `backup-codes-captured`: backup code file is non-empty and mode `0o600`.

## Pitfalls

- Zero-byte `backup-codes.txt` is not success.
- A `TOTP_SECRET` key in `account.txt` is not proof the secret is registered; it may be empty or pending.
- Google Workspace API `invalid_grant` is an OAuth-token problem, not proof the Gmail browser inbox is inaccessible.
- Himalaya account/config quirks are setup state; capture the usable fix/route, not a durable claim that email CLI is broken.
