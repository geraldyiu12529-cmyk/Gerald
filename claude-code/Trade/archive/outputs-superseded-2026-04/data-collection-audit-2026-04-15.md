# Data Collection Audit: Variables Logged & Sufficiency for Analysis

**Date:** 2026-04-15  
**Question:** Do we collect sufficient data to analyse the 11 improvement solutions?  
**Answer:** Partially. You have robust daily collection for 50+ variables, but missing critical interaction data and ledger-side metadata.

---

## Data Inventory: Variables Currently Collected

### Daily Collection (Market Brief + Audit-Data Staging)

**Cross-Asset Risk (7 variables)**
1. VIX (close)
2. VIX3M (term structure)
3. VIX/VIX3M ratio (derived)
4. MOVE (bond vol)
5. DXY (dollar index)
6. HY OAS (credit stress)
7. NFCI (financial conditions)

**Rates (6 variables)**
8. 2Y UST yield
9. 10Y UST yield
10. 2s10s spread (derived)
11. 10Y real yield
12. 10Y breakeven inflation
13. ACM term premium (monthly, lagged)

**Equities — Single Stocks (12 variables, 12 tickers)**
14–25. NVDA, TSLA, AAPL, GOOGL, AMZN, META, TSM, INTC, MU, PYPL, PLTR, WDC (closing prices)

**Equities — Indices (2 variables)**
26. SPY (S&P 500 close)
27. QQQ (Nasdaq-100 close)

**Equities — International (2 variables)**
28. EWJ (Japan ETF close)
29. EWY (South Korea ETF close)

**Commodities (8 variables)**
30. Brent crude spot
31. WTI crude spot
32. Brent M1–M3 curve shape (front-back spread)
33. Gold spot
34. Silver spot
35. Copper spot
36. (2 gaps: Palladium, Platinum not scored)

**Crypto (9 variables)**
37. BTC spot price
38. ETH spot price
39. BTC realized volatility (computed from OHLC)
40. BTC perp funding rate (Binance)
41. BTC active addresses (on-chain)
42. BTC hash rate (on-chain)
43. BTC exchange netflows (on-chain)
44. BTC ETF net flows (dollar volume)
45. ETH ETF net flows (dollar volume)

**FX (2 variables)**
46. EURUSD spot
47. USDJPY spot

**Audit-Addition Variables (3 computed)**
48. Residual momentum (FF5-residualized, 12 single stocks) — *COMPUTED DAILY but readings near zero*
49. Intermediary capital ratio (PD equity/total, z-score) — *COMPUTED WEEKLY, lag ~2 days*
50. Basis-momentum (4w/12w ΔF1–F2 slope, 5 commodities) — *COMPUTED DAILY*

---

## **TOTAL: 50 Market Variables + 3 Audit-Addition Variables = 53 primary data points**

---

## Data Collected in Hypothetical Ledger (Signal-Level Metadata)

**Currently logged per signal:**
- ID, Date, Asset, Direction, S, T, C, R, Sum
- Blocking leg, entry price, ATR stop, TP1, TP2, invalidation date
- Signal price at review, current price, days elapsed, hypothetical P&L %
- Status (STILL_OPEN, HIT_TARGET, HIT_STOP, EXPIRED)
- Notes

**Total columns per signal:** ~18

**Signals logged to date:** 9 (0 promoted, 9 near-miss)

---

## Sufficiency Analysis: Which Improvement Solutions Can We Analyze Now?

### **Can Analyze Immediately (have data today)**

**✓ #3 Catalyst × Momentum Interaction**
- Have: Days-to-catalyst (from brief §6), T-score (computed daily)
- Missing: None; just need to add 2 ledger columns
- Sample size needed: 10–15 signals (can detect by end of April)

**✓ #5 Correlation Conflict Detection**
- Have: S, T, C, R scores per signal; theme tags (commodities, semiconductors, etc.)
- Missing: None; just need to add conflict-detection logic to signal-review
- Sample size needed: 20 signals (can detect by early May)

**✓ #10 Invalidation Velocity**
- Have: Invalidation date (in rec), signal date (in rec)
- Missing: None; just need to compute days-to-invalidation at review time
- Sample size needed: 15 closed signals (can detect by mid-May)

**✓ #11 Fail-Loud Cost/Benefit**
- Have: MISSING status logged, fallback score (can compute retroactively), signal outcome
- Missing: None; systematic tracking of counterfactual
- Sample size needed: 20 blocked signals (available now; 4 blocking in first batch)

**✓ #6 Rolling Win-Rate Shock Detection**
- Have: Signal status (HIT_TARGET, HIT_STOP, EXPIRED) after each week
- Missing: None; pure statistical test on binary outcomes
- Sample size needed: 20 signals minimum (can begin testing by May 1)

### **Can Analyze After N ≥ 30 Signals (by ~May 15)**

**✓ #4 Position-Sizing Tail-Risk**
- Have: Recommended size formula (from Risk Rules), signal outcomes
- Missing: Recommended size column in ledger (need to add)
- Sample size needed: 30 signals (by May 15)
- Blockage: Risk Rules sizing formula must be audited first — is it sound?

**✓ #1 Component Correlation Matrix**
- Have: S, T, C, R scores (all signals); can compute Pearson correlations
- Missing: None; purely statistical
- Sample size needed: 30 signals minimum (by May 15)
- Expected insight: Does residual momentum T correlate with raw TSMOM T? (Should be ~0.6–0.8 if truly FF5-orthogonal)

**✓ #7 Component Strength Asymmetry**
- Have: All signal outcomes + component scores
- Missing: None; pure statistical analysis
- Sample size needed: 30 closed signals (by May 15)
- Expected insight: Does T have 2× higher Sharpe than S? If yes, reweight.

### **Can Begin Analysis by N ≥ 60 Signals (by ~early June)**

**✓ #8 Sequential Probability Testing (SPRT)**
- Have: Signal outcomes, hypothesis (audit variable improves Sharpe ≥ 20%)
- Missing: Bayesian likelihood-ratio framework (infrastructure, not data)
- Sample size needed: 20–30 signals per variable (can begin by May 20)
- Expected insight: Demote/promote audit variables before 2026-10-14 deadline

**✓ #2 Regime-Conditional Threshold Optimization**
- Have: Regime label (logged with each signal), Sum, outcome
- Missing: Multiple regimes observed. Currently 1–2 regimes; need ≥3 to see pattern
- Sample size needed: ≥15 signals per regime (need regime diversity, not just N)
- **BLOCKER:** Will only work after observing a 3rd distinct regime (risk-off or sideways). Currently at "energy-shock" and "risk-on"; need market transition.

**? #9 Regime × Asset Sensitivity Heatmap**
- Have: All outcomes stratified by regime and asset
- Missing: Full regime-asset matrix diversity
- Sample size needed: ≥5 signals per cell; 12 assets × 4 regimes = 48 cells = 240 signals (Q3 2026)
- **BLOCKER:** Need 3–4 distinct regimes and broad asset participation. Early data shows equity-only signals; need crypto/commodity diversity.

---

## **The Data Gap Problem**

### **What We're NOT Collecting (that would improve analyses)**

**On the Ledger side (signal-level metadata):**

1. **Intraday high/low prices** for each signal
   - Currently: Only closing prices at signal time + review time
   - Need for: Precise target/stop-hit dates, intraday volatility during holding period
   - Impact on: Analyses #3, #10 (catalyst timing and invalidation velocity)

2. **Volatility regime at signal time** (e.g., VIX bucket, DVOL bucket)
   - Currently: Not logged
   - Need for: Volatility-conditional win rates
   - Impact on: Analysis #7 (component asymmetry may be vol-dependent)

3. **Momentum sign consistency** (e.g., T score vs realized move direction)
   - Currently: T score +1, but did price actually move in predicted direction?
   - Need for: Validate whether T is actually predictive or self-fulfilling
   - Impact on: Analysis #7 (may reveal T is weaker than it appears)

4. **Regime transition markers**
   - Currently: Regime labels assigned by trader judgment
   - Need for: Explicit date of regime break + what triggered it (e.g., "BTC broke $60k" → regime shift)
   - Impact on: Analysis #2 (threshold optimization needs to know *when* regimes change)

5. **Correlation structure at signal time**
   - Currently: Only static correlation observation
   - Need for: Rolling correlation windows (e.g., "7d rolling correlation between Gold/Silver at entry")
   - Impact on: Analysis #5 (conflict detection would be quantitative, not rule-based)

6. **Position-sizing recommendation** (from Risk Rules formula)
   - Currently: Not logged in ledger
   - Need for: Size-weighted vs equally-weighted win-rate curves
   - Impact on: Analysis #4 (cannot assess whether sizing adds or hides value)

7. **Catalyst outcome** (did catalyst surprise, confirm, or miss?)
   - Currently: Only "catalyst exists" flag
   - Need for: Surprise direction + magnitude
   - Impact on: Analysis #3 (catalyst × momentum interaction incomplete without surprise sign)

---

## **Verdict: Sufficiency by Solution**

| Solution | Data Status | Can Start | Full Analysis By | Blocker |
|----------|-------------|-----------|------------------|---------|
| #3 Catalyst × Momentum | Have baseline; need ledger columns | Now | 2026-05-01 (N≥15) | None |
| #5 Correlation Conflict | Have baseline; need logic | Now | 2026-05-01 (N≥20) | None |
| #10 Invalidation Velocity | Have baseline; need computation | Now | 2026-05-15 (N≥30) | None |
| #11 Fail-Loud Cost/Benefit | Have baseline; need analysis | Now | 2026-05-01 (N≥20) | None |
| #6 Rolling Win-Rate Shocks | Have baseline; pure stats | Now | 2026-05-01 (N≥20) | Low SNR (noisy) |
| #4 Position-Sizing Tail-Risk | **Missing ledger column** | 2026-04-20 | 2026-05-15 (N≥30) | Add size recommendation to rec |
| #1 Component Correlation | Have baseline; pure stats | 2026-05-01 | 2026-05-20 (N≥30) | Need 30 signals |
| #7 Component Sharpe Ratios | Have baseline; pure stats | 2026-05-01 | 2026-05-20 (N≥30) | Need 30 signals |
| #8 SPRT | Have baseline; need infrastructure | 2026-04-20 | 2026-05-15 (N≥24) | Set up Bayesian framework |
| #2 Regime-Conditional Thresholds | Have baseline; data-sparse | 2026-05-15 | 2026-06-30 (need ≥3 regimes) | **Need regime diversity** |
| #9 Regime × Asset Heatmap | Have baseline; data-sparse | 2026-06-15 | 2026-09-01 (N≥240) | **Need regime + asset diversity** |

---

## **Recommendations: Data Collection Priorities**

### **High Priority (implement this week)**

1. **Add to ledger columns:**
   - `Days_to_Catalyst` (already in brief; extract from catalyst calendar)
   - `Position_Size_Recommendation` (integrate Risk Rules formula into rec Step 6)
   - `Invalidation_Threshold` (explicit rule at signal time)
   - `T_Momentum_Direction_Match` (did actual price move match T+1 prediction?)

2. **Add to audit-data-staging:**
   - Regime bucket at time of signal (not just label)
   - VIX bucket at signal time (normal <15, elevated 15–20, stressed >20)
   - Whether catalyst is earnings (Y/N) — will help #3 analysis

3. **Set up sequential tracking file:** `/Trade/sequential-audit-test-2026.md`
   - Will log Bayes factors for each audit variable
   - Will feed into #8 SPRT analysis

### **Medium Priority (by end of April)**

4. **Intraday high/low tracking**
   - Once you have N ≥ 10 signals, start recording intraday high/low for closed positions
   - Required for precise target/stop-hit dates (impacts #3, #10)

5. **Regime transition markers**
   - Define objective regime-break criteria (e.g., "VIX closes above 25 → risk-off", "BTC breaks $70k → regime shift")
   - Log date of each transition to Memory.md §9
   - This is the bottleneck for #2 (threshold optimization)

### **Lower Priority (defer to Q2)**

6. **Correlation snapshots**
   - Once N ≥ 60, log rolling 7d correlations between key pairs (Gold/Silver, TSM/NVDA, BTC/ETH)
   - Refines #5 conflict detection from rule-based to quantitative

---

## **Expected Data Sufficiency Timeline**

```
Today (Apr-15):
  - 50+ market variables ✓
  - 9 signals with basic metadata ✓
  - 3 audit-addition computed ✓
  - Missing: ledger enrichment columns, regime transitions
  
Week 1 (Apr-20):
  + Add Days_to_Catalyst, Position_Size, Invalidation_Threshold
  + Begin #4, #8 (setup frameworks)
  Can fully analyze: #3, #5, #10, #11 (design phase)
  
May 1 (N≈30):
  + 30 signals logged
  Can fully analyze: #3, #5, #10, #11 (results), #6 (early alert)
  Can begin: #1, #7, #8 (have N ≥ 30)
  
May 15 (N≈45):
  + 45 signals
  Can fully analyze: #4, #8 (mid-confidence)
  Can begin: #2 (if 2nd regime observed)
  
June 1 (N≈60, 2 regimes):
  + 60 signals across 2 regimes
  Can fully analyze: #1, #7 (high confidence)
  Can begin: #2 if 3rd regime appears
  
July 1 (N≈90, 3 regimes):
  + 90 signals across 3 regimes
  Can fully analyze: #2 (regime-conditional thresholds)
  Plan: #9 (defer to Q3)
  
Q3 2026 (N≈200):
  Can fully analyze: #9 (regime × asset heatmap)
```

---

## **Summary: Do You Have Enough Data?**

**Short answer:** Yes, for **6 of 11 solutions**. Partially for **3 of 11** (need ledger enrichment). Limited for **2 of 11** (need regime diversity and sample depth).

| Category | Solutions | Status |
|----------|-----------|--------|
| **Can start immediately** | #3, #5, #10, #11 | ✓ Ready to go |
| **Need ledger enrichment** | #4, #8 | ⚠ Doable this week |
| **Need N ≥ 30–60** | #1, #6, #7 | ⚠ By May 15 |
| **Need regime/asset diversity** | #2, #9 | ⚠ By June–July |

**Data quality bottleneck:** Regime transitions. You won't be able to optimize thresholds (#2, highest ceiling) until you observe a **3rd distinct regime**. Currently have 1–2; need the market to transition to risk-off or sideways for full learning.

**Next step:** Enrich the ledger schema this week (add 4 columns). Begin tracking SPRT on audit variables. By May 1, run comprehensive analysis on #3, #5, #10, #11. By June 1, run #1/#7 reweighting. By July 1, optimize for regime conditioning.
