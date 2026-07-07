---
author: Galyarder Labs
description: Use when executing Garry Tan gstack software-factory tools.
license: MIT
metadata:
  hermes:
    category: software-development
    homepage: https://github.com/garrytan/gstack
    related_skills:
    - claude-code
    - autonomous-ai-agents
    - gstack
    - office-hours
    - autowriting-plans
    - review
    - qa
    - ship
    - browse
    tags:
    - gstack
    - claude-code
    - ai-agents
    - qa
    - writing-plansning
    - review
    - browser
    - release
name: using-gstack
version: 1.0.0
---


# Using gstack

## Overview

`gstack` is Garry Tan's opinionated AI software factory: a set of role-based workflow skills plus browser/design/release utilities. It is primarily built for Claude Code slash commands, but this galyarder profile also has Hermes-format gstack skills generated and linked.

Use gstack for structured software work where a blank prompt is too weak: product interrogation, reviewed writing-plansning, architecture critique, browser QA, code review, security audit, release, and post-deploy checks.

## Installed State In This Profile

Canonical repo:

```bash
GSTACK_REPO="$HOME/gstack"
# /home/galyarder/.hermes/profiles/galyarder/home/gstack
```

Installed version:

```bash
cat "$HOME/gstack/VERSION"          # 1.26.0.0
git -C "$HOME/gstack" rev-parse --short HEAD  # bf65487 at install time
```

Claude Code install/link created by upstream setup:

```bash
$HOME/.claude/skills/gstack -> $HOME/gstack
$HOME/.claude/skills/<skill>/SKILL.md -> $HOME/gstack/<skill>/SKILL.md
```

Hermes generated skills are linked into this profile:

```bash
$HERMES_HOME/skills/gstack-workflow/<skill> -> $HOME/gstack/.hermes/skills/gstack-<skill>
```

`hermes skills list` shows the gstack workflow skills as enabled under category `gstack-workflow`, with user-facing names such as:

- `office-hours`
- `autowriting-plans`
- `writing-plans-ceo-review`
- `writing-plans-eng-review`
- `review`
- `qa`
- `qa-only`
- `ship`
- `land-and-deploy`
- `browse`
- `cso`
- `investigate`
- `design-review`
- `design-shotgun`
- `make-pdf`
- `gstack-upgrade`

Current session caveat: newly installed skills may not be visible to `skill_view` until a fresh session. If `skill_view(name="qa")` does not resolve now, use the file directly or start a new session.

## First Checks

Before using gstack seriously:

```bash
cd "$HOME/gstack"
git status --short
cat VERSION
bun --version
node --version
claude --version || true
./browse/dist/browse --help | sed -n '1,40p'
./browse/dist/browse status
bun run gen:skill-docs --host hermes --dry-run
```

Expected installed smoke results from setup:

- `browse/dist/browse` executable exists.
- `design/dist/design` executable exists.
- `make-pdf/dist/pdf` executable exists.
- Playwright Chromium and headless shell downloaded under `$HOME/.cache/ms-playwright`.
- `bun run gen:skill-docs --host hermes --dry-run` returns fresh generated files.
- `./browse/dist/browse status` returns `Status: healthy`.

## Installation / Upgrade

Install/update in the profile workspace:

```bash
repo="$HOME/gstack"
if [ -d "$repo/.git" ]; then
  git -C "$repo" pull --ff-only
else
  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$repo"
fi
cd "$repo"
./setup --no-prefix --no-team
```

Then link generated Hermes skills into this profile:

```bash
mkdir -p "$HERMES_HOME/skills/gstack-workflow"
python3 - <<'PY'
from pathlib import Path
import os, shutil
home = Path(os.environ['HOME'])
hermes_home = Path(os.environ['HERMES_HOME'])
src = home/'gstack'/'.hermes'/'skills'
dst_root = hermes_home/'skills'/'gstack-workflow'
dst_root.mkdir(parents=True, exist_ok=True)
for skill in sorted(src.iterdir()):
    if not skill.is_dir() or not (skill/'SKILL.md').exists():
        continue
    dst = dst_root/skill.name
    if dst.exists() or dst.is_symlink():
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        else:
            shutil.rmtree(dst)
    dst.symlink_to(skill, target_is_directory=True)
print('linked', len(list(dst_root.iterdir())), 'gstack skills')
PY
```

Verify:

```bash
hermes skills list | grep -i gstack | head -50
```

## Choosing The Right gstack Skill

Planning and product:

- `office-hours`: start with a product idea; reframes the real pain, asks forcing questions, writes design doc.
- `writing-plans-ceo-review`: strategic/scope review; find the stronger product or cut weak scope.
- `writing-plans-eng-review`: architecture, data flow, edge cases, test matrix.
- `writing-plans-design-review`: design critique before implementation.
- `writing-plans-devex-review`: developer experience writing-plansning.
- `autowriting-plans`: runs the review gauntlet automatically.

Implementation review and debugging:

- `review`: pre-landing staff-engineer review; bugs that pass CI but break production.
- `investigate`: root-cause debugging; no fixes before understanding.
- `cso`: OWASP + STRIDE security audit.
- `health`: code quality dashboard.

Browser, QA, design:

- `browse`: fast headless browser commands and screenshots.
- `qa`: real browser QA, bug finding, fixes, and re-verification.
- `qa-only`: bug report only, no code changes.
- `design-review`: live visual audit and fix loop.
- `design-shotgun`: generate multiple design variants and comparison board.
- `design-html`: production-quality HTML/CSS from a mockup/brief.

Release:

- `ship`: tests, review, push, PR.
- `land-and-deploy`: merge, CI/deploy wait, production verification.
- `canary`: post-deploy monitoring.
- `document-release`: update docs after shipping.
- `setup-deploy`: one-time deploy platform detection.

Ops and memory:

- `context-save` / `context-restore`: save and resume working state.
- `learn`: manage gstack learnings.
- `retro`: weekly retro.
- `careful`, `freeze`, `guard`, `unfreeze`: safety/scoping guards.

## How To Use From Hermes

### Native Hermes skill route

On a fresh session, load the relevant generated skill:

```text
/skill office-hours
/skill review
/skill qa
```

Or via tool call if available:

```python
skill_view(name="office-hours")
skill_view(name="review")
skill_view(name="qa")
```

Then follow the loaded skill as executable workflow instructions, not passive reference. gstack skills include a preamble shell block; run it when practical because it sets `GSTACK_ROOT`, `GSTACK_BIN`, `GSTACK_BROWSE`, telemetry state, routing state, and GBrain context hooks.

### Claude Code route

For workflows that depend on Claude Code slash-command semantics, spawn Claude Code with gstack loaded. Prefer `claude -p` for one-shot tasks and tmux for interactive multi-turn sessions.

Example review:

```bash
cd /path/to/repo
claude -p "Load gstack. Run /review on the current branch. Report findings and fixes." --max-turns 20
```

Example writing-plansning:

```bash
cd /path/to/repo
claude -p "Load gstack. Run /office-hours, then /autowriting-plans. Save the reviewed writing-plans. Do not implement." --max-turns 25
```

Example QA:

```bash
cd /path/to/repo
claude -p "Load gstack. Run /qa https://staging.example.com. Find bugs, fix only confirmed issues, and re-verify." --max-turns 30
```

Use the `claude-code` skill for detailed orchestration flags, tmux handling, and permissions.

## Browser CLI Quick Reference

Routing note: for general browser choice, load `galyarder-browser-routing` first. Use gstack browse when the task is QA/dev/visual testing, not human media browsing or isolated multi-account auth.

Scope warning: this section is only for **gstack browse**. If the user asks about Hermes Agent's native/built-in browser, do not answer from gstack status or screenshots; load `hermes` and verify `agent-browser` instead. In the Galyarder profile, gstack browse was verified as Playwright Chromium headless shell (`$HOME/.cache/ms-playwright/chromium_headless_shell-1208/.../chrome-headless-shell`) while Hermes native browser may route through Camofox; keep that distinction explicit. If the question is which browser stack should handle a task, load `browser-routing` first because Galih's preferred default for human-facing browser work is Brave CDP, Browserbase is the normal cloud fallback, Camofox is the isolated lab, and gstack is QA/dev.

The browser binary is:

```bash
B="$HOME/gstack/browse/dist/browse"
```

Runtime attribution: gstack browse is the stack that uses Playwright Chromium/headless shell in this profile. Verify with `$B status`, a harmless `$B goto https://example.com`, and `ps` for `bun run .../browse/src/server.ts` plus `chrome-headless-shell` under `$HOME/.cache/ms-playwright`. For the observed proof and commands, see `references/gstack-browser-runtime.md`. For the broader keep/remove routing decision versus Hermes Camofox, Brave, BrowserOS, and Browserbase, see `references/gstack-vs-hermes-browser-routing.md`.

Common commands:

```bash
$B status
$B goto https://example.com
$B snapshot -a
$B text
$B click @e3
$B fill 'input[name=email]' 'user@example.com'
$B press Enter
$B screenshot /tmp/page.png
$B console --errors
$B network
$B stop
```

Use Hermes native browser tools for ordinary page inspection when they are enough. Use gstack `browse` when a gstack skill explicitly calls for `$B`, when you need its snapshot/diff/domain-skill semantics, or when following `/qa`/`/browse` workflows.

## Safety Rules

- Do not run `./setup --team` or `gstack-team-init required` inside a user's repo unless they explicitly ask for team mode and a committed repo policy. Team mode edits repo files and can add hooks/CLAUDE.md or AGENTS.md outlines.
- Do not execute destructive gstack workflow steps (`ship`, `land-and-deploy`, deletes, deploys, force pushes) without clear user authorization and target repo/branch confirmation.
- gstack's telemetry setting is currently `off`. Do not enable telemetry without the user's explicit consent.
- Generated gstack skills can be very large. Load only the specific relevant skill, not all of gstack.
- gstack skills were designed around Claude Code. In Hermes, map tool instructions carefully: Bash → terminal, Read → read_file, Grep/Glob → search_files, Agent → delegate_task, Write/Edit → write_file/patch.

## Troubleshooting

If the user asks whether gstack is "double" with Keiya/default, answer the path/routing question first. In this setup duplication is intentional only when default and Galyarder need isolated tool state; the failure mode is mixed wiring. Load `gstack-local` and use `references/galyarder-profile-isolation.md` for the path map, wrapper, skill mirroring, and cleanup commands.

If gstack skill files are not visible to Hermes:

```bash
hermes skills list | grep -i gstack
find "$HERMES_HOME/skills/gstack-workflow" -maxdepth 2 -name SKILL.md | head
```

If generated Hermes docs are stale:

```bash
cd "$HOME/gstack"
bun run gen:skill-docs --host hermes
bun run gen:skill-docs --host hermes --dry-run
```

If browser is unhealthy:

```bash
cd "$HOME/gstack"
./browse/dist/browse stop || true
./browse/dist/browse status
bunx playwright install chromium
```

If `GSTACK_ROOT` paths inside generated skills fail, remember the profile `$HOME` is `/home/galyarder/.hermes/profiles/galyarder/home`; the generated skills expect `$HOME/.hermes/skills/gstack` but the active Hermes runtime skills live under `$HERMES_HOME/skills`. This profile has a compatibility symlink:

```bash
$HERMES_HOME/skills/gstack -> $HOME/gstack/.hermes/skills/gstack
```

For commands run outside Hermes with only `$HOME` available, export:

```bash
export GSTACK_ROOT="$HOME/gstack/.hermes/skills/gstack"
export GSTACK_BIN="$HOME/gstack/bin"
export GSTACK_BROWSE="$HOME/gstack/browse/dist"
```

## Verification Checklist

Before claiming a gstack task is complete:

- [ ] Loaded the relevant specific gstack skill or used Claude Code with `Load gstack`.
- [ ] Verified repository path, branch, and scope before any write/release/deploy action.
- [ ] Ran the skill's preamble or equivalent environment setup when required.
- [ ] Used browser evidence/screenshots/logs for QA/design/browser claims.
- [ ] Verified generated files, PRs, deployments, or reports exist at the paths/URLs reported.
- [ ] Left telemetry/team mode off unless explicitly approved.
