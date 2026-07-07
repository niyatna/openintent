# Device maintenance lookup and audit reference

Use this reference when Galih asks to read Obsidian for laptop cleanup, cache cleanup, or disk-maintenance routines.

## Known note locations

Under the Galyarder vault path `/home/galyarder/Documents/Obsidian Vault/galyarder/`:

- `device-maintenance/2026-04-08-device-maintenance-checklist.md` — class-level maintenance checklist.
- `device-maintenance/2026-04-08-home-cleanup-summary.md` — prior home cleanup results, kept/removed paths, and follow-up candidates.

## Lookup sequence

1. Search filenames under the vault for `*cleanup*` and `*maintenance*`.
2. Search note contents for operational keywords: `cleanup`, `cache`, `pacman`, `paru`, `npm`, `pip`, `bun`, `go`, `docker`, `temp`, `package`, `orphan`.
3. Read the canonical notes before giving cleanup advice.
4. If Galih asks for read-only, only inspect and report. Do not run deletion, prune, package-removal, or cleanup commands.

## What the Obsidian checklist expects

Routine cleanup categories in the note:

- Package manager cleanup: pacman cache, paru cache/build artifacts, orphan package review.
- User cache cleanup: `.cache`, `.npm`, `.bun`, Trash, `.local/share/uv`, `.local/share/pipx`.
- Browser/app data review: Brave, Mozilla, BrowserOS, Code, and stale app profiles.
- AI/dev tool data review: Claude, Gemini, Copilot, Continue, Codex, Opencode.
- Runtime/toolchain cleanup: `~/go`, old `.nvm` Node versions, cargo registry/git cache, JDKs, dotnet.
- Rarely used app audit: Applications, `.local/opt`, Zed preview, Anki, Telegram, Spicetify, Wine, Flatpak `.var`.
- Backup/residue review: old backup folders, strange `...` folder, and compatibility stubs.

## Session-derived audit lesson

A basic cleanup can leave disk usage high because the dominant space may be outside package cache and Trash. Check:

- OS-home caches and profile-home caches separately.
- Project build outputs like `.next`, `node_modules`, `.turbo`, `.venv`.
- Browser/app profile state that is not safe to delete while active.
- Agent/runtime backups and DB backups that need retention review.
- Docker images and Flatpak installations.
- `/tmp` separately from mail spool; do not call `/tmp` usage "temp mail" without evidence.

## Reporting buckets

Use these buckets in the answer:

1. Safe cache candidates.
2. Manual-review-only app/profile data.
3. Active-runtime paths to avoid right now.
4. Project build artifacts.
5. System/package/container findings.
6. Non-cache user-choice storage.
7. Priority cleanup order if execution is later approved.
