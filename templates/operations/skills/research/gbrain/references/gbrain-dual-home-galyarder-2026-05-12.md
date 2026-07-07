# GBrain dual-home audit — Galyarder Hermes profile — 2026-05-12

Use this when Galih asks whether GBrain is installed/healthy or how it differs from gstack on the Galyarder machine.

## Core distinction

- `gstack`: software-factory workflow suite — QA, review, ship/deploy, canary, browser testing, design/CEO/eng reviews.
- `gbrain`: DB-backed personal/project brain — imports markdown, stores pages/chunks/embeddings, supports search/query, minions, skillpack checks, and brain ops.

Do **not** answer GBrain status from the presence of a Hermes skill. Verify the actual CLI, repo, data path, DB path, and doctor/stats output.

## Dual-home pitfall

The Galyarder Hermes profile can run with synthetic home:

```text
profile HOME = /home/galyarder/.hermes/profiles/galyarder/home
OS HOME      = /home/galyarder
```

Therefore `~/gbrain`, `~/brain`, `~/.gbrain/config.json`, and `command -v gbrain` can point to the profile-local install instead of the OS-home install. This caused a real status discrepancy in the 2026-05-12 audit.

## Live audited state from 2026-05-12

### Canonical / healthy OS-home install

```text
repo: /home/galyarder/gbrain
data: /home/galyarder/brain
DB:   /home/galyarder/.gbrain/brain.pglite
CLI:  /home/galyarder/.bun/bin/gbrain
version: gbrain 0.26.0
```

Observed health:

- `gbrain stats`: 21 pages, 42 chunks, 42 embedded, 10 links, 18 tags, 22 timeline entries.
- `gbrain doctor --json`: DB connected, schema version latest, embeddings 100% playwright-pro / 0 missing.
- `gbrain skillpack-check`: healthy; migrations all up to date.
- Repo had local modified embedding/router patch files (`src/cli.ts`, `src/core/embedding.ts`, tests), so check git status before overwriting or upgrading.
- Doctor from repo cwd showed `routing_miss` warnings in bundled GBrain skills; these were not fatal because DB, embeddings, migrations, and skill conformance were OK.

### Profile-local / unhealthy install

```text
repo: /home/galyarder/.hermes/profiles/galyarder/home/gbrain
data: /home/galyarder/.hermes/profiles/galyarder/home/brain
DB:   /home/galyarder/.hermes/profiles/galyarder/home/.gbrain/brain.pglite
CLI:  /home/galyarder/.hermes/profiles/galyarder/home/.bun/bin/gbrain
version: gbrain 0.26.0
```

Observed issue:

- `gbrain stats` failed with `PGLite failed to initialize its WASM runtime`.
- `gbrain skillpack-check` reported unhealthy because `apply-migrations --list` failed.
- Treat this as non-canonical until intentionally repaired.

## Verification commands

Run both homes explicitly instead of relying on shell defaults:

```bash
for home in /home/galyarder /home/galyarder/.hermes/profiles/galyarder/home; do
  echo "=== HOME=$home ==="
  HERMES_HOME=$([ "$home" = "/home/galyarder" ] && echo /home/galyarder/.hermes || echo /home/galyarder/.hermes/profiles/galyarder)
  PATH="$home/.bun/bin:/home/galyarder/.bun/bin:/usr/local/bin:/usr/bin:/bin"
  HOME="$home" HERMES_HOME="$HERMES_HOME" PATH="$PATH" bash -lc '
    echo "gbrain=$(command -v gbrain || true)"
    gbrain --version || true
    cat "$HOME/.gbrain/config.json" 2>/dev/null || true
    gbrain stats || true
    gbrain doctor --json 2>&1 | head -c 4000 || true
    gbrain skillpack-check 2>&1 | head -c 4000 || true
  '
done
```

For resolver/skillpack checks, run from the repo cwd because `gbrain doctor` discovers bundled skills by walking from the current directory:

```bash
cd /home/galyarder/gbrain
gbrain doctor --fast --json
gbrain check-resolvable
```

## Recommended operating policy

- Prefer the OS-home canonical install (`/home/galyarder/gbrain` + `/home/galyarder/brain`) unless Galih explicitly wants isolated profile-local GBrain.
- Do not run destructive DB repair, migrations, or cleanup on the profile-local DB just because Galyarder profile commands fail; first prove which home is active.
- If Hermes/Galyarder needs reliable access, create a wrapper such as `gbrain-main` that sets `HOME=/home/galyarder` and prepends `/home/galyarder/.bun/bin` before invoking `gbrain`.
- Do not install the GBrain skillpack into Hermes skills blindly; GBrain has its own skill ecosystem and resolver.
- Avoid `gbrain autopilot --install` / systemd for local PGLite unless explicitly approved; prefer Hermes cron for cadence to avoid lock contention.

## Final answer pattern for Galih

Short version:

> GBrain beda dari gstack. Gstack = software factory workflow. GBrain = DB-backed brain. Canonical GBrain yang sehat ada di `/home/galyarder/gbrain`; profile-local GBrain ada tapi PGLite/skillpack check-nya broken, jadi jangan dijadikan source of truth dulu.
