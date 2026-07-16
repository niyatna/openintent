# Agentic Company Docs Site Rebuild — 2026-05-21

## Session signal

Owner rejected an initial static HTML guide as low-value: the UI was weak, the content was thin/yapping, and it did not represent the full Agentic Company setup stack. He explicitly wanted an Astro site deployable with Cloudflare Wrangler, using design/code skills and a complete step-by-step guide from the actual setup.

## Durable lesson

When the request is a serious public guide/docs/website for Default/Hermes/Agent OS infrastructure, do not produce a small one-file static HTML artifact unless the user explicitly asks for a throwaway mockup. Treat the deliverable as a real product/docs surface:

1. Use the requested production stack when stated (e.g. Astro + Wrangler for Cloudflare).
2. Build a real information architecture before visual polish.
3. Include full setup chapters, not positioning filler.
4. Keep content public-safe: publish patterns/templates, never private credentials, raw SOUL files, cookies, TOTP, backup codes, Discord IDs, wallet secrets, raw memories, or exact private paths.
5. Design for the brand/product canon and the reader's build path, not a generic SaaS landing page.
6. Verify build, local preview/crawl, responsive layout, secret scan, and deploy dry-run before reporting readiness.
7. Public deploy still requires user approval.

## Corrected artifact shape from session

The rebuilt project used:

- Astro static output.
- Cloudflare Workers static assets via Wrangler (`[assets] directory = "./dist"`).
- `pnpm build` as `astro check && astro build`.
- `wrangler deploy --dry-run` before public deploy.
- Premium command-docs UI with dark/luminous Default visual direction.
- Deep docs chapters covering runtime, profiles/SOUL, memory, communication HQ, accounts/access, tools/MCP, Paperclip control plane, workforce, relay, risk gates, security, deployment, maintenance, full setup playbook, and 30-day roadmap.
- Copyable templates for SOUL skeletons, access contract, Paperclip task packet, relay packet, and no-publish checklist.

## Specific pitfalls

- **Thin docs are failure:** A guide about setting up an agentic company must teach the system end-to-end. A nice hero section cannot compensate for missing setup substance.
- **Do not hide behind "public-safe" as an excuse for shallow content:** Replace private details with generalized patterns, schemas, and gates.
- **Do not overclaim Claude Code participation:** If Claude Code was attempted but hung or produced no usable output, report it as attempted/validated, not as the source of improvements.
- **Responsive verification matters:** Browser screenshots can reveal stable-diffusion-image-generationping not obvious from DOM width checks. Fix nav/hero breakpoints and rerun build/preview.

## Verification ladder used

- `pnpm build` → Astro check/build passes.
- Local preview returns HTTP 200.
- Internal crawl returns 0 errors.
- Secret/private leakage scan across source and build output returns 0 leaks.
- `wrangler deploy --dry-run` passes.
- Browser visual review catches layout/responsiveness issues.

## Reuse trigger

Use this reference when asked to build a public guide/docs website, especially for Company, Hermes Agent, Agent OS, Paperclip, identity/profile splits, or any infrastructure guide that must be both visually premium and operationally complete.
