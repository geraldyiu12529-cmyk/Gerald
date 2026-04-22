# T.system Architecture — v7
**Version:** 7  
**Dated:** 2026-04-22  
**Prior version:** `architecture-v6-2026-04-22.md`  
**Supersedes:** v6 (for consumer reads)

**Changes from v6:**
- **§9 Changelog:** prepended row for 2026-04-22 post-integration patch (V036 PCTECH registration + V030 citation correction + Systematic Review WATCH List + new scoring rule #5).
- **§10 Current Variable Registry:** new "Post-integration patch 2026-04-22" sub-table with V036 PCTECH row; V030 DealerGamma row Notes field updated — anchor paper corrected from Barbon-Buraschi 2021 "Gamma Fragility" (never in systematic-review corpus) to Baltussen-Da-Lammers-Martens 2021 JFE 142(1) 377–403 + Zhu et al. 2024; header count updated "Top-33" → "Top-34".
- **§11 Grade Distribution & Review Cohorts:** distribution header "33 variables" → "34 variables"; Grade B count 10→11 (V036 added); review cohort 2026-10-14 extended from 8 variables to 9 (V036 added); new §11.5 Systematic Review WATCH List (7 candidates: HMLDevil, QMJ, OppInsider, LazyPrices, ADS_Nowcast, LM_Text, CieslakPovala); new scoring-rule row "V009 × V036" in §11 Active double-count gates.
- **§2 Key Documents:** Methodology Prompt row — authority line "Top-33 variables" → "Top-34 variables"; new row for `reviews/methodology-audit-post-integration-patch-2026-04-22.md` (per-change rationale memo, evidence for V036 + V030 correction + WATCH list).
- **§7 Known Structural Risks:** V030 row rewritten — anchor paper corrected; severity unchanged (MED); note tightens to "single-paper Baltussen-Da-Lammers-Martens 2021 (+ Zhu 2024 extension); high re-estimation risk".

---

## ⚠️ GOVERNANCE — THIS IS THE HEART OF THE OPERATION

1. **This file is IMMUTABLE.** Never edit in place. Never patch. Never append to §Changelog of a sealed version. Once dated and committed, a version is frozen.
2. **All changes ship as a new version file** in `Trade/framework/architecture/` named `architecture-v{N}-{YYYY-MM-DD}.md`. Increment N monotonically.
3. **Every new version MUST include at the top:**
   - `**Prior version:**` → filename of the immediately previous version
   - `**Changes from v{N-1}:**` → bulleted diff listing every addition, modification, removal with section reference
4. **Source of truth for wiring** remains each skill's `~/.claude/skills/{skill}/SKILL.md`. When SKILL.md and this file conflict, SKILL.md wins — and a new architecture version must be cut to reconcile.
5. **Do not delete prior versions.** The folder is append-only history.
6. **Consumers read the latest version** — resolve via `ls Trade/framework/architecture/ | sort` and take the highest `v{N}`.

---

**Maintained by:** `architecture-health` skill — cuts a new version when skill wiring, file paths, task scheduling, or the variable registry / scoring rules change.  
**Source of truth for wiring:** each skill's `~/.claude/skills/{skill}/SKILL.md`.  
**Source of truth for variables and scoring rules:** `Trade/framework/Methodology Prompt.md`.

---

## Note on §1–§8

Sections 1–8 (Execution Order, Key Documents, Scripts, File Location Map, Skill Upstream/Downstream Detail, Full Dependency Graph, Known Structural Risks, Auto-Memory & Workspace State) are unchanged from v6 except for the two items noted above (§2 Methodology Prompt row authority update + new row for post-integration-patch memo; §7 V030 risk row citation correction). Consumers needing the full text of §1, §3, §4, §5, §6, §8 should read those sections in `architecture-v6-2026-04-22.md` — they are preserved verbatim. Only the sections that materially changed in v7 are reproduced below (§2 delta, §7 delta, and the full rewrites of §9, §10, §11).

---

## 2. Key Documents (deltas from v6)

The full §2 table in v6 is unchanged except for the following two rows:

| Document | Path | Authority over | Loaded by |
|---|---|---|---|
| Methodology Prompt | `framework/Methodology Prompt.md` | 8-step framework, **Top-34 variables** (A/B/C grades), S/T/C/R scoring rules (incl. rule #5 V009×V036 average on index tickers), Overlay Gate | market-brief, daily-trade-rec, signal-review, quarterly-review, architecture-health |
| **Post-Integration Patch Memo (NEW in v7)** | `reviews/methodology-audit-post-integration-patch-2026-04-22.md` | Per-change rationale for V036 PCTECH registration, V030 citation correction, WATCH-list introduction, new scoring rule #5 | architecture-health, quarterly-methodology-review, methodology-audit-6mo-review-2026-10-14, literature-review |

---

## 7. Known Structural Risks (delta from v6)

The full §7 table in v6 is unchanged except for the V030 row, which is replaced by:

| Risk | Severity | Affected skills | Mitigation status |
|---|---|---|---|
| **V030 DealerGamma single-paper dependency** — Baltussen-Da-Lammers-Martens 2021 JFE (+ Zhu et al. 2024 SPY extension); Grade B; high re-estimation risk. *Citation corrected 2026-04-22 from prior-draft error citing Barbon-Buraschi 2021 "Gamma Fragility" (not in systematic-review corpus).* | MED | market-brief, daily-trade-rec | Monitor for decay; flag at next quarterly-review; re-evaluate at 2026-10-14 audit |

---

## 9. Changelog

| Date | Change | Triggered by |
|---|---|---|
| **2026-04-22** | **V036 PCTECH registered (Shadow, pipeline pending); V030 DealerGamma citation corrected Barbon-Buraschi 2021 → Baltussen-Da-Lammers-Martens 2021 JFE + Zhu 2024; Systematic Review WATCH List introduced (7 candidates); new scoring rule #5 (V009×V036 average on SPY/QQQ); §10 Top-33 → Top-34; §11 cohort 8→9; §2 row for rationale memo; §7 V030 risk row rewritten.** | **Post-integration audit patch (evidence: `bnma/meta-analysis/meta_results.json`, `pl_nma_results.json`, `BNMA-meta-analysis-2026-04-18.md`); per-change memo: `reviews/methodology-audit-post-integration-patch-2026-04-22.md`** |
| 2026-04-22 | Skill renamed methodology-sync → architecture-health; all wiring references updated | Skill rename — architecture health dashboard introduced |
| 2026-04-22 | HypoLedger sheet added to master-data-log.xlsx (11th sheet); §2 Master Data Log count 10→11; §5 daily-trade-rec adds HypoLedger append row (Step 8.5); §5 signal-review adds HypoLedger read + mark-to-market + dim-14 efficacy rows; §6 Excel node label updated | HypoLedger backfill H001–H010 (2026-04-15→2026-04-21 recs); system efficacy tracking now live |
| 2026-04-22 | Skills path updated `Trade/.claude/skills/` → `~/.claude/skills/` throughout (§2, §4, §5, §6, governance rule §4); §2 removed deleted-file rows (Trade/.claude/rules/, Trade/.claude/CLAUDE.md); §8 workspace state updated to reflect 2026-04-22 cleanup | 2026-04-22 cleanup: Trade/.claude/ deleted, skills consolidated to ~/.claude/skills/, cowork/ deleted |
| 2026-04-21 | Added `gen_trade_rec_html.py` to §3 Scripts; updated `report-{date}-trade-rec.html` Notes in §4 to reference script and format lock | HTML report format canonicalized 2026-04-21; analyst sections added (freshness strip, V026 full table, factor exposure, signal age, regime sensitivity, closed-trade context); script is required Step 10 of daily-trade-rec |
| 2026-04-21 | Added §10 Current Variable Registry; added §11 Grade Distribution Summary | Variable registry completeness |
| 2026-04-21 | Added §5 entries for `asset-universe-update` and `pipeline-smoketest`; added §2 entries for `.claude/rules/` and CLAUDE.md files; added §8 auto-memory + workspace canonicalization | Architecture completeness audit |
| 2026-04-21 | File created — supersedes `pipeline-dependency-graph.mermaid` and `routine-output-map.md` | Manual (architecture review session) |
| 2026-04-21 | Added V029–V035, Overlay Gate, meta-additions-staging to all skill wiring | HIGH-3 meta-integration commit |
| 2026-04-21 | Added cloud agents (cloud-market-brief-6pm, cloud-news-events-630pm, cloud-trade-rec-7pm) | Existing tasks, first documented here |
| 2026-04-19 | Date-folder convention adopted (`Trade/{YYYY-MM-DD}/`) | Workspace canonicalization |
| 2026-04-18 | V026/V027/V028 audit-additions added to wiring; grade downgrades V001/V004/V006/V007/V008 A→B | Audit-addition integration |
| 2026-04-15 | master-data-log.xlsx 10-sheet structure established | Excel data layer creation |

*Append a row here whenever this file is patched — then cut v{N+1}, never edit in place.*

---

## 10. Current Variable Registry

**Authority:** `Trade/framework/Methodology Prompt.md` §4 Top-34 Variables. This table is a snapshot as of 2026-04-22; the Methodology Prompt is canonical if they diverge.

**Grade legend:** A = replicated, coherent mechanism, long history. B = regime-dependent or thinner coverage. C = weak/narrative (not used in scorecards). A→B = audit-downgraded 2026-04-18 (BNMA).

### Core Top-25 (pre-audit)
| ID | Variable | Grade | Scoring leg | Bucket | Notes |
|---|---|---|---|---|---|
| V001 | VIX | ~~A~~ **B** | R-overlay | Cross-asset | Downgraded 2026-04-18 — regime-sensitive |
| V002 | MOVE (rates vol) | A | R-overlay | Cross-asset | |
| V003 | 12m TSMOM | A | T (trend) | All assets | Raw TSMOM for indices/ETFs/commodities/crypto |
| V004 | HY OAS / credit spreads | ~~A~~ **B** | R-overlay | Cross-asset | Downgraded — 0.65–0.75 corr with V027 post-2008; double-count gate with V027 |
| V005 | Policy-path surprise sensitivity | A | C (catalyst) | Cross-asset | |
| V006 | 2s10s yield curve | ~~A~~ **B** | S (structural) | Bonds | Downgraded — lead-lag unstable post-QE |
| V007 | Real yields | ~~A~~ **B** | S | Bonds | Downgraded — inflation-regime dependent |
| V008 | ACM term premium | ~~A~~ **B** | S | Bonds | Downgraded — single-model dependency |
| V009 | Carry / roll yield | A | T | All assets | Spine factor — V026/V029/V030 sleeves sized vs. V009 budget; V036 averages with V009 on SPY/QQQ |
| V010 | Equity valuation spread | A | S | Equities | |
| V011 | Commodity front-back curve | A | S | Commodities | See V028 basis-momentum supplement |
| V012 | Earnings revision breadth | A | S | Equities | |
| V013 | Commodity inventories | A | S | Commodities | |
| V014 | Inflation breakevens | A | S | Bonds | |
| V015 | FX interest-rate differential | A | *(context only)* | FX | Not scored — regime identification |
| V016 | FX real valuation / PPP | B short / A long | *(context only)* | FX | Not scored — regime reference |
| V017 | CFTC speculative positioning | B | S | Cross-asset | |
| V018 | Dealer/customer order flow | B public / A proprietary | T | Cross-asset | |
| V019 | Options-implied skew | B | R | Equities | |
| V020 | Variance risk premium | B | R | Equities | |
| V021 | News-based sentiment | B | C | Cross-asset | |
| V022 | Cross-asset correlation regime | A (as filter) | Filter | Cross-asset | |
| V023 | Net supply / duration issuance | A (rates) | S | Bonds | |
| V024 | Buyback / net payout | B | S | Equities | |
| V025 | Insider net buying | B | S | Equities | |

### Audit additions 2026-04-14 (review due 2026-10-14)
| ID | Variable | Grade | Scoring leg | Bucket | Notes |
|---|---|---|---|---|---|
| V026 | Residual momentum (12m FF5-residualized) | A | T (single-stock) | Equities | DEPLOY_CONDITIONAL — peer-dominated by V009 (PL-NMA rank 53/54). Score only; zero independent sizing vs V009. **V009+V026 same ticker → score V026 only, no sum.** |
| V027 | Intermediary capital ratio (NY Fed PD z-score) | A | R-overlay | Cross-asset | Leading indicator for V004. **Double-count gate with V004 — take more-negative, not sum.** |
| V028 | Basis-momentum (4w/12w curve slope Δ) | A | S | Commodities | Supplements V011. P(V028>V011)=0.887. Divergence-cap: if static slope backwardation but basis-momentum flattening, cap S at 0. |

### Meta-analysis additions 2026-04-18 (review due 2026-10-14)
| ID | Variable | Grade | Scoring leg | Bucket | Notes |
|---|---|---|---|---|---|
| V029 | BAB — Betting-Against-Beta | A | S (sleeve) | Equities + ETF | Independent factor sleeve, capped at 1/3 V009 budget. ETF proxy USMV/SPLV. |
| V030 | DealerGamma (options dealer gamma) | **B** | R-overlay | Equities + Index | WATCH — single-paper. **Anchor paper: Baltussen-Da-Lammers-Martens 2021 JFE 142(1) 377–403 + Zhu et al. 2024 SPY extension (net Sharpe 1.33). Citation corrected 2026-04-22** — earlier drafts incorrectly cited Barbon-Buraschi 2021 "Gamma Fragility" which was never in the systematic-review corpus. Flag single-paper status in every trade rec. **Double-count gate with V001 VIX.** Source: SqueezeMetrics GEX → SpotGamma → MISSING. |
| V031 | GP/A — Gross Profitability / Assets | A | S | Equities | Quarterly rebalance; FF5 component. |
| V032 | CEI — Composite Equity Issuance | A | S (negative sign) | Equities | Self-compute CRSP + Compustat quarterly. |
| V033 | Faber TAA — SPY sleeve | A | **Step 1.5 Overlay Gate** | Equities | Non-additive to Sum — drawdown circuit-breaker. Monthly SPY vs. 10m-SMA. |
| V034 | Faber TAA — GSCI sleeve | A | **Step 1.5 Overlay Gate** | Commodities | Non-additive to Sum. Monthly GSCI vs. 10m-SMA. |
| V035 | Faber TAA — BTC sleeve | A | **Step 1.5 Overlay Gate** | Crypto | Non-additive to Sum. Monthly BTC vs. 10m-SMA. |

### Post-integration patch 2026-04-22 (review due 2026-10-14)
| ID | Variable | Grade | Scoring leg | Bucket | Notes |
|---|---|---|---|---|---|
| V036 | **PCTECH** — Neely-Rapach-Tu-Zhou PC-TECH composite | **B** | T (index sleeve) | SPY/QQQ only (NOT single stocks) | **Status: Shadow (registered 2026-04-22, data pipeline pending).** Source: Neely-Rapach-Tu-Zhou 2014 Management Science 60(7) 1772–1791. Composite of 14 technical signals (moving-average, momentum, on-balance-volume). Published Sharpe 0.55; projected operational Sharpe 0.30–0.45. **Double-count gate with V009 TSMOM: same index ticker → take average, do not sum** (Methodology Prompt scoring rule #5). VariableRegistry row 37. |

---

## 11. Grade Distribution & Review Cohorts

### Distribution (34 variables; V015/V016 context-only)
| Grade | Count | Variables |
|---|---|---|
| A | 22 | V002, V003, V005, V009, V010, V011, V012, V013, V014, V018(proprietary), V022, V023, V026, V027, V028, V029, V031, V032, V033, V034, V035 + V015(long-horizon) |
| B | 11 | V001↓, V004↓, V006↓, V007↓, V008↓, V017, V019, V020, V021, V024, V025, V030, **V036** |
| Context-only (not scored) | 2 | V015, V016 |

*↓ = audit-downgraded 2026-04-18 (BNMA). V036 = newly registered 2026-04-22 (Shadow pipeline pending).*

### Review cohorts
- **2026-10-14 six-month review** (9 variables registered + 7 WATCH candidates): V026, V027, V028, V029, V030, V031, V032, V033/V034/V035 (Faber TAA), **V036 PCTECH** — plus WATCH-list candidates: HMLDevil, QMJ, OppInsider, LazyPrices, ADS_Nowcast, LM_Text, CieslakPovala.
- **2026-04-18 BNMA downgrades** (permanent until next audit reverses): V001, V004, V006, V007, V008

### Active double-count gates
| Gate | Rule |
|---|---|
| V009 × V026 | Same ticker → score V026 only, zero sizing vs V009 |
| V004 × V027 | Simultaneous stress → more-negative, not sum. V027 leads V004 by design |
| V001 × V030 | Simultaneous stress → more-negative, not sum |
| V011 × V028 | Basis-momentum supplements slope; divergence caps S at 0 |
| V029, V030 sleeves × V009 spine | Each capped at 1/3 V009 risk budget; independent of spine sizing |
| **V009 × V036** | **Same index ticker (SPY/QQQ) → take average, do not sum** (Methodology Prompt scoring rule #5; rule effective only when V036 pipeline ships) |

### Step 1.5 Overlay Gate (V033–V035)
Non-additive to Sum but binding on execution. Sleeve OFF → post-Sum position × 0 regardless of signal. Logged as `Taken=NO, Block_Reason=OverlayGateOff`. Read from previous month-end close only; no intraday recompute.

### §11.5 Systematic Review WATCH List — 2026-04-22

Seven candidate variables flagged by the 2026-04-22 post-integration audit as evidence-sufficient for observation but not yet registered. Not scored; not consumed by any skill. Tracked here so the 2026-10-14 methodology audit can review whether any should promote to registered variables.

| Candidate | Proposed leg | Evidence basis (from `meta_results.json` / `pl_nma_results.json`) | Status |
|---|---|---|---|
| HMLDevil | S (sleeve) | PL-NMA θ meaningfully positive; low correlation with V029 BAB | WATCH — review 2026-10-14 |
| QMJ (Quality Minus Junk) | S (sleeve) | Published Sharpe; overlaps with V031 GP/A — evaluate independence | WATCH — review 2026-10-14 |
| OppInsider (opportunistic insider buys) | S | Extension of V025 insider net-buying; subset may add orthogonal info | WATCH — review 2026-10-14 |
| LazyPrices (10-K textual change) | C (catalyst) | Event-driven corporate-filing signal | WATCH — review 2026-10-14 |
| ADS_Nowcast (Aruoba-Diebold-Scotti) | *context/regime* | Real-time macro nowcast; potentially regime-identification only | WATCH — review 2026-10-14 |
| LM_Text (Loughran-McDonald 10-K sentiment) | C | Textual sentiment across filings | WATCH — review 2026-10-14 |
| CieslakPovala (short-rate expectations cycle) | S | Bonds — complements V023 net supply | WATCH — review 2026-10-14 |

**Promotion gate:** at 2026-10-14 audit, each candidate reviewed against Variable Discovery Protocol criteria (independent signal, replicable source, acceptable implementation cost). PROMOTE → allocate V037+ ID and integrate; KEEP-ON-WATCH → extend observation to 2027-04-14; DROP → remove from WATCH.

---

## End of v7
