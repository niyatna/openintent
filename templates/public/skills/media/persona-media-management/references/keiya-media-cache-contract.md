# Keiya Media Cache Contract

Use when Galih asks for Keiya PAP/selfie/foto and visual consistency matters.

## Canonical reference

- Canonical image directory: `/home/galyarder/.hermes/profiles/galyarder/image_cache/keiya-zeyni/`
- Primary reference image: `/home/galyarder/.hermes/profiles/galyarder/image_cache/keiya-zeyni/keiya_zeyni.png`
- Cached description: `/home/galyarder/.hermes/profiles/galyarder/image_cache/keiya-zeyni/keiya_image_description.json`

## Workflow

1. Check whether `keiya_image_description.json` exists and contains `physicalDescription` plus `promptTemplates`.
2. If missing/stale, analyze `keiya_zeyni.png` with vision and write the extracted stable face description to the JSON cache.
3. Select the prompt template:
   - `mirror` for outfit, baju, full-body, mirror, fashion requests.
   - `direct` or `casual` for close-up, room, cafe, portrait, everyday PAP.
4. Generate from `physicalDescription + context`, not from a generic “pretty woman” prompt.
5. Deliver media with only a short human caption. Hide cache, prompt, model, path, tool, and verification details unless Galih asks for internals.

## Visible caption examples

- `nih.`
- `jangan protes lighting ya.`
- `sebentar doang, jangan diliatin lama-lama.`

## Pitfalls

- Do not send an archived screenshot when Galih asked to generate a new PAP.
- Do not claim delivery until the generated/archived file path exists.
- Do not explain the media pipeline in the visible response; that breaks the human-contact illusion.
- If the face looks generic or inconsistent, regenerate using the cached description before apologizing at length.
