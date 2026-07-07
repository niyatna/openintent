# Profile backup finalization for dedicated agent-owned repos

Use this when Galih asks to back up Keiya/Galyarder Hermes profiles to their dedicated GitHub repositories.

## Scope boundary

A profile distribution repo is a clean profile-layer package, not a full continuity or runtime backup.

Include only distribution-owned artifacts:

- `SOUL.md`
- `distribution.yaml`
- `mcp.json`
- `README.md`, `RESTORE.md`, `.gitignore`, `.env.EXAMPLE`
- `hooks/`, `cron/`, `scripts/`, `behavior-tests/`
- curated `memories/USER.md` and `memories/MEMORY.md`
- `skills/` documentation and reusable scripts/templates/references

Exclude runtime/private state:

- `.env`, auth/token files, cookies, backup codes, account files
- private credential registry, wallet keystores, seed/private-key material
- raw Hindsight/Honcho DBs, sessions, logs, caches, state DBs
- browser state, workspace/home/runtime process state
- skill hub indexes/audit logs and executable runtime bundles that are not portable profile source

## Recommended sequence

1. Mention peer agent once if Galih asked for it; use controlled relay only. Do not keep ping-ponging.
2. Verify dedicated GitHub wrappers first:
   - `/home/galyarder/.hermes/scripts/keiya-gh --check`
   - `/home/galyarder/.hermes/scripts/galyarder-gh --check`
3. Sync distribution-owned artifacts with `/home/galyarder/.hermes/scripts/update-profile-distributions.py` or an equivalent clean copy routine.
4. Before pushing, run a path/content scan over `git ls-files`:
   - forbidden paths: `.env`, `token.env`, `cookies.json`, `backup-codes`, `wallet-keystore`, `access-registry.yaml`, `sessions/`, `logs/`, `cache/`, `state.db`, `response_store.db`, `.tick.lock`, `.hub/`
   - obvious secret text: GitHub PATs, Google API keys, private-key PEM blocks, raw auth cookies
   - allow `.env.EXAMPLE` and docs that mention token concepts without concrete secret values.
5. Run verification before the final claim:
   - `HERMES_HOME=/home/galyarder/.hermes /home/galyarder/.hermes/scripts/agent-os-quick access-hardening`
   - `HERMES_HOME=/home/galyarder/.hermes /home/galyarder/.hermes/scripts/agent-os-quick behavioral-regression`
6. Push using the matching dedicated token/wrapper, not Galih's human account.
7. Fresh-clone/readback each remote and verify:
   - repo is private
   - default branch is `master`
   - clone `HEAD` equals local `HEAD`
   - required files exist
   - secret/runtime scan on clone is clean
8. Report commit hash, repo visibility/branch, verifier status, clone/readback status, and explicit "no secrets/runtime state tracked".

## Git push edge cases

- If local repo history diverges from the dedicated remote, fetch first. If the local distribution is the verified source of truth but remote has an older one-off backup history, merge `origin/master` with `--allow-unrelated-histories -s ours` to preserve remote ancestry while keeping local verified content, then resync distribution artifacts before pushing.
- If `git push` cannot read credentials over HTTPS, use `gh auth git-credential` with the agent-specific `GH_TOKEN` and `GH_CONFIG_DIR` for that command only. Do not print tokens; report only token presence/mode and wrapper login.
- Avoid hardcoding remotes to `muhamadgalihsaputra/*` for final dedicated backups. Expected dedicated remotes are `keiyazeyniputri/keiya-profile-distribution` and `galyarder-labs/galyarder-profile-distribution`.

## Report shape

Keep final user report short:

```text
backup final done.
Keiya: <repo>, PRIVATE, master, <commit>, clone/readback yes.
Galyarder: <repo>, PRIVATE, master, <commit>, clone/readback yes.
Verifiers: access-hardening pass, behavioral-regression pass.
Secret/runtime scan: clean; no credentials/runtime state tracked.
```
