# Cloak-first HAR Capture Adaptation — 2026-05-25

## Trigger

A local HAR-capture skill package was installed, then Galih asked why Playwright was involved when CloakBrowser is the stronger browser route for this workstation.

## Decision

For Galyarder/Keiya, HAR capture should be CloakBrowser/Chrome CDP first.

- `harcapture <url>` should attach to `http://localhost:9222` by default.
- Playwright Chromium should only run when explicitly requested with `--standalone`.
- `--headless` only belongs to `--standalone`; fail fast otherwise.
- `camofox` must not be offered as a CDP preset because Camofox exposes REST on `9377`, not raw Chrome DevTools Protocol.
- Use a shared script target for both profiles: `/home/galyarder/.hermes/scripts/har_capture.py`.
- Use a shared command wrapper: `/home/galyarder/.local/bin/harcapture`.
- Keep profile skill docs aligned, but avoid profile-local `home/` recreation.

## Patch pattern

1. Make Playwright import lazy inside the standalone function so default CDP mode does not depend on it at startup.
2. Set default `args.cdp_url = "cloakbrowser"` unless `--standalone` or explicit `--cdp-url` is provided.
3. Reject invalid combinations:
   - `--standalone` + `--cdp-url`
   - `--headless` without `--standalone`
4. Reject `--cdp-url camofox` with a clear exwriting-plansation.
5. Set output cache to `/home/galyarder/.hermes/profiles/galyarder/cache/har-capture/` unless a different shared/profile cache is deliberately chosen.
6. Patch `har-capture` and `api-discovery` docs in both active Galyarder and Keiya/default roots.

## Verification ladder

- `python -m py_compile /home/galyarder/.hermes/scripts/har_capture.py`
- `harcapture --help` shows default CloakBrowser CDP and explicit `--standalone`.
- `harcapture --cdp-url camofox` exits non-zero with the REST-vs-CDP exwriting-plansation.
- `harcapture https://example.com --headless` exits non-zero unless `--standalone` is present.
- `harcapture --existing-tab` attempts `http://localhost:9222`, proving the default route is CDP, not Playwright.
- `skill_view("har-capture")` and `skill_view("api-discovery")` load.
- Parse skill roots for duplicate names and frontmatter issues.
- Confirm `/home/galyarder/.hermes/profiles/galyarder/home` was not recreated.

## Reporting style

Keep final status terse: what changed, where the shared script/wrapper live, and proof from the verification ladder. Do not explain browser theory unless asked.
