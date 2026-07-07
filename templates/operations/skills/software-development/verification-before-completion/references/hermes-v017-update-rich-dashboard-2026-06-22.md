# Hermes v0.17 update with local patches — 2026-06-22

## Context

Galih asked to review upstream Hermes releases, preserve local patches/fork state, update Hermes to the newest version, enable Telegram rich messages, rationalize dashboard services, and assess config migration/desktop rebuild risk.

## Durable procedure lessons

- Treat `latest` carefully. Latest release tag (`v2026.6.19`) can still be behind `upstream/main`. If Galih says the end state must be newest, finish with `HEAD..upstream/main = 0` and report `HEAD...upstream/main` counts.
- Preserve first: backup branch, binary patch, untracked tarball, and git bundle before merges. Untracked agent-skill sync files should be backed up but not mixed into the core Hermes update commit.
- If a merge-to-release then merge-to-main creates noisy ancestry, make a clean linear integration branch from `upstream/main` and apply the local diff as one preserve commit.
- Version banners can use stale `.update_check`; if `hermes --version` says behind but git says `HEAD..origin/main = 0`, clear the relevant `.update_check` files and re-run version checks.
- When restarting the current gateway would kill the reply, schedule delayed `systemd-run --user --on-active=...` restart and write a log path.
- For Telegram v0.17 rich messages, the config key is `telegram.extra.rich_messages`, not `telegram.rich_messages`. Enable per profile and restart gateways.
- v0.17 dashboard refuses public `0.0.0.0 --insecure` without auth. For single-machine use, bind dashboard to `127.0.0.1`; one dashboard can manage profiles, so duplicate per-profile dashboard services may be unnecessary.
- Config migration from 27 to 30 should be dry-run on copied configs first. In this session default/Galyarder only changed `_config_version` (plus comments for Galyarder); Niyatna had noisier default seeding but mostly visible defaults.
- Linux desktop artifacts are not refreshed by updating core source. `apps/desktop/package.json` may be v0.17 while `apps/desktop/release/linux-unpacked/Hermes` remains an older build. Rebuild with the desktop workspace scripts when desktop features matter.

## Verification shape used

- `hermes --profile <profile> --version` for all active profiles.
- `git rev-list --left-right --count HEAD...upstream/main` and `HEAD...origin/main`.
- `python -m py_compile` on touched critical modules.
- Focused `uv run --extra dev python -m pytest ... -o addopts= -q` for gateway/channel/stream/image/send-message tests.
- Systemd `show` for gateway/dashboard services and HTTP smoke for dashboards.
