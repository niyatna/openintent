---
name: cfo
description: "CFO operations: capital management, burn rate, runway, cost optimization, cashout/liquidation gates, and fundraising coordination."
version: 1.0.0
author: Company
license: MIT
metadata:
  hermes:
    tags: [finance, cfo, capital, runway, economics, tokens, cashout, fundraising]
    category: company-operations
---

# Chief Financial Officer (CFO)

The CFO skill manages capital command, cashflow, burn rate, token economics, cost optimization, and fundraising operations.

---

## 1. When to Use
- Analyzing company runway, burn rate, and capital allocations
- Optimizing server, API, and token costs (FinOps logic)
- Reviewing Unit Economics (LTV, CAC, payback periods)
- Designing or auditing investor pipeline and fundraising outreach
- Confirming transaction and transfer gates before broadcasting financial movements

---

## 2. Decision Lens
Evaluate all financial proposals through:
- **Cost**: What is the direct monetary/token cost and time exposure?
- **ROI**: What is the expected return, risk reduction, or leverage gained?
- **Blast Radius**: What is the risk of capital loss or lockup?

---

## 3. Financial Movements & Cashout Gates
For any transfer or spot liquidation of corporate/speculative assets:
1. **Wallet Balance Verification**: Confirm the on-chain wallet balance from public APIs.
2. **Gross Quote Calculation**: Run the math `balance × price = gross amount` before deducting network fees, exchange spread, and slippage.
3. **Audit Path Confirmation**: Map the path (local wallet → exchange deposit address → spot pair spot-sale → target asset).
4. **Approval Gate**: Present the final details (amount, destination, network fee, expected received amount) and require explicit Owner confirmation before broadcasting.

---

## 4. References & Sub-playbooks
- `references/fundraising-operator.md` — Investor pipeline mapping, pitch deck strategy, and CRM outreach templates.
