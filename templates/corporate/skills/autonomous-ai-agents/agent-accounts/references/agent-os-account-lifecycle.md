# Reference: agent-os-account-lifecycle

# Agent OS Account Lifecycle

## Overview

Use this as the umbrella playbook for promoting Keiya/Galyarder account skeletons into operational dedicated agent-owned identities.

Core rule: **account access is not permission to act**. Each account needs owner, scope, credential path, allowed actions, confirmation threshold, recovery path, audit check, and proof before it becomes operational.

## Additional references

- `references/x-cookie-web-ops.md` — operating agent-owned X accounts with saved web cookies: posting, profile/status verification, and follow-back handling.
- `platform-operator-router` — operating the Galyarder-owned Instagram/Threads accounts through browser login/session cookies with Meta checkpoint boundaries and confirmation-gated public actions.
- `references/profile-backup-finalization.md` — final clean backup flow for Keiya/Galyarder profile distribution repos: sync scope, secret/runtime exclusion, dedicated GitHub push, clone/readback verification, and concise report shape.
- `references/galyarderlabs-github-org-roles.md` — Galih-provided GitHub organization role baseline for `galyarder-labs`, `keiyazeyniputri`, and `muhamadgalihsaputra`; verify live permissions before sensitive actions.
- `references/soul-guide-gutluc-comparison-2026-05-21.md` — reusable comparison notes for Gutluc's SOUL Guide: personal-agent `user account = agent account`, per-tool risk classification, busy/status UX, maintenance packaging, and verifier-drift lessons.

## Current lifecycle map

| Surface | Operational meaning | Verification |
|---|---|---|
| Google | login/session + TOTP baseline works | private `account.txt`, cookies mode `0o600`, status `login-active-*` |
| GitHub web/2FA | browser login + authenticator configured | status `github-2fa-enabled`, `TOTP_STATUS=github-totp-registered` |
| GitHub CLI/API | per-agent token validates expected login | `/home/galyarder/.hermes/scripts/{keiya,galyarder}-gh --check` |
| Galyarder Labs GitHub org roles | `galyarder-labs`: read+write+CI/CD Admin+Security manager; `keiyazeyniputri`: read+maintain+CI/CD Admin+Security manager; Galih remains final owner | use `references/galyarderlabs-github-org-roles.md` + live repo/API permission checks |
| X | active X session/API access | status must be `x-login-active`; blocked statuses are not operational; if email-first login hits unusual activity, retry username-first in a dedicated Brave CDP profile and then save cookies; before claiming reusable access, run a cookie-only smoke test and never print cookie values; for public posting via cookies, verify the resulting profile/status links because X may show transient “Something went wrong” even after a post succeeds |
| Instagram / Threads | Meta social session state for Galyarder Labs `galyarderlabs.ai` | credentials are local-only in private account files; Instagram and Threads share credentials but cookies are surface-specific; status is `credential-stored-pending-login-session` until authenticated profile/session and cookie-only smoke test verify access |
| Wallet | read-only/funded/signing capability by policy | status, keystore mode, no funds/no signing until spend policy exists |
| Profile backup | clean distribution repo under the dedicated account | private repo, branch, fresh clone/readback, secret boundary scan |

## Exact commands

### Access hardening

```bash
HERMES_HOME=/home/galyarder/.hermes /home/galyarder/.hermes/scripts/agent-os-quick access-hardening
```

Expected: `status=pass`, no errors, no warnings. If X has an approved populated password but status starts with `x-login-blocked-`, the verifier must classify it as operational credential state, not a writing-plansned skeleton violation.

### GitHub wrappers

```bash
/home/galyarder/.hermes/scripts/keiya-gh --check
/home/galyarder/.hermes/scripts/galyarder-gh --check
```

Expected actual logins:

- Keiya: `keiyazeyniputri`
- Galyarder: `galyarder-labs`

If `actual_login` is `muhamadgalihsaputra`, stop: a human-account token leaked into the dedicated flow. Remove it from the agent token file and redo via the dedicated account's GitHub web token page.

### Dedicated profile backup repos

Expected dedicated repos:

- `keiyazeyniputri/keiya-profile-distribution`
- `galyarder-labs/galyarder-profile-distribution`

Verify with:

```bash
/home/galyarder/.hermes/scripts/keiya-gh repo view keiyazeyniputri/keiya-profile-distribution --json nameWithOwner,visibility,isPrivate,defaultBranchRef,pushedAt,url
/home/galyarder/.hermes/scripts/galyarder-gh repo view galyarder-labs/galyarder-profile-distribution --json nameWithOwner,visibility,isPrivate,defaultBranchRef,pushedAt,url
```

Backups may contain SOUL, distribution manifests, restore/readme docs, hooks, scripts, behavior tests, curated memories, and skills. They must exclude `.env`, token files, cookies, account files, private credential registry, backup codes, wallet keystores, raw sessions, raw memory DB/state, logs, caches, workspace/home, and runtime auth state.

For final backup/push operations, follow `references/profile-backup-finalization.md`: sync only distribution-owned artifacts, scan paths and text before push, push via the matching dedicated GitHub token, fresh-clone/readback the remote, and report commit hashes plus explicit no-secret/no-runtime evidence.

## Status language

Use these words precisely:

- `verified`: fresh command or direct readback proves it.
- `partial`: local foundation exists but not usable for the external action.
- `blocked`: platform/security gate stops progress.
- `not operational`: credentials exist but session/API/signing is not verified.

Examples:

- X with `x-login-blocked-suspicious-login-prevented` = blocked, not operational.
- Wallet `wallet-keystore-created-read-only-no-funds-no-signing` = partial foundation, not operational spending.
- GitHub wrapper `github-token-valid` with expected login = operational CLI/API.

## Wallet policy gate

No wallet spend/signing until Galih defines:

1. network(s),
2. max spend per request/session/day,
3. allowlisted addresses/contracts/services,
4. confirmation threshold,
5. monitoring/revocation path,
6. recovery/backup path.

Coinbase Agentic Wallet path preference:

- first: Agentic Wallet MCP / `payments-mcp` for address/balance/x402 checks and guarded requests;
- later: `awal send/trade/x402 pay` only after policy and visible auth/UI repair.

## SOUL / Mahiru-Waguri / personal-agent alignment checklist

Both Keiya and Galyarder SOUL files should include the concepts below. Exact heading names are useful for verifiers, but do not confuse a missing heading with a missing concept after SOUL compression; check both text semantics and verifier invariants.

- access ownership and credential references;
- autonomy matrix or equivalent confirmation policy;
- public/external confirmation boundaries;
- resource lifecycle `start → use → stop`;
- autonomous login boundary;
- behavior QA loop;
- default disposition for risky actions;
- no raw secrets, tokens, passwords, cookies, keys, or temporary task dumps.

When comparing external SOUL guides, especially Gutluc/Kai-style personal-agent guides, preserve the distinction between:

- **user-owned/personal accounts** — stricter confirmation for public, external, destructive, money, credentials, or reputation-affecting actions;
- **agent-owned accounts** — can receive higher autonomy only after owner/scope/credential path/capabilities/verification/recovery are explicit;
- **business/shared accounts** — require product/company approval boundaries and audit trail.

Do not blindly adopt `user account = agent account` as a global rule for Galih. Treat it as a design option for a dedicated single-user agent, not as default policy for Keiya/Galyarder.

## Common pitfalls

1. Treating GitHub browser login as API access. It is not; wrapper check is required.
2. Using `gh auth login --web` for dedicated accounts while the real browser is logged into Galih's human account. This can mint a wrong-account token.
3. Treating X credential storage as login success. It is not; X session/API must be verified.
4. Treating wallet keystore creation as spending autonomy. It is not; policy + funding + signing verification are required.
5. Writing secrets into Obsidian, memory, skill files, profile repos, or chat.
6. Saying “done” before running the exact verifier.

## Verification checklist

- [ ] `agent-os-quick access-hardening` passes.
- [ ] GitHub wrappers return expected dedicated logins.
- [ ] Profile backup repos are private and clone/readback cleanly.
- [ ] X status is clearly marked active vs blocked.
- [ ] Wallet status is clearly marked read-only/no funds/no signing unless policy exists.
- [ ] SOUL alignment checked against Mahiru/Waguri baseline.
- [ ] Working.md updated with sanitized evidence only.