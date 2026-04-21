# Claude Code Port — Orchestrator Prompt

**For:** Gerald's trading research workspace (`Trade/`)
**Source:** Claude Cowork (Windows, Desktop app, scheduled tasks)
**Target:** Claude Code (CLI + cloud routines)
**Authored:** 2026-04-19 (supersedes `claude-code-migration/MIGRATION-GUIDE.md` of 2026-04-18; folds in 2026-04-17/18 updates)
**Workspace model:** single shared folder — Claude Code and Cowork both read/write the same `Trade/` directory. No file copying between systems.

---

## How to use this prompt

1. Open a fresh Claude Code session **from the `Trade/` directory**:
   ```bash
   cd Trade
   claude
   ```
2. Paste **Phase 0** into the session and wait for approval before pasting Phase 1, etc.
3. Each phase ends with a **STOP gate** — do not advance without Gerald's explicit "proceed".
4. If a step fails, STOP and report. Do not silently retry. Do not auto-advance phases.

---

## BEFORE YOU START — read this once

You are porting a live, money-touching trading system. Rules that override anything else:

- **Fail-loud on Grade-A data gaps.** Never silently infer a missing variable.
- **Append-only SignalLedger.** Never rewrite or delete existing signal rows.
- **No new trade universe.** Do not expand beyond the assets listed in `Trade/.claude/CLAUDE.md`.
- **Preserve the 8-step methodology sequence.** `Methodology Prompt.md` is authoritative; if CLAUDE.md and `Methodology Prompt.md` conflict, the authoritative doc wins.
- **This is a port, not a rewrite.** Do not redesign skills. Do not drop behavior. Do not "simplify" SKILL.md files beyond what the existing migration bootstrap already shortened.
- **Both systems run in parallel during cutover.** Cowork remains the system of record until Phase 4 completes and Gerald toggles it off.

Key context you will need, loaded lazily per phase:
- `Trade/.claude/CLAUDE.md` — project instructions (lean, targeted reads per skill)
- `Trade/claude-code-migration/MIGRATION-GUIDE.md` — full migration playbook (2026-04-18)
- `Trade/claude-code-migration/.claude/skills/*/SKILL.md` — 11 pre-ported skills in Claude Code format
- `Trade/patches/*` — pending SKILL.md patches (RM1, META-B5, phase3 meta-integration)
- `Trade/skills-draft/skill-manager.zip` — 12th skill, not yet installed
- `master-data-log.xlsx` — 9 sheets, sole structured store

---

# PHASE 0 — Inventory & reconciliation (no writes)

**Goal:** confirm the current state of the workspace, the existing migration artifacts, and the deltas since the migration guide was last updated. Produce one inventory report and a gap list. STOP for approval.

Do the following, in order:

1. **Confirm working directory.** Run `pwd`. You must be at `Trade/` (the folder containing `Methodology Prompt.md`). If you're not, STOP and ask Gerald to relaunch from the right directory.

2. **Confirm Claude Code install.** Run `claude --version` and `claude doctor` (in a separate shell, or use the CLI). Report the version and any diagnostic failures.

3. **Read these files and summarize each in one line:**
   - `.claude/CLAUDE.md`
   - `.claude/settings.json` (if present)
   - `claude-code-migration/MIGRATION-GUIDE.md`
   - `claude-code-migration/setup-claude-code.py`
   - `patches/README.md`
   - `Memory.md` §1 Regime, §2 Open Positions (for awareness of live book)

4. **Enumerate skills:**
   - List `.claude/skills/*/` (what's already present in project scope).
   - List what the setup script would install.
   - Cross-check against the authoritative 12-skill list below.

   Authoritative skill list (as of 2026-04-19):

   | # | Skill | Scope | Status |
   |---|---|---|---|
   | 1 | `market-brief` | project | existing, needs E4 patch confirmed |
   | 2 | `news-events` | project | existing, needs E4 patch confirmed |
   | 3 | `daily-trade-rec` | project | existing, needs E4 patch confirmed |
   | 4 | `pipeline-recovery` | project | existing, needs RM1 patch applied |
   | 5 | `positions-monitor` | project | existing |
   | 6 | `signal-review` | project | existing |
   | 7 | `trade-update` | project | existing (on-demand only) |
   | 8 | `literature-review` | project | existing |
   | 9 | `quarterly-methodology-review` | project | existing |
   | 10 | `system-review` | project | existing |
   | 11 | `consolidate-memory` | DELETED 2026-04-17 | **do not re-install** |
   | 12 | `skill-manager` | project or user | **new, not yet installed — packaged at `skills-draft/skill-manager.zip`** |

5. **Enumerate scheduled tasks** that must become Claude Code routines. Authoritative list from `auto-memory/reference_pipeline.md` plus 2026-04-18 meta-integration additions:

   Daily (Mon–Fri, UTC+8):

   | Time | Task ID | Produces |
   |---|---|---|
   | 07:30 | `us-close-snapshot` | `us-close-snapshot-YYYY-MM-DD.md` |
   | 09:00 | `positions-monitor` | `positions-monitor-YYYY-MM-DD.md` (silent-when-OK) |
   | 19:45 | `preflight-audit-data` | `audit-data-staging-YYYY-MM-DD.md` + `.pipeline-health.json` |
   | 19:52 | `preflight-meta-additions` | `meta-additions-staging-YYYY-MM-DD.md` (shadow mode until 2026-04-25) |
   | 20:00 | `market-brief` | `market-brief-YYYY-MM-DD.md` |
   | 20:00 | `news-events` | `news-events/news-YYYY-MM-DD.md` + catalysts cache |
   | 21:00 | `trade-rec` | `trade-rec-YYYY-MM-DD.md` + HTML + SignalLedger append |
   | 22:00 | `pipeline-recovery` | recovery files if upstream failed |

   Weekly (Sunday, UTC+8):

   | Time | Task ID | Produces |
   |---|---|---|
   | 18:00 | `weekly-regime-signal-review` | `weekly-review-*.md` + `signal-review-*.md` + PerformanceStats |
   | 21:00 | `workspace-tidy` | archive moves + consolidate-memory + diagnostics |

   Quarterly / semi-annual / one-time:

   | Schedule | Task ID | Purpose |
   |---|---|---|
   | 19:00 1st of Jan/Apr/Jul/Oct | `quarterly-methodology-review` | meta-review + VariableRegistry |
   | 15:00 1st of Jan/Jul | `semi-annual-literature-review` | academic factor scan |
   | 19:00 1st Sun of May/Nov | `system-review-semi-annual` | architecture + efficiency audit |
   | 19:00 1st of May/Jun | `monthly-bootstrap-review` | bootstrap health check, auto-disable Jul 1 |
   | 10:00 2026-04-25 | `meta-shadow-mode-review` | one-time Phase 3 GO/NO-GO per V029–V035 |
   | 2026-10-14 | `methodology-audit-6mo-review` | 3-audit-variable keep/demote |

   **Count: 15 routines total** (8 daily + 2 weekly + 5 infrequent). Note: Pro plan caps at 5/day, Max at 15/day, Team/Enterprise at 25/day. Gerald needs at least Max to run all 8 daily routines in the cloud; otherwise some must stay as Desktop scheduled tasks.

6. **Delta check against migration guide.** The 2026-04-18 guide predates these changes:

   - **2026-04-17 E1** — read-override prepends landed on scheduled tasks; routine prompts below already include the override.
   - **2026-04-17 E4** — catalysts cache helper live; `market-brief`, `news-events`, `daily-trade-rec` SKILL.md files already patched. Verify in Phase 1.
   - **2026-04-17 RM1** — `pipeline-recovery` content-failure patch pending (audit-addition drift check). File: `patches/RM1-pipeline-recovery-SKILL-patch.md`.
   - **2026-04-17** — `consolidate-memory` folder deleted; do not recreate.
   - **2026-04-17 residual-mom** — `scripts/fetch_ff5_from_french_library.py`, `scripts/preflight_health_check.py`, `scripts/test_data_contract.py`, and `audit-data-missing-tracker.md` are new and must be included in any repo commit.
   - **2026-04-18 meta-integration** — V029–V035 + Step 1.5 added to `Methodology Prompt.md`, `Risk Rules.md`, `Data Sources.md`, `Trad core.md`; VariableRegistry 29→36 rows; SignalLedger 32→36 cols; new script `scripts/compute_meta_additions.py`. Phase 3 SKILL.md edits **blocked** pending 2026-04-25 shadow review — do not apply yet.
   - **2026-04-18 skill-manager** — new 12th skill at `skills-draft/skill-manager.zip`.
   - **2026-04-18 Part B.5 model tiering** — patch at `patches/META-B5-model-tiering-patch.md` not yet applied.

7. **Write a Phase 0 report** (inline, do not save a file yet) covering:
   - CWD + Claude Code version
   - Skills already present vs. expected (diff table)
   - Patches pending apply (list file paths)
   - Routines already set up in Claude Code (run `/schedule list` if you have any) vs. the 15 expected
   - GitHub repo status for `Trade/` — is it initialized? is there a remote?
   - Any blockers for proceeding to Phase 1

8. **STOP.** Ask Gerald: "Phase 0 inventory complete. Proceed to Phase 1 (install skills + apply pending patches)?" Wait for explicit "yes, proceed".

---

# PHASE 1 — Install skills + apply patches (local writes only, no commits)

**Goal:** `.claude/skills/` contains the 11 live skills (with all current patches applied) plus `skill-manager` as the 12th. `.claude/CLAUDE.md`, `.claude/settings.json`, and `.claude/rules/` are current.

**Guardrails:**
- **Do NOT apply the META Phase 3 SKILL.md edits.** Those are gated on the 2026-04-25 shadow review. If you're running after 2026-04-25 and Gerald has signed off on Phase 3, apply them separately in a Phase 1b sub-prompt; do not assume sign-off.
- **Do NOT recreate `consolidate-memory`.** It was deliberately deleted on 2026-04-17.
- **Do NOT overwrite existing SKILL.md files without diffing first.** The `.claude/skills/` folder may already contain the latest live versions from Cowork. Diff before writing.

Steps:

1. **Verify `.claude/` skeleton is present.** If `.claude/CLAUDE.md` or `.claude/settings.json` is missing, run:
   ```bash
   python3 claude-code-migration/setup-claude-code.py
   ```
   The script is idempotent — it SKIPs existing files. Report which files it created and which it skipped.

2. **Diff each existing SKILL.md against the bootstrap-script version** for the 11 core skills. For any differences:
   - If the on-disk version is newer (e.g. contains catalysts_cache references, RM1 audit drift check, etc.), **keep the on-disk version** — it's the live one.
   - If the on-disk version is older and the bootstrap version is the newer canonical one, overwrite with the bootstrap version.
   - Report every decision in a table: `Skill | On-disk status | Bootstrap status | Action taken`.

3. **Apply the RM1 patch** to `pipeline-recovery/SKILL.md`:
   - Read `patches/RM1-pipeline-recovery-SKILL-patch.md` — it describes a prepend + Step 4f + Step 5 CRITICAL escalation.
   - If the patch is already applied (grep for `audit-addition variable drift` or similar marker), SKIP and note idempotency.
   - If not, apply and leave a `# RM1 applied 2026-04-19` marker comment.

4. **Apply the B.5 model-tiering patch** (if present and not already applied):
   - Read `patches/META-B5-model-tiering-patch.md`.
   - It sets `model: haiku|sonnet|opus` in the frontmatter of each SKILL.md per the tiering table. If frontmatter already has the right model, skip.

5. **Apply any other phase3/phase-prefixed patches in `patches/`** that are NOT gated on the 2026-04-25 review. Read each patch file's header to determine gating. If gated, skip and list as pending.

6. **Install skill-manager (12th skill):**
   - Source: `skills-draft/skill-manager.zip` (18.4 KB, 10 files per auto-memory).
   - Unzip into `~/.claude/skills/skill-manager/` (user scope) so it's available across projects:
     ```bash
     unzip skills-draft/skill-manager.zip -d ~/.claude/skills/skill-manager
     ```
     Windows PowerShell equivalent:
     ```powershell
     Expand-Archive -Path skills-draft\skill-manager.zip -DestinationPath $env:USERPROFILE\.claude\skills\skill-manager
     ```
   - If Gerald prefers project scope, unzip to `.claude/skills/skill-manager/` instead.
   - Verify `SKILL.md` exists at the unpacked root and frontmatter `name: skill-manager` is valid.

7. **Verify the trimmed CLAUDE.md** (`.claude/CLAUDE.md`) matches the source at `Trade/.claude/CLAUDE.md` exactly — they must be identical since Claude Code and Cowork share the same workspace. If they drift, align to `Trade/.claude/CLAUDE.md` (the Cowork-visible one is authoritative because Gerald edits that).

8. **Verify `.claude/settings.json`** contains:
   - All required Bash allowlist entries for every script in `scripts/` (including the 2026-04-17 and 2026-04-18 additions: `fetch_ff5_from_french_library.py`, `preflight_health_check.py`, `test_data_contract.py`, `compute_meta_additions.py`, `cache_manager.py`, `catalysts_cache.py`).
   - The PostToolUse hook for trade-rec SignalLedger reminder.
   - Deny list includes `Bash(rm -rf *)` and `Bash(sudo *)`.

9. **Fix Python script paths** — one-time sed:
   - Linux/Mac:
     ```bash
     find scripts/ -name "*.py" -exec sed -i 's|/mnt/Trade/|./|g' {} +
     ```
   - Windows PowerShell:
     ```powershell
     Get-ChildItem scripts -Filter *.py -Recurse | ForEach-Object {
         (Get-Content $_.FullName) -replace '/mnt/Trade/','./' | Set-Content $_.FullName
     }
     ```
   - Idempotent — run safely.

10. **Run smoke test:** `python3 scripts/test_data_contract.py`. All 26 tests must pass. If any fail, STOP and report.

11. **Write a Phase 1 report:** skills present now (should be 11 + skill-manager = 12), patches applied, patches skipped (Phase 3 meta), test contract result, any drift detected.

12. **STOP.** Ask: "Phase 1 complete. Proceed to Phase 2 (convert scheduled tasks → routines)?"

---

# PHASE 2 — Convert scheduled tasks → Claude Code routines

**Goal:** 15 routines created at claude.ai/code/routines (or via `/schedule` CLI), each pointing at the `Trade/` GitHub repo, with the correct cron, model tier, prompt, and environment.

**Critical constraints:**
- Routines run on fresh git clones. **Every routine prompt must end with a git commit + push step** or the next routine won't see the prior routine's output.
- Enable **Allow unrestricted branch pushes** on the repo so routines push to `main` instead of `claude/*` branches (otherwise the daily chain is broken).
- The repo must be **private** — it contains methodology, open positions, and the signal ledger.
- Minimum routine interval = 1 hour. All cron times are in Gerald's local zone (UTC+8).
- Jitter: up to ~6 min on hourly schedules. The 1-hour gap between brief (20:00) and trade-rec (21:00) absorbs this.
- `trade-update` is **event-driven only** — do NOT schedule it.

Steps:

1. **Pre-check GitHub repo state.**
   - Run `git status` and `git remote -v`.
   - If no remote, STOP and ask Gerald to create a private GitHub repo and run:
     ```bash
     git init  # if not already
     echo ".data-cache/" > .gitignore
     git add -A && git commit -m "Port to Claude Code — 2026-04-19"
     git remote add origin https://github.com/<user>/trading-system.git
     git push -u origin main
     ```
   - If remote exists, confirm it's private (gh CLI: `gh repo view --json isPrivate`). If public, STOP — do not push methodology or Memory.md to a public repo.

2. **Confirm plan tier.** Gerald needs **Max** (15/day) or higher for the 8 daily routines. If on Pro (5/day cap), flag and recommend: keep `positions-monitor` and `pipeline-recovery` as Desktop scheduled tasks (local), route the other 6 daily tasks to cloud routines.

3. **Set up shared cloud environment** at claude.ai/code/routines → Environments → New:
   - **Name:** `trading-system-env`
   - **Network access:** `Trusted` (allows WebSearch for variable pulls)
   - **Setup script:** `pip install openpyxl requests pandas numpy`
   - **Environment variables:** any API keys Gerald's scripts need (FRED, etc. — leave blank if not used)

4. **Create the 15 routines** using the table below. Create them via `/schedule` CLI or claude.ai/code/routines web UI. After creating, run `/schedule list` to verify all 15 are registered.

   Every prompt template below ends with:
   ```
   Then git add -A, commit with message "routine: <name> <today>", and push to origin main.
   ```
   This is required — omit it and the next routine won't see the outputs.

   ### Daily routines (Mon–Fri, UTC+8)

   | # | Name | Cron | Model | Prompt |
   |---|------|------|-------|--------|
   | 1 | `us-close-snapshot` | `30 7 * * 1-5` | sonnet | `CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Do NOT read Methodology Prompt.md, Coin core.md, Trad core.md, or protocol documents. Read ONLY: Memory.md §2 Open Positions and the latest market-brief-*.md. For each open position, pull US close + any after-hours earnings reaction via WebSearch. Write us-close-snapshot-{today}.md with mark-to-market, >1σ ATR moves, AH earnings. Update .pipeline-status.json. Then commit + push.` |
   | 2 | `positions-monitor` | `0 9 * * 1-5` | haiku | `/positions-monitor` + commit + push |
   | 3 | `preflight-audit-data` | `45 19 * * 1-5` | sonnet | `Run scripts/preflight_health_check.py to write .pipeline-health.json. Then run scripts/compute_audit_additions.py to produce audit-data-staging-{today}.md. If compute fails, consult .data-cache/ for cached inputs within staleness windows per Data Sources.md §4-tier fallback and retry. Update audit-data-missing-tracker.md per RM1. Commit + push.` |
   | 4 | `preflight-meta-additions` | `52 19 * * 1-5` | sonnet | `Run scripts/compute_meta_additions.py to produce meta-additions-staging-{today}.md in shadow mode (V029 BAB, V030 DealerGamma, V031 GP/A, V032 CEI, V033–V035 Faber TAA). Log each variable's status to AuditAdditionLog (Type=SHADOW). Do NOT feed results into market-brief or trade-rec — shadow mode only until 2026-04-25 review. Commit + push.` |
   | 5 | `market-brief` | `0 20 * * 1-5` | sonnet | `/market-brief` + commit + push |
   | 6 | `news-events` | `0 20 * * 1-5` | sonnet | `/news-events` + commit + push |
   | 7 | `trade-rec` | `0 21 * * 1-5` | opus | `/daily-trade-rec` + commit + push. If the trade-rec mentions "no changes since prior rec" (Step 0 delta-check), still commit + push any Memory.md or .pipeline-status.json updates. |
   | 8 | `pipeline-recovery` | `0 22 * * 1-5` | haiku | `/pipeline-recovery`. If Phase A returns healthy, exit fast with no file writes. If unhealthy, proceed to Phase B. Commit + push only if files were created. |

   ### Weekly routines (Sunday, UTC+8)

   | # | Name | Cron | Model | Prompt |
   |---|------|------|-------|--------|
   | 9 | `weekly-regime-signal-review` | `0 18 * * 0` | opus | `Phase 1: Read Memory.md, latest market-brief-*.md, all news-events/news-*.md from the past 7 days. Write weekly-review-{today}.md with regime trajectory, key events, thesis validation, lessons. Condense memory-lessons.md entries. Phase 2: /signal-review. Commit + push all changes.` |
   | 10 | `workspace-tidy` | `0 21 * * 0` | haiku | `CRITICAL: utility task, do NOT follow CLAUDE.md §Session Startup Protocol. Apply Retention Policy.md: move files aged 8+ days to archive/YYYY-MM/; digest files aged 31+ days. Respect Memory.md pinned files. Run diagnostics (Excel integrity, pipeline liveness, output continuity, cache health, skill presence). Append to archive/cleanup-log.md. Commit + push.` |

   ### Quarterly / semi-annual / one-time

   | # | Name | Cron | Model | Prompt |
   |---|------|------|-------|--------|
   | 11 | `quarterly-methodology-review` | `0 19 1 1,4,7,10 *` | opus | `/quarterly-methodology-review` + commit + push |
   | 12 | `semi-annual-literature-review` | `0 15 1 1,7 *` | opus | `/literature-review` + commit + push |
   | 13 | `system-review-semi-annual` | `0 19 1-7 5,11 0` | opus | `First Sunday of May and November at 19:00 UTC+8 (cron filter: day 1–7 AND day-of-week=0). /system-review + commit + push.` |
   | 14 | `monthly-bootstrap-review` | `0 19 1 5,6 *` | sonnet | `Bootstrap health check: are all routines firing? Are skills producing valid output? Check git log for recent routine commits. Report status. If today's date ≥ 2026-07-01, print "auto-disable" and take no action (Gerald will disable manually). Commit + push.` |
   | 15 | `meta-shadow-mode-review` | One-time trigger: fire 2026-04-25 10:00 UTC+8 (create as `0 10 25 4 *` and disable after firing) | opus | `Read all meta-additions-staging-*.md files from 2026-04-20 to 2026-04-24. For each of V029-V035: report contribution rate, any decision-moving instances, whether to PROMOTE to live (Phase 3 GO), HOLD in shadow, or RETIRE. Cross-check against 2026-04-18 deployment memo. Write meta-shadow-review-2026-04-25.md with per-variable verdict. Commit + push.` |
   | 16 | `methodology-audit-6mo-review` | One-time: `0 10 14 10 *` (auto-disable after firing) | opus | `Six-month review of 3 audit-addition variables (residual mom, intermediary capital, basis-momentum). Read AuditAdditionLog and audit-data-missing-tracker.md. Per variable: days LIVE, decision-moving contributions, contribution rate normalized by days LIVE. Verdict: KEEP Grade A / DEMOTE to B / REMOVE. Write methodology-audit-6mo-review-2026-10-14.md. Commit + push.` |

   **⚠ Cron semantics check — routine #13 (`system-review-semi-annual`).** The expression `0 19 1-7 5,11 0` assumes AND-semantics between DOM (`1-7`) and DOW (`0`) — i.e., "day 1–7 AND Sunday" = first Sunday of May/Nov. Under classic Vixie cron (OR-semantics) it would fire every day 1–7 of May/Nov PLUS every Sunday of May/Nov — far too often. Claude Code's routine cron parser's DOM+DOW behavior is not documented. Verify on first fire (expected: 2026-05-03 19:00 UTC+8). If it misfires under OR-semantics, replace with two monthly routines gated by an in-prompt "is today a Sunday?" check:
   - `0 19 1-7 5 *` with prompt preamble: "If today is not Sunday, exit silently. Otherwise /system-review + commit + push."
   - `0 19 1-7 11 *` with same preamble.

5. **Decide: cloud routines vs Desktop scheduled tasks.**

   If Gerald is on Max: all 16 go to cloud routines.
   If Gerald is on Pro: cloud routines cap is 5/day. Recommend split:
   - **Cloud (5 daily):** preflight-audit-data, market-brief, news-events, trade-rec, pipeline-recovery
   - **Desktop (3 daily):** us-close-snapshot (morning check), positions-monitor (machine on), preflight-meta-additions (shadow)
   - All weekly + quarterly + one-time: cloud (low daily cost)

6. **Verify one routine end-to-end.** Pick `preflight-audit-data` (lowest risk, reads-heavy, minimal writes). Click **Run now** in the web UI. Watch the session. Confirm:
   - It clones the repo.
   - It runs the compute script.
   - It writes `audit-data-staging-{today}.md` and `.pipeline-health.json`.
   - It commits + pushes to `main`.
   - The next `git pull` on the local workspace shows the new files.

   If any step fails, STOP. Do NOT proceed to activate the rest of the routines.

7. **Parallel-run window (3 business days).** Leave Cowork scheduled tasks enabled. Every day for 3 days, diff Cowork's and Claude Code's outputs (`diff trade-rec-{today}-cowork.md trade-rec-{today}.md`). Expected: identical or near-identical. Discrepancies → STOP, investigate before cutover.

8. **STOP.** Ask: "Phase 2 complete, 1 routine verified end-to-end. Proceed to Phase 3 (CLAUDE.md + settings.json final alignment) or hold for parallel-run period?"

---

# PHASE 3 — CLAUDE.md + settings.json + rules final alignment

**Goal:** the `.claude/` directory is the single source of truth for Claude Code, kept perfectly in sync with what Cowork sees under `.claude/` in the same workspace. No drift.

Steps:

1. **Verify CLAUDE.md parity.** `Trade/.claude/CLAUDE.md` is the version Cowork reads. `Trade/claude-code-migration/.claude/CLAUDE.md` is what the migration bootstrap writes. They must be identical or any behavioral rule change will split between the two systems. Run `diff` — if they differ, copy the live Cowork one over the migration-bundled one.

2. **Verify `.claude/rules/evidence-grades.md` and `.claude/rules/risk-rules-summary.md`** have correct `globs:` frontmatter so they load only for trading output files. Expected globs:
   - `evidence-grades.md`: `["market-brief-*.md", "trade-rec-*.md", "signal-review-*.md", "weekly-review-*.md"]`
   - `risk-rules-summary.md`: `["trade-rec-*.md", "report-*-trade-rec.html"]`

3. **Verify `.claude/settings.json`** covers every script under `scripts/`. Run `ls scripts/*.py` and cross-check each against the Bash allowlist (currently `python3 *` covers all, so this is usually a no-op — just confirm the wildcard is present).

4. **Commit and push** the `.claude/` directory to the repo so routines see it on next clone. (Routines cannot see local-only changes.)
   ```bash
   git add .claude/ && git commit -m "claude-code: port .claude/ to repo" && git push
   ```

5. **STOP.** Ask: "Phase 3 complete. Proceed to Phase 4 (verification + cutover)?"

---

# PHASE 4 — Verification + cutover

**Goal:** confirm every skill, every routine, and every data path works. Then disable Cowork scheduled tasks.

Steps:

1. **Verify skills discoverable.** Run `/help` in Claude Code. Confirm 12 skills listed (11 + skill-manager). Run `/status` (shows model + account). Run `/memory` (shows auto-memory path). Report the auto-memory path so Gerald can copy `.auto-memory/*.md` files over if desired.

2. **Bootstrap verification.** Paste the prompt from `claude-code-migration/MIGRATION-GUIDE.md` §5 Step 6 (enumerates 8 checks: CLAUDE.md, skills, framework files, xlsx sheets, scripts, test_data_contract, .data-cache, news-events/README). Run it. Any MISSING → STOP and fix before cutover.

3. **End-to-end live-fire test on one trading day.** Pick a Monday. Let all 8 daily routines fire in sequence. At end-of-day, confirm:
   - `market-brief-{today}.md` written and sensible
   - `news-events/news-{today}.md` written
   - `trade-rec-{today}.md` written (or "no-change" comment appended)
   - `report-{today}-trade-rec.html` written if any signals
   - SignalLedger has new rows (or documented no-new-signal)
   - `audit-data-staging-{today}.md` exists
   - `meta-additions-staging-{today}.md` exists (shadow)
   - Pipeline recovery either no-op (healthy) or wrote expected recovery files
   - Git log shows 7–8 commits from today's routines

4. **Compare against Cowork output for the same day.** Should match within rounding. Material disagreement → STOP, investigate.

5. **Cutover checklist (only after 3+ clean parallel-run days):**
   - [ ] Disable Cowork scheduled tasks (pause, don't delete — rollback insurance for 2 weeks)
   - [ ] Leave Cowork skills installed (fallback invocation path)
   - [ ] Update `auto-memory/reference_pipeline.md` to note "migrated to Claude Code routines 2026-MM-DD"
   - [ ] Add auto-memory project entry documenting the port

6. **Rollback plan** (if needed):
   - Pause or delete routines at claude.ai/code/routines
   - Re-enable Cowork scheduled tasks
   - All workspace files are shared — no data to migrate back
   - Git history preserves every routine's changes for forensics

7. **Final report.** Summarize:
   - Skills ported: 12
   - Routines created: 16
   - Scripts path-fixed: count
   - Patches applied: list (RM1, B.5, E1/E4-confirmed)
   - Patches deferred: list (Phase 3 meta-integration, gated on 2026-04-25)
   - Parallel-run diffs: summary
   - Open issues / follow-ups

---

## Appendix A — Common gotchas

1. **Routines see only committed files.** If you update a SKILL.md locally and don't push, the next routine run uses the old version from the last `git push`. Always commit + push after Phase 1/3 changes.

2. **Skill invocation syntax is `/skill-name` in Claude Code**, not "run the skill". Inside a routine prompt, either `/skill-name` or a direct task description works; prefer `/skill-name` for clarity and token efficiency.

3. **Fresh clone per routine run** means `.data-cache/` starts empty each run. The cache gets rebuilt on the first preflight run of the day. If `.data-cache/` is in `.gitignore` this is expected; if it's committed (should not be), strip it from tracking.

4. **`allowed-tools` in SKILL.md frontmatter** pre-approves tools so Claude Code doesn't prompt. If a skill errors with "permission denied" during a routine run, add the tool to the SKILL.md frontmatter (not `settings.json` — `settings.json` doesn't apply inside cloud routines).

5. **The 2026-04-18 V001/V004 A→B downgrade is already in `Methodology Prompt.md`.** Do not reapply. If you notice V001 or V004 still at Grade A somewhere, check if that source file was committed before 2026-04-18 and diff against the live version.

6. **Do not trigger `meta-shadow-mode-review` before 2026-04-25.** It will have no shadow-run data to review. The cron `0 10 25 4 *` fires once on 2026-04-25 10:00 UTC+8. After it fires, pause or delete it.

7. **The `trade-update` skill is event-driven.** Do NOT create a routine for it. Gerald invokes it interactively via `/trade-update` when he enters/exits a position.

8. **`consolidate-memory` was deleted 2026-04-17.** Its functionality moved into the weekly `workspace-tidy` routine. Do not create a routine or skill folder for it.

9. **Jitter tolerance.** Brief at 20:00 and trade-rec at 21:00 leaves 60 min for brief to complete + jitter. If brief jitters to 20:06 and runs 40 min, trade-rec at 21:00 still sees it. Tighter gaps risk race conditions.

10. **Daily routine cap.** If Gerald hits the plan cap mid-day, the remaining routines silently drop (or pend to next day on some plans). `pipeline-recovery` at 22:00 is the safety net — it detects missed upstream runs.

---

## Appendix B — Files this prompt reads / may modify

**Reads only (never modifies):**
- `Methodology Prompt.md`, `Risk Rules.md`, `Data Sources.md`, `Coin core.md`, `Trad core.md`, `Retention Policy.md`, `Excel-Sync-Protocol.md`, `Trade-Execution-Protocol.md`
- `Memory.md` (read in Phase 0 for awareness; updates happen via skills, not this prompt)
- `master-data-log.xlsx`
- `auto-memory/*.md`
- `news-events/README.md`
- All files under `patches/`, `skill-patches/`, `skill-updates/`, `skill-backups/`
- `claude-code-migration/MIGRATION-GUIDE.md` + `setup-claude-code.py`

**May create / modify:**
- `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/rules/*.md`, `.claude/skills/*/SKILL.md`
- `~/.claude/skills/skill-manager/` (user scope for skill-manager)
- `scripts/*.py` (path sed fix only, no logic changes)
- Git state (`git init`, `git add`, `git commit`, `git push`)
- Routines at claude.ai/code/routines (create/update only, never delete without asking)

**Never modifies:**
- Any dated producer output (`market-brief-*.md`, `trade-rec-*.md`, `news-events/news-*.md`, `signal-review-*.md`, etc.)
- SignalLedger rows (append-only, and only via the daily-trade-rec skill)
- Authoritative framework docs (Methodology Prompt, Risk Rules, Data Sources, cores)
- Memory.md (skills own this)

---

## Appendix C — References

- Claude Code routines: https://code.claude.com/docs/en/web-scheduled-tasks
- Claude Code plugins: https://code.claude.com/docs/en/discover-plugins
- Announcement: https://claude.com/blog/introducing-routines-in-claude-code
- Migration guide (local): `claude-code-migration/MIGRATION-GUIDE.md`
- Bootstrap script (local): `claude-code-migration/setup-claude-code.py`
- Authoritative pipeline: `auto-memory/reference_pipeline.md`
- Authoritative methodology: `Methodology Prompt.md`

---

**End of orchestrator prompt.** The Claude Code session should now have four phase prompts it can execute sequentially, each with a STOP gate for Gerald's approval. Total port time estimated 60–90 minutes of active work across 3–5 business days (with parallel-run window).
