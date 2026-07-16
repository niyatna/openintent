# Governed-agent docs surface visual QA

Use this pattern when redesigning an agent/company/docs homepage away from cyber-hacker or field-manual styling toward a credible governed-agent documentation surface.

## Target feel

- Clean documentation/product-spec surface, not cyber cosplay.
- Governance reads through information architecture: chapters, gates, templates, checks, proof rows, and clear build path.
- Monospace and green accents are reserved for status, compliance, code, or evidence badges — not the whole brand tone.
- Public-safe cues are visible, but not theatrical.

## Homepage structure that worked

1. Short, plain nav labels to prevent laptop-width overflow.
2. Above-fold hero answers the actual build task in plain language.
3. Primary CTA visible above fold; secondary CTA(s) nearby but less dominant.
4. Right-side overview/manifest panel reinforces scope, output, and gates.
5. Stats/cards are compact enough not to push the chapter path too far below fold.
6. Chapter path appears immediately after the hero with concrete artifact/check framing.

## Verification ladder

Run all three checks before calling the redesign done:

1. Build/static check — e.g. `pnpm build` / framework equivalent exits 0.
2. DOM layout audit at a realistic laptop viewport — check `scrollWidth <= clientWidth`, no right/left offenders, nav inside viewport, CTA above fold.
3. Screenshot/vision review — confirm the actual screenshot reads like a clean governed docs surface, with no stable-diffusion-image-generationping, crowding, or cyber-cosplay residue.

## Evidence to report

Keep final report short:

- build result and error/warning count;
- viewport used;
- overflow result and offender count;
- CTA/nav above-fold status;
- one sentence visual verdict.

Do not paste long screenshots analysis unless the user asks.