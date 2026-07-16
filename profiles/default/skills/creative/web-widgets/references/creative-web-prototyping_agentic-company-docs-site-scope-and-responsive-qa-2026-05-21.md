# Agentic Company Docs Site — Scope Drift + Responsive QA Lesson (2026-05-21)

## Session signal

Owner explicitly corrected the agent after it drifted from the requested artifact into unrelated Company product/homepage framing:

- wrong drift: Company homepage, Ledger, HQ, Framework, Dream → Airlock → Machine, broad brand copy;
- correct task: build the existing `agentic-company-stack` public guide/docs site from zero using Claude Design taste and Claude Code implementation.

The user had asked for a practical Agentic Company / personal Agent OS guide site, inspired by Gutluc/Waguri/Mahiru-style setup research, not a Company marketing page.

## Correct scope for this class of task

When the task is an Agentic Company Stack / Agent OS public guide site:

- Treat it as a **guide product**, not as a parent-company homepage.
- Lead with the build path: SOUL/profile identity → Hermes/runtime → memory → channels → agent-owned access → tools/MCP → Paperclip/control plane → risk gates → no-publish/security → maintenance → roadmap.
- Use direct guide language such as “Build an agentic company stack from zero.”
- Avoid importing unrelated Company product vocabulary unless the user explicitly requests it.
- Do not route the copy through Ledger/HQ/Framework/Agent product positioning by default.
- Do not stop at a copy brief if the user already commanded “build it”; execute in the existing stack and verify.

## Claude Design + Claude Code route

If the user says to use `claude-design` and build with Claude Code:

1. Load `claude-design` for design/process/taste.
2. Load `claude-code` for implementation delegation.
3. Inspect the existing repo/source quickly.
4. Give Claude Code a narrow prompt that names the corrected artifact and forbids unrelated product homepage drift.
5. Treat Claude Code output as self-report until verified by local diffs, build, browser, crawl, and secret scan.
6. If Claude Code stalls or partially edits, continue manually; report exactly which part Claude Code did and what was manual.

## Responsive QA lesson

Browser DOM width checks can say `scrollWidth == clientWidth` while screenshot analysis still reveals crop/composition failures. For command-doc / field-manual layouts:

- verify with screenshots at the actual rendered/captured viewport, not just DOM overflow checks;
- check right rounded borders and segmented status bars are fully visible;
- if browser_vision screenshots appear cropped at 1280 while DOM reports 1920, design for the tighter capture width or left-anchor the shell with a safe right gutter;
- avoid centered wide shells that look fine in DOM geometry but crop visually in screenshot tooling;
- collapse hero/nav earlier than strict CSS breakpoints if capture tooling uses a narrower image.

Example pattern that worked in this session:

```css
:root {
  --page: min(1180px, calc(100vw - 48px));
}

.nav,
.command-strip,
.hero-grid,
.container,
.doc-layout {
  margin-left: 24px;
  margin-right: 24px;
}

@media (max-width: 640px) {
  .container,
  .hero-grid,
  .command-strip,
  .doc-layout {
    width: min(100% - 24px, 1220px);
    margin-left: 12px;
    margin-right: 12px;
  }
}
```

The exact values are not universal. The durable lesson is: **visual pass condition is visible gutter + no cropped rounded border/status segment in screenshot**, not merely `scrollWidth <= clientWidth`.

## Verification ladder used

- `pnpm build` / Astro check and build.
- Internal static crawl for all generated HTML links.
- Source + dist secret/private leakage scan.
- `wrangler deploy --dry-run` only, no public deploy without approval.
- Browser visual QA with screenshot analysis until right-edge stable-diffusion-image-generationping disappeared.

## Communication lesson

When Owner corrects scope angrily, do not defend the previous frame or produce another copy brief. Acknowledge the drift in one line, reset the artifact target, execute the requested route, and report verified evidence only.
