# Syncthing Mobile Sync for Obsidian

Session date: 2026-05-07

## When this applies

Use when Galih wants Obsidian notes on the laptop to be available on a phone over the same WiFi without using Obsidian Sync.

## Recommended pattern

Use Syncthing, not SMB/WebDAV, for Obsidian mobile access. Obsidian works best with a local folder on the phone; Syncthing keeps a local copy in sync.

## Galyarder host known-good setup

OS snapshot from setup:

```text
host: galyarderOS
LAN IP: 192.168.100.6/24 on wlan0
vault: /home/galyarder/Documents/Obsidian Vault
```

Syncthing installed without sudo by downloading the official GitHub release into:

```text
/home/galyarder/.local/bin/syncthing
```

User service installed at:

```text
/home/galyarder/.config/systemd/user/syncthing.service
```

Service command:

```text
/home/galyarder/.local/bin/syncthing serve --no-browser --no-restart --logflags=0
```

Syncthing home/config path:

```text
/home/galyarder/.local/state/syncthing
```

Laptop device ID from setup session:

```text
DWPLVMF-H4KFPNL-I3TOXDH-FNPUD4D-VIPWUXI-RNQEFLK-HMAY3A6-PLIEDAU
```

Phone device from setup session:

```text
name: 2201117PG
id: 5XXLX5H-VJHB2KM-LZANCW4-VWTIBN6-UIZ6QFQ-VVQFGSY-DNOHAZN-MYUSNQS
LAN: 192.168.100.5:22000
client: syncthing v2.0.11
```

Initial laptop-created folder:

```text
id: obsidian-vault
label: Obsidian Vault
path: /home/galyarder/Documents/Obsidian Vault
type: sendreceive
ignorePerms: true
fsWatcherEnabled: true
```

Important correction from pairing: the Android app may create/offer its own folder ID even when the label/path looks correct. In the setup session the phone offered:

```text
folder id: kwhg0-554dx
label: obsidian-vault
phone path: /storage/emulated/0/Documents/Obsidian Vault
```

If Obsidian opens an apparently empty vault on the phone, check for a pending phone-origin folder ID and align the laptop to that ID or re-create the phone folder using the laptop-origin ID. The UI label is not enough.

## Commands

Check service:

```bash
systemctl --user is-enabled syncthing.service
systemctl --user is-active syncthing.service
/home/galyarder/.local/bin/syncthing --version
```

Show device ID:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/syncthing -H /home/galyarder/.local/state/syncthing cli show system
```

Add Obsidian folder if missing:

```bash
HOME=/home/galyarder /home/galyarder/.local/bin/syncthing -H /home/galyarder/.local/state/syncthing cli config folders add \
  --id obsidian-vault \
  --label 'Obsidian Vault' \
  --path '/home/galyarder/Documents/Obsidian Vault' \
  --type sendreceive \
  --fswatcher-enabled \
  --ignore-perms
```

Accept/add phone device and share the laptop-origin folder:

```bash
HP='5XXLX5H-VJHB2KM-LZANCW4-VWTIBN6-UIZ6QFQ-VVQFGSY-DNOHAZN-MYUSNQS'
HOME=/home/galyarder /home/galyarder/.local/bin/syncthing -H /home/galyarder/.local/state/syncthing cli config devices add \
  --device-id "$HP" \
  --name '2201117PG' \
  --addresses dynamic \
  --compression metadata
HOME=/home/galyarder /home/galyarder/.local/bin/syncthing -H /home/galyarder/.local/state/syncthing cli config folders obsidian-vault devices add \
  --device-id "$HP"
```

If the phone created a different folder ID and the phone vault opens empty, verify pending folders:

```python
import json, urllib.request, xml.etree.ElementTree as ET
api = ET.parse('/home/galyarder/.local/state/syncthing/config.xml').getroot().find('gui/apikey').text
base = 'http://127.0.0.1:8384'
for path in ['/rest/cluster/pending/folders', '/rest/config/folders', '/rest/system/connections']:
    req = urllib.request.Request(base + path, headers={'X-API-Key': api})
    print(path, json.load(urllib.request.urlopen(req, timeout=15)))
```

Corrective pattern used in the session: remove the phone from the laptop-origin folder, add the phone-origin folder ID on laptop with the same vault path, and share it with the phone:

```bash
HP='5XXLX5H-VJHB2KM-LZANCW4-VWTIBN6-UIZ6QFQ-VVQFGSY-DNOHAZN-MYUSNQS'
ST=/home/galyarder/.local/bin/syncthing
HOME=/home/galyarder "$ST" -H /home/galyarder/.local/state/syncthing cli config folders obsidian-vault devices "$HP" delete
HOME=/home/galyarder "$ST" -H /home/galyarder/.local/state/syncthing cli config folders add \
  --id kwhg0-554dx \
  --label 'obsidian-vault' \
  --path '/home/galyarder/Documents/Obsidian Vault' \
  --type sendreceive \
  --fswatcher-enabled \
  --ignore-perms
HOME=/home/galyarder "$ST" -H /home/galyarder/.local/state/syncthing cli config folders kwhg0-554dx devices add --device-id "$HP"
systemctl --user restart syncthing.service
```

Verify with both folder IDs if both exist:

```python
import json, urllib.request, xml.etree.ElementTree as ET
api = ET.parse('/home/galyarder/.local/state/syncthing/config.xml').getroot().find('gui/apikey').text
base = 'http://127.0.0.1:8384'
for folder in ['kwhg0-554dx', 'obsidian-vault']:
    req = urllib.request.Request(base + f'/rest/db/status?folder={folder}', headers={'X-API-Key': api})
    data = json.load(urllib.request.urlopen(req, timeout=15))
    print(folder, {k: data.get(k) for k in ['globalFiles','localFiles','needFiles','needBytes','state','error']})
```

Healthy signs:

```text
connected: true
isLocal: true
errors: 0
needFiles: 0
state: idle
pending folders: {}
```

## Obsidian ignore file

Create `.stignore` at vault root to reduce workspace conflicts:

```text
// Syncthing ignore rules for Obsidian vault
(?d).obsidian/workspace.json
(?d).obsidian/workspace-mobile.json
(?d).obsidian/workspace-*.json
(?d).trash/
(?d).DS_Store
(?d)Thumbs.db
(?d)desktop.ini
(?d).syncthing*.tmp
(?d)*.tmp
(?d)*~
```

## Phone steps

Android:

1. Install Syncthing-Fork.
2. Add laptop device ID.
3. Wait for pending device on laptop and accept it.
4. Share folder `obsidian-vault` to the phone.
5. Accept the folder on phone into a local path, e.g. `/storage/emulated/0/Documents/Obsidian Vault`.
6. In folder settings, do not infer from grey toggles; confirm the actual folder ID and path. Some grey toggles are unrelated controls like pause/untrusted device.
7. Open Obsidian Mobile -> Open folder as vault -> select synced folder.
8. If Obsidian opens but appears empty, inspect Syncthing folder IDs and pending phone-origin folders before blaming Obsidian.

Safety:

- Do not edit the same note at the same time on laptop and phone.
- If `.sync-conflict` files appear, merge manually instead of deleting blindly.
- Disable battery optimization for Syncthing-Fork if background sync stops.

## Pitfalls

- `sudo pacman -S syncthing` may be unavailable in agent context when passwordless sudo is disabled. Downloading the official binary to `~/.local/bin` works without root.
- In the Galyarder Hermes profile, `$HOME` can resolve to profile-local home. For OS-user Syncthing commands, force `HOME=/home/galyarder` and `-H /home/galyarder/.local/state/syncthing`.
- When extracting the GitHub tarball programmatically, choose the large ELF member named `/syncthing`. The archive also contains metadata files named `syncthing` in other contexts; extracting the wrong member causes `Exec format error` or text-file execution errors.
- Avoid piping downloaded or HTTP output directly into Python/shell interpreters. Save to a temp file or use Python `urllib` directly.
- Do not assume Syncthing-Fork's Indonesian UI toggles from screenshots. The user corrected that the grey toggles shown were pause/untrusted controls, not the `galyarderOS` share state.
- Laptop-side `needFiles: 0` only proves the laptop has what it needs. If the phone vault is empty, verify phone folder ID/path and pending folder offers.
- Do not trust the label `Obsidian Vault` alone. Syncthing syncs by folder ID; a phone-created ID such as `kwhg0-554dx` with the right path can still be a separate empty cluster until laptop and phone are aligned on the same ID.
- After aligning a phone-origin folder ID on the laptop, verify both `/rest/cluster/pending/folders` is `{}` and `/rest/db/status?folder=<phone-id>` shows real local/global counts; if an old laptop-origin folder remains, remove it later only after confirming the phone sync is healthy.
