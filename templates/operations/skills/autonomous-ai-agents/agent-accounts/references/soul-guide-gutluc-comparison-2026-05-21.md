# SOUL Guide Gutluc comparison — reusable notes

Source reviewed: `https://soul-guide-gutluc.pages.dev`.

Use this reference when Galih asks to compare a new SOUL / Waguri / Mahiru-like agent setup guide against Keiya/Galyarder/Hermes Agent OS.

## Page playwright-pro pattern

For static docs sites, first discover the navigation/sitemap, then extract every page in batches. For the Gutluc site the useful page families were:

- overview and concepts: SOUL definition, philosophy, architecture;
- 10 pillars: identity, communication, capabilities, autonomy, boundaries, memory, verification, escalation, default disposition, resource management;
- practice pages: tool-use format, SOUL.md creation, credentials, memory/history, prompt-injection defense;
- backend/infra/tutorial pages: 9Router, Kiro, alternatives, VPS/PaaS, setup, deploy, systemd, maintain;
- appendix: sample SOUL.md, sample code, FAQ, credits.

Compare extracted content against live local state, not memory alone:

- current Keiya SOUL;
- current Galyarder SOUL;
- prior Mahiru/Waguri audit notes;
- current Agent OS verifier/report outputs;
- credential/access registry if relevant.

## Gutluc guide signal

Gutluc/Kai is a personal-agent variant of Mahiru/Waguri:

- philosophy: `user account = agent account` / agent as extension of self;
- reference stack: Telegram bot + Python + OpenAI-compatible API + VPS + systemd;
- concrete file blueprint: `main.py`, `SOUL.md`, `data/memory.json`, `history/<user_id>.json`, `credentials/*.env`;
- custom tool protocol: `<tool_use>{json}</tool_use>` with mandatory `risk: low|medium|high`;
- backend gating: low/medium auto, high saved as pending confirmation;
- secret redaction before saving history;
- per-user lock / busy status fast-path;
- daily/weekly/monthly maintenance scripts;
- backend market notes: 9Router, Kiro, OpenCode Free, Vertex AI, OpenRouter, Groq, DeepSeek, GLM/Kimi, self-host.

## What to adopt into Keiya/Galyarder/Hermes patterns

Adopt as patterns, not literal replacement:

1. **Risk-classification before dispatch** — use low/medium/high reasoning for shell/browser/platform/money actions even though Hermes native tools do not expose a visible `risk` field per call.
2. **Busy/status UX** — if a long task is running, user should be able to get a fast status: current task, age, and whether it is blocked/running/settled.
3. **Maintenance packaging** — daily service/disk/RAM/error checks and weekly cleanup/backup verification are useful as a profile health runbook or cron.
4. **External backend source map** — 9Router/Kiro/free-provider claims are leads, not facts; verify live before acting.
5. **SOUL size discipline** — keep stable identity/contract in SOUL; move procedural detail, examples, and session-specific lessons to skills/references/Obsidian.

## What not to copy blindly

- Do not apply pure `user account = agent account` to Galih's personal accounts. Treat personal/user-owned accounts as stricter and confirmation-gated for external, destructive, money, or reputation-affecting actions.
- Do not collapse Keiya and Galyarder into one generic extension-of-self agent. The role split is strategic.
- Do not replace Hermes native tool calling with a custom `<tool_use>` parser unless building a standalone non-Hermes agent.
- Do not trust backend/free/unlimited claims without current live verification.

## Verifier-drift lesson

During the Gutluc comparison, the older Waguri Obsidian audit said Keiya/Galyarder SOUL had exact headings like `Access Ownership Matrix`, `Autonomy Matrix`, and `Resource Management: start → use → stop`, but the live verifier reported those exact headings missing after later SOUL compression. Concepts may still exist in compact form while a verifier expects stale headings.

When auditing Agent OS state:

1. distinguish **concept missing** from **audit contract drift**;
2. either re-add a tiny canonical section to SOUL or update verifier invariants to accept the compact wording;
3. do not claim the baseline is gone solely because exact heading checks fail.
