# Hermes Unified Dashboard Port (9190) Setup and Verification

This reference documents the setup and verification steps for consolidating multiple profile-specific Hermes dashboards into a single unified dashboard on port `9190` in Hermes v0.17+.

## Background

Under Hermes v0.17+, running duplicate per-profile dashboard services (e.g., Keiya/default on 9119, Galyarder on 9120) is unnecessary because a single dashboard process can manage all profiles internally. Consolidating all profiles under a single unified dashboard running on port `9190` simplifies port allocation, saves system resources, and avoids iframe security blocks or cross-site cookie verification failures in external frontends (such as the Telegram Mini App).

## Configuration Procedure

### 1. Update the Systemd Override

Configure the main dashboard service to run on port `9190` by creating or editing the systemd user override file at:
`~/.config/systemd/user/hermes-dashboard.service.d/override.conf`

```ini
[Service]
ExecStart=
ExecStart=/home/galyarder/.hermes/hermes-agent/venv/bin/hermes --profile default dashboard --host 127.0.0.1 --port 9190 --no-open --skip-build
```

### 2. Decommission Stale Services

Stop and disable any redundant profile-specific dashboard services:
```bash
systemctl --user stop hermes-dashboard-galyarder.service
systemctl --user disable hermes-dashboard-galyarder.service
```

### 3. Reload and Restart Services

Apply the systemd change and restart the unified dashboard:
```bash
systemctl --user daemon-reload
systemctl --user restart hermes-dashboard.service
```

---

## Verification checklist

When verifying that the Hermes unified dashboard has been successfully port-aligned and deployed:

- [ ] **Check active port binding**: Verify `ss -lntp` shows process `hermes` is listening on port `9190`:
  ```bash
  ss -lntp | grep 9190
  ```
- [ ] **Test local API endpoint access**: Verify the dashboard raises `401 Unauthorized` (confirming the dashboard port is active and gated by access protection, not down or timed out):
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9190/api/health
  # Should return 401
  ```
- [ ] **Decommissioning verification**: Verify that the stale dashboard service (e.g. `hermes-dashboard-galyarder.service`) is inactive and dead:
  ```bash
  systemctl --user status hermes-dashboard-galyarder.service
  ```
- [ ] **Verify frontend proxy / build alignment**: Validate that the Mini App index/express server (`server/index.js`) maps proxy targets and default constants to `HERMES_DASHBOARD_URL=http://127.0.0.1:9190` and client bundle renders cleanly via:
  ```bash
  npm run build
  ```
