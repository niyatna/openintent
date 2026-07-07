# Dedicated agent profile backup repos — 2026-05-16

Session pattern: Galih asked to make Keiya and Galyarder GitHub accounts operational, then back up each profile distribution to a GitHub repo owned by the corresponding dedicated account.

## Correct PAT route

Do not use `gh auth login --web` to mint a token for a dedicated agent account when the machine/browser already has Galih's human GitHub session. In this session that route produced a token for `muhamadgalihsaputra`, not the intended agent account.

Use GitHub web token settings from the dedicated account session instead:

- classic PAT fallback: `https://github.com/settings/tokens/new`
- scopes used successfully: `repo`, `workflow`, `read:user`
- save only to local private token file:
  - `/home/galyarder/.hermes/private/credentials/agents/keiya/github/token.env`
  - `/home/galyarder/.hermes/private/credentials/agents/galyarder/github/token.env`

Verify before any side effect:

```bash
/home/galyarder/.hermes/scripts/keiya-gh --check
/home/galyarder/.hermes/scripts/galyarder-gh --check
```

Required proof:

- Keiya `actual_login=keiyazeyniputri`
- Galyarder `actual_login=galyarder-labs`
- token file mode `0o600`

## Profile backup repo pattern

For clean profile backup repos owned by each dedicated account:

1. Ensure remote repos exist and are private:
   - `keiyazeyniputri/keiya-profile-distribution`
   - `galyarder-labs/galyarder-profile-distribution`
2. Build a clean distribution tree from the curated profile distribution source, not from raw live profile home.
3. Include profile layer only:
   - `SOUL.md`
   - `distribution.yaml`
   - `mcp.json`
   - `README.md` / `RESTORE.md`
   - `.env.EXAMPLE` / `.gitignore`
   - `hooks/`
   - `scripts/`
   - `behavior-tests/`
   - curated `memories/USER.md` and `memories/MEMORY.md`
   - `skills/`
4. Exclude secrets and runtime state:
   - `.env`, auth/token files, cookies, backup codes
   - private credential registry
   - raw Hindsight/state DBs
   - sessions, logs, caches
   - workspace/home/runtime process state
5. Push to each repo using the matching dedicated token only.
6. Verify repo state with each wrapper:

```bash
/home/galyarder/.hermes/scripts/keiya-gh repo view keiyazeyniputri/keiya-profile-distribution --json nameWithOwner,visibility,isPrivate,defaultBranchRef,pushedAt,url
/home/galyarder/.hermes/scripts/galyarder-gh repo view galyarder-labs/galyarder-profile-distribution --json nameWithOwner,visibility,isPrivate,defaultBranchRef,pushedAt,url
```

## Discord relay to peer agent

When Galih asks to involve Keiya/Galyarder via Discord, use one bounded packet:

- raw mention at start exactly once;
- state the task and verification commands;
- ask for one reply only;
- require the peer to mention back at the start;
- do not treat the peer reply as proof of side effects without direct verification.

## Pitfalls from this session

- `gh auth login --web` is not a token creation route for dedicated accounts on a machine already logged into the human account.
- Fine-grained PAT form automation can redirect to `/repos` without exposing a token; classic PAT page was the working fallback here.
- Secret scanners may flag skill documentation examples as secret-like; distinguish example text from real token leakage, but still check blocked filenames/paths explicitly.
