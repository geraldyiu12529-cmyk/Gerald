# Signal Review — 2026-04-15

## 1. Review Period

**Date range:** 2026-04-14 (system inception) to 2026-04-15
**New signals since last review:** 9 (first review; all new)
**Total signals in ledger:** 9 (0 promoted, 9 near-miss)
**Previous review:** None (inaugural review)

**Process note:** The 2026-04-14 trade rec (`trade-rec-2026-04-14.md`) documented 9 near-miss signals in its narrative but did not auto-append them to `hypo-ledger-2026.md`. This review retroactively logged all 9 to establish the performance tracking baseline. The daily-trade-rec skill's Step 9 (auto-append) should be verified for future runs.

## 2. Mark-to-Market Summary

All 9 signals are 1–2 days old (logged 2026-04-14, reviewed 2026-04-15). No signals have been closed. Mark-to-market uses web-search closing/intraday prices for Apr-14/15; intraday high/low data is not available for precise target/stop checks. All signals remain **STILL_OPEN**.

### Near-Miss Signals (all 9)

| ID | Asset | Dir | Sum | Blocking Leg | Price at Signal | Current Price (Apr-15) | Est. Move % | Status |
|----|-------|-----|-----|--------------|-----------------|----------------------|-------------|--------|
| N001 | EWY | Long | +3 | fail-loud (intermediary capital) | $107.61 | ~$146.79* | +36.4%* | STILL_OPEN |
| N002 | Copper | Long | +2 | C (no catalyst) | $6.01 | ~$5.84 | −2.8% | STILL_OPEN |
| N003 | Gold | Long | +2 | R−1 (crowded) | $4,761.42 | ~$4,781 | +0.4% | STILL_OPEN |
| N004 | Silver | Long | +2 | R−1 (crowded) | $75.60 | ~$79.19 | +4.7% | STILL_OPEN |
| N005 | Brent | Long | +2 | R−1 (crowded) | $97.89 | ~$94.79 | −3.2% | STILL_OPEN |
| N006 | WTI | Long | +2 | R−1 (crowded) | $97.22 | ~$93.00 | −4.3% | STILL_OPEN |
| N007 | TSM | Long | +2* | fail-loud (residual mom) | $370.60 | ~$370.00 | −0.2% | STILL_OPEN |
| N008 | AMZN | Long | +2* | fail-loud (residual mom) | $238.38 | ~$249.00 | +4.5% | STILL_OPEN |
| N009 | META | Long | +2* | fail-loud (residual mom) | $634.53 | ~$655.00 | +3.2% | STILL_OPEN |

**\*EWY price discrepancy (UNRESOLVED):** The brief recorded EWY at $107.61 (Yahoo/Apr-13), but web search consistently returns ~$146–147 for the Apr-14/15 close. A +36% one-day move is implausible for a country ETF. **This almost certainly reflects a data-quality issue in the original brief's source** — the $107.61 may have been a stale or incorrect price. The signal price ($107.61) is preserved as-is per append-only rules; the move % should not be trusted until Gerald verifies the correct entry price. If the entry price should have been ~$144–146, the actual move is approximately +2%.

**Caveat:** Prices sourced from web search summaries (Apr 14–15 2026) and may be approximate. Without intraday high/low data, target/stop breach checks are conservative (closing prices only).

## 3. Rolling Statistics

**EARLY DATA WARNING: The ledger contains 9 signals (0 promoted, 9 near-miss), all STILL_OPEN after 1–2 days. No closed signals exist. All statistics below are structural descriptions, not performance measures. Statistical conclusions require ≥ 30 closed signals.**

### Promoted Signals
- Total: 0. No entries have cleared the methodology's |Sum| ≥ 3 + checklist gate.
- Reason: The sole |Sum| = +3 signal (EWY) was blocked by a fail-loud Grade A MISSING variable (intermediary capital ratio).

### Near-Miss Signals
- Total: 9
- Blocking leg distribution:
  - **R−1 crowding:** 4 signals (Gold, Silver, Brent, WTI) — 44%
  - **Fail-loud (data gap):** 4 signals (EWY/intermediary capital, TSM/AMZN/META residual momentum) — 44%
  - **C (no catalyst):** 1 signal (Copper) — 11%
- No signals blocked by S or T weakness — all had S = +1 and T ≥ +1 where scorable.

### Counterfactual Early Read (1–2 days, NOT statistically meaningful)

| Blocking Leg | Signals | Avg Move % | Would Be Winning? | Interpretation |
|-------------|---------|------------|-------------------|----------------|
| R−1 (crowded) | 4 | −0.6% (ex-EWY) | 1 of 4 (Silver +4.7%; Gold flat; oil down) | **Weakly supports the R−1 gate** — oil longs (2 signals) down 3–4%, validating crowding concern. Silver the exception. |
| Fail-loud (data gap) | 4 | +2.5% (ex-EWY) | 2 of 3 (AMZN +4.5%, META +3.2%, TSM flat) | **Suggests potential missed opportunities** — equity names moving in signal direction. But 1–2 days is noise. |
| C (no catalyst) | 1 | −2.8% | 0 of 1 (Copper down) | Copper down without catalyst — gate functioning. |

### By Asset Class
| Class | Signals | Avg Move % | Notes |
|-------|---------|------------|-------|
| Equities | 3 (TSM, AMZN, META) | +2.5% | AMZN and META rallying; TSM flat pre-earnings |
| ETFs/Indices | 1 (EWY) | +36.4%* (suspect) | Price discrepancy — exclude from statistics |
| Commodities | 5 (Cu, Au, Ag, Brent, WTI) | −1.0% | Oil dragging average; silver strong |
| Crypto | 0 | — | BTC below |Sum| = 2 threshold |

### By Score Component
| Component | +1 Count | −1 Count | 0/Blank Count | Avg Move (when +1) |
|-----------|----------|----------|---------------|-------------------|
| S | 9 | 0 | 0 | +0.6% (all signals; not discriminating) |
| T | 4 (+1) | 0 | 2 (0), 3 (BLANK) | +0.4% (where scored) |
| C | 6 (+1) | 0 | 3 (0) | +0.6% (where +1) |
| R | 0 (+1) | 4 (−1) | 5 (0) | R−1 avg: −0.6% (ex-EWY) |

### By Regime
All 9 signals under: **Post-shock reflation unwind → cautious risk-on** (shifted from "energy-led reflation shock" on Apr-15). No regime variation yet.

## 4. Score Component Analysis

**Premature — 0 closed signals.** Structural observations from initial signal set:

**S (Structural):** All 9 signals had S = +1. Universal in this regime. Cannot assess predictive power without variation.

**T (Tactical/Trend):** 4 scorable signals all had T = +1 (raw TSMOM for ETFs/commodities). 3 single-stock signals had T = BLANK because residual momentum was MISSING. **Update (2026-04-15):** The audit-data-staging pipeline computed residual momentum for all 12 stocks — all near 0.00% (10-month approximate window). T-block is formally lifted but no positive residual momentum exists to drive T = +1. Equity signals remain at effective +2.

**C (Catalyst):** 6 of 9 had C = +1. Earnings season provides abundant catalysts. C is not currently discriminating.

**R (Risk/Crowding):** The active gate. 4 signals blocked by R = −1 (crowded commodity/precious metal positioning). Early 1–2 day evidence: oil down 3–4% (consistent with crowding concern), silver up 4.7% (exception — industrial demand/DXY narrative overriding crowding). Gold flat. The R-gate's value is directionally supported by the oil outcome but challenged by the silver outcome.

## 5. Gating Rule Assessment

**Fail-loud rule:** Blocked 4 of 9 near-misses (44%). **Update (2026-04-15):** All three audit-addition variables have now been computed for the first time:
- Intermediary capital: z = +1.86 (ample capacity) → R stays 0 for EWY; fail-loud caveat resolved
- Residual momentum: all 12 stocks near 0.00% → T = 0; formal block lifted but no positive signal
- Basis-momentum: computed for 5 commodities; WTI and Gold divergence caps fired (S capped at 0)

The fail-loud blocking frequency should drop in future recs as these pipelines are now operational. However, residual momentum near zero means equity signals won't reach +3 via T until idiosyncratic alpha emerges.

**R−1 crowding filter:** Blocked 4 signals. Oil-specific evidence (WTI −4.3%, Brent −3.2%) weakly supports the block. Silver (+4.7%) is a counterexample. **Key question for next review:** Does the oil decline continue, confirming crowding exhaustion? Does silver's breakout persist, suggesting R−1 is over-filtering for industrial metals with structural demand?

**Correlation gate:** Not directly tested (no promoted signals). Documentation correctly identifies Gold/Silver/Copper/Oil as one reflation/DXY theme and EWY/TSM/QQQ as another.

## 6. Audit-Addition Variable Review

**Critical update vs. inaugural state: All three variables moved from MISSING to COMPUTED on 2026-04-15 via the audit-data-staging pipeline.**

| Variable | Present | MISSING | Blocking (fail-loud) | First Reading | Impact | Status |
|----------|---------|---------|---------------------|---------------|--------|--------|
| Residual momentum (FF5) | 0/9 at signal time → computed Apr-15 | 3/9 blocked at signal | T = 0 for all 12 stocks (near-zero residuals) | All ~0.00% (10m window, approximate) | Block lifted but no +1 signal; equities stay Sum +2 | **PIPELINE LIVE; DATA WEAK** |
| Intermediary capital (PD ratio) | 0/9 at signal time → computed Apr-15 | 1/9 blocked at signal | z = +1.86, R stays 0 | Ratio 0.140 (above 3y mean 0.129) | EWY fail-loud resolved; no downgrade | **PIPELINE LIVE; FIRST VALUE** |
| Basis-momentum (4w/12w ΔF1–F2) | 0/9 at signal time → computed Apr-15 | 0 directly blocking | WTI: divergence cap (S → 0); Gold: divergence cap (S → 0); Brent/Silver/Cu: steepening, no cap | Mixed by commodity | WTI and Gold scores downgraded; would have demoted those near-misses further | **PIPELINE LIVE; DECISION-MOVING** |

**Assessment for 2026-10-14 six-month review:**
- **Basis-momentum** already demonstrates decision-moving contribution: WTI and Gold divergence caps fired, which would have reduced those signals' S-scores. This is the variable working as designed.
- **Intermediary capital** provided its first data point (z = +1.86, ample) — no downgrade triggered. Value will only become clear when z-score approaches or crosses −1σ.
- **Residual momentum** is pipeline-live but near-zero across all stocks, suggesting the approximate 10-month window with web-search-derived returns may be too noisy. Accuracy should improve as the Kenneth French data library publishes Feb–Mar 2026 factors.

## 7. Methodology Improvement Candidates

**No recommendations at this time.** The system has operated for 1–2 days with 0 closed signals.

**Patterns to MONITOR (not act on):**

1. **MONITOR — Basis-momentum divergence cap may be too aggressive for WTI in backwardated markets.** The WTI divergence cap (4w flattening while still in deep backwardation) capped S at 0, but WTI had previously rallied 30%+ in the supply-shock regime. If backwardated commodities with flattening basis-momentum still outperform, the cap may need nuancing. *Sample:* 1 signal, 1 day. *Status:* MONITOR.

2. **MONITOR — R−1 crowding may be over-filtering silver in industrial-demand-driven breakouts.** Silver (R = −1, blocked) is up +4.7% in 1 day while oil (also R = −1) is down 3–4%. The difference may be that silver's move is demand-driven (industrial + DXY) while oil's crowding was geopolitical-premium-based. If this divergence persists, R−1 may need differentiation between supply-driven and demand-driven crowding. *Sample:* 2 assets, 1 day. *Status:* MONITOR.

3. **MONITOR — Equity near-misses (AMZN +4.5%, META +3.2%) suggest fail-loud may be costing opportunities.** These moves are in the signal direction despite being blocked by residual-momentum MISSING. Now that the pipeline is live (all T = 0), these signals would still not have been promoted (Sum = +2), so the fail-loud gate is not the binding constraint — the T = 0 reading is. No action needed unless residual momentum turns positive for specific names. *Sample:* 3 signals, 1 day. *Status:* MONITOR.

4. **MONITOR — All signals long-only in a single regime.** System untested for shorts or regime transitions. *Status:* MONITOR — structural, not actionable.

5. **MONITOR — EWY price discrepancy unresolved.** Entry price $107.61 vs market ~$146–147. Gerald must verify. *Status:* PENDING HUMAN VERIFICATION.

## 8. Ledger Maintenance

- **Retroactive logging:** 9 near-miss signals from `trade-rec-2026-04-14.md` were logged to `hypo-ledger-2026.md` during this review cycle. Future trade recs should auto-append.
- **No rows closed** (all 9 remain STILL_OPEN after 1–2 days).
- **Mark-to-market prices updated** for all 9 near-misses with Apr-15 web-search data.
- **No corrections applied** (EWY discrepancy flagged but append-only rules prevent retroactive edit — Gerald must sign off).
- **No deduplication needed.**
- **Rolling Performance Summary** in the ledger updated with Apr-15 prices and counterfactual early reads.

---

Signal count at review: promoted(0) + near-miss(9) = total(9). Closed this week: 0. Still open: 9.

**EARLY DATA BANNER:** This is the inaugural signal review. The system has operated for 1–2 days with 0 promoted entries, 9 near-misses, and 0 closed signals. All statistical patterns described above are structural observations, not performance conclusions. Meaningful statistics require ≥ 30 closed signals. Treat all observations as hypotheses to monitor, not conclusions to act on.
