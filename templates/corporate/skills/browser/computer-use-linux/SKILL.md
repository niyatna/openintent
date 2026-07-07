---
name: computer-use-linux
description: Use when Galyarder or Keiya needs Linux desktop observation or control through the OS-home computer-use-linux MCP server, including AT-SPI app trees, GNOME/Wayland window targeting, ydotool input, and Hermes MCP wiring.
version: 1.0.0
author: Galyarder Labs + agent-sh
license: MIT
metadata:
  hermes:
    category: browser
    tags: [linux, desktop-control, mcp, accessibility, wayland, gnome, ydotool]
    related_skills: [browser-routing, native-mcp, hermes]
---

# computer-use-linux

## Overview

**Routing preference:** prefer official Hermes native `computer_use` / `cua-driver` whenever it is installed and passes `hermes computer-use status`/doctor. Use this `computer-use-linux` stack as the Linux-specific fallback/compatibility route when native `computer_use` is unavailable, not installed, or blocked.

`computer-use-linux` is installed once in OS home and shared by profiles. The active binary path is `/home/galyarder/.local/bin/computer-use-linux`; the COSMIC helper is `/home/galyarder/.local/bin/computer-use-linux-cosmic`; source/repo checkout is `/home/galyarder/tools/computer-use-linux`.

Use this skill as the profile-local fallback access/runbook layer for both Galyarder and Keiya. Do **not** create a profile-local home or duplicate binary install under `/home/galyarder/.hermes/profiles/*/home`.

## When to Use

Use when:
- the agent needs local Linux GUI observation/control beyond browser DOM tools;
- a task needs AT-SPI app trees, desktop app lists, screenshots, windows, clicks, typing, scroll, keypress, or semantic accessibility actions;
- configuring Hermes MCP server `computer-use-linux`;
- diagnosing GNOME Wayland desktop-control readiness.

Do not use for normal web QA if `browser`, `Camofox`, Brave CDP, or gstack Playwright is the right surface. Do not use mutating desktop actions against external/public/high-blast-radius apps without Galih's explicit command.

## Current Install State

- Repo: `/home/galyarder/tools/computer-use-linux`
- Installed binaries: `/home/galyarder/.local/bin/computer-use-linux`, `/home/galyarder/.local/bin/computer-use-linux-cosmic`
- Installed version inspected from repo/package: `0.2.3`
- System package installed: `ydotool`
- AT-SPI setup has been run and `doctor` reports `can_build_accessibility_tree=true`
- GNOME Shell extension files were installed by `setup-window-targeting`, but GNOME must log out/in before the extension DBus backend is served
- `ydotoold` user unit exists at `/home/galyarder/.config/systemd/user/ydotoold.service`, but input is blocked until `/dev/uinput` permission is fixed and the service can start

## Fast Commands

Always force OS home/path:

```bash
export HOME=/home/galyarder
export PATH=/home/galyarder/.local/bin:/home/galyarder/.cargo/bin:$PATH
```

Readiness:

```bash
computer-use-linux doctor | jq .readiness
computer-use-linux apps | jq '.[0:10]'
computer-use-linux windows | jq .
computer-use-linux state | jq '.[0:20]'
```

Safe setup/idempotent checks:

```bash
computer-use-linux setup
computer-use-linux setup-window-targeting
systemctl --user status ydotoold.service --no-pager
```

MCP config entry for Hermes profiles:

```yaml
mcp_servers:
  computer-use-linux:
    command: /home/galyarder/.local/bin/computer-use-linux
    args: ["mcp"]
    enabled: true
    timeout: 120
    connect_timeout: 30
```

Hermes registers tools as `mcp_computer_use_linux_<tool>` and runtime toolset `mcp-computer-use-linux` after profile restart.

## Procedure

1. Run `scripts/computer-use-linux-status.sh` first.
2. If `can_build_accessibility_tree=false`, run `computer-use-linux setup`, restart target GUI apps, then rerun doctor.
3. If `can_query_windows=false` on GNOME Wayland, run `computer-use-linux setup-window-targeting`; if it says GNOME Shell is not serving the DBus API, Galih must log out/in before exact window targeting works.
4. If `can_send_development_input=false`, check `/dev/uinput`, ydotool package, and `ydotoold.service`. Do not claim input control works until the socket `/run/user/1000/.ydotool_socket` exists and doctor flips true.
5. For read-only observation, `apps` and AT-SPI `state` can still work even when window/input are blocked.
6. For mutating desktop action, identify the target app/window first, then prefer semantic selector/index from `state` or MCP `get_app_state`; coordinates are fallback only.
7. After any mutating action, read back state with `state`, `windows`, app-specific state, or screenshot.

## Remaining Local Blockers

If sudo is available, fix input with:

```bash
sudo tee /etc/udev/rules.d/60-uinput.rules >/dev/null <<'RULE'
KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"
RULE
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=misc --attr-match=name=uinput || true
sudo modprobe uinput || true
sudo chgrp input /dev/uinput
sudo chmod 660 /dev/uinput
systemctl --user reset-failed ydotoold.service || true
systemctl --user restart ydotoold.service
computer-use-linux doctor | jq .readiness
```

If sudo asks for a password and none is provided, stop and report the blocker. Do not loop.

Window targeting on GNOME Wayland requires a logout/login after `setup-window-targeting` if the extension was newly installed.

## Safety Boundaries

Read-only: `doctor`, `apps`, `windows`, `state` without input.

Mutating/high attention: MCP `click`, `drag`, `scroll`, `press_key`, `type_text`, `perform_action`, `set_value`, plus setup commands that change GNOME accessibility, GNOME extension state, systemd user units, udev, or `/dev/uinput` permissions.

Ask Galih before destructive/public/account/money actions performed through the desktop.

## Verification Checklist

- [ ] `command -v computer-use-linux` returns `/home/galyarder/.local/bin/computer-use-linux`
- [ ] `computer-use-linux doctor | jq .readiness` was run fresh
- [ ] AT-SPI app listing works with `computer-use-linux apps`
- [ ] If claiming window targeting, `can_query_windows=true` and `windows` returns real windows
- [ ] If claiming input, `can_send_development_input=true` and ydotool socket exists
- [ ] If claiming Hermes MCP availability, profile config contains server entry and Hermes has been restarted/tested
