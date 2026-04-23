---
PATCH FILE — system-review skill (NEW)
Created: 2026-04-17
Reason: /mnt/.claude/skills/ is read-only from inside this session. Gerald must manually
create the skill directory and copy the SKILL.md content below.

Install steps:
  1. Create directory: /mnt/.claude/skills/system-review/
  2. Copy the block between the BEGIN and END markers below into:
     /mnt/.claude/skills/system-review/SKILL.md
  3. Scheduled task `system-review-semi-annual` is already created and enabled
     (first Sunday of May and November, 19:00 UTC+8).
  4. On next session restart, verify the skill description appears in the
     available-skills list.
---

=========================== BEGIN SKILL.md ===========================
---
name: system-review
description: Semi-annual strategic architecture + efficiency audit of Gerald's trading system. Walks every skill, scheduled task, and workspace file; maps them to the research → trade → monitor → earn value chain; produces KEEP/MODIFY/MERGE/REMOVE verdicts using two tests (value: does it earn money; efficiency: at minimum token cost); identifies architecture gaps AND redundant token burn; ranks proposals by P&L impact or context-budget freed for the trade rec. Operates above quarterly-methodology-review (trading content), signal-review (OOS marking), and workspace-tidy (tactical hygiene) — audits whether the scaffold itself earns its keep and runs efficiently. Triggers on scheduled task `system-review-semi-annual` (first Sunday May/November, 19:00 UTC+8) and on phrases "system review", "strategic review", "audit my architecture", "optimize the system", "reduce token burn", "is the architecture working", "meta review". Not for trade recs, signal marking, or file tidying.
---

# System Review — Strategic Architecture + Efficiency Audit

Semi-annual review of the full trading scaffold. Every skill, scheduled task, and supporting file must pass two tests: (1) evidence that it moves money, protects money, or produces insight that will; AND (2) evidence that it does so at the minimum token cost needed for the decision quality. Processes that fail the first test earn REMOVE. Processes that pass the first but fail the second earn MODIFY. Unsupported recommendations fail loud.

This skill does NOT edit anything. It produces a ranked patch file. Gerald reviews, then invokes skill-creator, the schedule skill, or direct edits to implement.

---

## The two tests

For every skill, task, and supporting file, ask both:

> **Test 1 — Value:** Does this move money, protect money, or produce insight that will?
>
> **Test 2 — Efficiency:** Does it do so at the minimum cost in tokens, tool calls, and wall time — or is the same decision quality achievable for less?

A process that fails Test 1 earns REMOVE. A process that passes Test 1 but fails Test 2 earns MODIFY (tightened scope, cached inputs, shared artifacts, trimmed output, merged with a neighbour). Elegance, symmetry, and completeness are not acceptable justifications.

Token cost matters directly. Every token burned on meta-review, boilerplate re-reads, or bloated outputs is a token not available for the trade rec's reasoning budget. Efficiency here is not housekeeping — it's capacity for the decisions that earn money.

---

## Value chain

Every process maps to exactly one bucket:

1. **Research** — generate or evaluate variables, produce insight for future decisions (lit review, quarterly methodology, cores, weekly regime review)
2. **Rec-generation** — produce a trade recommendation for the next session (brief, news, preflight, audit-data, trade-rec)
3. **Execution** — act on a recommendation in the market (currently: nothing scheduled; trade-update is reactive)
4. **Monitoring** — watch live positions, catch thesis breaks, flag invalidation
5. **Post-trade review** — mark-to-market signals, review executed trades, attribute P&L (signal-review, weekly regime review)
6. **Infrastructure** — pipeline glue, recovery, archival, memory housekeeping (workspace-tidy, pipeline-recovery, consolidate-memory, us-close-snapshot)
7. **Meta-review** — audits other processes (this skill, quarterly-methodology-review, monthly-bootstrap while active)

Bucket imbalances are the headline finding of every run. A bucket with zero or one process is a structural gap unless justified.

---

## Execution — seven phases

### Phase 1 — Inventory (no interpretation)

Read and list:

- Every `SKILL.md` in `/mnt/.claude/skills/`
- Every scheduled task via `mcp__scheduled-tasks__list_scheduled_tasks` (taskId, cron, last-run, enabled)
- `/mnt/Trade/Memory.md`, `Methodology Prompt.md`, `Risk Rules.md`, `Data Sources.md`, `Coin core.md`, `Trad core.md`, `Retention Policy.md`
- `/mnt/.auto-memory/MEMORY.md` and every linked memory file
- Last 6 months of dated outputs: `market-brief-*.md`, `trade-rec-*.md`, `news-events/news-*.md`, `signal-review-*.md`, `weekly-review-*.md`, `us-close-snapshot-*.md`, `audit-data-staging-*.md`, `hypo-ledger-2026.md`
- `master-data-log.xlsx` summary: SignalLedger row count + hit rate, AuditAdditionLog, VariableRegistry, PerformanceStats
- Prior `system-review-*.md` if any
- Any unresolved `*-patch-*.md` files in `/mnt/Trade/` (drift indicator)

Output: flat inventory list. No judgments yet.

### Phase 2 — Value-chain map

Tag every skill and every scheduled task with exactly one value-chain bucket. Produce a matrix: bucket × process count. Flag:

- Any bucket with **zero** processes → structural gap
- Any bucket with **more than three** processes → potential redundancy
- Any process that **fits no bucket** → scope creep or dead weight

### Phase 3 — Per-process effectiveness and efficiency audit

For each recurring process (skill or task), answer six questions:

**Value questions (Test 1):**

1. **What did it produce in the last 6 months?** File count, ledger rows appended, memory entries, patch files.
2. **What action did Gerald take as a result?** Cite a specific ledger row, memory entry, executed trade, methodology change, or documentation edit. **No citation = no action.**
3. **What breaks if it disappears tomorrow?** Name the specific decision that loses support. "Gerald wouldn't know X" is acceptable; "we'd lose coverage" is not.

**Efficiency questions (Test 2):**

4. **Token cost per run:** estimate from input reads (files × approx length) + output length + intermediate tool calls. Express as a range (e.g., 15-25k tokens/run). Multiply by cadence to get monthly token burn.
5. **Is the output length justified by the decision it supports?** If the process produces a 3,000-token file that informs a one-line go/no-go, flag it. Output bloat is the most common efficiency leak.
6. **Are there cheaper paths to the same decision quality?** Specifically check for:
   - **Redundant reads** — same file read by multiple processes when a cached summary artifact would do (e.g., both brief and trade-rec reading the same news file in full)
   - **Stale boilerplate** — sections that restate framework that's already loaded from CLAUDE.md or authoritative docs
   - **Over-wide search** — web search with unfocused queries when targeted pulls suffice
   - **Unused output sections** — headings that appear in every run but are never referenced downstream
   - **Cadence mismatch** — running a process weekly when monthly would produce the same acted-on findings

Verdict — pick exactly one:

- **KEEP** — passes both Test 1 (acted-on output within last two cycles) and Test 2 (no obvious efficiency leak)
- **MODIFY** — passes Test 1 but fails Test 2; specify the efficiency change: narrower scope / cached input / shared artifact / trimmed output / cadence change
- **MERGE** — passes Test 1 but efficiency demands folding into another process (name target and merge rule)
- **REMOVE** — fails Test 1: no evidence of acted-on output, and no downstream process depends on its output

**Every verdict requires an evidence citation. An opinion-only verdict fails the run.**

Produce a table: process | bucket | last-acted evidence | token cost/run | monthly burn | verdict | rationale.

At the end of Phase 3, produce a **system-wide token burn estimate** (sum of monthly burn across all recurring processes) and compare to the prior cycle's estimate if available. Call out the top 3 contributors by token share.

### Phase 4 — Architecture gap and redundancy analysis

Against the earn-money aim, surface:

**Gaps (missing capability):**
- Which links in **research → rec-generation → execution → monitoring → post-trade review → earn** are thin or missing?
- What data is collected but never reviewed? (e.g., AuditAdditionLog rows that never trigger a decision; news capture entries not referenced in any trade rec)
- What failure modes have no monitor? (e.g., are Risk Rules actually being followed on actual entries vs. what the rec said)
- What decisions is Gerald currently making on feel that the system could support with structured input?
- Where does memory coverage end and improvisation start?
- Are audit-addition 6-month reviews templated for future promotions, or only hard-coded for 2026-04-14?

**Redundancy (excess capability — efficiency drag):**
- Which files are read by more than one scheduled process within the same run window? Could a shared cached artifact replace the duplicate reads?
- Which output sections are produced identically across multiple reviews (e.g., regime label, VIX-at-entry block) and could be written once and referenced?
- Which processes have overlapping triggers or scope (e.g., two processes that both mark ledger state)?
- Which processes run at a higher cadence than their acted-on output rate justifies?
- Which authoritative docs are loaded verbatim into context when a summary would suffice?

### Phase 5 — Strategic proposals

Produce four lists:

- **ADD** — new skill or scheduled task, each with: name, cadence, input it reads, output it produces, specific decision it supports, estimated token cost per run
- **REMOVE** — each with the Phase 3 evidence citation
- **MODIFY (scope)** — cadence change, scope change, merge, or replacement, each with specific before-and-after
- **MODIFY (efficiency)** — token reduction through caching, shared artifacts, trimmed output, pruned sections, or narrower search; each with estimated tokens saved per run × monthly cadence

Rank every proposal by expected impact:

- **HIGH** — plausibly worth >1% of annual returns over the next 12 months, OR frees >20% of the trade-rec context budget
- **MEDIUM** — reduces drag, improves signal quality, or saves 5-20% of the trade-rec context budget without degrading decision quality
- **LOW** — hygiene, nice-to-have, maintenance, minor efficiency wins

Efficiency gains count toward HIGH impact when they free context directly consumed by the trade-rec step. Freeing 10k tokens from the trade rec's available budget plausibly improves decision quality more than adding a new Grade-B variable. Rank accordingly.

Elegance is not an impact category. Proposals must trace to one of the two tests.

### Phase 6 — Self-audit (skip on first run only)

Read the prior `system-review-*.md`. For each proposal:

- Implemented fully? Partially? Not at all?
- If implemented, did the expected P&L impact materialize? Cite evidence from SignalLedger, PerformanceStats, or Gerald's trade log.
- If not implemented, why? Was the proposal wrong, or was it right but ignored?

**Hard self-removal rule:** if the prior two cycles have zero acted-on proposals, the first finding of this cycle is:

> **REMOVE system-review — failed own test: two consecutive cycles with zero acted-on recommendations.**

Write it as the top proposal in Phase 5. Do not soften. This skill applies the same discipline to itself that it applies to every other process.

### Phase 7 — Output

Write `/mnt/Trade/system-review-YYYY-MM-DD.md` with this structure:

1. **Headline finding** — one sentence
2. **Value-chain matrix** (Phase 2)
3. **Effectiveness + efficiency table** (Phase 3), including system-wide token burn estimate and top 3 contributors by token share
4. **Gap + redundancy list** (Phase 4), with gaps and redundancies as separate sub-sections
5. **Ranked proposals** (Phase 5) — ADD / REMOVE / MODIFY-scope / MODIFY-efficiency, each tagged HIGH / MEDIUM / LOW with evidence and (for efficiency items) estimated monthly tokens saved
6. **Efficiency tally** — total estimated tokens saved if all MODIFY-efficiency HIGH proposals are implemented; comparison vs. prior cycle if available
7. **Self-audit** (Phase 6, skip on first run)
8. **Next review date** — first Sunday of (current month + 6)

**Do not auto-apply anything.** This skill never edits skills, tasks, or files. It produces a proposal document.

At the end of the output, remind Gerald: "Adds → invoke skill-creator or schedule. Removes → delete the skill directory or disable the task. Modifies → edit via skill-creator or update via schedule."

Append a memory entry to `/mnt/.auto-memory/` recording: date, top-3 findings, top-3 proposals ranked HIGH, next review date.

---

## Scope boundaries

`system-review` does NOT:

- Audit methodology dimensions — `quarterly-methodology-review` owns that
- Mark-to-market signals or compute hit rates — `weekly-regime-signal-review` and `signal-review` own that
- Enforce file retention or archival — `workspace-tidy-sunday-9pm` owns that
- Fix pipeline failures — `pipeline-recovery-830pm` owns that
- Consolidate memory — `consolidate-memory` owns that
- Manage the variable candidate pipeline — `quarterly-methodology-review` owns that

`system-review` DOES evaluate whether **each of the above processes is earning its keep at the scaffold level**, which none of them can do for themselves.

---

## Evidence discipline

Every verdict and every proposal must cite one of:

- A specific file path and date
- A specific SignalLedger, AuditAdditionLog, or VariableRegistry row
- A specific memory entry in Memory.md or `/mnt/.auto-memory/`
- A specific prior chat log reference
- An explicit documented absence (e.g., "no SignalLedger row has referenced a lit-review-sourced variable in the last 6 months — searched 2025-10-17 through 2026-04-17")

An unsourced claim is a failed run, not a softer run.

---

## Triggers

**Scheduled:** `system-review-semi-annual` — first Sunday of May and November, 19:00 UTC+8. Cron `0 19 1-7 5,11 0`.

**On-demand phrases:** "system review", "strategic review", "review the system", "audit my skills", "audit my architecture", "optimize the system", "is the architecture working", "review my workspace strategically", "meta review".

---

## Why this skill exists

No existing skill evaluates whether the trading scaffold itself is working. `quarterly-methodology-review` evaluates methodology content. `signal-review` evaluates signal quality. `workspace-tidy` does tactical hygiene. `skill-creator` executes on-demand edits. None of them ask: given the earn-money aim, is the *architecture* — the set of skills, tasks, and supporting files — correctly shaped?

Reactive evidence that this layer is needed, from the memory index as of 2026-04-17: four task consolidations on 2026-04-16, structural-sniffs rubric enrichment on 2026-04-17, news-events 12-category taxonomy on 2026-04-17, skill-description-tightening patch blocked and carried as drift, unscheduled discovery that the scaffold has zero processes in the monitoring and execution buckets. This work is already being done reactively. A scheduled pass formalizes it and catches the drift that reactive passes miss.

============================ END SKILL.md ============================
