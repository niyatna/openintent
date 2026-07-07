# GNOME desktop control quick reference

Use this note when Galih asks whether the agent can control his Linux/GNOME desktop directly (volume, media, windows, apps).

## Observed environment

- Desktop: GNOME (`XDG_CURRENT_DESKTOP=GNOME`, `DESKTOP_SESSION=gnome`)
- Display/session variables observed: `DISPLAY=:0`, `WAYLAND_DISPLAY=wayland-0`, `XDG_SESSION_TYPE=wayland`
- Useful installed tools:
  - `wpctl` for PipeWire/WirePlumber default audio sink volume
  - `pactl` fallback for PulseAudio/PipeWire
  - `playerctl` for MPRIS browser/player controls and metadata
  - `wmctrl` for XWayland-visible window listing/focus/close
  - `gsettings` for GNOME settings when applicable
- `xdotool` may not be installed/usable; do not rely on it as the first path on this setup.

## Volume control

Read default output volume:

```bash
wpctl get-volume @DEFAULT_AUDIO_SINK@
```

Set absolute volume:

```bash
wpctl set-volume @DEFAULT_AUDIO_SINK@ 25%
```

Decrease/increase relative volume:

```bash
wpctl set-volume @DEFAULT_AUDIO_SINK@ 10%-
wpctl set-volume @DEFAULT_AUDIO_SINK@ 10%+
```

Mute/unmute/toggle mute:

```bash
wpctl set-mute @DEFAULT_AUDIO_SINK@ 1
wpctl set-mute @DEFAULT_AUDIO_SINK@ 0
wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
```

Fallbacks if `wpctl` is missing:

```bash
pactl set-sink-volume @DEFAULT_SINK@ -10%
pactl get-sink-volume @DEFAULT_SINK@
amixer sset Master 10%-
```

## Media control

Inspect MPRIS players and current title:

```bash
playerctl -l
for p in $(playerctl -l 2>/dev/null || true); do
  echo "[$p] $(playerctl -p "$p" status 2>/dev/null || true) — $(playerctl -p "$p" metadata --format '{{title}} — {{artist}}' 2>/dev/null || true)"
done
```

Play/pause a specific player when known:

```bash
playerctl -p brave.instance685596 pause
playerctl -p brave.instance685596 play
```

Pitfall: a single Brave MPRIS player can represent the currently active Brave media source, not necessarily the window you want. If TikTok PWA and YouTube PWA are both present, verify by title/window class before nudging playback.

## Window control

List windows with geometry/class/title:

```bash
wmctrl -lGx
```

Focus a window by id:

```bash
wmctrl -ia 0x01001b79
```

Close only a target window by class/title, avoiding other Brave profiles/PWAs:

```bash
TARGET=$(wmctrl -lx | awk 'BEGIN{IGNORECASE=1} /Shape of My Heart.*YouTube/ && $3 !~ /^crx_/ {print $1; exit}')
[ -n "$TARGET" ] && wmctrl -ic "$TARGET"
```

## Reporting rule

For desktop-control tasks, report the concrete before/after evidence: volume number, window id/class/title, process, or `playerctl` metadata. Do not claim control based only on issuing a command.
