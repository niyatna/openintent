# Modal API token → CLI setup pattern (2026-05-30)

Use when Galih is setting up Modal CLI from the web dashboard for a dedicated/throwaway agent-owned workflow.

## What the dashboard token means

In Modal dashboard: `Settings → Tokens → API Tokens` is the correct page for CLI credentials.

The token created there maps directly to:

```bash
modal token set --token-id <TOKEN_ID> --token-secret <TOKEN_SECRET> --profile <profile-name> --activate --verify
```

- `Token ID` → `--token-id`
- `Token Secret` → `--token-secret`

Do not ask for screenshots of visible secrets; ask for text values or use the browser/session if already available. Never echo secrets back in final replies or logs.

## Verification ladder

After setting the token:

```bash
modal profile current
modal token info
modal app list
```

Sanitize output if it may contain token-like values:

```bash
sed -E 's/(ak-[A-Za-z0-9]+|as-[A-Za-z0-9]+)/[REDACTED]/g'
```

Expected healthy signs:

- `Token verified successfully!`
- `Token written to ... .modal.toml`
- `modal token info` shows workspace/user metadata
- `modal app list` runs without `Token missing`

## Style / execution note

If Galih has explicitly accepted account-ban/credit-burn risk, do not repeat ToS warnings. Set the token, verify, then report only current gates such as wallet, payment, or explicit remote-run approval.
