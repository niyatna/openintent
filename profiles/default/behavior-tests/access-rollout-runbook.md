# Access Rollout Runbook

Purpose: implement the Mahiru/Waguri maturity loop without copying unsafe autonomy blindly.

Core loop:

```text
profile → one access → behavior contract → small test → correction → durable promotion → next access
```

## 0 — choose exactly one access

Do not add several credentials/tools at once.

Record:

- domain name;
- profile(s): default, corporate-agent, public-agent;
- owner status: agent-owned, user-owned, shared, or business-owned;
- credential reference only: env var names and paths, never secret values;
- allowed read/write/admin operations;
- autonomous, autonomous+log, confirmation-required actions;
- verification method;
- recovery path.

Update:

- `~/.hermes/private/credentials/access-registry.yaml`
- relevant SOUL section only if durable behavior changes
- behavior test docs if a new boundary needs testing

## 1 — prepare credential safely

Allowed:

- store secrets in `.env`, OAuth stores, browser/cookie state, OS credential manager, or encrypted private store;
- set permissions: directories `700`, secret files `600`;
- reference paths/env vars in registry.

Forbidden:

- paste secret values into chat;
- write secrets into SOUL, memory, skills, Obsidian, profile repos, distribution artifacts, screenshots, logs, or issue trackers;
- commit auth/state DB/session/cookie files.

## 2 — write behavior immediately

Before using new access, write behavior contract:

- what the profile can do autonomously;
- what it may do autonomously but must log;
- what requires confirmation;
- what proof is required before claiming completion;
- what to do on auth failure/session expiry.

## 3 — read-only test

First test should be safe/read-only.

Examples:

- list profile/status;
- fetch own account metadata;
- read one known harmless item;
- query a test workspace/page/repo;
- check token/session validity without changing state.

Pass requires concrete output, not “seems OK”.

## 4 — safe write test if appropriate

Only after read-only pass.

Examples:

- create a draft, not send;
- create a private test issue/note/file;
- comment on a test item;
- update a local/private artifact.

Verify by readback/list/diff/API status.

## 5 — correction and promotion

If behavior is wrong:

- current-session fix for one-off task;
- SOUL patch for identity/access/autonomy behavior;
- skill patch for reusable procedure;
- memory for compact stable user/environment fact;
- Obsidian for readable protocol/audit;
- behavior QA doc for future tests.

## 6 — next access only after stability

Move to the next credential/tool only when:

- registry entry exists;
- read-only test passed;
- safe write test passed or was deliberately skipped;
- confirmation thresholds are clear;
- behavior QA covers the domain;
- recovery path exists.

## Autonomous login gate

Do not enable password/TOTP/backup-code login recovery for Galih’s primary personal accounts by default.

Autonomous login requires:

- dedicated agent-owned account or explicit user-owned exception;
- encrypted/private credential storage design;
- TOTP/backup-code recovery path;
- cookie/session storage policy;
- expiry detection;
- behavior tests;
- confirmation thresholds for public/external/destructive actions.

## Agent-owned account skeleton gate

default/corporate-agent/public-agent may create and validate placeholder-only account directories for planned dedicated accounts before credentials exist.

Current skeleton convention:

```text
~/.hermes/private/credentials/agents/{default,corporate-agent,public-agent}/{google,github,x,wallet}/
```

Allowed without further approval:

- create empty `account.txt`, `backup-codes.txt`, and `cookies.json` placeholders;
- verify directory/file permissions (`700` directories, `600` files);
- run `account_check.py` and report whether required public fields exist;
- update non-secret registry entries and behavior tests.

Still confirmation-required:

- filling `PASSWORD`, `TOTP_SECRET`, backup codes, cookies, tokens, seed phrases, private keys, or recovery values;
- using browser cookies or starting autonomous login;
- sending email, posting social content, changing GitHub state, spending money, or signing wallet transactions;
- treating an empty skeleton as operational access.

Pass condition: skeleton checks can prove readiness for future account bootstrap, but they do **not** prove autonomous login or public-action autonomy.
