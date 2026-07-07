# Faithful logo/image edit verification — 2026-06-01

Use this reference when Galih asks to edit an existing raster/logo/image while preserving the original identity.

## Trigger pattern

- User points at an existing logo/image and says a specific visible element should change.
- The edit must preserve the original: colors, text, central motif, background, layout, and symbol meaning.
- User corrects outputs as “double/ghost line”, “looks like ads/two triangles”, “not like original”, or “can you see?”

## Lesson from the CV logo triangle session

The requested change was narrow: keep the original logo and make the **existing gold triangle’s top apex protrude outward like the lower left/right corners**.

Failures happened when the workflow treated it as a redesign/generation task:

- overlaying a new triangle on top of the old one created visible double/ghost lines;
- top-only caps looked like patches, not part of the original triangle;
- full AI regeneration produced clean-looking logos but materially changed the crown, geometric background, ring details, and symbol language;
- a single vision pass that says “pass” can miss the user’s actual requirement if it does not compare against the original.

## Correct workflow

1. Restate the user’s exact visual invariant before editing:
   - what must change;
   - what must not change;
   - what visual defect would fail the output.
2. For faithful edits, keep the original as the authority. Do not accept a clean reinterpretation unless the user explicitly accepts redesign.
3. Produce or request a side-by-side comparison: original vs candidate.
4. Verify against a checklist, not vibes:
   - original colors retained;
   - original text spelling and legibility retained;
   - original central motif/background/ring details retained;
   - requested geometry changed visibly;
   - no ghost/double lines, pasted caps, smeared/inpainted text, or AI-symbol drift.
5. If raster overlay/inpainting keeps causing artifacts, stop calling it done. State the blocker and move to vector/manual redraw of the specific element.
6. When reporting, separate:
   - **faithful minimal edit** = same logo, one requested change;
   - **clean reinterpretation** = acceptable only as a candidate if user/father wants a redesigned cleaner version.

## Practical edit outlines for this class

For a raster logo where one stroked geometric element must move:

- preferred: trace/redraw that element as a vector layer, remove the old stroke cleanly, and export;
- acceptable preview: show a rough candidate only if labeled as rough/non-final;
- avoid: drawing a second stroke over the old stroke, because it often creates ghost/double lines;
- avoid: image-generation “faithful edit” as the final proof unless side-by-side comparison confirms no material symbol drift.

## User-facing phrasing

Use blunt status language:

- `belum layak dikirim` when visible defects remain;
- `ini clean reinterpretation, bukan faithful edit` when AI changed the logo;
- `yang bener: manual/vector redraw bagian itu doang` when the raster path keeps failing.

Do not over-explain after repeated visual corrections. Give the failing defect and the next exact move.