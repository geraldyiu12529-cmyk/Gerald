---
globs: ["market-brief-*.md", "trade-rec-*.md", "signal-review-*.md", "weekly-review-*.md"]
---

# Evidence Grade Rules

When writing any trading analysis file:
- Cite evidence grades (A/B/C) on every variable and signal reference
- Grade A: replicated across samples, coherent economic mechanism, long history (momentum, carry, credit spreads, policy surprises, BTC order imbalance)
- Grade B: moderate, regime-dependent (news sentiment, options skew, MVRV/SOPR, exchange flows)
- Grade C: weak, narrative-heavy (stock-to-flow, halving cycles, seasonality)
- Never present Grade C as actionable without explicit qualification
- No stock-to-flow or halving-cycle timing — these are Grade C at best
- Fail-loud on MISSING Grade A: print `MISSING — [sources attempted]`, leave score leg blank
