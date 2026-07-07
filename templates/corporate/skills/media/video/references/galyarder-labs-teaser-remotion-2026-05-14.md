# Galyarder Labs Teaser with Remotion — 2026-05-14

## Context

Galih asked for a short test video explaining "apa itu Galyarder Labs?" after the video stack was installed. He allowed either HyperFrames or Remotion.

Because the request was public/product/brand-facing, the agent first grounded the content in canonical Galyarder Labs docs:

- `/home/galyarder/Documents/Obsidian Vault/galyarder/galyarder-labs/README.md`
- `BRAND.md`
- `DESIGN.md`
- `AGENTS.md`

Canon used:

```text
Dream → Airlock → Machine
Human intent becomes infrastructure.
Empowering Human Intent.
Galyarder Labs builds autonomous execution infrastructure for high-agency operators.
```

Avoided claims/categories:

```text
AI wrapper, chatbot company, generic dashboard, bookkeeping app, crypto-hype app, effortless/full-autonomy promise.
```

## Tool Choice

Initial intent was HyperFrames, but `content-generator init galyarder-labs-teaser --non-interactive` timed out and Hermes marked it blocked (`Do NOT retry this command`).

Successful fallback: use Remotion in the verified smoke workspace.

```text
Workspace: /home/galyarder/video-stack/remotion-smoke
Composition id: galyarder-labs-teaser
Output: /home/galyarder/video-stack/remotion-smoke/out/galyarder-labs-teaser.mp4
```

## Remotion Implementation Pattern

Add a standalone composition file, then register it in `Root.tsx`.

Important patterns:

- Use `useCurrentFrame`, `interpolate`, `spring`, and `<Sequence>`.
- Use canonical Galyarder colors from `DESIGN.md`.
- Keep public-facing style Dream-like: luminous, calm, editorial, threshold-like.
- Keep product truth concrete: Ledger, HQ, Framework, Agent.
- Run TypeScript before rendering.

If TypeScript 6 reports `moduleResolution=node10 is deprecated`, set:

```json
"moduleResolution": "Bundler",
"ignoreDeprecations": "6.0"
```

If React typings are missing, install:

```bash
npm install -D @types/react@latest @types/react-dom@latest
```

## Verification Commands

```bash
cd /home/galyarder/video-stack/remotion-smoke
npx tsc --noEmit
npx remotion versions
npx remotion compositions src/index.ts
npx remotion still src/index.ts galyarder-labs-teaser out/galyarder-labs-teaser-mid.png --frame=390 --overwrite
npx remotion render src/index.ts galyarder-labs-teaser out/galyarder-labs-teaser.mp4 --overwrite --codec=h264 --crf=23
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,duration -of json out/galyarder-labs-teaser.mp4
ffmpeg -y -i out/galyarder-labs-teaser.mp4 -ss 00:00:13 -vframes 1 out/galyarder-labs-teaser-preview.png
```

Verified output:

```text
galyarder-labs-teaser    30fps    1920x1080    780 frames / 26.00 sec
MP4 size: 3,537,552 bytes
ffprobe duration: 26.048000
Video stream: h264, 1920x1080, 30fps
Audio stream: aac, 26.048s (present even though the piece was visually authored)
```

## Visual QA Notes

A preview-frame vision check found:

- Main headline very readable.
- Brand fit strong: premium, strategic, dark, violet/gold, editorial.
- No stable-diffusion-image-generationping or overflow visible.
- Minor future refinements: brighten subtitle/small labels for compression and avoid one-word orphan wraps such as `the machine.` where possible.

## Delivery Pattern

For Discord delivery, include the media attachment path directly:

```text
MEDIA:/home/galyarder/video-stack/remotion-smoke/out/galyarder-labs-teaser.mp4
```
