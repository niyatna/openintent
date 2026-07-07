# Bitwarden vault migration for agent-owned credentials (2026-05-30)

Use this as the concrete migration pattern after Bitwarden account/org readiness is already verified. This is for **Bitwarden user/org vault items**, not Bitwarden Secrets Manager / BWS machine flow.

## Scope boundary

Allowed scope when Galih approves "playwright-pro Galyarder-owned credentials to Bitwarden":

- `/home/galyarder/.hermes/private/credentials/agents/galyarder/**`
- only Galyarder / agent-owned / company credentials
- no Keiya or Galih personal credentials unless separately approved
- no BWS / Secrets Manager migration unless explicitly requested
- do not print secret values, raw cookies, tokens, TOTP secrets, recovery codes, session keys, or vault item JSON to chat/logs

## Recommended vault target

- Organization: `galyarder-labs`
- Collection: `Koleksi Default` or the first visible org collection if the name changes
- Item shape: class-level items per service/account, not one item per tiny file

Canonical safe item names used in the migration:

```text
Galyarder / Bitwarden account
Galyarder / GitHub account + PAT
Galyarder / Google Workspace account
Galyarder / Instagram account
Galyarder / Threads account
Galyarder / X account
Galyarder / Canva browser session
Galyarder / Leonardo browser session
Galyarder / Wallet + Coinbase AgentKit
Galyarder / Pearl wallet
```

## CLI hygiene

Use an owner-scoped Bitwarden CLI config home so global OS/user state is not polluted:

```bash
export XDG_CONFIG_HOME=/home/galyarder/.hermes/private/credentials/agents/galyarder/bitwarden/bw-cli-config
chmod 700 "$XDG_CONFIG_HOME"
```

Use `bw login --passwordenv`, `bw unlock --passwordenv --raw`, `bw sync`, and keep the session key in-process only. Never print `BW_SESSION` or raw item payloads.

After migration, `bw lock` and verify:

```bash
stat -c '%a %n' \
  /home/galyarder/.hermes/private/credentials/agents/galyarder/bitwarden/bw-cli-config \
  '/home/galyarder/.hermes/private/credentials/agents/galyarder/bitwarden/bw-cli-config/Bitwarden CLI/data.json'
```

Expected: directory `700`, data file `600`.

## Creating/updating items

Pattern:

1. `bw sync`
2. `bw list organizations --raw`; require org `galyarder-labs`
3. `bw list collections --organizationid <org_id> --raw`; choose collection
4. Build item JSON locally from private credential files.
5. For an existing item, `bw get item <id> --raw`, preserve server fields, update login/secure-note body, and preserve any `large:` chunk fields from prior large-file embedding.
6. Use `bw create item <encodedJson>` for new items.
7. Use `bw move <item_id> <org_id> <encodedCollectionIds>` for org ownership/collection assignment.
8. `bw sync` again.
9. Verify by listing org items and fetching each expected item. Report only names/counts/types/field counts.

## Bitwarden limits and large/session files

Important durable finding: Bitwarden attachments can fail with:

```text
Error: Not enough storage available.
```

That does **not** mean the vault item migration failed. It means the account/org attachment quota cannot store file attachments.

Fallback that worked:

- store small text files directly as hidden custom fields;
- custom field encrypted value has a 5000 character limit, so chunk large text/session files into hidden fields of ~1000 base64 characters each;
- store a text metadata field with encoding, chunk count, byte size, mode, and sha256;
- verify by fetching the item and counting `large:` fields.

Do not store active binary runtime wallet DBs or blockchain chainstate into Bitwarden free vault chunks. For Pearl, store account metadata, seed/passphrase/config if approved, and leave runtime DB/chain files local/private until BWS or a proper backup mechanism exists.

## Verification output shape

Final non-secret evidence should include:

```text
status: done/partial
org: galyarder-labs
collection: Koleksi Default
verified items: 10/10
missing: []
duplicates: []
item names: <safe names only>
large/session handling: chunked into hidden fields + sha256 metadata, or excluded with reason
CLI locked: true
local permissions: config 700, data/account files 600
BWS/Secrets Manager: untouched unless explicitly requested
```

## Discord relay caveat

If replying to another agent through Discord, use the raw mention at the visible start. Be careful with tools or gateways that sanitize/mask mention strings in arguments or duplicate-send guards; if the mention is masked in the sent message, report the substantive status to the human and avoid spammy retry loops unless the human asks for a corrected relay.