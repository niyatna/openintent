# Local workstation cache audit and phase-1 cleanup — May 2026 pattern

## Trigger

Galih had already cleaned package cache/trash/basic cache but disk still showed about `158G / 239G`. He asked for a read-only check first, then approved phase-1 cleanup only.

## Obsidian grounding

Existing notes lived under:

- `/home/galyarder/Documents/Obsidian Vault/galyarder/device-maintenance/2026-04-08-device-maintenance-checklist.md`
- `/home/galyarder/Documents/Obsidian Vault/galyarder/device-maintenance/2026-04-08-home-cleanup-summary.md`

Those notes define the recurring routine: package manager cleanup, user cache cleanup, browser/app data review, AI/dev tool data review, runtime/toolchain cleanup, backup/residue review, and strange-folder audit.

## Read-only findings shape

Useful categories to report:

- filesystem: `/`, `/home`, `/tmp`, `/var/tmp`
- top home dirs: `Games`, `.local`, `.hermes`, `projects`, `.nvm`, `.config`, `.npm`, `.claude`, `.gemini`, `.bun`
- toolchain caches: npm, Bun, pip, uv, Go, Cargo, pnpm, nvm
- profile-local caches under `.hermes/profiles/<profile>/home/`
- project build artifacts: `.next`, `node_modules`, `.turbo`, venvs
- Docker reclaimable images
- active app/runtime state: Brave, Camofox, Discord, Waydroid, Paperstable-diffusion-image-generation, Hermes gateways

Important Hermes quirk: plain `npm`, `pip`, `go`, `pnpm`, `uv` may resolve cache paths under profile-local `HOME`; set `HOME=/home/galyarder` to inspect OS-home caches.

## Phase-1 executed safely

Explicit targets deleted in that pass:

```text
/home/galyarder/.npm/_cacache
/home/galyarder/.npm/_npx
/home/galyarder/.bun/install/cache
/home/galyarder/.cache/pip
/home/galyarder/.cache/go-build
/home/galyarder/.hermes/profiles/galyarder/home/.npm/_cacache
/home/galyarder/.hermes/profiles/galyarder/home/.npm/_npx
/home/galyarder/.hermes/profiles/galyarder/home/.bun/install/cache
/home/galyarder/.hermes/profiles/galyarder/home/.cache/uv
/home/galyarder/.hermes/profiles/galyarder/home/.cache/go-build
/home/galyarder/.hermes/profiles/galyarder/home/.cache/pip
```

Docker action:

```bash
docker image prune -a -f
```

Do not delete `~/.bun/install/global` as part of cache cleanup; that holds global installs, not just cache.

## Verification evidence from session

- Explicit cache deletion estimate: about `6.75G`
- Docker reclaimed: about `1.391G`
- Before: about `159G used / 239G` (`69%`)
- After: about `155G used / 239G` (`67%`)
- All explicit target paths verified gone
- Docker images dropped to `0B`
- Hermes gateway, Galyarder gateway, and Paperstable-diffusion-image-generation were active after cleanup
- Camofox service was found inactive and was restarted; final status active

## Pitfalls learned

- A terminal cleanup command involving recursive deletion may time out or wait for approval; do not assume success. Re-measure targets and check for lingering cleanup processes before retrying.
- `/tmp` content may already be gone because tmpfs was cleared/rebooted between audit and execution; phase-1 should not depend on stale `/tmp` numbers.
- Parent cache directories can look larger after service restart because browser/runtime cache is active again. Verify explicit targets, not just parent directory size.
- Report `temp mail` separately: in this session mail dirs were tiny; the large temp number was `/tmp` residue, not mail.
