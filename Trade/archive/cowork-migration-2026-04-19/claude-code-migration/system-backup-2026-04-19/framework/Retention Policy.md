# Workspace Retention Policy

**Purpose:** keep `/mnt/Trade/` operationally concise without losing historical signal. Enforced weekly by the `workspace-tidy-sunday-9pm` scheduled task. Authored 2026-04-14.

## Tiers

**Tier 1 — Live (days 0–7):** full fidelity, lives at the root of `/mnt/Trade/`. This is the working set the session-startup reads scan.

**Tier 2 — Archive (days 8–30):** moved to `/mnt/Trade/archive/YYYY-MM/`, full content preserved, still grep-able. Not read by default but available on request.

**Tier 3 — Digest (day 31+):** originals deleted; replaced by a single monthly digest at `/mnt/Trade/archive/YYYY-MM-digest.md` containing one short block per day (regime tag, key catalysts, trade rec decision + outcome if known, and any lesson logged). **Exceptions — never digested (Tier 1 → Tier 2 only, kept in full permanently):** weekly reviews (in `archive/weekly/`), trade recs (in `archive/YYYY-MM/`), and trade-rec HTML reports (in `archive/YYYY-MM/`).

## File classification

**In scope for tiering (dated producer outputs):**
- `market-brief-YYYY-MM-DD.md` (normal Tier 1 → 2 → 3)
- `us-close-snapshot-YYYY-MM-DD.md` (normal Tier 1 → 2 → 3)
- `news-events/news-YYYY-MM-DD.md` (normal Tier 1 → 2 → 3)
- `trade-rec-YYYY-MM-DD.md` (Tier 1 → Tier 2 only; never digested — decision documents and audit trail)
- `report-YYYY-MM-DD-trade-rec.html` (Tier 1 → Tier 2 only; never digested — visual audit trail with scorecard charts)
- `weekly-review-YYYY-MM-DD.md` (Tier 1 → Tier 2 only; never digested — kept in full permanently in `archive/weekly/`)

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

**Protection rule:** if `Memory.md` references a dated file in its "Open positions" or "Active theses" section, that file is pinned — skip tiering regardless of age. The cleanup task must grep `Memory.md` for dated filename patterns before archiving/deleting anything.

**News files:** `news-events/news-YYYY-MM-DD.md` files follow the standard Tier 1 → 2 → 3 pipeline above. The `news-events/README.md` defers to this policy (no separate retention logic). Items still driving the current regime or tied to an open position are protected by the pin rule above.

## Same-day duplicates

If the tidy task finds more than one file for the same (type, date) — e.g. two `trade-rec-2026-04-14.md` variants, or a `report-2026-04-14.html` and `report-2026-04-14-full.html` — it quarantines the non-canonical siblings to `/mnt/Trade/archive/duplicates/YYYY-MM-DD/` rather than deleting.

Canonical file is selected by **most recent modification time**, not size or "completeness". Size-based heuristics are unreliable: a shorter file is often the corrected or fail-loud version, not the incomplete one. On mtime ties, the group is skipped and flagged for manual review.

Grouping uses a **date-stripped stem key**, not a fixed type prefix. The date token `YYYY-MM-DD` is removed from the filename stem and everything else — including any suffix after the date — is kept as the group key. So `report-DATE.html`, `report-DATE-full.html`, and `report-DATE-trade-rec.html` produce three distinct keys and are never collapsed into one group. Only reruns of the *same* variant (identical stripped stem) get grouped together.

Quarantined duplicates follow normal retention once they're >7 days old (moved into the monthly archive tree). The durable fix for repeated duplicates is deterministic filenames in the producer tasks so reruns overwrite — this policy is a safety net, not the primary mechanism.

## Non-scoped dated files

Dated files at workspace root that are NOT listed above under "In scope for tiering" — e.g. `audit-data-staging-*.md`, `signal-review-*.md`, `data-collection-audit-*.md`, `system-health-audit-*.md`, `skill-patches-*.md`, `workflow-*.html`, `workflow-*.md`, `workflow-*.docx` — follow a simplified rule:

- **Age < 8 days:** keep at root (may still be useful for reference).
- **Age ≥ 8 days:** archive to `archive/YYYY-MM/`. Never digest — these are one-off artifacts, not daily series.

**Exempt from this rule (always live at root):** `.skill` files, `*.py` scripts, `memory-lessons.md`, `methodology-audit-*` files, `streamlining-*.md`, and anything in the "Never truncate" list above.

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
