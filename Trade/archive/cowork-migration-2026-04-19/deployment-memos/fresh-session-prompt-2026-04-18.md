# Fresh-session prompt — continue 2026-04-18 deployment work

Copy everything below the horizontal rule into a new Cowork session. It's self-contained — don't paste the recap-in-chat, just this.

---

Context: I'm continuing the 2026-04-18 deployment from a previous session. All high-value state is captured in auto-memory (`/mnt/.auto-memory/MEMORY.md` index → individual files) and `/mnt/Trade/deployment-memo-2026-04-18.md`. Read those first before doing anything.

**Session goal: pre-stage everything that needs to be ready for 2026-04-25, so review day is one PowerShell run, not a scramble.**

Two tasks, in this order.

## Task 1 — Phase 3 SKILL.md patches (primary)

Phase 3 unblocks when the scheduled task `meta-shadow-mode-review-2026-04-25` fires Saturday 2026-04-25 10:00 UTC+8 and writes `/mnt/Trade/meta-shadow-review-2026-04-25.md` with GO/NO-GO verdicts per variable (V029, V033, V034, V035; V030/V031/V032 stay MISSING by design).

The Phase 3 action when GO verdicts arrive is: edit five SKILL.md files to read `meta-additions-staging-*.md` and honor the Step 1.5 overlay gate. Those edits should be pre-drafted now so 2026-04-25 is cheap.

**Deliverables — five patch files in `/mnt/Trade/patches/`**, named `<skill>-phase3-SKILL-patch.md`:
- `market-brief-phase3-SKILL-patch.md` — reads overlay_gate_status row from staging, surfaces gate state in the regime block, fails-loud if staging file missing
- `daily-trade-rec-phase3-SKILL-patch.md` — wires Step 1.5 between Step 1 and Step 2 (multiply-by-zero sleeve logic), reads staging for V029/V033–V035 values, logs overlay_gate_status + v027_regime_bucket + bab_sleeve_weight + dealergamma_sleeve_weight to SignalLedger
- `signal-review-phase3-SKILL-patch.md` — adds 4 new SignalLedger cols to the weekly mark-to-market aggregation
- `positions-monitor-phase3-SKILL-patch.md` — checks overlay gate state on open positions' sleeve, flags if a live position's sleeve went OFF after entry
- `quarterly-methodology-review-phase3-SKILL-patch.md` — adds V029/V033–V035 to the quarterly ledger-vs-core reconciliation loop

Use the `skill-manager` skill if it's installed (check `/mnt/.claude/skills/skill-manager/`); otherwise generate patches by hand following the same convention as `/mnt/Trade/patches/META-B5-model-tiering-patch.md`. Each patch must include: summary, before/after or full-rewrite per file, idempotent PowerShell apply block, verify block, rollback block.

**Gate for each patch:** before generating, read the current SKILL.md and identify the minimum-surface edit that achieves the Phase 3 behavior. If the edit crosses 20% of the file, switch to full rewrite. Do NOT touch sections unrelated to Phase 3.

**Do not apply these patches.** They're pre-staged. Actual apply happens 2026-04-25 after GO verdicts, and only for variables that got GO.

## Task 2 — skill-manager eval loop (secondary, only if time)

`skill-manager` (new meta-skill from 2026-04-18 session) is at `/mnt/Trade/skills-draft/skill-manager/` and packaged as `skill-manager.zip`. It shipped without running through skill-creator evals. If Task 1 completes with time to spare:

1. Use `skill-creator` to write 3 eval prompts covering backup, patch, and scaffold modes
2. Run them in-skill and baseline, capture timing
3. Grade the outputs, identify the weakest mode
4. Write one revision to the SKILL.md if something's clearly broken
5. Re-package the zip

If skill-manager hasn't been installed Windows-side yet, skip Task 2 entirely — evals require the skill to be trigger-resolvable.

## Hard rules

- Read `/mnt/.auto-memory/project_meta_integration_2026-04-18.md` and `/mnt/.auto-memory/project_skill_manager_2026-04-18.md` before starting any edits. The deployment history lives there.
- Stop at any GATE in the original plan that wasn't pre-delegated. If unclear, stop and ask.
- Never touch V001/V004 grades (already downgraded 2026-04-18), never edit SignalLedger historical rows, never change an existing scheduled task — add siblings instead.
- When Task 1 completes, write a single paragraph to `/mnt/Trade/fresh-session-outcome-YYYY-MM-DD.md` listing the 5 patch paths + the SignalLedger col-read order + any GATE questions I need to answer before 2026-04-25.

## Not in scope this session

- Do NOT apply the B.5 model-tiering patch — that's mine to run in PowerShell.
- Do NOT install skill-manager for me — that's mine to extract in PowerShell.
- Do NOT touch `compute_meta_additions.py` or the shadow output files. Those are running correctly and the 2026-04-25 review depends on them being stable.
- Do NOT change the allow-list in `skill-manager/scripts/_common.py:TRADING_SKILLS`. 11 skills, as shipped.

Start by reading the two auto-memory files, then the deployment memo, then begin Task 1 on the first skill in the list (`market-brief`). Proceed sequentially.
