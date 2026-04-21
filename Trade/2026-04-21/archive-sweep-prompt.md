# Archive Sweep Prompt

Paste into a Claude Code session started in `T.system/Trade/`. Model: Opus max.

---

You are doing a one-pass **archive sweep** of the T.system trading workspace to label unused files and folders without breaking anything live. Work deliberately — do not rush.

## Canonical workspace and off-limits trees

- **Canonical:** `T.system/Trade/` (where you're running). Only touch things here.
- **OFF-LIMITS — do not read, rename, move, or edit:**
  - `T.system/cowork/` (Anthropic Cowork platform writes here live)
  - `T.system/Trade/.claude/worktrees/` (git worktrees — git expects these paths)
  - `T.system/Trade/.git/` (obvious)
  - Anything outside `T.system/Trade/`

## Archive convention

- Target: `T.system/Trade/.archive/{YYYY-MM-DD}-{category}/` where `{YYYY-MM-DD}` is today and `{category}` is a short slug you choose per batch (e.g. `mock-outputs`, `superseded-scripts`, `dead-framework-docs`).
- Move, don't delete. Preserve directory structure inside the archive folder so it can be restored with `mv` later.
- If `Trade/.archive/` doesn't exist, `mkdir -p` it. Leading dot hides it from `ls`.

## What IS a candidate for archiving

Flag any of:
1. **Mock / test / stub files** — contents start with `[MOCK`, `[TEST`, `TEST RUN`, `STUB`, `PLACEHOLDER`, or have headers claiming dates/runs that don't match mtime.
2. **Superseded artifacts** — older duplicates of a doc whose newer version clearly replaces it (e.g. two `framework/*.md` files where one explicitly says "supersedes the other").
3. **Orphan outputs** — files in `{YYYY-MM-DD}/` folders that don't match any producer pattern from the scheduled tasks (see list below).
4. **Empty or near-empty files** (< 50 bytes, no content).
5. **Files older than 60 days that are not referenced by any active SKILL.md, CLAUDE.md, or scripts/**.
6. **The existing `Trade/archive/` directory** — rename it to `Trade/.archive/pre-2026-04-21-legacy/` (the old archive, now unified under the dot-prefix convention).

## What is NOT a candidate (keep as-is, no matter how old)

- Any file referenced by a SKILL.md in `.claude/skills/*/` or `~/.claude/scheduled-tasks/*/`
- Any file referenced by `scripts/*.py`
- `framework/Memory.md`, `master-data-log.xlsx`, `pipeline/*`
- `.data-cache/`, `.catalysts-cache/` (live caches)
- Any file written within the last 14 days
- `SignalLedger` entries or anything the trading system reads at runtime
- Anything in `.claude/settings*.json` or `.mcp.json`

## Known producer patterns (for orphan detection)

A file in `{YYYY-MM-DD}/` is NOT an orphan if it matches one of:
- `market-brief-{date}.md`, `cloud-market-brief-{date}.md`
- `news-{date}.md`, `cloud-news-{date}.md`, `slack-digest-{date}.md`
- `trade-rec-{date}.md`, `cloud-trade-rec-{date}.md`, `report-{date}-trade-rec.html`
- `audit-data-staging-{date}.md`, `meta-additions-staging-{date}.md`
- `positions-monitor-{date}.md`, `us-close-snapshot-{date}.md`
- `daily-{date}.md`, `pipeline-recovery-{date}.md`
- `weekly-review-{date}.md`, `signal-review-{date}.md`, `report-{date}-signal-review.html`
- `quarterly-methodology-review-{date}.md`, `literature-review-{date}*.md`
- `system-review-{date}.md` + `.html`
- `pipeline-smoketest-{date}.md`

Anything else in a date folder → candidate orphan. Flag, don't auto-move.

## Process (in order — do not skip)

### Phase 1 — Inventory (read-only)

Walk `Trade/` (depth unlimited, but skip off-limits). For every file, record: path, size, mtime, first ~200 bytes (for mock-detection), whether it's referenced by any `.md`/`.py`/`.json` under active paths.

Reference check: `grep -r "filename" Trade/.claude/skills Trade/scripts Trade/framework ~/.claude/scheduled-tasks` before marking as unused.

### Phase 2 — Candidate report

Write `Trade/.archive/{today}-sweep-candidates.md` with:
- One section per category (mocks / superseded / orphans / empty / stale)
- For each file: path, size, mtime, why it's a candidate, what would happen if moved
- **Explicit confidence rating** per file: HIGH / MED / LOW
- Total counts at top

Stop here. Do NOT move anything yet.

### Phase 3 — Await approval

Print a one-line summary: `Sweep candidates: {N} HIGH-confidence, {M} MED, {K} LOW. Review Trade/.archive/{today}-sweep-candidates.md — reply 'archive high' / 'archive high+med' / 'specific list' / 'abort' to proceed.`

### Phase 4 — Move (only after approval)

Only move files the user approved. Preserve relative structure inside the archive folder. Log every move into `Trade/.archive/{today}-sweep-moves.log` as `{from} → {to}`.

### Phase 5 — Verify

After moves:
- `git status` (show what changed)
- Re-run the workspace anchor check from `pipeline-smoketest` skill
- Grep for any broken references in active skills/scripts that point at now-moved files. Flag immediately — do NOT silently break the pipeline.

## Hard rules

- Never `rm`. Only `mv`.
- Never touch off-limits trees.
- If you are unsure about a file, mark it LOW confidence and leave it.
- If a scheduled task is mid-run (check `pipeline/.pipeline-status.json` mtime within last 5 minutes), abort and retry later.
- Commit nothing. User will review and commit manually.

Begin with Phase 1. Report scope (file count, total size) before starting Phase 2.
