# Vision config stale after profile auxiliary patch — 2026-06-06

## Trigger

Use this note when a user sends images, `vision_analyze` fails with a provider/config error, and the active profile's `auxiliary.vision` config was recently changed.

## What happened

- A user image failed through `vision_analyze` with `No credentials for provider: antigravity`.
- Local config inspection showed the active Galyarder profile still had `auxiliary.vision.model: antigravity/gemini-3-pro-preview`, while the default/Keiya config used `agy/gemini-3.5-flash-high`.
- The config was patched via Hermes config CLI to match Keiya:
  - `hermes --profile galyarder config set auxiliary.vision.model agy/gemini-3.5-flash-high`
- A fresh direct runtime invocation of `tools.vision_tools.vision_analyze_tool` under `HERMES_HOME=/home/galyarder/.hermes/profiles/galyarder` succeeded.
- The chat-session `vision_analyze` wrapper still failed once with the stale provider until the gateway/session was restarted.
- After gateway restart, `vision_analyze` returned `success: true` on a new screenshot.

## Durable lesson

Do **not** harden a transient provider/config error into a durable refusal like “vision tool is broken.” The right pattern is:

1. Fall back to local inspection/OCR so the user still gets an answer.
2. Inspect the live active profile config path and `auxiliary.vision` values.
3. If config is wrong, patch via Hermes config CLI rather than direct file edit when config files are protected.
4. Verify the fresh runtime path directly.
5. If the chat wrapper still uses stale config, say it needs gateway/session refresh; after restart, retest the actual `vision_analyze` tool.

## Fallback OCR used in this session

RapidOCR ONNX Runtime was effective for screenshots when native vision failed:

```python
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
result, elapse = ocr('/path/to/screenshot.jpg')
for box, text, conf in result or []:
    print(f'{conf:.3f}\t{text}')
```

This is best for UI/text-heavy screenshots. It reads visible text but does not fully replace visual reasoning.
