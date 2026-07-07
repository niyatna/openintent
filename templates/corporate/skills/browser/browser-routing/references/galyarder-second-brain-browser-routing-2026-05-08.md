# Galyarder second-brain browser routing session — 2026-05-08

Use this as the concrete reference for the browser-stack decision that came out of the Camofox/Brave/gstack testing session.

## User corrections captured

- Do not treat Camofox as the universal Hermes browser. It is an automation lab, not Galih's lived browser.
- For second-brain/operator work, Brave CDP is the default human-facing cockpit because Galih's real tabs, sessions, music, and browser life are in Brave.
- Do not moralize generic platform ToS for local/disposable/owned-platform experiments. Frame real downside: credentials, account lock, rate limits, data corruption, malware, IP reputation, legal exposure, and blast radius.
- When the user asks for action, route and act. Keep the routing line short; no defensive lecture.

## Final routing doctrine

```text
Brave CDP = default lived/human browser cockpit
Camofox = isolated auth/session automation lab
gstack Playwright = deterministic QA/dev/visual evidence
Browserbase = normal cloud fallback
BrowserUse = secondary cloud option when Browserbase is unsuitable
Hermes native browser = quick inspection only
```

## Config state to preserve

Both Galyarder and default/Keiya should prefer Brave CDP for human-facing browser work and Browserbase for cloud fallback:

```yaml
browser:
  cdp_url: http://127.0.0.1:9222
  cloud_provider: browserbase
  camofox:
    managed_persistence: false
```

`managed_persistence: false` keeps Camofox disposable/clean for lab automation. Brave is the persistent cockpit.

If `CAMOFOX_URL` remains in `.env`, remember that it is only for explicit Camofox lab routes. Do not let it override the routing doctrine mentally.

## Brave CDP launch and verification

Launch Brave Origin Nightly with CDP bound to loopback:

```bash
BRAVE=/home/galyarder/.local/bin/brave-browser
PROFILE_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly
"$BRAVE" \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$PROFILE_DIR" \
  --restore-last-session
```

Verify:

```bash
curl -fsS http://127.0.0.1:9222/json/version
curl -fsS http://127.0.0.1:9222/json/list
python3 scripts/brave-cdp.py status
python3 scripts/brave-cdp.py list
```

`DevTools listening on ws://127.0.0.1:9222/devtools/browser/...` is the success signal.

Nonfatal warnings observed during successful launch:

```text
Gtk-WARNING Theme parser error
ERROR:profile_attributes_storage.cc Failed to PNG encode the image
ERROR:startup_browser_creator_impl.cc No browser window found for startup
Fontconfig error: Cannot load default config file
ERROR:services/network/p2p/socket_manager.cc Failed to resolve stun.l.google.com
```

These do not mean CDP failed if `/json/version` works.

## YouTube/music smoke test

Request: play `Aziz Hedra - Somebody's Pleasure`.

Correct route: Brave CDP.

Observed successful state after navigating to the official music video:

```text
URL: https://www.youtube.com/watch?v=cMqfTJdbXpY
Title: Aziz Hedra - Somebody's Pleasure (Official Music Video) - YouTube
video.paused: false
video.readyState: 4
video.muted: false
video.duration: ~237s
```

Useful CDP JS check:

```javascript
(() => {
  const v = document.querySelector('video');
  return JSON.stringify({
    url: location.href,
    title: document.title,
    video: v ? {
      paused: v.paused,
      currentTime: v.currentTime,
      readyState: v.readyState,
      volume: v.volume,
      muted: v.muted,
      duration: v.duration,
      src: !!v.currentSrc
    } : null
  });
})()
```

## Camofox visual pitfall

Hermes managed Camofox screenshots are not desktop visual truth. During the Ledger test, Camofox loaded assets but stayed on `Initializing Workspace...`, and the screenshot looked misaligned compared with the user's desktop Brave view. Treat this as tool mismatch first, not app proof.

When a visible Camofox check is required, launch manual headful `camoufox-bin` without `-headless` and without `-juggler-pipe`; however GNOME/Wayland may block desktop screenshots (`grim` unsupported, GNOME Screenshot `AccessDenied`). For visual QA, prefer Brave/manual or gstack Playwright.

## Skill-library consolidation note

`browser-routing` is the class-level umbrella. Any Galyarder-specific browser routing skill should act as an alias or be absorbed here; do not keep parallel doctrines that can diverge.
