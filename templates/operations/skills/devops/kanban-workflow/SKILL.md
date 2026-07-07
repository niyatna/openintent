---
name: kanban-workflow
description: Use when managing Kanban boards, routing tasks to specialist agents, decomposing objectives, or coordinating task lifecycles within a pipeline.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [devops, kanban, workflow, task-routing, orchestration]
    category: devops
---

# Kanban Board Management & Task Lifecycle (Kanban Workflow)

This class-level skill provides a comprehensive playbook for both **Kanban Orchestrators** (who decompose and route tasks) and **Kanban Workers** (who carry out tasks and report outcomes).

---

## 1. Kanban Orchestrator — Decomposition Playbook

Decompose, route, and summarize — that's the whole job of an orchestrator.

### When to use the board (vs. just doing the work)
Create Kanban tasks when any of these are true:
1. **Multiple specialists are needed.** Research + analysis + writing is three profiles.
2. **The work should survive a crash or restart.** Long-running, recurring, or important.
3. **The user might want to interject.** Human-in-the-loop at any step.
4. **Multiple subtasks can run in parallel.** Fan-out for speed.
5. **Review / iteration is expected.** A reviewer profile loops on drafter output.
6. **The audit trail matters.** Board rows persist in SQLite forever.

If *none* of those apply — it's a small one-shot reasoning task — use `delegate_task` instead or answer the user directly.

### The Anti-Temptation Rules
- **Do not execute the work yourself.**
- **For any concrete task, create a Kanban task and assign it.** Every single time.
- **If no specialist fits, ask the user which profile to create.** Do not default to doing it yourself under "close enough."

### Specialist Roster
- `researcher`: Reads sources, gathers facts, writes findings.
- `analyst`: Synthesizes, ranks, de-dupes. Consumes researcher outputs.
- `writer`: Drafts prose in the user's voice.
- `reviewer`: Reads output, leaves findings, gates approval.
- `backend-eng` / `frontend-eng`: Writes code.
- `ops`: Runs scripts, manages services, handles deployments.
- `pm`: Writes specs, acceptance criteria.

---

## 2. Kanban Worker — Pitfalls and Examples

Workers execute tasks assigned page by page, adhering to tenant boundaries and heartbeats.

### Workspace Handling
- `scratch`: Fresh temp directory. Read/write freely; it gets cleaned up on completion.
- `dir:<path>`: Shared persistent directory. Treat like persistent state.
- `worktree`: Git worktree at the resolved directory path. Commit work here.

### Tenant Isolation
If `$HERMES_TENANT` is set, prefix memory entries with the tenant identifier to prevent leakage across namespaces (e.g. `business-a: ...`).

### Heartsbeats, Block Reasons, and CLI Fallbacks
- Heartsbeats should name progress: `"epoch 12/50, loss 0.31"`.
- Block reasons should be short, distinct, and accompanied by detailed comments.
- CLI equivalents (`hermes kanban complete ...`) exist for operating from standard shell sessions. Use native python tools where available.

## References & Sub-playbooks
- `references/kanban-workflow.md` — Roster conventions and task decomposition guidelines
- `references/kanban-workflow.md` — Scenarios, pitfalls, and edge cases for Kanban execution agents
