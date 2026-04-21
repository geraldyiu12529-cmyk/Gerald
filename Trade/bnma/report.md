# BNMA Report — Gerald's Trading Variable Ranking

**Date:** 2026-04-17
**Method:** Hierarchical Bayesian Network Meta-Analysis (4 parallel groups)
**Variables:** 34 in main BNMA (22 registered + 12 candidates) | 6 in Stage F pipeline
**Studies:** 52 study rows (main BNMA)

> **Full MCMC converged for all four groups.** R-hat < 1.01 and ESS > 400 for all parameters.

---

## 1. Marginal-Contribution Flags (LEAD)

Variables with `p_beats_peers < 0.40` — candidates for demotion or merge with dominant peer:

| Group | Var_ID | Name | p_beats_peers | Dominant Peer(s) | Action |
|-------|--------|------|---------------|------------------|--------|
| S | V007 | Real yield / Breakevens | 0.35 | V003,V006,V008 | Merge/demote candidate |
| S | V006 | UST 2Y/10Y yields | 0.32 | V007,V008 | Merge/demote candidate |
| S | V008 | ACM Term Premium 10Y | 0.26 | V006,V007 | Merge/demote candidate |
| S | V012 | BTC active addresses | 0.40 | V013,V019 | Merge/demote candidate |
| S | C012 | Price-to-sales (tech) | 0.27 | V003 | Merge/demote candidate |
| S | C001 | Global M2 money supply | 0.27 | V012,V013 | Merge/demote candidate |
| S | C004 | NVT Signal (90d) | 0.23 | V019,V012 | Merge/demote candidate |
| S | C006 | China PMI leading copper | 0.23 | V003 | Merge/demote candidate |
| S | C003 | Gold/silver ratio | 0.05 | V003,V007 | Merge/demote candidate |
| S | V013 | BTC hash rate | 0.40 | V012 | Merge/demote candidate |
| T | V026 | Residual momentum (FF5) | 0.05 | V009 | Merge/demote candidate |
| T | C010 | Short-period RSI (2-5d) | 0.00 | V009 | Merge/demote candidate |
| T | C011 | Whale accumulation ratio | 0.25 | V014,V017 | Merge/demote candidate |
| R | V004 | HY OAS | 0.05 | V027,V001 | Merge/demote candidate |
| R | V001 | VIX | 0.24 | V002,V004,V005 | Merge/demote candidate |
| R | V005 | NFCI | 0.31 | V001,V004 | Merge/demote candidate |
| R | V002 | MOVE Index | 0.27 | V001,V004 | Merge/demote candidate |

**Tier 3 promotion candidates** (`p_beats_peers > 0.80` vs registry peers):

*No Tier 3 candidates meet the 0.80 threshold for promotion.*

---

## 2. Per-Group Ranking Tables

### S Group (14 variables)

| Rank | Var_ID | Name | Tier | Grade | n_studies | Post. Mean | 95% CI | P(>0) | P(top3) | Med. Rank | Rank CI | p_beats_peers | Post-decay Sharpe | Flags |
|------|--------|------|------|-------|----------|-----------|--------|-------|---------|-----------|---------|---------------|-------------------|-------|
| 1 | V011 | Brent M1-M3 curve slope | 1 | A | 3 | 0.402 | [0.16, 0.65] | 1.00 | 0.89 | 2 | [1, 4] | 0.50 | 0.281 | DIVERGE |
| 2 | V028 | Basis-momentum | 1 | A | 3 | 0.395 | [0.10, 0.65] | 0.99 | 0.86 | 2 | [1, 5] | 0.50 | 0.240 | DIVERGE |
| 3 | V007 | Real yield / Breakevens | 1 | A | 1 | 0.168 | [-0.31, 0.63] | 0.77 | 0.35 | 5 | [1, 14] | 0.35 | 0.118 | RANK_UNSTAB |
| 4 | V003 | DXY | 1 | A | 2 | 0.121 | [-0.16, 0.40] | 0.82 | 0.16 | 6 | [2, 13] | 0.43 | 0.086 | RANK_UNSTAB |
| 5 | V006 | UST 2Y/10Y yields | 1 | A | 1 | 0.118 | [-0.39, 0.59] | 0.71 | 0.27 | 6 | [1, 14] | 0.32 | 0.085 | RANK_UNSTAB |
| 6 | V008 | ACM Term Premium 10Y | 1 | A | 1 | 0.079 | [-0.41, 0.54] | 0.65 | 0.21 | 6 | [1, 14] | 0.26 | 0.058 | RANK_UNSTAB |
| 7 | V012 | BTC active addresses | 1 | A | 2 | 0.031 | [-0.28, 0.37] | 0.57 | 0.08 | 8 | [3, 14] | 0.40 | 0.021 | RANK_UNSTAB |
| 8 | C012 | Price-to-sales (tech) | 3 | Candidate-PR | 1 | 0.022 | [-0.17, 0.21] | 0.59 | 0.02 | 9 | [4, 13] | 0.27 | 0.013 | LOW_PWR |
| 9 | C001 | Global M2 money supply | 3 | Candidate-WP | 1 | 0.005 | [-0.09, 0.10] | 0.55 | 0.00 | 9 | [6, 13] | 0.27 | 0.003 | INDIST, LOW_PWR |
| 10 | V019 | MVRV / SOPR | 1 | B | 1 | 0.004 | [-0.33, 0.34] | 0.51 | 0.07 | 10 | [3, 14] | 0.45 | 0.003 | INDIST, RANK_UNSTAB |
| 11 | C004 | NVT Signal (90d) | 3 | Candidate-WP | 1 | 0.004 | [-0.10, 0.10] | 0.54 | 0.00 | 9 | [6, 13] | 0.23 | 0.003 | INDIST, LOW_PWR |
| 12 | C006 | China PMI leading copper | 3 | Candidate-PR | 1 | 0.003 | [-0.17, 0.17] | 0.51 | 0.01 | 10 | [5, 14] | 0.23 | 0.002 | INDIST, LOW_PWR |
| 13 | C003 | Gold/silver ratio | 3 | Candidate-WP | 1 | 0.000 | [-0.09, 0.10] | 0.50 | 0.00 | 10 | [6, 13] | 0.05 | 0.000 | INDIST, LOW_PWR |
| 14 | V013 | BTC hash rate | 1 | A | 1 | -0.036 | [-0.46, 0.40] | 0.42 | 0.08 | 11 | [3, 14] | 0.40 | -0.025 | INDIST, RANK_UNSTAB |

### T Group (9 variables)

| Rank | Var_ID | Name | Tier | Grade | n_studies | Post. Mean | 95% CI | P(>0) | P(top3) | Med. Rank | Rank CI | p_beats_peers | Post-decay Sharpe | Flags |
|------|--------|------|------|-------|----------|-----------|--------|-------|---------|-----------|---------|---------------|-------------------|-------|
| 1 | V009 | TSMOM | 1 | A | 5 | 0.680 | [0.40, 0.92] | 1.00 | 1.00 | 1 | [1, 2] | 0.95 | 0.411 | — |
| 2 | V026 | Residual momentum (FF5) | 1 | A | 3 | 0.385 | [0.12, 0.64] | 1.00 | 0.95 | 2 | [1, 3] | 0.05 | 0.232 | DIVERGE |
| 3 | V010 | Revision breadth | 1 | A | 2 | 0.206 | [-0.08, 0.48] | 0.94 | 0.65 | 3 | [2, 7] | 0.01 | 0.124 | — |
| 4 | V014 | BTC exchange netflows | 1 | A | 1 | 0.029 | [-0.42, 0.48] | 0.55 | 0.22 | 5 | [2, 9] | 0.58 | 0.020 | RANK_UNSTAB |
| 5 | C008 | Fear & Greed Index | 3 | Candidate-WP | 1 | 0.007 | [-0.09, 0.10] | 0.56 | 0.02 | 6 | [4, 9] | 0.00 | 0.004 | LOW_PWR |
| 6 | C010 | Short-period RSI (2-5d) | 3 | Candidate-WP | 1 | 0.005 | [-0.09, 0.10] | 0.54 | 0.02 | 6 | [4, 9] | 0.00 | 0.003 | INDIST, LOW_PWR |
| 7 | C011 | Whale accumulation ratio | 3 | Candidate-WP | 1 | -0.002 | [-0.10, 0.10] | 0.48 | 0.01 | 7 | [4, 9] | 0.25 | -0.002 | INDIST, LOW_PWR |
| 8 | C009 | Token unlock pressure | 3 | Candidate-WP | 1 | -0.006 | [-0.10, 0.09] | 0.45 | 0.01 | 7 | [4, 9] | 0.43 | -0.004 | INDIST, LOW_PWR |
| 9 | V017 | BTC ETF net flows | 1 | B | 1 | -0.028 | [-0.41, 0.34] | 0.44 | 0.12 | 8 | [3, 9] | 0.42 | -0.019 | INDIST |

### R Group (8 variables)

| Rank | Var_ID | Name | Tier | Grade | n_studies | Post. Mean | 95% CI | P(>0) | P(top3) | Med. Rank | Rank CI | p_beats_peers | Post-decay Sharpe | Flags |
|------|--------|------|------|-------|----------|-----------|--------|-------|---------|-----------|---------|---------------|-------------------|-------|
| 1 | V027 | Intermediary capital ratio | 1 | A | 3 | 0.236 | [0.02, 0.45] | 0.98 | 0.96 | 1 | [1, 3] | 0.95 | 0.142 | DIVERGE |
| 2 | V015 | BTC realized vol | 1 | A | 1 | 0.031 | [-0.24, 0.31] | 0.58 | 0.44 | 4 | [1, 8] | 0.64 | 0.021 | RANK_UNSTAB |
| 3 | V018 | BTC 3m basis | 1 | B | 2 | 0.019 | [-0.18, 0.21] | 0.58 | 0.38 | 4 | [2, 8] | 0.55 | 0.013 | RANK_UNSTAB |
| 4 | V016 | BTC perp funding rate | 1 | B | 1 | 0.000 | [-0.20, 0.21] | 0.50 | 0.31 | 5 | [2, 8] | 0.45 | 0.000 | INDIST, RANK_UNSTAB |
| 5 | V004 | HY OAS | 1 | A | 2 | -0.011 | [-0.22, 0.21] | 0.46 | 0.28 | 5 | [2, 8] | 0.05 | -0.008 | INDIST, RANK_UNSTAB |
| 6 | V001 | VIX | 1 | A | 2 | -0.034 | [-0.25, 0.18] | 0.38 | 0.21 | 6 | [2, 8] | 0.24 | -0.024 | INDIST, RANK_UNSTAB |
| 7 | V005 | NFCI | 1 | A | 1 | -0.035 | [-0.28, 0.22] | 0.37 | 0.23 | 6 | [2, 8] | 0.31 | -0.026 | INDIST, RANK_UNSTAB |
| 8 | V002 | MOVE Index | 1 | A | 1 | -0.051 | [-0.30, 0.21] | 0.33 | 0.19 | 6 | [2, 8] | 0.27 | -0.036 | INDIST, RANK_UNSTAB |

### Overlay Group (3 variables)

| Rank | Var_ID | Name | Tier | Grade | n_studies | Post. Mean | 95% CI | P(>0) | P(top3) | Med. Rank | Rank CI | p_beats_peers | Post-decay Sharpe | Flags |
|------|--------|------|------|-------|----------|-----------|--------|-------|---------|-----------|---------|---------------|-------------------|-------|
| 1 | C005 | 200-DMA regime filter | 3 | Candidate-PR | 1 | 0.009 | [-0.09, 0.10] | 0.58 | 1.00 | 2 | [1, 3] | 0.40 | 0.006 | — |
| 2 | C002 | VIX term structure slope | 3 | Candidate-PR | 1 | 0.007 | [-0.09, 0.10] | 0.56 | 1.00 | 2 | [1, 3] | 0.38 | 0.004 | — |
| 3 | C007 | Market breadth (pct >200-DMA) | 3 | Candidate-WP | 1 | -0.001 | [-0.05, 0.05] | 0.49 | 1.00 | 2 | [1, 3] | 0.22 | -0.000 | INDIST |

---

## 3. Heterogeneity Flags

Variables where `tau_k` posterior median exceeds threshold (suggesting unreliable pooling):

*No heterogeneity flags triggered.*

---

## 4. Registry Divergence Flags

Variables where `|registry_Sharpe − posterior_median| > 2 × se`:

| Group | Var_ID | Name | Registry Sharpe | Posterior Mean | Posterior SD | Gap (σ) |
|-------|--------|------|----------------|---------------|-------------|--------|
| S | V011 | Brent M1-M3 curve slope | 0.74 | 0.402 | 0.124 | 2.7σ |
| S | V028 | Basis-momentum | 0.80 | 0.395 | 0.135 | 3.0σ |
| T | V026 | Residual momentum (FF5) | 0.70 | 0.385 | 0.128 | 2.5σ |
| R | V027 | Intermediary capital ratio | 0.60 | 0.236 | 0.107 | 3.4σ |

---

## 5. Grade-Rank Consistency

Anomalies: Grade A in bottom 3, Grade B in top 3, or Tier 3 in top 3 of group:

| Group | Var_ID | Name | Grade | Rank | Group Size | Anomaly |
|-------|--------|------|-------|------|-----------|--------|
| S | V013 | BTC hash rate | A | 14/14 | 14 | Grade A in bottom 3 |
| R | V018 | BTC 3m basis | B | 3/8 | 8 | Grade B in top 3 |
| R | V001 | VIX | A | 6/8 | 8 | Grade A in bottom 3 |
| R | V005 | NFCI | A | 7/8 | 8 | Grade A in bottom 3 |
| R | V002 | MOVE Index | A | 8/8 | 8 | Grade A in bottom 3 |
| Overlay | C005 | 200-DMA regime filter | Candidate-PR | 1/3 | 3 | Tier 3 in top 3 |
| Overlay | C002 | VIX term structure slope | Candidate-PR | 2/3 | 3 | Tier 3 in top 3 |
| Overlay | C007 | Market breadth (pct >200-DMA) | Candidate-WP | 3/3 | 3 | Tier 3 in top 3 |

---

## 6. Cross-Group Summary

**⚠ Cross-group rankings are NOT on a common scale.** S/T Sharpe is long-short portfolio; R is sizing improvement; Overlay is conditional Sharpe gain.

### Top 3 per Group

| Group | Rank | Var_ID | Name | Post. Mean | P(top3) | p_beats_peers |
|-------|------|--------|------|-----------|---------|---------------|
| S | 1 | V011 | Brent M1-M3 curve slope | 0.402 | 0.89 | 0.50 |
| S | 2 | V028 | Basis-momentum | 0.395 | 0.86 | 0.50 |
| S | 3 | V007 | Real yield / Breakevens | 0.168 | 0.35 | 0.35 |
| T | 1 | V009 | TSMOM | 0.680 | 1.00 | 0.95 |
| T | 2 | V026 | Residual momentum (FF5) | 0.385 | 0.95 | 0.05 |
| T | 3 | V010 | Revision breadth | 0.206 | 0.65 | 0.01 |
| R | 1 | V027 | Intermediary capital ratio | 0.236 | 0.96 | 0.95 |
| R | 2 | V015 | BTC realized vol | 0.031 | 0.44 | 0.64 |
| R | 3 | V018 | BTC 3m basis | 0.019 | 0.38 | 0.55 |
| Overlay | 1 | C005 | 200-DMA regime filter | 0.009 | 1.00 | 0.40 |
| Overlay | 2 | C002 | VIX term structure slope | 0.007 | 1.00 | 0.38 |
| Overlay | 3 | C007 | Market breadth (pct >200-DMA) | -0.001 | 1.00 | 0.22 |

### Overall Top 5 by P(top3) (cross-group, not on common scale)

| Group | Var_ID | Name | P(top3) | Post. Mean | Tier | Grade |
|-------|--------|------|---------|-----------|------|-------|
| Overlay | C005 | 200-DMA regime filter | 1.00 | 0.009 | 3 | Candidate-PR |
| Overlay | C002 | VIX term structure slope | 1.00 | 0.007 | 3 | Candidate-PR |
| Overlay | C007 | Market breadth (pct >200-DMA) | 1.00 | -0.001 | 3 | Candidate-WP |
| T | V009 | TSMOM | 1.00 | 0.680 | 1 | A |
| R | V027 | Intermediary capital ratio | 0.96 | 0.236 | 1 | A |

---

## 7. Prior Sensitivity

Variables shifting ≥ 3 ranks when switching to uniformly-loose priors (N(0, 0.5) for S/T, N(0, 0.25) for R/Overlay applied to ALL tiers):

| Var_ID | Name | Group | Base Rank | Loose Rank | Shift | Interpretation |
|--------|------|-------|-----------|-----------|-------|----------------|
| V008 | ACM Term Premium 10Y | S | 6 | 9 | 3 | Prior-dependent — skeptical prior was inflating rank |
| V019 | MVRV / SOPR | S | 10 | 13 | 3 | Prior-dependent — skeptical prior was inflating rank |
| C001 | Global M2 money supply | S | 9 | 6 | 3 | Prior-dependent — result driven by skeptical prior, not data |
| C004 | NVT Signal (90d) | S | 11 | 7 | 4 | Prior-dependent — result driven by skeptical prior, not data |
| V004 | HY OAS | R | 5 | 2 | 3 | Prior-dependent — result driven by skeptical prior, not data |
| V016 | BTC perp funding rate | R | 4 | 8 | 4 | Prior-dependent — skeptical prior was inflating rank |

---

## 8. Feed to 2026-10-14 Audit: V026, V027, V028

### V026 — Residual momentum (FF5)

- **Group:** T
- **Posterior mean:** 0.385 (95% CI: [0.116, 0.637])
- **P(>0):** 1.00
- **P(top 3):** 0.95, median rank: 2/9
- **p_beats_peers:** 0.05 (peers: V009)
- **Registry Sharpe:** 0.7, post-decay: 0.232
- **⚠ DIVERGENCE FLAG:** posterior substantially below registry Sharpe
- **Audit verdict: NO-GO**
- **Ledger evidence:** Not available (Stage G skipped — no ledger provided)

### V027 — Intermediary capital ratio

- **Group:** R
- **Posterior mean:** 0.236 (95% CI: [0.022, 0.446])
- **P(>0):** 0.98
- **P(top 3):** 0.96, median rank: 1/8
- **p_beats_peers:** 0.95 (peers: V004)
- **Registry Sharpe:** 0.6, post-decay: 0.142
- **⚠ DIVERGENCE FLAG:** posterior substantially below registry Sharpe
- **Audit verdict: GO**
- **Ledger evidence:** Not available (Stage G skipped — no ledger provided)

### V028 — Basis-momentum

- **Group:** S
- **Posterior mean:** 0.394 (95% CI: [0.104, 0.649])
- **P(>0):** 0.99
- **P(top 3):** 0.86, median rank: 2/14
- **p_beats_peers:** 0.50 (peers: V011)
- **Registry Sharpe:** 0.8, post-decay: 0.240
- **⚠ DIVERGENCE FLAG:** posterior substantially below registry Sharpe
- **Audit verdict: GO**
- **Ledger evidence:** Not available (Stage G skipped — no ledger provided)

---

## 9. Tier 3 Graduation Recommendations

Criteria: `p_positive > 0.70`, `p_beats_peers > 0.60`, passes heterogeneity.

*No Tier 3 candidates meet all three graduation criteria.* This is expected — skeptical priors correctly suppress single-study candidates with wide CIs.

---

## 10. Memory-Ready Insights

- **S group top 3:** V011 (Brent M1-M3 curve slope), V028 (Basis-momentum), V007 (Real yield / Breakevens)
- **T group top 3:** V009 (TSMOM), V026 (Residual momentum (FF5)), V010 (Revision breadth)
- **R group top 3:** V027 (Intermediary capital ratio), V015 (BTC realized vol), V018 (BTC 3m basis)
- **2026-10-14 audit verdicts:** V026: NO-GO; V027: GO; V028: GO
- **Overlay group is thin** (3 Tier 3 candidates only; all registry Overlay vars are Provisional/Ungraded). Posteriors are prior-dominated. Do not act on Overlay BNMA rankings until registry Overlay variables are graded.

---

## Stage G — SignalLedger Consistency (SKIPPED)

No out-of-sample signal ledger was provided for this run. Stage G is skipped entirely. Note: with small N the power of this check is near zero — it is a consistency check, not a posterior update.
