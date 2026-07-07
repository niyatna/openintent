# Hermes Behavior QA Suite

Purpose: test Keiya/default and Galyarder behavior after access, autonomy, relay, config, or identity changes.

This suite is intentionally documentation-first plus script-verifiable invariants. Some checks are static, some require live conversation/manual prompt testing.

Run quick static/runtime checks:

```bash
/home/galyarder/.hermes/scripts/agent-os-quick behavioral-regression
/home/galyarder/.hermes/scripts/agent-os-access-hardening-audit.py
```

Files:

- `keiya-behavior-tests.md` — Keiya identity, media, tone, tools, GWS/Obsidian boundaries.
- `galyarder-behavior-tests.md` — Galyarder tool discipline, relay, execution, company/system boundaries.
- `access-boundary-tests.md` — cross-profile allowed vs confirmation-required actions.
- `relay-tests.md` — Discord bot-to-bot raw mention and no-ping-pong behavior.
- `access-rollout-runbook.md` — one-access-at-a-time maturity loop.
- `config-hardening-audit.md` — config checklist and latest audit evidence.

Promotion rule:

- one-off failure → fix current session;
- repeated behavior issue → patch SOUL or skill;
- stable user/environment fact → memory;
- reusable procedure → skill;
- readable long protocol/evidence → Obsidian.
