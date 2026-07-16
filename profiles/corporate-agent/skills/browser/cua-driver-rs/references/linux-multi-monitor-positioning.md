# Linux Multi-Monitor Window Positioning & Resolution

Under GNOME Shell on Wayland with multi-display setups (e.g., HDMI-2 at 0,0 and eDP-1 laptop screen at 1920,0), Xwayland windows can get positioned off-screen or stuck on a closed laptop display/secondary monitor. This file lists diagnostic and recovery steps.

## Symptoms
- Window exists in the tree but is invisible to the user.
- Workspace index in `wmctrl -l` is reported as `-1` (sticky), which happens when "Workspaces on primary display only" is enabled and the window is placed on a secondary display.
- Coordinates show x-offset is either shifted to the secondary screen boundary (e.g., 1920) or slightly off-screen (e.g., negative offset).

## Recovery Steps

### 1. Disable Maximization & Move Window
Wayland/Xwayland windows won't obey client-side movements via X11 tools if they are maximized. Remove maximization before moving:
```bash
# Remove maximization states
wmctrl -i -r <HEX_WINDOW_ID> -b remove,maximized_vert,maximized_horz

# Move to the primary screen (HDMI-2 space, usually starting at 0,0)
wmctrl -i -r <HEX_WINDOW_ID> -e 0,0,0,1920,1080
```

### 2. Send Compositor Shortcut Keys (Super + Shift + Left/Right)
If the window remains stuck on the secondary screen due to Wayland client restrictions, send keyboard events via the system keyboard emitter (like `ydotool`) to shift workspaces/monitors:
- **`Super + Shift + Left` Key Sequence (ydotool format)**: Keycode `125` (Super), `42` (Shift), `105` (Left Arrow).
```bash
ydotool key 125:1 42:1 105:1 105:0 42:0 125:0
```

### 3. Re-maximize & Activate Window
```bash
# Re-maximize on the active screen
wmctrl -i -r <HEX_WINDOW_ID> -b add,maximized_vert,maximized_horz

# Raise/Activate window
wmctrl -i -a <HEX_WINDOW_ID>
```
