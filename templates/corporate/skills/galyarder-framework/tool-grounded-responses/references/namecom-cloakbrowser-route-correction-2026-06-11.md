# Name.com CloakBrowser route/style correction — 2026-06-11

## What happened

Galih explicitly asked for Name.com checkout using CloakBrowser/headless and outcome only. The assistant:

- misread CloakBrowser install state because the wrapper cache path showed `Installed: False` while the real binary existed under `/home/galyarder/.cloakbrowser`;
- started an unnecessary reinstall;
- briefly controlled/inspected Galih's real Brave/desktop via computer-use even after CloakBrowser was requested;
- surfaced too much process narration instead of compact status;
- asked Galih to solve captcha too early before exhausting the requested headless CloakBrowser/session-cookie path.

## Durable response rule

When Galih says `pake CloakBrowser`, `headless`, or `hasilnya doang`:

1. Stay on the requested route. Do not switch to computer-use/real Brave unless Galih explicitly authorizes the route change.
2. Keep browser windows hidden/headless unless Galih asks to see them.
3. Try session/cookie continuity inside CloakBrowser before declaring a captcha/human gate.
4. Report status as `done / blocked / evidence`, not a long tool narrative.
5. If external checkout total is non-zero, promo invalid, domain missing, or unwanted cart items exist, stop before final order and say exactly which gate blocked completion.

## Compact status examples

```text
blocked: promo invalid.
evidence: checkout had galyarderlabs.dev, Name.com returned “That promo code appears to be invalid”, total stayed $35.37.
not clicked: final order.
```

```text
done: order completed.
evidence: confirmation page showed order id <id> for galyarderlabs.dev, total $0.00.
```
