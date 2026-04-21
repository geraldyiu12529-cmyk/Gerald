# T.system Architecture Review — 2026-04-21

**Reviewer:** architecture-review (read-only audit)
**Baseline:** `Trade/pipeline/architecture.md` (last updated 2026-04-21)
**Scope:** skills, scheduled tasks, framework docs, pipeline state, scripts, Excel, changelog.

---

## Summary

**Verdict: DEGRADED.** 12 gaps identified. Core wiring is intact (all 13 SKILL.md files present; all 10 framework docs present; all 10 scripts present; scheduled-tasks registry has 22 live tasks covering every architecture-listed routine). Drift is concentrated in (1) date-folder convention violations for today's preflight outputs, (2) missing catalysts-cache directory, (3) Risk Rules checklist count (architecture says 7 — Risk Rules has 8), (4) stale/contradictory Known Structural Risk entries (numpy is present), (5) Memory.md §2 does not reflect SPY promotion logged in `.pipeline-status.json`, (6) changelog in §8 is incomplete relative to the last 10 commits, and (7) three registered scheduled tasks are absent from the architecture record.

---

## Verified ✅

- All 13 SKILL.md files exist under `Trade/.claude/skills/{skill}/SKILL.md` (asset-universe-update, daily-trade-rec, literature-review, market-brief, methodology-sync, news-events, pipeline-recovery, pipeline-smoketest, positions-monitor, quarterly-methodology-review, signal-review, system-review, trade-update).
- All 13 framework documents listed in §2 exist on disk at declared paths.
- All 10 scripts listed in §3 exist under `Trade/scripts/` (plus 3 extras — see Orphans).
- numpy 2.4.4 is importable in the current Python environment.
- BNMA + PL-NMA meta-analysis files present at declared paths (`Trade/bnma/meta-analysis/`).
- 22 scheduled tasks registered; all architecture-listed tasks map to a live `taskId`.
- `.pipeline-health.json` shows all 7 external sources UP; cache coverage 53.5% (38/71); predicted MISSING = 0.
- `.pipeline-status.json` preflight/market-brief/news-events/trade-rec/recovery all recorded for 2026-04-20.
- `audit-data-missing-tracker.md`: no variable has ≥2 consecutive MISSING rows (ResidMom: 1 MISSING on 04-20 then FALLBACK on 04-21; InterCap: 1 MISSING then LIVE; BasisMom: 0 MISSING).
- V026/V027/V028 + Overlay Gate + V029–V035 present in `market-brief`, `daily-trade-rec`, `methodology-sync` SKILL.md wiring (66 references across 3 skills).
- Recent commits (12cef28, 62ac770, 5613928, b99e66d, 80352d9) match framework state.

---

## Gaps and Drift 🔶

| Item | Expected | Actual | Severity |
|---|---|---|---|
| `pipeline/.catalysts-cache/` directory | Exists, holds `catalysts-cache-{date}.json` per architecture §4 and news-events → market-brief wiring | **Directory does not exist** on disk under `Trade/pipeline/` | CRITICAL |
| Risk Rules pre-entry checklist gate count | Architecture §2 / `.claude/rules/risk-rules-summary.md` state "7 gates" | `framework/Risk Rules.md §7` lists **8 gates** (#8 V027 intermediary-capital sizing tier, added 2026-04-18) | HIGH |
| Today's audit-data-staging location | `Trade/2026-04-21/audit-data-staging-2026-04-21.md` (date-folder convention) | File at `Trade/audit-data-staging-2026-04-21.md` (workspace root) — convention violation | HIGH |
| Memory.md §2 Open Positions vs SignalLedger/pipeline-status | `.pipeline-status.json` trade-rec (v3, 2026-04-21 11:30) logged SPY Long +3 promoted half-size 1.0% (stop 696, target 730) | Memory.md §2 shows only P008 CLUSDT long — **no SPY row, no P009/P010**. Auto-memory index claims P008+P009+P010 — also inconsistent. Ghost-open risk | HIGH |
| Known Structural Risk #1 "numpy fragility" | Listed as HIGH unresolved risk in architecture §7 | numpy 2.4.4 imports cleanly; ResidMom logged LIVE 2026-04-17 and FALLBACK (not MISSING) 2026-04-21 — risk wording is stale | MED |
| `.pipeline-status.json` freshness | Daily routines should record `timestamp` dated 2026-04-21 after their respective fire times | Every leg (preflight, market-brief, news-events, trade-rec, positions-monitor, recovery) still dated 2026-04-20 — today's preflight-audit (19:47) has not yet updated status | MED |
| Scheduled task `lastRunAt` | All daily tasks should show `lastRunAt` after first local run | `preflight-audit-data`, `preflight-meta-additions`, `news-events-daily`, `daily-market-brief-8pm`, `trade-rec-daily`, `pipeline-recovery-daily`, `positions-monitor`, `us-close-snapshot` all lack `lastRunAt` in registry | MED |
| Today's dated outputs coverage | Expect market-brief-2026-04-21.md, news-2026-04-21.md, meta-additions-staging-2026-04-21.md in `2026-04-21/` | Only cloud-brief, methodology-sync, trade-rec, slack-digest-0810, pipeline-smoketest present; local 20:08 brief + 20:10 news + 19:58 meta-staging not yet fired (current local time 19:45) — non-critical (timing), but meta-additions-staging would block market-brief Overlay Gate if absent at 20:08 | LOW |
| `architecture.md §8` changelog completeness | Rows for each commit that changed wiring | Missing entries for commits 62ac770, 5613928, b99e66d (V015/V016 FX carry restore), 48ea6ee (FX removal + AVGO/BABA/MSFT + asset-universe-update skill), 834d1fa (methodology-sync skill added), 090dc2d (BNMA/PL-NMA integration + cloud-market-brief anchor) | MED |
| `CLAUDE.md` variable-count disagreement | `architecture.md` / `Methodology Prompt.md` reference **Top-33 variables**, V026–V035 + Overlay Gate | `Trade/.claude/CLAUDE.md` §"Authoritative Documents" still says "Top-28 variables" | MED |
| `pipeline-dependency-graph.mermaid` + `routine-output-map.md` | Marked "superseded by this file" in architecture §4 | Both still present in `pipeline/` — not deleted. Low risk but invites drift | LOW |
| master-data-log.xlsx integrity verification | Should be openable read-only | `PermissionError` — file currently held open (likely by Excel). Structural check (10 sheets, OPEN rows, AuditAdditionLog V026/V027/V028, RegimeHistory last row) **not completed** | MED (can't verify) |

---

## Broken Links 🔴

- `Trade/pipeline/.catalysts-cache/` — declared in architecture §2 (news-events), §4 (Pipeline state table), and §5 wiring for news-events + market-brief + daily-trade-rec. **Directory does not exist.**
- No `catalysts-cache-2026-04-21.json` anywhere on disk under `pipeline/`.
- No `catalysts-cache-2026-04-20.json` either — suggests the cache-write leg of news-events has been silent for ≥1 day (tracks the Known Structural Risk §7 "Catalyst cache authenticity" bullet, now manifest).

All other declared paths resolved cleanly.

---

## Orphans

**Scheduled tasks registered but not in architecture §1:**
- `monthly-bootstrap-review` (cron `0 19 1 5,6 *`, auto-disables after 2026-07-01) — transient bootstrap, should be documented with retirement date.
- `meta-shadow-review-2026-04-25` (one-time 2026-04-25 19:00 UTC+8) — Phase-3 GO/NO-GO for V029–V035 shadow.
- `weekly-backup-sunday` (cron `0 22 * * 0`) — git commit-and-push on Sunday 22:00 UTC+8.

**Scripts on disk but not in architecture §3:**
- `scripts/sync_trade_exits_2026-04-20.py` — one-off date-tagged script.
- `scripts/test_compute_audit_additions.py` — test harness.
- `scripts/test_data_contract.py` — test harness.

**Skills on disk but not clearly indexed in §4 skill table:**
- `.claude/skills/test_write/` — placeholder folder (no SKILL.md visible).

**Pipeline files still on disk despite §4 marking them superseded:**
- `pipeline/pipeline-dependency-graph.mermaid`
- `pipeline/routine-output-map.md`

---

## Action Items

- **P0 (fix now):**
  - Restore `Trade/pipeline/.catalysts-cache/` and verify news-events actually writes `catalysts-cache-{date}.json` per run — this is the Known Structural Risk made real. Without it the Overlay Gate / C-leg catalyst injection for market-brief + daily-trade-rec is running on empty.
  - Reconcile Memory.md §2 with SignalLedger + `.pipeline-status.json`. SPY Long (P009?) promoted in today's trade-rec but absent from Memory §2 → trade-update skill must be invoked to close the gap (ghost-open risk).
  - Close the open handle on `master-data-log.xlsx` (likely Excel) so openpyxl-based skills can write.

- **P1 (this week):**
  - Patch `architecture.md §2` and `.claude/rules/risk-rules-summary.md` — checklist is **8 gates**, not 7 (V027 sizing tier added 2026-04-18).
  - Patch `Trade/.claude/CLAUDE.md` — "Top-28 variables" → Top-33 (or current count).
  - Rewrite Known Structural Risk #1: numpy import is healthy; ResidMom degradation mode now FALLBACK, not MISSING. Keep as MED "compute-env single-point-of-failure" rather than HIGH unresolved.
  - Move `Trade/audit-data-staging-2026-04-21.md` into `Trade/2026-04-21/` and audit `preflight-audit-data` task / `compute_audit_additions.py` for where its write path is set — date-folder convention is being violated at the source.
  - Add §8 changelog rows for commits 090dc2d, 834d1fa, 48ea6ee, b99e66d, 5613928, 62ac770.
  - Register the 3 orphan tasks (`monthly-bootstrap-review`, `meta-shadow-review-2026-04-25`, `weekly-backup-sunday`) in architecture §1.

- **P2 (before next quarterly/system-review):**
  - Delete or relocate superseded `pipeline-dependency-graph.mermaid` + `routine-output-map.md` (or rename with `.superseded` suffix) so future readers can't drift to them.
  - Remove/retire `.claude/skills/test_write/` placeholder.
  - Move one-off scripts (`sync_trade_exits_2026-04-20.py`, `test_*.py`) to `scripts/archive/` and list test harnesses separately in architecture §3.
  - Add a health probe in `preflight_health_check.py` that fails loud if `.catalysts-cache/{today}.json` is absent at 20:05 UTC+8 — architecture Known Risk §7 bullet "Catalyst cache authenticity" currently relies on pipeline-smoketest catching it later, which missed today.

---

## Architecture Record Updates Needed

Line-level changes to `Trade/pipeline/architecture.md` (do NOT apply — list only):

1. **§2 "Risk Rules" row** → change authority summary `Pre-entry checklist (7 gates)` to `Pre-entry checklist (8 gates — incl. V027 intermediary-capital sizing tier added 2026-04-18)`.
2. **§4 Pipeline state table** → add explicit row note that `.catalysts-cache/` must exist as a directory; current state is MISSING on disk.
3. **§7 Known Structural Risks row #1 ("numpy fragility")** → downgrade severity HIGH → MED, rewrite to "compute-env fragility surfaced 2026-04-20 (all 12 T-scores MISSING for one day); market-model fallback restored 2026-04-21 (FALLBACK state)"; update "Mitigation status" to reflect restored environment.
4. **§7 Row "Catalyst cache authenticity"** → upgrade MED → HIGH and change "Mitigation status" to "CURRENTLY BREACHED — `.catalysts-cache/` directory absent 2026-04-21".
5. **§1 Execution Order** → add rows for `monthly-bootstrap-review` (transient, retires 2026-07-01), `meta-shadow-review-2026-04-25` (one-time), `weekly-backup-sunday`.
6. **§3 Scripts table** → note `test_compute_audit_additions.py` and `test_data_contract.py` as test harnesses (not production pipeline); decide whether to list `sync_trade_exits_2026-04-20.py` or move it to `scripts/archive/`.
7. **§4 Skills table** → add rows (or note omission) for `asset-universe-update` (already exists in live skills but not in the "§4 Skills" table); `test_write` placeholder — remove.
8. **§8 Changelog** → append rows for 2026-04-18 (methodology-sync skill creation), 2026-04-18 (BNMA/PL-NMA integration), 2026-04-19 (FX removed from universe; AVGO/BABA/MSFT added; asset-universe-update skill), 2026-04-20 (V015/V016 restored as FX context-only monitoring).
9. **§4 Pipeline state table** → either delete the rows for `pipeline-dependency-graph.mermaid` and `routine-output-map.md` or change "superseded by this file" to "REMOVED on {date}" once the files are actually removed.
10. **Cross-reference** `Trade/.claude/CLAUDE.md` § "Authoritative Documents" variable count (currently "Top-28") — update to match Methodology Prompt.md Top-33.

---

*End of report. Read-only — no framework, skill, Excel, or scheduled-task changes were made during this review.*
