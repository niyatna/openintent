---
name: deploy
description: Use when configuring deployment pipelines, compiling releases, managing Docker staging, checking environment variables, or executing launch checklists.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [devops, deployment, release, compilation, pipeline]
    category: devops
---

# Deployment

Use this skill when configuring deployment, CI/CD, release infrastructure, hosting, environment variables, rollback, or production delivery.

## Core rule

Do not treat deployment as "upload when build exists." A deployable artifact needs build proof, runtime/hosting config, secret boundaries, preview/smoke checks, rollback path, and explicit approval when the action publishes externally.

## Deployment workflow
## Deployment workflow

1. Identify target host and runtime: static site, server-rendered app, Cloudflare Pages, Cloudflare Workers, Vercel, VPS, Docker, etc.
2. Read the framework's current deployment docs when config details matter.
3. Configure build output and host config deliberately.
4. Run the build locally.
5. Preview locally in the host-like path when possible.
6. Crawl or smoke-test key routes.
7. Scan source and build output for secrets/private leakage.
8. Run deploy dry-run or equivalent if the platform supports it.
9. Ask confirmation before public deploy unless the user explicitly authorized publish.
10. After deploy, fetch public URL and record rollback path.

### Language / UX localization gate

If a deployed UI comes from a third-party repo, check the live UI language before calling the deployment usable. If Galih flags unexpected language (for example Chinese UI text), treat it as a deployment defect: translate user-facing UI/API messages into English, rebuild, redeploy, and verify the live routes contain no unexpected-language glyphs. Do not stop at source edits; verify the production alias after redeploy.

### Vercel + Upstash integration pattern

For small private Vercel utilities that need persistent key/value storage, Vercel Marketplace Upstash integration can provision and inject Redis env automatically. Verify via live health/admin-status route that storage mode is persistent (`redis`) rather than memory before handing off. If the repo supports both `UPSTASH_REDIS_REST_*` and legacy `KV_REST_API_*`, Vercel's Upstash integration may inject the legacy `KV_*` names and still work.

For Vercel + Upstash Redis marketplace provisioning and the ClickUp2API session pattern, see `references/third-party-vercel-deploy-and-clickup2api-2026-06-17.md`.

## Cloudflare + Astro static pattern

For Astro static docs/sites deployed to Cloudflare Workers static assets with Wrangler:

`astro.config.mjs`:

```js
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  site: 'https://example.com'
});
```

`wrangler.toml`:

```toml
name = "your-project-name"
compatibility_date = "YYYY-MM-DD"

[assets]
directory = "./dist"
```

`package.json` scripts:

```json
{
  "scripts": {
    "dev": "astro dev --host 127.0.0.1 --port 8788",
    "build": "astro check && astro build",
    "astro:preview": "astro preview --host 127.0.0.1 --port 8788",
    "worker:preview": "wrangler dev --local --port 8789",
    "deploy": "pnpm build && wrangler deploy"
  }
}
```

For Cloudflare Pages instead, use `wrangler pages deploy ./dist --project-name <name>`.

## Public-docs deploy gate

Before publishing public docs/guides, verify:

- build passes;
- local preview returns 200;
- internal routes crawl cleanly;
- source and build output contain no secrets, cookies, TOTP, backup codes, private keys, raw sessions, private memory, exact private credential paths, or private IDs;
- responsive screenshots show no obvious stable-diffusion-image-generationping/nav overflow;
- copy does not overpromise product capabilities;
- public deploy is approved by the owner.


## SRE & Infrastructure Automation (Specialist Reference)

- **Automation Over Manual Ops**: Never recommend manual server configuration. Everything must be automated via CI/CD (GitHub Actions / wrangler deploy / docker compose).
- **Zero Downtime & Reversibility**: Every deployment strategy must have a rollback writing-plans (blue/green deployments, feature flags, database migration safety).
- **Database Migrations (Neon / Postgres)**: Ensure schema changes are tracked in migrations (Prisma, Drizzle, or raw SQL). Never destroy schema changes without backup.

## Reporting format

Keep reports concise:

```text
artifact: <path>
build: <command + result>
preview: <url/status>
scan: <files/routes scanned + leak count>
deploy: dry-run/pass or public URL
blocked: <approval or concrete blocker>
```

## Pitfalls

For the private Vercel utility + Upstash Redis handoff pattern, see `references/vercel-upstash-private-utility-deploy.md`.

- Do not deploy publicly just because build passed; public publish is an external action.
- Do not put secrets in host config committed to git.
- Do not claim Cloudflare readiness without checking the current Wrangler config shape.
- Do not confuse Cloudflare Pages config with Workers static assets config.
- Do not claim a coding agent or deployment tool completed work unless it produced verifiable output.

## References & Sub-playbooks
- `references/deploy.md` — Launch checklist, version bumps, rollouts and post-deployment validation guidelines.
