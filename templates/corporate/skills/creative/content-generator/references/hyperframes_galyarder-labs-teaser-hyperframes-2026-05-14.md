# Galyarder Labs Teaser with HyperFrames — 2026-05-14

## Context

Galih asked for the Galyarder Labs test video to be made better with HyperFrames after a first Remotion version. For Galyarder Labs launch/product visuals, the preferred route is HyperFrames first because it is faster for editorial motion graphics, title-card sequences, website-style visuals, captions, and marketing teasers.

Canon grounding used before writing copy/design:

- `/home/galyarder/Documents/Obsidian Vault/galyarder/galyarder-labs/README.md`
- `BRAND.md`
- `DESIGN.md`
- `AGENTS.md`

Core public-safe lines:

```text
Dream → Airlock → Machine
Human intent becomes infrastructure.
Empowering Human Intent.
Autonomous execution infrastructure for high-agency operators.
```

Avoided categories:

```text
AI wrapper, chatbot company, generic dashboard, bookkeeping app, prompt pack, crypto-hype app, effortless/full-autonomy promise.
```

## Output

```text
Project: /home/galyarder/video-stack/galyarder-labs-hyperframes
Main HTML: /home/galyarder/video-stack/galyarder-labs-hyperframes/index.html
Design note: /home/galyarder/video-stack/galyarder-labs-hyperframes/DESIGN.md
Output MP4: /home/galyarder/video-stack/galyarder-labs-hyperframes/galyarder-labs-hyperframes.mp4
Preview frame: /home/galyarder/video-stack/galyarder-labs-hyperframes/preview-15s.png
Samples: sample-3s.png, sample-8s.png, sample-13s.png, sample-18s.png, sample-23s.png, sample-28s.png
```

Specs:

```text
Duration: 31s
Resolution: 1920x1080
FPS: 30
Codec: H.264
Size: 6,795,147 bytes (~6.5 MB)
Audio: none / visual-only
```

## Important Workflow Correction

`hyperframes init ... --non-interactive` previously timed out and Hermes marked it blocked. That does **not** mean HyperFrames cannot be used.

When scaffold blocks or times out, manually author a valid standalone HyperFrames project instead of immediately switching to Remotion:

1. Create a project directory.
2. Write a concise `DESIGN.md` from canon or user style direction.
3. Write `index.html` directly with a top-level `data-composition-id` element, `data-start`, `data-duration`, `data-width`, and `data-height`.
4. Register `window.__timelines["<composition-id>"]` synchronously.
5. Run lint, validate, inspect, render, ffprobe, and preview-frame checks.

Minimal skeleton:

```html
<!doctype html>
<html>
  <body>
    <div id="stage" data-composition-id="root" data-start="0" data-duration="31" data-width="1920" data-height="1080">
      <!-- scenes -->
    </div>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // synchronous GSAP timeline construction
      window.__timelines["root"] = tl;
    </script>
  </body>
</html>
```

## Composition Pattern Used

- Single standalone `index.html`.
- Six absolute-positioned scenes:
  1. short answer
  2. origin problem
  3. transformation
  4. Dream → Airlock → Machine doctrine
  5. public infrastructure suite
  6. final lockup
- Shared top bar and bottom gold threshold line.
- Violet/gold wipe transition between scenes.
- Canonical palette from `DESIGN.md`: deep midnight, charcoal navy, violet, soft gold, luminous ivory, periwinkle.
- Proof-safe product suite: Ledger, HQ, Framework, Agent.

## GSAP Pitfalls Found

### Avoid empty selector warnings

A generic `enter(scene)` function that tweens selectors not present in a scene causes many browser warnings like:

```text
GSAP target #s1 .chip not found
GSAP target #s2 .seal not found
```

Use a small guard:

```js
function tweenIf(selector, vars, position) {
  if (document.querySelector(selector)) {
    tl.from(selector, vars, position);
  }
}
```

Then call `tweenIf(scene + ' .chip', {...}, t + 0.86)` instead of unconditional `tl.from(...)`.

### Avoid transform conflicts on wipe elements

HyperFrames lint warns if CSS sets `transform` while GSAP animates `xPercent`:

```text
gsap_css_transform_conflict: "#wipe" has CSS `transform: ...` and GSAP tween animates xPercent
```

Move all transform state into GSAP:

```js
tl.set('#wipe', { opacity: 1 }, t);
tl.fromTo('#wipe',
  { xPercent: -130, skewX: -12 },
  { xPercent: 135, skewX: -12, duration: 0.78, ease: 'power3.inOut' },
  t
);
tl.set('#wipe', { opacity: 0 }, t + 0.78);
```

### Avoid overlapping tween warnings

Do not animate `opacity` in overlapping `fromTo` and `to` tweens on the same element. Use `tl.set()` for instantaneous visibility toggles around wipe animations.

## Verification Commands

```bash
cd /home/galyarder/video-stack/galyarder-labs-hyperframes

hyperframes doctor
hyperframes lint --strict
hyperframes validate
hyperframes inspect --samples 9 --json > .inspect.json

hyperframes render --output galyarder-labs-hyperframes.mp4 --quality high --fps 30 --strict

stat -c '%n %s bytes' galyarder-labs-hyperframes.mp4
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 galyarder-labs-hyperframes.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,duration -of json galyarder-labs-hyperframes.mp4

ffmpeg -y -i galyarder-labs-hyperframes.mp4 -ss 00:00:15 -vframes 1 preview-15s.png
```

Verified results:

```text
hyperframes lint --strict -> 0 errors, 0 warnings
hyperframes validate      -> No console errors · 227 text elements pass WCAG AA
hyperframes inspect       -> ok true, 0 errors, 0 warnings, 0 issues
ffprobe duration          -> 31.000000
video stream              -> h264, 1920x1080, 30/1 fps, 31s
```

## Visual QA Notes

Vision inspection of `preview-15s.png` found:

- Brand fit: premium sci-fi/tech lab aesthetic, dark violet/gold, polished and futuristic.
- Readability: top-right gold text clear; top-left gray brand slightly low contrast but readable.
- Layout: safe margins, no stable-diffusion-image-generationping or overflow.
- Artifacts: no major glitches; slight gradient banding/noise in central glow is acceptable for texture.
- Bottom threshold line is intentional; avoid making it look like accidental artifact by keeping it aligned and subtle.

## Delivery Pattern

For Discord delivery, attach the MP4 directly:

```text
MEDIA:/home/galyarder/video-stack/galyarder-labs-hyperframes/galyarder-labs-hyperframes.mp4
```

Keep the final response concise: file path, specs, and verification proof.
