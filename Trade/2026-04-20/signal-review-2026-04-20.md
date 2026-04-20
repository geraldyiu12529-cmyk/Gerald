# Signal Review — Week ending 2026-04-19
**[MOCK — TEST RUN 2026-04-20]**
**Generated:** 2026-04-20 18:00 UTC+8 (Sunday slot — Good Friday pushed to Monday)
**Routine:** signal-review (skill, Opus model — Phase 2 of weekly-regime-signal-review)
**Sources:** master-data-log.xlsx (SignalLedger, PerformanceStats, AuditAdditionLog); framework/Methodology Prompt.md; Memory.md §2/§5; framework/memory-lessons.md

---

## 1. SignalLedger Mark-to-Market

**OPEN positions (signals N030, N031, N032 original entries + N033–N035 today):**

| ID | Asset | Sum | Entry | Mark (Apr-17) | Return | Grade | Thesis holding? |
|----|-------|-----|-------|--------------|--------|-------|----------------|
| N028 | INTC Long | +3 | $64.68 | $69.92 | **+8.10%** | A-driven | YES — residual confirmed; earnings Apr-23 |
| N029 | Gold Long | +3 | $4,780.69 | $4,897.90 | **+2.45%** | A-driven | YES — DXY + real yield intact |
| N031 | QQQ Long | +4 | $640.09 | $649.13 | **+1.41%** | A-driven | YES — vol compression extending |

**CLOSED this week:**
| ID | Asset | Sum | Entry | Exit | Return | Signal correct? |
|----|-------|-----|-------|------|--------|----------------|
| N027 | EWY Long | +3 | $144.10 | $145.39 | **+0.92%** | YES — signal correct; execution error (stop too tight) |

---

## 2. Hit Rate Analysis

**All-time (inception to 2026-04-19):**

| Category | N | Wins | Hit rate | Notes |
|----------|---|------|----------|-------|
| Sum ≥ +3, A-grade-driven | 4 | 4 | **100%** (4/4 profitable; 3 open) | Very small sample |
| Sum = +2 (below threshold) | 12 | — | N/A — not entered | Per methodology: below threshold = no trade |
| Closed trades only | 1 | 1 | 100% (1/1) | EWY +0.92% |

**Sample is too small to draw statistical inference.** Methodology requires 30+ OOS trades for hit-rate stability. Current data is directionally positive but not statistically meaningful.

---

## 3. Audit-Addition Variable Contribution

| Variable | Decision-moving this week | Direction | AuditAdditionLog |
|----------|--------------------------|-----------|-----------------|
| Residual momentum | **YES** — INTC T flip; GOOGL T block; EWY T confirmation | Positive | +1 contribution (INTC) |
| Intermediary capital z | NO — stable +1.38; no R downgrade | Neutral | 0 contribution |
| Basis-momentum | **YES** — WTI cap fired Apr-16; cancelled Apr-19 | Avoided wrong score | +1 contribution (WTI cap) |

**Running contribution log (since 2026-04-14):** Residual = 3 decisions, Basis = 2 decisions, Intermediary = 0 decisions. On track for retention at 2026-10-14 review (threshold: at least 1 decision-moving contribution per variable).

---

## 4. Variable Registry Updates

| Variable | Grade | Change |
|----------|-------|--------|
| Residual momentum | A | RETAIN — decision-moving confirmed 3 trades |
| Basis-momentum | A | RETAIN — cap mechanism working |
| Intermediary capital | A | RETAIN — no demotion trigger (z hasn't crossed −1σ; non-event this regime) |
| HY OAS | A | RETAIN — Grade A anchor for R-leg; stable |
| VIX level | A | RETAIN — vol compression signal fired correctly |

No demotions. No promotions (candidates in Quarterly queue only).

---

## 5. Methodology Notes

**Performance observation:** The 3 open positions (+3/+3/+4 Sum signals) are all profitable within 4 days of entry. This is consistent with momentum-driven entry timing but is a small sample. No methodology changes warranted.

**Open question from weekly-review:** EWY stop lesson (L001/L002 above) should propagate to Risk Rules.md as a clarification on stop-tightening protocol. **Proposed addition to Risk Rules.md §4:** "If protective stop is tightened intraday below methodology stop (2×–3× ATR), document the reason and confirm position size is calibrated to the tighter stop, not the methodology stop." Flag for next quarterly review.

---

## 6. HTML Report

`2026-04-20/report-2026-04-20-signal-review.html` — **[MOCK: HTML report would be generated here by scripts/generate_html_report.py]**
