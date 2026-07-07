# Galyarder Labs GitHub org role baseline

Source: Galih-provided GitHub organization role-assignment text on 2026-05-19. Treat this as the intended operating baseline, but verify live GitHub permissions before any sensitive or write/destructive action.

## Accounts and assigned org roles

### `galyarder-labs`

Assigned roles in `galyarderlabs`:

- All-repository read
- All-repository write
- CI/CD Admin
- Security manager

Operating meaning:

- can read all org repositories;
- can write/push branches/commits where token scope allows;
- can create/edit PRs and issues as normal repo work;
- can manage GitHub Actions policies, runners, runner groups, network configurations, secrets, variables, and usage metrics;
- can manage security policies, security alerts, and security configuration across org repositories.

No explicit All-repository maintain/admin or Apps manager role was listed for this account.

### `keiyazeyniputri` / Keiya

Assigned roles in `galyarderlabs`:

- All-repository read
- All-repository maintain
- CI/CD Admin
- Security manager

Operating meaning:

- can read all org repositories;
- can maintain all repositories at repo-settings/maintenance level where GitHub role semantics allow;
- can do normal repo work and higher repo-maintenance actions where token scope allows;
- can manage GitHub Actions policies, runners, runner groups, network configurations, secrets, variables, and usage metrics;
- can manage security policies, security alerts, and security configuration across org repositories.

No explicit All-repository admin or Apps manager role was listed for this account.

### `muhamadgalihsaputra` / Galih

Assigned roles in `galyarderlabs`:

- All-repository read
- All-repository write
- Apps manager
- Security manager

Operating meaning:

- Galih remains the human owner/final decision maker;
- do not use Galih's personal GitHub credential for agent-owned work unless he explicitly asks;
- Apps manager means app management power belongs to Galih's account path unless separately delegated.

## Permission vs action policy

Role access is capability, not automatic permission to use it.

Autonomous when scoped by Galih's request and reversible:

- read repo/issues/PRs/actions/security status;
- clone/fetch/list/search;
- create branches/commits/PRs for requested work;
- comment/update issues or PRs when part of the requested workflow;
- read GitHub Actions status/log metadata.

Still requires explicit confirmation:

- deleting repos/branches/tags/releases;
- force-pushes or history rewrites;
- changing org/repo permissions, member roles, public visibility, default branches, branch protection, security settings, CI/CD policies/runners/network settings;
- creating/editing/deleting secrets or variables;
- enabling/disabling workflows at org/repo policy level;
- installing/managing GitHub Apps;
- any production deploy, billing, or security-impacting change.

## Verification commands

Use dedicated wrappers, not Galih's global `gh`, for agent-owned account work:

```bash
/home/galyarder/.hermes/scripts/galyarder-gh --check
/home/galyarder/.hermes/scripts/keiya-gh --check
```

For repo-level effective permissions, verify with live API before relying on the role assignment text:

```bash
/home/galyarder/.hermes/scripts/galyarder-gh api /repos/galyarderlabs/<repo> --jq '{full_name,private,permissions}'
/home/galyarder/.hermes/scripts/keiya-gh api /repos/galyarderlabs/<repo> --jq '{full_name,private,permissions}'
```

For Actions/security/org-role work, first check token scopes and then perform the smallest read-only API call for the exact endpoint. If the wrapper token lacks required scopes despite org role assignment, refresh/create the dedicated account token rather than falling back to Galih's personal token.
