# PRL / Modal Credit-Reset Relaunch Pattern — 2026-06-01

Use this as a session-specific reference for relaunching an Akoya/Pearl PRL mining run after Modal credits reset or a fresh monthly balance appears.

## Trigger

- User says Modal credits reset and asks to run PRL again with a dollar cap.
- Existing PRL/Akoya setup already exists under `/home/galyarder/experiments/modal-pearl/modal-pearl`.
- Goal is to burn/free-salvage a bounded credit amount, not prove long-term profitability.

## Pre-run checks

1. Confirm no active Modal apps/tasks:
   ```bash
   cd /home/galyarder/experiments/modal-pearl/modal-pearl
   HOME=/home/galyarder .venv/bin/modal app list --json
   ```
2. Confirm today's billing surface is readable:
   ```bash
   HOME=/home/galyarder .venv/bin/modal billing report --for today -r h --tz local --json
   ```
   `[]` can be valid immediately after reset/no completed billing interval. It is not proof current running cost is zero forever; Modal billing can lag by full intervals.
3. Confirm pool state before launch through Akoya miner API for the wallet:
   `https://akoyapool.com/api/v1/miners/<prl1...wallet>`.
4. Confirm the price/liquidity basis from a live market surface. For this run, SafeTrade PRL/USDT was about `0.79 USDT`, with visible order book depth and recent trades. Treat this as execution basis, not guaranteed liquidation.
5. Remove stale stop file before launch:
   ```bash
   rm -f .stop_mining
   ```

## Launch pattern used

Use the existing continuous supervisor, but run it with explicit cap, grace, and runtime ceiling:

```bash
cd /home/galyarder/experiments/modal-pearl/modal-pearl
rm -f .stop_mining
export HOME=/home/galyarder
export AKOYA_DAILY_CAP_USD=30
export AKOYA_COST_GRACE_USD=2
export AKOYA_SEGMENT_DURATION=7200
export AKOYA_MAX_RUNTIME_SECONDS=28800
python3 akoya_continuous_supervisor.py
```

Recommended Hermes execution: start this as a tracked background process with completion notification, not as an untracked shell `&` process.

## Supervisor hardening added from this run

The supervisor should support:

- `AKOYA_MAX_RUNTIME_SECONDS` — hard wall-clock ceiling independent of billing report lag.
- `AKOYA_COST_GRACE_USD` — configurable buffer before cap to avoid overshoot.
- Stop instead of running blind when `modal billing report` fails or returns unreadable data.
- Segment duration stable-diffusion-image-generationping when max-runtime remaining is shorter than the normal 2h segment.

Reason: after a monthly reset, `modal billing report --for today` may return `[]` during the first active hour. A cap-only supervisor can overshoot if it relies only on lagging billing data. Hard runtime is the second guard.

## Fresh launch verification ladder

Within a few minutes of launch, verify all five surfaces before reporting `jalan`:

1. Hermes/background process is running.
2. Local process chain exists:
   - `akoya_continuous_supervisor.py`
   - `akoya_2h_watchdog.py`
   - `modal run akoya_modal.py`
3. Modal app list shows one active `akoya-pearl-*` app with `Tasks=1`.
4. Watchdog state is fresh and `ok=true` with no warning storm.
5. Akoya pool live state shows:
   - `is_online=true` / `instance_connected=true`
   - low `last_seen_age_seconds`
   - accepted shares increasing
   - `stale_shares24_h=0`
   - hashrate around the expected H100 band (~640 TH/s in this run)

Do not treat `pending_balance=0` in the first minutes as failure; PRL pool rewards have maturity/minimum-payout delay. Keep `accepted shares`, `pending`, and `total paid` as separate fields.

## Report shape to Galih

Terse state-first reply:

```text
jalan.
- cap: $30, grace $2, max runtime 8 jam
- Modal: <app id>, 1 task
- Akoya: online, <hashrate>, accepted <n>, stale <n>
- pending: <amount> PRL; total paid: <amount> PRL
- background: <session id>
- stop manual: touch /home/galyarder/experiments/modal-pearl/modal-pearl/.stop_mining
```

Avoid re-litigating already accepted ToS/credit-burn risk. Name only live gates: cap, billing lag, pool liveness, payout maturity, and stop command.

## Optional monitoring

If the user wants or the run will continue for hours, schedule a bounded watchdog report back to the origin chat (for example every 30 minutes for 16 repeats). The monitoring job must not recursively create jobs or increase cap; it reports state and stop commands only.
