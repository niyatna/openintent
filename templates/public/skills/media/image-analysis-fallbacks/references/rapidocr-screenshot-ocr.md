# RapidOCR fallback for screenshot OCR

## Context

A user sent a local JPEG screenshot and reacted casually in Indonesian (“Gokil juga”). Native `vision_analyze` failed because the configured provider path was not usable in that session. The image itself was valid: JPEG, 576×1280, RGB, mostly dark UI.

## Useful fallback sequence

1. Confirm the image can be opened locally:

```python
from PIL import Image
from pathlib import Path

p = Path('/path/to/image.jpg')
print('exists', p.exists(), 'size_bytes', p.stat().st_size if p.exists() else None)
im = Image.open(p)
print('format', im.format, 'size', im.size, 'mode', im.mode)
```

2. If no OCR engine is present, install a Python-only OCR option:

```bash
python -m pip install --quiet rapidocr_onnxruntime
```

3. Run OCR:

```python
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
result, elapse = ocr('/path/to/image.jpg')
print('elapsed', elapse)
for item in result or []:
    print(item)
```

## Example recovered text from the session

High-confidence OCR from a dark mobile analytics screenshot included:

- `Insights`
- `Your weekly recap is ready`
- `See how things went last week`
- `Ringkasan`
- `7 hari`
- `Tayangan` → `43,5 rb`
- Chart labels: `15rb`, `10rb`, `5rb`, `1 Jan`, `4 Jun`
- `Interaksi` → `353`
- `Pengikut` → `174`
- `Konten populer`
- `wd hasil mining hermes`

## Response pattern

For casual Indonesian reactions, keep the reply short and mirror the vibe. Example:

> Wkwk iya, gokil sih 😄 Dari screenshot-nya: 7 hari dapat 43,5 rb tayangan, 353 interaksi, dan 174 pengikut. Konten populer-nya “wd hasil mining hermes”.

Do not narrate all failed tool attempts unless the user asks how you inspected it.
