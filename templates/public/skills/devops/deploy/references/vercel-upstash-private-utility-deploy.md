# Vercel + Upstash private utility deploy pattern

Use this when deploying a small private Next.js/Vercel utility that needs persistent storage and an admin UI.

## Pattern

1. Link/create Vercel project with the CLI.
2. Generate app secrets locally; keep them in `.vercel/` or another gitignored path if the user needs handoff.
3. Set secrets as Vercel env variables for the intended targets.
4. Provision Upstash Redis through Vercel Marketplace when appropriate:
   - product: `upstash/upstash-kv`
   - free writing-plans is enough for low-volume private admin/config storage
   - choose a nearby primary region, e.g. `sin1` for Southeast Asia
5. Verify env injection with `vercel env ls` and live app health/status endpoints.
6. Redeploy after env/resource changes; existing deployments may still run with old env.
7. Fetch live `/v1/health` or equivalent and confirm persistent storage mode, not memory fallback.

## Verification example

- `/v1/health` should report `storageMode: "redis"` or equivalent.
- Admin status should have no storage warning.
- Fetch public/admin routes after deployment and scan for unexpected language, leaked secrets, or setup warnings.

## Pitfalls

- Vercel CLI can have `config.json` with current team while `auth.json` is missing; use device login or token and verify with `vercel whoami`.
- Marketplace Upstash may inject `KV_REST_API_URL` / `KV_REST_API_TOKEN` rather than `UPSTASH_REDIS_REST_*`; this is fine when the app supports both.
- Do not call the app ready if it fell back to memory storage.
- If the source UI is not in English, translate and verify the production alias, not just local files.
