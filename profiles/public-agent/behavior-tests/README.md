# Hermes Behavior QA Suite

Purpose: test default operations, corporate, and public agent behavior after access, autonomy, relay, config, or identity changes.

This suite is intentionally documentation-first plus script-verifiable invariants. Some checks are static, some require live conversation/manual prompt testing.

Run quick static/runtime checks:

```bash
~/.hermes/scripts/agent-os-quick behavioral-regression
~/.hermes/scripts/agent-os-access-hardening-audit.py
```

Files:

- `public-behavior-tests.md` — public-agent identity, customer support, competitor tracking, web scraper tools, and external boundaries.
- `default-behavior-tests.md` (in default profile) — default agent identity, media, and local systems tasks.
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
