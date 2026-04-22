# Methodology Audit — Post-Integration Patch

**Run date:** 2026-04-22 (UTC+8)
**Trigger:** Post-integration audit of the 2026-04-18 meta-analysis rollout. Seven gaps surfaced between the systematic-review evidence base (`bnma/meta-analysis/meta_results.json`, `pl_nma_results.json`, `BNMA-meta-analysis-2026-04-18.md`) and the Methodology Prompt as it stood after the 2026-04-18 Phase-1 documentation pass.
**Scope:** Methodology Prompt only (7 targeted edits). Downstream propagation to Trad core.md §30, scripts/compute_meta_additions.py, master-data-log.xlsx (VariableRegistry row 31, new row 37 V036, MethodologyNotes row 4). Architecture v6 left untouched per governance.
**Commit:** `f0d0f4e`
**Next review:** 2026-10-14 (shared cohort with V026–V035).

---

## 1. Why this patch was necessary

The 2026-04-18 meta-integration promoted 5 variables (V029 BAB, V030 DealerGamma, V031 GP/A, V032 CEI, V033–V035 Faber TAA) and downgraded 5 (V001 VIX, V004 HY OAS, V006 2s10s, V007 Real yields, V008 ACM term premium). A post-rollout read of the underlying evidence files found:

- **1 robust top-10 candidate** (PCTECH) from the PL-NMA never made it into the methodology.
- **1 wrong primary citation** (V030 DealerGamma cited Barbon-Buraschi 2021 "Gamma Fragility" — a paper that is not in the systematic-review corpus at all).
- **1 unresolved construct split** (V014 BTC netflows, 1.12 posterior-median drift range in BNMA) acknowledged but not operationalised.
- **1 high-coverage variable held in silent limbo** (VRP — 6 reviews, DEPLOY_CONDITIONAL, no operational instruction).
- **1 unacknowledged PL-NMA vs BNMA contradiction** (V016 BTC funding — +0.96 PL-NMA θ vs BNMA EXCLUDE).
- **1 well-supported value-factor gap candidate** (HMLDevil) not tracked anywhere.
- **7 DEPLOY_CONDITIONAL / WATCH variables** with no re-evaluation mechanism — they would silently age out of the review cycle.

Without this patch, the 2026-10-14 six-month review would have no explicit mandate to revisit any of these.

---

## 2. Per-change rationale

### Change 1 — V036 PCTECH added (T-group, index sleeve, Grade B)

**Evidence basis.**
- `meta_results.json` → `PCTECH`: recommendation `DEPLOY_CONDITIONAL`; post_mean 0.484; prob_positive 1.0; sharpe_mean 0.55; 1 review (cl2, "OOS R² 1.32% monthly; survives GWZ 2024 qualitatively").
- `pl_nma_results.json` → PCTECH rank 9/54 primary, rank 6/54 S2. Appears in the "Robust top-10" table — deploy-tier in BOTH fits. *The only robust-top-10 new candidate not integrated on 2026-04-18.*
- Primary citation: Neely, Rapach, Tu, Zhou (2014) Management Science 60(7) 1772–1791.

**Why promoted now, not at 2026-10-14.**
Robust top-10 status in both PL-NMA fits means the evidence bar is already cleared. Holding it another six months would waste the signal on the index sleeve for no defensible reason. Grade B (not A) because only 1 formal review in the corpus — second independent replication is the A-gate.

**Why T-group, not S-group.**
PC composite of 14 *technical* indicators (MA crossovers, momentum, volume) — signal family is tactical, not structural. Horizon monthly, which matches the T-group cadence.

**Why index-sleeve only, not single-stock.**
On single stocks, V026 (residual momentum) is the established T-leg and V036 is a crude index-level PC; using both on the same stock would double-count a beta-loaded technical read. Scoring rule #5 codifies: on the index sleeve, V009 TSMOM and V036 PCTECH are *averaged* into a single T-leg (not summed).

**Alternative considered.** Hold at WATCH until 2026-10-14. Rejected because PL-NMA robust-top-10 is a harder bar than BNMA DEPLOY_CONDITIONAL alone, and we are already deploying V030 DealerGamma at Grade B on weaker evidence (1 paper, rank 5).

---

### Change 2 — V030 DealerGamma citation corrected

**Evidence basis.**
- `meta_results.json` → `DealerGamma.citation` = `"Baltussen-Da-Lammers-Martens 2021 JFE"`.
- The current Methodology Prompt (pre-patch) cited Barbon-Buraschi (2021) "Gamma Fragility" Working Paper. This paper does not appear in any of the 12 source papers listed in `pl_nma_results.json`. It was never in the systematic-review corpus.

**Why this matters.**
A Grade B variable with a flagged single-paper dependency is only defensible if the single paper is the correct one. The operational mechanism (dealer hedging flows amplify/damp intraday moves) is in the Baltussen et al. 2021 JFE paper, with Zhu et al. (2024) providing the SPY extension (net Sharpe 1.33) that grounds the grade-B headline. Barbon-Buraschi is a different mechanism (fragility via gamma concentration) and should not be cited as the operational anchor.

**What also changed.** The "What it is" paragraph was rewritten to match the corrected source: dealers net-short gamma delta-hedge pro-cyclically (buy rallies, sell declines), net-long damps. This is the Baltussen mechanism, not the Barbon fragility mechanism.

**Why architecture-v6 was NOT updated.**
Architecture files are immutable per governance. Architecture v6 §7 still reads "Barbon-Buraschi 2021 only". The correction is documented (a) inline in the Methodology Prompt V030 entry, (b) in Trad core.md §30 with an explicit "corrected 2026-04-22" annotation, (c) in VariableRegistry row 31 Review_History column, (d) in MethodologyNotes row 4. Next architecture version should carry the corrected citation.

---

### Change 3 — V014 construct-split note

**Evidence basis.**
- `BNMA-meta-analysis-2026-04-18.md` Stage 1 T-group row: V014 drift_range = **1.12** (P1: 1.15, P4: 0.03) — the largest instability of any T-group variable.
- `meta_results.json.prior_bnma.V014`: action `SPLIT`, note "1.12 posterior drift; split order-flow vs vol-sort".
- BNMA-2026-04-18 Stage 6 Registry actions calls explicitly for the split.

**Why the split wasn't operationalised on 2026-04-18.**
The integration plan flagged the split requirement but deferred implementation pending "next BNMA re-run with explicit construct separation". Without an operational rule in the interim, every daily trade rec faced ambiguous V014 semantics.

**Interim resolution adopted.**
- **Order-flow sub-construct** (Anastasopoulos et al. directional flow): tradable as T-input, **only when** exchange-level data distinguishes large-lot directional buying from vol-regime sorting. Labelled `V014-OF`.
- **Vol-sort sub-construct** (Lee-Wang cluster, negative BNMA posterior): EXCLUDE until separately re-tested.
- If the data source cannot distinguish the two, V014 is **MISSING** (fail-loud) and the BTC T-leg is left blank. Not pooled.

**Why this rule is conservative.**
Pooling a mechanically heterogeneous variable with a 1.12 drift range creates a coin-flip signal that looks tradable on paper. The fail-loud default ensures the pooled construct never scores.

---

### Change 4 — V020 VRP operational note (monitoring-only)

**Evidence basis.**
- `meta_results.json` → `VRP`: recommendation `DEPLOY_CONDITIONAL`; n_reviews 6 (**highest of any new candidate**); consensus 0.83; prob_positive 1.0; post_mean 0.364.
- One dissenting review (cg5, Grade C): "SEVERE decay per Goyal-Welch-Zafirov 2024".
- PL-NMA rank 17/54, θ=+0.47.
- V020 already sits in the Top-33 at position 20 with no operational definition.

**Why not promoted despite highest review count.**
The GWZ 2024 paper is the 2024 replication audit of the forecasting-risk-premia literature. For a *risk-management* framework, a post-2020 OOS decay finding overrules pre-2020 sample evidence regardless of how many reviewers liked the original paper. Deploying VRP operationally would require demonstrating the decay claim is reversed or bounded.

**What the note does.**
Marks V020 as Grade B monitoring-only with an explicit 2026-10-14 re-evaluation gate: if GWZ 2024 decay is unreversed, demote to Grade C at that review. This prevents silent resurrection of VRP in a future trade rec without evidence.

---

### Change 5 — V016 PL-NMA vs BNMA contradiction documented

**Evidence basis.**
- PL-NMA: V016 rank 11/54, θ=+0.96 — positive signal.
- BNMA 4-run: EXCLUDE (p_positive ≈ 0.50, PRIOR_SENS+4 flag in P4).
- These two outputs contradict each other on the same variable.

**Why the contradiction exists (diagnosis).**
- PL-NMA draws on systematic-review papers that include pre-2021 BTC futures data, when funding rate carried directional signal.
- BNMA 4-run uses post-2021 data, where funding lost directional content (consistent with the founding study's own admission of "no correlation with directional strategies").
- The discrepancy is a sample-period artefact, not a methodological disagreement.

**Resolution rule adopted.**
BNMA EXCLUDE stands. V016 remains a filter/crowding signal only, never an entry trigger. Flag the contradiction at 2026-10-14 with 12+ months of post-spot-ETF data to resolve definitively.

**Why this needed to be written down.**
A future reviewer reading the PL-NMA rank table alone could reasonably conclude V016 is a tradable long/short signal at rank 11. Without an explicit reconciliation, the methodology would silently drift toward that reading.

---

### Change 6 — HMLDevil WATCH registration

**Evidence basis.**
- `meta_results.json` → `HMLDevil`: recommendation `DEPLOY_CONDITIONAL`; post_mean 0.447; prob_positive 1.0; sharpe_mean 0.5; 2 reviews both EFFECTIVE.
- PL-NMA rank 23/54, θ=+0.16.
- `meta_results.json.gap_synthesis.Value (Stocks)`: `best: HMLDevil; grade: B; filled: true`.

**Why not promoted to V037 now.**
- Only 2-paper support (3+ is the conservative bar for a new single-stock factor sleeve given McLean-Pontiff decay risk).
- Value factor has been severely decayed 2017–2022; need confirmation that post-2022 value recovery is persistent, not mean-reversion fluke.
- Current equity sleeve covers profitability (V031 GP/A), issuance (V032 CEI), and low-beta (V029 BAB) — there is no explicit value factor, so the gap is real, but the bar to fill it is the same bar we held V030 to (and arguably higher because value decay has harder evidence than gamma decay).

**WATCH mandate.**
Include HMLDevil OOS Sharpe in the 2026-10-14 review inputs. If 3+ paper support and post-2022 OOS persistence are both confirmed, promote to V037 at Grade B with the same independent-factor-sleeve rule as V029 BAB (1/3 of V009 budget).

---

### Change 7 — Systematic Review WATCH List section created

**Evidence basis.** Seven variables from `meta_results.json` are at DEPLOY_CONDITIONAL or WATCH status with no tracking mechanism in the Methodology Prompt:

| Variable | SR verdict | PL-NMA rank | Promotion gate |
|---|---|---|---|
| HMLDevil | DEPLOY_CONDITIONAL | 23/54 | 3+ papers; post-2022 value-recovery OOS |
| QMJ | WATCH | 22/54 | Incremental Sharpe over GP/A standalone |
| OppInsider | DEPLOY_CONDITIONAL | 20/54 | Second independent replication |
| LazyPrices | DEPLOY_CONDITIONAL | 14/54 | Second replication + EDGAR NLP pipeline |
| ADS_Nowcast | DEPLOY_CONDITIONAL | 24/54 | Consistent OOS directional evidence |
| LM_Text | WATCH | 41/54 | Tradable long-short implementation |
| CieslakPovala | DEPLOY_CONDITIONAL | 16/54 | Second replication; distinguish from V008 |

**Why a registry, not individual promotion decisions.**
Each variable is individually too thin for promotion today, but collectively they represent seven coverage gaps (value, quality, insider, NLP, macro nowcast, text sentiment, bond risk premium). Without a registry, the 2026-10-14 review has no obligation to revisit any of them; with one, the review has an explicit per-variable gate question.

**Hard rule attached.** No entry persists indefinitely. At each review, the reviewer answers (a) has the gate been met? (b) is projected post-decay Sharpe > 0.30? If both YES → promote. Else → record the reason and extend review date by 6 months or reject outright.

---

## 3. What was deliberately NOT done

| Consideration | Decision |
|---|---|
| Update architecture-v6 §7/§10 to reflect V036 + corrected V030 citation | **No.** Architecture files immutable per governance. Gap documented inline in Methodology Prompt; carry to next architecture version. |
| Retroactively edit 2026-04-XX daily files that reference Barbon-Buraschi | **No.** Paper trail preserved. Correction is forward-looking from 2026-04-22. |
| Promote PCTECH to Grade A | **No.** Only 1 formal review in corpus; Grade A requires second independent replication. |
| Promote HMLDevil to V037 now | **No.** 2-paper support is below the defensible bar for a new single-stock factor sleeve. |
| Operationalise VRP despite highest review count | **No.** GWZ 2024 decay claim overrules pre-2020 sample evidence for a risk-management framework. |
| Resolve V016 PL-NMA/BNMA contradiction with an override | **No.** Need 12+ months post-spot-ETF data. BNMA EXCLUDE stands as interim default. |
| Re-split V014 construct in the BNMA run itself | **No.** Requires BNMA re-run with construct separation in the data layer; deferred. Interim rule is fail-loud MISSING when the data source can't distinguish. |

---

## 4. Paper trail — where each rationale is now permanently recorded

| Artefact | What it holds | Durability |
|---|---|---|
| `Trade/reviews/methodology-audit-post-integration-patch-2026-04-22.md` (this file) | Full per-change rationale, alternatives considered, decisions rejected | Git-versioned; permanent |
| `Trade/framework/Methodology Prompt.md` | Inline rationale with 2026-04-22 date stamps on each change | Git-versioned; authoritative |
| `Trade/framework/Trad core.md` §30 | V030 citation corrected + inline correction note | Git-versioned |
| `Trade/scripts/compute_meta_additions.py:218` | Corrected grade string (flows into trade-rec reports) | Git-versioned |
| `Trade/master-data-log.xlsx` VariableRegistry row 31 Review_History | V030 citation-correction entry appended to history column | Excel-versioned + backup |
| `Trade/master-data-log.xlsx` VariableRegistry row 37 | V036 PCTECH row with full Evidence_Strength, Source_Paper, Notes, Review_History | Excel-versioned + backup |
| `Trade/master-data-log.xlsx` MethodologyNotes row 4 | One-row summary of all 7 changes, affected sheets, approval status | Excel-versioned + backup |
| `Trade/master-data-log.xlsx.bak-2026-04-22` | Pre-mutation Excel snapshot | Git-versioned (one-step revert) |
| Git commit `f0d0f4e` | All of the above in one atomic commit | Reversible via `git revert f0d0f4e` |

---

## 5. 2026-10-14 review inputs (handoff)

The next methodology audit must answer, for each of the following:

- **V036 PCTECH** — has Phase-2 data pipeline shipped? Is OOS Sharpe consistent with the 0.30–0.45 post-decay projection?
- **V030 DealerGamma** — has second independent replication surfaced? If not, hold at Grade B.
- **V014 BTC netflows** — has the BNMA re-run with construct separation happened? If yes, operationalise V014-OF at Grade B and exclude vol-sort.
- **V020 VRP** — has the GWZ 2024 decay claim been reversed or bounded post-2020? If not, demote to Grade C.
- **V016 BTC funding** — do 12+ months of post-spot-ETF data resolve the PL-NMA/BNMA contradiction?
- **HMLDevil** — 3+ paper support and post-2022 value recovery OOS confirmed? If yes, promote to V037.
- **WATCH List (7 variables)** — per-variable gate evaluation per §7 above.

Any variable that fails its gate without a decision (promote / extend / reject) is a process failure of the review itself.
