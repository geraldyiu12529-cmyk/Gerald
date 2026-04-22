# Plugin Recommendation: PDF Viewer / Productivity / Data / Engineering / Finance

## Context

Gerald runs a sophisticated, evidence-graded trading pipeline with 10 skills, 16+ scheduled routines, and a strict methodology. The system handles: daily market briefs + trade recs (markdown outputs), a 10-sheet Excel workbook (master-data-log.xlsx), Python data-retrieval scripts, and semi-annual academic literature reviews. The question is whether enabling the 5 listed plugins would improve skill efficacy or prompt efficiency.

This is a **research/recommendation** deliverable — no code changes are needed.

---

## Findings: How Each Plugin Maps to the System

### 1. Finance — **ENABLE (Highest Priority)**

**Why it helps:**
- The biggest recurring pipeline problem is MISSING Grade A variables. The 2026-04-19 brief had 5 MISSING: `NFCI`, `ACM_TP_10Y`, `BTC_3mBasis`, `Revision_Breadth`, `Pct_Above_200DMA`.
- A Finance plugin with real-time market data, rates, or financial ratios could directly plug these holes — reducing `STALE-WARN` and `MISSING` flags in market-brief and trade-rec.
- The daily pipeline currently runs a 4-tier retrieval fallback (LIVE → STALE-OK → STALE-WARN → MISSING). An additional data source at Tier 1 improves uptime of Grade A variables.
- Skills that benefit: `market-brief`, `daily-trade-rec`, `signal-review`, `positions-monitor`.

**Caveat:** Value depends on what data the Finance plugin actually exposes. If it's a calculator rather than a market-data source, the benefit is low. Test on one brief cycle.

---

### 2. PDF Viewer — **ENABLE**

**Why it helps:**
- The `literature-review` skill (semi-annual) reads academic papers from SSRN, NBER, and working-paper repositories. WebSearch returns HTML excerpts, not full paper content — leading to surface-level variable assessments.
- PDF Viewer enables direct reading of full papers, improving depth of the 5-criteria screening (peer-reviewed, replicated, coherent mechanism, independent, real-time implementable) and McLean-Pontiff decay estimates.
- Also benefits `quarterly-methodology-review` when it references cited studies.
- The `anthropic-skills:pdf` skill is already in scope — the PDF Viewer plugin may activate richer inline rendering (images, tables in papers), complementing the skill.

**Note:** Impact is twice-yearly for literature-review, but paper-reading quality directly determines what variables enter the VariableRegistry as candidates.

---

### 3. Data — **CONDITIONAL ENABLE (read-only use only)**

**Why it might help:**
- The system uses a 10-sheet Excel workbook with strict append-only writes (Excel-Sync-Protocol.md) and custom openpyxl scripts. A Data plugin could improve ad-hoc exploration — slicing SignalLedger, querying DailyVariables, or running quick aggregations without writing Python.
- Useful for `signal-review` (13 analytical dimensions) and `quarterly-methodology-review` (variable pipeline stats).

**Critical risk:** The Excel-Sync-Protocol.md enforces strict append-only rules and sheet-by-sheet write gates. A generic Data plugin used for writes could bypass these guardrails and corrupt the SignalLedger (append-only, never overwrite). `anthropic-skills:xlsx` already provides safe write paths.

**Recommendation:** Enable, but restrict use to **read/query/analysis only**. All writes to master-data-log.xlsx must continue through the skill-driven openpyxl path.

---

### 4. Productivity — **SKIP**

**Why it doesn't add value:**
- The pipeline already has 16+ scheduled routines in Claude Code with UTC+8 crons, dependency ordering, phase-A/B recovery, and consecutive-failure escalation.
- A generic Productivity plugin (calendar/task management) would overlap without integrating with the existing `.pipeline-status.json` + scheduled-tasks infrastructure.
- Adding a parallel task-management layer creates sync risk (two sources of truth for pipeline state).

---

### 5. Engineering — **SKIP (for now)**

**Why it doesn't add value now:**
- The system's bottleneck is data quality and methodology fidelity, not code authoring speed.
- Python scripts (`data_retrieval_engine.py`, `compute_audit_additions.py`, etc.) are already written and maintained. Claude Code's Bash tool handles execution.
- Engineering plugin becomes relevant if Gerald expands the scripting surface significantly (e.g., building new data connectors post-2026-04-25 meta-review).
- Revisit at the 2026-10-04 system review if Python infrastructure grows.

---

## Priority Order

| Plugin      | Verdict          | Primary Skill Beneficiary                          | Impact Frequency |
|-------------|------------------|----------------------------------------------------|-----------------|
| Finance     | Enable           | market-brief, daily-trade-rec, positions-monitor   | Daily           |
| PDF Viewer  | Enable           | literature-review, quarterly-methodology-review    | Semi-annual / quarterly |
| Data        | Conditional      | signal-review, quarterly-methodology-review        | Weekly / quarterly |
| Productivity | Skip            | N/A                                                | —               |
| Engineering | Skip (revisit)  | N/A                                                | —               |

## Verification

After enabling Finance and PDF Viewer:
1. Run `market-brief` on next pipeline cycle and compare MISSING Grade A count vs. 2026-04-19 baseline (5 MISSING).
2. At next literature review, run one paper through PDF Viewer and confirm full-text extraction vs. WebSearch excerpt.
3. If Data plugin is enabled, test a read-only query on SignalLedger and confirm no accidental writes occurred (check Excel-Sync-Protocol.md compliance).
