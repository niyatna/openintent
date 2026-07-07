# GitHub Agent PAT Regeneration and 2FA Checkup Flow

When agent-owned GitHub operations fail with `HTTP 401 Bad credentials`, it typically indicates that the personal access token (PAT) stored in `token.env` has expired. Standard CLI re-login is not suitable for autonomous agents operating headless. The token must be regenerated via the browser using the agent's persistent CloakBrowser profile and credentials.

---

## 1. Diagnostics & Detection

1. **Token Expiry Indicator**:
   API calls return:
   ```json
   {
     "message": "Bad credentials",
     "documentation_url": "https://docs.github.com/rest"
   }
   ```
2. **Settings Check**:
   Navigating to `https://github.com/settings/tokens` showing:
   ```text
   hermes-agent-token — Expired yesterday.
   ```

---

## 2. Handling the 2FA Checkup (Lockout Page)

GitHub occasionally blocks settings/profile access with a "one-time verification of your recently configured 2FA credentials" page.

- **Title**: `Verify two-factor authentication`
- **Symptom**: Page redirects from `/settings/profile` or developer settings to a checkpoint prompting to "Verify 2FA now" or "skip 2FA verification".
- **Step 1**: Find and click the "Verify 2FA now" element (e.g. `page.get_by_role('button', name=/Verify 2FA/i)`).
- **Step 2**: The page redirects to `/settings/two_factor_checkup`. Generate local TOTP code from `account.txt` using the base32 `TOTP_SECRET`.
- **Step 3**: Locate the single input `input[name="app_otp"]` or split inputs, fill the code, and submit (press Enter).
- **Step 4**: Upon successful verification, the page displays "2FA verification successful!". Click the "Done" button (`page.get_by_role('button', name=/Done/i)`) to save the verification state and return to normal settings navigation. Failing to click "Done" leaves the session locked.

---

## 3. Direct Token Regeneration

Instead of navigating the complex GitHub Developer Settings UI manually:
1. Identify the direct numeric token ID from the `/settings/tokens` links. The URL format is `https://github.com/settings/tokens/<id>`.
2. Navigate directly to the regeneration initiator:
   ```text
   https://github.com/settings/tokens/<id>/regenerate?index_page=1
   ```
3. **Sudo Password Prompt**: If GitHub requests password confirmation (sudo mode), autofill the `#sudo_password` field with the `PASSWORD` value from `account.txt` and submit.
4. **Final Confirmation**: Click the primary token regeneration confirmation button:
   ```python
   page.locator('button[type="submit"]:has-text("Regenerate token")')
   ```
5. **Token Extraction**:
   The regenerated token is displayed on `/settings/tokens` only once.
   - Look for the token string inside `#new-token`, `.token-value`, `input[readonly]`, or `code` tags.
   - Match the regex pattern `^ghp_[A-Za-z0-9]+$` to isolate the token.
   - If not found immediately, do **not** refresh the page. Execute a DOM sweep of elements containing `ghp_`.

---

## 4. Environment Assembly

Update the agent's GitHub `token.env` file (mode `600`) with the new token:
```dotenv
# GitHub Personal Access Token (Classic) for galyarder
GITHUB_TOKEN=ghp_XYZ...
TOKEN_KIND=classic
TOKEN_STATUS=active
TOKEN_CREATED_AT=2026-06-16T00:00:00Z
TOKEN_EXPECTED_LOGIN=galyarder-labs
TOKEN_SCOPES=read:user,repo,workflow
```
Confirm the updated token works by running:
```bash
GH_TOKEN=<token> gh api user --jq '.login'
```

---

## 5. Organization Invitation State Acceptance

To accept pending organization invitations programmatically using the new token:
```bash
# Accept invitation to org (e.g. niyatna)
GH_TOKEN=<token> gh api --method PATCH /user/memberships/orgs/niyatna -f state=active
```
Verify the active membership by listing org members:
```bash
GH_TOKEN=<token> gh api /orgs/niyatna/members --jq '.[] | .login'
```
