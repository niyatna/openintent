# Termux + Ubuntu proot STB Hermes edge node (2026-06-11)

## Context

Galih tested Hermes Agent on an Android TV/STB reachable via Termux SSH (`u0_a42@192.168.100.32:8022`) with Ubuntu proot. The device had roughly 2GB RAM and reported Ubuntu userspace as `armv7l/armhf` while Termux host was `armv8l`.

## Durable routing lesson

For this class of low-resource Android/STB install, treat the box as a **thin always-on edge/gateway node**, not a full Hermes workstation.

Recommended split:

```text
Termux host:
- sshd
- termux-wake-lock
- Termux:Boot or equivalent startup script

Ubuntu proot:
- Hermes Agent core/gateway
- /root/.hermes config and logs
- Python deps via apt/venv

Browser:
- cloud browser / Firecrawl when configured
- avoid local Playwright Chromium / Camofox / Camoufox on 32-bit ARM STB
```

Do not recommend moving Hermes core to Termux-native just because Playwright/Chromium failed in Ubuntu proot. Termux-native still has Android/Bionic constraints, and local Chromium remains the wrong target on 2GB ARM STB. Keep Hermes in Ubuntu proot when already working; put only wake-lock/sshd/boot wrapper in Termux.

## What to verify before claiming viability

Always run fresh resource and process checks:

```bash
free -m
ps -eo pid,ppid,stat,rss,etime,cmd | grep -E '[h]ermes|[g]ateway|[p]ython3 .*hermes|[n]ode|[p]ip install' | sort -k4 -nr | head -20
pid=$(cat /root/.hermes/hermes-gateway.pid 2>/dev/null || true); [ -n "$pid" ] && ps -p "$pid" -o pid,ppid,stat,rss,etime,cmd
```

Report state first:

```text
Hermes installed: yes/no
Gateway running: yes/no + PID/RSS
Available RAM: <MB>
Swap used: <MB>
Heavy transient children: pip/build/node/chromium yes/no
```

## Observed numbers from this session

Before gateway:

```text
Mem total: 1988 MB
used: 1451 MB
available: 537 MB
swap used: 956 MB
Hermes processes: none
```

After `hermes gateway`:

```text
Gateway PID: 11642
Gateway RSS: ~51 MB
Mem used: 1575 MB
available: 413 MB
swap used: 914 MB
```

Transient child during first gateway start:

```text
python3 -m pip install discord.py[voice]==2.7.1 brotlicffi==1.2.0.1
```

This temporarily added more RAM/build pressure. Do not judge steady state until first-run dependency installs complete.

## Firecrawl / browser lesson

If config is:

```yaml
web:
  backend: firecrawl
browser:
  cloud_provider: firecrawl
```

and `/root/.hermes/.env` has `FIRECRAWL_API_KEY`, local Chromium install failure is not proof Firecrawl is unset. It usually means the setup hook tried local `agent-browser` Chromium anyway. Treat local Chromium/Playwright failure as a setup-hook/local-browser problem, not as a reason to reinstall Hermes elsewhere.

On this hardware, avoid:

- local Chromium / Playwright
- Camofox / Camoufox local engine
- Browserbase/Camofox local driver tests unless explicitly needed
- Hindsight daemon / embeddings / Postgres
- Paperstable-diffusion-image-generation full stack
- Docker
- local LLM
- many MCP servers
- multi-agent/subagent-heavy workloads

Good fit:

- lightweight Hermes gateway
- SSH remote control
- Telegram/Discord relay if dependency install settles
- Firecrawl/web cloud tools
- small watchdog/cron tasks
- boot/wake-lock edge node

## Reply posture for Galih

When Galih asks whether a 2GB STB can run Hermes, answer bluntly with evidence. Useful shape:

```text
Bisa, tapi sebagai thin edge node, bukan workstation agent.
Evidence: RAM available <x>, swap used <y>, Hermes PID/RSS <z>.
Keep: sshd, wake-lock, Hermes gateway minimal, cloud browser.
Avoid: local browser, Hindsight, Paperstable-diffusion-image-generation, Docker, local LLM, many MCP.
```

Do not overpromise. Do not say “should be fine” without `free -m` and `ps` output.