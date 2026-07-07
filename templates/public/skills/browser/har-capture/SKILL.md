---
name: har-capture
description: "Capture network traffic (XHR, Fetch, WebSocket) from websites. Defaults to CloakBrowser/Chrome CDP for Galyarder/Keiya; Playwright Chromium is explicit fallback via --standalone. Saves HAR 1.2 and extracts API endpoints."
---

# HAR Capture Tool

Capture HTTP requests/responses and WebSocket frames from any website. Saves in HAR 1.2 format (importable in browser DevTools).

## When to Use

- Discovering API endpoints from SPAs/JS-heavy sites (instead of manual curl guessing)
- Capturing WebSocket traffic (real-time data, live updates)
- Recording request/response payloads for replay or analysis
- Debugging network issues on websites
- Reverse engineering API flows (auth, captcha, data submission)

## Command

```bash
harcapture <url> [options]                         # default: CloakBrowser CDP
harcapture --cdp-url <endpoint> [url] [options]
harcapture --standalone <url> [options]            # explicit Playwright fallback
```

**Default route:** CloakBrowser/Chrome CDP on `http://localhost:9222`. Playwright Chromium is only used when `--standalone` is explicit.

**Options:**
- `-o, --output <file>` — Output HAR file (default: `/home/galyarder/.hermes/profiles/galyarder/cache/har-capture/<domain>_<timestamp>.har`)
- `-f, --filter <types>` — Resource types: `xhr,fetch,ws,document,script,all` (default: `xhr,fetch,ws`)
- `--standalone` — Explicitly launch Playwright Chromium instead of CloakBrowser/Chrome CDP
- `--headless` — Run without visible browser window (`--standalone` only)
- `--wait <sec>` — Auto-close after N seconds (default: 0 = manual, press Enter to stop)
- `--cdp-url <url>` — Attach to existing browser via CDP (URL or preset name)
- `--existing-tab` — Attach to first existing tab instead of opening new one

**CDP Presets:**
- `cloakbrowser` → `http://localhost:9222`
- `camofox` is intentionally disabled: Camofox exposes REST on `9377`, not raw Chrome CDP.

## Two Modes

### CloakBrowser CDP (default)
Attaches to CloakBrowser/Chrome CDP on `http://localhost:9222`. Best default for Galyarder/Keiya because it avoids silently spawning a fresh Playwright Chromium and can preserve the stronger browser surface when Cloak is running.

```bash
# Default: open/capture via CloakBrowser CDP
harcapture 'https://target.com'

# Explicit Playwright fallback, headless + auto-close after 10s
harcapture --standalone 'https://target.com' --headless --wait 10

# Filter XHR/Fetch only (skip WS), still CloakBrowser CDP by default
harcapture 'https://target.com' -f xhr,fetch

# Capture everything including static assets
harcapture 'https://target.com' -f all

# Custom output path
harcapture 'https://target.com' -o ~/scripts/project/api-capture.har
```

### Explicit CDP Attach
Connects to an existing Chrome/Chromium browser via **raw CDP websocket** (NOT Playwright). Captures ALL traffic regardless of how navigation is triggered.

```bash
# 1. Start Chrome with CDP port
google-chrome --remote-debugging-port=9222 --no-first-run &

# 2. Attach harcapture (creates new tab with URL)
harcapture --cdp-url http://localhost:9222 'https://target.com'

# 3. Interact via raw CDP websocket, browser_cdp, or user clicks
# 4. Press Enter in harcapture terminal → stop capture

# Attach to existing tab instead of creating new one
harcapture --cdp-url http://localhost:9222 --existing-tab

# Preset shortcuts
harcapture --cdp-url cloakbrowser 'https://target.com'
```

**When to use CDP Attach:**
- Need to interact with the site (click buttons, fill forms, navigate SPA)
- Want to use a real Chrome profile (cookies, extensions)
- Server-side: launch Chrome on Xvfb with CDP, attach from terminal
- Complex multi-step flows (login → dashboard → API calls)

**CDP Attach workflow on server:**
1. `export DISPLAY=:99` (Xvfb)
2. `google-chrome --remote-debugging-port=9222 --no-first-run &`
3. `harcapture --cdp-url http://localhost:9222 'https://target.com'`
4. Interact via raw CDP websocket or `browser_cdp` tool
5. Press Enter → capture stops with all traffic recorded

**How CDP Attach works internally:**
- Connects to Chrome via raw CDP websocket (`ws://localhost:9222/devtools/...`)
- Creates new tab via `PUT /json/new?<url>` (or attaches to existing)
- Listens to CDP `Network.requestWillBeSent`, `Network.responseReceived`, `Network.loadingFinished`
- Fetches response bodies via `Network.getResponseBody`
- Captures WebSocket frames via `Network.webSocketCreated/FrameReceived/FrameSent/Closed`
- Uses `drain_events()` loop for timed capture or manual Enter stop

## Usage Patterns

```bash
# Quick API discovery (headless, 10s)
harcapture 'https://target.com' --headless --wait 10

# Interactive SPA capture (CDP attach, manual close)
harcapture --cdp-url http://localhost:9222 'https://app.com/dashboard'

# WebSocket-only capture
harcapture 'https://trading.com' -f ws --headless --wait 30

# Full capture (all resources)
harcapture 'https://target.com' -f all -o full-capture.har
```

## Workflow: API Discovery

1. Run `harcapture <url>` for CloakBrowser CDP default, or `harcapture --standalone <url>` only for disposable Playwright fallback
2. Perform actions in browser (click buttons, submit forms, navigate)
3. Press Enter to stop
4. Review extracted API summary in terminal output
5. HAR file saved — import in DevTools (Network → Import HAR) for full inspection
6. Use extracted endpoints in scripts (curl, Python requests, etc.)

## Output

**Terminal:** Live log of captured requests + API summary at the end.

**HAR file:** JSON with all request/response data:
- Request: method, URL, headers, body
- Response: status, headers, body
- WebSocket: connection URLs, frame direction (recv/sent), payload data

## WebSocket Capture

Uses CDP (Chrome DevTools Protocol) to intercept WebSocket frames:
- `[WS OPEN]` — new WS connection detected
- `[WS RECV]` — incoming frame (server → client)
- `[WS SENT]` — outgoing frame (client → server)
- `[WS CLOSE]` — connection closed

WS frames saved in HAR under `_websockets[]` with direction, data, and timestamp.

## Operating Posture

Galih corrected this tool route: CloakBrowser is the serious default for HAR/API discovery in this setup; Playwright is only a disposable fallback. Do not install extra Playwright browsers or let `harcapture <url>` silently spawn Playwright Chromium unless the user explicitly chooses `--standalone`. If a package or upstream doc is Playwright-first, adapt it to Cloak/Chrome CDP first, remove misleading Camofox-CDP presets, then keep Playwright as an opt-in fallback.

When mirroring this skill across Galyarder and Keiya/default, keep the command wrapper shared at `/home/galyarder/.local/bin/harcapture` and the executable script shared at `/home/galyarder/.hermes/scripts/har_capture.py`; profile-specific copies should not be the command target.

## Pitfalls

1. **Playwright route creep** — `harcapture <url>` must default to CloakBrowser/Chrome CDP on `127.0.0.1:9222`. Use `--standalone` for Playwright Chromium. `--headless` without `--standalone` should fail fast instead of implying CDP can be headless.

2. **Camofox is not raw CDP** — Camofox exposes REST on `9377`, not Chrome DevTools Protocol. Keep `camofox` disabled/rejected as a `--cdp-url` preset, even if upstream examples list it.

3. **Event listener syntax** — Playwright's CDP session does NOT support `@cdp.on()` decorator syntax. Use direct method calls: `cdp.on('Network.webSocketFrameReceived', handler)`, NOT `@cdp.on('Network.webSocketFrameReceived')`. The decorator pattern causes `TypeError` at runtime.

4. **`asyncio.sleep` in event handlers** — CDP event handlers run in the event loop. Using `await asyncio.sleep()` inside a handler blocks all other event processing. Use fire-and-forget patterns or queue events for later processing.

5. **WebSocket capture requires CDP `Network.enable`** — Before intercepting WS frames, must call `await cdp.send('Network.enable')`. Without this, no WS events fire.

6. **Chrome `/json/new` requires PUT** — Chrome 148+ rejects GET requests to `/json/new` with "Using unsafe HTTP verb GET". Must use `PUT` method: `urllib.request.Request(url, method="PUT")` or `curl -X PUT`. Used internally by `--cdp-url` to create new tabs.

7. **Playwright `page.on("response")` misses raw CDP traffic** — In CDP attach mode, if navigation is triggered via raw CDP websocket (`Page.navigate`), Playwright's response listener does NOT see those responses. The CDP attach mode uses raw CDP `Network.*` events instead, which capture ALL traffic regardless of navigation source.

8. **SPA routing may not trigger API calls** — Client-side routing (React Router, Next.js, etc.) navigates without server requests. Navigating to `/puzzle`, `/memory`, `/leaderboard` on an SPA may produce zero XHR/Fetch traffic. API calls only happen on user interactions (button clicks, form submissions, data fetches). Don't assume navigation = API calls.

## Limitations

- Playwright Chromium only in explicit `--standalone` mode (no Firefox/WebKit)
- CDP attach works with any Chromium-based browser (Chrome, Edge, Brave, CloakBrowser)
- WebSocket capture requires CDP session (works in both standalone and attach modes)
- Response body capture may fail for large responses or streaming
- Some sites detect Playwright — use CloakBrowser CDP for serious/stealth capture, not standalone Playwright
- Filter applies at resource type level, not URL pattern
- Camofox REST API (`http://localhost:9377`) does NOT support CDP — use CloakBrowser/Brave/Chrome CDP directly

## File Location

Script: `/home/galyarder/.hermes/scripts/har_capture.py`
Command wrapper: `/home/galyarder/.local/bin/harcapture`
References: `references/cdp-protocol.md`, `references/api-discovery-patterns.md`, `references/cloak-first-har-capture-2026-05-25.md`
