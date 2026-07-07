# Identity-Preserving Persona Image Generation

Use when Galih asks for PAP/selfie/foto of an established persona and expects the same face/identity, not a generic generated person.

## Lessons from Galyarder PAP failure

A generated image can pass a generic vision checklist and still be wrong if it does not look like the canonical reference. Do not treat `vision_analyze` as identity verification unless it compares against the actual reference image.

Failure pattern to avoid:

1. Sending a cached reference file when the user asked to generate a new PAP.
2. Falling back to prompt-only generation from a loose text description.
3. Running vision on only the generated output and accepting it because it matches generic traits.
4. User rejects it because it is not the same person.

## Canonical Galyarder reference

Primary reference image:

`/home/galyarder/.hermes/image_cache/galyarder/galyarder.jpg`

Do not use `/home/galyarder/.hermes/profiles/galyarder/image_cache/galyarder/*` as primary identity source unless the OS-level primary image is unavailable or the user explicitly points there. Profile-local images may be older tests, mirrors, or non-canonical examples.

## Correct workflow

1. Resolve the account/posting surface first. If the target is a company account (for example `galyarderlabs.ai`), do not generate Galih/Galyarder face portraits unless Galih explicitly asks for founder-personal content.
2. Resolve the canonical reference path first when a human/persona image is actually appropriate.
3. If the request is identity-preserving (`same face`, `reff image`, `ubah doang`, `based on this image`, `PAP gua sendiri`), prefer an image-to-image/edit/reference backend.
4. Only use prompt-only generation when the user accepts approximate output or no image-reference backend is available.
5. If prompt-only output is used, label it internally as approximate and verify against the reference, not just against the prompt.
6. Before sending, compare generated output with the canonical reference using vision or manual inspection. Reject obvious face drift.

## Tool reality

Hermes `image_generate` currently accepts only:

- `prompt`
- `aspect_ratio`

It does not accept `input_image`, `reference_image`, `image_url`, `mask`, or `strength`. For real reference-image generation, use or build a backend/tool that supports image input.

## Better backend classes

Good candidates for identity-preserving edit/reference workflows:

- ComfyUI img2img / IP-Adapter / FaceID / InstantID pipelines.
- OpenAI/ChatGPT/Codex image edit if the active API path supports image input.
- Local 9Router `/v1/images/generations` models whose metadata includes `input_modalities: ["text", "image"]`, such as Flux Kontext / Flux 2 variants, if the payload contract accepts image data.

Avoid relying on text-only models for face preservation, even if they are high-quality image models.

## Visible response rule

If the user asks for internals or brainstorming, explain the limitation directly. If the user asks for a PAP, keep the visible delivery short and only send a generated/verified file path; do not expose prompts, model names, or cache paths unless asked.
