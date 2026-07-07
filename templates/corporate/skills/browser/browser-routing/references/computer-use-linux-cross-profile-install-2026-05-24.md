# computer-use-linux cross-profile install pattern — 2026-05-24

## Why this exists

Galih asked to analyze and install `agent-sh/computer-use-linux` for both Galyarder and Keiya profiles, with one OS-level tool install and profile-specific skills/supporting access layers. The session exposed a reusable pattern for Linux desktop-control MCP servers and cross-profile Hermes setup.

## Correct architecture

- Install shared binaries/tools once under OS home (`/home/galyarder`), not under any profile home.
- Keep profile-specific access as skills/config under each profile root.
- Do not recreate profile-local `home` directories for shared tool installs.
- For commands that depend on user-level tools, force OS home:
  ```bash
  export HOME=/home/galyarder
  export PATH=/home/galyarder/.local/bin:/home/galyarder/.cargo/bin:$PATH
  ```

## computer-use-linux install route

Observed repo/package version during the session: `0.2.3`.

Expected binary locations after OS-home install:

```bash
/home/galyarder/.local/bin/computer-use-linux
/home/galyarder/.local/bin/computer-use-linux-cosmic
```

If npm global install with `--prefix /home/galyarder/.local` stalls during `postinstall`, switch to direct GitHub release assets with sha256 verification instead of waiting silently. The npm package downloads the same release assets.

## Profile MCP config

Add the same MCP server entry to both relevant profile configs when both profiles need access:

```yaml
mcp_servers:
  computer-use-linux:
    command: /home/galyarder/.local/bin/computer-use-linux
    args: ["mcp"]
    enabled: true
    timeout: 120
    connect_timeout: 30
```

Then verify explicitly per profile:

```bash
hermes --profile galyarder mcp test computer-use-linux
hermes --profile default mcp test computer-use-linux
hermes --profile galyarder mcp list
hermes --profile default mcp list
```

Expected discovery at the time of this session: connected, 16 tools discovered.

## Skill support pattern

For a shared OS-home tool used by multiple profiles:

1. Create or update a class-level/profile access skill in the right category.
2. Mirror the skill to the other profile only when it is a universal capability and the user asked for both profiles.
3. Include a small status script under `scripts/` when repeated verification is likely.
4. Include current known blockers in the skill as readiness state, not permanent negative claims.

For `computer-use-linux`, the profile skill created was `browser/computer-use-linux`, with `scripts/computer-use-linux-status.sh`.

## Readiness distinction

Separate these states in reports:

- MCP server availability: `hermes ... mcp test` connects and tools are discovered.
- Read-only desktop observation: `computer-use-linux doctor`, `apps`, and AT-SPI `state` work.
- Window targeting: `can_query_windows=true` and `windows` returns real windows.
- Input control: `can_send_development_input=true`, `ydotoold` active, and `/run/user/$UID/.ydotool_socket` exists.

Do not collapse partial readiness into “fully working.” Report exact gates.

## Known setup gates from this session

These are setup gates to verify/fix when needed, not permanent failures:

- AT-SPI became ready after `computer-use-linux setup`.
- GNOME Wayland window targeting may require `computer-use-linux setup-window-targeting` plus logout/login before the extension DBus backend appears.
- ydotool input needs `ydotool`, a running user `ydotoold.service`, `/dev/uinput` permissions, and often logout/login or udev permission refresh.
- If sudo asks for a password and none is provided, stop after one failed attempt and report the blocker instead of looping.

## Speed/reporting lesson

For long installs/downloads/builds in Discord, avoid long silent foreground waits. If a step may exceed ~60–90 seconds, prefer a background process with completion notification, or send a terse progress/blocker update before continuing. When interrupted or corrected for slowness, immediately summarize verified state and continue the nearest safe action; no apology speech.
