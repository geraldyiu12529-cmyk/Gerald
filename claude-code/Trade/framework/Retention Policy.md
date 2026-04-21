# Workspace Retention Policy

**Purpose:** keep `/mnt/Trade/` operationally concise without losing historical signal. Enforced weekly by the `workspace-tidy-sunday-9pm` scheduled task. Authored 2026-04-14.

## Tiers

**Date-folder convention (effective 2026-04-19):** dated outputs now live under `{YYYY-MM-DD}/` at workspace root, one folder per local UTC+8 date. The **folder** is the retention unit — move, archive, and digest by folder, not by individual file. Legacy root-level dated files (produced before 2026-04-19) are folded into `archive/YYYY-MM/{YYYY-MM-DD}/` during Tier 2 migration.

**Tier 1 — Live (days 0–7):** full fidelity. Today's folder lives at `/mnt/Trade/{YYYY-MM-DD}/`. This is the working set the session-startup reads scan.

**Tier 2 — Archive (days 8–30):** entire date folder moved to `/mnt/Trade/archive/YYYY-MM/{YYYY-MM-DD}/`, full content preserved, still grep-able. Not read by default but available on request.

**Tier 3 — Digest (day 31+):** the date folder is deleted after its contents are folded into a single monthly digest at `/mnt/Trade/archive/YYYY-MM-digest.md` (one short block per day: regime tag, key catalysts, trade rec decision + outcome if known, any lesson logged). **Exceptions — never digested (Tier 1 → Tier 2 only, kept in full permanently):** weekly reviews (moved to `archive/weekly/{YYYY-MM-DD}/` preserving the whole Sunday folder), trade recs, and trade-rec HTML reports (both preserved inside `archive/YYYY-MM/{YYYY-MM-DD}/`). When the rest of the date folder would otherwise be digested but these never-digest artifacts remain, keep the `{YYYY-MM-DD}/` folder in place inside the monthly archive and prune only the digestable files from it.

## File classification

**In scope for tiering (dated producer outputs, now inside `{YYYY-MM-DD}/` folders):**
- `{YYYY-MM-DD}/market-brief-{YYYY-MM-DD}.md` (normal Tier 1 → 2 → 3)
- `{YYYY-MM-DD}/us-close-snapshot-{YYYY-MM-DD}.md` (normal Tier 1 → 2 → 3)
- `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` (normal Tier 1 → 2 → 3) — legacy `news-events/news-YYYY-MM-DD.md` path is swept in during Tier 2 migration
- `{YYYY-MM-DD}/daily-{YYYY-MM-DD}.md` (normal Tier 1 → 2 → 3 — consolidated pack target)
- `{YYYY-MM-DD}/trade-rec-{YYYY-MM-DD}.md` (Tier 1 → Tier 2 only; never digested — decision documents and audit trail)
- `{YYYY-MM-DD}/report-{YYYY-MM-DD}-trade-rec.html` (Tier 1 → Tier 2 only; never digested — visual audit trail with scorecard charts)
- `{YYYY-MM-DD}/weekly-review-{YYYY-MM-DD}.md` (Tier 1 → Tier 2 only; never digested — kept in full permanently in `archive/weekly/{YYYY-MM-DD}/`)
- `{YYYY-MM-DD}/signal-review-{YYYY-MM-DD}.md` + `{YYYY-MM-DD}/report-{YYYY-MM-DD}-signal-review.html` (Tier 1 → Tier 2 only; never digested)
- `{YYYY-MM-DD}/quarterly-methodology-review-{YYYY-MM-DD}.md`, `{YYYY-MM-DD}/literature-review-{YYYY-MM-DD}[-scope].md`, `{YYYY-MM-DD}/system-review-{YYYY-MM-DD}.md` (+ `.html`) — all permanent (never digested)

**Never truncate, never archive — always live at root:**
- `Memory.md`, `Methodology Prompt.md`, `Risk Rules.md`, `Data Sources.md`
- `Coin core.md`, `Trad core.md`
- Any future numbered research docs (e.g. `01 - …`, `02 - …`) if created
- `Retention Policy.md` (this file)
- `master-data-log.xlsx` — the master analytical data store (accumulates time-series data, signal ledger, variable registry; NEVER archive or delete)
- `Excel-Sync-Protocol.md` — defines how skills sync to the workbook
- `*.skill` files
- Any subfolder `README.md`

**Never digest — Tier 1 → Tier 2 only (full content preserved permanently):**
- `trade-rec-YYYY-MM-DD.md` — decision documents and audit trail for methodology review
- `report-YYYY-MM-DD-trade-rec.html` — visual audit trail; scorecard charts, gap-closure evidence, audit-addition status panels
- `weekly-review-YYYY-MM-DD.md` — (already specified above in File classification; kept in full at `archive/weekly/`)

**Rationale:** Trade recs and their HTML reports are the primary evidence base for the 2026-10-14 six-month audit review and any future methodology reviews. Digesting them after 30 days would destroy the scored scorecards, gap-closure doughnuts, and audit-addition contribution evidence that the review process depends on. Storage cost is low (~50–100 KB per pair per day, ~3.5 MB/month); the cost of losing the audit trail is high.

**Protection rule:** if `Memory.md` references a dated file in its "Open positions" or "Active theses" section, pin the **entire date folder** containing that file — skip tiering regardless of age. The cleanup task must grep `Memory.md` for dated filename patterns (both `{YYYY-MM-DD}/<file>` and legacy root-level `<file>-YYYY-MM-DD.md`) before archiving/deleting anything.

**News files:** `{YYYY-MM-DD}/news-{YYYY-MM-DD}.md` follows the standard Tier 1 → 2 → 3 pipeline above. The `news-events/README.md` (12-category taxonomy spec) lives permanently at `news-events/README.md` and is outside the tiering system. Items still driving the current regime or tied to an open position are protected by the pin rule above.

## Same-day duplicates

If the tidy task finds more than one file for the same (type, date) — e.g. two `trade-rec-2026-04-14.md` variants, or a `report-2026-04-14.html` and `report-2026-04-14-full.html` — it quarantines the non-canonical siblings to `/mnt/Trade/archive/duplicates/YYYY-MM-DD/` rather than deleting.

Canonical file is selected by **most recent modification time**, not size or "completeness". Size-based heuristics are unreliable: a shorter file is often the corrected or fail-loud version, not the incomplete one. On mtime ties, the group is skipped and flagged for manual review.

Grouping uses a **date-stripped stem key**, not a fixed type prefix. The date token `YYYY-MM-DD` is removed from the filename stem and everything else — including any suffix after the date — is kept as the group key. So `report-DATE.html`, `report-DATE-full.html`, and `report-DATE-trade-rec.html` produce three distinct keys and are never collapsed into one group. Only reruns of the *same* variant (identical stripped stem) get grouped together.

Quarantined duplicates follow normal retention once they're >7 days old (moved into the monthly archive tree). The durable fix for repeated duplicates is deterministic filenames in the producer tasks so reruns overwrite — this policy is a safety net, not the primary mechanism.

## Non-scoped dated files

Dated files that are NOT listed above under "In scope for tiering" — e.g. `{YYYY-MM-DD}/data-collection-audit-*.md`, `{YYYY-MM-DD}/system-health-audit-*.md`, `{YYYY-MM-DD}/skill-patches-*.md`, and any legacy root-level `audit-data-staging-*.md`, `workflow-*.html`, `workflow-*.md`, `workflow-*.docx` — follow a simplified rule:

- **Age < 8 days:** keep at the current location (inside today's date folder, or at root for legacy pre-2026-04-19 files).
- **Age ≥ 8 days:** archive the containing date folder to `archive/YYYY-MM/{YYYY-MM-DD}/`. For legacy root-level files, archive individually to `archive/YYYY-MM/{YYYY-MM-DD}/`. Never digest — these are one-off artifacts, not daily series.

**Exempt from this rule (always live at root, never moved into a date folder):** `.skill` files, `*.py` scripts, `memory-lessons.md`, `methodology-audit-*` files, `streamlining-*.md`, and anything in the "Never truncate" list above.

## Cleanup log

Every run appends to `/mnt/Trade/archive/cleanup-log.md`:
- Run timestamp
- Files moved to archive (old path → new path)
- Files digested + deleted (with digest destination)
- Files skipped due to pin rule
- Phase 3 diagnostics summary table (Excel, pipeline, continuity, cache, skills, disk)
- Any errors or ambiguous cases flagged for manual review

## Recovery window

Because Tier 2 preserves full content for 30 days, any misclassification caught within a month is fully recoverable. Only Tier 3 deletes originals — and only after content has been folded into the monthly digest.

## Change control

Amendments to this policy should be dated and logged at the bottom of this file. Do not let producer tasks (daily brief, trade rec, etc.) silently add their own retention logic — keep cleanup centralized in the weekly tidy task.

## Changelog

- 2026-04-14: initial policy.
- 2026-04-15: trade-rec and HTML report files promoted to never-digest (Tier 1 → Tier 2 only, kept in full permanently). Rationale: these are the primary evidence base for the 2026-10-14 six-month audit review and future methodology reviews; digesting them after 30 days would destroy scored scorecards, gap-closure evidence, and audit-addition contribution data.
- 2026-04-15: Added explicit news-file clause — news files follow the standard Tier 1 → 2 → 3 pipeline. The `news-events/README.md` now defers to this policy (separate retention logic removed to prevent conflicts).
- 2026-04-16: Added non-scoped dated file rule — artifacts not in the tiering list (audit-data-staging, signal-review, workflow-*, etc.) archive at ≥8 days. Added Phase 3 diagnostics to cleanup log format (Excel integrity, pipeline liveness, output continuity, cache health, skill presence, disk usage).
- 2026-04-19: **Date-folder convention adopted.** All dated outputs now live under `{YYYY-MM-DD}/` at workspace root (one folder per local UTC+8 date). Retention unit is the folder, not individual files. Tier 2 migration moves the whole folder to `archive/YYYY-MM/{YYYY-MM-DD}/`. Legacy root-level dated files (pre-2026-04-19) are swept into the corresponding `archive/YYYY-MM/{YYYY-MM-DD}/` bucket during tidy. Pin rule pins the entire containing folder. `news-events/README.md` clarified as the 12-category spec (not a dated output) and lives permanently at `news-events/README.md`.
