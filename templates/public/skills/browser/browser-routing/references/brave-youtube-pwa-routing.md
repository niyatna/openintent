# Brave YouTube PWA routing

Use this note when Galih asks to play/open YouTube through his Brave-installed YouTube PWA instead of a normal Brave tab.

## Observed YouTube PWA identity

From the real OS user's Brave Origin Nightly profile:

- Profile: `Profile 3`
- App name: `YouTube`
- App id: `agimnkijcaahngcdmfeangaknmldooml`
- StartupWMClass / window class: `crx_agimnkijcaahngcdmfeangaknmldooml`
- Launcher: `/home/galyarder/.local/share/applications/brave-agimnkijcaahngcdmfeangaknmldooml-Profile_3.desktop`
- Exec from launcher:
  ```bash
  /opt/brave.com/brave-origin-nightly/brave-origin-nightly "--profile-directory=Profile 3" --app-id=agimnkijcaahngcdmfeangaknmldooml
  ```

Nearby comparison from same session:

- TikTok PWA app id: `nlalbmkafgmoifbeooblidblkmlhhpnc`
- TikTok StartupWMClass: `crx_nlalbmkafgmoifbeooblidblkmlhhpnc`

## How to discover PWA identity next time

List active PWA windows:

```bash
wmctrl -lx | grep -Ei 'crx_|youtube|music|brave'
```

List installed Brave PWA desktop entries:

```bash
grep -R "Name=\|Exec=\|StartupWMClass=" \
  /home/galyarder/.local/share/applications/brave-*-Profile_3.desktop
```

Machine-readable extraction:

```bash
python3 - <<'PY'
from pathlib import Path
for p in Path('/home/galyarder/.local/share/applications').glob('brave-*-Profile_3.desktop'):
    txt=p.read_text(errors='ignore')
    if 'YouTube' in txt or 'youtube' in txt.lower():
        print(p)
        for line in txt.splitlines():
            if line.startswith(('Name=','Exec=','StartupWMClass=')):
                print(' ', line)
PY
```

## Launching the YouTube PWA

Prefer the desktop launcher or explicit OS-user environment so Hermes profile `$HOME` does not create a wrong/session-local Brave context:

```bash
timeout 8s env \
  HOME=/home/galyarder \
  XDG_CONFIG_HOME=/home/galyarder/.config \
  CHROME_USER_DATA_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly \
  /opt/brave.com/brave-origin-nightly/brave-origin-nightly \
  "--profile-directory=Profile 3" \
  --app-id=agimnkijcaahngcdmfeangaknmldooml
```

Then verify the PWA window:

```bash
wmctrl -lx | grep 'crx_agimnkijcaahngcdmfeangaknmldooml'
```

## Playing a specific video in PWA context

Best path when CDP is unavailable:

1. Open/activate YouTube PWA.
2. For a specific URL, prefer Chromium's app shortcut launch argument; plain `--app-id ... "$URL"` can open only the PWA shell/home instead of navigating to the video:
   ```bash
   URL='https://www.youtube.com/watch?v=-osvYFAWkrs&autoplay=1'
   timeout 8s env \
     HOME=/home/galyarder \
     XDG_CONFIG_HOME=/home/galyarder/.config \
     CHROME_USER_DATA_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly \
     /opt/brave.com/brave-origin-nightly/brave-origin-nightly \
     "--profile-directory=Profile 3" \
     --app-id=agimnkijcaahngcdmfeangaknmldooml \
     "--app-launch-url-for-shortcuts-menu-item=$URL"
   ```
3. Verify whether the window class is PWA (`crx_agim...`) or normal Brave (`brave-origin-nightly.brave-origin`) before claiming success.
4. Use `playerctl` only as verification/nudge; it controls the current Brave MPRIS player and can affect the wrong active media source if TikTok or another PWA is active.
5. If focus is needed, activate the PWA window first with `wmctrl -ia <window_id>` before sending input.
6. To close a previously opened normal Brave YouTube window without killing another Brave profile/PWA, identify the non-`crx_` window by title/class and close only that window ID:
   ```bash
   TARGET=$(wmctrl -lx | awk 'BEGIN{IGNORECASE=1} /Shape of My Heart.*YouTube/ && $3 !~ /^crx_/ {print $1; exit}')
   [ -n "$TARGET" ] && wmctrl -ic "$TARGET"
   ```

When CDP is needed, Brave/PWA must already be launched with `--remote-debugging-port`; you cannot attach CDP to an already-running Brave process that was launched without it.

## Verification

Confirm both window target and playback target:

```bash
wmctrl -lx | grep -Ei 'crx_agimnkijcaahngcdmfeangaknmldooml|YouTube'
for p in $(playerctl -l 2>/dev/null || true); do
  echo "[$p] $(playerctl -p "$p" status 2>/dev/null || true) — $(playerctl -p "$p" metadata --format '{{title}} — {{artist}}' 2>/dev/null || true)"
done
```

Do not claim the PWA route worked unless the active/target window class or title proves the YouTube PWA was used, not only a normal Brave tab. When switching from one YouTube PWA video to another, stale PWA windows can keep the old MPRIS metadata alive; close only the old matching PWA window(s), activate the new one, and then verify again. See `references/session-2026-05-10-youtube-pwa-phonk-playback.md`.
