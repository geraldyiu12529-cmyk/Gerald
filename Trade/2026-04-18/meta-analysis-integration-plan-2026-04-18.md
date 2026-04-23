# Meta-Analysis Integration Plan — 2026-04-18

Source: `full-review-meta-analysis-2026-04-18.html` (synthesizes BNMA × 4 + PL-NMA of 54 variables × 12 papers + systematic reviews × 10). Cross-referenced against `BNMA-meta-analysis-2026-04-18.md`, `PL-NMA-meta-analysis-2026-04-18.md`, `meta_results_compact.json`.

**Decision form:** Integration plan, no file edits. Phased rollout, Grade-cited, with explicit risks flagged.

---

## 1. Executive summary (ten lines)

1. The meta-analysis **confirms** the 2026-04-14 audit spine: **V009 (TSMOM), V027 (intermediary capital), V028 (basis-momentum)** are the three top-robust variables across every synthesis method. Keep them at Grade A.
2. It **promotes** five new variables with enough evidence to enter the framework now: **BAB, DealerGamma, GP/A, CEI, C009 Faber TAA**. All five appear in the PL-NMA top-10 OR as DEPLOY in ≥2 independent reviews.
3. It **contradicts** V026 (residual momentum, added 2026-04-14) — peer-dominated by V009 in all 4 BNMA runs. Current framework already mandate-restricts V026 to single-stock sleeves; meta says go further: **treat V026 as sleeve-only, never as a co-input with V009**.
4. It **flags V014 (BTC netflows) as construct-ambiguous** — order-flow leg works, vol-sort leg doesn't. Register as two variables (V014a/V014b), kill V014b.
5. It recommends **downgrading five variables A→B** on construct heterogeneity and/or V027-redundancy: V001 VIX, V004 HY OAS, V006 2s10s, V007 Real yield, V008 Term Premium. (I recommend **accepting V001 and V004 now, deferring V006/V007/V008 to 2026-10-14 audit review** — reasoning in §3.3.)
6. It recommends **an allocation topology**: 75% spine (V009+V027+V028), 20% satellite (BAB, DealerGamma, V011, GP/A, CEI), 5% overlay (C009 Faber TAA).
7. The **biggest current gap** is the absence of a dedicated **Overlay regime-gate layer** in the 8-step — C009 and siblings have nowhere to live. Proposed: add explicit "Overlay Gate" as a Step 1.5 input, sleeve-on / sleeve-off, non-additive to Sum.
8. The **second gap** is the single-stock sleeve: residual momentum is the only current single-stock input. Meta adds **GP/A (profitability), CEI (composite equity issuance), HMLDevil (factor-timing)** as cross-sectional companions — JKP-tangency implementation to avoid overlap double-count.
9. **Nomenclature mismatch**: Gerald's framework uses S=Structural, T=Tactical, C=Catalyst, R=Risk. Meta uses S=Sentiment, T=Tactical, R=Regime, Overlay, Stocks. Do **not** rename Gerald's bucket codes (live ledger depends on them); do map each meta variable to the correct Gerald bucket in a lookup table (§3.1).
10. **Rollout**: Phase 1 documentation (this week), Phase 2 data-pipeline additions (next 2 weeks, blocking), Phase 3 live scoring (after Phase 2 green), Phase 4 ledger re-validation at 2026-10-14 audit review.

---

## 2. What's confirmed / what's new / what's contradicted

### 2.1 Confirmed (no change)

| Variable | Role in framework | Why meta confirms | Action |
|---|---|---|---|
| V009 TSMOM (Grade A) | Step 3 Tactical, cross-asset | PL-NMA rank 1/54, θ=+2.46; 4/4 BNMA DEPLOY | Keep. |
| V027 Intermediary capital (Grade A, added 2026-04-14) | Step 5 Risk Overlay | PL-NMA rank 4/54, θ=+1.71; cleanest R-group separator | Keep. Promote to primary **sizer** (§3.2). |
| V028 Basis-momentum (Grade A, added 2026-04-14) | Step 2 Structural, commodities | PL-NMA rank 10/54 primary but **rank 1 within S-group** on S2 sensitivity; θ=+1.30 | Keep. Current divergence-cap rule is correct. |
| V011 Brent curve slope (Grade A) | Step 2 Structural, commodities | PL-NMA rank 12/54, θ=+0.78 DEPLOY_CONDITIONAL | Keep, no change. |
| V018 BTC basis (Grade B) | Step 3 Tactical, crypto | WATCH; θ=+1.32 primary but S2 rank drops to 19 — regime-dependent | Keep at Grade B, no change. |
| V015 BTC realized vol (Grade A) | Step 5 Risk Overlay, crypto | WATCH, θ=−0.17; post-ETF regime incomplete | Keep, note meta caution. |

### 2.2 New — recommend adopting now (5 variables)

| Variable | Proposed Grade | Proposed bucket | Mechanism | Evidence summary |
|---|---|---|---|---|
| **BAB** (Betting-Against-Beta, Frazzini-Pedersen 2014) | A | Step 2 Structural, single-stock + ETF | Leverage-constrained investors overweight high-beta; long low-β / short high-β earns Sharpe | PL-NMA rank 6/54, θ=+1.60; 4 papers; single-group "Other" with no peer shrink. |
| **DealerGamma** (options dealer gamma positioning, SqueezeMetrics-style) | B (single-paper; 2nd replication required before Grade A) | Step 5 Risk Overlay, single-stock / index | Short-gamma dealer regimes amplify intraday vol; long-gamma damps it | PL-NMA rank 5/54 primary, rank 5 S2; θ=+1.68; single review but cleanly decoupled from V009 |
| **GP/A** (Gross Profitability / Assets, Novy-Marx 2013) | A | Step 2 Structural, single-stock | Gross profitability predicts cross-sectional equity returns; Fama-French 5F component | PL-NMA rank 15, θ=+0.63; multiple reviews; canonical Grade A factor |
| **CEI** (Composite Equity Issuance, Daniel-Titman 2006) | A | Step 2 Structural, single-stock | Net share issuance is a real-investment disinvestment signal; predicts underperformance | PL-NMA rank 7, θ=+1.33; canonical Grade A |
| **C009 Faber TAA** (Faber 10-month SMA tactical asset allocation) | A | **New: Step 1.5 Overlay Gate** | Price-vs-10m-SMA as sleeve-on/off switch; drawdown circuit-breaker, not alpha sizer | PL-NMA rank 2/54, θ=+2.26; multi-review |

### 2.3 Contradicted / modified

| Variable | Current treatment | Meta finding | Proposed response |
|---|---|---|---|
| V026 Residual momentum (Grade A, added 2026-04-14) | Single-stock T-input, replaces TSMOM on 12 named equities | PL-NMA rank 53/54 (θ=−1.79); 4/4 BNMA peer-dominated by V009 | Keep mandate-restriction. Add rule: **never co-present V026 and V009 as independent inputs on the same ticker** (already true by mandate, make explicit). Flag for 2026-10-14 audit review: **demote to Grade B or remove** if OOS ledger shows no edge after 6-month live period. |
| V014 BTC exchange netflows (Grade B) | Not currently in framework (crypto variable but not in Top-28) | PL-NMA rank 3 primary but S2 rank 17 — construct-split | Do not adopt. Flag V014a (order-flow imbalance, specifically) as **candidate for 2026-07-01 lit-review scan**. |
| V001 VIX (Grade A) | Step 5 Risk Overlay | CONSTRUCT_HETEROGENEOUS in P1/P4 BNMA; WATCH | **Downgrade A→B now.** Still scored; no longer cited as primary R input when V027 is available. |
| V004 HY OAS (Grade A) | Step 1 Regime + Step 5 Risk Overlay | REDUNDANT_VS_V027 post-2008 (ρ≈0.65–0.75); BNMA INDIST in 2/4 runs | **Downgrade A→B now.** Apply existing double-count gate from Methodology Prompt §5: when both flag stress, count once. |
| V006 2s10s, V007 Real yield, V008 Term Premium (all Grade A) | Step 1 Regime inputs | Borderline downgrade evidence — 1 BNMA run flags each, not 2+ | **Defer. Keep Grade A** for now. Re-score at quarterly methodology review 2026-07-01 with a second independent replication pass. |
| R-group pad: V001/V002/V003/V005 | Currently all scored in Step 5 | Meta: "kill the R-group pad" — V002/V005 bottom-10; V003 endogenous | **V002 MOVE, V005 NFCI: EXCLUDE from active scoring** (keep in DataQuality for monitoring). **V003 DXY: retain as cross-asset sign gate only**, not as a scored R-input. |

### 2.4 Deferred to 2026-07-01 quarterly review

Sleeve-worthy but single-paper or needing replication: **HMLDevil, PCTECH, CieslakPovala, OppInsider, LazyPrices, CrossAssetValue, GoldTIPSbeta, GoogleSVI, QMJ, VRP, CorrelationRiskPremium, HedgingPressure, LM_Text, C005 200-DMA, C002 VIX term slope.** Add to `VariableRegistry` as WATCH; do not score live.

---

## 3. Proposed architecture changes, per authoritative document

### 3.1 `Methodology Prompt.md` — main surgery

**A. Variable list: Top-25 → Top-30**, with new entries and reclassifications.

Add to the Top-25 table:

| # | Variable | Grade | Step | Notes |
|---|---|---|---|---|
| 26 | V026 Residual momentum (FF5) | A (review 2026-10-14) | Step 3 — single-stock only | Already present; add "never co-score with V009 on same ticker". |
| 27 | V027 Intermediary capital ratio | A (review 2026-10-14) | Step 5 + sizing | Already present; elevate to **primary sizer** role. |
| 28 | V028 Basis-momentum (4w/12w) | A (review 2026-10-14) | Step 2 — commodities | Already present; no change. |
| 29 | **BAB (Betting-Against-Beta)** | A | Step 2 — single-stock + ETF | New. Long low-β / short high-β. Cap at 25% of V009's risk budget. |
| 30 | **DealerGamma** | B | Step 5 — single-stock + index | New. Short-gamma regime → widen R stop; long-gamma → tighten. Second replication required before A. |
| 31 | **GP/A (Gross Profitability)** | A | Step 2 — single-stock | New. JKP-tangency implementation with HMLDevil/QMJ when they arrive. |
| 32 | **CEI (Composite Equity Issuance)** | A | Step 2 — single-stock | New. Negative sign: high issuance = structural headwind. |
| 33 | **C009 Faber TAA** | A | **new Step 1.5 Overlay Gate** | New. Non-additive to Sum. Sleeve-on/off. |

**B. Add Step 1.5 — Overlay Regime Gate**

Between Step 1 (Regime) and Step 2 (Structural):

> **Step 1.5 — Overlay Regime Gate**
> Binary sleeve-on / sleeve-off switch applied *after* regime identification, *before* structural scoring. Inputs:
> - **C009 Faber TAA (Grade A)**: price vs 10-month SMA on SPY/EFA/GSCI/BTC. If below SMA → sleeve-off for that risk-asset class (go to cash/gold on that sleeve).
> - Sleeve-off does NOT zero the score — it multiplies the post-Sum position size by 0 for that sleeve.
> Output: sleeve status per asset class (on / off).

Non-additive to Sum. This answers meta-analysis Recommendation 7.1.4 (dedicated Overlay scope).

**C. Bucket nomenclature reconciliation — do NOT rename, add a lookup table**

The SignalLedger and every downstream tool uses Gerald's S/T/C/R buckets. Renaming would break OOS tracking. Instead, add an appendix:

> **Appendix: Meta-analysis group ↔ Gerald bucket crosswalk**
> - Meta "S" (Sentiment / Structural slow) → Gerald **S (Structural)**
> - Meta "T" (Tactical / momentum) → Gerald **T (Tactical)**
> - Meta "R" (Regime / macro conditions) → Gerald **R (Risk Overlay)**
> - Meta "Overlay" (gates) → Gerald **Overlay Gate (new Step 1.5)**
> - Meta "Stocks" (cross-sectional equity factors) → Gerald **S (Structural), single-stock sleeve**
> When citing a meta-analysis rank or posterior, disclose which group the variable sits in.

**D. Scoring rule additions**

- "V009 and V026 on the same ticker: score V026 only (mandate); do **not** sum."
- "V027 and V004 simultaneously flagging stress: count once (more-negative of the two)."
- "C009 Faber TAA sleeve-off: position size × 0 for that sleeve, regardless of Sum."
- "BAB and DealerGamma are independent sleeves — each capped at 1/3 of V009's risk budget."

### 3.2 `Risk Rules.md`

**A. V027 as primary sizer** (new §):

> **Intermediary-capital-aware sizing:**
> - z > +0.5σ (expansion): full inverse-ATR sizing on V009+V028 spine.
> - −1σ < z < +0.5σ (neutral): standard inverse-ATR sizing.
> - z < −1σ (contraction): halve gross exposure on all risk-asset sleeves.
> - This sits *above* the quarter-Kelly cap; take the more restrictive of the two.

**B. C009 Faber as drawdown circuit-breaker** (new §):

> **Overlay drawdown gate (C009 Faber TAA):**
> - SPY/QQQ sleeve below 10m-SMA: reduce equity gross to zero on that sleeve (allow V009+V028 inside remaining sleeves).
> - GSCI (commodities aggregate) below 10m-SMA: reduce commodity sleeve to zero.
> - BTC below 10m-SMA: reduce crypto sleeve to zero.
> - This gate is **independent of** the −15% / −20% portfolio drawdown breakers; both apply, take the more restrictive.

**C. R-group scale-consistency rule** (from BNMA-meta):

> **R-group aggregation:** when multiple R-inputs flag the same stress, do not sum. Count the single most-negative input (V027 or V004, pre-downgrade; V027 alone post-downgrade).

**D. BAB / DealerGamma sleeve sizing** (new §):

> **Factor sleeves:** BAB and DealerGamma each run as independent sleeves, each capped at 1/3 of V009's risk budget. Do NOT aggregate into the spine sizing.

### 3.3 `Data Sources.md`

**New variable pulls required:**

| Variable | Source | Frequency | Fallback chain | Notes |
|---|---|---|---|---|
| BAB | AQR BAB factor returns (Ken French-style download) OR replication from CRSP β-bucketed deciles | Monthly (ETF proxy: USMV/SPLV spread, daily) | AQR → French library → self-compute | ETF proxy acceptable for tactical use; canonical BAB for grading |
| DealerGamma | SqueezeMetrics GEX OR SpotGamma daily composite | Daily | SqueezeMetrics → SpotGamma → MISSING (no self-compute option) | Paid data, flag for subscription cost |
| GP/A | Compustat / Ken French GP portfolio | Quarterly (financials) | French library → Compustat → self-compute from CRSP/Compustat | Slow-moving; monthly rebalance of ranked basket |
| CEI | Daniel-Titman composite equity issuance (computed from CRSP+Compustat) | Quarterly | self-compute only | Document computation in `scripts/compute_cei.py` (new) |
| C009 Faber 10m-SMA | Yahoo Finance monthly closes on SPY/EFA/GSCI/BTC-USD | Monthly (end-of-month) | Yahoo → Stooq → MISSING | Trivial computation; extend `compute_audit_additions.py` |

All Grade-A new variables obey **fail-loud** rule: if MISSING on pull day, the corresponding score leg prints `MISSING — [sources attempted]` and does not block the day's scoring.

Extend the existing `audit-data-compute-750pm` scheduled task (or create a sibling `meta-additions-compute-755pm`) to pull BAB / GP/A / CEI / DealerGamma / Faber-SMA. Expected runtime +3–5 minutes; keep the 8pm market-brief SLA.

### 3.4 `Trad core.md` / `Coin core.md`

New entries required in `Trad core.md`:

- BAB: Frazzini-Pedersen 2014 JFE. Mechanism, replication history, current decay evidence (post-2018 underperformance flagged in GWZ 2024; still Grade A on long-sample evidence).
- DealerGamma: SqueezeMetrics / Barbon-Buraschi 2021 WP. Single-paper primary source; flag for replication.
- GP/A: Novy-Marx 2013 JFE. Mechanism, FF5 integration.
- CEI: Daniel-Titman 2006 JoF. Mechanism, construction details.
- C009 Faber TAA: Faber 2007 J. Wealth Mgmt. Mechanism as gate, not alpha-generator. OOS evidence from subsequent papers.

No `Coin core.md` additions — the meta-analysis does NOT recommend any new crypto variables for live deployment (all crypto on-chain variables flagged as post-ETF-regime incomplete).

### 3.5 Excel — `master-data-log.xlsx`

**VariableRegistry sheet additions** (7 new rows):
- V029 BAB, V030 DealerGamma, V031 GP/A, V032 CEI, V033 C009_FaberTAA_SPY, V034 C009_FaberTAA_GSCI, V035 C009_FaberTAA_BTC.
- Columns: variable_id, name, grade, bucket (S/T/R/Overlay), asset_scope, source, pull_frequency, live_date, review_date, mandate_restrictions.
- Pre-fill `review_date = 2026-10-14` for all (match audit-addition cadence).

**SignalLedger sheet new columns** (if schema update required — check `Excel-Sync-Protocol.md` first):
- `overlay_gate_status` — on/off for each signal (inherited from Step 1.5)
- `v027_regime_bucket` — contraction/neutral/expansion — for later regime-conditional attribution
- `bab_sleeve_weight`, `dealergamma_sleeve_weight` — if factor sleeves active that day

**MethodologyNotes sheet:** append dated entry documenting the 2026-04-18 meta integration, with pointer to this plan file.

**PerformanceStats sheet:** no structural change; at next weekly signal-review the marks should stratify by `v027_regime_bucket` to produce the regime-conditional attribution the meta-analysis calls for (Recommendation 7.5.2).

### 3.6 Skills — which edits are needed

| Skill | Change | Why |
|---|---|---|
| `market-brief` | Add BAB / GP/A / CEI / DealerGamma / C009 to the scorecard columns. Extend fail-loud to cover new Grade-A pulls. | New variables need daily surface. |
| `daily-trade-rec` | Extend 8-step template to include Step 1.5 Overlay Gate output. Update pre-entry checklist with V027 regime bucket + C009 sleeve state. | New gate blocks entry when off. |
| `signal-review` | Mark-to-market logic unchanged, but add grouping-by-V027-regime-bucket to the weekly stats. | Meta-analysis Recommendation 7.5.2. |
| `quarterly-methodology-review` | Add explicit 2026-07-01 agenda items: re-score V006/V007/V008 downgrade question; review DealerGamma single-paper status; promote WATCH bucket per 2-consecutive-quarter rule. | Deferred items must not drift. |
| `positions-monitor` | Add C009 sleeve-off check — if a held position is in a sleeve that flipped overlay-off, flag for review (not auto-close — discretionary). | New gate affects existing positions. |
| `trade-update` | No immediate change; existing 4-layer sync still applies. | New variables use same ledger write path. |

### 3.7 Scheduled tasks

No new tasks. Extend existing:
- `preflight-audit-data-1945pm` — add BAB / GP/A / CEI / DealerGamma / Faber-SMA to pull list. Update `.pipeline-health.json` schema to cover the 5 new pulls.
- `quarterly-methodology-review` (1st of Jul/Oct/Jan/Apr at 19:00) — reminder in cron description to re-evaluate deferred downgrades and single-paper DEPLOYs.

---

## 4. Rollout sequencing

### Phase 1 — Documentation (this week, no live impact)

1. Patch `Methodology Prompt.md` with Top-30, Step 1.5 Overlay Gate, scoring rule additions, bucket crosswalk appendix.
2. Patch `Risk Rules.md` with V027 sizing, C009 drawdown gate, R-group scale-consistency, factor sleeve sizing.
3. Patch `Data Sources.md` with new variable source mappings.
4. Patch `Trad core.md` with the 5 new variable mechanism entries.
5. Append dated entry to `MethodologyNotes` sheet documenting the integration.

**Gate to proceed to Phase 2:** documentation patches reviewed by Gerald and approved.

### Phase 2 — Data pipeline (2 weeks, blocking for live scoring)

1. Extend `compute_audit_additions.py` (or new `compute_meta_additions.py`) to pull BAB ETF proxy (USMV/SPLV), GP/A (French library), CEI (self-compute), DealerGamma (SqueezeMetrics subscription — check if already available), Faber-SMA (Yahoo monthly).
2. Wire into `preflight-audit-data-1945pm` task; verify fail-loud triggers.
3. Add VariableRegistry rows V029–V035 with `live_date` field empty.
4. Run 5 consecutive pipeline days in "shadow mode" — compute values but do not score into SignalLedger; surface values in brief only.

**Gate to proceed to Phase 3:** 5 consecutive clean pipeline days with no MISSING for the 5 new Grade-A pulls (DealerGamma allowed to MISSING as Grade B).

### Phase 3 — Live scoring (after Phase 2 green)

1. Update `market-brief` and `daily-trade-rec` skills to include new variables in scorecard and 8-step.
2. Set `live_date` on VariableRegistry rows V029–V035.
3. First live rec under new framework: note the fact in the trade rec header.
4. Weekly signal-review starts stratifying by V027 regime bucket.

### Phase 4 — Ledger re-validation (2026-10-14 audit-addition review)

1. Mark-to-market V026, V027, V028 over 6-month live window (matches original audit cadence).
2. Add 2026-04-18 additions (V029–V035) into the same review template (though with shorter live window; note this).
3. GO / NO-GO decision per variable using the audit rubric.
4. Roll any GO decisions into permanent Grade A; any NO-GO back to WATCH or EXCLUDE.

---

## 5. Risks and open questions

### 5.1 Construct and mechanism risks

- **V027 re-anchor risk.** If the meta-analysis conclusion V027 > V004 reverses in a credit-stress regime we haven't yet observed, V027's downgrade-by-one-notch rule will under-fire and we'll take more risk than intended. **Mitigation:** retain V004 in scoring (just downgraded to B), and if V004 spikes while V027 is neutral, treat that as a second independent signal and override the gate.
- **V014 split deferred.** We're not adopting the V014a/V014b split now because V014 isn't live in Gerald's framework. If meta recommends re-adding V014a at a future lit-review, we need a fresh BNMA run on V014a specifically.
- **DealerGamma is single-paper.** Adopting at Grade B is the right move per fail-loud on single-paper DEPLOYs (meta Recommendation 7.5.4). Flag for second-replication search at 2026-07-01 quarterly.

### 5.2 Construction / implementation risks

- **BAB via ETF proxy (USMV/SPLV) is a compromise.** The canonical BAB uses leveraged long/short β deciles; ETF proxy captures only a fraction. For tactical scoring it's adequate, but any OOS ledger evidence showing BAB leg underperforming its academic spec should trigger a self-compute pipeline migration.
- **GP/A and CEI computation.** Quarterly financial-statement data has reporting lag. Meta-analysis evidence is on equal-weight, quarterly-rebalanced portfolios — we need to replicate that rebalance discipline, not daily rescore.
- **C009 Faber end-of-month.** Sleeve flips happen on last trading day of the month. The Overlay Gate reads the *previous* month's close against its 10m-SMA for the following month. Document this explicitly to avoid same-day execution confusion.

### 5.3 Framework-level risks

- **Nomenclature mismatch causes attribution errors.** If the bucket crosswalk is sloppy, weekly signal-review will mis-attribute meta-R variables (V027) to Gerald-R slot but meta-Overlay variables (C009) to Gerald-R as well. The crosswalk appendix in Methodology Prompt must be treated as load-bearing documentation.
- **Overlay Gate at Step 1.5 vs post-Sum.** I've recommended non-additive-to-Sum gating. Alternative is to make overlay a multiplier on the final score. Non-additive preserves the "|Sum|≥3 with C scored" pre-entry rule, which is wired into the Risk Rules checklist. Changing it would cascade.
- **2026-10-14 audit-addition GO/NO-GO.** V026 comes up for review with this plan's additions. If V026 is marked NO-GO (likely per meta evidence), the "single-stock residual-mom T-input" rule needs a replacement — candidates would be the JKP-tangency of GP/A + CEI + HMLDevil (when added). Do NOT leave the single-stock T-slot empty.

### 5.4 Operational risks

- **Token / context burden.** Adding 7 variables to every market-brief means extra pulls + extra lines in every brief. Audit brief template token count after Phase 3 goes live; if it expands >20%, trim Grade-B lines that aren't actively scored.
- **DealerGamma subscription cost.** If SqueezeMetrics isn't already subscribed, flag to Gerald before Phase 2.

---

## 6. Explicit "what I did NOT adopt" list (transparency)

Items the meta-analysis recommends that this plan does **not** adopt now:

1. **Downgrade V006/V007/V008 to B.** Evidence is borderline (1 BNMA run each). Defer to 2026-07-01 quarterly. Reason: downgrading a regime input without replication risks over-correction in tight-cycle transitions.
2. **HMLDevil, PCTECH, CieslakPovala, OppInsider, LazyPrices, QMJ, VRP, CorrelationRiskPremium, HedgingPressure, LM_Text, GoldTIPSbeta, GoogleSVI, CrossAssetValue, ADS_Nowcast, C005, C002, C011 as live variables.** All deferred to 2026-07-01 quarterly for replication / construction work. Reason: single-paper or WATCH evidence, not ready for live.
3. **V014 split / V014a re-adoption.** Deferred — V014 not currently live.
4. **Combined cross-asset BNMA pool** (meta Recommendation 7.5.1). This is a research/methodology task, not a live-framework task. Queue for Q3 methodology work.
5. **Joint-portfolio synthesis layer** (meta Recommendation 7.5.3). Requires covariance estimation infrastructure we don't have. Longer-horizon project.

---

## 7. Summary of most important decisions

1. **Adopt the 75/20/5 allocation spine** — V009/V027/V028 primary, BAB/DealerGamma/V011/GP/A/CEI satellite, C009 Faber overlay.
2. **Add Step 1.5 Overlay Regime Gate** to the 8-step — this is the single biggest structural change. Non-additive to Sum.
3. **Keep bucket codes (S/T/C/R) unchanged** — add a crosswalk to meta-analysis nomenclature instead of renaming. Protects OOS ledger continuity.
4. **Downgrade V001 and V004 to B now; defer V006/V007/V008 to Q2 methodology review.** Prevents over-correction.
5. **V027 becomes the primary sizer**, not just a Risk Overlay input. This is the mechanical embedding of the meta-analysis's highest-conviction architectural claim.
6. **Phased rollout, 5-day shadow mode before live scoring.** New variables enter the ledger only after the pipeline runs clean.
7. **Keep V026 mandate-restricted and flag for 2026-10-14 review** — likely demotion candidate, but honor the original 6-month audit contract.

---

*Plan written 2026-04-18 by Claude. No authoritative documents have been edited. Next user decision: approve Phase 1 documentation patches OR request scope adjustments before any edits begin.*
