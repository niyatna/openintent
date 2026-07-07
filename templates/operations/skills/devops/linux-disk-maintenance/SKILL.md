---
author: Galyarder Labs
description: Use when auditing Linux user file directories, cleaning package manager
  or language tool caches, reclaiming disk storage, or checking root mounts.
license: MIT
metadata:
  hermes:
    category: devops
    related_skills:
    - obsidian
    - docker-management
    - verification-before-completion
    tags:
    - linux
    - disk
    - cleanup
    - cache
    - devops
    - maintenance
name: linux-disk-maintenance
version: 1.0.0
---

# Linux Disk Maintenance

Use this skill for Linux/CachyOS laptop or server disk audits and cleanup writing-plansning. Default posture is **read-only audit first**, then explicit cleanup only after user confirms scope.

## Core rule

Never treat cache cleanup as one generic `.cache` deletion. Modern dev machines accumulate disk in package caches, language tool stores, profile-local homes, project build outputs, browser/app profiles, container images, flatpaks, and agent runtime backups. Classify before cleaning.

If Galih says **read-only**, do not run deletion, prune, package-removal, `rm`, `trash-empty`, `docker image prune`, `npm cache clean`, `pnpm store prune`, `pip cache purge`, or commands that prompt for cleanup. Inspect and report only.

## Galyarder Obsidian runbook lookup

When Galih asks to "baca di Obsidian" for laptop cleanup, load the `obsidian` skill and read the maintenance notes before advising.

Known notes under `/home/galyarder/Documents/Obsidian Vault/galyarder/`:

- `device-maintenance/2026-04-08-device-maintenance-checklist.md`
- `device-maintenance/2026-04-08-home-cleanup-summary.md`

See `references/device-maintenance-lookup.md` for the lookup and audit pattern.

## Read-only audit sequence

Use the terminal for live system state. Prefer bounded `du`/`df` commands and avoid destructive flags.

```bash
df -h / /home /tmp /var/tmp 2>/dev/null || true
(du -xhd1 /home/galyarder 2>/dev/null || true) | sort -h | tail -40
(du -xhd1 /home/galyarder/.config 2>/dev/null || true) | sort -h | tail -40
(du -xhd1 /home/galyarder/.local 2>/dev/null || true) | sort -h | tail -40
(du -xhd1 /home/galyarder/.local/share 2>/dev/null || true) | sort -h | tail -50
(du -xhd1 /home/galyarder/.cache 2>/dev/null || true) | sort -h | tail -50
(du -xhd1 /tmp 2>/dev/null || true) | sort -h | tail -50
(du -xhd1 /var/tmp 2>/dev/null || true) | sort -h | tail -50
```

Check system/package caches:

```bash
(du -sh /var/cache/pacman/pkg /home/galyarder/.cache/paru /home/galyarder/.cache/yay 2>/dev/null || true)
paccache -dk1 2>/dev/null || true
journalctl --disk-usage 2>/dev/null || true
pacman -Qdtq 2>/dev/null | sed -n '1,80p'
flatpak list --app --columns=application,origin,installation,size 2>/dev/null || true
flatpak uninstall --unused --dry-run 2>/dev/null || true
```

Check Docker read-only:

```bash
docker system df 2>/dev/null || true
docker system df -v 2>/dev/null || true
```

## Dual-home tool cache check

Hermes profile runs may rewrite `$HOME`, so language managers can report profile-home caches even when the user's OS-home caches are larger. Check both.

```bash
# OS home
HOME=/home/galyarder npm config get cache 2>/dev/null || true
HOME=/home/galyarder pnpm store path 2>/dev/null || true
HOME=/home/galyarder python -m pip cache info 2>/dev/null || true
HOME=/home/galyarder uv cache dir 2>/dev/null || true
HOME=/home/galyarder go env GOPATH GOCACHE GOMODCACHE 2>/dev/null || true

# Current/profile home
npm config get cache 2>/dev/null || true
pnpm store path 2>/dev/null || true
python -m pip cache info 2>/dev/null || true
uv cache dir 2>/dev/null || true
go env GOPATH GOCACHE GOMODCACHE 2>/dev/null || true
```

Also size common paths directly:

```bash
for p in \
  /home/galyarder/.npm /home/galyarder/.bun /home/galyarder/.cache/pip \
  /home/galyarder/.cache/uv /home/galyarder/.cache/go-build \
  /home/galyarder/.local/share/pnpm /home/galyarder/.local/share/pipx \
  /home/galyarder/.cargo/registry /home/galyarder/.cargo/git \
  /home/galyarder/.nvm /home/galyarder/go \
  /home/galyarder/.hermes/profiles/galyarder/home/.npm \
  /home/galyarder/.hermes/profiles/galyarder/home/.bun \
  /home/galyarder/.hermes/profiles/galyarder/home/.cache/uv \
  /home/galyarder/.hermes/profiles/galyarder/home/.cache/pip \
  /home/galyarder/.hermes/profiles/galyarder/home/.cache/go-build \
  /home/galyarder/.hermes/profiles/galyarder/home/go; do
  [ -e "$p" ] && du -sh "$p" 2>/dev/null || true
done
```

## Project build artifact audit

For project roots, aggregate build outputs separately from source repos. Do not blindly delete `node_modules` or `.venv`; report candidates and ask before removal.

Useful artifact names:

- JS/web: `node_modules`, `.next`, `.nuxt`, `.turbo`, `.vercel`, `.vite`, `.parcel-cache`, `dist`, `build`, `playwright-pro`.
- Python: `.venv`, `venv`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `.tox`, `__pycache__`.
- Rust/Go/Java: `target`, `.gradle`, Gradle/Maven caches.

Report top offenders by project path and size.

## Active runtime guardrails

Before recommending deletion of app/profile/runtime data, check whether related processes/services are active. Examples:

```bash
systemctl --user is-active hermes-gateway.service hermes-gateway-galyarder.service camofox-browser-galyarder.service 2>/dev/null || true
pgrep -af 'camofox|camoufox|chrome|brave|zed|waydroid|docker|dockerd|containerd|hermes|gateway|discord|Code|claude|gemini' | sed -n '1,80p' || true
```

Manual-review-only or active-sensitive paths include:

- browser profiles under `.config/BraveSoftware`, `.mozilla`, Chrome/Chromium profile dirs;
- editor/app state under `.config/Code`, `.local/share/zed`, `.var/app/*`;
- Waydroid data under `.local/share/waydroid`;
- Hermes runtime dirs, venvs, sessions, private state, profile homes, Camofox/Playwright caches;
- AI/dev tool history under `.claude`, `.gemini`, `.codex`, `.opencode`;
- backup directories and DB backups unless retention is known.

## Reporting format

Keep the final response concise and operational. Separate:

1. What the Obsidian runbook says.
2. Current live disk state.
3. Safe cache candidates.
4. Manual-review-only app/profile/runtime data.
5. Active-runtime paths to avoid right now.
6. Biggest project build artifacts.
7. System/package/container findings.
8. Priority cleanup order if the user later authorizes execution.

Do not overstate. If a path is app/profile state rather than cache, label it as app/profile state. If the user calls something "temp mail", verify mail paths and `/tmp` separately before agreeing.

## Verification after cleanup

After any approved cleanup, rerun the same `df`/`du`/tool-specific disk checks and report before/after. For Docker, compare `docker system df`. For package caches, compare `paccache` dry-run and direct `du` on cache dirs. For project artifact deletion, compare per-project `du`.
