# Deployment Prompt — Paste into Claude Cowork

Copy everything between the `===` markers into a fresh Cowork session.

===

You are deploying two coordinated changes to Gerald's trading workspace at `/mnt/Trade/`. Read both plan documents IN FULL before editing any file. Do not skim. Authoritative plans:

1. **Meta-analysis integration** — `/mnt/Trade/meta-analysis-integration-plan-2026-04-18.md`
2. **Token-savings optimization** — summarized below; no separate plan file, so follow the rules in this prompt exactly.

Follow the session-startup protocol in `/mnt/.claude/CLAUDE.md` first (read auto-memory index, Methodology Prompt, latest market brief, Memory.md). Then execute the work below in the stated phase order. Stop at every gate marked **[GATE]** and wait for my explicit approval before continuing.

---

## PART A — Meta-analysis integration (follow the plan file)

Execute Phase 1, 2, 3, 4 in order per `/mnt/Trade/meta-analysis-integration-plan-2026-04-18.md` §4. Do not skip phases. Do not reorder. At each phase gate, print:
- Files changed (with one-line description each)
- Files deferred to a later phase
- Any finding that contradicts the plan (if you see one, STOP and ask; do not silently deviate)

**Phase 1 — Documentation** (no live impact, safe to execute without further approval):
- Patch `Methodology Prompt.md`: add V029–V035 to the Top-30 variable list; insert new Step 1.5 Overlay Regime Gate between Step 1 and Step 2; add the bucket-nomenclature crosswalk appendix; add the four new scoring rule lines.
- Patch `Risk Rules.md`: add V027 sizing tier rule; add C009 Faber drawdown circuit-breaker; add R-group scale-consistency rule; add BAB/DealerGamma sleeve-sizing rule.
- Patch `Data Sources.md`: add BAB, DealerGamma, GP/A, CEI, C009 Faber-SMA rows with source, frequency, fallback chain.
- Patch `Trad core.md`: add mechanism + evidence entries for BAB (Frazzini-Pedersen 2014), DealerGamma (Barbon-Buraschi 2021), GP/A (Novy-Marx 2013), CEI (Daniel-Titman 2006), C009 Faber TAA (Faber 2007).
- Append a dated `MethodologyNotes` sheet entry in `master-data-log.xlsx` pointing to the integration plan. Use `Excel-Sync-Protocol.md` for column mappings — read it before writing.

**[GATE 1]** — Print full diff summary. Wait for my approval before Phase 2.

**Phase 2 — Data pipeline** (blocking for live scoring):
- Extend `scripts/compute_audit_additions.py` (or create `scripts/compute_meta_additions.py` if cleaner) to fetch BAB ETF proxy (USMV/SPLV), GP/A (Ken French library), CEI (self-compute CRSP+Compustat), DealerGamma (SqueezeMetrics — ASK ME IF SUBSCRIPTION IS ACTIVE BEFORE CODING THE PULL), Faber-SMA (Yahoo monthly closes).
- Wire into `preflight-audit-data-1945pm` scheduled task. Verify fail-loud prints `MISSING — [sources attempted]` when upstream fails.
- Add VariableRegistry rows V029–V035 with `live_date` empty, `review_date = 2026-10-14`.
- Run pipeline in SHADOW MODE for 5 consecutive weekdays — values computed and surfaced in the daily market-brief but NOT scored into SignalLedger. Do not shortcut this shadow window.

**[GATE 2]** — Show the 5-day shadow-mode pipeline health. If any Grade-A pull hit MISSING more than once across the 5 days, STOP and escalate. Wait for my approval before Phase 3.

**Phase 3 — Live scoring**:
- Update `market-brief` SKILL.md, `daily-trade-rec` SKILL.md, `signal-review` SKILL.md, `positions-monitor` SKILL.md, `quarterly-methodology-review` SKILL.md per integration plan §3.6.
- Set `live_date` on V029–V035 to the date of the first live rec.
- First trade-rec under the new framework must include a header note: "First rec under 2026-04-18 meta-integration — V029–V035 live".

**[GATE 3]** — Print the first post-live trade-rec for my review before scheduled execution continues.

**Phase 4 — 2026-10-14 audit review** (calendar entry only now; work executes on that date).

---

## PART B — Token-savings optimization (with three modifications)

The original recommendation claimed 44–51% reduction. My verification cut that to 30–40% after applying three safety modifications. Apply those modifications — do not follow the claim verbatim.

**B.1 — Remove mandatory startup reads from `/mnt/.claude/CLAUDE.md`, but ONLY for these skills:**
- `news-events` — skip Methodology Prompt + Memory.md. (News capture doesn't score.)
- `pipeline-recovery` — skip everything except `.pipeline-health.json` on healthy-path runs.
- `positions-monitor` — skip cores + Data Sources; read Memory.md §2 only.

**B.2 — KEEP mandatory reads for these skills (DO NOT remove):**
- `market-brief` — keep Methodology Prompt + Data Sources + Memory.md. The scorecard and fail-loud rule depend on them.
- `daily-trade-rec` — keep all four startup reads. The 8-step synthesis is where bad reasoning costs real money.
- `signal-review` — keep Methodology Prompt + Memory.md + SignalLedger read.

Each skill's SKILL.md must explicitly enumerate its required reads in its own frontmatter or opening section. Do not rely on CLAUDE.md to enforce this.

**B.3 — Skill instruction shrinkage (157KB → 34KB goal):**
- Walk each of the 11 custom trading skills (consolidate-memory, daily-trade-rec, literature-review, market-brief, news-events, pipeline-recovery, positions-monitor, quarterly-methodology-review, signal-review, system-review, trade-update).
- For each, identify boilerplate that can be extracted to a shared rules file (e.g., `/mnt/Trade/.claude/rules/`) and globbed in per file pattern.
- Do NOT remove operational steps, fail-loud discipline, or evidence-grade citation rules. Those stay.
- Target: ≥50% byte reduction per skill. Accept smaller reductions where rules are truly skill-specific.

**B.4 — Path-scoped rule files:**
- Extend `/mnt/Trade/.claude/rules/` with rules files that declare `globs: [...]` frontmatter matching only the files they apply to.
- Existing examples: `risk-rules-summary.md` and `evidence-grades.md`. Use the same pattern.

**B.5 — Model tiering (REVISED from original claim):**
- `pipeline-recovery` healthy-path → Haiku. Safe — pure JSON + file-exists checks.
- `positions-monitor` → **Sonnet, NOT Haiku.** (Original claim used Haiku; rejected. Positions-monitor does ATR math and catalyst-proximity checks on live positions. A Haiku miscount = missed stop = one losing trade that swamps months of token savings.)
- `news-events`, `market-brief` → Sonnet.
- `daily-trade-rec`, `signal-review`, `quarterly-methodology-review`, `system-review` → Opus.
- `trade-update` → Sonnet (ledger sync needs discipline but no novel reasoning).

**[GATE 4]** — Before applying Part B, print a before/after byte count per SKILL.md and a table of which skills gain/lose which mandatory reads. Wait for my approval before writing any changes.

---

## Coordination rules between Part A and Part B

- **Do Part A first, then Part B.** Part A writes new operational content into SKILL.md files (market-brief, trade-rec, signal-review, etc.); Part B then shrinks those same files. Running Part B first would force rewrites.
- **Do not combine commits.** One commit per phase. One commit per skill in Part B.3. This keeps rollback surgical if something breaks live production.
- **Fail-loud discipline survives all shrinkage.** If any proposed token-save removes a fail-loud line, a Grade-A citation rule, or a pre-entry checklist item, stop and escalate. These are load-bearing.
- **SignalLedger is append-only. Never rewrite existing rows.** If any refactor touches the ledger schema, add columns — do not modify existing ones without a migration plan I approve.

## Expected outputs

- A diff summary per phase gate.
- A post-deployment memo at `/mnt/Trade/deployment-memo-2026-04-18.md` listing: files changed, token baseline before, projected savings, deferred items, and any discovered risks.
- An auto-memory `project_*.md` entry capturing the deployment event.

## What NOT to do

- Do not deploy Part B's skip-logic on `market-brief` or `daily-trade-rec`. (This was the biggest overclaim in the original recommendation.)
- Do not use Haiku for anything that does math on live positions.
- Do not rename S/T/C/R bucket codes. The SignalLedger depends on them.
- Do not promote any DEPLOY_CONDITIONAL variable to DEPLOY without the 2026-07-01 or 2026-10-14 review gate.
- Do not add any crypto on-chain variable to live scoring (V012, V013, V015, V016, V017, V019 remain EXCLUDE/WATCH per meta).
- Do not skip a phase gate, even if the next phase looks trivial.

If any instruction in this prompt contradicts `/mnt/Trade/meta-analysis-integration-plan-2026-04-18.md`, the plan wins. If it contradicts `Methodology Prompt.md` or `Risk Rules.md`, STOP and ask me.

Begin with the session-startup protocol, then read both plans in full, then print a one-page pre-flight summary of what you're about to do. Wait for my approval before touching any file.

===

Paste ends here. Save any longer follow-up instructions as a reply in the same Cowork thread.
