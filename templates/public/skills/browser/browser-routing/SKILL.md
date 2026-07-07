---
name: browser-routing
description: Use when choosing configuring or troubleshooting which browser stack should handle a task across Brave CDP Hermes native browser Camofox gstack Playwright BrowserOS or cloud browsers.
metadata:
  hermes:
    category: browser
---

# Browser Routing

## Core rule

There is no single primary browser/desktop-control stack for every task. Route by usecase and blast radius.

For Galih's lived workflow, **Brave CDP is the default human-facing browser**. For dedicated Keiya/Galyarder owned-agent browser sessions, **CloakBrowser persistent profiles are now the primary route**. For full desktop control, **official Hermes native `computer_use` / `cua-driver` wins when installed and verified**; `computer-use-linux` is the Linux-specific fallback/compatibility route while native is unavailable. Camofox is a legacy/fallback automation lab unless a platform skill still has a verified Camofox-only CRUD flow. gstack Playwright is the QA machine. Cloud browser is fallback isolation. Hermes native browser is quick inspection.

## Routing map

- **Brave CDP / real Brave session**: default for human/browser-life tasks: YouTube/music, logged-in web work, continuing real tabs, desktop visual truth, high-trust account workflows Galih explicitly wants in his real browser. If CDP is down and the task only needs opening media/URL, use the real-browser explicit-env fallback instead of forcing a relaunch.
- **CloakBrowser**: primary route for Keiya/Galyarder owned-agent persistent browser profiles, Google login/session capture, high-friction login, and serious HAR/API discovery. Use `/home/galyarder/.hermes/private/browser-profiles/agents/<owner>/<service>-cloakbrowser` plus the account's normal cookie path. Load `cloakbrowser-browser` for exact commands. If Galih explicitly says `pake CloakBrowser`, do not fall back to controlling his real Brave/desktop browser unless he approves; repair/use CloakBrowser or state the precise live gate (for example reCAPTCHA).
- **Camofox/Camoufox**: legacy/fallback isolated automation lab and disposable role/session testing. Use it only when the current platform skill has a verified Camofox-only flow that CloakBrowser has not replaced yet, or when Cloak is blocked.
- **gstack Playwright Chromium**: deterministic QA/dev browser: flow tests, deployment checks, visual/design review evidence, screenshots, repeatable bug reports. Note: If the backend has no local Chrome/Chromium binaries cached under `~/.cache/ms-playwright/`, you may need to explicitly execute `playwright install chromium` inside the terminal before running a screenshot or browser test.
- **Cloud browser**: remote clean room/fallback: local browser broken, region/IP isolation, remote session needed, or intentionally off-machine execution. In this setup, Browserbase is the normal cloud fallback; BrowserUse is the secondary option when Browserbase is unsuitable or fails.
- **Hermes native browser tool**: quick inspection: open page, read title/text/DOM, lightweight click/form checks when fidelity is not the point.
- **BrowserOS**: dormant/remove candidate unless Galih names a specific workflow it wins.

## Decision triggers

```text
"putar music", "youtube", "open in my browser", "akun gua", "lanjutin tab" -> Brave CDP / real Brave session
"YouTube PWA", "ytb PWA", "ytb pws", "PWA lu" -> Brave YouTube PWA (crx_agimnkijcaahngcdmfeangaknmldooml) when available
"di Brave" + media request -> browser route, not Spotify, unless Spotify is explicitly named
"bulk auth", "account.txt", "banyak akun", "test role/session", "agent-owned login" -> CloakBrowser persistent profile first; Camofox fallback only if platform skill still has a Camofox-specific verified flow or Cloak is blocked
"owned-agent high-friction login", "autonomous login anti-bot", "CloakBrowser", "Browser Profile Manager" -> CloakBrowser persistent profile via `cloakbrowser-browser` + account/platform operator skill
"HAR capture", "API discovery with browser traffic", "capture request/response", "WebSocket capture" -> CloakBrowser/Chrome CDP first; Playwright only with explicit standalone fallback
"Threads/Instagram CRUD", "post/delete/repost media", "Meta cookies" -> platform operator; prefer CloakBrowser profile when the skill has been updated/verified, otherwise use its current verified Camofox flow
"QA", "cek flow", "visual", "screenshot", "deploy", "find bugs" -> gstack Playwright
"clean remote", "region", "local gagal", "cloud" -> cloud browser
"cek web cepat", "ambil teks/meta" -> Hermes native browser
```

When routing is non-obvious, state the route in one line before acting:

```text
route: gstack Playwright, karena ini flow QA dan butuh screenshot reliable.
```

Keep this line short. Do not turn routing into a lecture.

## Brave CDP posture

Brave CDP touches Galih's real browser state. Use it as the cockpit, not the lab.

Do:
- use it for media, lived browsing, and explicit account workflows;
- keep CDP bound to `127.0.0.1`;
- verify `http://127.0.0.1:9222/json/version` before claiming CDP access;
- if CDP is down but Brave is already running, use the real desktop/browser-launch route instead of trying CDP;
- avoid dumping cookies, tokens, localStorage, or extension internals into chat.

Don't:
- use Brave CDP for bulk account testing when CloakBrowser/Camofox can isolate it;
- modify high-value account state without explicit command;
- confuse Brave CDP with Hermes native browser, gstack browse, or ordinary Brave URL launching.

### Fast Brave media route

For `puterin music`, `youtube`, and similar human-facing media tasks, speed beats CDP purity:

1. If the user says `di Brave`, `YouTube`, `ytb`, asks for browser/PWA playback, or a Discord relay says “puterin”, do not route through Spotify first and do not stop at a recommendation.
2. Pick one item that matches the constraint; for `1 hour` requests, prefer a mix/loop around 60 minutes and verify title/channel/duration with `yt-dlp --print '%(title)s|||%(channel)s|||%(duration_string)s' "$URL"` when available.
3. If the exact YouTube URL is known or found via one quick search, open it directly in Brave or the YouTube PWA target.
4. Use the OS user's real Brave environment, not Hermes profile `$HOME`:
   ```bash
   env HOME=/home/galyarder \
     XDG_CONFIG_HOME=/home/galyarder/.config \
     CHROME_USER_DATA_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly \
     /home/galyarder/.local/bin/brave-browser --new-tab "$URL"
   ```
5. Verify with `wmctrl -lx` for the YouTube/PWA window and `playerctl -l` / `playerctl metadata` for playback.
6. If autoplay leaves the player stopped, activate the correct YouTube/PWA window before sending input. `playerctl play` may toggle the wrong Brave MPRIS source when TikTok or another PWA is active.
7. If switching videos/mixes in the YouTube PWA, close stale matching PWA windows before final verification; otherwise MPRIS can keep reporting/playing the old video while the new PWA window exists.
8. In Discord thread replies for media execution, answer only `playing: judul — channel/artist` or `gagal: alasan` unless the user asks for detail.

Only use CDP for this route if Brave was already launched with `--remote-debugging-port` and `/json/version` is reachable. See `references/session-2026-05-10-youtube-pwa-phonk-playback.md` for a concrete phonk/1-hour YouTube PWA recipe and stale-window pitfall.

### Brave YouTube PWA route

Galih's observed Brave YouTube PWA:

- profile: `Profile 3`
- app id: `agimnkijcaahngcdmfeangaknmldooml`
- window class: `crx_agimnkijcaahngcdmfeangaknmldooml`
- launcher: `/home/galyarder/.local/share/applications/brave-agimnkijcaahngcdmfeangaknmldooml-Profile_3.desktop`

When the user says `YouTube PWA`, `ytb PWA`, `ytb pws`, or asks whether the Brave PWA can be used, target this PWA before opening a normal Brave tab. For direct video URLs, launch the PWA with `--app-launch-url-for-shortcuts-menu-item=$URL`; plain `--app-id ... "$URL"` may open only the PWA home/shell. See `references/brave-youtube-pwa-routing.md` for discovery, launch, close-only-target-window, and verification commands.

Setup and verification details: see `references/brave-cdp-setup.md`. Use `scripts/brave-cdp.py` for status/list/open/close helpers.

## CloakBrowser posture

CloakBrowser is the primary owned-agent browser profile route. It uses OS-home install/cache only and private per-agent persistent profiles.

Canonical Google profile/cookie paths:

```text
Keiya profile:     /home/galyarder/.hermes/private/browser-profiles/agents/keiya/google-cloakbrowser
Galyarder profile: /home/galyarder/.hermes/private/browser-profiles/agents/galyarder/google-cloakbrowser
Keiya cookies:     /home/galyarder/.hermes/private/credentials/agents/keiya/google/cookies.json
Galyarder cookies: /home/galyarder/.hermes/private/credentials/agents/galyarder/google/cookies.json
```

Use `cloakbrowser-browser` for install checks, Browser Profile Manager interpretation, Google login/session capture, cookie storage, and process cleanup.

## Camofox posture

Camofox is not the default human browser. It is no longer the primary Keiya/Galyarder owned-agent profile route. Use it for legacy verified platform flows, disposable role/session labs, and fallbacks where CloakBrowser is blocked.

Known pitfalls:
- Camofox/YouTube playback can fail because codecs/media support differ.
- Hermes managed screenshots can differ from desktop truth.
- GNOME/Wayland may block desktop screenshot capture of manual headful Camofox.
- Shared Camofox ports can conflict across Keiya/Galyarder; use separate ports for parallel-safe automation.

For Camofox-specific setup and failure modes, load `camofox-browser`.

## gstack posture

gstack browse is the Playwright Chromium route. Use it when evidence and repeatability matter more than using Galih's real session.

For gstack setup and `$B` commands, load `using-gstack` or the specific gstack skill (`gstack`, `qa`, `open-gstack-browser`).

## Linux desktop-control MCP route

For Linux desktop observation/control beyond browser DOM automation, use the `computer-use-linux` skill. This route is for AT-SPI app trees, GNOME/Wayland window targeting, ydotool input, screenshots, and Hermes MCP wiring.

Cross-profile rule: install shared desktop-control binaries once under OS home, then add profile-specific skills/config for Galyarder and Keiya/default. Do not recreate profile-local `home` directories or duplicate binaries under profile homes. See `references/computer-use-linux-cross-profile-install-2026-05-24.md` for the reusable cross-profile install/readiness pattern.

Report readiness in layers: MCP connected, read-only AT-SPI observation, window targeting, and input control are separate gates. Do not call the stack fully ready if only MCP discovery works.

## Active process cleanup

If a prior test left a manual headful CloakBrowser, Camoufox, or other browser process running, clean it up before declaring the stack ready unless Galih explicitly wants to inspect it. Do not kill Brave unless Galih asks or it is the CDP-launched process for this task.

## Common mistakes

- Treating `browser.cloud_provider = camofox` as the answer to every browser task.
- Using Camofox headless screenshots as proof of desktop visual bugs.
- Using Brave CDP for bulk automation that should be isolated.
- Using gstack screenshots to infer Hermes native browser behavior.
- Starting cloud browser by default when local route is enough.
- Over-explaining the routing decision after Galih asked for a direct action.

## Session references

- `references/galyarder-second-brain-browser-routing-2026-05-08.md`: concrete session notes for the Brave-as-cockpit decision, Browserbase fallback config, Camofox persistence choice, YouTube smoke test, and Camofox visual pitfall.
- `references/brave-real-browser-media-fallback.md`: fallback for opening media in Galih's real Brave session when CDP is down, including explicit `HOME`/`XDG_CONFIG_HOME` env and `playerctl` verification.
- `references/brave-youtube-pwa-routing.md`: Brave YouTube PWA identity, `--app-launch-url-for-shortcuts-menu-item=$URL` launch pattern, safe close-only-target-window commands, and PWA verification.
- `references/gnome-desktop-control.md`: GNOME/PipeWire/MPRIS/window-control quick reference for volume, media, and window operations.
- `../autonomous-ai-agents/hermes/references/session-2026-05-09-browser-media-and-desktop-control.md`: session-specific Brave/YouTube PWA media playback, explicit OS-user env, safe window closing, and GNOME volume-control notes.
- `references/computer-use-linux-cross-profile-install-2026-05-24.md`: cross-profile install/readiness pattern for `agent-sh/computer-use-linux`, including OS-home single install, profile MCP config, profile skill mirroring, and partial-readiness reporting.

## CloakBrowser install/cache verification

When asked whether CloakBrowser is installed or missing, verify the layers separately: Python package/venv, wrapper, Chromium binary cache, and `cloakbrowser info`. A package import or wrapper existing is not proof that the Chromium binary exists; `Installed: False` plus an empty `~/.cache/cloakbrowser` means the binary cache was cleared, not that the package was uninstalled. Keep `~/.cache/cloakbrowser` out of broad “safe cache” cleanup unless Galih explicitly wants browser binaries removed/redownloaded. See `cloakbrowser-browser` and `references/cloakbrowser-layered-install-and-cache-verification.md`.

## Termux / Ubuntu proot STB route

For Android TV/STB installs running Hermes inside Ubuntu proot, especially when Ubuntu reports `armv7l` / `armhf`, prefer cloud browser routes such as Firecrawl over local Playwright/agent-browser Chromium. A `npx agent-browser install --with-deps` / Chromium install failure after choosing Firecrawl usually means the setup hook tried an unnecessary local-browser install; it does not prove Firecrawl is broken.

- `references/cloakbrowser-layered-install-and-cache-verification.md`.\n- `references/cloakbrowser-layered-install-and-cache-verification.md`: layered verification for CloakBrowser package/wrapper/cache status.\n- `references/termux-proot-stb-firecrawl-routing-2026-06-11.md`: low-resource Termux + Ubuntu proot STB route, Firecrawl-vs-local-Chromium separation, gateway/model/platform layer checks, same-WiFi custom provider trap, and thin-edge-node resource posture.\n\n## Same-Origin Dashboard Proxying & Auth Routing\nWhen proxying developer dashboards (such as Galyarder Design, Paperclip, or 9Router) through same-origin tunnels (e.g. Telegram Mini App proxy):\n- **Cookie Path Scoping**: Do not prepend custom subpaths (like `/p/target/`) to `Set-Cookie` path specs for Better-Auth backends. Session cookies must stay scoped to `Path=/` so the browser sends them on absolute `/auth` and `/api` requests.\n- **Deter Token Auto-Injection**: Avoid automatically embedding system/board tokens (`Bearer ${token}`) into browser-facing proxy requests. Doing so logs the user into a headless system agent context, showing a blank onboarding screen. Let the browser handle transparent cookie sessions.\n- **WebSocket Upgrade Verification**: Raw request headers in Node `upgrade` listeners are unsafe. Always wrap headers/URL check with optional chaining (`req.headers?.cookie`, `req.originalUrl?.startsWith`) to prevent server crashes on socket attempts.\n- **Resource Scope Exclusions**: Guard common assets (like `/icons/`, `/favicon`, `/manifest`) from candidate scope hijacking. If a request lacks design/paperclip referrers, let it fall through (`next()`) to static file local rendering.\n- For detailed step-by-step auth proxying playbooks, see `references/same-origin-dashboard-proxying-and-auth.md`.\n\n## Verification checklist

Before finalizing a browser-routing task:

- [ ] Named or implied route matches the task class.
- [ ] Verified the actual runtime/process/port, not just memory.
- [ ] Used Brave CDP only when real browser state is appropriate.
- [ ] Used CloakBrowser/Camofox/gstack/cloud when isolation or repeatability mattered.
- [ ] For CloakBrowser status, separated wrapper/package presence from Chromium binary-cache presence.
- [ ] Reported concrete evidence: URL, title, process, port, screenshot path, command output, or `cloakbrowser info` result.
