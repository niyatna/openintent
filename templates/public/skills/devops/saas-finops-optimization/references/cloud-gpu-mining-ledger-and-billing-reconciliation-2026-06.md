# Cloud GPU Mining: Ledger and Billing Reconciliation Pitfalls (2026-06)

Use this reference when a cloud GPU mining run has multiple visible ledgers: pool dashboard/API, chain explorer, wallet balance, cloud billing credits, and process/runtime state.

## Lesson from PRL / AlphaPool / DigitalOcean AMD credit burn

A mining pool can expose several numbers that look like “total,” but they are not interchangeable:

- **Pool pending / balance** — un-matured or not-yet-paid pool rewards. This is not on-chain yet.
- **Pool `total_paid` / paid history** — cumulative payout history from the pool. It is not current holdings if the wallet has later outgoing transactions.
- **Explorer current balance** — current on-chain holdings at the wallet address.
- **Explorer received / sent** — cumulative transaction history; current balance is normally `received - sent`.
- **Relevant current total** for “how much do we have now?” is usually:

```text
on-chain current balance + pool pending balance
```

Do **not** answer current holdings with:

```text
pool total_paid + pool pending
```

That number is pool payout history plus pending, not spendable/current wallet value.

## Verification sequence

1. Fetch pool API/dashboard:
   - pending / balance
   - total paid history
   - payment statuses (`sent`, `pending`, `orphaned`)
   - workers and hashrate
2. Fetch chain explorer or wallet RPC for the payout address:
   - current balance
   - unconfirmed balance
   - received
   - sent
   - tx count / latest tx
3. Calculate separately:

```text
current_onchain_plus_pending = explorer_balance + pool_pending
pool_history_plus_pending = pool_total_paid + pool_pending
```

4. In the final answer, label both if needed. If the user asks “total now,” lead with `current_onchain_plus_pending`.

## Pool worker and hashrate lag

Pool dashboards can keep showing a worker as online or showing 1h/24h hashrate after the miner process stopped. This is trailing/decay data.

For active mining state, verify both:

- remote process/log (`alpha-miner`, supervisor, timeout status, latest submitted share)
- pool worker/API state

If they disagree, say it explicitly:

```text
remote miner is stopped; pool still shows worker/hashrate because of lag/trailing window
```

## Cloud billing credit ledgers

Provider dashboards can show stale posted billing and more-live available credit on the same page. For DigitalOcean-style credit pages, reconcile:

- estimated balance / amount owed now
- month-to-date total usage
- credits applied
- grant table `Amount Remaining`
- top-level `Available Credits`
- saved payment method state

When these disagree, use the most conservative live operational ceiling — usually **top-level Available Credits** — for remaining runtime. Treat daily-updated usage and grant tables as posted/lagged ledgers.

Example interpretation pattern:

```text
cash owed now: $0
posted usage: $X
credit table remaining: $Y
available credit: $Z  <- operational ceiling
remaining runtime ~= $Z / hourly_rate
```

## Timeout and droplet lifecycle pitfall

A bounded miner timeout stops the mining process; it does **not** destroy or stop the billable cloud VM/droplet. After any bounded burn:

1. Verify miner process stopped.
2. Verify pool worker/hashrate is only trailing or offline.
3. Verify cloud resource is stopped/destroyed if the user does not want further billing.
4. If the user intentionally wants to burn the last credit, run a short bounded final burn and monitor it, but report the risk that credit may run out before timeout.
