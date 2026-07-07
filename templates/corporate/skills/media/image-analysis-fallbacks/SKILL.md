---
description: Use when native vision tools fail, parsing local OCR strings, or building
  descriptive screenshots overlays summaries.
name: image-analysis-fallbacks
tags:
- images
- screenshots
- ocr
- vision-fallback
- media
---


# Image Analysis Fallbacks

## When to use

Use this skill when:
- The user sends an image or provides a local image path and expects a reaction, description, OCR, or summary.
- `vision_analyze` fails because of provider setup, unsupported format, file size, or transient backend issues.
- Browser/image preview tooling is unavailable, overkill, or not enough for text-heavy screenshots.
- You need to verify visible text/numbers from a screenshot before responding.

Do **not** turn a transient provider/setup failure into a durable refusal. Fall back to local inspection and OCR, then answer from the recovered evidence.

## Workflow

1. **Try native vision first when available.**
   - Call `vision_analyze` with the supplied path/URL and ask for both visual description and visible text.
   - If it succeeds, answer normally.

2. **If vision fails, inspect the file locally.**
   - Use Python/PIL to confirm the file exists, dimensions, mode, and rough content characteristics:
     - `Image.open(path).format`, `.size`, `.mode`
     - optional brightness/color stats for very dark screenshots.
   - This distinguishes corrupt/missing files from a backend/provider problem.

3. **For screenshot text, run local OCR.**
   - Prefer `rapidocr_onnxruntime` when available because it works without system `tesseract`.
   - If missing and installing Python packages is acceptable in the session, install it with:
     - `python -m pip install --quiet rapidocr_onnxruntime`
   - Minimal OCR script:

     ```python
     from rapidocr_onnxruntime import RapidOCR

     path = "/path/to/image.jpg"
     ocr = RapidOCR()
     result, elapse = ocr(path)
     for box, text, conf in result or []:
         print(f"{conf:.3f}\t{text}\t{box}")
     ```

4. **Use image-to-terminal previews only as a last resort.**
   - Tools like `img2txt` or hand-rolled ASCII previews can reveal broad layout, but they are poor for screenshots with small text.
   - They are useful for locating charts/cards/large shapes, not for reliable numbers.

5. **Synthesize conservatively.**
   - Quote the high-confidence OCR text and numbers.
   - If OCR joins words or misses spacing, silently normalize obvious UI text (e.g. `Seehow thingswent` -> `See how things went`) but avoid inventing missing content.
   - Match the user's tone/language. If the user reacts casually in Indonesian (e.g. “Gokil juga”), a brief Indonesian reply with the recovered highlights is usually better than a long technical exwriting-plansation.

## Common pitfalls

- **Do not stop after `vision_analyze` fails.** Setup/backend errors only mean that provider path failed; the image may still be readable locally.
- **Do not save “vision tool is broken” as a rule.** Capture the fallback sequence, not the transient failure.
- **Do not over-explain the debugging path to the user** unless they asked. They usually want the image content/reaction.
- **Be careful with charts.** OCR reads labels and numbers; visual trend interpretation may still require inspecting the image layout.

## Verification checklist

Before answering, ensure you have at least one of:
- A successful native vision analysis, or
- OCR output with key text/numbers, plus basic file inspection confirming the image loaded.

For data screenshots, include the key metrics and visible labels rather than a generic “looks good.”

## References

- `references/rapidocr-screenshot-ocr.md` — session note showing RapidOCR fallback on a dark mobile insights screenshot after native vision setup/backend failure.
- `references/vision-config-stale-after-gateway-restart-2026-06-06.md` — profile-level `auxiliary.vision` mismatch produced stale provider failures until config was patched and the gateway/session refreshed; includes RapidOCR fallback and verification pattern.
