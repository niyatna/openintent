# PRL Pool Comparison: Akoya vs AlphaPool — 2026-06-01

Use this reference when Galih asks whether to keep mining PRL on Akoya or switch to AlphaPool after seeing accepted shares but `pending_balance=0`.

## Trigger

- A PRL/Akoya Modal run is online, accepted shares are increasing, but the dashboard/API still shows `pending_balance=0`.
- User shares `https://pearl.alphapool.tech/` or says someone claimed AlphaPool is more “gacor”.
- Goal is to decide whether to keep burning bounded Modal credits on Akoya or run a short AlphaPool proof.

## Live inspection pattern

### AlphaPool public/API surfaces

Fetch the page and API directly:

```bash
curl -sL https://pearl.alphapool.tech/ -o /tmp/alphapool_pearl.html
curl -sL -H 'Accept: application/json' https://pearl.alphapool.tech/api/stats
curl -sL -H 'Accept: application/json' 'https://pearl.alphapool.tech/api/blocks?limit=100'
curl -sL -H 'Accept: application/json' 'https://pearl.alphapool.tech/api/miners?limit=50'
curl -sL -H 'Accept: application/json' 'https://pearl.alphapool.tech/api/miner/<wallet>'
```

Direct miner UI route uses a hash tab. Use:

```text
https://pearl.alphapool.tech/miner/<wallet>#miners
```

Do not omit `#miners` when Galih asks for the active worker page; the base `/miner/<wallet>` route can look empty or misleading before the frontend tab/state updates. If the UI is blank, verify with `/api/miner/<wallet>` and look for `workers[].online`, `hashrate_live`, `shares24h`, `balance_prl`, `payments[].status`, and `recent_shares[].valid`. AlphaPool accounting can lag: miner logs may show submitted shares first, then API/UI worker state and pending balance appear minutes later.

Useful AlphaPool fields observed on 2026-06-01:

- `pool.hashrate`: around `4.4 EH/s`
- `pool.blocks24h`: around `136`
- `pool.payouts24h`: around `3.67M PRL`
- `coins[0].payout_min`: `1` in `/api/stats`, while the page copy said minimum payout `0.5 PRL`; treat as surface mismatch and verify before relying on exact threshold.
- `feePercent`: `5`
- page copy: `alpha-miner` client dev fee `1%`
- page copy: payout every `4 hours`
- page copy: time-weighted PPLNS, 65-minute half-life
- page copy: H100 benchmark around `610–620 TH/s`
- stratum endpoint: `us2.alphapool.tech:5566` or nearest regional endpoint; Asia endpoint listed as `sg1.alphapool.tech:5566`.
- cloud/Docker route uses `alphaminetech/pearl-miner` and environment variables like `PEARL_ADDRESS`, `PEARL_WORKER`, `PEARL_POOL_HOST`, `PEARL_POOL_PORT`, and optionally `PEARL_DIFFICULTY`.

### Akoya public/API surfaces

The Akoya SPA uses `/api/v1` endpoints discovered from its JS bundle:

```bash
curl -sL https://akoyapool.com/stats -o /tmp/akoya_stats.html
curl -sL https://akoyapool.com/assets/index-*.js -o /tmp/akoya_index.js  # use actual asset filename from HTML
curl -sL -H 'Accept: application/json' https://akoyapool.com/api/v1/pool/stats
curl -sL -H 'Accept: application/json' https://akoyapool.com/api/v1/pool/info
curl -sL -H 'Accept: application/json' 'https://akoyapool.com/api/v1/pool/blocks?page=1&page_size=5'
curl -sL -H 'Accept: application/json' 'https://akoyapool.com/api/v1/miners/<wallet>'
```

Useful Akoya fields observed on 2026-06-01:

- `total_hashrate`: around `0.52 EH/s`
- `blocks_found24_h`: around `14`
- `total_paid24_h`: around `37,962 PRL`
- `avg_time_to_block_seconds`: around `4930s` (~82 minutes)
- `min_payout_prl`: `10`
- `pool_fee_percent`: `5`
- `payout_interval_seconds`: `900` (15 minutes)
- miner API fields: `accepted_shares24_h`, `stale_shares24_h`, `pending_balance`, `total_paid`, `total_hashrate_formatted`, `maturing_pool_blocks_count`, `next_pool_block_maturity_eta_seconds`, and `instances`.

## Interpretation rule

Keep these distinct:

- **Running proof**: provider task active, miner registered, hashrate, accepted shares, low stale rate.
- **Maturity proof**: pool pending balance increases after block/round maturity.
- **Payout proof**: pool payout history/`total_paid` increases or wallet receives PRL.
- **Profit proof**: paid PRL can be deposited/sold/withdrawn at real price.

`accepted_shares > 0` with `pending_balance=0` can be normal before maturity, but it is not economic proof.

## Decision heuristic from this session

For short, bounded Modal-credit runs:

- **AlphaPool looked better for fast visible feedback** because it had much higher 24h block count, lower apparent payout threshold, and regular 4-hour payout copy.
- **Akoya was technically running normally** when accepted shares increased with `stale=0`, but lower pool hashrate/block cadence plus 10 PRL minimum made `pending=0` more likely during short checks.
- Pool size does not automatically improve long-run expected ROI per hash; it mainly reduces variance and speeds visible accounting. AlphaPool also has an extra `alpha-miner` dev fee if using its miner.

Recommended move when Akoya has accepted shares but zero pending and AlphaPool looks stronger:

1. Wait for any active Akoya maturity ETA if it is short (for example <30–60 minutes), unless the user explicitly says to switch immediately.
2. If pending remains zero or tiny after maturity, stop Akoya with the stop-file/supervisor cleanup path.
3. Run a bounded AlphaPool proof (60–90 minutes) with the same wallet, nearest stratum endpoint, static difficulty appropriate for H100 if supported, hard Modal cap/runtime, and the same liveness watchdog surfaces.
4. Judge AlphaPool by actual miner registration, accepted shares, miner page/API balance, payout threshold progress, and any payout history — not by site marketing copy alone.

## Response shape

```text
iya, AlphaPool keliatan lebih gacor buat short proof:
- Alpha: <pool EH/s>, <blocks24h>, min payout <x>, payout cadence <x>
- Akoya: <pool EH/s>, <blocks24h>, min payout <x>, current pending <x>
verdict: wait maturity if near; if still 0/tiny, stop Akoya and run bounded Alpha proof.
```

Do not claim AlphaPool is “more profitable” until payout and sell/cashout gates are proven. Say “more likely to show visible pending/payout faster” unless real realized PRL/hour and sale route have been verified.
