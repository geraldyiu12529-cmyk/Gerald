# Bayesian Network Meta-Analysis — Variable Ranking (v4 spec)

**Run date:** 2026-04-18 · **Location:** Singapore · **Scope:** Stages A (completed from M1/M2/m3) · B (network construction) · C (hierarchical Bayesian fit) · D (ranking + diagnostics + marginal contribution) · F (candidate pipeline) · G (skipped — no ledger provided).

---

## TL;DR — What matters

**Fit quality.** Four parallel hierarchical Bayesian network meta-analyses converged cleanly. Max r_hat = 1.000 and min ESS_bulk = 1,329 across all four groups (PyMC 5.28, 3 chains × 2,000 draws × 1,500 tune, non-centered parameterization, target_accept = 0.95). Pool size: 32 variables (10 S, 12 T, 8 R, 2 Overlay); 18 of those carry at least one likelihood-study input, 14 are prior-only (they shrink toward prior mean and appear as RANK_UNSTABLE — this is exclusion-by-posterior working as designed).

**Per-group leaders (by p_top3).**

| group | 1st | 2nd | 3rd |
|---|---|---|---|
| S | V011 Brent carry (0.86) | V028 Basis-momentum (0.86) | V012 BTC addresses (0.21) |
| T | C015 Overnight L/S (0.71) | V014 BTC netflows (0.65) | C008 BTC-ETH pairs (0.41) |
| R | V027 Intermediary cap (0.89) | V004 HY OAS / EBP (0.87) | V001 VIX (0.77) |
| Overlay | C009 Faber TAA (1.00) | C011 VIX term structure (1.00) | — |

**Strongest peer-dominance signal.** V001 VIX (p_beats_peers = 0.807) — the cleanest single-variable choice when only one R-group overlay slot is available.

**Audit verdict for 2026-10-14 (V026, V027, V028).** **GO on all three.** Zero framework-change actions; three registry-maintenance actions: (i) update V026 post-decay target from 0.42 → 0.35; (ii) propagate V027 re-anchor onto AEM 2014 (not HKM 2017); (iii) correct V028 registry headline Sharpe from "1.2–1.5" to 0.9.

**Tier-3 graduation.** **C009 Faber TAA → Grade B Overlay** is the sole formal promote (passes all three criteria: `p_positive > 0.70`, `p_beats_peers > 0.60`, heterogeneity OK). **C015 Overnight-intraday L/S** recommended as conditional provisional Grade B at 2026-10-14 pending a 6-month paper-trade ≤ 1% of book and declaration of a peer linkage.

**Prior sensitivity.** Zero variables move ≥ 3 ranks between grade-tiered and uniformly-loose priors. Ranking is fully robust to prior choice.

**Registry-divergence flag.** V014 BTC netflows — registry 0.45 vs posterior 1.15 — driven by order-flow ML cluster. Recommend splitting V014 into order-flow construct (positive anchor) and vol-sort construct (separate Provisional entry).

---

## Stage A — Consolidated input summary

Compiled from three Stage A memos: **M1** (R + S literature validation), **M2** (T-group replications + Tier 3 admission), **m3** (Sharpe extraction pass).

### A.1 registry validation outcomes

- **17 of 17 Grade A/B primary citations PASS** for R + S groups (M1).
- **9 of 11 PASS** for remaining T / Overlay / C rows (M2). Two FAILs:
  - **V014** authorship error — Aloosh-Ouzan-Shahzad 2023 does not exist. **Corrected to Aloosh & Li 2024, Mgmt Sci 70(12):8875–8921.**
  - **V031** journal error — published in Journal of Portfolio Management, not Financial Analysts Journal. **Corrected.**

### A.2 replication density

- R + S groups (M1): 41 new post-2023 replications located; 23 with se_imputation (Lo 2002); 7 NUMERIC_MISSING (economic-validation studies without tradable Sharpes).
- T group (M2): 20 new replications; 19 NUMERIC_MISSING at M2 stage, reduced to 10 residual after m3 extraction pass.

### A.3 Tier 3 admission (10 of 15 cap)

| candidate | group | grade tier | stage D first-pass |
|---|---|---|---|
| C004 M2-vs-BTC cointegration | S | working paper | NEEDS_MORE_EVIDENCE |
| C006 Whale-alert ML momentum | T | working paper | LOW_POWER_CANDIDATE |
| C007 Perp funding arb | T | working paper | LOW_POWER_CANDIDATE (peer-dominated) |
| C008 BTC-ETH pairs | T | working paper | WATCH |
| C009 Faber TAA | Overlay | working paper | **PROMOTE** |
| C011 VIX futures term structure | Overlay | peer-reviewed | NEEDS_MORE_EVIDENCE |
| C012 Antonacci GEM dual momentum | T | working paper | LOW_POWER (dominated by V009) |
| C013 Crypto perp carry | T | working paper | WATCH (merge with C014) |
| C014 Crypto perp basis | T | working paper | WATCH (merge with C013) |
| C015 Overnight-intraday | T | working paper | WATCH (conditional promote) |

### A.3 Tier 3 rejections (9 of 19 embedded candidates)

Rejection reasons: CITATION_MISSING (7: MVRV Z-Score, NVT variants, Fear & Greed, RSI 2–5d, gold/silver ratio, market breadth, China PMI), EVENT_STUDY_NOT_SHARPE (2: EIA inventory, OPEC+), REDUNDANT_WITH_REGISTRY (1: tech P/S), AMBIGUOUS_SCORE_COMPONENT (1: HRP). Token unlocks hit two flags. Full table in `candidates_rejected.csv`.

### m3 registry-anchor corrections (applied before Stage B)

| var_id | correction | reason |
|---|---|---|
| V014 | Aloosh & Li 2024 Mgmt Sci (replaces fictitious Aloosh-Ouzan-Shahzad 2023) | authorship + mechanism |
| V015 | Liu-Tsyvinski-Wu 2022 JF dual-listed with Liu-Tsyvinski 2021 RFS | 2022 paper has cross-sectional Sharpe anchor |
| V017-R1 | Oefele (not "Soeder") 2025, Economics Letters | author name |
| V027 | Re-anchor on AEM 2014 SR ≈ 1.0 (HKM 2017 is non-traded by construction) | HKM has no tradable factor SR |
| V028 | Headline Sharpe 0.9 (not 1.2–1.5) | primary paper text says 0.9 |
| V028-P2 | Fan & Zhang 2024 JFM 44(7):1097 (not "Fan-Ma-Wen JFM") | author + journal |
| V028-P3 | Qian, Jiang, Liu 2024/2025 JFM (not "Jiang-Liu EFMA") | lead authorship |
| V027-P3 | Fontaine-Garcia-Gungor 2025 JoF 80(1):57 (not BoC WP) | publication venue |
| V031 | Journal of Portfolio Management (not FAJ) | journal name |

### Studies per variable (18 variables with likelihood input, 14 prior-only)

| group | var_id | n_studies | group | var_id | n_studies | group | var_id | n_studies |
|---|---|---|---|---|---|---|---|---|
| S | V011 | 3 | T | V009 | 4 | R | V001 | 3 |
| S | V028 | 2 | T | V026 | 3 | R | V004 | 1 |
| S | V003 | 0 | T | V014 | 2 | R | V027 | 1 |
| S | V006 | 0 | T | C015 | 2 | R | V002 | 0 |
| S | V007 | 0 | T | V010 | 1 | R | V005 | 0 |
| S | V008 | 0 | T | C006 | 1 | R | V015 | 0 |
| S | V012 | 0 | T | C007 | 1 | R | V016 | 0 |
| S | V013 | 0 | T | C008 | 1 | R | V018 | 0 |
| S | V019 | 0 | T | C012 | 1 | Overlay | C009 | 2 |
| S | C004 | 0 | T | C013 | 1 | Overlay | C011 | 0 |
| | | | T | C014 | 1 | | | |
| | | | T | V017 | 0 | | | |

### Readiness gate from m3

**GO** for V009, V026, V027 (re-anchored), V028 (re-anchored), Tier 3 (8 of 10 numeric). **HOLD** on V010 (single bin-selected study — prior-dominant treatment). **EXCLUDE-FROM-POOL** for V017 (structural low-power, all replications n ≤ 18m). **PARTIAL-GO** for V014 (cluster-level — order-flow cluster used, vol-sort cluster excluded). All dispositions honored in data layer.

---

## Stage B — Network construction

### Group S (Structural Directional, K = 10)

**Nodes.** V003 DXY, V006 UST 2s10s, V007 Real yield/breakevens, V008 ACM term premium, V011 Brent M1-M3 carry, V012 BTC active addresses, V013 BTC hash rate, V019 MVRV/SOPR, V028 basis-momentum, C004 M2-vs-BTC cointegration.

**Asset-class anchors.** Cross-Asset, Rates (×3), Commodities (×2), Crypto (×4). Intercept `alpha_a ~ N(0, 0.3)` absorbs mean-level differences.

**Edges.** 0 — no study tests two S variables head-to-head in a paired horse-race with both Sharpes tabulated. All inference is common-scale + asset-class-intercept.

**Peer adjacency (|correlation| ≥ 0.5).**

| node | declared peers | cluster |
|---|---|---|
| V006/V007/V008 | each other | rates |
| V011/V028 | each other | commodity carry pairing (dual-use convention) |
| V012/V013/V019 | each other | BTC on-chain fundamentals |
| V003, C004 | none | — |

**Likelihood input.** 5 study rows: V011-S1/S2/S3 (Fan 2024, Rad-Zaremba 2019, KMPV 2018); V028-S1/S2 (Boons-Prado 2019 corrected, Fan-Zhang 2024). Qian-Jiang-Liu SR *improvement* of 0.13 not entered — wrong scale.

**τ prior.** `HalfNormal(0.25)` (S/T scale). Posterior τ_med ranges 0.14–0.21 — no heterogeneity flag.

### Group T (Tactical Timing, K = 12)

**Nodes.** V009 TSMOM, V010 revision breadth, V014 BTC exchange netflows, V017 BTC ETF flows, V026 residual momentum, C006 whale-ML, C007 perp funding arb, C008 BTC-ETH pairs, C012 Antonacci GEM, C013 crypto perp carry, C014 crypto perp basis, C015 overnight-intraday L/S.

**Asset-class anchors.** Cross-Asset (×2), Equities (×3), Crypto (×7 — heavy).

**Edges.** 0.

**Peer adjacency.**

| cluster | members |
|---|---|
| Trend family | V009, V026, C012 |
| Crypto flow/positioning | V014, V017, C006, C007, C013, C014 |
| Equities revision (solo) | V010 |
| Narrow stat-arb (solo) | C008 |
| Equity intraday (solo) | C015 |

**Likelihood input.** 18 study rows. Three flags carried forward:
- V014 construct split: order-flow cluster only (Anastasopoulos L-only 1.88 + orthogonalized L/S 1.34). **Lee-Wang vol-sort negative cluster deliberately excluded per m3 "do not pool naively" guidance.**
- V009 CONSTRUCT_HETEROGENEOUS: Song-Jeon 0-bp-TC 1.41 vs Poh-Roberts-Zohren net 0.645 vs SG CTA index 0.61 — costs + ML vs classical.
- V010 SELECTION_BIAS: Sharpe-Gil 2024 is a 1-of-6 bin pick (other 5 bins SR < 1.0).

**τ prior.** `HalfNormal(0.25)`. Highest τ_med in pool: C015 (0.75 — gross-vs-net spread), V010 (0.63 — single-study artifact), V004 (0.66 — crosses into R). See Stage D §3.

### Group R (Risk Overlay, K = 8)

**Nodes.** V001 VIX, V002 MOVE, V004 HY OAS/EBP, V005 NFCI, V015 BTC realized vol, V016 BTC perp funding, V018 BTC 3m basis, V027 intermediary capital ratio.

**Asset-class anchors.** Cross-Asset (×4), Credit (×1), Crypto (×3).

**Edges.** 0.

**Peer adjacency + double-count gates.**

| cluster | members | note |
|---|---|---|
| Cross-asset vol/stress | V001, V002, V005 | V005 is hub node (peers all three) |
| Credit + dealer capacity | V004, V027 (double-count gate; "take more negative, not sum") | V004 dominates 0.624 > V027 0.366 head-to-head |
| BTC positioning/carry | V016, V018 (near-duplicate; p_beats 0.499/0.501) | treat as single positioning signal |
| V015 | none | — |

**Likelihood input.** 5 study rows: V001-S1/S2/S3 (Tsai 2025 L/S 1.70, PMC 2024 C-MVO 0.623, Dai-Wu vol-managed 0.45 — CONSTRUCT_HETEROGENEOUS); V004-S1 (Hu 2024 JFE RF bond ML 3.27 — ML_MULTI_FACTOR); V027-S1 (AEM 2014 LMP 1.00 — re-anchored).

**Effect-scale caveat.** V1 spec says R is "Sharpe *improvement* from vol-targeting" (scale ~0.0–0.4). Study inputs for V001/V004 are raw long-short Sharpes (~1.0+). Heterogeneity prior absorbs the scale mismatch; posteriors should be read as "signal quality" rather than literal sizing-improvement deltas.

**τ prior.** `HalfNormal(0.15)` (R/Overlay compressed scale). V004 τ_med 0.66 and V001 τ_med 0.37 flagged HETEROGENEOUS — both reflect real construct heterogeneity, not noise.

### Group Overlay (Regime Filter, K = 2)

**Nodes.** C009 Faber TAA, C011 VIX futures term structure. V029/V031/V032 registry Overlay entries are Provisional/Ungraded → Stage F, not main ranking.

**Asset-class anchors.** Both Cross-Asset.

**Edges.** 0. **Peer adjacency.** Neither has a peer; `p_beats_peers` falls back to `P(rank = 1)`.

**Likelihood input.** 2 study rows, both Faber 2013 (SMA improvement delta 0.23; GTAA improvement delta 0.29) — **correctly entered on the Overlay delta scale** ("conditional Sharpe gain when filter ON vs OFF"), not raw strategy Sharpe. C011 has no numeric extraction (regression t-stats only).

**τ prior.** `HalfNormal(0.15)`. C009 τ_med = 0.074 (consistent 2-study pool); C011 τ_med = 0.133 (prior-dominant).

---

## Stage C — Hierarchical Bayesian model

Per group, 4-level non-centered model:

```python
mu_k      ~ Normal(prior_mean_k, prior_sd_k)       # variable effect, grade-tiered prior
tau_k     ~ HalfNormal(tau_scale_g)                # between-study heterogeneity
theta_raw ~ Normal(0, 1)                           # non-centered parameterization
theta_ik  = mu[k_idx] + tau[k_idx] * theta_raw     # study-level true effect
y_ik      ~ Normal(theta_ik, sigma_ik)             # observed Sharpe, σ known
```

Fit with PyMC 5.28 NUTS, 3 chains × 2,000 draws × 1,500 tune, target_accept = 0.95, non-centered to avoid funnel pathology in low-study variables. Same model run twice: (a) grade-tiered priors per v4 spec table, (b) uniformly-loose `N(0, 0.5)` S/T and `N(0, 0.25)` R/Overlay for prior sensitivity.

**Convergence diagnostics.**

| group | max r̂ | min ESS_bulk |
|---|---|---|
| S | 1.000 | 1,761 |
| T | 1.000 | 2,786 |
| R | 1.000 | 3,590 |
| Overlay | 1.000 | 1,329 |

All well above the r̂ < 1.01 and ESS > 400 thresholds. No reparameterization needed beyond the non-centered default.

Full model in `model.py`; data layer (variable roster + studies + peer adjacency) in `data.py`.

---

## Stage D — Rankings, diagnostics, marginal contribution

### D.1 Marginal-contribution flags (LEAD)

**Demote / merge candidates (`p_beats_peers < 0.40`).**

| group | var_id | name | tier | grade | p_beats_peers | dominant peer |
|---|---|---|---|---|---|---|
| R | V005 | NFCI | 1 | A | 0.034 | V001, V002, V004 |
| T | C007 | Perp funding arb | 3 | Tier3 | 0.038 | C013, C014, V014 |
| T | V017 | BTC ETF net flows | 2 | B | 0.042 | V014 |
| T | C006 | Whale-alert ML | 3 | Tier3 | 0.052 | V014 |
| R | V002 | MOVE Index | 2 | A-minus | 0.095 | V001, V005 |
| T | V026 | Residual momentum (FF5) | 1 | A | 0.165 | V009 |
| T | C014 | Crypto perp basis | 3 | Tier3 | 0.176 | C013, C007, V014 |
| T | C013 | Crypto perp carry | 3 | Tier3 | 0.248 | C014, C007, V014 |
| S | V019 | MVRV / SOPR | 2 | B | 0.257 | V012, V013 |
| T | C012 | Antonacci GEM | 3 | Tier3 | 0.264 | V009 |
| S | V007 | Real yield / Breakevens | 1 | A | 0.295 | V006, V008 |
| S | V008 | ACM Term Premium 10Y | 1 | A | 0.335 | V006, V007 |
| S | V013 | BTC hash rate | 1 | A | 0.349 | V012, V019 |
| R | V027 | Intermediary capital | 1 | A | 0.365 | V004 |
| S | V006 | UST 2s10s | 1 | A | 0.369 | V007, V008 |
| S | V012 | BTC active addresses | 1 | A | 0.395 | V013, V019 |

**Promotion candidates (Tier 3, `p_beats_peers > 0.60` AND `p_positive > 0.70`).**

| group | var_id | name | p_positive | p_beats_peers |
|---|---|---|---|---|
| Overlay | C009 | Faber TAA | 0.991 | 0.679 |

**Read.** The demotion list is largely prior-only S and R variables whose posteriors cannot separate from peers (V005 NFCI, V002 MOVE, V007 Real yield, V008 ACM TP, V019 MVRV, C004). None should be removed from the registry — they are legitimately unclear under current evidence and will behave as prior-informed fallbacks. They should not dominate trade decisions on their own. V017 (p_beats vs V014 = 0.04) confirms the Stage-A "exclude from Sharpe pool" call. V027 p_beats_peers = 0.366 vs V004 is the declared double-count gate working as designed (EBP dominates head-to-head, keep V027 as more-negative-take overlay). Sole promotion candidate: **C009 Faber TAA**.

### D.2 Per-group ranking tables

#### D.2.1 Group S (K = 10) — sorted by p_top3

| var_id | name | tier | grade | n_std | post_mean | ci95 | p_pos | p_top3 | med_rank | rank_ci_w | p_beats_peers | τ_med | reg_SR | post-decay | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V011 | Brent M1-M3 carry | 1 | A | 3 | 0.793 | [0.45, 1.01] | 1.000 | 0.861 | 2 | 4 | 0.489 | 0.185 | 0.74 | 0.476 | — |
| V028 | Basis-momentum | 1 | A | 2 | 0.792 | [0.43, 1.07] | 1.000 | 0.858 | 2 | 4 | 0.511 | 0.144 | 0.90 | 0.475 | — |
| V012 | BTC active addresses | 1 | A | 0 | 0.256 | [−0.64, 1.13] | 0.710 | 0.209 | 6 | 9 | 0.395 | 0.204 | 0.40 | 0.154 | RANK_UNSTABLE |
| V003 | DXY (Dollar Index) | 1 | A | 0 | 0.296 | [−0.37, 0.96] | 0.804 | 0.191 | 6 | 9 | 0.045 | 0.207 | 0.50 | 0.178 | RANK_UNSTABLE |
| V013 | BTC hash rate | 1 | A | 0 | 0.207 | [−0.65, 1.09] | 0.679 | 0.186 | 6 | 9 | 0.349 | 0.203 | 0.35 | 0.124 | RANK_UNSTABLE |
| V008 | ACM Term Premium 10Y | 1 | A | 0 | 0.201 | [−0.59, 0.99] | 0.692 | 0.159 | 6 | 9 | 0.335 | 0.202 | 0.50 | 0.120 | RANK_UNSTABLE |
| V006 | UST 2s10s slope | 1 | A | 0 | 0.250 | [−0.43, 0.92] | 0.764 | 0.151 | 6 | 9 | 0.369 | 0.203 | 0.50 | 0.150 | RANK_UNSTABLE |
| V007 | Real yield / Breakevens | 1 | A | 0 | 0.141 | [−0.74, 1.02] | 0.624 | 0.150 | 7 | 9 | 0.295 | 0.200 | 0.50 | 0.071 | RANK_UNSTABLE |
| V019 | MVRV / SOPR | 2 | B | 0 | 0.098 | [−0.78, 0.97] | 0.590 | 0.130 | 7 | 9 | 0.257 | 0.209 | 0.30 | 0.059 | RANK_UNSTABLE |
| C004 | M2-vs-BTC cointegration | 3 | Tier3 | 0 | 0.002 | [−0.97, 0.97] | 0.502 | 0.106 | 8 | 9 | 0.035 | 0.202 | — | 0.001 | INDIST · RANK_UNSTABLE |

**Commentary.** Only V011 and V028 separate cleanly from the pack — both ≥ 2 clean replications with narrow SE, both p_positive = 1.0, p_top3 ≈ 0.86 is numerically identical because they are declared peers and their posteriors overlap heavily. Every variable below rank 2 has `rank_ci_width = 9` on K = 10 — the remaining eight are a flat posterior mass once the prior centers them near zero and no study-level likelihood pulls any one of them out.

#### D.2.2 Group T (K = 12)

| var_id | name | tier | grade | n_std | post_mean | ci95 | p_pos | p_top3 | med_rank | rank_ci_w | p_beats_peers | τ_med | reg_SR | post-decay | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C015 | Overnight-intraday L/S | 3 | Tier3 | 2 | 1.259 | [0.37, 2.16] | 0.997 | 0.708 | 2 | 8 | 0.394 | 0.748 | — | 0.881 | HETEROG · TIER3_TOP3 |
| V014 | BTC exchange netflows | 1 | A | 2 | 1.148 | [0.39, 1.61] | 0.997 | 0.646 | 3 | 9 | 0.532 | 0.367 | 0.45 | 0.689 | RANK_UNSTABLE · DIVERGENCE · HETEROG |
| C008 | BTC-ETH stat pairs | 3 | Tier3 | 1 | 0.917 | [−0.05, 1.75] | 0.966 | 0.412 | 4 | 10 | 0.121 | 0.419 | — | 0.550 | RANK_UNSTABLE · HETEROG |
| V010 | Revision breadth | 1 | A | 1 | 0.839 | [0.04, 1.68] | 0.980 | 0.336 | 5 | 10 | 0.098 | 0.626 | 0.50 | 0.419 | RANK_UNSTABLE · HETEROG |
| C013 | Crypto perp carry | 3 | Tier3 | 1 | 0.823 | [−0.14, 1.77] | 0.952 | 0.348 | 5 | 11 | 0.248 | 0.454 | — | 0.494 | RANK_UNSTABLE · HETEROG |
| V009 | TSMOM | 1 | A | 4 | 0.771 | [0.43, 1.04] | 1.000 | 0.107 | 6 | 7 | **0.657** | 0.356 | 0.90 | 0.463 | HETEROG |
| C014 | Crypto perp basis | 3 | Tier3 | 1 | 0.730 | [−0.18, 1.59] | 0.942 | 0.261 | 6 | 11 | 0.176 | 0.315 | — | 0.438 | RANK_UNSTABLE · HETEROG |
| V026 | Residual momentum (FF5) | 1 | A | 3 | 0.584 | [0.30, 0.81] | 1.000 | 0.008 | 8 | 7 | 0.165 | 0.190 | 0.70 | 0.350 | — |
| C012 | Antonacci GEM | 3 | Tier3 | 1 | 0.580 | [−0.11, 1.04] | 0.957 | 0.059 | 8 | 9 | 0.264 | 0.214 | — | 0.348 | RANK_UNSTABLE · LOW_POWER |
| C007 | Perp funding arb | 3 | Tier3 | 1 | 0.294 | [−0.62, 1.21] | 0.732 | 0.062 | 10 | 10 | 0.038 | 0.209 | — | 0.177 | RANK_UNSTABLE · LOW_POWER |
| V017 | BTC ETF net flows | 2 | B | 0 | 0.140 | [−0.65, 0.94] | 0.640 | 0.020 | 11 | 8 | 0.042 | 0.203 | 0.30 | 0.084 | — |
| C006 | Whale-alert ML | 3 | Tier3 | 1 | 0.131 | [−0.79, 1.09] | 0.613 | 0.032 | 11 | 9 | 0.052 | 0.198 | — | 0.079 | RANK_UNSTABLE · LOW_POWER |

**Commentary.** T-group is crowded in the 0.5–1.3 posterior range, driven by high-Sharpe crypto studies and the overnight-equity anomaly. **C015 leads on p_top3** despite only two studies because SR 3.0 gross / ~2.3 net on a 360-month sample dominates the skeptical Tier-3 prior. **V014 is the highest-ranking registry Grade-A variable** and shows a registry-divergence flag (posterior 1.15 vs registry 0.45) — driven by the Anastasopoulos order-flow cluster, with Lee-Wang negative-sign vol-sort cluster deliberately excluded per m3 guidance. **V009 TSMOM has the strongest peer-dominance signal in T** at 0.657 — it reliably beats V026 and C012 within the trend family. V026 p_top3 = 0.008 is not a weakness: posterior median 0.58, CI excludes zero; in a K = 12 group packed with high-Sharpe crypto studies it cannot reach top 3 under any prior. Honest mid-rank Grade A; exactly what exclusion-by-posterior is supposed to do.

#### D.2.3 Group R (K = 8)

| var_id | name | tier | grade | n_std | post_mean | ci95 | p_pos | p_top3 | med_rank | rank_ci_w | p_beats_peers | τ_med | reg_SR | post-decay | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V004 | HY OAS / EBP | 1 | A | 1 | 0.933 | [0.26, 1.63] | 0.996 | 0.871 | 1 | 5 | 0.624 | 0.656 | 0.50 | 0.560 | HETEROG |
| V027 | Intermediary capital ratio | 1 | A | 1 | 0.809 | [0.43, 1.15] | 1.000 | 0.895 | 2 | 3 | 0.365 | 0.135 | 1.00 | 0.485 | — |
| V001 | VIX | 1 | A | 3 | 0.720 | [0.26, 1.12] | 0.998 | 0.774 | 3 | 5 | **0.807** | 0.367 | 0.50 | 0.432 | HETEROG |
| V005 | NFCI | 1 | A | 0 | 0.211 | [−0.45, 0.91] | 0.719 | 0.119 | 6 | 6 | 0.034 | 0.141 | 0.35 | 0.127 | RANK_UNSTABLE · GRADE_A_BOTTOM3 |
| V002 | MOVE Index | 2 | A-minus | 0 | 0.203 | [−0.46, 0.87] | 0.717 | 0.120 | 6 | 6 | 0.095 | 0.138 | 0.40 | 0.122 | RANK_UNSTABLE |
| V015 | BTC realized vol | 2 | A-minus | 0 | 0.155 | [−0.51, 0.83] | 0.682 | 0.092 | 6 | 6 | 0.013 | 0.133 | 0.40 | 0.093 | RANK_UNSTABLE |
| V018 | BTC 3m basis | 2 | B | 0 | 0.151 | [−0.43, 0.73] | 0.695 | 0.068 | 6 | 5 | 0.501 | 0.133 | 0.25 | 0.090 | — |
| V016 | BTC perp funding rate | 2 | B | 0 | 0.144 | [−0.45, 0.72] | 0.681 | 0.061 | 6 | 5 | 0.499 | 0.139 | 0.30 | 0.086 | — |

**Commentary.** Cleanest picture of any group — V004, V027, V001 dominate on posterior Sharpe, p_positive, and rank stability. **V001 VIX has the highest p_beats_peers in the entire BNMA** at 0.807. **V004 EBP has the widest heterogeneity** (τ = 0.656) driven by Hu 2024 multi-factor ML (SR 3.27) — posterior p_top3 of 0.87 remains reliable. **V005 NFCI is the only Grade A variable in group bottom 3** — GRADE_A_BOTTOM3 quarterly-review flag. No tradable Sharpe has been extracted post-Brave-Butters 2012; consider reclassifying as non-tradable diagnostic.

#### D.2.4 Group Overlay (K = 2)

| var_id | name | tier | grade | n_std | post_mean | ci95 | p_pos | p_top3 | med_rank | rank_ci_w | p_beats_peers | τ_med | post-decay | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C009 | Faber TAA | 3 | Tier3 | 2 | 0.248 | [0.07, 0.44] | 0.991 | 1.000 | 1 | 1 | 0.679 | 0.074 | 0.174 | TIER3_TOP3 |
| C011 | VIX futures term structure | 3 | Tier3 | 0 | 0.098 | [−0.49, 0.69] | 0.622 | 1.000 | 2 | 1 | 0.321 | 0.133 | 0.059 | TIER3_TOP3 |

**Commentary.** Both in top 3 by construction (K = 2). The gap matters: **C009 CI [0.07, 0.44] is tight and entirely above zero; p_positive = 0.991**, while C011 CI [−0.49, 0.69] straddles zero with p_positive = 0.62. C009 earns promotion candidacy on its own merits; C011 is a hold-for-more-evidence.

### D.3 Heterogeneity flags (τ_k above threshold)

Threshold: τ_med > 0.25 (S/T) or > 0.15 (R/Overlay).

| group | var_id | name | τ_med | interpretation |
|---|---|---|---|---|
| T | C015 | Overnight L/S | 0.748 | Gross-vs-net spread (3.0 vs 2.35) |
| R | V004 | HY OAS / EBP | 0.656 | Hu 2024 ML composite (3.27) vs single-EBP construct |
| T | V010 | Revision breadth | 0.626 | Single selection-biased study — prior-dominant, not identified |
| T | C013 | Crypto perp carry | 0.454 | Single aggressive-venue extraction (6.45) vs skeptical prior |
| T | C008 | BTC-ETH pairs | 0.419 | Single narrow-universe 5-min study |
| R | V001 | VIX | 0.367 | L/S futures (1.70) vs vol-managed (0.45) — CONSTRUCT_HETEROGENEOUS |
| T | V014 | BTC netflows | 0.367 | Two order-flow studies vs skeptical prior |
| T | V009 | TSMOM | 0.356 | 0-bp-TC ML (1.41) vs net CTA (0.61–0.65) — construct + cost |
| T | C014 | Crypto perp basis | 0.315 | Single tier-dependent extraction |

**Reading.** Most elevated τ in T-group is single-study artifacts (τ absorbs distance between observation and prior when there is no actual between-study variation to estimate). Only two carry real meaning: **V004 EBP** (ML composite vs single-variable) and **V001 VIX** (L/S futures vs vol-managed overlay). Both are flagged CONSTRUCT_HETEROGENEOUS and the posterior has propagated that uncertainty correctly.

### D.4 Registry-divergence flags (|registry − posterior_median| > 2·se)

Only one variable exceeds the divergence threshold:

| group | var_id | registry | posterior_median | CI95 | divergence |
|---|---|---|---|---|---|
| T | V014 | 0.45 | 1.148 | [0.39, 1.61] | LOW vs posterior |

**Interpretation.** Anastasopoulos et al. (2026) order-flow study reports cleaned Sharpe 1.34–1.88 on 54-month OOS with TC included, pulling the posterior strongly above the 0.45 registry anchor. Lee-Wang (2024) vol-sort cluster pointed the other way (SR ≈ −4.0) but was deliberately excluded from likelihood per m3 guidance. **Registry-update candidate conditional on construct clarification.** Recommend splitting V014 into (a) order-flow construct (positive anchor 0.6–0.8) and (b) vol-sort construct (separate Provisional entry).

Also noted but below threshold: V028 (posterior 0.79 vs corrected registry 0.9 — within CI), V027 (posterior 0.81 vs re-anchored 1.0 — within CI). Both corrections applied pre-Stage-B.

### D.5 Grade-rank consistency flags (quarterly review surface)

| group | var_id | name | grade | med_rank | group_K | flag |
|---|---|---|---|---|---|---|
| R | V005 | NFCI | A | 6 | 8 | GRADE_A_BOTTOM3 |
| T | C015 | Overnight-intraday L/S | Tier3 | 2 | 12 | TIER3_TOP3 |
| Overlay | C009 | Faber TAA | Tier3 | 1 | 2 | TIER3_TOP3 |
| Overlay | C011 | VIX term structure | Tier3 | 2 | 2 | TIER3_TOP3 |

**Reading.** Only one genuinely awkward case: **V005 NFCI as Grade A with rank 6 of 8**. Primary citation (Brave-Butters 2012) is solid but no clean tradable Sharpe has been extracted for a pure NFCI overlay; the posterior has nothing to work with beyond the prior. At next quarterly, consider reclassifying as a non-tradable regime diagnostic. The three Tier3-top3 flags are expected small-group prominence and are addressed as promotion candidates in §D.9.

### D.6 Cross-group summary

**IMPORTANT.** Groups operate on different effect scales by design: S/T report long-short Sharpe; R reports Sharpe *improvement* from vol-targeting/regime conditioning; Overlay reports conditional Sharpe gain when filter ON vs OFF. Posteriors are **not directly comparable across groups.**

**Overall top 5 by p_top3** (for context only, see caveat):

| rank | var_id | group | name | p_top3 | note |
|---|---|---|---|---|---|
| 1 | C009 | Overlay | Faber TAA | 1.000 | K = 2 ceiling artifact; real promotion candidate |
| 2 | C011 | Overlay | VIX term structure | 1.000 | K = 2 ceiling artifact; no real endorsement |
| 3 | V027 | R | Intermediary capital | 0.895 | Real; audit target |
| 4 | V004 | R | HY OAS / EBP | 0.871 | Real; highest R-group posterior |
| 5 | V011 | S | Brent M1-M3 carry | 0.861 | Real; 3 replications |

### D.7 Prior sensitivity

Re-fit all four groups with uniformly-loose prior: N(0, 0.5) for S/T, N(0, 0.25) for R/Overlay, applied to every tier. Rank-move threshold: |median_rank_main − median_rank_loose| ≥ 3 → prior-dependent.

**Result: zero prior-dependent variables.** Maximum rank move across all 32 variables = 2 positions. Grade-tiered prior is not doing the work; likelihood (where present) dominates, and prior-only variables behave symmetrically under both priors. Ranking is fully robust.

### D.8 Feed to 2026-10-14 audit

#### V026 — Residual momentum (FF5), group T

- Posterior median **0.584**, CI95 [0.302, 0.806], p_positive = 0.9997
- p_top3 = 0.008 (low, but group T is packed with high-Sharpe crypto studies — absolute posterior is healthy)
- p_beats_peers vs V009 = 0.165 (TSMOM dominates head-to-head)
- Registry 0.70 → posterior 0.58; post-decay (40%) = 0.35 (registry carried 0.42)
- No divergence flag, 3 study inputs
- m3 note: decay has NOT occurred in stock-specific variant (Gerard-Jehl Period II SR 0.77 > Period I SR 0.44)

**Verdict: GO.** Action: lower registry post-decay prior from 0.42 → 0.35; keep Grade A; flag disagreement-gate rule (V026-replaces-V009-for-single-stocks) for discussion — TSMOM's 0.66 peer-dominance suggests the gate may be triggering too aggressively.

#### V027 — Intermediary capital ratio, group R

- Posterior median **0.809**, CI95 [0.429, 1.148], p_positive = 1.000
- p_top3 = 0.895 (second-strongest in R)
- p_beats_peers vs V004 = 0.366 (EBP dominates — double-count gate working as designed)
- **Re-anchored** on AEM 2014 LMP SR ≈ 1.0 (not HKM 2017 which is non-traded)
- Registry (re-anchored) 1.0 → posterior 0.81; post-decay = 0.49 (registry carried 0.36 under old 0.6 HKM anchor)
- No divergence flag, 1 study input

**Verdict: GO with registry update.** Propagate AEM 2014 anchor into v4 registry; keep HKM 2017 as structural/non-traded supporting citation; revise projected operational Sharpe from 0.36 → ~0.50; keep double-count gate vs V004.

#### V028 — Basis-momentum (commodity), group S

- Posterior median **0.792**, CI95 [0.435, 1.067], p_positive = 1.000
- p_top3 = 0.858 (tied with V011 at top of S)
- p_beats_peers vs V011 = 0.511 (coin-flip — declared peers with near-identical posteriors)
- Registry (corrected to Boons-Prado headline) 0.90 → posterior 0.79; post-decay (40%) = 0.48 (matches registry's projected 0.48)
- No divergence flag, 2 study inputs

**Verdict: GO with registry number correction.** Fix registry headline from "1.2–1.5" → 0.9 (Boons-Prado primary paper says 0.9); keep "always use WITH V011 static slope" convention confirmed by posterior overlap.

**Overall audit verdict: GO on all three.** Zero framework-change actions. Three registry-maintenance actions.

### D.9 Tier 3 graduation recommendations

Admission criteria: `p_positive > 0.70`, `p_beats_peers > 0.60`, passes heterogeneity.

**Formal PROMOTE (meets all three).**

| var_id | group | name | p_pos | p_beats_peers | τ_med | post-decay | notes |
|---|---|---|---|---|---|---|---|
| C009 | Overlay | Faber TAA | 0.991 | 0.679 | 0.074 | 0.174 | 112-year sample + GTAA extension; recommend Grade B Overlay admission |

**WATCH / conditional.**

| var_id | group | name | p_pos | p_beats_peers | verdict |
|---|---|---|---|---|---|
| C015 | T | Overnight-intraday L/S | 0.997 | 0.394 (fallback p_rank1) | Provisional Grade B conditional on 6-month paper-trade ≤ 1% of book + declared peer |
| C008 | T | BTC-ETH pairs | 0.966 | 0.121 (fallback) | Conditional on 5-min execution; narrow-universe |
| C013 | T | Crypto perp carry | 0.952 | 0.248 | MERGE with V014 flow-suite |
| C012 | T | Antonacci GEM | 0.957 | 0.264 | Dominated by V009; keep as practitioner composite, not independent entry |

**HOLD.**

| var_id | group | reason |
|---|---|---|
| C004 | S | NUMERIC_MISSING; posterior ≈ prior |
| C006 | T | n = 10 months; LOW_POWER |
| C007 | T | Dominated by perp cluster; p_beats 0.038 |
| C011 | Overlay | p_pos 0.62; indistinguishable from zero |
| C014 | T | Overlaps C013; merge not admit |

### D.10 Memory-ready insights (framework update bullets)

1. **V027 must be re-anchored on Adrian-Etula-Muir (2014) JF, not He-Kelly-Manela (2017) JFE.** HKM's factor is non-traded by construction; its risk price (≈ 9%/quarter) does not correspond to a tradable Sharpe. AEM LMP SR ≈ 1.0 gross, 0.60 post-decay vs the registered 0.36.

2. **V028 basis-momentum headline is 0.9, not "1.2–1.5" (older copies) or 0.8 (v4 prompt body).** Boons-Prado 2019 JF text explicitly states 0.9. Posterior 0.79 with 3 replications fully consistent. Must always pair with V011 (p_beats 0.51 is a coin-flip — complementary construct working as designed, not a demotion).

3. **V014 primary citation is Aloosh & Li (2024) Mgmt Sci, not Aloosh-Ouzan-Shahzad (2023) which does not exist.** Mechanism correct (exchange flow / wash-trade forensics). Additionally, V031 absorption ratio journal is Journal of Portfolio Management (not FAJ). Both corrections baked into the posterior.

4. **V019 MVRV/SOPR should be downgraded Grade B → Grade C.** Zero peer-reviewed replications; posterior p_pos = 0.59. Keep on watch; do not use as sole entry trigger. **V017 BTC ETF flows** should stay excluded from Sharpe pooling until 2027+ (structural low-power; all replications n ≤ 18m).

5. **C009 Faber TAA graduates to Grade B Overlay.** Sole formal promote. **C015 Overnight-intraday** is the T-group sleeper (highest posterior at 1.26) but falls short on peer-fallback — provisional admission at 2026-10-14 conditional on paper-trade. Other Tier-3 admits (C006, C007, C012) fail on low power and stay in candidate pipeline.

**Supplementary observations:** Prior sensitivity is nil (no variables move ≥ 3 ranks). Rank instability is pervasive in prior-only variables (19 of 32 have rank_ci_width ≥ 0.7×K) — this is exclusion-by-posterior working, not a method weakness. V005 NFCI GRADE_A_BOTTOM3 flag suggests reclassifying as non-tradable diagnostic.

---

## Stage F — Candidate pipeline

### F.1 Provisional / Ungraded registry rows

| var_id | name | score_component | grade | verdict | rationale |
|---|---|---|---|---|---|
| V020 | News sentiment (Tetlock/Garcia) | C | B | OUT_OF_BNMA_SCOPE | C-group catalyst; event-study scale |
| V029 | GEX / Gamma Exposure | Overlay | Provisional | WATCH | No tradable SR extracted; needs dealer-gamma tape access |
| V030 | Cross-asset lead-lag | T | Provisional | WATCH | Overlaps TSMOM for led asset; needs per-pair tradable Sharpes |
| V031 | Absorption ratio (Kritzman 2011 JPM) | Overlay | Provisional | WATCH | Journal correction applied; no tradable SR |
| V032 | Decision tree feature importance | Overlay | Ungraded | NEEDS_MORE_EVIDENCE | Meta-variable, not standalone |
| V033 | Pre-FOMC drift / calendar | C | Ungraded | OUT_OF_BNMA_SCOPE | C-group catalyst |

### F.2 Admitted Tier 3 failing peer-dominance

| var_id | name | score | p_pos | p_beats | verdict |
|---|---|---|---|---|---|
| C004 | M2-vs-BTC cointegration | S | 0.502 | 0.035 | NEEDS_MORE_EVIDENCE |
| C006 | Whale-alert ML | T | 0.613 | 0.052 | NEEDS_MORE_EVIDENCE |
| C007 | Perp funding arb | T | 0.732 | 0.038 | WATCH (peer-dominated) |
| C008 | BTC-ETH pairs | T | 0.966 | 0.121 (fallback) | WATCH (conditional promote) |
| C011 | VIX term structure | Overlay | 0.622 | 0.321 | NEEDS_MORE_EVIDENCE |
| C012 | Antonacci GEM | T | 0.957 | 0.264 | WATCH (dominated by V009) |
| C013 | Crypto perp carry | T | 0.952 | 0.248 | WATCH (merge with C014 / V014 suite) |
| C014 | Crypto perp basis | T | 0.942 | 0.176 | WATCH (merge with C013) |
| C015 | Overnight-intraday | T | 0.997 | 0.394 (fallback) | PROMOTE_AT_NEXT_QUARTERLY (conditional) |

### F.3 Stage A.3 rejected — watch list

| candidate | rejection reason | watch note |
|---|---|---|
| MVRV Z-Score | CITATION_MISSING (practitioner) | Overlaps V019; low priority |
| NVT Signal 90d | CITATION_MISSING (attribution unverifiable) | Appears fabricated; do not admit without independent citation |
| Token unlocks | EVENT_STUDY_NOT_SHARPE + CITATION_MISSING | C-group tracking |
| Fear & Greed < 10 | CITATION_MISSING + NUMERIC_MISSING | n < 10 since 2018; underpowered |
| RSI 2–5d on S&P | CITATION_MISSING | Connors literature; no academic SR |
| Price-to-sales (tech) | REDUNDANT | FF3/FF5 value via V026 residualization |
| Gold/silver ratio | CITATION_MISSING | Practitioner only |
| China PMI → copper | CITATION_MISSING | Becerra 2022 MAPE only, no tradable SR |
| EIA crude inventory | EVENT_STUDY_NOT_SHARPE | C-group |
| OPEC+ production | EVENT_STUDY_NOT_SHARPE | C-group |
| Market breadth > 200-DMA | CITATION_MISSING | Practitioner only |
| HRP (Burggraf 2021 FRL) | AMBIGUOUS_SCORE_COMPONENT | Portfolio-construction, not signal |

### F.4 2026-10-14 quarterly pipeline actions

**Promote:**
- C009 Faber TAA → Grade B Overlay (formal)

**Conditional promote:**
- C015 Overnight-intraday L/S → provisional Grade B T (paper-trade + peer declaration)

**Downgrade:**
- V019 MVRV/SOPR → B → C (M1 recommendation confirmed)
- V005 NFCI → reclassify as non-tradable diagnostic (GRADE_A_BOTTOM3 flag)

**Merge:**
- C014 ⊂ C013 (keep one crypto perp basis/carry entry)
- C006, C007 → fold into V014 flow-suite operational notes

**Watch through 2027-04:** V029, V030, V031, V032, C004, C008, C011, C013.

**Registry-maintenance (non-audit):**
- V014: split order-flow vs vol-sort; fix citation to Aloosh & Li 2024
- V015: add Liu-Tsyvinski-Wu 2022 JF as dual-listed anchor
- V017-R1: Oefele (not "Soeder") 2025 author correction
- V027: update source citation to AEM 2014 as tradable anchor
- V028: correct headline Sharpe to 0.9 (not 1.2–1.5)
- V028-P2: Fan & Zhang 2024 JFM (not Fan-Ma-Wen)
- V028-P3: Qian, Jiang, Liu 2024/2025 JFM (not Jiang-Liu EFMA)
- V027-P3: Fontaine-Garcia-Gungor 2025 JoF (not BoC WP)
- V031: correct journal to JPM (not FAJ)

---

## Closing checklist

**Per-group top 3 (by p_top3):**

- **S:** V011 (0.86 / peer 0.49), V028 (0.86 / peer 0.51), V012 (0.21 / peer 0.40)
- **T:** C015 (0.71 / peer 0.39), V014 (0.65 / peer 0.53), C008 (0.41 / peer 0.12)
- **R:** V027 (0.89 / peer 0.37), V004 (0.87 / peer 0.62), V001 (0.77 / peer 0.81)
- **Overlay:** C009 (1.00 / peer 0.68), C011 (1.00 / peer 0.32)

**Exclusion flags raised:**

- INDISTINGUISHABLE_FROM_ZERO (1): S/C004
- RANK_UNSTABLE (19): S/V003, S/V006, S/V007, S/V008, S/V012, S/V013, S/V019, S/C004; T/V010, T/V014, T/C006, T/C007, T/C008, T/C012, T/C013, T/C014; R/V002, R/V005, R/V015
- LOW_POWER_CANDIDATE (3): T/C006, T/C007, T/C012
- DIVERGENCE (1): T/V014
- HETEROGENEOUS (9): T/C015, T/V010, T/V014, T/C008, T/C013, T/C014, T/V009, R/V004, R/V001
- GRADE_RANK_CONSISTENCY (1 material): R/V005 GRADE_A_BOTTOM3

**Prior-dependent variables (|rank move| ≥ 3):** none. Ranking fully robust.

**Tier 3 graduation:** C009 Faber TAA (formal, Grade B Overlay). Conditional: C015 Overnight-intraday L/S.

**GO/NO-GO at 2026-10-14 audit:** V026 **GO**, V027 **GO** (re-anchor), V028 **GO** (headline correction). Three registry-maintenance actions; zero framework-change actions.

---

## Artifacts

All in `/mnt/user-data/outputs/bnma/`:

| file | description |
|---|---|
| `report.md` | Stand-alone Stage D report (this document is its superset) |
| `stage_a_summary.md` | Stage A consolidated summary |
| `stage_a.csv` | 32-variable × 14-column consolidated roster |
| `candidates_rejected.csv` | 12-row rejection ledger |
| `network_S.md`, `network_T.md`, `network_R.md`, `network_Overlay.md` | Per-group Stage B network construction |
| `candidate_pipeline.md` | Stage F — full watch list + pipeline actions |
| `ranking_S.csv`, `ranking_T.csv`, `ranking_R.csv`, `ranking_Overlay.csv` | Per-group posterior tables |
| `ranking_all.csv`, `ranking_all_enriched.csv`, `ranking_all_loose.csv` | Cross-group + prior-sensitivity |
| `prior_sensitivity.csv` | Rank-move comparison |
| `traces/trace_{S,T,R,Overlay}.nc` and `_loose.nc` | arviz InferenceData |
| `data.py`, `model.py` | Reproducibility layer |
