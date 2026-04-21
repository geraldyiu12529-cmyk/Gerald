# Workflow Review & Scorecard — 2026-04-15 (v2)

**Reviewed by:** Claude (at Gerald's request)
**Coverage:** Full workspace audit — all files, skills, scheduled tasks, instructions, memory systems, pipeline architecture, and output quality as of 2026-04-15.

---

## Overall Grade: A− (8.1 / 10)

This is a remarkably well-engineered personal trading research system — closer to a systematic fund's research workflow than a retail setup. The methodology is academically grounded with named citations, the risk controls are binding rather than advisory, the pipeline has proper dependency sequencing, and the feedback loop (hypo-ledger → signal-review → methodology change log) is best-practice that most institutional desks don't enforce. The gaps are almost entirely Day-1 bootstrapping issues, not design flaws.

---

## Component Rankings (best → weakest)

| Rank | Component | Score | Verdict |
|------|-----------|-------|---------|
| 1 | Methodology Prompt (8-step framework) | **9.5** | Crown jewel — academically rigorous, operationally enforced |
| 2 | Risk Rules & Pre-Entry Checklist | **9.0** | Institutional-grade; conjunctive checklist prevents override |
| 3 | Evidence Grading System (A/B/C) | **9.0** | Grades have consequences, not just labels |
| 4 | Data Sources Manifest + Fail-Loud Rule | **8.5** | Comprehensive source map; silence-on-absence is banned |
| 5 | Daily Pipeline Architecture (6-task chain) | **8.5** | Well-sequenced, documented failure modes |
| 6 | Retention Policy (3-tier + pin rules) | **8.5** | Over-engineered in the best sense; audit trail protected |
| 7 | Memory.md (working state) | **8.0** | Rich cockpit view; catalyst calendar and watchlist are strong |
| 8 | Preflight-Check Skill | **8.0** | Clean separation of "is data ready?" from "what to trade?" |
| 9 | Daily Trade-Rec Skill | **8.0** | Comprehensive 9-step flow with gap closure and ledger auto-append |
| 10 | Hypothetical Ledger + Signal Review | **8.0** | Correct OOS architecture; untested (ledger empty, day 1) |
| 11 | News-Events Skill + Hotspot System | **7.5** | Category-based search is the right pattern; quality is variable |
| 12 | Market-Brief Skill | **7.5** | Solid producer; scorecard format well-defined |
| 13 | Auto-Memory System | **7.5** | Clean index (7 entries), good type coverage |
| 14 | Audit-Addition Variables (compute pipeline) | **7.0** | Correct methodology; data pipeline hasn't delivered yet |
| 15 | CLAUDE.md (session instructions) | **7.0** | Effective but ~40% redundant with skill definitions |
| 16 | Weekly Pipeline (review + tidy + signal) | **6.5** | Co-scheduling risk; tidy task untested |

---

## What's Genuinely Excellent

**The 8-step methodology** prevents the most common discretionary-trading failure mode: conviction-first reasoning that reverse-engineers supporting evidence. The strict sequence (regime → structural → tactical → catalyst → risk → aggregate → expression → invalidation) forces bottom-up construction. The requirement that every thesis carry a concrete, date-bounded invalidation before entry is a discipline that many professional PMs don't enforce. The reconciliation notes (MVRV demotion, funding-rate as filter not trigger, McLean-Pontiff decay haircuts) show intellectual honesty about alpha decay.

**Risk Rules are binding, not advisory.** Quarter-Kelly, 6–8% portfolio heat, ATR-based stops, correlation gate, circuit breakers — the pre-entry checklist is conjunctive (all six items must pass; any "no" = no trade). This prevents overriding one weak leg with strength elsewhere, which is the right design.

**The fail-loud rule** is perhaps the single most important design decision in the entire system. Silently writing `n/a` for a missing Grade A variable and proceeding to score produces false-confidence trades. Making absence visible (`MISSING — [source]`) and forcing blank scores is correct engineering. On Day 1, this rule held under real pressure — EWY reached |Sum| = +3 but was correctly blocked because intermediary capital data was MISSING.

**Evidence grading is load-bearing.** The explicit prohibition against padding with Grade C, the sunset review for audit additions, the McLean-Pontiff 30–50% Sharpe haircut applied to new variables — these prove the grades have consequences beyond labeling.

---

## What Needs Attention

**Audit-data compute pipeline (P0).** `compute_audit_additions.py` exists and is well-structured, but it depends on CSV files in `/tmp/audit-data/` that aren't being placed by the web-fetch step. After one full day of operation, all three audit-addition variables (residual momentum, intermediary capital, basis-momentum) are still MISSING. This blocks 12 single-stock T-scores, the commodity S divergence-cap, and the cross-asset R-overlay leading gate — roughly half the scoring framework. This is the single biggest operational gap.

**Weekly pipeline co-scheduling.** The weekly regime review and signal review both fire at Sunday 18:00 UTC+8. The reference-pipeline memory notes "jitter separates them" but this is fragile. If the signal review ever writes to Memory.md (which its skill description contemplates), you get a last-write-wins race.

**Memory.md growth rate.** After one day of operation, Memory.md is already at the context-window pressure boundary (~10,000 tokens). The weekly condensation mechanism (Sunday review task) is the right fix, but it hasn't run yet. If the Day-1 growth rate continues before condensation, analysis quality degrades within 2–3 weeks.

**CLAUDE.md redundancy.** The session startup protocol, methodology adherence section, and "What NOT to Do" in CLAUDE.md overlap ~40% with the daily-trade-rec skill's Step 1 and the Methodology Prompt. This isn't harmful (redundancy is cheap insurance), but it creates a maintenance burden: any methodology change must be updated in 3–4 places.

---

## Cross-Reference Integrity Check

| Check | Result |
|-------|--------|
| Methodology Prompt Top-25 entries 26–28 ↔ Data Sources audit rows | ✅ Consistent |
| Risk Rules §5 correlation gate ↔ Methodology Step 6 overlay | ✅ Consistent |
| CLAUDE.md audit-addition binding ↔ Methodology reconciliation note | ✅ Consistent |
| Pipeline task IDs (auto-memory) ↔ skill file references | ✅ Consistent |
| Retention Policy never-digest list ↔ trade-rec + HTML patterns | ✅ Consistent |
| News-events README ↔ master Retention Policy | ✅ Consistent |
| Hypo-ledger columns ↔ signal-review Step 3 status definitions | ✅ Consistent |
| Memory.md regime label ↔ latest market brief (2026-04-14) | ✅ Consistent |
| Data Sources fail-loud rule ↔ Methodology Prompt §163 | ✅ Consistent |
| Auto-memory index ↔ actual memory files | ✅ All 7 entries resolve |

**No broken cross-references found.** Document coherence is strong for a system built over two days.

---

## Top Recommendations (prioritized)

| # | Issue | Impact | Effort |
|---|-------|--------|--------|
| P0 | Get audit-data compute pipeline actually producing data — the CSV fetcher isn't landing files | Critical — blocks ~50% of scoring | Medium |
| P1 | Offset Sunday signal-review to 18:30 UTC+8 to eliminate co-scheduling race | Prevents data corruption | Trivial |
| P2 | Run a manual dry-run of workspace-tidy task this Sunday — validate pin rule, digest, cleanup log | Catches bugs before they matter | Low |
| P3 | Track audit-addition MISSING rates for 2 weeks; if >30%, add backup data sources or caching | Determines whether audit additions are operationally viable | Low |
| P4 | Consolidate CLAUDE.md to purely procedural instructions; keep substantive rules in Methodology Prompt and Risk Rules only | Reduces maintenance burden from 4 places to 2 | Low |
| P5 | Add unit tests and test fixtures for `compute_audit_additions.py` | Prevents silent logic bugs in scoring inputs | Medium |

---

## Structural Risks (not scored)

**Single-point-of-failure: the brief.** The trade rec is almost entirely downstream of the market brief. If the brief has a scoring error (wrong regime label, miscoded S/T/C/R), the rec inherits it. The rec's Step 3 says "confirm or revise" but in practice it mostly rubber-stamps. Brief quality is the binding constraint on rec quality.

**No backtesting infrastructure.** The system measures forward performance (hypo-ledger) but can't test "what would the methodology have recommended over the last 6 months?" before deploying a variable change. Acceptable at day 1; becomes a real gap after the first quarterly audit when methodology changes are proposed.

**Session continuity depends entirely on Memory.md + auto-memory.** If a session fails to update Memory.md after a regime shift, the next session starts with stale state. The startup protocol mitigates this, but a failed edit that goes unnoticed would propagate.

---

## Summary Verdict

The architecture is excellent. The execution is day 1. The bones are right — the methodology is rigorous, the pipeline is well-sequenced, the risk controls are binding, and the feedback loop is properly closed. Fix the audit-data compute pipeline (P0), validate the weekly tasks this Sunday (P1–P2), and this system is fully operational.
