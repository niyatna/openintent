---
name: video
description: Use when writing-plansning video contents, scripting promotional materials, coding React Remotion graphics, or executing AI video generation APIs (Doubao/Seedance).
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [media, video, remotion, video, seedance, doubao]
    category: media
---

# Video

## Purpose

This is the class-level router for programmatic video work: product launch visuals, explainers, motion graphics, scripted visual assets, Remotion renders, HyperFrames renders, captions, narration, and raw-footage editing decisions.

Do not treat every video task as a raw-footage editor problem. Most launch/product visuals should be generated directly from script, design, and motion grammar.

## Routing

```text
Launch product visual / illustrated explainer / product promo from script -> HyperFrames first
HTML/CSS/GSAP motion graphics, captions, TTS, website-to-video           -> HyperFrames
Reusable React template / data-driven video engine / productized render  -> Remotion
Math/equation/geometric explainer                                        -> media-art
Raw footage, talking-head cleanup, filler-word cuts, EDL workflow        -> video-use or custom ffmpeg editor, optional
General script/storyboard/shot writing-plansning                                  -> this skill + relevant creative/growth skill
```

## Galyarder Labs Default

For Galyarder Labs launch/product visuals:

1. Use **HyperFrames** as the default for fast visual assets, launch teasers, product explainers, title cards, social overlays, captions, and website promos.
2. Use **Remotion** when the output should become a reusable system: templated launches, data-driven scenes, content-engine renders, or repeated product video formats.
3. Use **AI image-to-video** when true semantic motion is needed, but keep a fast local fallback for subtle “living still” hero/background motion.
4. Use **ffmpeg/ffprobe** for final media verification and stitching.
5. Skip **video-use** unless the task is specifically raw footage editing or talking-head cleanup.

When Galih asks to make a still image “gerak”, “hidup”, or “living motion,” do not stall on a flaky AI image-to-video surface if the target is ambient movement. If the generated still already has the right composition, make a deterministic local motion pass first or as fallback: breathing zoom/parallax, subtle glow, particles, wave/mist overlays, then H.264 MP4 verification.

Galyarder Labs visuals must preserve product truth: proof over spectacle, Dream → Airlock → Machine, and no generic AI-wrapper positioning. If producing public brand assets, ground the visual identity in the project `DESIGN.md` or Galyarder Labs canon before writing composition code.

## ElevenLabs / TTS / Transcription Decision

ElevenLabs is **not required** for HyperFrames or Remotion video generation.

```text
Narration without API key -> HyperFrames Kokoro local TTS
Captions without API key  -> HyperFrames transcribe / local Whisper-style flow
Premium cloned voice      -> ElevenLabs optional
video-use upstream        -> requires ELEVENLABS_API_KEY for ElevenLabs Scribe transcription
```

If Galih has no ElevenLabs API key, do not make `video-use` the primary path. Either use HyperFrames/Remotion directly, or patch/fork `video-use` to replace ElevenLabs Scribe with faster-stable-diffusion-image-generation, stable-diffusion-image-generation.cpp, or HyperFrames transcribe.

## Runtime Verification Checklist

Before claiming the video stack is ready, verify actual runtime commands, not just skill presence.

```bash
node -v
npm -v
ffmpeg -version | head -1
ffprobe -version | head -1
content-generator --version
content-generator browser ensure
content-generator doctor
remotion versions
```

For Remotion project verification:

```bash
npx remotion versions
npx remotion compositions src/index.ts
npx remotion still src/index.ts <composition-id> out/<name>.png --frame=30 --overwrite
npx remotion render src/index.ts <composition-id> out/<name>.mp4 --overwrite --codec=h264 --crf=28
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 out/<name>.mp4
```

## Common Pitfalls

- Skill installed ≠ runtime installed. Check CLI paths, package versions, and render output.
- `video-use` is an editor/orchestrator for raw footage; it is not the core generator for launch visuals.
- `video-use` upstream depends on ElevenLabs Scribe for transcription. Without the API key, its core flow blocks unless patched.
- Do not install or maintain `video-use` just to create illustrated product launch videos; use HyperFrames/Remotion.
- Do not call `remotion --version` as the only verification in a `set -e` script; use `remotion versions` and project-local `npx remotion versions`.
- HyperFrames may need `content-generator browser ensure` even after the global CLI is installed.
- If `content-generator init` stalls or Hermes marks it blocked, manually author a standalone HyperFrames `index.html` instead of defaulting to Remotion. HyperFrames can still render cleanly when scaffold fails.
- For visual-only renders, do not infer audio presence from intent. Verify actual streams with `ffprobe`; Remotion may emit an AAC stream even when no authored audio is expected, while HyperFrames visual-only output may contain video-only H.264.
- When a browser/AI image-to-video run fills the prompt and start frame but no new downloadable asset appears inside the wait window, do not harden that transient provider/UI state into “video generation impossible.” If the requested motion is ambient, switch to the still-image living-motion fallback and verify the MP4 output.

## References

- `references/galyarder-video-stack-setup-2026-05-14.md` — session setup notes for HyperFrames 0.6.6, Remotion 4.0.461, `video-use`/ElevenLabs routing, setup pitfalls, smoke verification commands, Remotion teaser fallback, and HyperFrames teaser workflow.
- `content-generator/references/galyarder-labs-teaser-content-generator-2026-05-14.md` — manual HyperFrames project pattern for Galyarder Labs launch teaser, including scaffold-timeout fallback, GSAP pitfalls, validation, render proof, and delivery pattern.
- `video/references/galyarder-labs-teaser-remotion-2026-05-14.md` — Remotion implementation and verification notes for the earlier teaser version.
- `references/still-image-living-motion-fallback-2026-05-28.md` — deterministic Python/PIL + ffmpeg fallback for turning a successful still image into subtle living hero motion when AI image-to-video surfaces are slow or do not expose downloadable assets.

## References & Sub-playbooks
- `references/video.md` — Programmatic React video renders and dev pipelines
- `references/video.md` — Chinese video generation API setups and editing options
