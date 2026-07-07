# Case note: native `gws` auth vs Hermes legacy token

## Symptoms observed

- User showed `gws auth status` with `token_valid: true`, encrypted keyring storage, and user `mhmdgalihsaputra249@gmail.com`.
- Direct `gws` calls worked:
  - Gmail profile read
  - Gmail messages list
  - Calendar primary calendar and events list
  - Drive files list
  - Tasks tasklists list
- Legacy Hermes helper path failed:
  - `setup.py --check` returned `REFRESH_FAILED: invalid_grant`
  - `google_api.py gmail search ...` failed because `gws` was forced to use stale `~/.hermes/google_token.json`

## Root cause

The legacy Hermes Google Workspace helper scripts treated `~/.hermes/google_token.json` as authoritative and set `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` for `gws` invocations. That overrode native `gws` encrypted/keyring credentials under `~/.config/gws/`, so a stale/revoked Hermes token made wrappers fail while direct `gws` remained healthy.

## Applied fix shape

- `setup.py --check` probes `gws auth status` first.
- `google_api.py` skips the legacy credential override when native `gws` auth is valid.
- `gws_bridge.py` runs native `gws` normally when its auth is valid, falling back to legacy token only when necessary.
- JSON parsing tolerates preamble text such as `Using keyring backend: keyring` before JSON.

## Verification commands used

```bash
python -m py_compile \
  ~/.hermes/skills/productivity/google-workspace/scripts/setup.py \
  ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py \
  ~/.hermes/skills/productivity/google-workspace/scripts/gws_bridge.py

python ~/.hermes/skills/productivity/google-workspace/scripts/setup.py --check
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail search 'newer_than:1d' --max 1
python ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py calendar list --calendar primary
python ~/.hermes/skills/productivity/google-workspace/scripts/gws_bridge.py gmail users getProfile --params '{"userId":"me"}'
```

Fresh good results included `AUTHENTICATED: gws token valid ...`, successful Gmail search JSON, successful Calendar list, and successful Gmail profile via bridge.
