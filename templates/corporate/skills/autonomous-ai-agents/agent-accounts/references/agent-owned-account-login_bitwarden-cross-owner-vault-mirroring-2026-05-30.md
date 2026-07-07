# Bitwarden cross-owner vault mirroring (2026-05-30)

Use this when Galih approves copying one agent-owned credential set (for example Keiya) into another agent's Bitwarden org vault (for example Galyarder), without touching Bitwarden Secrets Manager/BWS.

## Trigger

- User says the source agent's Bitwarden has both sets, but destination agent's Bitwarden only has its own secrets.
- User explicitly approves adding `Keiya` credentials into `Galyarder` Bitwarden, or the reverse.
- Scope is local private credential store under `/home/galyarder/.hermes/private/credentials/agents/<source>/` into destination Bitwarden account/org.

## Boundary

- Do **not** print secrets, Bitwarden session keys, passwords, TOTP seeds, PATs, cookies, private keys, recovery codes, or raw storage.
- Do **not** touch Galih personal credentials unless separately approved.
- Do **not** playwright-pro to Bitwarden Secrets Manager/BWS unless explicitly approved; this is vault/org item mirroring only.
- Prefer org collection target when destination account can write there; keep item names owner-prefixed (`Keiya / ...`, `Galyarder / ...`) to avoid ambiguity.

## Durable workflow

1. Load the destination Bitwarden account credentials from:
   `/home/galyarder/.hermes/private/credentials/agents/<dest>/bitwarden/account.txt`.
2. Set `XDG_CONFIG_HOME` to the destination Bitwarden CLI config directory:
   `/home/galyarder/.hermes/private/credentials/agents/<dest>/bitwarden/bw-cli-config`.
3. `bw login` if unauthenticated, then `bw unlock --passwordenv BW_PASSWORD --raw`; never print the session.
4. `bw sync`, list orgs, locate org `galyarder-labs`, locate collection `Koleksi Default` or first visible collection.
5. Build one item per service/account using local source files from:
   `/home/galyarder/.hermes/private/credentials/agents/<source>/...`.
6. For normal `account.txt` / `.env` / backup-code text files:
   - store exact content in hidden custom fields when under Bitwarden field size;
   - store `mode`, `size`, `sha256` metadata in visible text fields.
7. For large browser/session files (`cookies.json`, `storage-state*.json`):
   - store metadata (`mode`, `size`, `sha256`);
   - base64 chunk into hidden fields (tested with 1000-char chunks) when exact vault copy is required.
8. Create/edit Bitwarden items using stdin for encoded JSON when payloads are large; CLI argv can hit argument-size or value limits.
9. If `bw create item` includes `organizationId` and `collectionIds`, the item may already be created inside the org. A follow-up `bw move` can return `This item already belongs to an organization.` Treat that as a non-fatal informational warning **only if** the final org verification proves the item exists in the expected org/collection.
10. Final verification must list org items from destination account and check:
    - expected item count for each owner group;
    - `missing=[]`;
    - `duplicates=[]`;
    - `organizationId_present=true`;
    - `collection_count>=1`;
    - `bw lock` succeeded.

## Safe evidence format

Report only non-secret evidence, e.g.:

```text
status: done
target: Galyarder Bitwarden org vault
org: galyarder-labs
collection: Koleksi Default
Galyarder items: 10/10
Keiya items: 9/9
missing: 0
duplicate: 0
CLI locked: yes
BWS/Secrets Manager: untouched
```

Item names are safe to list. Field counts, source-field counts, chunk-field counts, collection counts, and sha256 metadata are safe. Raw values are not.

## Known item sets from the 2026-05-30 migration

Galyarder items:

- `Galyarder / Bitwarden account`
- `Galyarder / GitHub account + PAT`
- `Galyarder / Google Workspace account`
- `Galyarder / Instagram account`
- `Galyarder / Threads account`
- `Galyarder / X account`
- `Galyarder / Canva browser session`
- `Galyarder / Leonardo browser session`
- `Galyarder / Wallet + Coinbase AgentKit`
- `Galyarder / Pearl wallet`

Keiya items:

- `Keiya / Bitwarden account`
- `Keiya / GitHub account + PAT`
- `Keiya / Google Workspace account`
- `Keiya / Instagram account`
- `Keiya / Threads account`
- `Keiya / X account`
- `Keiya / Canva browser session`
- `Keiya / Leonardo browser session`
- `Keiya / Wallet + Coinbase AgentKit`

Keiya does not have a Pearl item in this migration set unless a future source file exists and Galih approves adding it.
