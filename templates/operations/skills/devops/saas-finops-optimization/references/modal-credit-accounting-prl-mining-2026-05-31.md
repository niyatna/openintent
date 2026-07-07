# Modal Credit Accounting for PRL / Cloud-GPU Experiments

Session lesson from a Modal + Akoya PRL mining run where the user believed unused monthly credits were about to expire and considered burning the rest immediately.

## Facts verified in-session

- Modal credits screen showed:
  - Plan includes `$30` of credits each month.
  - Additional grant remaining: `$30.32 / $50`.
  - Grant activated `Jul 29, 2025`, expires `Jul 31, 2026`.
- Modal billing report for the Akoya app showed gross monthly usage of about `$49.6772`.
- Reconciliation:
  - Grant used = `$50 - $30.32 = $19.68`.
  - Monthly writing-plans credit `$30` + grant used `$19.68` ≈ `$49.68` gross usage.
- Therefore the visible remaining `$30.32` was likely long-lived grant credit, not monthly credit about to expire that night.
- `modal app list` showed no active apps/tasks before deciding whether to continue.

## Durable rule

Do not assume “remaining credits” are monthly credits expiring at the end of the current billing cycle. Reconcile three surfaces first:

1. Credits tab: monthly writing-plans credit statement, grant remaining, grant expiry.
2. Billing report: `modal billing report --for 'this month' --json` and/or `--for today -r h --tz local --json`.
3. Active remote state: `modal app list` must be empty or intentionally running.

If gross usage ≈ monthly writing-plans credit + grant used, the monthly credit may already be consumed and the remainder may be grant credit with a later expiry.

## Decision rule for compute-credit mining

Treat idle/free cloud credits as a research budget, not as cash profit:

- “Credit would otherwise sit idle” can justify a bounded experiment.
- It does not justify unbounded burn, card overage risk, or ignoring exchange/cashout proof.
- Keep a grace buffer because billing data can lag.
- If the remaining credit has a later expiry, do not rush-burn it because of a false “last day” premise.

## Suggested response shape

```text
state:
- screenshot credits: <monthly writing-plans, grant remaining, expiry>
- billing report gross usage: <amount>
- active apps/tasks: <none or app IDs>

reconciliation:
- grant used = grant_total - grant_remaining
- gross usage ≈ monthly_credit + grant_used ?

verdict:
- do not burn because of month-end if remainder is grant credit
- optional bounded run only if user explicitly wants research/experience

cap:
- conservative: $10–15
- aggressive: remaining_credit - $2 buffer
```

## PRL-specific economics note from this run

Observed paid PRL was `22.6012 PRL` for about `$49.68` gross Modal usage, or roughly `0.455 PRL / $ credit`. At an OTC price around `$0.8969`, this was about `$0.408 value / $ credit`. That made it useful as proof/learning, not profitable as cash-equivalent spend.
