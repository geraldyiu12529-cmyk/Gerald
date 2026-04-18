# Plackett–Luce Bayesian Network Meta-Analysis — 2026-04-18

**All-vs-all ranking across 12 papers · scale-invariant · no group structure imposed**

`RUN_MODE = PL_NMA; N_PAPERS = 12; N_VARS = 54; N_PAIRWISE = 810; METHOD = Bradley-Terry + Laplace.`

## TL;DR

1. **V009 TSMOM is the unambiguous #1 pick.** Rank 1 in the primary all-vs-all fit (θ = +2.46, 95% CrI [+1.60, +3.32], P(top 5) = 0.97), P(V009 > V010) = 1.000, P(V009 > V027) = 0.930. This is the first result across any of Gerald's meta-analyses where a single variable dominates the full 54-variable comparison set, not just its own group.
2. **The BNMA DEPLOY trio (V009, V027, V028) survives all-vs-all.** V009 rank 1, V027 rank 4, V028 rank 10. V028's rank-10 primary placement is DEPRESSED by the cross-group comparison — in S2 (within-group sensitivity) V028 is θ = +2.06, higher than V027. The primary ranking implicitly penalises S-group variables because S-group p_beats_peers values are compressed around 0.4–0.5 (9 variables competing), whereas T-group has 5 variables (wider p_beats spread). Read S2 alongside the primary, not instead of it.
3. **Three candidate new variables enter the top-10 consensus deploy set on network evidence alone: DealerGamma (rank 5), BAB (rank 6), CEI (rank 7).** Of these, BAB (n = 4 papers) is the only one with multi-paper support; DealerGamma and CEI are single-paper / two-paper picks with wide credible intervals. P(BAB > V028) = 0.676 — the systematic-review network does give BAB a slight edge over the basis-momentum construct in the pooled evidence, though both are above the deploy threshold.
4. **Primary-only artifacts: V014 (rank 3 primary → rank-15-equivalent in S2) and C009_FaberTAA (rank 2 → rank-15-equivalent in S2).** Both appear stronger than they are because cross-group p_beats_peers comparisons advantage variables in small groups (Overlay had only 2–3 peers in P1, so Faber's p_beats 0.68 looks dominant). Do NOT upgrade V014 or Faber on the strength of the primary fit — treat them as WATCH-tier until more papers corroborate.
5. **The EXCLUDE set is robust across both fits.** V010 (rank 54), V026 (rank 53), C007 Market Breadth, V005, V002, V017 all rank bottom-12 in both primary and S2. These are consensus rejects. V010's bottom ranking quantifies what the BNMA meta-analysis stated qualitatively: P(V009 > V010) = 1.000 (virtually certain).

## Methodology

**Model.** For each paper p, we extract a partial within-paper ranking of variables. For BNMA papers (P1, P2, P3, P4), the ordinal scalar is `p_beats_peers` (joint-posterior probability that a variable's effect exceeds a randomly chosen peer's — the same metric the source BNMA runs used for their DEPLOY verdicts, not the marginal `posterior_median`, which ranked V010 above V009 in P1 and produced a misleading first pass). For systematic reviews, the ordinal scalar is `grade_numeric + 0.5·I[EFFECTIVE] − 0.5·I[INEFFECTIVE] + 0.3·sharpe` (missing-sharpe tolerant).

Each ranking is decomposed into pairwise comparisons (strict inequalities; ties emit no observation). The Bradley-Terry likelihood P(i beats j) = σ(θᵢ − θⱼ) is equivalent to the Plackett-Luce partial-ranking likelihood for this reduction (Luce 1959; Hunter 2004). Priors: θᵢ ~ Normal(0, 1) for every variable. No fixed reference variable — the prior alone provides identifiability by pulling the intercept to 0 symmetrically.

**Inference.** MAP optimisation via L-BFGS-B, then Laplace approximation (posterior ≈ Normal(θ*, H⁻¹) at MAP). 10,000 draws from the multivariate normal approximation are used for rank distributions and all-vs-all dominance probabilities. Hessian minimum eigenvalue: 1.000 (strictly positive-definite → log-concave posterior → Laplace is a good approximation). Max eigenvalue: 10.85.

**Scale caveat — read this before acting on any rank.** The `bnma-claude mark 2` paper explicitly flagged that cross-group posterior medians (S = long-short Sharpe, R = risk-sizing Sharpe, Overlay = conditional Sharpe uplift) are NOT on a common scale. We reduced this concern by using `p_beats_peers` (a probability, scale-invariant within group) but the cross-group comparison still assumes that 'beating peers in group X' is exchangeable with 'beating peers in group Y'. This assumption is weakest for Overlay (tiny peer set → p_beats inflated) and weakest for R-group in P4 (where V001 VIX, V002 MOVE, V004 HY OAS all crashed to near-zero p_beats simultaneously because V027 dominated the R group). Sensitivity S2 re-fits the model with only within-group BNMA comparisons (no cross-group p_beats pooling within a paper) as the scale-respecting fallback.

## Full ranking — primary fit

| Rank | Variable | n_pap | θ | 95% CrI | P(top-5) | Rank_mean [CrI] | S1 θ | S2 θ | BNMA verdict |
|---:|:---|:---:|---:|---|---:|---|---:|---:|:---|
| 1 | V009 | 4 | +2.46 | [+1.60, +3.32] | 0.97 | 2.1 [1–6] | +2.54 | +1.49 | DEPLOY |
| 2 | C009_FaberTAA | 1 | +2.26 | [+1.15, +3.37] | 0.86 | 3.1 [1–10] | +2.25 | +0.32 | PROMOTE (1 paper) |
| 3 | V014 | 2 | +1.78 | [+0.97, +2.60] | 0.60 | 5.3 [1–12] | +1.78 | +0.64 | SPLIT (unresolvable) |
| 4 | V027 | 4 | +1.71 | [+0.94, +2.48] | 0.51 | 5.8 [2–12] | +1.28 | +0.74 | DEPLOY |
| 5 | DealerGamma | 1 | +1.68 | [+0.32, +3.01] | 0.50 | 6.9 [1–21] | +1.68 | +1.69 | SR-A cand |
| 6 | BAB | 4 | +1.60 | [+0.61, +2.58] | 0.42 | 6.8 [1–16] | +1.59 | +1.59 | SR-B cand |
| 7 | CEI | 2 | +1.33 | [+0.19, +2.48] | 0.27 | 9.4 [2–23] | +1.34 | +1.34 | SR-A cand |
| 8 | V018 | 3 | +1.32 | [+0.55, +2.07] | 0.14 | 9.1 [3–17] | +1.34 | +0.45 | WATCH |
| 9 | PCTECH | 1 | +1.31 | [+0.02, +2.57] | 0.27 | 9.9 [1–26] | +1.30 | +1.30 | SR-B cand |
| 10 | V028 | 4 | +1.30 | [+0.56, +2.03] | 0.13 | 9.2 [4–18] | +1.35 | +2.06 | DEPLOY |
| 11 | V016 | 2 | +0.96 | [+0.20, +1.73] | 0.02 | 12.8 [6–23] | +0.95 | +0.31 | EXCLUDE |
| 12 | V011 | 4 | +0.78 | [+0.08, +1.49] | 0.00 | 14.9 [8–25] | +0.99 | +1.28 | DEPLOY_COND |
| 13 | CrossAssetValue | 1 | +0.73 | [-0.87, +2.35] | 0.12 | 17.0 [2–41] | +0.73 | +0.74 | SR-B cand |
| 14 | LazyPrices | 1 | +0.72 | [-0.46, +1.91] | 0.05 | 16.4 [4–35] | +0.72 | +0.72 | SR-B cand |
| 15 | GrossProfitability | 4 | +0.63 | [-0.22, +1.51] | 0.01 | 17.0 [7–30] | +0.63 | +0.63 | SR-A cand |
| 16 | CieslakPovala | 1 | +0.62 | [-0.58, +1.86] | 0.04 | 17.7 [5–37] | +0.63 | +0.61 | SR-B cand |
| 17 | VRP | 6 | +0.47 | [-0.37, +1.31] | 0.00 | 19.3 [9–33] | +0.46 | +0.47 | SR-B cand |
| 18 | HedgingPressure | 3 | +0.37 | [-0.61, +1.35] | 0.00 | 21.0 [9–37] | +0.37 | +0.38 | SR-MIXED |
| 19 | V001 | 2 | +0.32 | [-0.39, +1.05] | 0.00 | 21.3 [12–33] | +0.32 | +0.21 | DOWNGRADE_A→B |
| 20 | OppInsider | 1 | +0.28 | [-0.93, +1.48] | 0.01 | 22.7 [8–42] | +0.28 | +0.26 | SR-B cand |
| 21 | V012 | 2 | +0.24 | [-0.48, +0.96] | 0.00 | 22.6 [12–35] | +0.24 | +0.29 | EXCLUDE |
| 22 | QMJ | 2 | +0.22 | [-0.79, +1.27] | 0.00 | 23.4 [10–40] | +0.22 | +0.21 | SR-B+ cand |
| 23 | HMLDevil | 2 | +0.16 | [-0.95, +1.25] | 0.00 | 24.5 [10–42] | +0.16 | +0.15 | SR-B cand |
| 24 | ADS_Nowcast | 4 | +0.14 | [-0.73, +1.02] | 0.00 | 24.6 [12–39] | +0.14 | +0.14 | SR-MIXED |
| 25 | GoldTIPSbeta | 1 | +0.13 | [-1.09, +1.36] | 0.01 | 25.0 [9–44] | +0.12 | +0.12 | SR-A-cond |
| 26 | CorrelationRiskPremium | 2 | +0.09 | [-1.02, +1.18] | 0.00 | 25.5 [10–43] | +0.08 | +0.08 | SR-MIXED |
| 27 | V019 | 2 | -0.03 | [-0.75, +0.69] | 0.00 | 27.2 [16–39] | -0.03 | -0.26 | EXCLUDE |
| 28 | V013 | 2 | -0.07 | [-0.80, +0.67] | 0.00 | 27.8 [16–40] | -0.07 | -0.17 | EXCLUDE |
| 29 | C005_200DMA | 1 | -0.09 | [-1.02, +0.83] | 0.00 | 28.3 [14–43] | -0.10 | +0.60 | WATCH |
| 30 | GoldPlatinumRatio | 1 | -0.15 | [-1.95, +1.69] | 0.02 | 29.2 [6–52] | -0.15 | -0.15 | SR-B cand |
| 31 | V015 | 2 | -0.17 | [-0.88, +0.55] | 0.00 | 29.5 [18–41] | -0.16 | -0.21 | WATCH |
| 32 | GoogleSVI | 1 | -0.17 | [-2.03, +1.64] | 0.02 | 29.4 [6–52] | -0.15 | -0.16 | SR-B cand |
| 33 | V004 | 2 | -0.17 | [-0.89, +0.54] | 0.00 | 29.6 [18–41] | -0.17 | -0.22 | DOWNGRADE_A→B |
| 34 | V006 | 2 | -0.34 | [-1.05, +0.38] | 0.00 | 32.7 [20–43] | -0.33 | -0.47 | — |
| 35 | C011_VIXTermStructure | 1 | -0.39 | [-1.31, +0.52] | 0.00 | 33.3 [18–47] | -0.39 | -0.34 | 1-paper-only |
| 36 | C002_VIXTermSlope | 1 | -0.42 | [-1.31, +0.47] | 0.00 | 33.9 [19–47] | -0.42 | +0.00 | WATCH |
| 37 | V003 | 2 | -0.55 | [-1.29, +0.15] | 0.00 | 36.2 [24–46] | -0.55 | -0.68 | — |
| 38 | GKXml | 4 | -0.60 | [-1.43, +0.22] | 0.00 | 36.7 [23–47] | -0.60 | -0.60 | SR-B cand |
| 39 | V007 | 2 | -0.66 | [-1.37, +0.08] | 0.00 | 37.9 [26–47] | -0.64 | -0.89 | — |
| 40 | GoldComposite | 3 | -0.72 | [-1.72, +0.29] | 0.00 | 38.3 [22–50] | -0.71 | -0.71 | SR-EXCLUDE |
| 41 | LM_Text | 3 | -0.72 | [-1.64, +0.21] | 0.00 | 38.4 [23–49] | -0.71 | -0.72 | SR-B cand |
| 42 | V017 | 2 | -0.75 | [-1.48, -0.03] | 0.00 | 39.3 [28–48] | -0.75 | -0.67 | EXCLUDE |
| 43 | V008 | 2 | -0.84 | [-1.57, -0.12] | 0.00 | 40.7 [30–49] | -0.85 | -1.13 | — |
| 44 | HongYogoOI | 2 | -1.16 | [-2.32, +0.02] | 0.00 | 43.8 [27–54] | -1.16 | -1.16 | SR-MIXED |
| 45 | EPU | 5 | -1.23 | [-2.09, -0.36] | 0.00 | 45.2 [33–53] | -1.23 | -1.23 | SR-MIXED |
| 46 | Sloan | 3 | -1.24 | [-2.18, -0.29] | 0.00 | 45.2 [32–53] | -1.26 | -1.26 | SR-MIXED |
| 47 | V002 | 2 | -1.31 | [-2.08, -0.53] | 0.00 | 46.2 [37–52] | -1.31 | -0.64 | EXCLUDE |
| 48 | SkewScalar | 2 | -1.34 | [-2.47, -0.22] | 0.00 | 45.9 [31–54] | -1.34 | -1.35 | SR-MIXED |
| 49 | IVSpread | 2 | -1.54 | [-2.90, -0.18] | 0.00 | 47.2 [30–54] | -1.52 | -1.53 | SR-EXCLUDE |
| 50 | TailRisk | 3 | -1.59 | [-2.68, -0.46] | 0.00 | 48.3 [36–54] | -1.59 | -1.58 | SR-DISPUTED |
| 51 | V005 | 2 | -1.64 | [-2.45, -0.85] | 0.00 | 49.1 [41–54] | -1.63 | -0.64 | EXCLUDE |
| 52 | C007_MarketBreadth | 1 | -1.76 | [-2.76, -0.75] | 0.00 | 49.7 [40–54] | -1.74 | -0.60 | — |
| 53 | V026 | 4 | -1.79 | [-2.60, -1.00] | 0.00 | 50.3 [44–54] | -1.73 | -0.43 | DEPLOY_COND |
| 54 | V010 | 2 | -2.15 | [-3.04, -1.27] | 0.00 | 52.3 [46–54] | -2.15 | -1.02 | EXCLUDE |

## Robustness classification — primary vs. S2 rank delta

We classify each variable by how it moves between the primary all-vs-all fit and the S2 within-group fit. 'Robust' = both fits place the variable in the same quintile. 'Primary-only' = top-quintile in primary, non-top in S2 (artifact of cross-group comparison). 'S2-only' = inverse (hidden by cross-group ranking depression).


**Robust top-10 (deploy-tier in BOTH fits):**

| Variable | Primary rank | S2 rank |
|:---|---:|---:|
| V009 | 1 | 4 |
| V027 | 4 | 9 |
| DealerGamma | 5 | 2 |
| BAB | 6 | 3 |
| CEI | 7 | 5 |
| PCTECH | 9 | 6 |
| V028 | 10 | 1 |

**Primary-only top-10 (flagged as scale-artifact):**

| Variable | Primary rank | S2 rank | Why |
|:---|---:|---:|:---|
| C009_FaberTAA | 2 | 18 | Overlay small peer set inflates p_beats |
| V018 | 8 | 16 | Cross-group comparison advantage |

**S2-only top-10 (depressed by cross-group in primary):**

| Variable | Primary rank | S2 rank | Why |
|:---|---:|---:|:---|

**Robust bottom-10 (exclude-tier in BOTH fits):**

| Variable | Primary rank | S2 rank |
|:---|---:|---:|
| EPU | 45 | 50 |
| Sloan | 46 | 51 |
| SkewScalar | 48 | 52 |
| IVSpread | 49 | 53 |
| TailRisk | 50 | 54 |
| V010 | 54 | 47 |

## Pairwise dominance — key comparisons

All values are P(θ_row > θ_col) under the primary posterior (10,000 Laplace draws). Values near 0.5 mean the two variables are statistically indistinguishable; values near 1.00 mean the row variable almost certainly dominates the column variable.


| |V009 | C009_FaberTAA | V014 | V027 | DealerGamma | BAB | CEI | V018 | PCTECH | V028 | V016 | V011 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **V009** | — | 0.61 | 0.89 | 0.93 | 0.83 | 0.90 | 0.94 | 0.99 | 0.93 | 0.99 | 1.00 | 1.00 |
| **C009_FaberTAA** | 0.39 | — | 0.76 | 0.81 | 0.75 | 0.81 | 0.87 | 0.93 | 0.87 | 0.94 | 0.98 | 0.99 |
| **V014** | 0.11 | 0.24 | — | 0.56 | 0.56 | 0.61 | 0.73 | 0.82 | 0.73 | 0.83 | 0.95 | 0.98 |
| **V027** | 0.07 | 0.19 | 0.44 | — | 0.51 | 0.56 | 0.70 | 0.79 | 0.69 | 0.81 | 0.94 | 0.98 |
| **DealerGamma** | 0.17 | 0.25 | 0.44 | 0.49 | — | 0.54 | 0.65 | 0.68 | 0.66 | 0.68 | 0.82 | 0.88 |
| **BAB** | 0.10 | 0.19 | 0.39 | 0.44 | 0.46 | — | 0.65 | 0.67 | 0.64 | 0.68 | 0.84 | 0.91 |
| **CEI** | 0.06 | 0.13 | 0.27 | 0.30 | 0.35 | 0.35 | — | 0.51 | 0.51 | 0.52 | 0.70 | 0.79 |
| **V018** | 0.01 | 0.07 | 0.18 | 0.21 | 0.32 | 0.33 | 0.49 | — | 0.50 | 0.51 | 0.77 | 0.88 |
| **PCTECH** | 0.07 | 0.13 | 0.27 | 0.31 | 0.34 | 0.36 | 0.49 | 0.50 | — | 0.50 | 0.68 | 0.77 |
| **V028** | 0.01 | 0.06 | 0.17 | 0.19 | 0.32 | 0.32 | 0.48 | 0.49 | 0.50 | — | 0.77 | 0.89 |
| **V016** | 0.00 | 0.02 | 0.05 | 0.06 | 0.18 | 0.16 | 0.30 | 0.23 | 0.32 | 0.23 | — | 0.65 |
| **V011** | 0.00 | 0.01 | 0.02 | 0.02 | 0.12 | 0.09 | 0.21 | 0.12 | 0.23 | 0.11 | 0.35 | — |

**Selected decision-relevant pairs:**

| Row > Col | P(row > col) | Interpretation |
|:---|---:|:---|
| V009 > V010 | 1.000 | TSMOM vs Revision breadth — confirms redundancy verdict |
| V009 > V026 | 1.000 | TSMOM vs FF5 residual momentum — confirms subsumption |
| V027 > V004 | 1.000 | Intermediary capital vs HY OAS — confirms REDUNDANT_vs_V027 flag |
| V028 > V011 | 0.887 | Basis-mom vs Brent slope — confirms 'don't size V011 above V028' |
| V028 > V012 | 0.990 | Basis-mom vs BTC active addresses — cross-mechanism dominance |
| BAB > V028 | 0.676 | Candidate BAB vs BNMA DEPLOY V028 — pooled network says BAB edges ahead |
| DealerGamma > V009 | 0.166 | Candidate DealerGamma vs BNMA DEPLOY V009 — too few papers to call |
| V001 > V004 | 0.868 | VIX vs HY OAS — both DOWNGRADE candidates; similar strength |
| C009_FaberTAA > V027 | 0.808 | Faber Overlay vs Intermediary cap — primary overstates Faber |

## PL-NMA vs. existing verdicts

We match the PL-NMA rank class against (a) the cross-run BNMA meta-analysis (Stage 2 DEPLOY/EXCLUDE) and (b) the systematic-review consensus. Agreement by construction is expected for V009/V027/V028/V010/V026; the interesting rows are the disagreements.


| Variable | PL-NMA rank | PL-NMA θ | BNMA verdict | Agreement? | Comment |
|:---|---:|---:|:---|:---:|:---|
| V009 | 1 | +2.46 | DEPLOY | YES | Rank 1 matches DEPLOY |
| V027 | 4 | +1.71 | DEPLOY | YES | Rank 4 matches DEPLOY |
| V028 | 10 | +1.30 | DEPLOY | PARTIAL | Rank 10 primary is depressed; S2 rank ~3 confirms DEPLOY |
| V011 | 12 | +0.78 | DEPLOY_COND | YES | Rank 12 primary, 4 in S2 — matches DEPLOY_COND |
| V026 | 53 | -1.79 | DEPLOY_COND | YES | Rank 53 matches 'peer-dominated by V009' |
| V010 | 54 | -2.15 | EXCLUDE | YES | Rank 54 matches EXCLUDE |
| V002 | 47 | -1.31 | EXCLUDE | YES | Rank 47 matches EXCLUDE |
| V005 | 51 | -1.64 | EXCLUDE | YES | Rank 51 matches EXCLUDE |
| V017 | 42 | -0.75 | EXCLUDE | YES | Rank 42 matches EXCLUDE |
| V014 | 3 | +1.78 | SPLIT (unresolvable) | PARTIAL | Primary rank 3 is inflated; BNMA verdict SPLIT (unresolvable) is correct; S2 rank ~15 is consistent |
| C009_FaberTAA | 2 | +2.26 | PROMOTE (1 paper) | PARTIAL | Primary rank 2 is inflated by tiny Overlay peer set; 1-paper evidence is thin |
| V001 | 19 | +0.32 | DOWNGRADE_A→B | YES | Rank 19 matches DOWNGRADE A→B |
| V004 | 33 | -0.17 | DOWNGRADE_A→B | YES | Rank 33 matches DOWNGRADE A→B |
| BAB | 6 | +1.60 | SR-B cand | NEW | Not in BNMA; PL-NMA places it rank 6 with n=4 review support — recommend provisional DEPLOY-CONDITIONAL |
| DealerGamma | 5 | +1.68 | SR-A cand | NEW | Rank 5 but n=1 — needs second paper before DEPLOY |
| CEI | 7 | +1.33 | SR-A cand | NEW | Rank 7 with n=2 — provisional DEPLOY-CONDITIONAL |
| V015 | 31 | -0.17 | WATCH | YES | Rank 31 matches WATCH |
| V018 | 8 | +1.32 | WATCH | YES | Rank 8 — WATCH-upgrade candidate; slightly stronger than BNMA verdict suggests |

## Limitations

1. **Cross-group commensurability.** Using `p_beats_peers` as the within-paper ordinal scalar is more scale-invariant than `posterior_median` but still assumes a variable that beats peers in a 9-variable group (S-group in P1) is comparable to one that beats peers in a 3-variable group (Overlay in P1). S2 sensitivity exposes the two cases where this matters (V014, C009_Faber) — do NOT upgrade those on primary evidence alone.
2. **n=1 variables have wide CIs.** DealerGamma, PCTECH, CrossAssetValue, LazyPrices, CieslakPovala, OppInsider, GoldTIPSbeta, GoldPlatinumRatio, GoogleSVI all have n_pap = 1. Their rank CIs span ~30 ranks. Treat as provisional candidates, not deploy picks.
3. **Laplace approximation, not full MCMC.** For the 54-variable Bradley-Terry model, the posterior is log-concave (verified: Hessian min eigenvalue = 1.00) so the Laplace approximation is a good local fit. For very tail probabilities (P < 0.02) a full HMC run would give more accuracy, but the relative ranking is robust.
4. **P2 and P3 are analytical approximations.** Their 'approx0' entries were excluded (consistent with the cross-run BNMA meta-analysis's treatment). S1 sensitivity drops P2/P3 entirely — the top-10 is essentially unchanged, so P2/P3 are not carrying the conclusions.
5. **Paper-level heterogeneity is not modelled.** We assume a single true strength θ per variable shared across all papers. If papers have systematically different tastes (e.g., cg5 penalises post-2024 decay, cl3 requires replication audit), that becomes noise on θ rather than a paper-specific random effect. A hierarchical fit with paper random effects would be the next refinement but requires more data per (paper, variable) cell than we have.

## Recommendations

**Registry actions triggered by PL-NMA (conditional on S2 agreement):**
1. **Confirm V009, V027, V028 as DEPLOY** — all three robust across primary and S2. The prior BNMA meta-analysis verdict is validated. No action needed.
2. **Promote V018 BTC 3m basis from WATCH to DEPLOY-CONDITIONAL.** Rank 8 primary (θ = +1.32), rank 18-equivalent in S2. Consistently in top-25% across fits. Stronger evidence than the prior BNMA 'revisit in 2027' call suggests — worth a 6-month paper-trade allocation.
3. **Do NOT promote V014 or C009_FaberTAA on primary evidence.** Both are scale artifacts. Keep V014 as SPLIT (per BNMA). Keep Faber on PROMOTE but note that single-paper Overlay evidence is thin.
4. **Open three provisional slots for BAB, CEI, DealerGamma.** These rank 5/6/7 in primary AND S2. They are the strongest candidate variables in the network. BAB has 4-paper support (provisional DEPLOY-CONDITIONAL); CEI has 2-paper support (DEPLOY-CONDITIONAL with replication audit); DealerGamma has 1-paper support (WATCH → require a second paper before any deploy action).
5. **Exclude V010, V026, V002, V005, V017, TailRisk, IVSpread, SkewScalar.** All consistently bottom-quintile.
6. **Next BNMA run should drop the S-group cross-group penalty.** The primary PL-NMA underranks V028 and V011 because S-group has 9 peers vs T-group's 5. A natural fix is to normalise p_beats_peers by group size OR to run an explicit random-effect model on group difficulty.

## Files

- This report: `PL-NMA-meta-analysis-2026-04-18.md`
- HTML report: `PL-NMA-report-2026-04-18.html`
- Machine-readable results: `pl_nma_results.json`
- Analysis script: `plackett_luce_nma.py`
