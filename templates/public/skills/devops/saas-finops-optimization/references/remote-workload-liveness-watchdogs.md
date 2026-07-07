# Remote Workload Liveness Watchdogs

Use this when a bounded cloud workload can appear locally "running" while the paid remote resource has stopped producing upstream work, or when the user explicitly asks to continue but make sure it is *actually* running.

## Trigger

- Paid remote GPU/job/miner/inference workload with previous idle-burn, disconnect, stale pool/dashboard, or non-continuous logs.
- User asks for rechecks during the run (for example every 15 minutes).
- Provider CLI process can remain alive even though upstream accounting no longer advances.

## Principle

A hard timeout prevents infinite spend, but it does not prove useful work continued. Pair the timeout with a liveness watchdog that checks multiple surfaces and can stop/restart early.

## Minimum watchdog surfaces

Track at least three independent signals:

1. **Provider resource state** — fresh list of app/job/container IDs, state, and active task count.
2. **Local process/log progress** — recent stats lines, accepted-work lines, hashrate/throughput, warning storms, and log modification time.
3. **Authoritative upstream state** — pool/API/dashboard/account address with online/offline state, last_seen age, accepted-work count, stale/rejected count, pending/paid balance when relevant.

Do not trust any single surface by itself:

- Local process alive is not proof of useful remote work.
- Provider task active is not proof the upstream accepted work.
- Accepted shares/requests are not proof of realized payout.
- Log streaming warnings can hide a dead/stale worker.

### Modal-specific: log discontinuity as disconnect signal

Modal emits `WARNING: Logs may not be continuous` when the log stream from the remote container breaks. A few of these during a long run can be benign (transient network). But 20+ warnings with no new stats/share lines means the container is effectively dead while the local CLI process keeps waiting. Treat `warning_count >= 20 AND no local log progress AND pool offline` as a hard failure requiring restart, not just a transient warning.

## Check cadence pattern

- Startup grace: short frequent checks (60-120s) until registration and first accepted work are visible.
- Regular checkpoint: user-requested interval (often 15 minutes) with full provider + upstream + log summary.
- Light check: optional 60s cheap check for stale/offline state or warning storms when the previous failure mode burned idle time.

## Failure conditions worth enforcing

Stop or restart before the hard timeout when one of these appears after startup grace:

- Upstream worker is offline/stale and `last_seen_age` exceeds a threshold.
- Provider task is active but local log stats/accepted-work count stopped advancing.
- Local log contains repeated discontinuity warnings with no new stats or upstream progress.
- Local process exited before the approved window and remaining time is still material.
- Provider app/job list shows no active task for the target workload.

If the remaining approved window is too short for a useful restart, stop and report instead of thrashing.

## Implementation shape

Prefer a small script over manual polling:

```text
pre-run cleanup -> start workload in background -> pump stdout/stderr to timestamped run log
-> every N seconds query provider/app list
-> query upstream account/API with browser-like headers if needed
-> parse run log for stats, accepted work, warnings
-> write latest JSON state atomically
-> stop/restart on stale/offline/no-progress
-> final cleanup -> re-list provider until terminal/zero tasks
```

Recommended outputs:

- `watchdog_<workload>_<duration>_<run_id>.log` — supervisory events and checkpoints.
- `<workload>_<duration>_<run_id>_run<N>.log` — raw workload logs per attempt/restart.
- `<workload>_watchdog_latest.json` — machine-readable latest state for quick inspection.

## Reporting to Galih

When Galih is angry about wasted time/cost, answer state first, not process:

- `jalan` / `mati` / `stale` / `restarting` / `stopped`
- provider active task count
- upstream online/connected + last_seen age
- accepted-work delta since start/checkpoint
- log paths and background session ID

Keep it terse. Do not re-litigate already accepted risks; name only the live gate and what the watchdog is doing.
