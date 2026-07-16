# Dedicated agent profile backup repos — 2026-05-16

Session pattern: Owner asked to make Co-Founder and Default GitHub accounts operational, then back up each profile distribution to a GitHub repo owned by the corresponding dedicated account.

## Correct PAT route

Do not use `gh auth login --web` to mint a token for a dedicated agent account when the machine/browser already has Owner's human GitHub session. In this session that route produced a token for `developer-account`, not the intended agent account.

Use GitHub web token settings from the dedicated account session instead:

- classic PAT fallback: `https://github.com/settings/tokens/new`
- scopes used successfully: `repo`, `workflow`, `read:user`
- save only to local private token file:
  - `~/.hermes/private/credentials/agents/co-founder/github/token.env`
  - `~/.hermes/private/credentials/agents/default/github/token.env`

Verify before any side effect:

```bash
~/.hermes/scripts/co-founder-gh --check
~/.hermes/scripts/default-gh --check
```

Required proof:

- Co-Founder `actual_login=co-founder`
- Default `actual_login=company-labs`
- token file mode `0o600`

## Profile backup repo pattern

For clean profile backup repos owned by each dedicated account:

1. Ensure remote repos exist and are private:
   - `co-founder/co-founder-profile-distribution`
   - `company-labs/default-profile-distribution`
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
~/.hermes/scripts/co-founder-gh repo view co-founder/co-founder-profile-distribution --json nameWithOwner,visibility,isPrivate,defaultBranchRef,pushedAt,url
~/.hermes/scripts/default-gh repo view company-labs/default-profile-distribution --json nameWithOwner,visibility,isPrivate,defaultBranchRef,pushedAt,url
```

## Discord relay to peer agent

When Owner asks to involve Co-Founder/Default via Discord, use one bounded packet:

- raw mention at start exactly once;
- state the task and verification commands;
- ask for one reply only;
- require the peer to mention back at the start;
- do not treat the peer reply as proof of side effects without direct verification.

## Pitfalls from this session

- `gh auth login --web` is not a token creation route for dedicated accounts on a machine already logged into the human account.
- Fine-grained PAT form automation can redirect to `/repos` without exposing a token; classic PAT page was the working fallback here.
- Secret scanners may flag skill documentation examples as secret-like; distinguish example text from real token leakage, but still check blocked filenames/paths explicitly.
