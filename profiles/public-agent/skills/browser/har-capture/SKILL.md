---
name: har-capture
description: "Capture network traffic (XHR, Fetch, WebSocket) from websites using the Camofox browser agent. Saves in HAR 1.2 format."
version: 1.0.0
author: Company
license: MIT
---

# HAR Capture

Capture HTTP requests, responses, and WebSocket frames from any website using the Camofox browser agent. All captures are saved in standard HAR 1.2 format (importable into any browser's DevTools Network tab).

---

## 1. When to Use

- **API Discovery**: Intercept XHR and Fetch calls from single-page applications (SPAs) or JS-heavy sites to map endpoints.
- **WebSocket Audits**: Capture raw WebSocket connection payloads, frame directions, and messages.
- **Traffic Analysis**: Record full request and response headers and payloads.
- **Debug Routing**: Analyze traffic patterns generated during automated agent tasks.

---

## 2. Command Options

Use the `harcapture` CLI utility:

```bash
harcapture <url> [options]
```

### Options
- `-o, --output <file>` — Output HAR file path (defaults to `~/.hermes/profiles/default/cache/har-capture/<domain>_<timestamp>.har`).
- `-f, --filter <types>` — Resouce filters: `xhr,fetch,ws,document,script,all` (default: `xhr,fetch,ws`).
- `--wait <sec>` — Automatically close the session after N seconds (default is 0: wait for manual Enter key to stop).
- `--existing-tab` — Attach to the currently active tab inside the browser agent session.

---

## 3. Workflow: API Discovery

1. Run `harcapture <url>` pointing to the target address.
2. The Camofox browser agent loads the page. Perform necessary interactions (login, navigation, button clicks).
3. Press **Enter** in the terminal to stop capturing.
4. The utility saves the HAR file and prints a summary of discovered API endpoints block to stdout.
5. Import the resulting `.har` file into any browser Developer Tools (Network Tab -> Import HAR) for full inspection of request payloads and response bodies.

---

## 4. Troubleshooting & Pitfalls

- **Bypassing Captchas**: Camofox handles stealth fingerprinting dynamically. If a captcha is encountered, let the session remain open and do not trigger rapid reload loops.
- **WebSocket Frame Interception**: WebSocket capture requires the devtools protocol to be active. Ensure `Network.enable` is configured.
- **SPA Client Routing**: Page changes on modern frameworks (React / Vue) may happen purely client-side without firing network requests. Intercept actions rather than page URLs.
