# System Review — 2026-04-17 (inaugural run, on-demand)

**Coverage:** all skills, scheduled tasks, and workspace files at `/mnt/Trade/` and `/mnt/.claude/skills/` as of 2026-04-17 evening UTC+8.
**Window for acted-on evidence:** 2026-04-14 (workspace inception) through 2026-04-17 — 4 calendar days, 3 trading sessions, 4 executed trades, 17 SignalLedger rows (approx).
**Prior system-review:** none.
**Self-audit:** skipped (first run).

---

## Headline finding

**The architecture is correctly shaped but is leaking ~900K–1.3M tokens/month on avoidable startup boilerplate and repeated-artifact reads, while the monitoring bucket holds zero processes despite four live-money positions. Fix the boilerplate leak on `us-close-snapshot-730am-v2` and `workspace-tidy-sunday-9pm`, apply the six drift-patch files blocked by the read-only Windows mount, and add a scheduled positions/thesis monitor — these three moves free ~25–35% of monthly burn and close the largest structural gap.**

---

## 1. Value-chain matrix

| Bucket | Skills | Scheduled tasks | Count | Status |
|---|---|---|---|---|
| 1. Research | literature-review | `semi-annual-literature-review`, (½ of weekly-regime-signal-review) | ~1.5 | thin — 2 runs since inception |
| 2. Rec-generation | market-brief, news-events, daily-trade-rec | `us-close-snapshot-730am-v2`, `preflight-audit-data-1945pm`, `daily-market-brief-8pm-v2`, `daily-news-events-810pm-v2`, `daily-trade-recommendation-820pm-v2` | 5 | dense — the system's load-bearing spine |
| 3. Execution | trade-update (reactive) | none | 0.5 | reactive only; no scheduled hook |
| 4. Monitoring | none | none | **0** | **structural gap** |
| 5. Post-trade review | signal-review | (½ of `weekly-regime-signal-review-6pm`) | 1.5 | one full cycle run; inaugural |
| 6. Infrastructure | pipeline-recovery, consolidate-memory | `pipeline-recovery-830pm`, `workspace-tidy-sunday-9pm` | 3 | healthy |
| 7. Meta-review | system-review, quarterly-methodology-review | `system-review-semi-annual`, `quarterly-methodology-review`, `monthly-bootstrap-review` (transient), `methodology-audit-6mo-review-2026-10-14` (one-time) | 3–4 | borderline over-represented for a 4-day, <30-closed-signal system; justified only by audit-addition deadline commitment |

**Headline imbalance:** Monitoring = 0. Gerald holds INTC + Gold + QQQ concurrently (combined ~1.08% portfolio heat, combined equity heat ~0.79%) and just closed EWY on an over-tightened stop (Memory §7). No scheduled process watches stop breaches, thesis invalidation, time-inv clocks, or correlation-gate drift.

Utility skills (docx/pdf/pptx/xlsx, skill-creator, schedule, setup-cowork) are unused by the trading scaffold and cost zero per-run tokens until invoked — excluded from bucket map.

---

## 2. Per-process effectiveness + efficiency audit

### Trading-core (Rec-generation + Execution)

| Process | Bucket | Last-acted evidence | Token cost/run (K) | Monthly burn (K) | Verdict | Rationale |
|---|---|---|---|---|---|---|
| `daily-trade-recommendation-820pm-v2` / daily-trade-rec | Rec-generation | Gold LONG promoted 2026-04-16 v3 → executed 22:28 UTC+8. INTC/EWY/QQQ also traced. Four money-moving trades in 4 days. | 45 | 990 | **KEEP** | The earn-money process; output length justified by the 8-step decision trace. |
| `daily-market-brief-8pm-v2` / market-brief | Rec-generation | trade-rec-2026-04-16 §1 cites brief 4× directly. Gold Sum +3 signal originated in brief §4. | 24 | 528 | **MODIFY-efficiency** | Scorecard §3 has 25 rows; 8 of them are Sum≤+1 with no open thesis. Collapse flat rows → save 2–4K/run. |
| `daily-news-events-810pm-v2` / news-events | Rec-generation | news-2026-04-16 Iran "major breakthrough" drove Gold C+1 and Brent C−1 scoring in trade-rec v3. | 15 | 330 | **MODIFY-scope** | 2026-04-17 lit review flagged 3 HIGH-severity overlaps with brief (calendar double-count, data-release double-count, political-communication filter). Patch drafted (`news-events-skill-md-patch-2026-04-17.md`) but blocked by ro mount. |
| `preflight-audit-data-1945pm` | Rec-generation | audit-data-staging-2026-04-16.md drove 2 decision-moves in v3 trade rec: WTI S cap (divergence), GOOGL T-unblock (+30.52% residual). | 22 | 484 | **KEEP** | Lean output, already read-override optimized, 3-of-3 Grade A audit variables decision-moving. |
| `us-close-snapshot-730am-v2` | Rec-generation (upstream) | trade-rec-2026-04-16 §1 cites us-close-snapshot-2026-04-16 for SPX/NDX dual ATH + EIA failure-to-rally. | 52 (incl. ~40 leak) | 1,155 (incl. ~880 leak) | **MODIFY-efficiency HIGH** | Read-override NOT YET applied (per reference_pipeline.md "Future optimization"). 30–50K boilerplate leak × 22 sessions. Single largest efficiency leak in pipeline. |
| `pipeline-recovery-830pm` / pipeline-recovery | Infrastructure | No observed failures since 2026-04-14 — so no recovery events to cite. But Phase A triage ran every day (<3K tokens/run by design). | 3 | 66 | **KEEP** | Cheap insurance; structural-sniff hardening 2026-04-17 documented in project_system_state.md. |
| trade-update (reactive) | Execution | 4 execution events Apr-15 through Apr-17 (EWY enter/stop, INTC, Gold, QQQ ×2). Memory §2 reflects all. | 5 per fire | ~20 (4 fires/month observed) | **KEEP** | Reactive-only; working. |

### Research + post-trade review + meta

| Process | Bucket | Last-acted evidence | Token cost/run (K) | Monthly burn (K) | Verdict | Rationale |
|---|---|---|---|---|---|---|
| `weekly-regime-signal-review-6pm` | Research + Post-trade | weekly-review-2026-04-15 graduated EWY from watchlist to first clean Sum +3; signal-review-2026-04-15 surfaced 5 MONITOR items. | 39 | 156 | **KEEP** | Merger (Apr-16) already saved ~1 startup/week. Small overlap between phases is tolerable. |
| `quarterly-methodology-review` / quarterly-methodology-review | Meta-review | Inaugural Q1 2026-04-15: all 13 dimensions RETAIN, 0 change proposals, 5 candidates DEFER. No methodology changes resulted — which is correct at N=0 closed signals, not evidence of waste. | 47 | 15.5 | **KEEP** | Owns audit-addition Q4 GO/NO-GO gate ahead of 2026-10-14 deadline; that alone justifies retention. |
| `semi-annual-literature-review` / literature-review | Research | 2026-04-17 scope-limited run produced 5 deferred variable candidates + 3 HIGH-severity news-events overlap flags. Patches drafted but blocked. | 47 | 8 | **KEEP** | Cheap on monthly basis; pipeline has 1 warm candidate (daily GPR). |
| `monthly-bootstrap-review` (transient) | Meta-review | Not fired yet (first run 2026-05-01). | 25 | 25 | **HOLD** | Structurally sound; transient audit during early sample; auto-disables after Jul 1. |
| `methodology-audit-6mo-review-2026-10-14` (one-time) | Meta-review | Not fired yet. | — | — | **KEEP** | Hard-coded deadline commitment. |
| `system-review-semi-annual` / system-review | Meta-review | This file. First run. | 50 | 10.5 | **HOLD** (cannot self-remove on first run) | Self-removal rule arms if next 2 cycles produce 0 acted-on proposals. |
| `workspace-tidy-sunday-9pm` | Infrastructure | archive/2026-04, archive/weekly, archive/duplicates all populated; cleanup-log.md actively maintained. | 43 (incl. ~35 leak) | 172 (incl. ~120 leak) | **MODIFY-efficiency HIGH** | Read-override NOT YET applied (per reference_pipeline.md). Same Windows ro mount issue as us-close. |
| consolidate-memory | Infrastructure | MEMORY.md is a 10-entry compact index — consolidation has clearly run at some point, but no direct recent fire to cite. | 10 on demand | 0 scheduled | **KEEP** | 34-line SKILL.md; reactive-only. |

### Utility skills (docx / pdf / pptx / xlsx / skill-creator / schedule / setup-cowork)

All on-demand, not scheduled into the trading loop, zero baseline burn. **KEEP all.**

### System-wide token burn (estimated)

| Process | Monthly tokens (K) | Share |
|---|---|---|
| us-close-snapshot-730am-v2 | 1,155 | 29% |
| daily-trade-recommendation-820pm-v2 | 990 | 25% |
| daily-market-brief-8pm-v2 | 528 | 13% |
| preflight-audit-data-1945pm | 484 | 12% |
| daily-news-events-810pm-v2 | 330 | 8% |
| workspace-tidy-sunday-9pm | 172 | 4% |
| weekly-regime-signal-review-6pm | 156 | 4% |
| pipeline-recovery-830pm | 66 | 2% |
| Remainder (quarterly, literature, bootstrap, system-review, monthly-bootstrap, trade-update fires) | ~60 | 2% |
| **Total** | **~3,940** | 100% |

**Top-3 burn:** us-close-snapshot (29%, ~76% of which is boilerplate leak), trade-rec (25%, justified), brief (13%). **Prior cycle comparison:** N/A (first run).

---

## 3. Gaps and redundancies

### Gaps (missing capability)

1. **Monitoring bucket is empty.** INTC, Gold, QQQ are live. EWY just stopped out. No scheduled process watches for stop breach, thesis invalidation trigger, time-inv clock (INTC earnings Apr-23 in 6 days; time-inv 2026-05-13 — 26 days), correlation-gate drift, or catalyst-resolution. This is the structural gap with the highest money-protection payoff.

2. **No executed-trade P&L attribution in the pipeline.** SignalLedger marks *hypothetical* signals. EWY realized +$2.75 is in Memory.md §7 Closed Trades but there is no scheduled job that attributes this P&L by regime / score component / lesson. `signal-review` marks hypotheticals; `trade-update` logs execution events but does not run attribution.

3. **No pre-entry-checklist compliance audit on executed entries.** EWY's stop was $145, not the methodology $133 (Memory §7 lesson). The deviation was recorded only after the stop hit. Nothing in the pipeline cross-references the entry price/stop actually used against the pre-entry checklist written in the trade rec for that asset.

4. **Audit-addition 6-month review is hard-coded to the 2026-04-14 additions only.** If Q3/Q4 quarterly review promotes new Grade A candidates, there is no template task for their N-month live review. Variable-Discovery-Protocol.md (260 lines) codifies discovery, not review lifecycle.

5. **Authoritative-doc session bloat.** Session Startup Protocol calls for reading Methodology Prompt (~7K), Cores (~19K), Data Sources (~4K), Risk Rules (~2K), Retention Policy (~2K), MEMORY.md + linked memory files (~5K), Memory.md (~3K), plus Data-Retrieval-Fallback-Framework (674 lines ~22K) when it fires. The brief and rec use ~5–8K of that per run for actual decisions; the rest is ambient context.

6. **Lessons-to-gates loop is manual.** memory-lessons.md accumulates lessons ("stop too tight", "sell-the-news on catalyst beat") but nothing converts them into Risk Rules checklist additions or trade-update deviation checks. EWY stop-tightening pattern could repeat.

### Redundancies (excess capability / efficiency drag)

1. **Startup-boilerplate leak on `us-close-snapshot-730am-v2` + `workspace-tidy-sunday-9pm`.** Both tasks execute the full Session Startup Protocol (Methodology + Cores + Memory + Risk Rules + Retention + MEMORY.md) when they should not — per reference_pipeline.md "Future optimization" section, both were identified as candidates for read-override back on 2026-04-16 but not yet applied because the task prompts live on `C:\Users\Lokis\Documents\Claude\Scheduled\` which the sandbox cannot reach. Estimated combined leak ~1.0M tokens/month.

2. **Catalyst calendar duplicated 5 ways.** Brief §5 (12 rows), news §3 (9 rows), trade-rec §5/§8 (catalyst notes), weekly-review §7 (6 rows), Memory §6 (16 rows). Same dates, same events. One `catalysts-YYYY-MM-DD.md` artifact read by all would save ~4–6K tokens/day.

3. **Scorecard restated 5 ways per week.** Brief §3 (25 rows), trade-rec §3 (7–10 rows), us-close snapshot §1 (delta table), weekly-review §8 (closing scorecard), signal-review §4 (score component table). master-data-log.xlsx is the sole structured store — producers still restate the tables in prose.

4. **News file read by two processes in full (brief and trade-rec).** Trade rec also reads the brief that already summarizes the news. A cached `news-signals.json` with extracted C-score triggers could replace ~4–5K token re-reads.

5. **Six unresolved `*-patch-*.md` drift files at root,** all blocked by the same ro mount issue: `news-events-skill-md-patch-2026-04-17.md`, `system-review-skill-patch-2026-04-17.md`, `skill-description-tightening-2026-04-17.md`, `retrieval-monitoring-patches.md`, `streamlining-patches.md`, `skill-patches-2026-04-15.md`. Each represents uncommitted improvements that workspace-tidy must walk. Indicator of a broken write path, not just backlog.

6. **Dated producer-output duplicates and stale folders.** `skill-patches/`, `skill-patches.zip`, `system-review-skill-package-2026-04-17.zip`, `system-review/`, `skill-updates/`, and several zi* suffixed scratch folders (`zi742LF3`, `ziR3ccgi`, `ziTRiBMK`, `ziXZFMx3`, `zinV6fOW`, `zir3gEmR`, `zivrfzcP`) accumulate at root. Workspace-tidy Phase 3 should be flagging these; they're not in the Retention Policy's "In scope for tiering" list so they fall under the ≥8-day archive rule — but some are still there.

---

## 4. Ranked proposals

### MODIFY-efficiency — HIGH

**E1. Apply read-override prepend to `us-close-snapshot-730am-v2` and `workspace-tidy-sunday-9pm` task prompts.**
- Evidence: `reference_pipeline.md` "Future optimization" section explicitly names these two tasks with exact prepend text drafted. Sandbox cannot reach `C:\Users\Lokis\Documents\Claude\Scheduled\`, so Gerald must edit manually.
- Estimated savings: 30–50K tokens/run × (22 us-close + 4 tidy) = **780K–1.3M tokens/month**. 20–33% of total monthly burn.
- Risk: low — preflight-audit-data merger applied the same pattern successfully on 2026-04-16.

**E2. Apply the six blocked `*-patch-*.md` files.**
- Evidence: `project_literature_review_2026-04-17_news-events.md` (3 HIGH-severity news-events gaps), `project_structural_sniffs_2026-04-17.md` (pipeline rubric enrichment), `reference_skill_description_limit.md` (1024-char cap), plus three pre-existing patch files.
- Impact: closes news-events scope overlaps and skill-description truncation risk; removes drift files from root.
- Mechanism: Gerald applies via the same Windows-side edit path as E1, OR we regenerate clean SKILL.md replacements that Gerald drops in via the Cowork mount (which is writable on the skills side). Worth Gerald confirming which path unblocks faster.

**E3. Trim market-brief output ~30%.**
- Evidence: `market-brief-2026-04-16.md` §3 scorecard has 25 rows; 8 rows are Sum ≤+1 with no open thesis (Palladium, USDJPY, PLTR zero-thesis, etc.). Key Variable Readings sections restate unchanged values daily.
- Rule: collapse flat rows to a single line; table delta-only variables where unchanged.
- Estimated savings: 2–4K tokens/run × 22 sessions = **44–88K tokens/month** freed for trade-rec input budget.

**E4. Externalize rolling catalyst calendar to `catalysts-YYYY-MM-DD.md` written once (by news-events), read by brief / rec / weekly-review / Memory sync.**
- Evidence: 5× duplication observed in current outputs. Same 9–16 rows restated.
- Estimated savings: ~4–6K tokens/day across producers = **80–120K tokens/month**.
- Scope: small refactor to news-events skill (add Section 3 → write catalysts file); brief/rec SKILL.md prepend to read the shared file instead of re-listing.

**Efficiency-HIGH tally:** If E1+E2+E3+E4 applied, estimated **~900K–1.5M tokens/month saved (~25–38% of current burn)**, directly freeing trade-rec context budget for higher-signal decisions.

### MODIFY-scope — MEDIUM

**S1. Raise catalyst-calendar ownership to news-events; remove duplicate restatement from brief §5 and trade-rec §5/§8 narratives.** Pairs with E4.

**S2. Add an "executed-trade attribution" phase to `weekly-regime-signal-review-6pm`.** Phase 3 marks hypothetical signals today; Phase 3.5 should mark-to-market actual executed trades with P&L by regime, score component, and deviation-from-checklist, pulled from Memory §7 Closed Trades. Evidence: EWY closed 2026-04-16 21:55 +$2.75 — no attribution in ledger downstream.

### ADD — MEDIUM/HIGH

**A1 (HIGH). Add `positions-monitor` skill + scheduled task.**
- Fills the zero-process Monitoring bucket.
- Triggers: (a) intraday at 09:00 UTC+8 Mon–Fri (checks open-position prices, stop buffer, time-inv clock), (b) on-demand via "check positions" / "monitor book" phrases.
- Reads: Memory §2 Open Positions, latest market quotes (web pull), master-data-log DailyVariables correlation snapshot.
- Writes: `positions-monitor-YYYY-MM-DD.md` only when at least one flag fires (stop buffer <2×ATR, time-inv <7 days, correlation gate drift, catalyst date ±1 day, thesis-invalidation variable breach).
- Fail-loud if silent: no output means all-green, explicit.
- Estimated cost: 8–12K/run × 22 sessions = ~220K/month. Justified by ~$4K at-risk book.
- Evidence this is needed: EWY stop-too-tight (Memory §7 lesson); INTC earnings Apr-23 with no scheduled pre-event check; QQQ time-inv 2026-05-14.

**A2 (MEDIUM). Extend trade-update skill with pre-entry-checklist compliance check.**
- When a trade execution event fires, cross-reference the entry price/stop/size actually used against the pre-entry checklist for that asset in the most recent trade rec.
- Log any deviation (stop tighter/looser than methodology, size differs from recommended, correlation gate violated) to memory-lessons.md automatically.
- Prevents the EWY stop-tightening pattern from repeating silently.
- Cost: ~3K per execution event, negligible monthly.

**A3 (LOW). Add an N-month audit-review template** instantiable for any future promoted variable, so Q3/Q4 2026 promotions inherit a review slot automatically rather than being one-off schedules.

### REMOVE

**None.** Every process cites acted-on evidence within the 4-day window. Premature at N<30 closed signals.

---

## 5. Efficiency tally

| Proposal | Tokens/month saved (K) |
|---|---|
| E1 — read-override on us-close + workspace-tidy | 780–1,300 |
| E2 — apply 6 blocked patches (structural, not token) | ~15 (remove re-read of drift files) + quality gain |
| E3 — trim market-brief flat rows | 44–88 |
| E4 — shared catalysts artifact | 80–120 |
| **Efficiency-HIGH total** | **~920–1,520** |
| A1 — positions-monitor (NEW burn) | −220 |
| **Net monthly change** | **~+700K to +1,300K tokens freed** |

Current burn ~3.94M → projected post-change burn ~2.6–3.2M tokens/month. The freed ~700K–1.3M directly feeds the trade-rec context window for higher-signal decisions.

Prior-cycle comparison: N/A (first run).

---

## 6. Self-audit

Skipped — first run. Self-removal rule arms next cycle. If the next two cycles produce zero acted-on proposals, the first finding of cycle 3 must read: *"REMOVE system-review — failed own test: two consecutive cycles with zero acted-on recommendations."*

---

## 7. Next review date

Per skill spec ("first Sunday of (current month + 6)"): **2026-10-04 (Sunday).**

Per scheduled task cron (`0 19 1-7 5,11 0`, first Sunday of May/Nov): **next firing 2026-05-03 (Sunday, 16 days after this on-demand run).**

Gerald's call on whether to let the scheduled May 3 run fire or disable it once and let the natural semi-annual cadence pick up 2026-10-04 / 2026-11-01. Recommendation: let May 3 fire — it will be the self-audit cycle that tests whether any of the proposals above got applied, and that's the whole point of the self-removal discipline.

---

## Implementation pointers

- **Adds (A1–A3)** → invoke `skill-creator` to scaffold the skill; invoke `schedule` for the cron.
- **Removes** → none this cycle.
- **Modifies (E1, E2, parts of E3/E4)** → Gerald edits Windows-side task prompts for E1; Gerald applies patch files for E2; skill-creator for E3/E4 SKILL.md changes.

All proposals above are proposals, not applied changes. This skill does not edit anything.
