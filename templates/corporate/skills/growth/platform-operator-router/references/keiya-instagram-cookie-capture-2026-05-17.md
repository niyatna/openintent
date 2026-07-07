# Keiya Instagram cookie capture — 2026-05-17

Sanitized session detail from completing Keiya Instagram login and cookie capture. No secrets, cookies, codes, or passwords are stored here.

## What mattered

- Keiya Instagram used the same Meta credential pair as Keiya Threads, but Instagram cookies had to be captured separately.
- Initial login automation failed because the Instagram web login form did not use the expected `username/password` field names.
- `account.txt` had shell-style single quotes around the password value; automation had to strip one wrapping quote pair before filling the form, without printing or rewriting the secret.
- The profile page could still contain footer/header text like `Log In` / `Sign Up` even after successful authentication. Owner controls were the reliable proof.

## Robust login selectors

When filling Instagram web login, include these variants:

```js
const userInput = page.locator(
  'input[name="username"], input[name="email"], input[autocomplete*="username"], input[type="text"]'
).first();

const passInput = page.locator(
  'input[name="password"], input[name="pass"], input[type="password"], input[autocomplete="current-password"]'
).first();
```

If the body says something like `See everyday moments... Open Instagram / Log in / Sign up`, inspect actual DOM `input` nodes before assuming there is no login form.

## Secret parsing rule

When reading `KEY=VALUE` account files for browser automation:

```js
let value = rawValue.trim();
if ((value.startsWith("'") && value.endsWith("'")) ||
    (value.startsWith('"') && value.endsWith('"'))) {
  value = value.slice(1, -1);
}
```

Do not print the parsed value. Report only sanitized booleans/lengths if needed.

## Auth classifier rule

Do not fail authentication just because the page text contains login/signup words. Instagram profile pages can include these words in global UI/footer text.

Treat Keiya Instagram as owner-state when the profile URL contains/loads `keiyazeyniputri` and at least one owner control is visible, for example:

- `Edit profile`
- `View archive`
- `Professional dashboard`
- `New`
- `Messages`

Then perform a fresh-context cookie-only smoke test by injecting saved cookies and rechecking owner-state before setting `STATUS=cookies-active-*`.

## Verified final shape from this session

- Real login submitted password + TOTP.
- Owner-state proof included `Edit profile` and `View archive`.
- Fresh cookie-only smoke test passed.
- `account.txt`, `cookies.json`, and `backup-codes.txt` remained `0600`.
- Registry owner status was updated only after the smoke test passed.
