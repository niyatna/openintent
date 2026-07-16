---
name: camofox-browser
description: "Install, verify, configure, and operate the Camofox stealth browser (persistent profiles, cookies, headless/headed sessions)."
version: 1.0.0
author: Company
license: MIT
tags: [browser, camoufox, stealth, scraping, crawler, automation, cookies, cdp]
platforms: [linux, macos, windows]
---

# Camofox Stealth Browser Skill

Guidelines and exact commands for running, verifying, and repairing the Camofox stealth browser (based on Camoufox) under dedicated agent-owned profiles.

---

## 1. When to Use
- Spawning a stealth browser for owned-agent accounts (such as X, Threads, GWS)
- Performing headless/headed sessions requiring anti-fingerprinting and proxying
- Capturing HAR traffic or capturing session cookies securely
- Troubleshooting browser crashes, missing binaries, or launcher wrapper errors

---

## 2. Core Concepts & Directory Structure
Camofox isolation relies on specific user data directories mapped per agent profile:

```text
~/.hermes/private/browser-profiles/agents/<profile>/
  default-camofox/                  # User data directory (cache/localstorage)
  default-camofox-cookies.json     # Decrypted session cookies
```
Keep raw user profiles and cookies secured (mode `600`/`700`).

---

## 3. Installation & Verification

The installation has separate layers: Python API wrapper, CLI wrappers, and the Chromium binary cache.

### Verification Ladder
Always run this verification before assuming Camofox is ready:
```bash
# 1. Check venv and wrapper package
[ -x ~/.hermes/.local/bin/camofox-default ] && echo "Wrapper installed"
[ -d ~/.hermes/.local/share/camofox-venv ] && echo "Venv ready"

# 2. Check binary cache status
HOME=~/.hermes ~/.hermes/.local/bin/camofox-default info
```
If the command output says `Installed: False`, the CLI is present but the Chromium binary is missing.

### Repair & Reinstall
If the Chromium binary is missing or cache got cleared:
```bash
HOME=~/.hermes ~/.hermes/.local/bin/camofox-default install
```
Always run downloads using a background process or check the progress. Do not lock the main execution channel on long downloads.

---

## 4. Headless & Headed Run Patterns

When automating, prioritize headless CDP connection first. If targeted anti-bot measures require a headed interface, enable headed mode only if a local display or Xvfb matches.

### Custom CDP Launcher Example
```python
import subprocess
import time

# Launching via CLI wrapper with remote debugging
cmd = [
    "~/.hermes/.local/bin/camofox-default",
    "--headless",
    "--remote-debugging-port=9222",
    "--user-data-dir=~/.hermes/private/browser-profiles/agents/default/default-camofox"
]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)  # Wait for socket handshake
```

---

## 5. Common Pitfalls

- **Stale Singleton Lock**: If an aborted session leaves lock files behind, check for matching active Chromium processes before deleting `SingletonLock` or `SingletonCookie` manually.
- **Cache Clearance**: Running a generic cache clean command can wipe `~/.cache/camofox/` and force a slow 300MB download during execution. Only clear cache on explicit instructions.
- **Header Modification**: Stiffly overriding user-agent headers cancels the built-in stealth fingerprinting profiles. Let Camofox handle header selection.
