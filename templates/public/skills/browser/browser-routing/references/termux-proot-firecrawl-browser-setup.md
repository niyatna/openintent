# Termux/Ubuntu proot STB: Firecrawl browser setup vs local Chromium

Session lesson: Galih installed Hermes Agent inside Ubuntu proot on an Android TV/STB through Termux SSH. The Ubuntu environment reported `armv7l` / `armhf`, while the Android/Termux host reported `armv8l`. The device had only ~2GB RAM, with high memory pressure even before Hermes gateway was actually running.

## Durable routing lesson

For Hermes browser setup on Termux/proot STB-class hardware, do not treat Firecrawl as requiring local Playwright/agent-browser Chromium.

Firecrawl browser is a cloud browser route:

```yaml
web:
  backend: firecrawl

browser:
  cloud_provider: firecrawl
```

Required credential in the active Hermes profile `.env`:

```bash
FIRECRAWL_API_KEY=...
```

A setup wizard may still try the `agent_browser` post-setup hook and run something like:

```bash
npx agent-browser install --with-deps
```

On `armhf` / `armv7l` Ubuntu proot this can fail because Playwright/Chromium local browser binaries are not available or practical for 32-bit ARM, and compiling/downloading local browser deps is the wrong route. That failure does not prove Firecrawl is unusable.

## Correct response pattern

- Verify or ask for the selected route: `browser.cloud_provider: firecrawl` vs local browser.
- If the task is Firecrawl cloud browser, skip or ignore local Chromium install failure unless the wizard hard-fails.
- Ensure `FIRECRAWL_API_KEY` is set in the active Hermes profile `.env` and mask it in replies.
- If setup hard-fails only because Chromium install failed, patch/configure the setup to bypass the local `agent_browser` post-setup for Firecrawl rather than trying to make local Chromium work on armhf.
- Do not recommend Playwright/local Chromium as the primary browser route for this hardware unless the user explicitly wants a best-effort local experiment.
- Do not imply Hermes gateway/browser is live just because config is set. Verify the process, PID, port, or actual tool invocation first.

## Low-RAM STB checks

For 2GB Android TV/STB hardware, RAM pressure is expected. A useful status check separates installed/configured/live:

```bash
proot-distro login ubuntu -- bash -lc '
  free -m
  pid=$(cat /root/.hermes/hermes-nohup.pid 2>/dev/null || true)
  echo "pidfile=${pid:-none}"
  if [ -n "$pid" ]; then ps -p "$pid" -o pid,ppid,stat,rss,etime,cmd || true; fi
  ps -eo pid,ppid,stat,rss,etime,cmd | grep -E "[h]ermes|[p]ython|[n]ode" | sort -k4 -nr | head -12
'
```

Report in layers:

- `Hermes installed`: binary/version/venv exists.
- `Firecrawl configured`: `web.backend`, `browser.cloud_provider`, and `FIRECRAWL_API_KEY` set.
- `Gateway/Hermes daemon live`: process/port/PID evidence exists.
- `Browser route live`: Firecrawl session/tool smoke test succeeds.

## Persistence caveat

Ubuntu proot under Termux often does not provide real systemd boot semantics. For gateway persistence on STB hardware, prefer Android/Termux-side wake-lock and boot/startup wiring plus proot-side `nohup`/supervision, rather than assuming a systemd unit will start at device boot.

Keep the STB route minimal: `sshd`, `termux-wake-lock`, Hermes gateway/CLI as needed, and cloud browser. Avoid local browser engines, heavy MCP stacks, and memory daemons unless the user explicitly accepts the RAM cost.
