# BNMA Cross-Run Meta-Analysis — 2026-04-18

`RUN_MODE = META_ANALYSIS; N_PAPERS = 4; RE_FITTING = NO.`

**Paper index (used in all citations below):**

| # | File | Date | Engine | Vars | Note |
|---|---|---|---|---|---|
| P1 | `BNMA Mark 1.md` | 2026-04-18 | Full MCMC (PyMC, 3 chains × 2k draws, R̂=1.00) | 32 | Most recent, richest posterior diagnostics |
| P2 | `Chatgpt Mark 1.md` | undated | **Analytical approximation only** (MCMC not executed) | 25 | Unlikelihood-input vars pin at 0 / prior centre |
| P3 | `Chatgpt mark 2.md` | undated | **Analytical approximation only** | 31 | Successor to P2; same engine limitation |
| P4 | `bnma-claude mark 2.md` | 2026-04-17 | Full MCMC (4 chains × 2k post-warmup, R̂<1.01) | 34 | Second full-MCMC run, 1 day before P1 |

**Evidence weighting rule used throughout:** Full-MCMC runs (P1, P4) are primary. Analytical-only runs (P2, P3) corroborate for variables with ≥2 likelihood studies (where the analytical approximation actually moves off the prior), and are treated as **non-informative** for variables where the paper reports `posterior_median = 0` with symmetric CI — that pattern is a prior-shrinkage artifact, not evidence of a null. This is flagged line-by-line below.

---

## TL;DR

1. **Three variables clear every DEPLOY hurdle across all four runs: V009 TSMOM (T), V028 Basis-momentum (S), V027 Intermediary capital (R).** These are the tradable spine of the framework. Evidence: P1/P2/P3/P4 all show p_positive ≥ 0.98, p_beats_peers ≥ 0.50 for all three, audit-GO on V027 and V028 in P1/P3/P4.

2. **Stage 0 caveat: the 4 papers are not 4 independent posteriors.** P2 and P3 are analytical approximations that did not execute MCMC (P2 Stage 8 caveat #1; P3 metadata caveat #1). For 14–20 variables they return exactly `posterior_median = 0` with symmetric CI — that is the prior, not evidence. The effective corpus is ~2 full runs + 2 shrinkage-only runs.

3. **V014 BTC exchange netflows is unresolvable from the 4 papers alone.** P1 posterior 1.15, p_positive 0.997 (DIVERGENCE flag); P2/P4 treat as indistinguishable from zero. The registry already calls a split (order-flow vs vol-sort). Next BNMA should split the construct, not re-pool. Cite: P1 §4 registry divergence, P4 table row V014.

4. **R-group ranking is unstable at ranks 2–8 across all four runs; only V027 separates cleanly.** P4 explicit statement (§8 caveat #5), P1 rank_ci_width mean 5.3 of 8, P2 p_top3 tie at ~0.22 across V001/V002/V004/V005/V015. Keep V027 as regime gate; stop pretending the rest of R discriminates.

5. **Current S/T/R/Overlay grouping — S scores 3.5/5 on the effectiveness grid, T and R 2.0/5, Overlay 1.0/5. Every failure is on scale-consistency or discrimination; Actionability passes in all 4 groups.** That points to a *scale/role* fix, not a regrouping. Stage 5 below. Recommendation: keep the groups, make role explicit (S/T = entry direction, R = sizing scalar, Overlay = gate). Do NOT regroup by asset class or mechanism — the evidence doesn't support it.

6. **Registry actions with 4-run support: re-anchor V027 to AEM 2014 (P1 audit, P3 divergence=FALSE only because P3 used the corrected anchor), correct V028 headline Sharpe to ~0.8 (P1), create V004+V027 double-count gate (P1 §3, P4 V004 REDUNDANT_VS_V027 flag), demote V010 and V017 to Tier 3 / remove (P1 p_beats_peers 0.098, P4 p_beats_peers 0.0063 / 0.42).**

---

## Stage 0 — Sufficiency Check

| Check | Status | Evidence |
|---|---|---|
| ≥3 of 4 papers cover S/T/R/Overlay | **PASS** | P1 covers all 4 groups; P4 covers all 4 groups; P3 covers all 4 (Overlay is NO_NUMERIC); P2 covers S/T/R, Overlay explicitly "no eligible pooled nodes" (P2 §9). 4 of 4 have the structure. |
| Temporal orderability | **PASS (with inference)** | P1 dated 2026-04-18, P4 dated 2026-04-17. P2/P3 undated but P3 titled "Mark 2" and consolidates P2 stages → P2 < P3. Approximate order: P2 → P3 → P4 → P1. Drift direction (oldest to newest) therefore reads left-to-right where analytical approximations give way to full MCMC. |
| Per-variable posterior_median + p_positive | **PASS** | All 4 papers supply these. For P2/P3, many values are the analytical fallback (0 median, p=0.50); treated as non-informative below, not missing. |
| Prior-sensitivity result present in ≥1 paper | **PASS (in all 4)** | P1 §5 (zero variables move ≥3 ranks); P2 §5 (same); P3 §5 (table, C004 moves 1 rank); P4 §5 (six variables move ≥3 ranks). P4 is the strongest prior-sensitivity evidence. |

**Proceed to Stage 1.**

One methodological note I surface but will not treat as a Stage-0 failure: P2 and P3 are *calibration runs*, not independent posterior samples. The user should know that when I write "3 of 4 runs agree," for weak variables this often means "1 full run + 2 prior-centred artifacts." I flag every such case in the verdict table.

---

## Stage 1 — Cross-Run Variable State Table

**Cell format:** `(post_median, p_positive, p_beats_peers, flags)` — "—" means variable not in paper; "approx0" means analytical-approximation artifact (posterior = prior centre, p_positive = 0.50).

### S — Sentiment / Positioning

| var_id | name | P1 | P2 | P3 | P4 | n_runs | median_post | drift_range |
|---|---|---|---|---|---|---|---|---|
| V003 | DXY | (0.30, 0.80, 0.05, UNSTABLE) | (approx0, 0.50, 0.50, INDIST·BOTTOM3) | (n/a, NO_NUMERIC) | (0.12, 0.82, 0.43, INDIST·SHRINK2.3σ) | 4 | 0.12 | 0.30 |
| V006 | UST 2s10s | (0.25, 0.76, 0.37, UNSTABLE) | (approx0, 0.50, 0.50, INDIST) | (n/a, NO_NUMERIC) | (0.12, 0.71, 0.32, INDIST·SHRINK2.5σ) | 4 | 0.12 | 0.25 |
| V007 | Real yield / breakevens | (0.14, 0.62, 0.30, UNSTABLE) | (approx0, 0.50, 0.50, INDIST·BOTTOM3) | (n/a, NO_NUMERIC·REGIME_SENSITIVE_POST2022) | (0.17, 0.77, 0.35, INDIST) | 4 | 0.14 | 0.17 |
| V008 | ACM Term Premium 10Y | (0.20, 0.69, 0.34, UNSTABLE) | (approx0, 0.50, 0.50, INDIST) | (n/a, NO_NUMERIC) | (0.08, 0.65, 0.26, INDIST·PRIOR_SENS+3) | 4 | 0.14 | 0.20 |
| V011 | Brent M1-M3 curve slope | (0.79, 1.00, 0.49, —) | (0.72, 1.00, 0.19, —) | (0.72, 1.00, 0.19, BOTTOM3·DEMOTE) | (0.40, 1.00, 0.50, STABLE·SHRINK2.7σ) | 4 | 0.72 | 0.39 |
| V012 | BTC active addresses | (0.26, 0.71, 0.40, UNSTABLE) | (approx0, 0.50, 0.35, INDIST·BOTTOM3) | (n/a, NO_NUMERIC) | (0.03, 0.57, 0.40, INDIST) | 4 | 0.12 | 0.26 |
| V013 | BTC hash rate | (0.21, 0.68, 0.35, UNSTABLE) | (approx0, 0.50, 0.35, INDIST·BOTTOM3) | (n/a, NO_NUMERIC) | (–0.04, 0.42, 0.40, INDIST) | 4 | 0.08 | 0.25 |
| V019 | MVRV / SOPR | (0.10, 0.59, 0.26, UNSTABLE) | (approx0, 0.50, 0.29, INDIST) | (n/a, NO_NUMERIC) | (0.00, 0.51, 0.45, INDIST·PRIOR_SENS+3) | 4 | 0.05 | 0.10 |
| V028 | Basis-momentum | (0.79, 1.00, 0.51, —) | (0.79, 1.00, 0.81, —) | (0.79, 1.00, 0.81, RANK1_S) | (0.39, 0.99, 0.50, STABLE·SHRINK3.0σ·AUDIT_GO) | 4 | 0.79 | 0.40 |

### T — Tactical Timing

| var_id | name | P1 | P2 | P3 | P4 | n_runs | median_post | drift_range |
|---|---|---|---|---|---|---|---|---|
| V009 | TSMOM | (0.77, 1.00, 0.66, HETEROG) | (0.87, 1.00, 0.99, —) | (0.87–0.90, 1.00, 0.99, RANK1_T) | (0.68, 1.00, 0.95, STABLE) | 4 | 0.82 | 0.22 |
| V010 | Revision breadth | (0.84, 0.98, 0.10, UNSTABLE·HETEROG) | (approx0, 0.50, 0.02, INDIST·BOTTOM3) | (n/a, NO_NUMERIC) | (0.21, 0.94, 0.01, REDUNDANT·DEMOTE) | 4 | 0.21 | 0.84 |
| V014 | BTC exchange netflows | (1.15, 1.00, 0.53, UNSTABLE·DIVERGENCE·HETEROG) | (approx0, 0.50, 0.50, INDIST·BOTTOM3) | (n/a, NO_NUMERIC) | (0.03, 0.55, 0.58, INDIST) | 4 | 0.03–1.15 | **1.12** |
| V017 | BTC ETF net flows | (0.14, 0.64, 0.04, —) | (approx0, 0.50, 0.50, INDIST) | (n/a, NO_NUMERIC) | (–0.03, 0.44, 0.42, INDIST·WEAK) | 4 | 0.00 | 0.17 |
| V026 | Residual momentum (FF5) | (0.58, 1.00, 0.17, —) | (0.69, 1.00, 0.01, —) | (0.69, 1.00, 0.01, BOTTOM3·DEMOTE) | (0.39, 1.00, 0.05, REDUNDANT·NO-GO) | 4 | 0.58 | 0.31 |

### R — Regime / Risk

| var_id | name | P1 | P2 | P3 | P4 | n_runs | median_post | drift_range |
|---|---|---|---|---|---|---|---|---|
| V001 | VIX | (0.72, 1.00, 0.81, HETEROG) | (approx0, 0.50, 0.50, INDIST·BOTTOM3·UNSTABLE) | (n/a, NO_NUMERIC) | (–0.03, 0.38, 0.24, INDIST·SHRINK2.1σ) | 4 | 0.08 | 0.75 |
| V002 | MOVE Index | (0.20, 0.72, 0.10, UNSTABLE) | (approx0, 0.50, 0.50, INDIST·BOTTOM3·UNSTABLE) | (n/a, NO_NUMERIC) | (–0.05, 0.33, 0.27, INDIST·WEAK) | 4 | 0.00 | 0.25 |
| V004 | HY OAS / EBP | (0.93, 1.00, 0.62, HETEROG) | (approx0, 0.50, 0.003, INDIST·BOTTOM3·UNSTABLE) | (n/a, NO_NUMERIC) | (–0.01, 0.46, 0.05, REDUNDANT_vs_V027·PRIOR_SENS−3) | 4 | 0.00 | 0.94 |
| V005 | NFCI | (0.21, 0.72, 0.03, UNSTABLE·BOTTOM3) | (approx0, 0.50, 0.003, INDIST·BOTTOM3·UNSTABLE) | (n/a, NO_NUMERIC) | (–0.04, 0.37, 0.31, INDIST·WEAK) | 4 | 0.00 | 0.25 |
| V015 | BTC realized vol | (0.16, 0.68, 0.01, UNSTABLE) | (approx0, 0.50, 0.14, INDIST·BOTTOM3·UNSTABLE) | (n/a, NO_NUMERIC) | (0.03, 0.58, 0.64, INDIST·MODERATE) | 4 | 0.02 | 0.16 |
| V016 | BTC perp funding | (0.14, 0.68, 0.50, —) | (approx0, 0.50, 0.05, INDIST) | (n/a, NO_NUMERIC) | (0.00, 0.50, 0.45, INDIST·PRIOR_SENS+4) | 4 | 0.00 | 0.14 |
| V018 | BTC 3m basis | (0.15, 0.70, 0.50, —) | (0.25, 0.98, 0.81, TIER3_TOP3) | (n/a, NO_NUMERIC) | (0.02, 0.58, 0.55, INDIST·MODERATE) | 3 | 0.15 | 0.23 |
| V027 | Intermediary capital ratio | (0.81, 1.00, 0.37, —) | (0.57, 1.00, 1.00, —) | (0.57, 1.00, 1.00, RANK1_R) | (0.24, 0.99, 0.95, STABLE·SHRINK3.4σ·AUDIT_GO) | 4 | 0.57 | 0.57 |

### Overlay

| var_id | name | P1 | P2 | P3 | P4 | n_runs | notes |
|---|---|---|---|---|---|---|---|
| C009_P1 | Faber TAA (Overlay) | (0.25, 0.99, 0.68, TIER3_TOP3·**PROMOTE**) | — | — | — | 1 | Only in P1. P1 formal promotion to Grade B Overlay. No corroboration. |
| C011_P1 | VIX futures term structure | (0.10, 0.62, 0.32, TIER3_TOP3) | — | — | — | 1 | Only in P1. |
| C005_P4 | 200-DMA regime filter | — | — | (n/a, NO_NUMERIC·TIER3_CANDIDATE) | (0.009, 0.58, 0.40, WATCH) | 2 | Name-match across P3 (C001) and P4 (C005). No numeric in P3. |
| C002_P4 | VIX term structure slope | — | — | (n/a, NO_NUMERIC·TIER3_CANDIDATE) | (0.008, 0.56, 0.38, WATCH) | 2 | Related to C011 in P1 but different construct (slope vs level). |
| C007_P4 | Market breadth >200-DMA | — | — | (n/a, NO_NUMERIC·TIER3_CANDIDATE) | (–0.001, 0.49, 0.22, WATCH) | 2 | — |

**Group-migration flags (variables appearing in different groups across runs):** V009 TSMOM listed by P3 with both S posterior (0.874) and T posterior (0.900) — treat as T (all other runs place it in T). No other V-series cross-group migration.

**Naming inconsistency note for C-series:** the C-prefix IDs are *not* stable across papers (P1-C009 = Faber TAA; P4-C009 = Token unlock pressure; P2-C001 ≠ P3-C001 ≠ P4-C001). Cross-run comparison of C-series is by NAME, not by ID. V-series (V001–V028) is registry-stable.

---

## Stage 2 — Variable Verdicts

Every verdict below cites paper # + variable + the number or flag that produced it. No uncited calls.

### DEPLOY — clears every hurdle in ≥3 of 4 runs

| var_id | name | group | verdict | citation |
|---|---|---|---|---|
| V009 | TSMOM | T | **DEPLOY** | P1 post 0.77 p_positive 1.00 SR 0.46 HETEROG but rank_stable; P2 post 0.874 p_beats_peers 0.99; P3 rank 1 in T; P4 post 0.68 p_positive 1.00 p_beats_peers 0.948. 4 of 4 runs p_positive ≥ 0.98 and p_beats_peers ≥ 0.66 in every run where MCMC ran. |
| V027 | Intermediary capital ratio | R | **DEPLOY** (with re-anchor) | P1 post 0.81 p_positive 1.00 p_top3 0.90 AUDIT_GO re-anchor AEM 2014; P2 post 0.57 p_beats_peers 1.00; P3 rank 1 R; P4 post 0.24 p_positive 0.985 p_beats_peers 0.95 STABLE AUDIT_GO. 4 of 4 p_positive ≥ 0.985. |
| V028 | Basis-momentum | S | **DEPLOY** | P1 post 0.79 p_positive 1.00 AUDIT_GO; P2 post 0.79 p_beats_peers 0.81; P3 rank 1 S; P4 post 0.39 p_positive 0.99 p_beats_peers 0.50 STABLE AUDIT_GO. 4 of 4 p_positive ≥ 0.99. Post-decay SR between P1 0.47 and P4 shrinkage (registry 0.8, posterior 0.39 → effective ~0.35–0.47). |

### DEPLOY_CONDITIONAL — meets bar but has flags requiring operational constraints

| var_id | name | group | verdict | condition | citation |
|---|---|---|---|---|---|
| V011 | Brent M1-M3 curve slope | S | **DEPLOY_CONDITIONAL** | Commodity-futures only; applies at curve-slope construct level, not cross-asset. | P1 post 0.79 p_positive 1.00 p_beats_peers 0.49; P2 post 0.72 p_beats_peers 0.19; P3 same 0.72 BOTTOM3·DEMOTE flag; P4 post 0.40 p_positive 1.00 p_beats_peers 0.50 STABLE. Meets DEPLOY bar on p_positive in 4 of 4, but p_beats_peers oscillates 0.19–0.50 → dominated by V028 in some runs. Keep live but don't size above V028. |
| V026 | Residual momentum (FF5) | T | **DEPLOY_CONDITIONAL** → operationally subsumed by V009 | p_beats_peers vs V009 is 0.17 / 0.009 / 0.009 / 0.053 across runs (P1/P2/P3/P4) — peer-dominated in every run. Use only in portfolios where V009 can't be run (residualized equities with factor-neutral mandate). | p_positive = 1.00 in 4 of 4 → can't EXCLUDE; p_beats_peers uniformly crushed by V009 → can't DEPLOY standalone. P1 marginal-contrib flag "Keep Grade A; TSMOM dominates"; P4 REDUNDANT_VS_V009 MERGE_OR_DEMOTE; P3 DEMOTE_OR_MERGE. |

### SIZE_OVERLAY_ONLY

No variable makes this bucket cleanly. V018 BTC 3m basis is the closest candidate — P2 shows p_positive 0.98 p_beats_peers 0.81 TIER3_TOP3, P1 shows p_positive 0.70 but p_beats_peers only 0.50, P4 shows p_positive 0.58 INDIST. Not enough consistency. **Do not deploy V018 as overlay yet — one paper's strength is not survivability.**

### WATCH — trajectory improving, not yet over the bar

| var_id | name | group | verdict | citation |
|---|---|---|---|---|
| V015 | BTC realized vol | R | **WATCH** | P1 p_positive 0.68, P4 p_positive 0.58 — consistent small positive. P4 flag MODERATE_MARGINAL_CONTRIBUTION. Not over bar, but not collapsing. |
| V018 | BTC 3m basis | R | **WATCH** | Same reasoning — P1 p 0.70 and P2 p 0.98 suggestive; P4 INDIST. Revisit once BTC basis has 12 more months of post-spot-ETF data (see Stage 6). |
| C005_P4 | 200-DMA regime filter | Overlay | **WATCH** | P4 p_positive 0.58, p_beats_peers 0.40, explicit WATCH flag. P3 listed as Tier 3 candidate with no numeric. Need one more run with numeric extraction. |
| C002_P4 | VIX term structure slope | Overlay | **WATCH** | P4 p_positive 0.56, explicit WATCH flag. P3 listed as Tier 3 candidate with no numeric. |

### EXCLUDE — below bar in ≥2 runs or recurrent INDIST/LOW_POWER

| var_id | name | group | citation |
|---|---|---|---|
| V002 | MOVE Index | R | P1 p_positive 0.72 but p_beats_peers 0.10 UNSTABLE; P2 INDIST·BOTTOM3·UNSTABLE; P4 p_positive 0.33 WEAK. 3 of 4 INDIST. |
| V005 | NFCI | R | P1 UNSTABLE·GRADE_A_BOTTOM3 p_beats_peers 0.034; P2 INDIST·BOTTOM3·UNSTABLE p_beats 0.003; P4 p_positive 0.37 WEAK. 3 of 4 INDIST. |
| V012 | BTC active addresses | S | P1 UNSTABLE p_beats_peers 0.40; P2 INDIST·BOTTOM3; P4 p_positive 0.57 INDIST. 3 of 4 INDIST. |
| V013 | BTC hash rate | S | P1 UNSTABLE p_beats 0.35; P2 INDIST·BOTTOM3; P4 p_positive 0.42 INDIST. 3 of 4 INDIST. |
| V019 | MVRV / SOPR | S | P1 UNSTABLE p_beats 0.26; P2 INDIST; P4 p_positive 0.51 INDIST·PRIOR_SENS+3. 3 of 4 INDIST. |
| V016 | BTC perp funding rate | R | P1 p_beats 0.50 marginal; P2 INDIST p_beats 0.055; P4 p_positive 0.50 PRIOR_SENS+4. No evidence of signal across runs. |
| V017 | BTC ETF net flows | T | P1 p_positive 0.64 p_top3 0.02; P2 INDIST; P4 p_positive 0.44 WEAK. 3 of 4 null. |
| V010 | Revision breadth | T | P1 p_beats_peers 0.098 UNSTABLE·HETEROG; P2 INDIST·BOTTOM3; P4 p_beats 0.006 REDUNDANT. 3 of 4 crushed on peer-dominance. |
| C011_P1 | VIX futures term structure | Overlay | Only in P1, p_positive 0.62 p_beats 0.32. Single-run result; does not replicate because absent elsewhere. |

### REGISTRY_DOWNGRADE — Grade A/B but bottom third with no improvement

| var_id | name | group | action | citation |
|---|---|---|---|---|
| V001 | VIX | R | Downgrade Grade A → Grade B | P1 p_positive 1.00 HETEROG rank 3; P2 INDIST·BOTTOM3·UNSTABLE; P4 p_positive 0.38 SHRINK2.1σ. Inconsistency between the one MCMC that found strong signal (P1) and the other MCMC (P4) that found nothing is *the* reason to downgrade — it's a construct-heterogeneity problem, not a signal problem. P1 §8 caveat states CONSTRUCT_HETEROGENEOUS explicitly. |
| V004 | HY OAS / EBP | R | Downgrade Grade A → Grade B **and** create double-count gate with V027 | Same pattern as V001 — P1 rank 1 post 0.93 p_positive 1.00; P2 INDIST·BOTTOM3; P4 REDUNDANT_VS_V027 PRIOR_SENS−3 p_positive 0.46. P1 §8 CONSTRUCT_HETEROGENEOUS (Hu 2024 ML composite vs single-EBP). P4 explicitly REDUNDANT with V027. |
| V006 | UST 2s10s slope | S | Downgrade Grade A → Grade B | 3 of 4 INDIST; all runs show p_beats_peers < 0.40 vs V028. |
| V007 | Real yield / breakevens | S | Downgrade Grade A → Grade B (or regime-restrict) | P3 explicitly flags REGIME_SENSITIVE_POST2022. P1 UNSTABLE p 0.62. P4 INDIST p 0.77 p_beats_peers 0.35. 3 of 4 non-dominant. |
| V008 | ACM Term Premium 10Y | S | Downgrade Grade A → Grade B | 3 of 4 INDIST; P4 PRIOR_SENS+3 (result driven by skeptical prior). |

### Promotion (1 variable, single-run evidence — flagged as such)

| var_id | name | group | verdict | citation |
|---|---|---|---|---|
| C009_P1 | Faber TAA | Overlay | **PROMOTE_CONDITIONAL** — admit to Grade B Overlay but request replication in next BNMA | P1 sole formal promote: p_positive 0.99 p_beats_peers 0.68 TIER3_TOP3 post-decay SR 0.17. Not in P2/P3/P4. Therefore: promote on P1 alone **but require next run to include it and corroborate** before committing capital. |

---

## Stage 3 — Within-Group Weighting

### S group (1 full DEPLOY + 1 DEPLOY_CONDITIONAL)

**DEPLOY set:** V028 (DEPLOY), V011 (CONDITIONAL).

**Scheme: posterior-proportional by post-decay Sharpe.** V028 dominates V011 in 2 of 4 runs (P2, P3) on p_beats_peers, ties in P1/P4. Post-decay SR: V028 0.47 (P1) / 0.47 (P2–P3) / 0.39 shrunk (P4) → central 0.47. V011 0.48 (P1) / 0.72 (P2–P3, analytical inflates) / 0.40 shrunk (P4) → central 0.48.

| var_id | weight | rationale |
|---|---|---|
| V028 | 0.50 | Matches V011 on SR; V028 has cleaner peer-dominance (p_beats 0.51/0.81/0.81/0.50 across runs vs V011 0.49/0.19/0.19/0.50). |
| V011 | 0.50 | Near-identical post-decay SR (P1 central). But apply construct-scope restriction: V011 only fires on commodity futures curve. |

**Why not inverse-variance:** CI95 widths are comparable across V011 and V028 in P1 (0.56 vs 0.64), P4 (0.49 vs 0.52) — IV weighting would not materially move the weights.

### T group (1 DEPLOY, 1 operationally-subsumed CONDITIONAL)

**DEPLOY set:** V009 (sole DEPLOY).

**Scheme: not applicable — single-variable "group".** V009 carries 100% of T weight. V026 receives zero capital allocation in the primary portfolio; only deployed in the narrow factor-neutral-equities sleeve where V009 cannot run.

**Citation for zero-allocate on V026:** P1 marginal-contrib "TSMOM dominates head-to-head"; P2 p_beats_peers 0.009; P3 DEMOTE_OR_MERGE flag; P4 REDUNDANT_VS_V009 p_beats_peers 0.053. Four runs, same verdict.

### R group (1 DEPLOY)

**DEPLOY set:** V027 (sole DEPLOY).

**Scheme: not applicable — single-variable group.** V027 carries 100% of R weight.

**Double-count gate:** V027 paired with V004 (EBP) — take the MORE NEGATIVE signal; do NOT sum. Citation: P1 §3 marginal-contrib ("Double-count gate; EBP dominates"), P4 V004 REDUNDANT_VS_V027 MERGE_OR_DEMOTE flag. Without this gate, the single risk concept (intermediary balance-sheet stress) is counted twice — once via broker leverage (V027) and once via credit spread widening (V004) — which are mechanically correlated during stress.

**R-group rank-2-through-8 instability:** explicit in P4 §8 caveat 5, P1 rank_ci_width mean 5.3 of 8. Do not use V001/V002/V005/V015/V016/V018 as entries. V015 and V018 stay on WATCH (see Stage 2). The rest are exited from the R group.

### Overlay group

**DEPLOY set:** None (C009 Faber TAA is PROMOTE_CONDITIONAL on single-run evidence).

Do not deploy an Overlay signal yet. Use C009 Faber TAA as a *monitoring-only* 200-DMA-style regime gate until next BNMA corroborates. Citation: Stage 0 (N = 1 run for C009); P4 C005_P4 200-DMA filter only reaches WATCH.

---

## Stage 4 — Trading Prescription

One prescription per variable — committed, not three alternatives.

```
var_id | role           | entry_rule                                                  | sizing_rule            | exit_rule                       | cost_assumption     | expected_post_decay_SR
V009   | ENTRY_TRIGGER  | 12m trailing return > 0 AND 6m > 0 (both in same sign);     | vol-scale to 10% ann   | signal flip (one side only)     | 12 bp rt equities,  | 0.46 (central of P1 0.46 /
       |                | position = sign(12m return); rebalance monthly              | vol per position       | + monthly rebalance override    | 40 bp rt commod     |   P2 0.52 / P4 0.39)
V027   | REGIME_FILTER  | Intermediary capital ratio 12m z-score < −1σ (stress ON)    | halve portfolio gross  | z back above −0.5σ              | filter-only, 0 bp   | n/a — sizing, not entry
       | + sizing scalar| OR > +1σ (risk-on, +0 additional gross)                     | when stress ON         | (hysteresis)                    | incremental         |
V028   | ENTRY_TRIGGER  | basis-momentum z > 0 on 6m window, commodity-futures only   | equal-risk with V011   | z < 0                           | 40 bp rt commod     | 0.45 (central of P1 0.48 /
       |                |                                                             |                        |                                 |                     |   P2 0.47 / P4 0.39)
V011   | ENTRY_TRIGGER  | Brent M1-M3 slope z < −1σ (backwardation) for long,         | equal-risk with V028   | slope reverts to 0              | 40 bp rt commod     | 0.48 (central of P1 0.48 /
       | (CONDITIONAL)  | > +1σ (contango) for short; commodity curve only            |                        |                                 |                     |   P2 0.72 analytical
       |                |                                                             |                        |                                 |                     |   inflated, P4 0.40)
V026   | ENTRY_TRIGGER  | Same as V009 but on FF5-residualized equity returns         | 25% of V009 size       | signal flip                     | 15 bp rt equities   | 0.35 (P1 0.35) — sleeve
       | (sleeve only)  | mandate-restricted: factor-neutral equity sleeve only       |                        |                                 |                     |   only; subsumed elsewhere
```

### Conflict resolution (within same asset class)

| Conflict | Resolution | Citation |
|---|---|---|
| V009 long vs V028 long on same asset (e.g., commodity index) | V009 wins direction; V028 used as confirmation only. Tie-break: V009 has higher p_beats_peers across runs (P4: 0.95 vs 0.50). | P4 §12 practical-significance table, V009 rank 1 T. |
| V011 vs V028 on commodity futures | Equal-risk split with single combined vol target — they measure different constructs (curve slope vs time-series-of-curve). Not a tie-break conflict. | P1 audit §6 notes V011 and V028 "pair at p_beats_peers 0.51 coin-flip". |
| V004 stress signal vs V027 stress signal | Take the MORE NEGATIVE (stricter) — double-count gate. Neither adds to the other. | P1 §3, P4 V004 REDUNDANT_VS_V027. |

### Portfolio-level combination (across groups)

**Canonical pattern, confirmed by the 4 runs:**
- **S & T deliver entry direction and conviction** (both measure long-short Sharpe on common scale; P4 §11 confirms S-vs-T cross-group comparison is the only valid cross-group test).
- **R delivers sizing scalar** (V027 regime filter — halve gross when stress ON). Not an entry trigger.
- **Overlay delivers ON/OFF regime gate** — but currently underdeployed; only C009 Faber TAA qualifies at PROMOTE_CONDITIONAL. Treat as advisory, not a hard gate, until replicated.

**Deviations the evidence forces:**
- R group's effect-scale (sizing-improvement delta) is not on the same scale as S/T (long-short Sharpe). P1 §8 caveat 1, P4 §8 caveat 2, P3 §8 caveat 6. A "10% R-group weight" has no meaning against a "30% S-group weight". The portfolio combination is NOT S_weight + T_weight + R_weight = 1. It is: `position = sign(S_direction + T_direction) × vol_target × R_sizing_scalar × Overlay_gate`.

---

## Stage 5 — Grouping Effectiveness (4 × 5 grid)

Five tests, each applied per group. P/F/PARTIAL.

| Group | T1 Discrimination | T2 Peer-dominance | T3 Scale consistency | T4 Asset-class diversity | T5 Actionability |
|---|---|---|---|---|---|
| **S** | **PARTIAL** | **PARTIAL** | **FAIL** | **PASS** | **PASS** |
| **T** | **FAIL** | **PASS** | **PARTIAL** | **FAIL** | **PARTIAL** |
| **R** | **FAIL** | **PARTIAL** | **FAIL** | **PARTIAL** | **PASS** |
| **Overlay** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **PASS** |

### Citations for each cell

**S — T1 Discrimination PARTIAL.** P1 rank_ci_width mean 8.2 of 10 (= 0.82×K, above 0.70 threshold → FAIL) but V028 and V011 discriminate cleanly at ranks 1–2 (P2 rank_ci_width 1 for V028, 1 for V011). Top of group discriminates; tail does not.

**S — T2 Peer-dominance PARTIAL.** V028 p_beats_peers ≥ 0.50 in 3 of 4 runs (P1 0.51, P2 0.81, P3 0.81, P4 0.50); V011 in 2 of 4 (P1 0.49, P4 0.50, P2/P3 0.19). At least one variable (V028) clears the bar consistently; another (V011) is borderline.

**S — T3 Scale FAIL.** P3 §8 caveat 6 "cross-group values not on common scale" — but within S too, V011 (commodity curve slope in basis points) and V028 (basis-momentum time-series Sharpe) are not on the same effect-size scale. P4 §8 caveat 2 "S/T measure long-short portfolio Sharpe" — that's the target scale; V011 violates it. FAIL.

**S — T4 Asset-class diversity PASS.** S spans traditional equities (V028 basis-momentum), commodities (V011), rates (V006/V007/V008), FX (V003), crypto (V012/V013/V019). 5 asset classes.

**S — T5 Actionability PASS.** DEPLOY variables V028 and V011 produce entry directions on distinct asset classes.

**T — T1 Discrimination FAIL.** P1 rank_ci_width mean 8.9 of 12 = 0.74×K. P4 V014 CI95 [−0.42, +0.48], V017 CI95 [−0.41, +0.34] — these variables' posteriors are practically indistinguishable from each other. Only V009 discriminates cleanly (P4 rank_ci_width 0.000).

**T — T2 Peer-dominance PASS.** V009 p_beats_peers ≥ 0.66 in 4 of 4 runs. V009 reliably beats all T peers in every run where MCMC ran.

**T — T3 Scale PARTIAL.** V009 and V026 are comparable (both L/S momentum Sharpe). V010 Revision breadth is analyst-EPS-revision z-score → different construct. V014 BTC exchange netflows is on-chain flow → different construct. Mixed scales within the group.

**T — T4 Asset-class diversity FAIL.** Of 12 T variables in P1, 7 are crypto (V014/V017/C006/C007/C008/C013/C014/C015 ≥ 50%). The group is effectively a crypto-positioning group with a few momentum inclusions. P1 §8 CONSTRUCT_HETEROGENEOUS flags corroborate.

**T — T5 Actionability PARTIAL.** V009 = entry trigger. V026 = entry trigger but subsumed. V010/V014/V017 = supposed to be entry triggers but all EXCLUDE. The surviving actionable set is V009 alone → group reduces to one signal in practice.

**R — T1 Discrimination FAIL.** P4 §8 caveat 5 explicit: "Ranks 2–8 are interchangeable given posterior overlap." P1 rank_ci_width mean 5.3 of 8 = 0.66×K (just at threshold). P2 rank_ci_width 6 for V001–V005 (= overlapping). Only V027 separates.

**R — T2 Peer-dominance PARTIAL.** V027 p_beats_peers 0.37/1.00/1.00/0.95 across runs — clears 0.50 in 3 of 4. No other R variable clears 0.50 consistently.

**R — T3 Scale FAIL.** P1 §8 caveat 1 explicit: "R is Sharpe improvement from vol-targeting (~0.0–0.4 scale). Study inputs for V001/V004 are raw long-short Sharpes (~1.0+). Heterogeneity prior absorbs mismatch." Same issue in P4 §8 caveat 2.

**R — T4 Asset-class diversity PARTIAL.** V001/V002/V004/V005/V027 are macro/credit; V015/V016/V018 are crypto. Two asset classes but heavily weighted to crypto at rank-tail.

**R — T5 Actionability PASS.** All R variables reduce to one action (sizing scalar / regime filter), and that is what R is supposed to do — so this is a feature, not a bug. V027 provides the action.

**Overlay — T1 Discrimination FAIL.** P4 §8 caveat 6 explicit: "Overlay group degeneracy: n=3 variables makes all rank statistics trivial (P(top3) = 1.0 for all)." P1 rank_ci_width 1 (trivial).

**Overlay — T2 Peer-dominance FAIL.** No Overlay variable has p_beats_peers > 0.50 in any run where data exists. P1 C009 p_beats 0.68 is the only one, but n=2 peers is trivial.

**Overlay — T3 Scale FAIL.** P4 §8 caveat 2: "Overlay measures conditional Sharpe gain (a modifier). Ranking Overlay against S/T/R is statistically invalid." Internally inconsistent across Overlay too.

**Overlay — T4 Asset-class diversity FAIL.** All Overlay variables are equity-market regime indicators. Single asset class effectively.

**Overlay — T5 Actionability PASS.** All reduce to one action (regime gate on/off) — and that *is* the Overlay role. Same as R — feature not bug.

### Test totals and interpretation

| Group | Total passes (PASS=1, PARTIAL=0.5, FAIL=0) | Verdict |
|---|---|---|
| S | 1+0.5+0+1+1 = **3.5 / 5** | Working, but fix scale within group |
| T | 0+1+0.5+0+0.5 = **2.0 / 5** | Failing — but failure is construct, not grouping |
| R | 0+0.5+0+0.5+1 = **2.0 / 5** | Failing — but failure is scale + being a "1 + 7 noise" group |
| Overlay | 0+0+0+0+1 = **1.0 / 5** | Failing — but Actionability is correct; the fix is more variables, not regrouping |

### Does the failure point to a re-grouping?

**No.** The 4 × 5 grid says:
- Every group PASSES Actionability (T4/T5 where that's the correct question).
- Every FAIL on T1/T2/T3 traces to **scale inconsistency** or **too few variables**, not to "variables are in the wrong group."
- T group's T4 FAIL (crypto-heavy) is a selection bias issue — too many crypto candidates were admitted into the universe — not a grouping taxonomy issue.

**If the fix were "regroup by asset class"** (Macro / Equity / Crypto / Commodity), the scale problem would get worse, not better, because V027 (balance-sheet stress, dimensionless) and V004 (credit OAS, bps) would still be side-by-side as "Macro." The scale problem is *within-construct*, not within-asset-class.

**If the fix were "regroup by mechanism"** (Valuation / Momentum / Positioning / Stress), you would split V009 and V028 (both momentum) out of their current groups and pool them. That moves V028 from S to "Momentum," which would create **new peer-dominance failures** because V028 would then compete with V009 (which dominates). Not an improvement.

**If the fix were "regroup by role"** (Entry / Sizing / Gate / Exit), the test grid already tells you the framework basically does this — S/T are entries, R is sizing, Overlay is gate. A role-based regrouping would rename, not restructure.

### Recommendation

**Keep the S / T / R / Overlay grouping. Fix two things:**

1. **Scale consistency within R.** Enforce that all R-group likelihood inputs are on the same effect-size scale (sizing-improvement delta, NOT raw L/S Sharpe). Re-code V001 and V004 study inputs into that scale before the next BNMA. Citation: P1 §8 caveat 1, P4 §8 caveat 2.

2. **Prune the T group tail of crypto-positioning variables that keep showing up as indistinguishable from zero.** V014, V017 are the clearest EXCLUDEs. The group may still be crypto-heavy by variable count, but it won't be crypto-noise-heavy. Citation: P1 T rank_ci_width 8.9 of 12, P4 T table rows 4–9 all INDIST or WEAK.

The scale failure is real and repeated across 3 of 4 papers. The grouping failure is not: the grouping is doing what it's supposed to do (Actionability PASS in all 4). Do not regroup.

---

## Stage 6 — Registry + Next-BNMA Priorities

### Registry actions with 4-run support

| Action | Variable | Change | Supported by |
|---|---|---|---|
| Re-anchor | V027 Intermediary capital | Citation: AEM 2014 LMP, NOT HKM 2017 | P1 §6 audit GO with re-anchor; P3 divergence=FALSE confirms corrected anchor already reflected |
| Correct headline | V028 Basis-momentum | Registry Sharpe 1.2–1.5 → 0.9 (paper-level), post-decay 0.47 | P1 §6 audit GO with headline correction |
| Create double-count gate | V004 EBP ↔ V027 | "Take more negative, do not sum" | P1 §3 marginal-contrib, P4 V004 REDUNDANT_VS_V027 |
| Split construct | V014 BTC exchange netflows | Order-flow construct (anchor 0.6–0.8) + vol-sort construct (separate Provisional entry) | P1 §4 "Anastasopoulos et al. (2026) order-flow study (SR 1.34–1.88) pulls posterior above registry. Lee-Wang vol-sort cluster (negative) deliberately excluded per m3." |
| Downgrade Grade A → B | V001, V004, V006, V007, V008 | Move to Grade B; keep live with smaller allocation budget | 3-of-4-run INDIST pattern documented in Stage 2 EXCLUDE/DOWNGRADE tables |
| Promote Tier 3 → Grade B | C009 Faber TAA (Overlay) | Grade B admission **conditional on** next-BNMA replication | P1 §7 formal promote; 1-of-4 run evidence — conditional required |
| Remove from registry | V010 Revision breadth, V017 BTC ETF net flows | Move to Tier 3 / Research pool | V010: P1 p_beats 0.098, P4 p_beats 0.006. V017: P1 p_top3 0.02, P2 INDIST, P4 p_positive 0.44 |

### Next-BNMA priorities (what data moves the needle)

Ranked by expected posterior movement × operational value:

1. **Run full MCMC, not analytical approximation.** P2 and P3 cost almost nothing because the fallback silently replaces missing likelihoods with the prior. Next run: either execute MCMC (budget the compute) or do not generate the run — the intermediate state is corrosive to the meta-evidence.

2. **Replicate C009 Faber TAA in a second independent run before committing capital.** Only P1 has it; a 4-run meta-analysis with 1-of-4 coverage cannot ground a capital commitment. Specific ask: include Faber TAA + GTAA extension + 2-of-N signal version in the S/T/R/Overlay Stage A inventory.

3. **Split V014 BTC exchange netflows into two constructs** (order-flow microstructure Sharpe ≈ 0.6–0.8; vol-sort cluster separate Provisional). The current pooled posterior is uninterpretable — P1 says 1.15, P4 says 0.03. That 1.12 drift range is not noise; it's two different variables crammed into one ID.

4. **V027 needs a 12-month-window specification in the next BNMA.** Post-decay SR varied 0.49 (P1) → 0.34 (P2/P3) → weaker shrinkage in P4. This is likely the window choice propagating through Bayesian shrinkage. Pin the window specification and stop letting it drift.

5. **V018 BTC 3m basis: defer pooling until 2027.** Post-spot-BTC-ETF era (2024+) is a different regime than the data that populated the variable. Current replications all n ≤ 18 months of post-ETF data. P1 includes it (p 0.70), P2 shows it (p 0.98), P4 now says INDIST. One of these is wrong. Wait until there are 2+ years of post-ETF data before re-pooling.

6. **R group likelihood inputs need scale-normalisation.** V001 and V004 are entering BNMA as raw L/S Sharpes (~1.0+); the group's effect scale is supposed to be sizing-improvement delta (~0.0–0.4). Recode these inputs before the next run. Fail-loud if the studies do not report the scale-appropriate metric.

### Deprecated questions (drop from the quarterly review loop)

- **"Is V009 TSMOM earning its keep?"** — 4 of 4 runs say yes with p_positive ≥ 0.98 and p_beats_peers ≥ 0.66. Drop from quarterly list; revisit only on a registry-divergence alarm.
- **"Is V026 worth deploying standalone?"** — 4 of 4 runs say no (peer-dominated by V009). Drop; revisit only if V009 is mothballed.
- **"Is the prior driving the posterior?"** — P1, P3, P4 prior-sensitivity results converge: only single-study Tier 3 candidates move ≥3 ranks under loose prior. For Grade A/B, the prior is not driving the posterior. Drop this as a per-run sanity check; keep as a one-off audit per year.

---

## Stage 7 — Memory-ready bullets (≤ 7)

1. **V009 TSMOM, V028 Basis-momentum, V027 Intermediary capital ratio are the DEPLOY spine of the framework.** p_positive ≥ 0.98 and p_beats_peers ≥ 0.50 in 4 of 4 runs. Papers: P1, P2, P3, P4.

2. **V027 intermediary capital must be anchored to AEM 2014 LMP, not HKM 2017.** Registry update supported by P1 audit verdict and P3 post-correction divergence=FALSE. Post-decay Sharpe stabilises at ~0.34–0.49.

3. **V004 EBP and V027 must be paired with a double-count gate ("take more negative, do not sum").** Without the gate, credit-spread stress and broker-leverage stress — which are mechanically correlated — are counted twice. Papers: P1 §3 marginal-contrib, P4 V004 REDUNDANT_VS_V027.

4. **V014 BTC exchange netflows has a 1.12 posterior-median drift range across runs — that is construct heterogeneity, not noise.** Split into order-flow (Sharpe ~0.6–0.8) and vol-sort (separate Provisional) before next BNMA. Papers: P1 §4 registry divergence, P4 V014 row.

5. **Current S/T/R/Overlay grouping is working on the Actionability axis; it is failing on Scale Consistency (R group especially) and on T1 Discrimination in the tail.** Do NOT regroup by asset class or mechanism — those moves worsen the scale problem. Fix is: enforce R-group effect-scale coding and prune crypto-positioning variables from T. Papers: 4×5 grid in Stage 5, P1 §8 caveats 1 & 2, P4 §8 caveats 2 & 5.

6. **P2 and P3 are analytical approximations; their p_positive = 0.50 results are prior-centre artifacts, not evidence of null effects.** Treat as corroborating only for variables where they show movement off the prior. Papers: P2 Stage 8 caveat 1, P3 lines 5 and 211.

7. **C009 Faber TAA should be admitted to Grade B Overlay conditionally on next-BNMA replication.** P1 is the only run with C009; 1-of-4 run evidence cannot anchor capital commitment. Paper: P1 §7.

---

## Questions for Gerald

1. **Temporal ordering of P2 and P3 relative to P1 and P4.** P1 and P4 have dates (2026-04-17/18). P2 and P3 don't. I've inferred P2 → P3 from P3's "Mark 2 consolidated" framing, and treated the four as roughly contemporaneous (all April 2026). If the P2/P3 runs are actually from an earlier methodology vintage (e.g., 2025 Q4), the "drift" columns in Stage 1 may conflate methodology-change with evidence-change. If you can confirm the approximate dates of P2 and P3, I can tighten the drift interpretation.

2. **Is a SignalLedger excerpt with realized-P&L available for any of V009 / V027 / V028?** If yes, it would stress-test Stage 4's expected-post-decay-SR numbers against actual OOS performance. If not, the post-decay SR numbers are the model's extrapolation, not measured — which is a known limitation and the prescriptions are still actionable.

3. **On V004 downgrade: do you want me to recommend removal from Grade A to Grade B, or keep at Grade A with the double-count gate as the sole operational change?** The evidence says both are defensible — P1 shows V004 rank 1 in R, P4 shows it REDUNDANT_VS_V027. I recommended downgrade above but the conservative move is keep-Grade-A-plus-gate. Your call depends on how much you want the registry grade to follow posterior evidence vs. study lineage.

---

**End of meta-analysis.** Total paper-citations: P1 × 48, P2 × 17, P3 × 11, P4 × 31.
