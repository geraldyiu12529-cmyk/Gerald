# Network: S Group

**Variables:** 14
**Study rows:** 20

## Nodes

- **V003** — DXY [A, Tier 1, Cross-Asset] (2 studies)
- **V006** — UST 2Y/10Y yields [A, Tier 1, Rates] (1 studies)
- **V007** — Real yield / Breakevens [A, Tier 1, Rates] (1 studies)
- **V008** — ACM Term Premium 10Y [A, Tier 1, Rates] (1 studies)
- **V011** — Brent M1-M3 curve slope [A, Tier 1, Commodities] (3 studies)
- **V012** — BTC active addresses [A, Tier 1, Crypto] (2 studies)
- **V013** — BTC hash rate [A, Tier 1, Crypto] (1 studies)
- **V019** — MVRV / SOPR [B, Tier 1, Crypto] (1 studies)
- **V028** — Basis-momentum [A, Tier 1, Commodities] (3 studies)
- **C001** — Global M2 money supply [Candidate-WP, Tier 3, Crypto] (1 studies)
- **C003** — Gold/silver ratio [Candidate-WP, Tier 3, Commodities] (1 studies)
- **C004** — NVT Signal (90d) [Candidate-WP, Tier 3, Crypto] (1 studies)
- **C006** — China PMI leading copper [Candidate-PR, Tier 3, Commodities] (1 studies)
- **C012** — Price-to-sales (tech) [Candidate-PR, Tier 3, Equities] (1 studies)

## Edges (head-to-head studies)

No direct head-to-head comparisons found within a single study for this group. All variables are connected to the common asset-class benchmark node only.

## Peer Map (correlation ≥ 0.5 declared or inferred)

- V003 (DXY) ↔ V007
- V006 (UST 2Y/10Y yields) ↔ V007, V008
- V007 (Real yield / Breakevens) ↔ V003, V006, V008
- V008 (ACM Term Premium 10Y) ↔ V006, V007
- V011 (Brent M1-M3 curve slope) ↔ V028
- V012 (BTC active addresses) ↔ V013, V019
- V013 (BTC hash rate) ↔ V012
- V019 (MVRV / SOPR) ↔ V012
- V028 (Basis-momentum) ↔ V011
- C001 (Global M2 money supply) ↔ V012, V013
- C003 (Gold/silver ratio) ↔ V003, V007
- C004 (NVT Signal (90d)) ↔ V019, V012
- C006 (China PMI leading copper) ↔ V003
- C012 (Price-to-sales (tech)) ↔ V003

## Pooling Rationale

Cross-asset pooling within this group rests on common-scale (annualized Sharpe of long-short portfolio) + asset-class intercept `alpha_a`. This is NOT indirect evidence chains — each variable is measured independently.
