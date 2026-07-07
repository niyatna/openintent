# PRL AlphaPool Modal Proof Pattern — 2026-06-01

Use this reference when moving an existing Pearl/PRL Modal credit-burn proof from Akoya Pool to AlphaPool.

## Why this exists

Akoya can accept work but still show no PRL when pool variance is poor and no valid/maturing pool block lands inside the PPLNS window. AlphaPool has higher pool cadence and a lower payout threshold, so it can be a better bounded proof target. It still needs hard spend limits and separate payout verification.

## Runner shape

Use a separate Modal app instead of mutating the Akoya runner in-place.

Observed working shape:

- app name: `alphapool-pearl-miner`
- GPU class: H100
- image: Debian slim plus TLS certificates and HTTP downloader
- install AlphaPool's published Pearl worker binary during image build
- use the AlphaPool high-difficulty Pearl stratum endpoint closest to the Modal region
- use a native Pearl wallet address, a stable worker name, and static difficulty suitable for H100-class hardware

Keep wallet seeds/private keys out of Modal, logs, repo, and chat. The runner only needs the payout address.

## Bounded wrapper

Use a local wrapper with a hard timeout and cleanup:

1. launch the Modal app under a known run id
2. capture raw logs to `alphapool_modal_<run_id>.log`
3. after timeout or exit, list Modal apps fresh
4. stop any non-terminal `alphapool-pearl-miner` app by freshly discovered app id
5. re-list until terminal/zero tasks before saying billing stopped
6. write a latest-state JSON from AlphaPool public APIs for follow-up checks

For a first proof, about 65 minutes is useful: long enough for PPLNS/accounting visibility, short enough to stay near a small dollar cap.

## Verification signals

Keep these claims separate:

- **technical start**: Modal app exists with one active task
- **pool connection**: logs show connection, challenge, and workspace-ready events
- **work proof**: logs show both candidate discovery and submit events
- **performance proof**: status lines report stable H100 throughput in the expected band
- **pool accounting proof**: AlphaPool miner API shows worker/hashrate/shares/balance for the wallet
- **economic proof**: balance, payout history, wallet receipt, and sell/cashout route are visible

Observed early-run pitfall: local logs may show submitted work while the AlphaPool miner API still returns empty workers and zero hashrate. Do not stop immediately if logs are actively progressing and Modal still has one live task. Treat it as: technical proof alive, pool/economic proof pending.

## API surfaces

Useful public surfaces:

- AlphaPool global stats API
- AlphaPool miner-by-wallet API
- AlphaPool miners search/list endpoint when debugging visibility lag

Do not paste private wallet material into docs; use `<native-prl-wallet>` placeholders in reusable instructions.

## Reporting shape

For Galih, report state first:

```text
jalan / stale / stopped
- app: <app-id>, state/tasks
- submitted work from log: <n>
- throughput: <range>
- pool API: worker/shares/balance state
- Modal cost: <$x>
- next gate: wait maturity / stop / recheck payout
```

Do not repeat generic risk lectures after the bounded credit-burn risk is accepted. Name only the live gate: submitted work vs pool accounting vs payout/cashout.