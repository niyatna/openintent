# Termux Ubuntu proot STB browser routing and gateway checks (2026-06-11)

Use this reference when Hermes is being installed or debugged on a low-resource Android TV/STB running Termux + Ubuntu proot.

## Durable routing pattern

Recommended split:

```text
Termux host:
- sshd
- termux-wake-lock
- Termux:Boot / start script

Ubuntu proot:
- Hermes Agent core and gateway
- profile config and env under the proot root home
- Python venv/deps through apt/venv

Browser:
- Firecrawl/cloud browser for Hermes browser tools
- no local Chromium/Playwright/Camofox on constrained armhf/armv7 STB unless explicitly proven viable
```

Do not treat this as a generic ban on local browsers. It is the low-resource/armhf edge-node route: make the STB a thin gateway and offload browser execution to cloud.

## Firecrawl vs local Chromium failure

If Hermes setup selects Firecrawl but then logs something like:

```text
Installing Chromium...
npx agent-browser install --with-deps
Chromium install failed
```

separate the layers:

- `web.backend: firecrawl` and `browser.cloud_provider: firecrawl` are config choices.
- `FIRECRAWL_API_KEY` in the profile env file is Firecrawl auth.
- local Chromium/agent-browser installation is a local-browser post-setup step; on armhf/armv7 it may fail because compatible browser binaries are unavailable or too heavy.

For Firecrawl cloud browser use, verify config + key + live provider call before calling the browser route broken. A local Chromium failure alone does not prove Firecrawl is unusable.

Minimal config shape:

```yaml
web:
  backend: firecrawl

browser:
  cloud_provider: firecrawl
```

Sanitized key check pattern:

```bash
if grep -q '^FIRECRAWL_API_KEY=.' "$HERMES_ENV_FILE"; then
  echo firecrawl_key_set
else
  echo firecrawl_key_missing
fi
```

## Gateway/platform/model layers

When Telegram/Discord appears silent, check layers separately before concluding the bot is dead:

1. gateway process exists (`hermes gateway` PID/RSS)
2. platform token and allowlist env vars exist (redact token; hash/length only)
3. inbound message reached gateway logs
4. provider API key/base URL exists
5. model is non-empty in `config.yaml`
6. upstream call succeeds

Failure signature from this session:

```text
provider=openrouter base_url=https://openrouter.ai/api/v1 model=
HTTP 400: No models provided
```

That means the platform/gateway can be alive while model routing is empty. Fix the model key first, then restart gateway.

Example model-only patch pattern:

```bash
python_from_hermes_venv - <<'PY'
from pathlib import Path
import yaml
p = Path('PROFILE_CONFIG_PATH')
c = yaml.safe_load(p.read_text()) if p.exists() else {}
c['model'] = 'MODEL_ID_HERE'
p.write_text(yaml.safe_dump(c, sort_keys=False, allow_unicode=True))
print('model_set', c['model'])
PY
```

Then restart the manual gateway using the profile's gateway PID/log path.

## Same-WiFi custom provider trap

For a custom provider hosted on another machine on the same WiFi:

- `localhost` / `127.0.0.1` from the STB means the STB itself, not the laptop/PC.
- Use the provider host's LAN IP, e.g. `http://LAN-IP:PORT/v1`.
- The provider server must bind to `0.0.0.0` or its LAN interface, and firewall must allow the port.

## Resource posture

On 2GB Android TV/STB class devices, Hermes gateway can run but should stay minimal:

- avoid local browser engines, Docker, local LLMs, heavy MCP stacks, Hindsight/Postgres/embedding daemons, and multi-agent fanout;
- prefer one profile/gateway and cloud-only browser/search/extract;
- measure before/after with `free -m` and PID RSS before claiming it fits.

Status wording should be direct:

```text
gateway alive: yes/no
platform token: set/missing
model: set/missing
last log failure: <exact redacted error>
RAM available: <MB>
next move: <single fix>
```
