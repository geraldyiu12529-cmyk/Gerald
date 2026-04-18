# Network: R Group

**Variables:** 8
**Study rows:** 13

## Nodes

- **V001** — VIX [A, Tier 1, Cross-Asset] (2 studies)
- **V002** — MOVE Index [A, Tier 1, Cross-Asset] (1 studies)
- **V004** — HY OAS [A, Tier 1, Cross-Asset] (2 studies)
- **V005** — NFCI [A, Tier 1, Cross-Asset] (1 studies)
- **V015** — BTC realized vol [A, Tier 1, Crypto] (1 studies)
- **V016** — BTC perp funding rate [B, Tier 1, Crypto] (1 studies)
- **V018** — BTC 3m basis [B, Tier 1, Crypto] (2 studies)
- **V027** — Intermediary capital ratio [A, Tier 1, Cross-Asset] (3 studies)

## Edges (head-to-head studies)

No direct head-to-head comparisons found within a single study for this group. All variables are connected to the common asset-class benchmark node only.

## Peer Map (correlation ≥ 0.5 declared or inferred)

- V001 (VIX) ↔ V002, V004, V005
- V002 (MOVE Index) ↔ V001, V004
- V004 (HY OAS) ↔ V027, V001
- V005 (NFCI) ↔ V001, V004
- V015 (BTC realized vol) ↔ V001
- V016 (BTC perp funding rate) ↔ V018
- V018 (BTC 3m basis) ↔ V016
- V027 (Intermediary capital ratio) ↔ V004

## Pooling Rationale

Cross-asset pooling within this group rests on common-scale (annualized Sharpe of Sharpe improvement from vol-targeting/sizing) + asset-class intercept `alpha_a`. This is NOT indirect evidence chains — each variable is measured independently.
