# HyperFrames Kokoro TTS Local Setup — 2026-05-14

## Context

During Company video-stack work, HyperFrames `tts` was tested on the Default Hermes profile. The CLI exposed voices, but generation failed until Python dependencies and Kokoro assets were prepared.

## What Worked

Voice listing is a lightweight smoke test and does not prove synthesis readiness:

```bash
hyperframes tts --list
```

Actual synthesis needs Python packages visible to the same Python executable that `hyperframes` finds with `which python3` / `which python`:

```bash
python3 -m pip install kokoro-onnx soundfile
```

If running inside the Hermes agent virtualenv, `pip install --user ...` can fail with:

```text
Can not perform a '--user' install. User site-packages are not visible in this virtualenv.
```

Use plain `python3 -m pip install kokoro-onnx soundfile` in that environment.

## Asset Cache

HyperFrames stores Kokoro assets under:

```text
~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx
~/.cache/hyperframes/tts/voices/voices-v1.0.bin
```

First synthesis downloads:

- `kokoro-v1.0.onnx` — about 311 MB
- `voices-v1.0.bin` — about 27 MB

Observed source URLs in HyperFrames 0.6.6:

```text
https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

## Slow/Interrupted Download Recovery

If HyperFrames' internal downloader stalls or a command timeout leaves a `.tmp`/partial model file, do not repeatedly rerun `hyperframes tts` blindly. Use a resumable external download and place the finished file exactly where HyperFrames expects it:

```bash
CACHE="$HOME/.cache/hyperframes/tts"
mkdir -p "$CACHE/models" "$CACHE/voices"

# Preserve any partial download from HyperFrames before resuming.
[ -f "$CACHE/models/kokoro-v1.0.onnx.tmp" ] && \
  mv -f "$CACHE/models/kokoro-v1.0.onnx.tmp" "$CACHE/models/kokoro-v1.0.onnx.part"
[ -f "$CACHE/models/kokoro-v1.0.onnx" ] && \
  mv -f "$CACHE/models/kokoro-v1.0.onnx" "$CACHE/models/kokoro-v1.0.onnx.part"

curl -L --fail --continue-at - --retry 10 --retry-delay 5 --connect-timeout 30 \
  -o "$CACHE/models/kokoro-v1.0.onnx.part" \
  "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"

mv -f "$CACHE/models/kokoro-v1.0.onnx.part" "$CACHE/models/kokoro-v1.0.onnx"

curl -L --fail --continue-at - --retry 10 --retry-delay 5 --connect-timeout 30 \
  -o "$CACHE/voices/voices-v1.0.bin" \
  "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
```

Then verify synthesis with a short smoke file:

```bash
cat > tts-smoke.txt <<'EOF'
Company turns human intent into infrastructure.
EOF
hyperframes tts tts-smoke.txt --voice am_michael --output tts-smoke.wav
stat -c '%n %s bytes' tts-smoke.wav
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 tts-smoke.wav
```

## Routing Notes

- English narration: HyperFrames Kokoro is the default local/no-key path.
- Indonesian narration: Kokoro may work as stylized English-voice pronunciation, but expect weaker Bahasa Indonesia quality; consider Edge TTS, Piper, Coqui, or another Indonesian-capable TTS if natural pronunciation matters.
- `hyperframes tts --list` only proves CLI availability. Always generate a short WAV and inspect duration before saying TTS is ready.
