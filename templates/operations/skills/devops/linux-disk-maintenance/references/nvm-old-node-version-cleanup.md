# nvm old Node version cleanup — read-only gate pattern

## Trigger

Use this when Galih asks whether an old Node version under `~/.nvm/versions/node/` is safe to remove during disk cleanup.

## Read-only audit before removal

Do not answer from assumption. Check live state first:

```bash
export NVM_DIR=/home/galyarder/.nvm
. "$NVM_DIR/nvm.sh"
printf 'current='; nvm current
printf 'default='; nvm alias default || true
nvm ls
```

Check active processes and explicit references to the old version:

```bash
old=/home/galyarder/.nvm/versions/node/v22.22.0
pgrep -af "$old" || true
grep -RIn --exclude-dir=.git --exclude-dir=node_modules "$old\|v22.22.0" \
  /home/galyarder/.config/systemd/user \
  /home/galyarder/.config/environment.d \
  /home/galyarder/.local/bin \
  /home/galyarder/scripts 2>/dev/null || true
```

Check project version pins and engine constraints before removal:

```bash
find /home/galyarder/projects /home/galyarder/.hermes/hermes \
  -name .nvmrc -o -name .node-version -o -name package.json 2>/dev/null
```

Review only the relevant files; `>=22` is satisfied by Node 24, but exact `22`, `<24`, or hardcoded binary paths are blockers.

## Stale symlink pitfall

An old version can be unused at runtime but still referenced by stale symlinks, e.g. `~/.local/bin/codex -> ~/.nvm/versions/node/v22.../bin/codex` while PATH resolves `codex` from Node 24 first. Fix/remove stale symlinks before uninstalling the old Node version.

Preferred fix if the tool exists in the new version:

```bash
ln -sfn /home/galyarder/.nvm/versions/node/v24.15.0/bin/codex /home/galyarder/.local/bin/codex
```

## Removal

Prefer nvm-managed removal over `rm -rf`:

```bash
export NVM_DIR=/home/galyarder/.nvm
. "$NVM_DIR/nvm.sh"
nvm deactivate || true
nvm uninstall v22.22.0
```

## Verification

After removal, verify:

```bash
export NVM_DIR=/home/galyarder/.nvm
. "$NVM_DIR/nvm.sh"
nvm use default >/dev/null
nvm current
nvm alias default
node --version
npm --version
command -v codex && codex --version || true
[ ! -e /home/galyarder/.nvm/versions/node/v22.22.0 ] && echo 'old node path gone'
pgrep -af '/home/galyarder/.nvm/versions/node/v22.22.0' || true
```

Also sanity-check expected active services after changing Node toolchain state:

```bash
for svc in hermes-gateway.service hermes-gateway-galyarder.service camofox-browser-galyarder.service paperstable-diffusion-image-generationai.service; do
  systemctl --user is-active "$svc" 2>/dev/null | sed "s/^/$svc: /" || true
done
```

## Reporting

Report verdict in this shape:

- current/default Node version
- whether any active process uses the old version
- project pins / engine blockers
- stale symlink fixes
- removal method (`nvm uninstall`, not manual deletion)
- reclaimed size and service sanity
