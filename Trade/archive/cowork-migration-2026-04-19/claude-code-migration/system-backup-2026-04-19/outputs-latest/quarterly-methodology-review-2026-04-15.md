# Quarterly Methodology Review — 2026-04-15

> **Early-stage review — statistical patterns below 30 signals are directional hypotheses, not evidence. Focus on system health checks rather than performance conclusions.**

> **First quarterly review — establishing baselines. All assessments are initial readings, not trend conclusions.**

> **Note:** This review fired on 2026-04-15, one day after system inception (2026-04-14). The scheduled first run was 2026-07-01. All dimension assessments below are structural readiness evaluations, not performance-based judgments. No dimension should be DEMOTED or RETIRED based on 1 day of data.

## 1. Review Summary

The trading recommendation system has been operational for 1 day (2026-04-14 to 2026-04-15). The ledger contains 9 near-miss signals (0 promoted, 0 closed). One weekly signal review has been conducted (inaugural, 2026-04-15). All three audit-addition variable pipelines (residual momentum, intermediary capital, basis-momentum) are now LIVE as of 2026-04-15, with basis-momentum already demonstrating decision-moving contribution (WTI and Gold divergence caps fired). The system is structurally healthy: the 8-step methodology was followed correctly, fail-loud rules fired as designed, R-gate blocked appropriately, and the scheduled pipeline (brief → news → preflight → rec) is operational. No methodology changes can be evidence-based at this sample size — this review establishes the baseline for future quarterly assessments.

## 2. Analytical Dimension Fitness Audit

### Summary Table

| # | Dimension | Status | Findings to date | Sample adequate? | Context cost (est. tokens) | Recommendation |
|---|-----------|--------|------------------|------------------|---------------------------|----------------|
| 1 | Win rate by score component (S/T/C/R) | Active | S=+1 universal (no variation); R−1 weakly validated by oil decline | No (0 closed) | ~300 | **RETAIN** — foundational |
| 2 | Win rate by asset class | Active | Equities +2.5%, commodities −1.0% (1-day unrealized) | No (0 closed) | ~200 | **RETAIN** — foundational |
| 3 | Win rate by regime label | Active | Single regime only ("post-shock reflation unwind") | No (1 regime) | ~150 | **RETAIN** — foundational |
| 4 | Blocking leg distribution (near-miss) | Active | R−1: 44%, fail-loud: 44%, C: 11% | Descriptive only | ~200 | **RETAIN** — high diagnostic value |
| 5 | Near-miss counterfactual | Active | R−1 blocks: oil down 3-4% (gate validated); fail-loud blocks: equities up 2-5% (missed opps?) | No (0 closed) | ~300 | **RETAIN** — core feedback loop |
| 6 | Audit-addition variable contribution | Active | Basis-momentum decision-moving (2 caps); intermediary capital resolved 1 fail-loud; residual mom all near-zero | Descriptive | ~250 | **RETAIN** — required for 2026-10-14 deadline |
| 7 | Threshold sensitivity (|Sum|=2 vs 3) | Active | No variation yet (all signals at +2 or +3-blocked) | No | ~150 | **RETAIN** — needed at scale |
| 8 | Score component interaction matrix | Active | All cells empty (0 closed signals) | No (need 30+) | ~400 | **RETAIN** — too early to assess |
| 9 | Time-to-exit distribution | Active | All cells empty (0 closed signals) | No (need 30+) | ~200 | **RETAIN** — too early to assess |
| 10 | MAE/MFE analysis | Active | All cells empty (0 closed signals) | No (need 30+) | ~200 | **RETAIN** — too early to assess |
| 11 | Catalyst resolution tracking | Active | All cells empty (no catalysts resolved yet) | No (need 15+) | ~200 | **RETAIN** — too early to assess |
| 12 | VIX-at-entry conditioning | Active | All 9 signals entered at VIX ~29 (single bucket) | No (need multi-regime) | ~200 | **RETAIN** — too early to assess |
| 13 | Near-miss counterfactual regression | Active | N=0 (requires N≥20 in sub-group) | No (need 60+) | ~300 | **RETAIN** — too early to assess |

**Total estimated context cost:** ~3,050 tokens for enhancement dimensions (8-13), ~1,550 tokens for original dimensions (1-7). Total ~4,600 tokens in weekly review cycle.

### Dimension Assessments

**Dimension 1 — Win rate by score component (S/T/C/R):** Foundational dimension. At inception, S=+1 is universal across all 9 signals (no variation to test), T is scorable for only 4/9 signals due to initial fail-loud gaps (now resolved), C=+1 for 6/9 (not discriminating during earnings season), and R is the active gate with R=−1 blocking 4 signals. The R-gate showed early validation: oil longs blocked by R−1 crowding fell 3-4%, while silver (+4.7%) represents a counter-example. No closed signals exist to compute actual win rates. RETAIN — this is the backbone of the signal evaluation system.

**Dimension 2 — Win rate by asset class:** One-day unrealized moves show equities +2.5% avg (AMZN, META up; TSM flat), commodities −1.0% avg (oil dragging; silver strong), ETFs/indices excluded (EWY price discrepancy). No crypto signals generated. Too early for any conclusion. RETAIN — essential for identifying asset-class-specific methodology weaknesses.

**Dimension 3 — Win rate by regime label:** All 9 signals fall under a single regime ("post-shock reflation unwind → cautious risk-on"). Regime variation is impossible until the macro environment shifts. RETAIN — value will emerge over multiple quarters.

**Dimension 4 — Blocking leg distribution:** Already providing diagnostic value. The 44%/44%/11% split (R−1 / fail-loud / C) reveals that the system's current binding constraints are crowding assessment and data pipeline completeness, not structural or tactical weakness. This informed the P0 fix of building the audit-data compute pipeline. RETAIN — proven useful for pipeline diagnostics even at N=9.

**Dimension 5 — Near-miss counterfactual:** The most actionable dimension even at N=9. The R−1 counterfactual (oil down, silver up, gold flat) provides the earliest testable hypothesis about gate calibration. The fail-loud counterfactual (equities moving in signal direction despite being blocked) surfaces potential missed opportunities. RETAIN — core feedback mechanism.

**Dimension 6 — Audit-addition variable contribution:** Mandatory for the 2026-10-14 deadline. Already shows differentiation: basis-momentum is decision-moving (WTI/Gold S-caps fired), intermediary capital provided first reading (z=+1.86, resolved EWY fail-loud), residual momentum is pipeline-live but near-zero. RETAIN — non-negotiable due to hard deadline.

**Dimension 7 — Threshold sensitivity:** No data variation yet. All near-misses are at |Sum|=2 or blocked-at-3. When the ledger has 30+ closed signals across |Sum| levels, this will inform whether the +3 threshold is too conservative or appropriately selective. RETAIN — needed at scale.

**Dimensions 8-13 (Enhancement dimensions — added 2026-04-15):** All six enhancement dimensions (interaction matrix, time-to-exit, MAE/MFE, catalyst resolution, VIX conditioning, near-miss regression) have zero populated cells. They were added on the same day as the system's first signal review, so this is expected. None can be assessed for fitness yet. All require minimum 15-30 closed signals across relevant sub-groups before producing findings. RETAIN all — they should be evaluated no earlier than the Q3 review (2026-07-01) when ~60-90 closed signals are expected.

## 3. Research Core Reconciliation

### Variable Reconciliation Table

| Variable | Grade | Scored in pipeline? | Ledger supports grade? | Regime concern? | Action |
|----------|-------|---------------------|------------------------|-----------------|--------|
| 1. 12m TSMOM | A | Yes (T-input for indices/ETFs/commodities/FX/crypto) | DATA GAP (0 closed) | No | DATA GAP |
| 2. Carry / roll yield | A | Yes (commodity curve slope) | DATA GAP | No | DATA GAP |
| 3. Credit spreads / EBP | A | Yes (HY OAS in R-overlay) | DATA GAP | No | DATA GAP |
| 4. Financial conditions / RORO | A | Yes (NFCI, VIX, DXY in regime) | DATA GAP | No | DATA GAP |
| 5. Policy-path surprise | A | Yes (FOMC in catalyst map) | DATA GAP | No | DATA GAP |
| 6. Equity valuation spread | A | Partial (P/S cited, no systematic scoring) | DATA GAP | No | DATA GAP |
| 7. Earnings revision breadth | A | Partial (narrative only, not scored as S/T input) | DATA GAP | No | DATA GAP |
| 8. Gross profitability / quality | A | Partial (narrative) | DATA GAP | No | DATA GAP |
| 9. Yield-curve forward-rate factor | A | Not observed in recent recs | DATA GAP | No | DATA GAP |
| 10. Term premium (ACM) | A | MISSING (Jan-2026 only; Apr not posted) | DATA GAP | Stale data risk | WATCH |
| 11. Inflation breakevens | A | Yes (T10YIE in rates dashboard) | DATA GAP | No | DATA GAP |
| 12. Real yields | A | Yes (DFII10 in dashboard) | Trad core flags R²=84%→3-7% for gold since 2022 | YES — gold link broken | WATCH |
| 13. Commodity inventories | A | Yes (EIA crude in catalyst map) | DATA GAP | No | DATA GAP |
| 14. Commodity front-back curve slope | A | Yes (Brent M1-M3, F1-F2) | DATA GAP | No | DATA GAP |
| 15. FX interest-rate diff | A | Partial (DXY tracked, not differential) | DATA GAP | No | DATA GAP |
| 16. FX real valuation / PPP gap | B/A | Not observed in pipeline | DATA GAP | No | DATA GAP |
| 17. CFTC speculative positioning | B | Narrative only (crowding assessment) | DATA GAP | No | DATA GAP |
| 18. Dealer/customer order flow | B/A | Not available (free tier) | DATA GAP | No | DATA GAP |
| 19. Options-implied skew | B | Not observed in pipeline | DATA GAP | No | DATA GAP |
| 20. Variance risk premium | B | Not scored | DATA GAP | No | DATA GAP |
| 21. News-based text sentiment | B | Yes (news-events skill) | DATA GAP | No | DATA GAP |
| 22. Cross-asset correlation / beta | A (filter) | Narrative only (correlation gate documentation) | DATA GAP | No | DATA GAP |
| 23. Net supply / issuance | A (rates) | Not observed | DATA GAP | No | DATA GAP |
| 24. Buyback / net payout | B | Not observed | DATA GAP | No | DATA GAP |
| 25. Insider net buying | B | Not observed | DATA GAP | No | DATA GAP |
| **26. Residual momentum** | **A** | **Yes — pipeline LIVE 2026-04-15** | **DATA GAP (T=0 for all 12 stocks)** | **Data quality concern (10m window, approx FF5)** | **WATCH** |
| **27. Intermediary capital ratio** | **A** | **Yes — pipeline LIVE 2026-04-15** | **DATA GAP (first reading z=+1.86)** | **No — first data point, no trend** | **WATCH** |
| **28. Basis-momentum** | **A** | **Yes — pipeline LIVE 2026-04-15** | **Early positive: decision-moving (2 divergence caps)** | **No** | **CONFIRMED (early)** |

### Commentary

**All Top-25 variables: DATA GAP** — With 0 closed signals and 1 day of operation, no variable's grade can be empirically confirmed or challenged. The reconciliation table above is a structural audit of whether each variable is being scored in the pipeline, not a performance assessment.

**Grade A pipeline coverage:** Of the 25+3 variables, approximately 15-18 are actively pulled and scored in the daily pipeline. Variables 6-8 (equity valuation, revision breadth, profitability) appear in narrative but are not systematically scored as S/T/C/R inputs — they inform the analyst's judgment rather than feeding a quantitative leg. Variables 16, 18-20, 23-25 are not observed in the pipeline at all. This is acceptable for a discretionary framework (Gerald scores by judgment informed by data, not by algorithm), but the gap between "narrative mention" and "systematic scoring" should be monitored as the ledger grows.

**Variable #10 — ACM term premium:** MISSING since Jan-2026. This is a persistent Grade A data gap. The NY Fed publishes monthly with ~2-3 week lag. If Apr-2026 data is not available by early May, this becomes a chronic fail-loud item.

**Variable #12 — Real yields / gold:** The Trad core explicitly documents the post-2022 structural break (R² = 84% → 3-7%). The current framework correctly uses real yields as a dashboard item rather than a binding gold S-input, but this regime concern should be formally noted.

### Audit-Addition Variables — Status Update for 2026-10-14 Deadline

**Timeline:** 183 days remain until the 2026-10-14 hard deadline. All three variables became pipeline-LIVE on 2026-04-15 (day 1 of operation).

**Basis-momentum (S-input, commodities):** Already decision-moving. The WTI and Gold divergence caps (4w flattening while static slope still backwardated) reduced those signals' S-scores from +1 to 0. This is exactly the behavior the variable was added to capture. Memory.md §10 has 2 contribution log entries. At current pace, this variable will comfortably clear the 2026-10-14 gate.

**Intermediary capital ratio (R-overlay, cross-asset):** First data point: z = +1.86 (ample dealer capacity, no downgrade triggered). The variable resolved the EWY fail-loud caveat, which is a structural contribution. However, the variable's core value proposition — leading HY OAS during stress — has not been tested because the regime has been broadly risk-on. It will only prove itself if a stress episode occurs before October. Memory.md §10 has 1 contribution log entry.

**Residual momentum (T-input, single stocks):** Pipeline live but all 12 stocks show near-zero residual returns (~0.00%). The 10-month approximate window using web-search-derived returns is noisy. Accuracy should improve as the Kenneth French data library publishes Feb-Mar 2026 factors (expected May-June 2026). Until the signal shows non-zero variation, it cannot be decision-moving. Memory.md §10 has 1 contribution log entry (block lifted, but no positive signal generated).

**Assessment:** Basis-momentum is on track for GO. Intermediary capital needs a stress test (regime-dependent — may not occur before October). Residual momentum needs data quality improvement and non-zero variation. Formal GO/NO-GO will be issued in the Q4 review (2026-10-01, closest to the deadline).

## 4. Variable Candidate Pipeline

| Candidate | Data ready? | Weekly review evidence? | Impl. cost | Recommendation |
|-----------|-------------|------------------------|------------|----------------|
| GEX (gamma exposure) as regime overlay | No — requires SpotGamma or options data infrastructure | Trad core §GEX cites 78% of days SPX closes inside predicted range | Medium (new data source, new column in ledger, regime overlay logic) | **DEFER** — no data infra; revisit when ledger has 60+ signals |
| Cross-asset lead-lag (BTC→ETH, NVDA→semis, copper→ISM, MOVE→VIX) | Partial — price data available; systematic lag computation not built | No weekly review evidence yet (1 review, no closed signals) | Medium (retroactive tagging possible; new ledger columns) | **DEFER** — build infrastructure after Q3 review if interactions dimension shows value |
| Correlation-regime signal quality (trailing 20d cross-asset correlation as filter) | Partial — price data available; filter logic not built | No evidence yet | Low-Medium (new column, filter logic in rec skill) | **DEFER** — needs 30+ signals to test filter value |
| Decision tree feature importance | No — requires 50+ closed signals for meaningful splits | No | High (new computation, interpretation overhead) | **DEFER** — revisit at 50+ closed signals (est. Q4 2026) |
| Calendar/seasonal effects (day-of-week, OpEx, FOMC week) | Yes — date data exists in ledger | No evidence yet | Low (tag existing signals; compute in review) | **DEFER** — can be retroactively computed once N≥30; no implementation needed now |

**Pipeline summary:** All candidates remain at DEFER. The system needs to build a meaningful signal history (30-60+ closed signals) before any candidate can be piloted. Retroactive tagging (calendar effects, lead-lag) can be applied later without changing the real-time pipeline now.

**Pipeline funnel:**
- Idea stage: 0 (none pending intake)
- Data assessment: 5 (all current candidates)
- Data ready: 0
- Piloting: 0
- Active: 0
- Retired: 0

## 5. Methodology Change Proposals

No RECOMMEND-status items exist from any source:

- **Weekly signal review §7:** 0 RECOMMEND items (5 MONITOR items from inaugural review)
- **Dimension audit (Step 2):** All 13 dimensions RETAIN (too early for any DEMOTE/RETIRE/PROMOTE)
- **Research reconciliation (Step 3):** No DOWNGRADE or UPGRADE candidates (all DATA GAP except basis-momentum early-CONFIRMED)
- **Variable pipeline (Step 4):** All DEFER (insufficient data)

### MONITOR Items Carried Forward

These are the 5 MONITOR items from the 2026-04-15 signal review, carried forward for weekly tracking:

```
### Item: SR-2026-04-15-M01

**Pattern:** Basis-momentum divergence cap may be too aggressive for WTI in backwardated markets
**Evidence:** 1 signal, 1 day — WTI divergence cap fired while still in deep backwardation
**Risk:** Cap may prevent valid backwardation-trend entries
**Status:** MONITOR — revisit at N ≥ 10 WTI signals
```

```
### Item: SR-2026-04-15-M02

**Pattern:** R−1 crowding may be over-filtering silver in industrial-demand-driven breakouts
**Evidence:** Silver +4.7% despite R−1 block; oil −3-4% (R−1 validated). 2 assets, 1 day.
**Risk:** Binary gate doesn't differentiate supply-driven vs demand-driven crowding
**Status:** MONITOR — revisit at N ≥ 10 precious metals signals
```

```
### Item: SR-2026-04-15-M03

**Pattern:** Equity near-misses moving in signal direction despite fail-loud blocks
**Evidence:** AMZN +4.5%, META +3.2% after 1 day. Fail-loud was not the binding constraint (Sum=+2 even with T resolved).
**Status:** MONITOR — resolved itself once audit-addition pipeline went live
```

```
### Item: SR-2026-04-15-M04

**Pattern:** All signals long-only in a single regime
**Evidence:** 9/9 signals are long. System untested for shorts or regime transitions.
**Status:** MONITOR — structural, requires regime shift to test
```

```
### Item: SR-2026-04-15-M05

**Pattern:** EWY price discrepancy unresolved
**Evidence:** Entry price $107.61 vs market ~$146-147. Almost certainly a data quality error in the original brief.
**Status:** PENDING HUMAN VERIFICATION — Gerald must confirm correct entry price
```

## 6. Context Budget Assessment

### Current Token Estimates (weekly review cycle)

| Component | Est. tokens | Notes |
|-----------|-------------|-------|
| Ledger (hypo-ledger-2026.md) — signal rows | ~1,350 (9 rows × ~150 tokens) | Grows ~150 tokens/signal/week |
| Ledger — rolling summary tables (original 7) | ~1,200 | Fixed overhead, cells populate as data arrives |
| Ledger — enhancement tables (6 new) | ~1,500 | Fixed overhead, mostly empty now |
| Ledger — column definitions + rules | ~500 | Fixed |
| Signal review file | ~3,000-4,000 | Grows with analytical sections |
| HTML report | ~8,000-12,000 | Not read into context (rendered separately) |
| **Total ledger read** | **~4,550** | Within budget |
| **Total weekly review context** | **~8,000-9,000** | Acceptable |

**Budget ceiling:** The enhancement dimensions added ~3,000 tokens to the weekly review's context budget. At 9 signals, the ledger is compact. At 80 signals (archival threshold), the ledger would reach ~12,000+ tokens for signal rows alone — the archival tier (Step 8A) is correctly configured to prevent this.

**Archival health:** No archival needed yet (9 rows, threshold is 80). The archive file does not exist. This is correct.

**Assessment:** Context budget is healthy. No trimming needed. The archival tier at 80 rows is appropriately set for the projected signal accumulation rate (~5-10 signals/week → archive threshold reached in ~8-16 weeks, roughly Q3 2026).

## 7. Action Items for Next Quarter

**For the Q3 review (2026-07-01, next scheduled run):**

- Re-run the full dimension fitness audit with actual closed-signal data. Expect 60-90 signals, of which 30-50 should be closed. This is the first review where statistical conclusions become directionally meaningful.
- Assess which enhancement dimensions (8-13) have produced any findings. If an enhancement dimension still shows "insufficient data" or "sample too small" across all cells at Q3, consider DEMOTE to on-demand.
- Re-run research core reconciliation with actual performance data. Focus on whether R−1 crowding gate and fail-loud rules are empirically validated.
- Assess whether any variable candidate has enough data to PILOT.
- Monitor the 5 MONITOR items from the inaugural signal review — are patterns persisting or resolving?
- Track audit-addition contribution log (Memory.md §10) entries — especially residual momentum, which needs to show non-zero variation.
- Verify Kenneth French data library has published Feb-Mar 2026 factors (expected May-June) — if not, residual momentum accuracy remains compromised.
- Track ACM term premium data availability — if still MISSING at Q3, escalate to permanent fail-loud item.

**For the Q4 review (2026-10-01, critical):**
- **MANDATORY: Formal GO/NO-GO recommendation for all three audit-addition variables ahead of the 2026-10-14 hard deadline.**
- Full statistical assessment of all 13 dimensions with 120+ expected signals.
- First meaningful variable candidate pipeline assessment.

**Next quarterly review date:** 2026-07-01 (scheduled task `quarterly-methodology-review`, cron `0 19 1 1,4,7,10 *`).

---

Review covers: 2026-04-14 to 2026-04-15 (1 day). Closed signals: 0. Open signals: 9 (all near-miss). Ledger health: OK (9 rows, well under 80-row archival threshold).
