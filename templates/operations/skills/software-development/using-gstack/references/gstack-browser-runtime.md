# gstack browse runtime attribution

Use when distinguishing gstack browse from Hermes native browser tools, BrowserOS, Brave, or Camofox.

## Verified in Galyarder profile, 2026-05-08

Command path:

```bash
B="$HOME/gstack/browse/dist/browse"
```

Smoke test:

```bash
export GSTACK_ROOT="$HOME/gstack/.hermes/skills/gstack"
export GSTACK_BIN="$HOME/gstack/bin"
export GSTACK_BROWSE="$HOME/gstack/browse/dist"
B="$HOME/gstack/browse/dist/browse"
"$B" status
"$B" goto https://example.com
"$B" text | head -40
"$B" status
ps -eo pid,ppid,comm,args \
  | grep -Ei 'gstack|browse/dist|chrome-headless|chromium|playwright|ms-playwright' \
  | grep -v grep || true
```

Observed output summary:

```text
Status: healthy
Mode: launched
URL: https://example.com/
```

Browser/server processes:

```text
bun run /home/galyarder/.hermes/profiles/galyarder/home/gstack/browse/src/server.ts
/home/galyarder/.hermes/profiles/galyarder/home/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell --headless --mute-audio --remote-debugging-pipe ...
```

Conclusion: gstack browse uses its own Bun daemon plus Playwright Chromium headless shell. It is separate from Hermes native browser tools, which may route to Camofox depending on `browser.cloud_provider` and `CAMOFOX_URL`.

## Short answer pattern

If Galih says “si gstack itu yang pake playwright kan?”, answer:

```text
iya. gstack browse = Playwright Chromium/headless shell. Hermes native browser sekarang beda stack kalau config-nya Camofox.
```
