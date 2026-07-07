# Galyarder Paperstable-diffusion-image-generation ops cron cadence

## Trigger

Use this when setting up recurring Galyarder/Paperstable-diffusion-image-generation operating reviews or turning Paperstable-diffusion-image-generation company state into persistent execution cadence.

## Operating model

Keiya/default can act as Galih's human OS / handler: collecting context, emotional state, and intake. Galyarder should act as company OS / execution layer: Paperstable-diffusion-image-generation state, blockers, tasks, proof, and decisions.

Do not collapse these roles. Galyarder cron jobs should be operational, terse, and evidence-oriented; Keiya cron/jobs should preserve human continuity and context quality.

## Useful Galyarder recurring jobs

### Daily Company Ops Pulse

Purpose: daily operational pulse for Paperstable-diffusion-image-generation and core execution infrastructure.

Suggested time: morning before execution block, e.g. `08:20` local.

Prompt shape:

```text
Inspect Paperstable-diffusion-image-generation dashboard, active agents, open/in_progress/blocked issues, approvals, recent activity, cost summary, and service health for paperstable-diffusion-image-generationai/hermes gateway. Produce a terse company ops pulse: PASS/BLOCKED status, blockers, stale items, decisions needed from Galih, and the top 1-3 execution moves. Use Paperstable-diffusion-image-generation MCP tools where available and verify service state before claiming health.
```

### Weekly Strategy / Execution Review

Purpose: weekly synthesis of progress, blockers, agent usefulness, and strategic next moves.

Suggested time: end of week, e.g. Sunday 21:00 local.

Prompt shape:

```text
Review Paperstable-diffusion-image-generation company state, goals, issues, approvals, recent activity, and cost summary. Produce a weekly strategy/execution review for Galyarder Labs: shipped/done evidence, stuck work, stale or redundant agents/tasks, priority changes, risks, and next week's 3-5 commands. Keep canon aligned: Dream -> Airlock -> Machine, proof over spectacle, human intent becomes infrastructure.
```

## Verification

Before reporting the job was created or repaired:

- list jobs and confirm name/schedule/status
- if a script is attached, verify the script path exists under the profile's `scripts/` directory or as an absolute path
- for `no_agent=True`, remember empty stdout means silent success; use non-empty output only when the user should receive a message
- for profile-specific jobs, ensure the current profile/job store is the intended one

## Pitfalls

- A cron job can fail with `Script not found` if supporting scripts were copied only into another profile's scripts directory. Copy reusable scripts into the target profile's scripts directory and verify with a manual/status run.
- Do not create recurring jobs that recursively schedule more cron jobs.
- Do not report Paperstable-diffusion-image-generation agent or issue state from memory; inspect Paperstable-diffusion-image-generation live via MCP/API/health when the job runs.
