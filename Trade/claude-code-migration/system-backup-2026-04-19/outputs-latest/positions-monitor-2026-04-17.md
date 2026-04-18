# Positions Monitor — 2026-04-17 (09:00 UTC+8)

## Flag summary

| Position | Flags fired | Severity | Action suggested |
|---|---|---|---|
| **INTC** | F1 stop_buffer | HIGH | Monitor; stop-buffer ~1.9× ATR (below 2.0 threshold). Do not tighten further. Earnings Apr-23 (T−6). |
| **QQQ** | F5 catalyst | HIGH | Monthly equity options expiry TODAY (Apr-17). Expect positioning-flush volatility; do not chase moves driven by gamma unwind. NFLX −9% AH is extra tech-sentiment drag risk. |
| **Gold** | — | — | All-green. Distance to stop 2.6× ATR; DXY sub-99, real yield 1.90% both intact; Iran binary Apr-22 still 5 days out. |

## Per-position detail

### INTC (Long, entry $64.68, size $49.78 USDT, ~0.77 units)
- **Price (latest):** ~$64.09–$64.94 (web quotes diverged; midpoint ~$64.50). Note the Memory.md §2 mark of $67.60 appears stale vs. current quotes — pending reconciliation at next snapshot.
- **Distance to stop ($56):** ~$8.50 (~13% of price).
- **ATR_14d (implied from methodology 2× ATR stop):** ~$4.34 → **buffer ≈ 1.96σ ATR. F1 fires (<2.0).**
- **Time-to-invalidation:** 2026-05-13 (26 days). OK.
- **Next earnings:** 2026-04-23 (6 days). F4 does not fire yet (threshold ≤2 days) — will trigger Apr-21 at the earliest.
- **Thesis variable status:** Green. Terafab/foundry structural read intact; residual momentum +38.48% (confirmed Apr-16 staging); trend not broken (>$55).
- **Recommended action:** **Hold, do NOT tighten stop.** Post-mortem of EWY (stopped out Apr-16 on an over-tightened protective stop) explicitly warned against this. Methodology stop $56 is earning its keep — 9-day uptrend plus semiconductor re-rating implies the position needs room for post-catalyst chop.

### QQQ (Long, avg entry $640.09, combined size $396.85 USDT — tranche 1 $198.10 @ $639.04, tranche 2 $198.75 @ $641.14)
- **Price (latest):** $638.93 premarket (Apr-16 close $637.40, intraday day range $635.26–$639.58).
- **Distance to stop ($600):** ~$38.93 (~6.1% of price).
- **ATR_14d (estimated):** ~$5 → buffer ≈ 7.8σ ATR. F1 clear.
- **Time-to-invalidation:** 2026-05-14 (27 days). OK.
- **Next named catalyst:** **Monthly options expiry TODAY (2026-04-17, days=0). F5 fires (|0|≤1).**
- **Other catalysts:** GOOGL/TSLA earnings Apr-22 (T−5); INTC Apr-23; AMZN Apr-23; FOMC Apr-28–29; META Apr-29.
- **Thesis variable status:** Green. VIX 18.17 (<25); Nasdaq 12-day streak intact through Apr-16; no break of $600.
- **Recommended action:** **Hold, do NOT add on opex strength.** Opex positioning flush can move 1-2% in either direction intraday; NFLX −9% AH compounds tech-sentiment drag risk. If intraday gap down trips $620s on unrelated flow, revisit tranche sizing — do NOT average down without fresh S/T/C confirmation.

### Gold / XAU (Long, entry $4,780.69, size $396.80 USDT, ~0.0830 oz)
- **Price (latest):** ~$4,790–$4,797 (midpoint ~$4,793).
- **Distance to stop ($4,640):** ~$153.
- **ATR_14d:** $58.31 (per TipRanks/Investing Apr-15) → buffer ≈ 2.62σ ATR. F1 clear.
- **Time-to-invalidation:** 2026-05-14 (27 days). OK.
- **Next named catalyst:** Iran ceasefire expiry 2026-04-22 (5 days). F5 not yet armed (>1 day).
- **Thesis variable status:** Green. DXY ~98 (<100); real yield 1.90% (<2.2%); no break of $4,640; contango/basis-momentum signals intact.
- **Recommended action:** **Hold.** Position is structurally the cleanest in the book. Watch for Apr-22 binary.

## Regime / portfolio flags

- **F9 portfolio_heat:** 1.08% of $4,000 NAV (INTC 0.17% + Gold 0.29% + QQQ 0.62%). Well within 6% cap. **Clear.**
- **F10 correlation_gate:** No hard fire — but note: INTC is a component of QQQ (mega-cap semiconductor weighting). Concurrent INTC + QQQ exposure is structurally concentrated in US mega-cap tech, even though recent realized ρ has been decoupled by INTC's +56%/8d re-rating. If INTC reverts and moves in-line with QQQ, combined equity sensitivity is effectively ~$447 USDT (~11% of NAV) with shared FOMC/earnings-season catalyst exposure. **Not an alarm — a watch.** No action required unless a third equity is considered for entry (combined equity heat + shared catalyst risk would fire the gate).

## Data gaps

- **INTC price quote divergence:** StockStory $64.94 (+1.77% 24h); CNN $64.09 (+0.44%); Memory.md §2 mark $67.60 (+4.31%). Memory mark appears stale vs. Apr-17 pre-open quotes — investigate at next snapshot. Does NOT fire F6 (prices were obtained in ≤2 tries) but flags a reconciliation task. **Action: next us-close-snapshot should verify Apr-16 official close and update Memory.md §2 current mark.**

## Claude's read

Two HIGH flags (F1 INTC marginal stop-buffer, F5 QQQ opex-today) but no CRITICAL. Book is structurally fine — heat 1.08%, all stops intact, Gold clean. The main behavioural risk today is (a) reacting to opex-driven QQQ moves as signal when they're positioning noise, and (b) repeating the EWY error by tightening INTC's stop in response to a single down print. Methodology says stand-pat on both. No position changes recommended.

---
*Generated by positions-monitor skill — scheduled run 09:00 UTC+8. Reads: Memory.md §2 §7, .pipeline-status.json, us-close-snapshot-2026-04-17.md. Web-search price pull: INTC, Gold, QQQ. No CRITICAL flags → no escalation to /mnt/.auto-memory/.*
