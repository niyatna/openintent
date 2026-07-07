# Bounded Cloud GPU Experiments

Use this protocol for speculative, cost-bearing, or payout-seeking cloud GPU tests: mining, inference benchmarks, reward programs, proof-of-compute experiments, and other workloads where remote resources can continue billing after the local shell exits.

## Objective

Generate a small amount of trustworthy evidence without allowing a forgotten GPU allocation to become an uncontrolled bill.

## Pre-run gate

1. Define the maximum runtime and acceptable spend before launching.
2. Use a local wrapper with a hard timeout and a short kill-after grace period.
3. Capture stdout/stderr to a timestamped log.
4. Keep credentials, wallet seeds, signing material, and provider tokens out of logs and chat.
5. Record the remote resource namespace or project scope that belongs to the test.
6. Record the authoritative result surface before the run: provider billing/usage, upstream dashboard/API, wallet/balance endpoint, and any payout minimum/maturity window.

## Run wrapper pattern

```bash
set +e
timeout --kill-after=30s 65m provider-cli run workload 2>&1 | tee -a "$LOG"
run_rc=${PIPESTATUS[0]}
# rc=124 is expected when timeout intentionally ends the bounded test.
```

Adapt the runtime to the approved experiment. Do not treat local shell termination as proof that remote resources stopped.

For remote platforms with ephemeral app IDs, create a duration-specific wrapper (`run_<workload>_one_hour.sh`, `run_<workload>_two_hours.sh`, etc.) rather than hand-editing one script without naming the blast radius. Include `HOME`/profile/env setup explicitly if the CLI depends on user-level config.

## Cleanup pattern

1. List active remote apps, jobs, instances, or containers fresh from the provider.
2. Stop resources by freshly discovered provider ID when ephemeral resources are not reliably addressable by name.
3. Re-list after the stop request.
4. Poll until the provider reports a terminal state and zero active tasks, or report `stopping` rather than claiming completion.
5. Inspect local residual processes if relevant.

## Evidence ladder

Keep these claims separate:

1. **Workload started** — remote runtime exists.
2. **Workload accepted by upstream** — registration, API response, accepted share, accepted request, or equivalent is visible.
3. **Performance measured** — parse runtime metrics from logs; report min/avg/max where useful.
4. **Remote billing stopped** — provider reports terminal state and zero active tasks.
5. **Economic result proven** — payout, balance, invoice, credit burn, or sale proceeds are visible in the authoritative external system.

Accepted work is not the same as realized payout. Provider cleanup is not proven while the remote state is merely `stopping`.

For payout-seeking workloads, do not equate `accepted shares`, `accepted requests`, high throughput, or dashboard hashrate with realized money. Model the full accounting chain, for example:

```text
accepted work -> upstream/pool accounting -> block/job maturity -> pending balance -> minimum threshold -> payout/sweep -> wallet/bank/exchange balance -> liquidation if needed
```

Report which link is currently proven and which link is still unproven.

## Payout/maturity accounting pattern

When a workload has maturity, PPLNS, delayed settlement, rev-share, points, or threshold payout:

1. Read the upstream docs/API for payout cadence, minimum payout, fee, maturity period, and expiration policy.
2. Query the authoritative account/address endpoint, not only the local logs.
3. Track at least these fields when available: pending balance, total paid, online/offline state, accepted work count, stale/rejected count, maturing jobs/blocks, next maturity ETA, payout history.
4. Use logs for local performance; use upstream API/dashboard for economic state.
5. If the first run shows accepted work but zero pending/paid, schedule/perform a maturity-window recheck before concluding zero revenue.
6. If pending remains zero after the relevant maturity window, treat it as a stop signal unless the user explicitly accepts more burn for research.

## Economics gate

Before extending a speculative cloud run beyond the first bounded proof:

1. Estimate cost/hour from provider billing or the user's known observed burn.
2. Estimate output/hour from authoritative live data when possible, not just social posts or one model's answer.
3. Express the result as a break-even price or loss/profit per hour.
4. Use conservative and optimistic bands when price/liquidity is uncertain.
5. Separate technical proof from profit proof:
   - technical proof = upstream accepted the work and performance is stable
   - profit proof = matured pending/paid balance exceeds cloud cost after fees and realistic liquidation price
6. Do not scale to multi-hour or overnight runs solely from high hashrate/throughput.

If a user asks to continue while economics are uncertain, allow a bounded next proof only when there is an explicit stop condition and auto-cleanup. Example stop conditions: pending balance still zero after maturity, realized output/hour below break-even, remote provider warning/suspension, spend cap approaching, or no clear liquidation route.

If a previous bounded run burned paid time while the useful workload silently stopped, a plain timeout wrapper is not enough. Use the liveness watchdog pattern in `references/remote-workload-liveness-watchdogs.md`: check provider resource state, local log progress, and authoritative upstream online/last_seen/accepted-work state on a cadence (for example every 15 minutes, with cheap light checks when the prior failure mode was idle burn). Stop/restart early on stale/offline/no-progress rather than waiting for the hard timeout.

## Post-run report

Report tersely:

- bounded runtime and termination reason
- fresh remote resource state and active task count
- accepted-work count or upstream confirmation
- measured performance range
- authoritative payout/balance state if available
- exact remaining uncertainty and next recheck time if maturity or accounting propagation applies
- cost-vs-output gate for any proposed continuation

## Scaling gate

Do not scale a speculative workload solely from throughput. Require a fresh cost-vs-output check and an observable payout or monetization path first.

If the bounded test produces evidence and the user explicitly approves continuous usage ("abisin creditnya", "keep it running"), graduate to the continuous supervisor pattern in `references/continuous-supervisor-with-billing-cap.md`. Always confirm a hard daily spend cap before building the supervisor. Do not assume "keep running" means "no safety" — it means "run aggressively within a confirmed cap."
