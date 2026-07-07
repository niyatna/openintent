# GBrain Profile Dedupe — 2026-05-12

Galih chose to stop maintaining a separate profile-local GBrain under the Galyarder Hermes profile and use the healthy OS-home GBrain as the single canonical instance.

## Canonical instance

Use:

- tool repo: `/home/galyarder/gbrain`
- data repo: `/home/galyarder/brain`
- DB: `/home/galyarder/.gbrain/brain.pglite`
- CLI: `/home/galyarder/.bun/bin/gbrain`

Do **not** recreate a separate profile-local instance at:

- `/home/galyarder/.hermes/profiles/galyarder/home/gbrain`
- `/home/galyarder/.hermes/profiles/galyarder/home/brain`
- `/home/galyarder/.hermes/profiles/galyarder/home/.gbrain`

unless Galih explicitly asks for isolated profile-local GBrain again.

## What was changed

The broken profile-local duplicate was backed up then archived:

- backup: `/home/galyarder/.hermes/backups/gbrain-profile-dedupe-20260512-204554`
- archive: `/home/galyarder/.hermes/profiles/galyarder/archives/gbrain-profile-duplicate-20260512-204633`

A wrapper was installed at:

- `/home/galyarder/.hermes/profiles/galyarder/home/.bun/bin/gbrain`
- `/home/galyarder/.hermes/profiles/galyarder/home/.bun/bin/gbrain-main`

The wrapper forces:

```bash
export HOME=/home/galyarder
export PATH="/home/galyarder/.bun/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
exec /home/galyarder/.bun/bin/gbrain "$@"
```

This means `gbrain` from the Galyarder profile still resolves in profile PATH, but executes against the canonical OS-home repo/data/DB.

## Verification evidence

From the Galyarder profile shell after dedupe:

- `command -v gbrain` → `/home/galyarder/.hermes/profiles/galyarder/home/.bun/bin/gbrain` wrapper
- active profile-local `gbrain`, `brain`, `.gbrain` paths: absent
- `gbrain --version` → `gbrain 0.26.0`
- `gbrain stats` → 21 pages, 42 chunks, 42 embedded, 10 links, 18 tags, 22 timeline
- `gbrain doctor --json` → status `warnings`, health score `80`, embeddings OK with 100% playwright-pro
- `gbrain skillpack-check` → healthy true, migrations up to date

Detailed verification artifact for that run:

- `/tmp/gbrain_profile_dedupe_verify.md`
- `/tmp/gbrain_profile_dedupe_verify.json`

## Operating rule

When using GBrain from Hermes/Galyarder, trust the canonical OS-home instance. If future commands appear to use profile-local paths, fix PATH/wrapper first; do not debug the archived profile-local PGLite DB as if it were active.
