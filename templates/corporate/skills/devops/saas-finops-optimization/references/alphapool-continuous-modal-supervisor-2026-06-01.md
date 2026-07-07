# AlphaPool PRL Continuous Modal Supervisor — 2026-06-01

Use this reference after a bounded AlphaPool PRL proof succeeds technically and Galih explicitly approves burning idle Modal credits within a hard workspace limit.

## Why this reference exists

The AlphaPool proof produced live pool-side evidence after an indexing delay:

- Modal app active with one task.
- `alpha-miner` connected to `sg1.alphapool.tech:5566`.
- Miner logs showed H100 hashrate and `share submitted` events.
- `/api/miner/<wallet>` later populated `workers[]`, `recent_shares[].valid=true`, `shares24h`, `balance_prl`, and pending payment rows.

The first empty wallet page/API was not proof of failure; it was startup indexing/accounting delay.

## Exact human dashboard route

```text
https://pearl.alphapool.tech/miner/<wallet>#miners
```

The wallet is part of the URL path. The fragment is only `#miners`; do not append another wallet after the fragment.

## Verified local artifacts

Under `/home/galyarder/experiments/modal-pearl/modal-pearl/`:

- `alphapool_modal.py` — Modal H100 runner using `alpha-miner`, AlphaPool SG stratum, wallet, worker name, and static difficulty.
- `run_alphapool_proof.sh` — bounded segment wrapper with local timeout and post-run Modal app cleanup.
- `alphapool_continuous_supervisor.py` — cap-gated loop around bounded segments.

Treat these as local implementation references; inspect them live before reuse because provider behavior and limits may change.

## Cap correction learned in-session

Do not infer that a visible `$60` grant balance means the workspace can burn `$60`. The actual workspace usage ceiling may still be `$50`. Reconcile these ledgers separately:

1. writing-plans credit / grant balance,
2. grant expiration,
3. billing report gross usage,
4. workspace usage limit,
5. active-resource state.

For a `$50` workspace ceiling, use a conservative supervisor target below the hard limit and leave lag buffer. In the verified correction sequence:

```text
hard workspace usage limit: $50
internal supervisor cap:     $48
grace buffer:                 $2
```

The exact safe cap is not universal. Re-check the visible workspace usage limit every billing cycle and choose a buffer that absorbs billing-report lag.

## Safe correction sequence when a supervisor starts with the wrong cap

1. Query billing and active apps fresh.
2. Kill the incorrect local supervisor.
3. Stop every active AlphaPool Modal app by freshly listed app ID.
4. Verify provider state is `stopped` and tasks are `0`.
5. Verify local miner/supervisor processes are gone.
6. Recalculate spend against the real workspace limit.
7. Relaunch supervisor with corrected cap and grace buffer.
8. Verify exactly one active app, one active task, new supervisor PID/session, and fresh share/hashrate logs.

Do not merely edit environment variables while the old supervisor is still alive.

## Evidence surfaces

Keep these separate:

- **Provider running:** `modal app list --json` shows one `alphapool-pearl-miner` app with active task.
- **Local miner live:** segment log shows `pool connected`, challenge solved, hashrate, candidate shares, and submissions.
- **Pool acceptance:** `/api/miner/<wallet>` shows `workers[].online=true`, `recent_shares[].valid=true`, and advancing `shares24h`.
- **Maturity accounting:** `balance_prl` and pending payment rows increase.
- **Payout:** `total_paid_prl` or transaction history increases.
- **Cleanup:** app state `stopped`, tasks `0`, and no residual local processes.

## Reporting posture

When Galih asks status, report state first:

```text
jalan / stopped / stale
- active app + tasks
- cap + grace + remaining safe spend
- live hashrate + share progress
- pending balance vs total paid
```

Avoid presenting local `share submitted` as paid PRL. Avoid presenting a grant balance as proof that the workspace usage cap permits more runtime.
