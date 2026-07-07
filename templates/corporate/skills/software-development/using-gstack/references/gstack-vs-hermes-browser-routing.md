# gstack vs Hermes browser routing

Use when Galih asks which browser stack is using Playwright, which browser to keep/remove, or why Hermes screenshots differ from gstack/desktop.

## Runtime attribution observed

gstack browse uses Playwright Chromium headless shell in the Galyarder profile.

Verification command:

```bash
export GSTACK_ROOT="$HOME/gstack/.hermes/skills/gstack"
export GSTACK_BIN="$HOME/gstack/bin"
export GSTACK_BROWSE="$HOME/gstack/browse/dist"
B="$HOME/gstack/browse/dist/browse"
"$B" status
"$B" goto https://example.com
"$B" text | head -40
ps -eo pid,ppid,comm,args \
  | grep -Ei 'gstack|browse/dist|chrome-headless|chromium|playwright|ms-playwright' \
  | grep -v grep || true
```

Observed output:

```text
Status: healthy
Mode: launched
URL: https://example.com/
bun run .../gstack/browse/src/server.ts
.../.cache/ms-playwright/chromium_headless_shell-1208/.../chrome-headless-shell --headless --mute-audio --remote-debugging-pipe
```

## Keep/remove decision rule

- Brave Origin Nightly: keep as the human/manual browser and media truth.
- gstack Playwright Chromium: keep for QA, screenshots, visual/design review, deployment checks, and `$B` automation.
- Camofox/Camoufox: keep for Hermes native browser tools from Telegram, but prefer on-demand service unless always-ready browser tools are required.
- Hermes `agent-browser`: keep as internal Hermes dependency.
- BrowserOS: remove candidate if no active workflow needs it; it overlaps with Brave, gstack, and Camofox.
- Browserbase/BrowserUse: keep dormant as fallback, not default, if cloud browser fallback is still useful.

## Screenshot fidelity rule

Do not use Camofox headless screenshots for desktop visual QA. Use gstack headed/headless Playwright screenshots for automated visual evidence, or Brave/manual for human desktop truth.

## Cleanup warning

Do not delete `$HOME/.cache/ms-playwright` while gstack browse is kept. It contains Chromium/headless shell needed by gstack and will be re-downloaded if removed.
