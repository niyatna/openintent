# Paseo CLI integration — 2026-05-21

## Why this reference exists

Galih asked for the existing Paseo skill set in both Keiya/default and Galyarder to be checked, safety-reviewed, and upgraded into a main operational skill like `claude-code` / `codex`.

This is session-specific evidence and caveat detail. The class-level rules belong in `SKILL.md`; this file preserves the observed integration facts without bloating the main skill.

## Observed skill inventory

Both profile skill trees had the same Paseo set:

- `paseo` — main reference/orchestration skill.
- `paseo-advisor` — single outside second opinion.
- `paseo-committee` — two-agent adversarial/root-cause writing-plansning.
- `paseo-epic` — heavy end-to-end orchestration.
- `paseo-handoff` — hand current task to another agent.
- `paseo-loop` — bounded worker/verifier loops.
- `paseo-orchestrate` — deprecated alias redirecting to `paseo-epic`.
- `release-beta` and `release-stable` — only for releasing Paseo itself.

The existing set was structurally useful, but the main `paseo` skill was too reference-like and lacked Hermes/Galih safety gates, PATH caveats, command examples, and verification posture.

## Observed local CLI/runtime facts

At the time of the integration pass:

- CLI package: `@getpaseo/cli`.
- CLI version: `0.1.78`.
- Real command: lowercase `paseo`, not uppercase `Paseo`.
- Binary path: `/home/galyarder/.nvm/versions/node/v24.15.0/bin/paseo`.
- Daemon home: `/home/galyarder/.paseo`.
- Daemon log: `/home/galyarder/.paseo/daemon.log`.
- Daemon listen address: `127.0.0.1:6767`.
- Live providers observed: Claude Code, Codex, OpenCode available; Copilot and Pi not available in that probe.
- Keiya/default and Galyarder shared the same OS-home daemon by default, so profile labels are required on new agents.

Do not treat these as eternal facts. Re-check live before running agents, but preserve the PATH/OS-home pattern as the likely local setup.

## Verification lessons

Useful checks from the session:

- Runtime skill loadability was proven with `skill_view("paseo")`.
- Hermes installed-skill visibility was proven with `hermes --profile <profile> skills list` showing `paseo` enabled.
- `hermes skills inspect paseo` did **not** prove local runtime skill loadability in this setup; it behaved like a hub/registry inspect path and returned `No skill named 'paseo' found` even while `skills list` showed local `paseo` enabled.
- Therefore, for local personal skills, prefer: frontmatter parse + `skill_view(<name>)` + `hermes skills list`; do not rely on `hermes skills inspect` alone.

## Safety posture encoded into SKILL.md

The main `paseo` skill was upgraded to include:

- read-only safe commands;
- explicit confirmation gates for daemon restart/stop, delete, stop-all, worktree archive, and risky permission allows;
- detached run patterns for long tasks;
- worktree isolation pattern for risky or parallel implementation;
- bounded loops and schedules only;
- permission request inspection before allowing;
- post-agent independent verification before completion claims;
- profile labels: `profile=galyarder` / `profile=keiya` plus `source=hermes`.

## Reusable pattern

For future agent-runner integrations, do this shape:

1. Inspect current class skill and companion skills.
2. Probe CLI read-only first: `--version`, `--help`, `status`, provider list, active agents.
3. Patch the class-level main skill, not a one-session skill.
4. Put exact observed path/version/provider facts in a `references/` file.
5. Add a one-line pointer from `SKILL.md` to the reference.
6. Verify runtime loadability through the actual skill loader, not only registry/hub inspection.
