# GBrain v0.26.0 local router notes — 2026-05-04

Session-specific detail for configuring GBrain embeddings through Owner's local OpenAI-compatible router.

## Verified environment

- GBrain repo: `~/.hermes/gbrain`
- Brain data path: `~/.hermes/brain`
- PGLite DB: `~/.hermes/.gbrain/brain.pglite`
- Router base URL: `http://localhost:20128/v1`
- Working embedding model: `nebius/Qwen/Qwen3-Embedding-8B`
- Requested dimensions: `1536`
- Key source: `OMNIROUTE_API_KEY` from the local Hermes environment
- Version: GBrain v0.26.0

## What worked

GBrain was installed with Bun and linked globally, then markdown pages were imported into PGLite. The upstream embedding code was patched minimally so its OpenAI client could read environment overrides for base URL, API key, model, and dimensions.

Environment shape used:

```bash
export GBRAIN_EMBED_BASE_URL="http://localhost:20128/v1"
export GBRAIN_EMBED_MODEL="nebius/Qwen/Qwen3-Embedding-8B"
export GBRAIN_EMBED_DIMENSIONS="1536"
export GBRAIN_EMBED_API_KEY="$OMNIROUTE_API_KEY"
```

Important: if the Hermes env file contains non-shell syntax, do not source the full file in a shell profile. Parse or export only the needed key.

## Dimension findings

- GBrain's `content_chunks.embedding` schema expected `vector(1536)`.
- `nebius/Qwen/Qwen3-Embedding-8B` returned `4096` dimensions by default.
- The same model returned `1536` dimensions when the embeddings request included `dimensions: 1536`.

## Provider failures observed

These were credential/permission issues through the available router credentials, not universal model failures:

- `github/text-embedding-3-*`: `401` without GitHub Models permission.
- `mistral/mistral-embed`: auth error.
- `nvidia/nvidia/nv-embedqa-e5-v5`: auth error.

## Verification commands

```bash
cd ~/.hermes/gbrain
gbrain import "~/.hermes/brain"
gbrain embed --stale
gbrain stats
gbrain doctor --json
```

Successful observed state:

- 42 chunks embedded.
- Doctor reported embeddings OK with 100% playwright-pro.
- Brain score reached 76/100.

## Scheduling decision

Avoid `gbrain autopilot` via systemd for this local PGLite setup because it can cause `Timed out waiting for PGLite lock` when manual commands run. Prefer Hermes cron jobs:

- hourly lightweight sync/import,
- daily update check,
- weekly health/extract/embed as needed,
- nightly dream cycle if desired.

Embedding every 15 minutes was considered too aggressive for current data volume.

## Pitfalls to remember

- Do not frame local router usage as a fallback limitation; it is the preferred cost/privacy path here.
- Verify `/v1/embeddings` directly before changing application code.
- Never print or paste the actual router key in notes, logs, or replies.
- Check vector length before running bulk backfill.
- If GBrain's CLI hangs on locks, inspect for background daemons/jobs before changing schema or deleting DB files.
