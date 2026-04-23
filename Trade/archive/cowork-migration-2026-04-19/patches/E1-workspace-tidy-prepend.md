# E1 Patch — workspace-tidy-sunday-9pm read-override prepend

**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\Scheduled\workspace-tidy-sunday-9pm\SKILL.md`

**Action:** Paste the block below at the **very top** of the file, above all existing content. Save. Done.

**Estimated savings:** ~30–50K tokens per run × 4 fires/month = ~120–200K tokens/month freed.

**Why prepend-only and not full rewrite:** This task has a detailed 3-phase workflow (archival, memory consolidation + diagnostics, Excel/pipeline/cache/disk checks). Blind rewriting from the sandbox risks losing nuance. A prepend is additive and zero-risk.

---

## Paste this block at the top of the file

```
**CRITICAL: This is a weekly hygiene + diagnostics utility task, NOT a trading decision question. Do NOT follow the CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, Risk Rules.md, Data Sources.md, or any authoritative framework doc unless a specific phase below requires it. Do NOT pre-load the latest market-brief or trade-rec. The files required for each phase are listed inline within the phase — read only those.**

**Reads per phase (fresh, task-owned — NOT session startup):**
- Phase 1 (archival): `/mnt/Trade/Retention Policy.md` + directory listings only.
- Phase 2 (memory / doc audit): `/mnt/Trade/Memory.md`, `/mnt/.auto-memory/MEMORY.md`, and any memory-lessons file. Authoritative doc size audit is a file-stat operation — do NOT read the docs themselves.
- Phase 3 (integrity / liveness): `master-data-log.xlsx` via xlsx skill + `.pipeline-status.json` + `.data-cache/retrieval-log.jsonl` only.

Do not read anything outside these lists unless a phase result specifically triggers a deeper investigation.

---
```

---

## How to apply

1. Open `C:\Users\Lokis\Documents\Claude\Scheduled\workspace-tidy-sunday-9pm\SKILL.md` in any text editor.
2. Move cursor to the very beginning of the file.
3. Paste the block above.
4. Save and close.

Next scheduled run (Sunday 2026-04-19 21:00 UTC+8) will pick it up automatically.

## Verification

After the next fire, check:
- `/mnt/Trade/archive/2026-04/` still received the week's archival moves per Retention Policy.
- `cleanup-log.md` (or equivalent) was updated.
- Token consumption dropped from ~43K baseline to ~8–14K.

If any phase breaks or misses a file, revert by deleting the prepend block. Zero lossy edits.
