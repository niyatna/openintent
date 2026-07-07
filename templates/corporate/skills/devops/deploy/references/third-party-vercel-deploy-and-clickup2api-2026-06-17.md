# Third-party repo deploy to Vercel: ClickUp2API session notes (2026-06-17)

## Trigger
Galih asked to clone/analyze an unknown third-party repo, then deploy it to Vercel (`hibiyaQAQ/clickup2api`). During the session he corrected two process/style failures:

- Do **not** execute unknown repo scripts (`npm install`, build, tests) before analysis/approval; package managers can run lifecycle hooks.
- Do **not** frame use of a paid subscription/entitlement adapter as `nyolong`; say leverage/utilization/routing owned capacity.

## Safe default for unknown repos
1. Clone into `/home/galyarder/projects`.
2. Static inspect first:
   - `package.json` scripts and package manager hooks
   - lockfile `hasInstallScript` / lifecycle scripts
   - env examples and secret handling
   - deployment config (`vercel.json`, CI files)
   - exposed routes/auth/storage paths
3. Only after static inspection, ask/confirm before running dependency install/build/test/dev server unless the user already explicitly authorized execution.
4. If execution is authorized, prefer local/sandboxed verification and report exactly what executed.

## Vercel CLI/auth pattern used
- `vercel` binary may not be in PATH, but `npx --no-install vercel` can still be available.
- Check auth with `npx --no-install vercel whoami`.
- If auth token missing, use device flow: `npx --no-install vercel login` and give Galih the URL/code.
- Vercel auth/config lives under real user home, e.g. `/home/galyarder/.local/share/com.vercel.cli/`; do not assume sandbox-only state before verifying `HOME`.

## Project setup pattern
1. Link/create project:
   ```bash
   npx --no-install vercel link --yes --project <project-name>
   ```
2. Generate secrets locally and store only under `.vercel/` (gitignored):
   - `SESSION_SECRET`
   - `ADMIN_SETUP_KEY`
3. Add env via CLI:
   ```bash
   npx --no-install vercel env add SESSION_SECRET production --value "$SESSION_SECRET" --yes --force
   npx --no-install vercel env add ADMIN_SETUP_KEY production --value "$ADMIN_SETUP_KEY" --yes --force
   ```
   Repeat for `development`/`preview` if needed.
4. Provision Upstash Redis through Vercel Marketplace when URL/token are not manually supplied:
   ```bash
   npx --no-install vercel install upstash/upstash-kv \
     --name <resource-name> \
     --writing-plans free \
     -m primaryRegion=sin1 \
     -m eviction=true \
     -m prodPack=false \
     -m autoUpgrade=false \
     --no-claim \
     --format=json
   ```
   Verify env vars appear: `KV_REST_API_URL`, `KV_REST_API_TOKEN`, etc.
5. Deploy:
   ```bash
   npx --no-install vercel deploy --prod --yes
   ```

## Verification gates used
- Local `npm run build` after dependency patching.
- `npm audit` result: high/critical must be gone before public deploy; avoid `npm audit fix --force` if it would downgrade core framework drastically.
- Live health:
  ```bash
  curl -fsS https://<domain>/v1/health
  curl -fsS https://<domain>/api/admin/status
  ```
- For this repo, proof of Redis readiness is `storageMode: "redis"` and no warnings.

## ClickUp2API-specific operational notes
- Repo exposes ClickUp Brain as OpenAI-compatible API.
- It supports Vercel Upstash env names `KV_REST_API_URL` / `KV_REST_API_TOKEN` and direct Upstash names `UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN`.
- Final functional proof requires Galih's real ClickUp Team ID + Brain JWT; do not ask him to paste JWT in chat if he can enter it via `/admin`.
- Correct JWT source: ClickUp browser DevTools Network after triggering Brain/AI, request similar to `access-token`, `Authorization: Bearer ...`; not `cu_form_jwt`.
- First test `/v1/usage`; only then test `/v1/chat/completions`.
