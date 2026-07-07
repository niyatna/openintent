# Galyarder Media Cache Contract

Use when generating or selecting images of Galyarder/Galih.

## Canonical reference

- Canonical image directory: `/home/galyarder/.hermes/image_cache/galyarder/`
- Primary reference image: `/home/galyarder/.hermes/image_cache/galyarder/galyarder.jpg`
- Profile-local mirror/cache may also exist at `/home/galyarder/.hermes/profiles/galyarder/image_cache/galyarder/`, but the OS-level `galyarder.jpg` is the primary identity reference.
- Use available images in that directory as identity/style anchors.
- If unsure which file matches the requested style, inspect candidate images with `vision_analyze` before generating or sending.

## Stable visual anchor

Galyarder/Galih should remain a young adult masculine-presenting Indonesian/Sundanese-coded man with medium tan/light-brown skin, rounded oval face, soft cheeks, dark eyes, natural dark eyebrows, medium rounded nose, medium lips, clean-shaven face, and thick messy black short-to-medium hair with casual volume/fringe.

The default mood is calm, grounded, introspective, strategic, and human.

## Common style motifs

- Casual smartphone photo or grounded portrait.
- Soft indoor lighting, plain wall/background, low-drama composition.
- White semi-formal shirt or modest clean clothing.
- Optional natural-wood acoustic guitar with non-readable assorted stickers.
- Optional simple black wristband.

## Generation workflow

1. Prefer true image-to-image / image-edit when the user wants “same person, changed scene/outfit/style”. Text-only generation from a vision description is lower fidelity and can drift.
2. Hermes `image_generate` is currently prompt-only (`prompt` + `aspect_ratio`) and does **not** accept a reference image path. For real reference-preserving edits, use an image backend that supports img2img/edit/inpaint/reference input (for example ComfyUI img2img with `--input-image`, OpenAI image edit if configured, or another explicit image-reference pipeline).
3. If only prompt-only generation is available, inspect/read the primary reference image and build a careful prompt from stable traits; label it as approximate if reporting internals.
4. Save or verify the generated output path (prefer `/home/galyarder/.hermes/profiles/galyarder/image_cache/generated/`).
5. Run `vision_analyze` on generated output when identity consistency matters; reject outputs with face drift, generic CEO look, anime/style drift, heavy beard, readable logo/text, or over-polished output.
6. Send the generated file with `MEDIA:/absolute/path`. Do not send the canonical `image_cache/galyarder/*` reference file as the generated PAP unless the user explicitly asks for the reference itself.

## Prompt constraints

Include: identity-consistent face, medium tan skin, messy black hair, calm neutral expression, grounded human realism.

Avoid: anime, generic stock CEO, cyberpunk excess, sigma caricature, heavy beard/mustache, random face drift, overly polished studio glamour, readable copied logos, or changing the person into someone else.

## Keiya-related requests

If the requested image includes or concerns Keiya, use Keiya's reference cache first: `/home/galyarder/.hermes/profiles/galyarder/image_cache/keiya-zeyni/`.
