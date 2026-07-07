# Config Hardening Audit

Purpose: track Hermes config posture against the access/autonomy lessons.

## Checklist

| Item | default/Operations target | corporate-agent/public-agent target | Notes |
|---|---|---|---|
| fallback providers | present | present | `fallback_providers` should exist and point to available provider/model refs |
| approval mode | high-autonomy but domain-boundary aware | stricter/manual for destructive risk | domain SOUL boundaries override global mode |
| cron approval mode | deny/confirm risky cron | deny/confirm risky cron | no recursive cron job creation |
| MCP reload confirmation | true | true | avoid silent MCP reload changes |
| browser recording | false unless scoped QA/debug | false unless scoped QA/debug | private/intimate work should not be recorded by default |
| privacy/secret redaction | security redaction true | security redaction true | PII redaction can be separate choice |
| terminal timeout/resource lifetime | sane timeouts | sane timeouts | use start → use → stop |
| code execution limits | bounded | bounded | max tool calls/timeout explicit |
| delegation | bounded concurrency/depth | bounded concurrency/depth | subagent auto-approve must still obey domain boundaries |
| skills guard | true | true | avoid low-quality agent-created skills |
| logging/session retention | bounded enough | bounded enough | avoid secret leakage |
| memory limits | enough for curated USER/MEMORY | enough for curated USER/MEMORY | avoid flooding context |
| Discord admin toolset | disabled | disabled | native `discord` allowed, `discord_admin` not enabled |

## Latest audit command

```bash
~/.hermes/scripts/agent-os-access-hardening-audit.py
```

The command writes:

```text
~/.hermes/reports/agent-os/access-hardening-latest.json
```

## Interpretation

- `pass`: required access/autonomy/credential/QA/config invariants are present.
- `warn`: deliberate caveat or non-blocking risk. Read details.
- `fail`: do not claim maturity loop complete.
