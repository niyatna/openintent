# Cloud GPU Mining: Payout and Cashout Gates

Use this reference when evaluating speculative token mining or compute-credit salvage using cloud GPUs.

## Trigger

- User is mining or validating a token via rented/serverless GPUs.
- Pool/dashboard shows accepted shares, pending balance, or payout threshold.
- Token price/liquidity is volatile and the user asks whether to continue, scale, or cash out.

## Principle

Treat mining profitability as unproven until the full cash loop works:

`cloud GPU spend/credit -> accepted work -> matured pending -> pool payout -> local/native wallet balance -> exchange/OTC deposit -> sell to liquid quote asset -> withdraw route`

Accepted shares, hashrate, whitepaper quality, and dashboard pending balance are not enough. They are intermediate evidence only.

## Required gates before scaling

1. **Work proof** — accepted shares or equivalent useful-work metric is increasing and stale/reject rate is acceptable.
2. **Maturity proof** — pool pending balance increases after the expected maturity window.
3. **Payout proof** — pending crosses the minimum payout threshold and `total_paid` or payout history updates.
4. **Wallet proof** — native wallet balance/transaction confirms the payout landed at the configured wallet address.
5. **Exchange/OTC proof** — a small test deposit reaches the chosen venue on the correct chain/network.
6. **Sell proof** — a small amount sells into USDT/USDC/BTC or another liquid quote asset with acceptable slippage.
7. **Withdrawal proof** — funds can leave the venue to the user's desired cashout rail.

Do not increase budget/cap or turn a one-off credit burn into a repeatable operation before gates 3-6 are verified.

## Price handling

For volatile, thinly traded tokens:

- Separate **project thesis** from **token execution**. A serious whitepaper does not prove current token liquidity.
- Use live order book/deposit/sell-route data when available; search result snippets are weak evidence.
- Recalculate value at the current bid/realizable price, not ATH, last screenshot, or marketing price.
- If the token dumps during the experiment, do not chase. Shift from profit mode to proof-of-cashout mode.

## Native-wallet pitfall

Many early L1s do not pay to EVM wallets. Verify the pool payout address prefix and native wallet tooling first. If an EVM address is rejected by the pool, create/use a native wallet, keep seed/passphrase private, and point the miner to the native address only.

## Recommended response shape

```text
state:
- pending / paid / hashrate / spend cap / price basis

verdict:
- continue until payout proof / stop / cashout test / do not scale

why:
- project thesis vs token liquidity
- cost basis vs current realizable price

next move:
- exact smallest proof step
```

For multi-ledger cloud mining runs, see `references/cloud-gpu-mining-ledger-and-billing-reconciliation-2026-06.md`. Key rule: current holdings are usually **explorer/wallet current balance + pool pending**, not **pool total_paid + pending**; top-level available credit is the conservative runtime ceiling when billing ledgers disagree.

## Kill/stop conditions

Stop or avoid scaling when:

- payout threshold is not reached after reasonable maturity.
- payout lands but exchange deposit/sell route cannot be verified.
- realized price falls below cost basis if spending real cash rather than expiring credits.
- cloud spend risks hitting payment card or account suspension.
- pool or token liquidity becomes opaque, custodial-only, or dominated by OTC trust risk.
