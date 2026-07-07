# Modal Pearl / Akoya mining bootstrap notes (2026-05-30)

Use this when a dedicated Galyarder-owned Modal account is being used for a short PRL/Pearl mining experiment and the task touches Modal API tokens, Pearl wallet generation, or Akoya pool registration.

## What was verified

- Modal dashboard `Settings -> Tokens -> API Tokens -> New Token` produces the credentials needed by the CLI:
  - `Token ID` -> `modal token set --token-id ...`
  - `Token Secret` -> `modal token set --token-secret ...`
- After setting the token, verify with:
  - `modal profile current`
  - `modal token info`
  - `modal app list`
- Sanitize token patterns in logs: `ak-*` and `as-*`.
- `direkturcrypto/modal-pearl` `akoya_modal.py` runs `registry.akoyapool.com/akoya-miner:latest` and registers `AKOYA_POOL_WALLET` against Akoya.
- Modal/H100 side can start and benchmark before pool registration. One failed run reached about `650 TH/s` before registration failed.

## Durable pitfall: wallet prefix

Do not use an EVM/Base wallet (`0x...`) as the Akoya/Pearl payout address. Akoya rejected it with:

```text
Register rejected by pool: Wallet address prefix is not recognized.
```

Akoya/Pearl expects a native Pearl address, observed/documented as `prl1...` / `prl1p...`.

## Native Pearl wallet local flow

Release source:

```text
https://github.com/pearl-research-labs/pearl/releases/tag/pearl-wallet-v1.0.0
asset: go-binaries-linux-amd64-v1.0.2.tar.gz
binaries: oyster, prlctl, pearld
```

Safe private storage pattern:

```text
/home/galyarder/.hermes/private/credentials/agents/galyarder/pearl/
  wallet-passphrase.txt        # 600, private only
  rpc-password.txt             # 600, private only
  create-wallet.json           # 600, contains seed/passphrase; never print/commit
  oyster-file/                 # 700, wallet DB
  pearld-data/                 # chain data
  account.txt                  # 600, public address + local file references only
```

Create a wallet non-interactively with `oyster --createfromfile=<create-wallet.json>` where JSON contains `PrivatePassphrase`, optional `PublicPassphrase`, `Seed` (hex), and `Bday`. **Important:** this command may print the seed to stdout; redirect to a private file and then truncate/sanitize it. Never paste output into chat.

To obtain a mainnet address from a newly-created wallet:

1. Start `pearld` locally with private RPC credentials and `--notls` bound to `127.0.0.1`.
2. Start `oyster` bound to `127.0.0.1`, pointed at local `pearld` via `--rpcconnect`, `--pearldusername`, `--pearldpassword`, and with its own wallet RPC user/pass.
3. Call:

```bash
prlctl --wallet --notls -s 127.0.0.1:44207 -u rpcuser -P "$RPCPASS" getnewaddress default bech32 true
```

This produced a native Pearl address with `prl1p...` prefix. Patch `akoya_modal.py` `WALLET = "..."` with that address and compile-check before remote run.

## One-hour Modal run wrapper pattern

Use a bounded wrapper, not a naked `modal run`, when Galih wants to sleep or leave the session:

- `timeout --kill-after=30s 65m modal run akoya_modal.py`
- always run with `terminal(background=true, notify_on_complete=true)`
- after timeout or process exit, stop Modal apps by **app id** discovered from `modal app list`, not only by app name; ephemeral app names may not match `akoya-pearl-miner`
- verify final `modal app list` shows `stopped` and `Tasks 0`

The earlier name-only stop failed with:

```text
No App with name 'akoya-pearl-miner' found in the 'main' environment.
```

A subsequent app-id stop successfully moved the app to `stopped` with `Tasks 0`.

## User-facing posture

For this class of task, Galih already accepted ban/account/credit downside. Do not loop ToS sermons. State only the live operational gate:

- Modal token missing / verified
- payment attached / not attached
- Pearl wallet missing / generated
- miner running / stopped
- pool rejected wallet / accepted registration
- PRL pending / paid out

Keep final status terse: `running`, `stopped`, `blocked`, or `failed at <gate>` plus 2-5 evidence bullets.
