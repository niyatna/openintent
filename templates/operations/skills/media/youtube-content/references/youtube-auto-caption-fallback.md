# YouTube auto-caption fallback with yt-dlp

Use when `youtube-transcript-api` is missing, returns no transcript, or the video only has auto-generated captions.

## Reliable fallback

Run from `/tmp` or another neutral directory so `uv run` does not parse the current repo's `pyproject.toml` or mutate project environments.

```bash
cd /tmp
URL='https://youtu.be/VIDEO_ID'
yt-dlp --skip-download --dump-json "$URL" > /tmp/video-meta.json
python3 - <<'PY'
import json
m=json.load(open('/tmp/video-meta.json'))
print('title:', m.get('title'))
print('channel:', m.get('channel') or m.get('uploader'))
print('duration:', m.get('duration'))
print('subtitles:', sorted((m.get('subtitles') or {}).keys())[:20])
print('auto_captions:', sorted((m.get('automatic_captions') or {}).keys())[:40])
PY

yt-dlp --skip-download --write-auto-subs --sub-lang 'id,en' --sub-format 'vtt' \
  -o 'VIDEO_ID.%(ext)s' "$URL"
```

If `youtube-transcript-api` is needed ad hoc, avoid installing into the project:

```bash
cd /tmp
uv run --no-project --with youtube-transcript-api python /path/to/fetch_transcript.py "$URL" --timestamps
```

## VTT cleanup pattern

YouTube VTT auto-captions include inline timestamp tags and repeated growing cues. Strip tags and deduplicate before summarizing:

```python
import html, re
from pathlib import Path
vtt = Path('/tmp/VIDEO_ID.id.vtt').read_text(errors='replace')
blocks = re.split(r'\n\s*\n', vtt)
entries = []
for block in blocks:
    lines = block.strip().splitlines()
    for i, line in enumerate(lines):
        if '-->' in line:
            start = line.split('-->')[0].strip()
            raw = ' '.join(lines[i+1:])
            raw = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>', ' ', raw)
            raw = re.sub(r'</c>|<[^>]+>', ' ', raw)
            raw = re.sub(r'\s+', ' ', html.unescape(raw)).strip()
            if raw:
                entries.append((start, raw))
            break
```

## Pitfalls

- `youtube-transcript-api` can say "No transcript found" even when `yt-dlp` can download auto-captions.
- `uv run` inside the Hermes source checkout may parse Hermes `pyproject.toml` and build/install project dependencies. Use `cd /tmp` plus `--no-project` for one-off transcript tools.
- English captions may 429 while Indonesian captions succeed; use available language metadata instead of assuming failure.
- Web page summaries are useful as a fallback, but for user-facing summaries prefer actual transcript/captions when available.
