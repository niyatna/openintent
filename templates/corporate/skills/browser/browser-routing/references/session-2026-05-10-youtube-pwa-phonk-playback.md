# Session 2026-05-10 — Brave YouTube PWA phonk playback

Use this as a concrete playback recipe for Discord/Keiya relay requests like “puter lagu/phonk buat kerja” where Galih expects actual YouTube playback, not only a recommendation.

## What happened

- Initial mistake: routing through Spotify/recommendation and saying playback was unavailable. Correction: Galih wanted Brave CDP / Brave YouTube PWA using the runtime/memory setup.
- CDP was not reachable on `127.0.0.1:9222`, but the Brave YouTube PWA was already available.
- Target PWA:
  - Profile: `Profile 3`
  - App id: `agimnkijcaahngcdmfeangaknmldooml`
  - Window class: `crx_agimnkijcaahngcdmfeangaknmldooml`
  - MPRIS player observed: `brave.instance685596`

## Selection pattern

For “one track”:

```bash
# Use web search or YouTube search for the exact track.
# Example result used: DVRST - Close Eyes
```

For “1 hour / sekitar 60 menit”:

```bash
yt-dlp --skip-download --no-warnings \
  --print '%(title)s|||%(channel)s|||%(duration_string)s' \
  'https://www.youtube.com/watch?v=I6Ch7JeEQ04'
```

Observed good output:

```text
shadow work • dark phonk mix for unstoppable focus (1 hour)|||iron focus|||1:12:13
```

Prefer `yt-dlp --print` over piping JSON into `python3`; the pipe-to-interpreter pattern can trigger a security approval warning and is unnecessary for title/channel/duration.

## Launch pattern

```bash
URL='https://www.youtube.com/watch?v=I6Ch7JeEQ04&autoplay=1'
APP_ID='agimnkijcaahngcdmfeangaknmldooml'
timeout 8s env \
  HOME=/home/galyarder \
  XDG_CONFIG_HOME=/home/galyarder/.config \
  CHROME_USER_DATA_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly \
  /opt/brave.com/brave-origin-nightly/brave-origin-nightly \
  "--profile-directory=Profile 3" \
  --app-id="$APP_ID" \
  "--app-launch-url-for-shortcuts-menu-item=$URL"
```

Activate and nudge only if stopped:

```bash
WIN=$(wmctrl -lx | awk 'BEGIN{IGNORECASE=1} /crx_agimnkijcaahngcdmfeangaknmldooml/ && /shadow work|dark phonk|unstoppable focus/ {print $1; exit}')
[ -n "${WIN:-}" ] && wmctrl -ia "$WIN" || true
STATUS=$(playerctl -p brave.instance685596 status 2>/dev/null || true)
if [ "$STATUS" != "Playing" ]; then
  playerctl -p brave.instance685596 play 2>/dev/null || playerctl play 2>/dev/null || true
fi
```

## Multi-window pitfall

Opening a new URL in the PWA can leave the old YouTube PWA window alive. MPRIS metadata may continue to show the old video even when the new PWA window exists. If the user asked to switch tracks/mixes, close the old matching PWA window and keep the new one before verifying:

```bash
for id in $(wmctrl -lx | awk 'BEGIN{IGNORECASE=1} /crx_agimnkijcaahngcdmfeangaknmldooml/ && /Close Eyes/ {print $1}'); do
  wmctrl -ic "$id" || true
done
```

Then verify both window and playback metadata:

```bash
wmctrl -lx | grep -Ei 'crx_agimnkijcaahngcdmfeangaknmldooml|YouTube' || true
for p in $(playerctl -l 2>/dev/null || true); do
  printf '[%s] ' "$p"
  playerctl -p "$p" status 2>/dev/null || true
  printf ' — '
  playerctl -p "$p" metadata --format '{{title}} — {{artist}}' 2>/dev/null || true
  printf '\n'
done
```

Successful observed verification:

```text
0x01002a0c -1 crx_agimnkijcaahngcdmfeangaknmldooml.brave-origin  ... shadow work • dark phonk mix for unstoppable focus (1 hour) - YouTube
[brave.instance685596] Playing — shadow work • dark phonk mix for unstoppable focus (1 hour) — iron focus
```

## Reply format

For these Discord thread requests, stay terse:

```text
playing: shadow work • dark phonk mix for unstoppable focus (1 hour) — iron focus
```

If it fails:

```text
gagal: <short concrete reason>
```

Do not return a recommendation list when the task is to play one item.
