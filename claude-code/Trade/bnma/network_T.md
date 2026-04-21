# Network: T Group

**Variables:** 9
**Study rows:** 16

## Nodes

- **V009** — TSMOM [A, Tier 1, Cross-Asset] (5 studies)
- **V010** — Revision breadth [A, Tier 1, Equities] (2 studies)
- **V014** — BTC exchange netflows [A, Tier 1, Crypto] (1 studies)
- **V017** — BTC ETF net flows [B, Tier 1, Crypto] (1 studies)
- **V026** — Residual momentum (FF5) [A, Tier 1, Equities] (3 studies)
- **C008** — Fear & Greed Index [Candidate-WP, Tier 3, Equities] (1 studies)
- **C009** — Token unlock pressure [Candidate-WP, Tier 3, Crypto] (1 studies)
- **C010** — Short-period RSI (2-5d) [Candidate-WP, Tier 3, Equities] (1 studies)
- **C011** — Whale accumulation ratio [Candidate-WP, Tier 3, Crypto] (1 studies)

## Edges (head-to-head studies)

No direct head-to-head comparisons found within a single study for this group. All variables are connected to the common asset-class benchmark node only.

## Peer Map (correlation ≥ 0.5 declared or inferred)

- V009 (TSMOM) ↔ V026
- V014 (BTC exchange netflows) ↔ V017
- V017 (BTC ETF net flows) ↔ V014
- V026 (Residual momentum (FF5)) ↔ V009
- C009 (Token unlock pressure) ↔ V014
- C010 (Short-period RSI (2-5d)) ↔ V009
- C011 (Whale accumulation ratio) ↔ V014, V017

## Pooling Rationale

Cross-asset pooling within this group rests on common-scale (annualized Sharpe of long-short portfolio) + asset-class intercept `alpha_a`. This is NOT indirect evidence chains — each variable is measured independently.
