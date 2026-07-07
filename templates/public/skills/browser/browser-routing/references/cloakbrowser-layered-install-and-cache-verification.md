# CloakBrowser layered install + cache verification

Use this when Galih asks whether CloakBrowser is installed, broken, missing, or safe to clean.

## Core lesson

CloakBrowser has separate layers:

1. **Python package / venv** — wrapper API and CLI can exist and import successfully.
2. **CLI wrappers** — usually OS-home wrappers such as `~/.local/bin/cloakbrowser-galyarder` and `~/.local/bin/cloakbrowser-python`.
3. **Chromium binary cache** — the actual stealth browser under `~/.cache/cloakbrowser/chromium-<version>/chrome`.
4. **User/profile data** — separate browser profile/session dirs when a workflow supplies `user_data_dir` or `HOME`.

`cloakbrowser info` can show the expected version/path even when the binary is missing. The decisive field is `Installed: True/False`, plus direct executable-file check.

## Verification ladder

Use OS home explicitly unless a workflow intentionally overrides it:

```bash
OS_HOME=/home/galyarder

# Package / wrapper layer
[ -x "$OS_HOME/.local/bin/cloakbrowser-galyarder" ] && echo wrapper-ok
[ -x "$OS_HOME/.local/bin/cloakbrowser-python" ] && echo py-wrapper-ok
[ -x "$OS_HOME/.local/share/cloakbrowser-venv/bin/python" ] && \
  "$OS_HOME/.local/share/cloakbrowser-venv/bin/python" -m pip show cloakbrowser

# Binary layer
HOME="$OS_HOME" "$OS_HOME/.local/bin/cloakbrowser-galyarder" info
find "$OS_HOME/.cache/cloakbrowser" -maxdepth 3 -type f -name chrome -perm -111 -print 2>/dev/null
```

Interpretation:

- package import ok + `Installed: False` = wrapper installed, Chromium binary missing / cache cleared.
- cache directory exists but is empty = binary cache was removed or cleared, not package uninstall.
- wrapper missing but binary exists = PATH/venv wrapper issue, not necessarily browser loss.

## Repair

If the package exists but binary is missing:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/cloakbrowser-galyarder install
HOME=/home/galyarder /home/galyarder/.local/bin/cloakbrowser-galyarder info
```

For long downloads, use Hermes background process or give a terse progress note in Discord. Do not run a long silent foreground install.

## Cleanup warning

Treat `~/.cache/cloakbrowser` as a **runtime browser binary cache**, not disposable language/package cache. `cloakbrowser clear-cache` or broad cache cleanup can delete the installed Chromium binary and force a redownload. Only clear it when Galih explicitly wants browser binaries removed or redownloaded.
