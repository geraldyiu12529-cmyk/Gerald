---
name: signal-review
description: Weekly out-of-sample performance review of the trade recommendation system. Marks-to-market every hypothetical signal in the SignalLedger sheet of `master-data-log.xlsx`, computes hit rates by asset class / score component / regime, and identifies methodology improvements. Use when the user asks to "review signals", "check performance", "how are the recs doing", "signal review", "ledger review", "weekly review of trades", "OOS performance", "out of sample", "track the recs", "hypothetical performance", or "improve the system". Also triggers on scheduled task `weekly-signal-review`. If the SignalLedger has fewer than 5 rows, the skill runs but flags that statistical conclusions are premature.
---

# Signal Review — Weekly Performance & Methodology Feedback Loop

This skill reviews every signal logged in the SignalLedger sheet of `master-data-log.xlsx`, marks them to market, computes performance statistics, and surfaces methodology improvement candidates. The output is a dated review file plus updates to the PerformanceStats sheet in Excel.

The core principle: this is an out-of-sample record. The signals were logged at rec time with the market price at that moment. The review looks at what happened *after* — did the market move in the signal's direction? Did the stop get hit? Did the target get hit? The answers feed back into methodology improvement, but only through Gerald's sign-off — never through automatic parameter changes.

---

## Step 1 — Read the inputs

1. `/mnt/Trade/master-data-log.xlsx` — read the **SignalLedger** sheet (all rows) using openpyxl. This is the sole signal store.
2. `/mnt/Trade/master-data-log.xlsx` — read the latest row of **RegimeHistory** (current regime label) and **PerformanceStats** (prior rolling statistics).
3. `/mnt/Trade/Methodology Prompt.md` — to understand what each score component means
4. `/mnt/Trade/Memory.md` — open positions (§2), watchlist (§5)
4b. `/mnt/Trade/memory-lessons.md` — the full lessons log. Read this (not Memory.md §8, which is now a pointer) when looking for repeated blocking patterns or prior methodology notes.
5. `/mnt/.auto-memory/MEMORY.md` — scan index for any relevant feedback memories
6. The most recent `signal-review-*.md` file in `/mnt/Trade/` (if one exists) — to carry forward any pending observations

If the SignalLedger sheet doesn't exist or has zero data rows, stop and tell the user: "The SignalLedger sheet is empty — the daily-trade-rec skill needs to run at least a few times before there's data to review."

## Step 2 — Expire stale signals, then fetch prices for live ones

**2a. Date-based expiry pass (no price fetch needed):**

Before fetching any prices, scan every OPEN row in the SignalLedger:
- **Near-Miss signals** past their `Inv_Date` (or past 4 weeks from signal date if `Inv_Date` is blank): mark `Status = EXPIRED` immediately. No price lookup required — the expiry is date-driven.
- **Near-Miss signals** whose corresponding Promoted signal was DE-PROMOTED: mark `Status = EXPIRED` with a note referencing the de-promotion. No price lookup required.
- **Promoted signals** past their `Inv_Date` that were never taken (`Taken != YES`): mark `Status = EXPIRED`. No price lookup required.

This pass eliminates the bulk of stale rows before any web searches run.

**2b. Price fetch for remaining live signals:**

For every row still `Status = OPEN` after the expiry pass, look up the current market price. Use these sources in order of preference:

1. The most recent `us-close-snapshot-*.md` or `market-brief-*.md` in `/mnt/Trade/` — these have closing prices for the full universe
2. WebSearch if the latest brief/snapshot doesn't cover a specific asset (e.g., `"{ASSET} price close {latest trading date}"`)

**Priority order for price fetches:** Promoted signals with `Taken = YES` first (these are real positions), then remaining Promoted signals, then Near-Miss signals last. If the skill is hitting web-search rate limits, Near-Miss price fetches can be deferred to the next weekly run — note which were skipped.

Record the current price for each fetched signal. This is the mark-to-market reference.

## Step 3 — Update signal statuses

For each OPEN signal that received a price in Step 2b, determine whether it should be closed:

**Promoted Signals:**
- `HIT_TARGET`: current price reached TP1 (or TP2 if TP1 was already hit). Use the conservative target — TP1 for the primary P&L calculation.
- `HIT_STOP`: current price breached the ATR stop level
- `EXPIRED`: the invalidation date has passed without hitting target or stop
- `STILL_OPEN`: none of the above — the signal is still live

Calculate `Hypothetical P&L %` = (current or exit price − entry price) / entry price × 100 × direction multiplier (×1 for long, ×−1 for short).

**Near-Miss Signals (that survived the Step 2a expiry pass):**
- `WOULD_HIT_TARGET`: price moved from signal price to what would have been target (use the rec's standard TP1 = 1.5× ATR from signal price)
- `WOULD_HIT_STOP`: price moved against the signal direction by 2.5× ATR (midpoint of the 2–3× ATR stop range)
- `EXPIRED`: more than 4 weeks elapsed (the standard time-to-invalidation from Risk Rules §3)
- `STILL_OPEN`: none of the above

Calculate `Hypothetical Move %` = (current price − price at signal) / price at signal × 100 × direction multiplier.

Fill in `Would Have Hit Target?` and `Would Have Hit Stop?` as YES/NO based on whether the price *at any point* during the signal's life reached those levels. If you only have current prices (not intraday highs/lows), note this limitation and use closing prices as a conservative approximation.

## Step 4 — Compute rolling statistics

Update the **PerformanceStats** sheet in `master-data-log.xlsx`. Calculate:

**Promoted Signals:**
- Total logged, taken vs not-taken split
- Win rate = (HIT_TARGET count) / (HIT_TARGET + HIT_STOP + EXPIRED count). Exclude STILL_OPEN.
- Average hypothetical P&L across all closed signals
- Best and worst individual signals

**Near-Miss Signals:**
- Total logged
- Counterfactual win rate = would-have-hit-target / (would-have-hit-target + would-have-hit-stop + expired)
- Blocking leg breakdown: count how many times each component (S, T, C, R, fail-loud) was the blocking leg

**By Asset Class:** Group signals into Crypto, Equities, ETFs/Indices, Commodities. Compute win rate and average move for each.

**By Score Component:** For each of S, T, C, R, compute the win rate when that component was +1 vs −1 vs 0. This reveals which score legs are actually predictive out of sample.

**By Regime Label:** Group signals by the regime label active at signal time (from the rec's §2). Compute win rate per regime.

**Score Component Interaction Matrix (2026-04-15 addition):**
For each pair (S×T, S×R, T×R, T×C, S×C, C×R), build a 3×3 contingency table (+1/0/−1 for each component) and compute win rates in each cell. The key question: does any pair produce a synergistic or antagonistic interaction — e.g., does S+1 AND T+1 win at a rate meaningfully higher than S+1 alone and T+1 alone would predict? Update the "Score Component Interaction Matrix" table in the PerformanceStats sheet. Flag any cell with a win-rate differential > 15pp as "SYNERGY" or "CONFLICT" (with sample size caveat).

**Time-to-Exit Distribution (2026-04-15 addition):**
For every closed signal (promoted and near-miss), compute `Days to Exit` = exit date − entry date. Bucket into ≤5 days, 6–14 days, 15–28 days, >28 days. Compute win rate and average P&L within each bucket. Update the "Time-to-Exit Distribution" table in the PerformanceStats sheet. If the >28-day bucket has a worse win rate than shorter buckets, flag for invalidation window review.

**MAE / MFE Analysis (2026-04-15 addition):**
For every closed signal:
- `MAE %` = (worst closing price before exit − entry price) / entry price × 100 × direction multiplier. If intraday data is unavailable, use worst daily close as a conservative estimate.
- `MFE %` = (best closing price before exit − entry price) / entry price × 100 × direction multiplier.
Fill these into the SignalLedger rows and update the "MAE / MFE Summary" table in the PerformanceStats sheet. Key diagnostics:
1. What fraction of winners had MAE exceeding half the stop distance? (If high → stops may be too tight, shaking out eventual winners.)
2. What fraction of losers had MFE exceeding half the target distance? (If high → trades that would have won are giving back gains before reversing, suggesting the target is too ambitious or trailing stops should be tighter.)

**Catalyst Resolution Tracking (2026-04-15 addition):**
For every signal whose named catalyst date has passed, classify the outcome:
- `SURPRISE`: catalyst broke in a direction the consensus didn't expect
- `IN-LINE`: catalyst delivered approximately at consensus
- `NO-SHOW`: the anticipated catalyst didn't materialize within the signal's window
- `OPPOSITE`: catalyst resolved directly against the signal's thesis direction
Fill `Catalyst Outcome` in the SignalLedger and update the "Catalyst Resolution Tracking" table in the PerformanceStats sheet. Compare win rates across categories. If SURPRISE signals significantly outperform IN-LINE, the system is correctly positioned for convexity. If NO-SHOW signals have the worst outcomes, the C-score may be overweighting event dependency.

**VIX-at-Entry Conditioning (2026-04-15 addition):**
Bucket all signals by VIX at entry: <15, 15–25, 25–35, >35. Compute win rate, average P&L, and average days-to-exit per bucket. Update the "VIX-at-Entry Conditioning" table in the PerformanceStats sheet. The key question: does the R-score adequately capture volatility-regime risk, or do high-VIX entries systematically underperform even when R=0 or R=+1? If so, recommend a VIX-conditional threshold tightening (e.g., require |Sum| ≥ 4 when VIX > 30) as a Methodology Change Candidate.

**Audit-Addition Variables:** For residual momentum, intermediary capital, and basis-momentum: count how many times each was present vs MISSING, how many times it was the blocking leg, and whether signals where it was present had better outcomes than signals where it was MISSING.

**Meta-Integration Variables (Phase 3 addition — SignalLedger cols 33–36):**

*Overlay Gate Outcomes (V033/V034/V035).* Parse `overlay_gate_status` per row. Bucket every signal by whether its sleeve was ON or OFF at signal time. For overlay-OFF signals with Type='Promoted' / Taken='NO' / Block_Reason ∈ {'OverlayGateOff', 'OverlayStagingMissing'}: compute the *counterfactual* move from Price_at_Signal to current price, and classify as would-have-hit-target / would-have-hit-stop / expired. The key question: does the gate's OFF state systematically protect returns (hypothetical PnL worse on OFF sleeves than ON)? Or does it systematically block winners (OFF counterfactual wins > ON actual wins)? Update the "Overlay Gate Outcomes" table in the PerformanceStats sheet with columns: sleeve, gate_state, N_signals, counterfactual_win_rate, actual_win_rate (gate-ON population only), gate_protection_pp. Flag gate_protection_pp below −10pp as GATE-BLOCKING-WINNERS.

*V027 Regime Bucket Conditioning.* Group signals by `v027_regime_bucket`. Compute win rate, average P&L, and average days-to-exit per bucket (expansion / neutral / contraction / MISSING). The key question: does the V027 sizing tier (Risk Rules §1.B) correctly downsize in contraction regimes? Compare realized P&L in contraction-bucket Taken=YES signals against the halved-gross-exposure expectation. Update the "V027 Regime Bucket Conditioning" table in PerformanceStats with: bucket, N_signals, win_rate, avg_pnl_pct, avg_days_to_exit, avg_bab_sleeve_weight, avg_dealergamma_sleeve_weight.

*BAB Sleeve Activation.* Split single-stock signals on `bab_sleeve_weight > 0` vs `= 0`. Compute win rate for each split. The key question: when V029 signals BAB-on (USMV − SPLV spread > 0), do our long single-stock signals on low-β names outperform? Require N ≥ 10 per split before drawing conclusions. Update the "BAB Sleeve Activation" table in PerformanceStats.

*DealerGamma* remains MISSING across this cohort (V030 subscription pending — expected MISSING until at least 2026-07-01). Count MISSING rows for audit completeness; no outcome analysis possible until subscription is live.

## Step 5 — Identify methodology improvement candidates

This is the most important analytical step. Look for patterns in the data that suggest the methodology could be improved. Be honest about sample size limitations — flag when a pattern is based on fewer than 10 signals.

**What to look for:**

1. **Score components that don't predict:** If a component (say, C) has similar win rates at +1 and −1, it's not adding information. Flag it as "non-discriminating" and note the sample size.

2. **Gating rules that are too aggressive:** If near-misses blocked by R−1 (crowding) would have hit their targets at a higher rate than promoted signals, the crowding filter might be too conservative. Conversely, if blocked signals consistently would have hit stops, the filter is working.

3. **Asset classes with systematic bias:** If commodity signals consistently underperform while equity signals outperform, there may be a regime-dependent issue with how S-scores are computed for commodities.

4. **Threshold sensitivity:** Are there signals at |Sum| = 2 that consistently move in the predicted direction? This might suggest the |Sum| ≥ 3 threshold is too conservative. Conversely, if |Sum| = 3 signals have a poor win rate, the threshold might be too loose.

5. **Audit-addition variable value:** Are the three 2026-04-14 audit additions (residual momentum, intermediary capital, basis-momentum) actually improving signal quality? Compare outcomes when they're present vs MISSING. This directly feeds the 2026-10-14 six-month review.

6. **Time-to-target patterns:** Are signals hitting targets quickly (within a week) or slowly (3–4 weeks)? This informs whether the invalidation window is well-calibrated.

7. **Regime dependency:** Do certain score combinations work in one regime but fail in another? For example, maybe S+1/T+1 signals work in risk-on regimes but fail in reflation-shock regimes.

8. **Near-miss counterfactual regression (2026-04-15 addition):** When the ledger has ≥ 20 near-miss signals with resolved outcomes, go beyond counting blocking legs. Ask: among near-misses blocked by the same leg (e.g., all R−1 blocks), which features predict whether they would have won or lost? If R−1 blocks in low-VIX environments would have won at 70%+ (the R filter is over-conservative when vol is calm), that's a specific, actionable finding. If R−1 blocks in high-VIX environments would have hit stops at 80%+ (the R filter is correctly protecting), that validates the filter. Document the pattern with the specific conditioning variable and sample size. Require N ≥ 15 in the sub-group before labeling RECOMMEND; below that, label MONITOR.

**What NOT to do:**
- Do not recommend changing variable weights or thresholds based on fewer than 30 signals. Flag the pattern and say "monitor — sample too small."
- Do not recommend adding new variables unless there's a clear, repeated failure mode that an existing Grade A/B variable from the research cores could address.
- Do not auto-adjust anything. Every recommendation goes into the "Methodology Change Candidates" section of the review file for Gerald to sign off on.

## Step 6 — Write the review file

Path: `/mnt/Trade/signal-review-{YYYY-MM-DD}.md`. Use this structure:

```
# Signal Review — YYYY-MM-DD

## 1. Review Period
[Date range of signals reviewed, count of new signals since last review, total signals in ledger]

## 2. Mark-to-Market Summary
[Table of all OPEN signals that were updated this week, showing: asset, direction, entry/signal price, current price, move %, new status. Group by promoted vs near-miss.]

## 3. Rolling Statistics
[Copy of the updated Rolling Performance Summary from the ledger — win rates, averages, breakdowns by class/component/regime. Flag any statistic based on < 10 signals with "(low N)" caveat.]

## 4. Score Component Analysis
[For each of S, T, C, R: is it discriminating? What's the win rate differential between +1 and −1? Which components are carrying the system vs which are noise?]

## 4A. Score Component Interactions
[For each component pair (S×T, S×R, T×R, T×C, S×C, C×R): is the interaction synergistic, antagonistic, or neutral? Table from the Rolling Summary interaction matrix. Flag any pair with win-rate differential > 15pp. Sample size caveats on every cell.]

## 4B. Time-to-Exit Analysis
[Distribution of days-to-exit by outcome (target hit / stop hit / expired). Is the invalidation window well-calibrated? Are certain asset classes resolving faster or slower than others? If >28-day bucket underperforms, flag for window review.]

## 4C. Stop & Target Calibration (MAE/MFE)
[Are stops too tight (many winners had deep MAE before recovering)? Are targets too far (many losers showed significant MFE before reversing)? Specific ATR-multiple adjustment candidates if evidence warrants and N ≥ 30.]

## 4D. Catalyst Resolution
[How did named catalysts resolve? Win rates by SURPRISE / IN-LINE / NO-SHOW / OPPOSITE. Is the C-score adding value or overweighting event dependency?]

## 4E. VIX-at-Entry Conditioning
[Win rates and P&L by VIX bucket (<15, 15–25, 25–35, >35). Does the R-score adequately capture vol-regime risk?]

## 5. Audit-Addition Variable Review
[For residual momentum, intermediary capital, basis-momentum: present vs MISSING counts, blocking-leg frequency, outcome differential. Feeds the 2026-10-14 six-month review.]

## 5B. Meta-Integration Variable Review (Phase 3, added 2026-04-25)
[Four sub-sections:
 (a) Overlay Gate Outcomes — per-sleeve gate-ON vs gate-OFF counts, counterfactual vs actual win rates, gate_protection_pp. Flag GATE-BLOCKING-WINNERS if any sleeve shows protection_pp < −10.
 (b) V027 Regime Bucket Conditioning — win rate, avg P&L, avg days-to-exit across expansion / neutral / contraction.
 (c) BAB Sleeve Activation — win rate split by bab_sleeve_weight > 0 vs = 0 on single-stock signals.
 (d) DealerGamma — MISSING count only; no outcome analysis until V030 subscription live.
 Feeds the 2026-10-14 six-month meta-integration review (shared cohort with V026–V028 Batch-1).]

## 6. Methodology Improvement Candidates
[Consolidated list of patterns worth monitoring or recommending. Each candidate: pattern observed, sample size, confidence level (MONITOR / RECOMMEND), and proposed change.]

## 7. Variable Discovery — Repeated Behavior (Source D)
[Flag any repeated blocking patterns that suggest a missing variable. If a pattern has appeared 3+ times across weekly reviews, write a Candidate row to the VariableRegistry sheet in master-data-log.xlsx. Clean/validate any Candidate entries accumulated during the week. Recommend REJECT for Candidates with no new evidence after 8 weeks.]

## 8. Escalation Flags
[CONDITIONAL — include only when ≥ 1 threshold below is breached. If none fire, omit this section entirely.]

Thresholds:
- **SCORE-LEG-COLLAPSE:** Any S/T/C/R win rate ≤ 40% over ≥ 10 closed signals → name component, rate, N.
- **DATA-SOURCE-DEGRADATION:** Any Grade A variable MISSING in ≥ 3 of last 5 daily briefs → name variable, miss count.
- **GATE-TOO-AGGRESSIVE:** Near-miss counterfactual win rate exceeds promoted win rate by > 15pp (≥ 10 each) → state both rates, blocking leg(s).
- **AUDIT-ADDITION-STALL:** Any audit-addition variable has 0 decision-moving contributions and > 90 days elapsed since 2026-04-14 → name variable, days elapsed.
- **OVERLAY-GATE-BLOCKING-WINNERS** *(Phase 3, added 2026-04-25)*: Any sleeve shows counterfactual_win_rate (gate-OFF) exceeding actual_win_rate (gate-ON) by > 10pp with N ≥ 10 gate-OFF signals → name sleeve, bot