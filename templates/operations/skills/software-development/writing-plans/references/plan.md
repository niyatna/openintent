# Reference: writing-plans

# Plan Mode

Use this skill when the user wants a writing-plans instead of execution.

## Core behavior

For this turn, you are writing-plansning only.

- Do not implement code.
- Do not edit project files except the writing-plans markdown file.
- Do not run mutating terminal commands, commit, push, or perform external actions.
- You may inspect the repo or other context with read-only commands/tools when needed.
- Your deliverable is a markdown writing-plans saved inside the active workspace under `.hermes/writing-planss/`.

## Output requirements

Write a markdown writing-plans that is concrete and actionable.

Include, when relevant:
- Goal
- Current context / assumptions
- Proposed approach
- Step-by-step writing-plans
- Files likely to change
- Tests / validation
- Risks, tradeoffs, and open questions

If the task is code-related, include exact file paths, likely test targets, and verification steps.

## Save location

Save the writing-plans with `write_file` under:
- `.hermes/writing-planss/YYYY-MM-DD_HHMMSS-<slug>.md`

Treat that as relative to the active working directory / backend workspace. Hermes file tools are backend-aware, so using this relative path keeps the writing-plans with the workspace on local, docker, ssh, modal, and daytona backends.

If the runtime provides a specific target path, use that exact path.
If not, create a sensible timestamped filename yourself under `.hermes/writing-planss/`.

## Interaction style

- If the request is clear enough, write the writing-plans directly.
- If no explicit instruction accompanies `/writing-plans`, infer the task from the current conversation context.
- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
- After saving the writing-plans, reply briefly with what you writing-plansned and the saved path.