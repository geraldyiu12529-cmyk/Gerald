# Positions Monitor — 2026-04-22

**Last run:** 09:23 UTC+8 (refresh; prior run 09:00 UTC+8)  
**Positions open:** 3 (P008 CL · P009 SPY · P010 EWJ)  
**Pending triggers:** 3 (P013 INTC · P014 AAPL · P015 GOOGL)  
**Portfolio heat (09:23):** ~2.05% / 8% cap — WITHIN LIMITS  
**Pipeline status:** OK (last pipeline run 2026-04-21 21:12 UTC+8)  
**Digest ingested:** 2026-04-22/slack-digest-2026-04-22-0923.md ✓

---

## Flag Summary

| Flag | Position | Severity | Status | Detail |
|---|---|---|---|---|
| F1 stop_buffer | P008 CL | HIGH | ⚠ WATCH | Buffer $4.31 / ATR~$3.0 = 1.44× — below 2.0 threshold. Improved from critical $1.35 at 09:00 but regime vol elevated. |
| F1 stop_buffer | P009 SPY | HIGH | ⚠ ACTIVE | Buffer ~$10.0 / ATR~$10 = ~1.0× — well below 2.0 threshold. FOMC exit trigger at $700 within $6. |
| F4 earnings | P015 GOOGL / P009 SPY | HIGH | ⚠ ACTIVE | GOOGL+TSLA earnings tonight (Apr-22 AC US = Apr-23 ~08:00 UTC+8). P015 entry gate. SPY sentiment exposed. |
| F4 earnings | P013 INTC | HIGH | ⚠ ACTIVE | INTC earnings Apr-23 AC US = Apr-24 ~08:00 UTC+8. ~46h. P013 entry gate. |
| F5 catalyst | P008 CL | HIGH | ⚠ ACTIVE | Iran ceasefire binary live. WTI range today $85.67–$91.42. Hormuz talks ongoing, no resolution. |
| F10 correlation | P009 SPY / P010 EWJ | MED | ℹ NOTE | Both equity ETFs long; ρ~0.7–0.8. Haircut already applied (EWJ sized 0.75% vs SPY 1.0%). No action required. |
| F13 cloud_alert | P008 CL | MED | ℹ RESOLVED | Cloud digest (09:23) flagged stop-proximity. Price now $89.61 — materially improved. Alert origin logged. |
| F3 time_inv | P014 AAPL | NOTE | ⚪ 8 days | time-stop 2026-04-30 fires at ≤7 days. Fires **tomorrow** (Apr-23). Pre-flag. |
| F11 COT | P008 CL | MED | ⚠ UNRESOLVED | COT search inconclusive — elevated speculative longs expected in Hormuz vol regime. Cannot confirm. |

**No flags:** F2 · F6 · F7 · F8 · F9 · F12

---

## §1 — P008 CLUSDT — WATCH: Stop Buffer Improving, Binary Still Live

| Field | 09:00 UTC+8 | 09:23 UTC+8 |
|---|---|---|
| Asset | CLUSDT Bybit Perp Long (WTI proxy) | ← |
| Entry | $88.250 | ← |
| Stop | $85.300 | ← |
| Current price | ~$86.65 | **$89.61** |
| Buffer to stop | ~$1.35 (CRITICAL) | **$4.31 (WATCH)** |
| ATR 14d (est.) | ~$2.5 (elevated) | ~$3.0 (extreme vol) |
| Buffer / ATR ratio | 0.54× → F1 CRITICAL | **1.44× → F1 WATCH** |
| Intraday range | $85.67 – $91.42 | ← (same session) |
| Risk to stop | ~$6.01 | **~$19.15** |

**Assessment:** WTI recovered strongly to $89.61 — up $4 from the 09:00 level. The extreme intraday range ($5.75) reflects the Hormuz binary still unresolved. Iran ceasefire talks ongoing in Pakistan with Iran non-participating. Any breakdown in talks sends WTI sharply lower — a move back to $86 retests the stop zone. This is off-methodology; no thesis to repair.

**Flags active:** F1 (buffer/ATR 1.44× < 2.0), F5 (Hormuz binary active), F13 origin logged.

**Action options (for Gerald):**
- **Hold with stop**: Current $4.31 buffer provides more cushion — acceptable if ceasefire binary is neutral-to-bullish.
- **Discretionary close**: Consider if WTI retraces toward $87-88. No methodology basis to add or widen stop.
- **Do not widen stop** without methodology basis.

---

## §2 — P009 SPYUSDT — WATCH: FOMC Exit Protocol Active

| Field | Value |
|---|---|
| Asset | SPYUSDT Bybit Perp Long |
| Status | Methodology — Sum+3 (S+1/T+1/C0/R+1) |
| Entry avg (4 tranches) | $710.17 |
| Stop | $696.00 |
| Current price | ~$706 (09:00 reading; US close ~$706) |
| Intraday range | $702.64 – $711.28 |
| Buffer to stop | ~$10.0 (1.44%) |
| ATR 14d (est.) | ~$10 (SPY vol regime) |
| Buffer / ATR ratio | ~1.0× → F1 ACTIVE |
| FOMC exit trigger | Exit if SPY <$700 before Apr-28 |
| Distance to exit trigger | ~$6 |
| Intraday low vs trigger | $702.64 — within $2.64 of triggering |
| Risk to stop | ~$19.60 |
| Time-stop | 2026-05-13 |
| Unrealized P&L | ~−$4.17 vs avg entry |

**Thesis invalidation checks:**
| Variable | Threshold | Current | Status |
|---|---|---|---|
| VIX | >25 | ~19.5 | ✓ CLEAR |
| HY OAS | >4.50% | 2.85% (stale) | ✓ CLEAR |
| SPY price | <$696 | ~$706 | ✓ CLEAR |
| FOMC protocol | SPY <$700 before Apr-28 | $706 — 6 days to FOMC | ⚠ MONITOR |

**Flags active:** F1 (buffer/ATR ~1.0×), F4 (GOOGL+TSLA earnings tonight affect SPY gap).

**Catalyst note — GOOGL/TSLA earnings tonight (Apr-22 AC US):**
- GOOGL: Consensus EPS $2.68 / rev $106.88B. Beat → gap-up SPY tomorrow, provides FOMC trigger relief. Miss → gap-down, may push SPY <$700 triggering exit protocol.
- TSLA: Consensus EPS $0.37 / rev $22.7B. 6% deliveries growth YoY but below expectations (372K est vs 358K actual).
- Results will be known ~Apr-23 08:00+ UTC+8.

**No action yet.** FOMC exit rule triggers only below $700.

---

## §3 — P010 EWJUSDT — CLEAR

| Field | Value |
|---|---|
| Asset | EWJUSDT Bybit Perp Long |
| Status | Methodology — Sum+3 (S+1/T+1/C0/R+1) |
| Entry avg (2 tranches) | $88.44 |
| Stop | $86.00 |
| Current price | ~$89.18 |
| Buffer to stop | $3.18 (3.6%) |
| ATR 14d (est.) | ~$1.2 |
| Buffer / ATR ratio | ~2.6× → F1 CLEAR |
| P&L vs entry | +$0.74 (+0.84%) |
| Risk to stop | ~$43.10 |
| Time-stop | 2026-06-30 |

**Thesis invalidation checks:**
| Variable | Threshold | Current | Status |
|---|---|---|---|
| USDJPY | <150 | 158.9 | ✓ CLEAR (ample margin) |
| BOJ emergency | ≥50bp hike | None detected | ✓ CLEAR |
| Nikkei | −5% move | No signal | ✓ CLEAR |
| US-China escalation | Escalation signal | None | ✓ CLEAR |

**No flags. CLEAR.**

---

## §4 — Portfolio Heat (09:23 UTC+8)

| Position | Units | Stop | Current | Risk to stop |
|---|---|---|---|---|
| P008 CL | 4.444 | $85.300 | $89.61 | ~$19.15 |
| P009 SPY | 1.9601 | $696.00 | ~$706.00 | ~$19.60 |
| P010 EWJ | 13.553 | $86.00 | $89.18 | ~$43.10 |
| **Total** | — | — | — | **~$81.85** |

**Portfolio heat: ~$81.85 / ~$4,000 NAV ≈ 2.05%** — within 8% cap. F9 not triggered.

---

## §5 — Pending Triggers Status

### P013 INTC — Entry after Apr-23 AC beat (~$68–72 limit)
- **F4 ACTIVE:** Earnings Apr-23 after US close = Apr-24 ~08:00 UTC+8. ~46h away.
- Sum+4 (S+1/T+1/C+1/R+1). V026 residual +13.89% (A). C+1 for Terafab/foundry validation.
- Entry trigger: confirmed beat → enter Apr-24 UTC+8 morning. Size 1.0%.

### P014 AAPL — Entry zone ~$271–274 (active)
- **Current price: ~$273.05** (Apr-22; AH ~$271 after CEO announcement, recovered).
- **IN ENTRY ZONE.** Entry zone $271–274 = ACTIVE.
- **CEO transition (Apr-20):** Tim Cook stepping down Sept 1; John Ternus (SVP Hardware) confirmed as successor. Market reaction: −0.5% AH on Apr-20 → recovered to $273 today.
- **Methodology note:** C=0 in trade-rec (no near-term catalyst). CEO transition could be a C-leg input, but is a known multi-month event (Sept 1 effective). Does not change Sum — C=0 was already scored on structural momentum. No C-leg revision required by this announcement.
- **F3 pre-flag:** time-stop 2026-04-30 is 8 days away. F3 fires at ≤7 days → **fires tomorrow (Apr-23)**. Hard exit April 30 before May 1 earnings.
- **Recommendation:** AAPL is IN zone. Entry on limit $271–274 is valid. Size 0.75% (correlation haircut vs SPY). Must exit before 2026-04-30.

### P015 GOOGL — Entry after Apr-22 AC beat confirmation
- **F4 ACTIVE:** GOOGL reports tonight (Apr-22 AC US = Apr-23 ~08:00 UTC+8).
- Sum+3 (S+1/T=0/C+1/R+1). C+1 scored pre-earnings. Entry trigger: confirmed beat confirmed.
- **Do not enter pre-results.** Entry after UTC+8 morning confirmation.
- GOOGL consensus: EPS $2.68 / rev $106.88B. Alphabet has beaten in each of the past 4 quarters.

---

## §6 — Upcoming Events (next 24h)

| Time (UTC+8) | Event | Positions affected |
|---|---|---|
| Apr-22 AC (tonight ET) | GOOGL Q1 earnings | P015 entry gate; SPY gap catalyst |
| Apr-22 AC (tonight ET) | TSLA Q1 earnings | SPY/QQQ sentiment |
| Apr-23 AC (tomorrow ET) | INTC Q1 earnings | P013 entry gate |
| Apr-23 morning UTC+8 | GOOGL/TSLA results known | P015 decision; SPY gap confirmed |
| Apr-28–29 | FOMC | P009 SPY exit protocol ($700) |

---

## §7 — Monitor Verdict (09:23 UTC+8)

**P008 CL:** WATCH — stop buffer improved from critical ($1.35) to watch ($4.31) as WTI recovered to $89.61. F1 still active given elevated regime ATR. Ceasefire binary remains live (F5). No action required unless WTI retraces to $87–88.

**P009 SPY:** WATCH — FOMC exit protocol ($700) within $6 of intraday low ($702.64). Stop buffer F1 active (~1.0× ATR). GOOGL earnings tonight are the key swing factor: beat → gap-up relief; miss → may trigger $700 exit. No action until $700 breached.

**P010 EWJ:** CLEAR — +0.84%, 3.6% buffer, all invalidation variables clear.

**P014 AAPL:** IN ZONE at $273. CEO transition digested, C=0 unchanged. Valid to enter on limit $271–274, 0.75%. F3 fires tomorrow.

**P013 INTC / P015 GOOGL:** Both F4 active — earnings within 48h. No entry until post-confirmation.
