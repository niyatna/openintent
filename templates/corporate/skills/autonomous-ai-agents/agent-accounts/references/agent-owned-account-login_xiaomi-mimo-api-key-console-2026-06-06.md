# Xiaomi MiMo API key creation via CloakBrowser (2026-06-06)

Use after a dedicated agent-owned Xiaomi MiMo account is logged in through the owner-scoped CloakBrowser Google profile.

## Scope

- Account tested: Galyarder dedicated account (`/home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser`).
- Console page: `https://platform.xiaomimimo.com/console/api-keys`.
- Credential root: `/home/galyarder/.hermes/private/credentials/agents/<owner>/xiaomi/`.
- Never print API keys, cookies, passwords, session JSON, or raw key values in chat/tool summaries.

## Proven flow

1. Ensure Google owner-state if needed:
   ```bash
   HOME=/home/galyarder /home/galyarder/.hermes/scripts/cloak_google_profile.py --owner galyarder --timeout-ms 90000
   ```
2. Launch the owner-scoped CloakBrowser persistent profile and go directly to:
   `https://platform.xiaomimimo.com/console/api-keys`.
3. Close only cookie/noise overlays. Do not close required platform agreement modals before accepting them.
4. Click `Create API Key`.
5. Fill `API Key Name` with a stable descriptive name such as `galyarder-xiaomi-mimo-api-key`.
6. Click `Confirm`.
7. The key is visible/copyable only at creation time. Extract it immediately from the disabled input in the success modal and store it privately.

## Private storage contract

Recommended file:

```text
/home/galyarder/.hermes/private/credentials/agents/<owner>/xiaomi/api-key.txt
```

Recommended mode: directory `700`, file `600`.

Recommended content shape:

```dotenv
ACCOUNT_ID=<owner>-xiaomi
OWNER=<owner>
SERVICE=xiaomi-mimo
TYPE=api-key
BASE_URL=https://api.xiaomimimo.com/v1
ALT_BASE_URL=https://token-writing-plans-sgp.xiaomimimo.com/v1
MODEL_HINT=mimo-v2.5-pro,mimo-v2.5-flash,mimo-v2.5-omni
API_KEY=<secret; never print>
SHA256=<sha256 of API_KEY for safe identity checks>
CREATED_AT=<UTC ISO timestamp>
NOTES=Created via CloakBrowser Xiaomi MiMo console. Do not print this key.
```

Add `API_KEY_FILE=/home/galyarder/.hermes/private/credentials/agents/<owner>/xiaomi/api-key.txt` to the owner `xiaomi/account.txt` if present.

## Verification without leaking the key

Read the key from the private file in-process, then call:

- `GET https://api.xiaomimimo.com/v1/models`
- small `POST https://api.xiaomimimo.com/v1/chat/completions` with `max_tokens` tiny and a harmless prompt (`Say OK only.`)

Verified result for the Galyarder key:

- `https://api.xiaomimimo.com/v1/models` returned `200` with 10 models, including `mimo-v2.5-pro`, `mimo-v2.5`, `mimo-v2-flash`, `mimo-v2-omni`.
- Tiny chat completion returned `200` and `OK`.
- `https://token-writing-plans-sgp.xiaomimimo.com/v1` returned `401` for this key, so use `https://api.xiaomimimo.com/v1` as canonical base.

## Pitfalls

- Do not announce “saved” before verifying the key file exists with mode `600` and the API returns `200`.
- Do not paste or log the raw key. In tool output, report only key path, length, sha256 prefix, HTTP statuses, and model names.
- The API key page table may show a masked key after creation; the full key is only available in the success modal at creation time.
- Do not confuse MiMo bonus credits/token balance with real-money spend. API-key creation itself is a credential action; store securely and verify, but it is not a payment action.
