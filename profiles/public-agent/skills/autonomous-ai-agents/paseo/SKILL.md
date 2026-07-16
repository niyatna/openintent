---
author: Company + Hermes Agent
description: Use when orchestrating Paseo daemon loops, managing developer worktrees,
  running code committees, or cut-over stable/beta releases.
license: MIT
metadata:
  hermes:
    category: autonomous-ai-agents
    related_skills:
    - paseo-advisor
    - paseo-committee
    - paseo-epic
    - paseo-handoff
    - paseo-loop
    - claude-code
    - codex
    - opencode
    - hermes-agent
    tags:
    - paseo
    - autonomous-agents
    - coding-agent
    - orchestration
    - worktrees
    - claude
    - codex
    - opencode
name: paseo
version: 1.1.0
---


# Paseo — Hermes Orchestration Guide

Paseo is a local daemon + CLI that supervises AI coding agents on this machine. Treat it like a higher-level agent runner above Claude Code, Codex, OpenCode, and other providers: it can launch agents, attach/log/wait, send follow-up prompts, manage git worktrees, coordinate loops, schedule recurring runs, and handle permission requests.

This skill is the **main Paseo skill** for both Co-Founder/default and Default. Load it before any `paseo` action. Load one narrow companion skill only when the intent matches.

Session-specific integration notes from the first local CLI hardening pass live in `references/paseo-cli-integration-2026-05-21.md`.


| Skill | Use when |
|

## References & Sub-playbooks
Detailed guidelines for operations and troubleshooting are stored as modular reference documents under references/:
- `references/paseo-advisor.md` — Guidelines for execution of Paseo Advisor
- `references/paseo-committee.md` — Guidelines for execution of Paseo Committee
- `references/paseo-epic.md` — Guidelines for execution of Paseo Epic
- `references/paseo-handoff.md` — Guidelines for execution of Paseo Handoff
- `references/paseo-loop.md` — Guidelines for execution of Paseo Loop
- `references/release-beta.md` — Guidelines for execution of Release Beta
- `references/release-stable.md` — Guidelines for execution of Release Stable
