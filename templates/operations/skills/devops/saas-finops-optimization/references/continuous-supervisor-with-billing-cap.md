# Continuous Supervisor with Billing Cap

Use this when the user explicitly approves continuous (indefinite) resource usage but spend must not exceed a hard cap. This sits above the bounded-experiment and liveness-watchdog patterns.

## Trigger

- User says something like "abisin aja creditnya", "jangan pernah mati", "keep it running", "run until credits are gone".
- The workload is already proven viable via a bounded test.
- The provider bills by usage (not flat subscription) and has no built-in spend cap, or the cap is higher than user wants.

## Architecture

Three-layer stack:

1. **Miner/workload process** — the actual GPU task (e.g. `modal run workload.py`).
2. **Liveness watchdog** (see `remote-workload-liveness-watchdogs.md`) — bounded 2h segment with 15-min rechecks, auto-restart on disconnect, hard timeout.
3. **Continuous supervisor** — spawns watchdog segments in a loop, checks billing between segments, stops when daily cap is reached.

```
supervisor (indefinite, cap-gated)
  └─ watchdog segment 1 (2h bounded, liveness-checked)
       └─ miner run 1.1
       └─ miner run 1.2 (auto-restart on disconnect)
  └─ watchdog segment 2
       └─ miner run 2.1
  └─ ... until cap reached or stop signal
```

## Confirmation gate

Before building a continuous supervisor, confirm:

1. **Hard daily spend cap** — ask user for a number. Modal CLI exposes `modal billing report --for today --json` but does NOT expose remaining credits directly. The billing report only shows cost incurred; remaining credit/balance must be inferred or checked via web dashboard.
2. **Credit-source reconciliation** — before treating remaining credits as “must burn before month end,” reconcile monthly writing-plans credits, grant remaining/expiry, and gross billing report. The remaining balance may be long-lived grant credit, not expiring monthly credit. See `modal-credit-accounting-prl-mining-2026-05-31.md`.
3. **Grace buffer** — stop when remaining < $2 (configurable) to avoid overshoot since billing data can lag.
4. **Stop mechanism** — at least two: signal (SIGTERM/SIGINT) and stop file (touch `.stop_mining`).

## Cost check pattern

```python
from decimal import Decimal

def get_today_cost() -> Decimal:
    """Query provider billing for today's workload cost."""
    cp = subprocess.run(
        ["modal", "billing", "report", "--for", "today", "-r", "h", "--tz", "local", "--json"],
        capture_output=True, text=True, timeout=90, env={"HOME": "/home/galyarder", ...}
    )
    data = json.loads(cp.stdout)
    return sum(
        (Decimal(str(row["Cost"])) for row in data if "workload-name" in row.get("Description", "").lower()),
        Decimal("0"),
    )

# In supervisor loop:
cost = get_today_cost()
remaining = DAILY_CAP - cost
if remaining <= GRACE_BUFFER:
    stop_all_apps()
    break
```

## Supervisor loop pattern

```python
segment_num = 0
while not shutdown_requested:
    if stop_file_exists():
        break
    cost = get_today_cost()
    if DAILY_CAP - cost <= GRACE_BUFFER:
        break
    segment_num += 1
    run_watchdog_segment(segment_num)  # blocks for segment_duration
    time.sleep(30)  # settle between segments
# Final cleanup: stop all provider apps, snapshot pool/billing, log
```

## Pitfalls

1. **Billing data lags** — Modal billing report may not include the current hour's cost until the hour closes. The grace buffer ($2) exists to absorb this lag. Do not set grace to $0.
2. **Segment handoff gap** — between segments, the miner is briefly offline (cleanup + restart). Pool may show `is_online=false` for 30-60 seconds. This is expected, not a failure.
3. **Provider may stop accepting workloads** — if credits are exhausted, `modal run` will fail at startup. The watchdog treats this as a failed segment and the supervisor eventually hits max-restart or cap-check.
4. **Duplicate apps** — each watchdog segment should clean up previous apps before starting. The pre-run cleanup step in the watchdog prevents duplicate billing.
5. **Don't confuse "keep running" with "no safety"** — user approving continuous usage still expects a hard cap. Always ask for the cap number before building the supervisor.

## Stop methods

| Method | How | When |
|---|---|---|
| Stop file | `touch .stop_mining` | Clean stop after current check |
| Signal | `kill <supervisor-pid>` | Clean stop with final cleanup |
| Hard kill | `kill -9 <supervisor-pid>` then manually `modal app stop <id> -y` | Emergency only |

## Logs

The supervisor produces three log layers:
- `akoya_supervisor_<timestamp>.log` — supervisor-level: segment starts, cost checks, cap decisions.
- `akoya_watchdog_2h_seg<N>_<timestamp>.log` — per-segment: liveness checks, restart decisions.
- `akoya_modal_watchdog_2h_seg<N>_<timestamp>_run<M>.log` — per-miner-run: raw miner output, hashrate, shares.

## Reference implementation

See `/home/galyarder/experiments/modal-pearl/modal-pearl/akoya_continuous_supervisor.py` (supervisor) and `akoya_2h_watchdog.py` (watchdog segment).
