# Archive Sweep Candidates — 2026-04-21

**Scope inventoried:** `Trade/` excluding `.git/`, `.claude/worktrees/` (not present), and `cowork/` (outside Trade/).

**Totals:**
- Files: **1,061**
- Size: **28.61 MB**
- `Trade/archive/` (existing legacy archive): **805 files, 13 MB** (≈76% of file count, ≈45% of size)
- Active workspace (excl. archive/): 256 files, ~15.6 MB
- Files outside `archive/` older than 14 days: **0**
- Mock/stub-header files (`[MOCK`, `[TEST`, `STUB`, `PLACEHOLDER`): **0** found anywhere
- Near-empty files (<50B) outside `archive/`: **1** (`test_write`)

**Counts by confidence:** HIGH **1** · MED **0** · LOW **2** · BLOCKED **2**

---

## 1. HIGH confidence

### 1.1 `Trade/dist-skills/zifFNfdb` — cowork temp ZIP cruft
- **Size:** 3,256 bytes
- **Mtime:** 2026-04-20 19:03
- **Why candidate:** Cowork-platform temporary filename (no extension). `file` identifies it as a ZIP archive containing `slack-ingest/SKILL.md` (uncompressed 6,502 B, which exactly matches `Trade/patches/slack-ingest-SKILL.md`). Byte-identical in size to `dist-skills/slack-ingest-v2.skill` (also 3,256 B, same mtime). Not referenced anywhere in `Trade/` or `~/.claude/scheduled-tasks/`.
- **If moved:** No broken references. It's a naming-glitch duplicate of `slack-ingest-v2.skill`.
- **Note on 14-day protection:** The "files within last 14 days" rule normally protects this; I'm escalating it to HIGH because (a) it's a one-off download artifact from a chat tool (`ziXXXXXX` is the cowork tmpfile naming pattern — the existing `archive/duplicates/2026-04-19/` has 7 similar orphans), (b) it's a bit-for-bit duplicate of a file that's already named properly, and (c) zero references. Feel free to downgrade to LOW if you want strict 14-day enforcement.
- **Target:** `Trade/.archive/2026-04-21-cowork-tmp/dist-skills/zifFNfdb`

---

## 2. MED confidence

*(none)*

---

## 3. LOW confidence

### 3.1 `Trade/2026-04-20/lit-review-prompt-intraday-volume.md`
- **Size:** 16,952 bytes
- **Mtime:** 2026-04-20 16:19
- **Why candidate:** Filename doesn't match any known producer pattern (`literature-review-{date}*.md` does match — but this is a *prompt*, not the output). Unreferenced in `Trade/` and `~/.claude/scheduled-tasks/`. Looks like the driver prompt that produced `literature-review-2026-04-20-intraday-volume.md` (the actual output) — i.e. working material, not a routine artifact.
- **If moved:** No broken references, but you may want this prompt around if you plan to re-run the literature review on a different window.
- **14-day protected.** Flagging only so you know it's an orphan.
- **Target:** `Trade/.archive/2026-04-21-orphan-prompts/2026-04-20/lit-review-prompt-intraday-volume.md`

### 3.2 `Trade/news-events/README.md`
- **Size:** 8,459 bytes
- **Mtime:** 2026-04-17 10:16
- **Why candidate:** `Trade/news-events/` is an otherwise-empty legacy directory (just the README). The README documents a `news-events` skill setup that has since been superseded by `.claude/skills/news-events/SKILL.md`. Not referenced by anything (pattern match on `news-events/README` returns zero).
- **If moved:** Directory becomes empty and harmless. No broken references.
- **14-day protected** (Apr 17 is 4 days old). Flagging only.
- **Target:** `Trade/.archive/2026-04-21-legacy-readmes/news-events/README.md`

---

## 4. BLOCKED — flagged but cannot proceed cleanly

### 4.1 `Trade/archive/` → `Trade/.archive/pre-2026-04-21-legacy/` (prompt rule #6)

- **Size:** 13 MB, 805 files, 6 top-level entries (`cleanup-log.md`, `cowork-migration-2026-04-19/`, `duplicates/`, `memory-log-2026-W16.md`, `one-offs/`, `outputs-superseded-2026-04/`)
- **Prompt directive:** explicit — rename into `.archive/pre-2026-04-21-legacy/`.
- **Why BLOCKED:** The rename collides with active tooling that writes to `archive/` (no dot). Six references across three scheduled-task SKILL.md files and one framework doc:
  - `Trade/framework/Retention Policy.md:11` — `/mnt/Trade/archive/YYYY-MM/{YYYY-MM-DD}/`
  - `Trade/framework/Retention Policy.md:13` — (long match)
  - `Trade/framework/Retention Policy.md:51` — `/mnt/Trade/archive/duplicates/YYYY-MM-DD/`
  - `Trade/framework/Retention Policy.md:70` — `/mnt/Trade/archive/cleanup-log.md`
  - `~/.claude/scheduled-tasks/workspace-tidy/SKILL.md:21,23,33` — `archive/YYYY-MM/`, `archive/cleanup-log.md`
  - `~/.claude/scheduled-tasks/setup-claude-code-routines/SKILL.md:206,208` — `archive/YYYY-MM/`, `archive/cleanup-log.md`
  - `~/.claude/scheduled-tasks/create-trading-pipeline-routines/SKILL.md:75` — long match
- **What happens if I just rename without updating docs:** The next `workspace-tidy` run will silently recreate `Trade/archive/` with a fresh `cleanup-log.md`, so you'll end up with BOTH `archive/` and `.archive/pre-2026-04-21-legacy/` coexisting — exactly the split the prompt was trying to avoid.
- **Three options — need your call:**
  - **(a) Rename + update refs**: I move `archive/` → `.archive/pre-2026-04-21-legacy/` AND update the 3 scheduled-task SKILL.md files + `framework/Retention Policy.md` to use `.archive/YYYY-MM/`, `.archive/cleanup-log.md`, etc. Clean unification.
  - **(b) Skip the rename**: Leave `Trade/archive/` where it is. Dot-prefix convention remains an aspiration; status quo continues.
  - **(c) Rename without ref updates**: Hide the legacy blob, let future tidy runs start a fresh `archive/`. Ugly but intentional split.
- **Default if you say `archive high`:** I will skip this item (option b) unless you say `archive high+rename-refs` (option a).

### 4.2 `Trade/.claude/skills/test_write` — empty file
- **Size:** 0 bytes
- **Mtime:** 2026-04-20 15:57
- **Why candidate:** Empty file, clearly a leftover from a write test.
- **Why BLOCKED:** `Trade/.claude/skills/pipeline-smoketest/SKILL.md:35` lists `test_write` as one of the 11 expected skills; today's smoketest (`2026-04-21/pipeline-smoketest-2026-04-21.md:9, 61, 74`) already flagged this as spec/reality drift and recommended "restore the skill or remove from expected-11 list." So moving it in isolation leaves the spec saying `test_write` should exist.
- **Options — need your call:**
  - **(a) Archive file + patch smoketest spec**: move `test_write` AND edit `pipeline-smoketest/SKILL.md` line 35 to drop it from the expected list (`Expected 10 skills: daily-trade-rec, …, trade-update.`). Also drop from today's smoketest log warn line.
  - **(b) Skip**: Leave both the empty file and the spec drift until you decide whether to actually author a `test_write` skill.
- **Default if you say `archive high`:** I skip this item (option b) unless you say `archive high+patch-smoketest` (option a).

---

## What I am NOT flagging (and why)

- **`Trade/bnma/`** (28 files, ~14 MB): referenced in `framework/Methodology Prompt.md` and `framework/Trad core.md`. Active research artifact. Keep.
- **`Trade/scripts/sync_trade_exits_2026-04-20.py`**: within 14 days, one-off but recent. Keep.
- **`Trade/scripts/__pycache__/`**: auto-regenerates; not worth archiving (would just reappear). Leave to .gitignore cleanup if desired.
- **`Trade/patches/slack-ingest-SKILL.md`**: within 14 days. Staging for the slack-ingest v2 patch. Keep.
- **`Trade/reviews/methodology-audit-6mo-review-2026-10-14*.md`**: referenced by `~/.claude/scheduled-tasks/methodology-audit-6mo-review-2026-10-14/SKILL.md`. Keep.
- **`Trade/dist-skills/*.skill`, `SCHEDULE-PROMPT*.md`, `COWORK-PROMPTS.md`, `DOWNSTREAM-CHANGES.md`, `slack-scheduled-updates-bundle.zip`**: within 14 days, active staging for cowork deployment. Keep.
- **All `2026-04-14` through `2026-04-21` date folders**: every file matches a producer pattern in the smoketest skill spec, and all are within 14 days. Zero orphans.
- **`Trade/.catalysts-cache/`, `Trade/.data-cache/`**: live caches (Apr 17–20 reads). Keep.
- **`Trade/framework/*`, `Trade/pipeline/*`, `master-data-log.xlsx`**: canonical production. Keep.
- **`Trade/2026-04-18`, `Trade/2026-04-19` thinness**: these date folders have only 1–2 files (no trade-rec). That's a pipeline-health concern for those days, not an orphan issue — do not archive partial routines on the theory that they're incomplete.

---

## Summary

Almost the entire workspace passes the 14-day protection rule. The sweep surfaces two small real items (`zifFNfdb`, `lit-review-prompt-intraday-volume.md` + `news-events/README.md` as LOW) and two BLOCKED items that need your explicit decision before I can proceed cleanly: the `archive/` rename (because it collides with active tooling) and the `test_write` empty file (because the smoketest spec still expects it).
