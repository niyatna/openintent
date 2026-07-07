---
name: antigravity-cli
description: Use when delegating coding, repo inspection, refactoring, bugfixing, documentation, second-opinion review, or file-aware analysis to the Antigravity CLI (`agy`) from Hermes.
version: 1.0.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    category: autonomous-ai-agents
    tags:
      - Coding-Agent
      - Antigravity
      - agy
      - Code-Review
      - Refactoring
      - Automation
    related_skills:
      - claude-code
      - opencode
      - pi-cli
      - codex
---

# Antigravity CLI (`agy`) — Hermes Orchestration Guide

## Overview

Use Antigravity CLI through the `agy` binary as a coding/review worker from Hermes. Keiya and Galyarder should route implementation or long technical work to the right coding agent instead of hand-coding inside the main chat. `agy` is one of the approved coding-agent routes.

Verified live on Galih's machine:

```text
agy path: /home/galyarder/.local/bin/agy
smoke command: agy -p 'Respond exactly AGY_SMOKE_OK' --print-timeout 60s
smoke result: AGY_SMOKE_OK
```

## When to Use

Use when:

- Galih asks to use Antigravity or `agy`.
- A repo task needs file-aware coding, review, refactor, docs, or analysis.
- You need a one-shot coding worker for bounded implementation or second opinion.
- A task should not be hand-coded by Keiya/Galyarder inside the main Hermes chat.

Prefer Kanban when the work is long-running, multi-specialist, parallel, audit-heavy, crash-survivable, or expected to have review loops.

Prefer Claude Code/OpenCode/Pi/Codex when a specific route is better suited or explicitly requested.

## Live CLI Surface

`agy --help` shows:

```text
Usage of agy:
  --add-dir                       Add a directory to the workspace (repeatable) (default [])
  -c                              Short alias for --continue
  --continue                      Continue the most recent conversation
  --conversation                  Resume a previous conversation by ID
  --dangerously-skip-permissions  Auto-approve all tool permission requests without prompting
  -i                              Short alias for --prompt-interactive
  --log-file                      Override CLI log file path
  -p                              Short alias for --print
  --print                         Run a single prompt non-interactively and print the response
  --print-timeout                 Timeout for print mode wait (default 5m0s)
  --prompt                        Alias for --print
  --prompt-interactive            Run an initial prompt interactively and continue the session
  --sandbox                       Run in a sandbox with terminal restrictions enabled

Available subcommands:
  changelog       Show changelog and release notes
  help            Show help for subcommands
  install         Configure environment paths and shell settings
  plugin          Manage plugins (install, uninstall, list, enable, disable)
  plugins         Alias for plugin
  update          Update CLI
```

## One-Shot Mode — Default

Use print mode for bounded work:

```bash
agy -p 'Inspect this repo and identify the top 5 concrete issues. Do not edit files.' \
  --print-timeout 5m
```

Hermes terminal pattern:

```python
terminal(
  command="agy -p 'Review the current diff for bugs. Do not edit files.' --print-timeout 5m",
  workdir="/path/to/repo",
  timeout=360,
)
```

For tasks that may need additional workspace roots:

```bash
agy --add-dir /path/to/extra/context \
  -p 'Use the repo and extra context to propose the smallest implementation writing-plans.' \
  --print-timeout 5m
```

## Interactive / Continued Work

Use interactive mode only when follow-up is genuinely needed:

```bash
agy -i 'Start by inspecting this repo and wait for my next instruction.'
agy --continue
agy --conversation <conversation-id>
```

In Hermes, long interactive sessions should run with `background=true` and be monitored with `process` tools. Do not leave sessions running unattended.

## Permission and Sandbox

- `--sandbox` runs with terminal restrictions enabled. Prefer this for untrusted or exploratory work.
- `--dangerously-skip-permissions` auto-approves tool permission requests. Use only when the workspace is trusted and the task is scoped. Avoid for destructive operations.
- Even when `agy` reports success, verify file changes yourself with `git diff`, build/test output, browser QA, or source reads before telling Galih work is done.

## Recommended Workflow

1. Set `workdir` to the repo root.
2. Run a quick prerequisite check yourself if needed (`git status`, relevant files, current failure).
3. Route the bounded task to `agy` with `-p` and a timeout.
4. Read the output; if it changed files, inspect `git diff`.
5. Run the relevant verification command yourself.
6. Report only verified outcomes to Galih.

## Prompt Template

```text
You are an Antigravity coding worker. Work inside this repository only.
Goal: <specific outcome>
Constraints: smallest safe change, no unrelated refactor, preserve secrets, keep public/private boundaries.
Output: changed files, rationale, verification commands run or recommended.
If blocked: state the exact blocker and stop.
```

## Common Mistakes

- Calling the old route `antigravity-cli`. Galih corrected this: the current coding-agent route is `antigravity-cli` / `agy`.
- Letting Keiya or Galyarder hand-code for a long time instead of routing to a coding agent or Kanban.
- Using `--dangerously-skip-permissions` on a broad or risky task.
- Trusting `agy` self-reports without independent diff/build/test/browser verification.
- Forgetting `--print-timeout` for non-trivial print-mode tasks.
