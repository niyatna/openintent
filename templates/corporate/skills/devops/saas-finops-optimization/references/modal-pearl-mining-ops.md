# Reference: saas-finops-optimization

- Pool size does not automatically improve long-run expected ROI per hash; it mainly reduces variance and speeds visible accounting. AlphaPool also has an extra `alpha-miner` dev fee if using its miner.

### Exact AlphaPool miner page and delayed-indexing pitfall

AlphaPool's SPA search route for an individual wallet uses a `#miner/<wallet>` hash, not `#miners`:

```text
https://pearl.alphapool.tech/#miner/<wallet>
```

The website may also produce a redundant-looking route after search:

```text
https://pearl.alphapool.tech/miner/<wallet>#miner/<wallet>
```

That route is valid because the SPA reads the hash. `#miners` is the **Top Miners** tab, not the wallet detail page; do not tell Galih to use `#miners` for his active worker detail. If the UI looks blank or routes oddly, verify with the authoritative API:

```text
https://pearl.alphapool.tech/api/miner/<wallet>
```

A fresh AlphaPool worker may be technically active before the wallet page/API is populated. Treat the first empty page as **indexing/accounting delay**, not immediate proof of failure. During startup grace:

1. Check Modal provider state (`ephemeral`, active tasks).
2. Read miner logs for pool connection, challenge solved, hashrate, `found_candidate`, and `share submitted`.
3. Poll `/api/miner/<wallet>` until `workers[]`, `shares24h`, `recent_shares`, and `balance_prl` appear.
4. Only after the startup grace expires without pool-side registration should the run be treated as stale or misconfigured.

Keep distinctions explicit in reporting: local `share submitted` proves the miner attempted submission; pool API `recent_shares[].valid=true` and `workers[].online=true` prove pool-side acceptance; `balance_prl` / pending payments prove maturity accounting; `total_paid_prl` proves payout.

Recommended move when Akoya has accepted shares but zero pending and AlphaPool looks stronger:

- `references/bounded-cloud-gpu-experiments.md` — use for speculative, cost-bearing remote GPU tests that need hard auto-stop, fresh remote cleanup verification, accepted-work metrics, and a separate payout/monetization proof gate before scaling.
- `references/remote-workload-liveness-watchdogs.md` — use when a paid remote workload previously went stale/disconnected while local/provider state still looked alive; pair hard timeout with provider + log + upstream liveness checks and stop/restart on stale/no-progress.
- `references/continuous-supervisor-with-billing-cap.md` — use when user explicitly approves indefinite/continuous resource burn; three-layer stack (miner → liveness watchdog → cost-gated supervisor loop) with daily spend cap, stop-file, and signal-based shutdown.
- `references/cloud-gpu-mining-payout-and-cashout-gates.md` — use for speculative cloud-GPU token mining or compute-credit salvage; requires full cash-loop proof (accepted work → matured pending → payout → native wallet → exchange/OTC deposit → sell/withdraw) before scaling.
- `references/modal-credit-accounting-prl-mining-2026-05-31.md` — use when Modal credit screens, grant balances, monthly writing-plans credits, and mining billing reports must be reconciled before deciding whether to burn remaining credits.
- `references/prl-modal-credit-reset-relaunch-2026-06-01.md` — use when relaunching the existing Akoya/Pearl PRL Modal miner after a credit reset with a bounded dollar cap, hard runtime guard, liveness checks, and terse state-first reporting.
- `references/prl-pool-comparison-akoya-alphapool-2026-06-01.md` — use when comparing Akoya vs AlphaPool for PRL mining after accepted shares but zero pending; includes discovered public APIs, fields, exact miner dashboard route, indexing-delay interpretation, and switch/proof heuristic.
- `references/alphapool-continuous-modal-supervisor-2026-06-01.md` — use when graduating the AlphaPool PRL proof into a continuous Modal-credit salvage run; includes the verified runner shape, workspace hard-cap correction, relaunch sequence, and live-state verification surfaces.
- `references/prl-alphapool-modal-proof-2026-06-01.md` — use when running a bounded AlphaPool Modal proof after Akoya variance; includes separate runner shape, timeout/cleanup pattern, visibility-lag pitfall, and state-first reporting format.