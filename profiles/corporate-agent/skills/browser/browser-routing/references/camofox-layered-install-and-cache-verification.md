# Camofox layered install + cache verification

Use this when Owner asks whether Camofox is installed, broken, missing, or safe to clean.

## Core lesson

Camofox has separate layers:

1. **Python package / venv** — wrapper API and CLI can exist and import successfully.
2. **CLI wrappers** — usually OS-home wrappers such as `~/.local/bin/camofox-default` and `~/.local/bin/camofox-python`.
3. **Chromium binary cache** — the actual stealth browser under `~/.cache/camofox/chromium-<version>/chrome`.
4. **User/profile data** — separate browser profile/session dirs when a workflow supplies `user_data_dir` or `HOME`.

`camofox info` can show the expected version/path even when the binary is missing. The decisive field is `Installed: True/False`, plus direct executable-file check.

## Verification ladder

Use OS home explicitly unless a workflow intentionally overrides it:

```bash
OS_HOME=~/.hermes

# Package / wrapper layer
[ -x "$OS_HOME/.local/bin/camofox-default" ] && echo wrapper-ok
[ -x "$OS_HOME/.local/bin/camofox-python" ] && echo py-wrapper-ok
[ -x "$OS_HOME/.local/share/camofox-venv/bin/python" ] && \
  "$OS_HOME/.local/share/camofox-venv/bin/python" -m pip show camofox

# Binary layer
HOME="$OS_HOME" "$OS_HOME/.local/bin/camofox-default" info
find "$OS_HOME/.cache/camofox" -maxdepth 3 -type f -name chrome -perm -111 -print 2>/dev/null
```

Interpretation:

- package import ok + `Installed: False` = wrapper installed, Chromium binary missing / cache cleared.
- cache directory exists but is empty = binary cache was removed or cleared, not package uninstall.
- wrapper missing but binary exists = PATH/venv wrapper issue, not necessarily browser loss.

## Repair

If the package exists but binary is missing:

```bash
HOME=~/.hermes ~/.hermes/.local/bin/camofox-default install
HOME=~/.hermes ~/.hermes/.local/bin/camofox-default info
```

For long downloads, use Hermes background process or give a terse progress note in Discord. Do not run a long silent foreground install.

## Cleanup warning

Treat `~/.cache/camofox` as a **runtime browser binary cache**, not disposable language/package cache. `camofox clear-cache` or broad cache cleanup can delete the installed Chromium binary and force a redownload. Only clear it when Owner explicitly wants browser binaries removed or redownloaded.
