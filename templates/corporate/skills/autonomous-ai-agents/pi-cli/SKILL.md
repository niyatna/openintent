---
name: pi-cli
description: Use when delegating coding, repo inspection, refactoring, bugfixing, lightweight code review, or quick automation to the Pi CLI instead of heavier coding agents.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - Coding-Agent
    - Pi
    - Lightweight
    - Automation
    - Refactoring
    - Code-Review
    related_skills:
    - claude-code
    - opencode
    - hermes
    category: autonomous-ai-agents
---

# Pi CLI — Lightweight Coding Agent

## Overview

Pi is a lightweight AI coding assistant CLI with read, bash, edit, and write tools. Use it when the task benefits from a fast external coding worker but does not need the heavier Claude Code or OpenCode workflow.

Verified on Galih's machine: `pi 0.72.1` is installed at `/home/galyarder/.nvm/versions/node/v24.15.0/bin/pi` and smoke test output included `PI_SMOKE_OK`.

## When to Use

Use Pi for:

- quick repo inspection or file-aware answers
- small bugfixes, refactors, docs edits, config cleanup
- lightweight code review before committing
- fast one-shot automation from Hermes terminal
- extension-backed work when Pi packages are enabled

Prefer Claude Code/OpenCode instead when:

- task is large, multi-hour, or needs strong autonomous writing-plansning
- interactive review loop matters more than startup speed
- you need mature PR/worktree workflows
- destructive commands or production deploys are involved

## Prerequisites

Check before promising a Pi workflow:

```bash
command -v pi
pi --version
pi list
```

Useful installed packages seen on this machine:

- `pi-subagents`
- `pi-prompt-template-model`
- `@writing-plansnotator/pi-extension`
- `pi-resource-center`
- `@eko24ive/pi-ask`
- `pi-mcp-adapter`
- `pi-intercom`

## Core Commands

### One-shot mode, preferred

```bash
pi -p --no-session "inspect this repo and summarize the architecture"
```

Use from Hermes:

```python
terminal(command="pi -p --no-session 'Respond with exactly: PI_SMOKE_OK'", workdir="/path/to/project", timeout=120)
```

### Safer read-only review

```bash
pi -p --no-session --tools read,bash "review the current git diff for bugs; do not edit files"
```

### Allow edits for small tasks

```bash
pi -p --no-session --tools read,bash,edit,write "fix the failing unit test with the smallest safe change, then run the relevant test"
```

### Attach context files

Pi accepts `@files` in the initial message:

```bash
pi -p --no-session @package.json @src/index.ts "explain the dependency and entrypoint structure"
```

### Choose provider/model

```bash
pi -p --no-session --provider GalyarderRoute --model openrouter/qwen/qwen3-coder-flash "make a small refactor"
```

Model can also include thinking suffix when supported:

```bash
pi -p --no-session --model openrouter/qwen/qwen3-coder:high "debug this failure"
```

### List models

```bash
pi --list-models coder
pi --list-models qwen
```

## Interactive Sessions

For iterative work, run Pi with a PTY in a background Hermes process:

```python
terminal(command="pi", workdir="/path/to/project", background=True, pty=True)
process(action="submit", session_id="<id>", data="inspect the failing tests and propose the smallest fix")
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>", limit=200)
process(action="write", session_id="<id>", data="\x03")
```

Use interactive mode only when follow-up turns are genuinely needed. Otherwise use `pi -p`.

## Sessions and Speed

- `--no-session`: fastest/cleanest for ephemeral automation.
- `--continue` / `-c`: continue previous session.
- `--resume` / `-r`: select a saved session to resume.
- `--session <path|id>`: use a specific session.
- `--session-dir <dir>`: isolate sessions per project.
- `--offline`: disables startup network operations when available.

Default recommendation:

```bash
pi -p --no-session --no-context-files "small bounded task"
```

If project instructions exist, allow Pi to load them only when they are relevant to the task.

## Tool Scoping

Pi supports tool control:

- `--no-tools` / `-nt`: disable all tools.
- `--no-builtin-tools` / `-nbt`: disable built-in tools but keep extensions.
- `--tools read,bash,edit,write`: enable only listed tools.

Use least privilege:

- inspection: `--tools read,bash`
- review: `--tools read,bash`
- small edits: `--tools read,bash,edit,write`
- pure answer: `--no-tools`

## Recommended Hermes Workflow

1. Set `workdir` to the repo root.
2. Run `git status --short` yourself before delegation.
3. Use `pi -p --no-session` for the task.
4. Verify the result yourself: inspect `git diff`, run tests/linters, read touched files.
5. Never tell Galih it is done until verification passes.

Example:

```python
terminal(command="git status --short", workdir="/repo", timeout=30)
terminal(command="pi -p --no-session --tools read,bash,edit,write 'fix the import error with minimal changes and run the relevant test'", workdir="/repo", timeout=300)
terminal(command="git diff --stat && git diff --check", workdir="/repo", timeout=60)
terminal(command="npm test -- --runInBand", workdir="/repo", timeout=300)
```

## Extension Management

```bash
pi list
pi install npm:<package>
pi remove npm:<package>
pi update
pi update pi
pi update --extensions
pi config
```

Use `-l` / `--local` to install/remove packages in project-local `.pi/settings.json`.

## Common Pitfalls

1. **Do not assume Pi exists.** Check `command -v pi && pi --version`.
2. **Do not let Pi edit blindly.** Scope tools and verify diffs yourself.
3. **Do not use one shared repo for parallel editing agents.** Use worktrees or separate copies.
4. **Do not expose secrets in prompts.** Redact `.env`, tokens, credentials, cookies.
5. **Do not confuse Pi extensions with Hermes native tools.** Pi runs as an external CLI; Hermes still verifies outputs independently.
6. **Model/provider names are installation-specific.** Use `pi --list-models <search>` before hardcoding a model.
7. **Interactive mode needs PTY.** Use `background=true, pty=true`; prefer print mode for automation.
8. **`--system-prompt` replaces the default prompt.** Prefer `--append-system-prompt` unless intentionally replacing behavior.

## Verification Checklist

- [ ] `pi --version` works.
- [ ] For smoke test, output contains exactly `PI_SMOKE_OK`.
- [ ] Workdir is correct repo root.
- [ ] Tool scope matches task risk.
- [ ] `git diff` shows only intended changes.
- [ ] Relevant tests/lints pass or failures are reported plainly.
- [ ] Background/interactive sessions are stopped when no longer needed.
