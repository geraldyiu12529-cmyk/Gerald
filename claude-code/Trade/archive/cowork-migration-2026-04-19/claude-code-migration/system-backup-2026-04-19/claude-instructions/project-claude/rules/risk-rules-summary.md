---
globs: ["trade-rec-*.md", "report-*-trade-rec.html"]
---

# Risk Rules — Pre-Entry Checklist (binding)

Full rules in `Risk Rules.md`. Summary for quick reference:

**Pre-entry — ALL must pass or no trade:**
1. |Sum| ≥ 3 with C scored (not blank)
2. Invalidation written, concrete, date-bounded
3. Correlation gate clean (shared regime variable = single theme, size to sector cap)
4. Per-position risk ≤ 2% AND post-entry portfolio heat ≤ 8%
5. ATR stop set (2–3× commodities/crypto, 1.5–2× equities)
6. Catalyst asymmetry stated (surprise vs confirmation dependent)

**Sizing:** Inverse-ATR with quarter-Kelly cap, max 25% single position.
**Heat limits:** 6–8% total, 25% sector cap, 5–15% crypto cap.
**Drawdown breakers:** −15% → 50% reduce; −20% → defensive (gold + cash).
**Correlation gate:** BTC + ETH ≈ one bet (~80% co-fire). Never double-count.
