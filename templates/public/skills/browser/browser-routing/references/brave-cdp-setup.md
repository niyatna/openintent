# Brave CDP setup for Galyarder

Use when Galih wants Hermes/Galyarder/Keiya to operate the real Brave browser via Chrome DevTools Protocol (CDP).

## Observed state, 2026-05-08

Before setup:

- Brave Origin Nightly was running without `--remote-debugging-port`.
- Common CDP ports `9222`, `9223`, `9224`, `9229`, `34567` refused connections.

After Galih closed browsers, the process list was clean and ports were closed.

## Launch command

Use the real Brave Origin Nightly profile and bind CDP only to loopback:

```bash
BRAVE=/home/galyarder/.local/bin/brave-browser
PROFILE_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly
"$BRAVE" \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$PROFILE_DIR" \
  --restore-last-session
```

When launched from Hermes terminal, use `terminal(background=true)` rather than shell-level `nohup`, `&`, or `disown` so Hermes can track the process.

## Verification

```bash
curl -fsS http://127.0.0.1:9222/json/version
curl -fsS http://127.0.0.1:9222/json/list
ps -eo pid,ppid,comm,args | grep -Ei 'brave.*remote-debugging|remote-debugging-port=9222' | grep -v grep
```

Expected `/json/version` shape:

```json
{
  "Browser": "Chrome/148.0.7778.96",
  "Protocol-Version": "1.3",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/..."
}
```

Observed tabs included:

- `https://www.tiktok.com/` with title `TikTok - Make Your Day`
- extension/background targets such as uBlock Origin and Volume Master

## Safe smoke test

Open and close a harmless tab without touching user accounts:

```python
import urllib.request, urllib.parse, json, time
base='http://127.0.0.1:9222'
req=urllib.request.Request(base + '/json/new?' + urllib.parse.quote('https://example.com', safe=':/?&=%'), method='PUT')
with urllib.request.urlopen(req, timeout=5) as r:
    tab=json.loads(r.read().decode())
time.sleep(2)
with urllib.request.urlopen(base + '/json/list', timeout=5) as r:
    tabs=json.loads(r.read().decode())
# verify title Example Domain, then close
urllib.request.urlopen(base + '/json/close/' + tab['id'], timeout=5).read()
```

Observed smoke result:

```text
OPENED https://example.com/
FOUND_AFTER_OPEN title: Example Domain
CLOSE_RESULT Target is closing
```

## Safety posture

- Treat Brave CDP as Galih's cockpit: real session, real accounts, real browser state.
- Do not run bulk automation here unless Galih explicitly asks and accepts the blast radius.
- Avoid reading or printing cookies, tokens, localStorage, extension internals, or private page content unless required for the task.
- Prefer Camofox isolated profiles for bulk auth/account testing and gstack Playwright for repeatable QA.
- Keep `--remote-debugging-address=127.0.0.1`; do not bind CDP to `0.0.0.0`.

## Common pitfalls

- Launching Brave with CDP while an existing Brave process owns the profile can cause flags to be ignored. Ask Galih to close all Brave windows first, or use a dedicated profile.
- `brave-browser --version` reports Brave Origin Nightly `148.1.92.24`, while `/json/version` reports Chrome protocol/browser version `148.0.7778.96`. This is normal.
- Hermes terminal may reject foreground commands with shell-level background wrappers. Use the terminal tool's `background=true` option.
