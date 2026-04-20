# Risk Rules — Policy Doc

**Last updated:** 2026-04-18 (meta-integration additions — §1.B, §4.B, §5.A, §8)
**Status:** Active. Binding on every trade.

This file promotes the sizing, heat, and stop rules from `framework/Trad core.md` and `framework/Coin core.md` into explicit policy. Reference at every entry. When a rule here conflicts with research prose in the cores, this file wins.

---

## 1. Position Sizing

- **Method:** Inverse-ATR volatility targeting with fractional-Kelly overlay.
  - Position $ = (Target Risk $) / (ATR × Multiplier).
  - ATR multiplier: 2–3× for trending assets (commodities, crypto); 1.5–2× for equities.
  - Source: `framework/Trad core.md:203`.
- **Kelly fraction:** **Quarter-Kelly**, maximum 25% single-position cap.
  - Rationale: Full Kelly produces 40–60%+ drawdowns; quarter-Kelly is the professional consensus for crypto and is the right regime for current elevated VIX. Source: `framework/Trad core.md:205`, `framework/Coin core.md:53`.

### 1.B Intermediary-capital-aware sizing (V027 as primary sizer — added 2026-04-18)

V027 (NY Fed primary-dealer capital z-score) is the primary cross-asset sizer above the inverse-ATR / quarter-Kelly rules. Apply this tier first, then take the more restrictive of V027 and the standard sizer.

| V027 z-score regime | Sizing action | Scope |
|---|---|---|
| z > +0.5σ (capital expansion) | Full inverse-ATR sizing on V009 + V028 spine | All risk-asset sleeves |
| −1σ ≤ z ≤ +0.5σ (neutral) | Standard inverse-ATR sizing (no V027 adjustment) | All risk-asset sleeves |
| z < −1σ (capital contraction) | **Halve gross exposure** on all risk-asset sleeves | Equities, commodities, FX longs, crypto |

This sits *above* the quarter-Kelly cap. Take the more restrictive of the two. See also the Step 5 double-counting gate with V004 HY OAS in `framework/Methodology Prompt.md §4 Reconciliation note 2026-04-18`.

## 2. Risk per Trade and Portfolio Heat

- **Single position risk at stop:** 0.5–2% of portfolio.
  - 0.5% for illiquid names: PLTR, palladium, platinum. Source: `framework/Trad core.md:210`.
  - 1–2% for liquid names.
- **Total portfolio heat:** **6–8%** max (sum of all live position risks to stop). Source: `framework/Trad core.md:209`.
- **Sector cap:** 25% max any single sector. Source: `framework/Trad core.md:211`.
- **Crypto cap:** 5–15% of portfolio. Source: `framework/Trad core.md:211`.

## 3. Stops and Exits

- **Stops:** ATR-based trailing at 2–3× ATR. Not fixed-percentage.
  - Evidence: 2–3× ATR reduces momentum strategy max DD from −49.8% to −11.4% (Han et al. 2016, via `framework/Trad core.md:213`).
- **TP structure (crypto baseline):** TP1 at 1.5× ATR, TP2 at 3× ATR; at TP1 hit, move stop to breakeven. Source: `framework/Coin core.md:57`.
- **Chandelier exit:** 3× ATR below highest high for crypto trend follows. Source: `framework/Coin core.md:57`.
- **Time-to-invalidation:** Every thesis must also carry a date by which the setup must have moved in favor. A 4-week thesis that hasn't moved in 4 weeks is a failed thesis. Close and free the capital.

## 4. Drawdown Circuit Breakers

- At **−15% portfolio DD:** reduce gross exposure to 50%.
- At **−20% portfolio DD:** move to defensive (gold + cash overweight; no new risk-on entries).
- Source: `framework/Trad core.md:214`.

### 4.B Overlay drawdown gate (C009 Faber TAA — added 2026-04-18)

V033–V035 C009 Faber 10-month SMA is a per-sleeve drawdown circuit-breaker, independent of the −15% / −20% portfolio-level breakers above. Both gates apply; take the more restrictive.

- **SPY/QQQ below 10m-SMA** at previous month-end close → equity-sleeve gross to zero (no new longs). V009 + V028 continue to size inside the remaining non-gated sleeves.
- **GSCI (commodity aggregate) below 10m-SMA** → commodity sleeve to zero.
- **BTC-USD below 10m-SMA** → crypto sleeve to zero.
- **EFA (optional, international equity) below 10m-SMA** → EWJ/EWY sleeve to zero.

**Read cadence.** Overlay state flips only at end-of-month. Daily pipeline reads the last month-end close vs the 10m-SMA; intraday recompute is prohibited.

**Gate interaction.** If the portfolio is already at the −15% breaker and a sleeve is simultaneously gated off, the more restrictive rule wins — in practice both apply additively (reduce gross AND zero the gated sleeve). Log the binding constraint in `framework/Memory.md §2` Notes.

## 5. Correlation / Concentration Gate (Step 6 overlay)

Before accepting a |sum|≥3 signal as a fresh trade, check:
- Does this thesis share its primary regime variable with any open position? (e.g., Copper long + Gold long + Silver long = one reflation/DXY-weak bet, not three.)
- If yes: treat as an **add** to the existing theme and size the combined bet to the sector cap, not the per-position cap.
- BTC and ETH momentum fire simultaneously ~80% of the time (`framework/Trad core.md:199`) — never double-count these as independent.

### 5.A R-group scale-consistency (added 2026-04-18)

When multiple R-inputs (Step 5 risk overlay variables) flag the same stress on the same asset, **do not sum their contributions — count only the single most-negative input**:

- Post-2026-04-18 meta downgrade (pending Gerald approval at Phase 1 diff review): V001 VIX and V004 HY OAS are Grade B, retained for monitoring but not additively scored alongside V027.
- Primary R input is V027 (intermediary capital z-score). If V027 flags stress, V004 and V001 do not add to the score even if they also flag.
- If V027 is neutral but V004 and V001 both flag, take the more-negative of V004 / V001 for the R-score (single value, not their sum).
- V030 DealerGamma short-gamma regime also participates in this rule — when co-firing with V001, take the more-negative.

## 6. Rebalancing Cadence

- **Hybrid threshold rebalance:** monitor daily, rebalance when 5% absolute drift or a signal change. Tighter 3% bands for crypto.
- Source: `framework/Trad core.md:218`.

## 7. Pre-Entry Checklist (use every trade)

1. Methodology aggregate |sum| ≥ 3? (`framework/Methodology Prompt.md:73`)
2. Invalidation written, concrete, date-bounded? (`framework/Methodology Prompt.md:87`)
3. Correlation gate clean (Section 5 above)?
4. Per-position risk ≤ 2% AND portfolio heat post-entry ≤ 8%?
5. ATR stop set, not fixed %?
6. Catalyst scored and aligned (surprise vs confirmation dependency stated)?
7. **Step 1.5 Overlay Gate status for this sleeve is ON?** (added 2026-04-18; if OFF, position size × 0 — no trade regardless of Sum)
8. **V027 intermediary-capital sizing tier applied?** (added 2026-04-18; if z < −1σ, the halved gross sizing is the binding constraint)

If any answer is no: no trade.

## 8. Factor Sleeves (added 2026-04-18, meta-integration)

V029 BAB and V030 DealerGamma run as **independent factor sleeves**, separate from the V009 / V027 / V028 spine.

- **Each sleeve capped at 1/3 of V009's risk budget.**
- Do NOT aggregate sleeve weights into the spine sizing.
- Correlation gate still applies: if a BAB sleeve leg and a V009 spine long are on the same ticker, size to the combined sector cap, not double-sized.
- V030 DealerGamma is Grade B (single-paper, pending second replication). Review status at 2026-07-01 quarterly and at every trade rec referencing it.
- Sleeve weights, when active on a given day, are logged to the SignalLedger under `bab_sleeve_weight` and `dealergamma_sleeve_weight` (schema delta proposed at Phase 1 Gate 1 — see deployment memo for approval status).
