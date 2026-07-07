# Brave real-browser media fallback

Use this note when Galih asks to play music/video in Brave and CDP is not available.

## Session signal

2026-05-09: User asked: `Puterin music di brave shape of my heart dari backstreet boy`.

Expected route: Brave real browser, because this is a lived media task.

## What happened

- `http://127.0.0.1:9222/json/version` refused: Brave was running without CDP.
- Existing Brave process had the real OS profile at `/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly`.
- Hermes profile `$HOME` was `/home/galyarder/.hermes/profiles/galyarder/home`, so `/home/galyarder/.local/bin/brave-browser URL` defaulted to a profile-local Brave config and started a separate Brave instance instead of controlling the lived session.
- `gio open URL` did not visibly open the target in the real browser in this state.
- `xdg-open` was mis-called as `xdg-open open URL`; correct syntax is `xdg-open URL`, but for Brave here the explicit env path was more reliable.

## Reliable fallback command

When CDP is down but a normal Brave window is already open, open the URL into the real OS Brave session with explicit environment:

```bash
timeout 8s env \
  HOME=/home/galyarder \
  XDG_CONFIG_HOME=/home/galyarder/.config \
  CHROME_USER_DATA_DIR=/home/galyarder/.config/BraveSoftware/Brave-Origin-Nightly \
  /home/galyarder/.local/bin/brave-browser --new-tab 'https://www.youtube.com/watch?v=OT5msu-dap8&autoplay=1'
```

Expected output can include:

```text
Opening in existing browser session.
```

## Verification

Use window list and MPRIS, not only process creation:

```bash
wmctrl -lx | tail -20
playerctl -l
for p in $(playerctl -l 2>/dev/null || true); do
  echo "[$p] $(playerctl -p "$p" status 2>/dev/null || true) — $(playerctl -p "$p" metadata --format '{{title}} — {{artist}}' 2>/dev/null || true)"
done
```

In the session, after opening the URL, `playerctl` showed:

```text
[brave.instance685596] Playing — Backstreet Boys - Shape Of My Heart (Official HD Video) — BackstreetBoysVEVO
```

## Operational rule

For simple media playback, do not force-close or relaunch Galih's Brave just to enable CDP. If CDP is down, use the explicit-env URL-open fallback and verify with `playerctl`. Relaunch with CDP only when the task needs tab inspection/control beyond opening a URL.
