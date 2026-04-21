# Skill description tightening patch — 2026-04-17

## Context

Anthropic's official skill authoring spec caps the `description` frontmatter field at **1024 characters**. Four of Gerald's custom skills were at ≥91% of that limit and four more at ≥68%, leaving little headroom and adding unnecessary token weight to the pre-loaded system prompt (every skill's description is loaded at session start, on every session).

**Source of limit:** <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>

> `description`: Must be non-empty. Maximum 1024 characters. Cannot contain XML tags.

## Why this patch exists as a file, not a direct edit

`/mnt/.claude/skills/` is mounted read-only in this session (same blocker as the news-events lit-review patch on the same date). Gerald applies these edits from the write-enabled side.

## Summary table

| Skill | Before | After | Saved | After %limit | Triggers preserved |
|---|---:|---:|---:|---:|---:|
| daily-trade-rec | 962 | 770 | 192 | 75% | 8/8 + 2 refs |
| xlsx *(stock)* | 945 | 773 | 172 | 75% | 4/4 |
| literature-review | 936 | 818 | 118 | 80% | 10/10 + 1 ref |
| trade-update | 934 | 859 | 75 | 84% | 26/26 |
| docx *(stock)* | 787 | 693 | 94 | 68% | 7/7 |
| quarterly-methodology-review | 776 | 723 | 53 | 71% | 11/11 + 1 ref |
| signal-review | 730 | 700 | 30 | 68% | 11/11 + 2 refs |
| pipeline-recovery | 703 | 604 | 99 | 59% | 12/12 + 1 ref |
| **TOTAL** | **6773** | **5940** | **833** | | **89 triggers + 7 refs, all preserved** |

**Note on stock skills (xlsx, docx).** These ship with Anthropic's document-creation skill set. Editing them locally risks being overwritten on a future Anthropic update. Recommend: apply the Gerald-authored skills now; leave xlsx/docx alone unless you want to fork them.

## How to apply

For each skill below, replace the `description:` value in the frontmatter of `/mnt/.claude/skills/<skill>/SKILL.md` with the "New" block. Everything outside the frontmatter is unchanged.

After applying, verify with:

```bash
python3 -c "
import re, pathlib
for s in ['daily-trade-rec','literature-review','trade-update','quarterly-methodology-review','signal-review','pipeline-recovery','xlsx','docx']:
    p = pathlib.Path(f'/mnt/.claude/skills/{s}/SKILL.md').read_text()
    m = re.search(r'^---\n(.*?)\n---', p, re.DOTALL)
    d = re.search(r'^description:\s*(.+?)(?=\n(?:name|type|[a-z_]+):|\Z)', m.group(1), re.DOTALL|re.MULTILINE).group(1).strip()
    print(f'{s:32s} {len(d):4d}/1024')
"
```

---

## 1. daily-trade-rec  (962 → 770)

**Path:** `/mnt/.claude/skills/daily-trade-rec/SKILL.md`

**Old:**
```
Produce a pre-open trade recommendation for Gerald's trading workspace by synthesising the day's market brief, news capture, US close snapshot, and weekly regime review through the 8-step evidence-graded methodology and the binding Risk Rules pre-entry checklist. Automatically logs every promoted and near-miss signal to the SignalLedger sheet in `master-data-log.xlsx` for out-of-sample performance tracking. Use this skill whenever the user asks for a "trade rec", "trade recommendation", "pre-open rec", "daily rec", "trade synthesis", or asks Claude to "run the 8-step", "score the book", or "tell me what to trade today", even if they don't name the file. Also use when the scheduled task `daily-trade-recommendation-820pm-v2` fires. When the user asks to close fail-loud Grade-A data gaps before deciding, this skill also runs the web-search closure pass. Not for generic market commentary — use the market-brief or news-events skills/workflows for those.
```

**New:**
```
Produces Gerald's pre-open trade recommendation by synthesising the day's market brief, news capture, US close snapshot, and weekly regime review through the 8-step evidence-graded methodology and Risk Rules pre-entry checklist. Logs every promoted and near-miss signal to the SignalLedger sheet in `master-data-log.xlsx` for out-of-sample tracking. Also closes fail-loud Grade-A data gaps via web search when asked. Use when Gerald says "trade rec", "trade recommendation", "pre-open rec", "daily rec", "trade synthesis", "run the 8-step", "score the book", or "tell me what to trade today", even without naming the file. Also triggers on scheduled task `daily-trade-recommendation-820pm-v2`. Not for generic market commentary — use market-brief or news-events instead.
```

**Preserved:** 8 trigger phrases · `master-data-log.xlsx` · `daily-trade-recommendation-820pm-v2` · 4 upstream inputs · 8-step + Risk Rules · SignalLedger · fail-loud Grade-A web search · disambiguation vs market-brief/news-events. Third-person voice (Anthropic style).

---

## 2. xlsx  (945 → 773)  *[stock skill — apply only if forking]*

**Path:** `/mnt/.claude/skills/xlsx/SKILL.md`

**Old:**
```
Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like "the xlsx in my downloads") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
```

**New:**
```
Use whenever a spreadsheet is the primary input or output: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (adding columns, formulas, formatting, charts, cleaning messy data); create a new spreadsheet from scratch or from other sources; or convert between tabular formats. Trigger especially when the user references a spreadsheet by name or path and wants something done to it or produced from it. Also trigger for restructuring messy tabular data (malformed rows, misplaced headers, junk data) into proper spreadsheets. Deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.
```

**Preserved:** file extensions (.xlsx, .xlsm, .csv, .tsv) · primary-deliverable gate · disambiguation (Word/HTML/Python/DB/Google Sheets) · messy-data restructuring trigger. **Cut:** the "even casually (like 'the xlsx in my downloads')" illustrative aside — trigger still fires on file-path references without it.

---

## 3. literature-review  (936 → 818)

**Path:** `/mnt/.claude/skills/literature-review/SKILL.md`

**Old:**
```
Semi-annual systematic scan of academic finance literature for new tradeable variables. Searches working papers and published journals for factors meeting the five inclusion criteria (peer-reviewed, replicated, mechanism-grounded, independent, real-time implementable), assesses them against Gerald's existing framework gaps, and writes structured candidate proposals for the variable pipeline. Use this skill whenever the user asks for a "literature review", "lit review", "new variables", "academic scan", "paper scan", "factor scan", "what's new in the research", "any new factors", "scan for new signals", or "research update". Also use when the scheduled task `semi-annual-literature-review` fires. This is NOT the quarterly methodology review (use quarterly-methodology-review for that) — this specifically searches for NEW variables outside the current framework, while the quarterly review evaluates variables already inside it.
```

**New:**
```
Semi-annual scan of academic finance literature for new tradeable variables. Searches working papers and journals for factors meeting five inclusion criteria (peer-reviewed, replicated, mechanism-grounded, independent, real-time implementable), assesses them against Gerald's framework gaps, and writes structured candidate proposals for the variable pipeline. Use when the user asks for a "literature review", "lit review", "new variables", "academic scan", "paper scan", "factor scan", "what's new in the research", "any new factors", "scan for new signals", or "research update". Also triggers on scheduled task `semi-annual-literature-review`. NOT the quarterly methodology review (use quarterly-methodology-review) — this searches for NEW variables outside the framework; quarterly evaluates those already inside.
```

**Preserved:** 10 trigger phrases · 5 inclusion criteria · `semi-annual-literature-review` · disambiguation vs quarterly-methodology-review.

---

## 4. trade-update  (934 → 859)

**Path:** `/mnt/.claude/skills/trade-update/SKILL.md`

**Old:**
```
On-demand skill that keeps Memory.md, master-data-log.xlsx (SignalLedger), memory-lessons.md, and auto-memory in sync whenever Gerald reports a trade execution event — entries, exits, stop moves, tranche adds, size trims, or ad-hoc near-miss promotions. Use this skill whenever the user says 'I entered X', 'I bought X', 'I sold X', 'filled X at $Y', 'opened X', 'added to X', 'scaled into X', 'stopped out of X', 'stop hit on X', 'hit target on X', 'TP1 on X', 'took profit on X', 'closed X', 'cut X', 'invalidated X', 'time-stop on X', 'moved stop on X to $Y', 'stop to breakeven', 'trailed stop on X', 'trimmed X', 'reduced X', 'sized up X'. Also use when the user asks to 'reconcile the ledger', 'sync memory and ledger', 'backlog update on trades', or 'log a trade after the fact'. Not for placing trades, not for running the daily rec or brief, not for weekly signal mark-to-market — use the respective skills/tasks for those.
```

**New:**
```
On-demand skill that syncs Memory.md, master-data-log.xlsx (SignalLedger), memory-lessons.md, and auto-memory whenever Gerald reports a trade execution event — entries, exits, stop moves, tranche adds, size trims, or ad-hoc near-miss promotions. Use when the user says 'I entered X', 'I bought X', 'I sold X', 'filled X at $Y', 'opened X', 'added to X', 'scaled into X', 'stopped out of X', 'stop hit on X', 'hit target on X', 'TP1 on X', 'took profit on X', 'closed X', 'cut X', 'invalidated X', 'time-stop on X', 'moved stop on X to $Y', 'stop to breakeven', 'trailed stop on X', 'trimmed X', 'reduced X', or 'sized up X'. Also use for 'reconcile the ledger', 'sync memory and ledger', 'backlog update on trades', or 'log a trade after the fact'. Not for placing trades, the daily rec/brief, or weekly signal mark-to-market — use those skills/tasks instead.
```

**Preserved:** all 22 execution-event phrases · 4 reconciliation phrases · all four synced files · 6 event categories · disambiguation vs daily rec / brief / weekly signal review. **Note:** this skill has the highest trigger density in the workspace; little further compression is possible without dropping a phrase.

---

## 5. docx  (787 → 693)  *[stock skill — apply only if forking]*

**Path:** `/mnt/.claude/skills/docx/SKILL.md`

**Old:**
```
Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
```

**New:**
```
Use whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include any mention of 'Word doc', 'word document', '.docx', or requests for professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use for extracting or reorganizing content from .docx files, inserting or replacing images, find-and-replace, tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', or 'template' as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.
```

**Preserved:** 7 deliverable types · all core verbs (create/read/edit/manipulate/extract/reorganize/insert/replace/find-replace/tracked changes/convert) · disambiguation (PDFs, spreadsheets, Google Docs, coding).

---

## 6. quarterly-methodology-review  (776 → 723)

**Path:** `/mnt/.claude/skills/quarterly-methodology-review/SKILL.md`

**Old:**
```
Quarterly meta-review of the signal review system and trading methodology. Audits whether each analytical dimension is earning its keep, reconciles the research cores against out-of-sample ledger evidence, and manages the variable candidate pipeline. Use this skill whenever the user asks to "review the methodology", "audit the system", "quarterly review", "meta-review", "is the system working", "are the analytics useful", "prune the review", "research reconciliation", "variable pipeline", "methodology fitness", or "review the review". Also use when the scheduled task `quarterly-methodology-review` fires. This is NOT the weekly signal review (use signal-review for that) — this operates one level up, evaluating the signal review itself and the methodology it measures.
```

**New:**
```
Quarterly meta-review of the signal review system and trading methodology. Audits whether each analytical dimension is earning its keep, reconciles research cores against OOS ledger evidence, and manages the variable candidate pipeline. Use when the user asks to "review the methodology", "audit the system", "quarterly review", "meta-review", "is the system working", "are the analytics useful", "prune the review", "research reconciliation", "variable pipeline", "methodology fitness", or "review the review". Also triggers on scheduled task `quarterly-methodology-review`. NOT the weekly signal review (use signal-review) — this operates one level up, evaluating the signal review itself and the methodology it measures.
```

**Preserved:** 11 trigger phrases · `quarterly-methodology-review` scheduled task · disambiguation vs signal-review.

---

## 7. signal-review  (730 → 700)

**Path:** `/mnt/.claude/skills/signal-review/SKILL.md`

**Old:**
```
Weekly out-of-sample performance review of the trade recommendation system. Marks-to-market every hypothetical signal in the SignalLedger sheet of master-data-log.xlsx, computes hit rates by asset class / score component / regime, and identifies methodology improvements. Use this skill whenever the user asks to "review signals", "check performance", "how are the recs doing", "signal review", "ledger review", "weekly review of trades", "OOS performance", "out of sample", "track the recs", "hypothetical performance", or "improve the system". Also triggers on the weekly scheduled task `weekly-signal-review`. If the SignalLedger has fewer than 5 rows, the skill still runs but flags that statistical conclusions are premature.
```

**New:**
```
Weekly out-of-sample performance review of the trade recommendation system. Marks-to-market every hypothetical signal in the SignalLedger sheet of `master-data-log.xlsx`, computes hit rates by asset class / score component / regime, and identifies methodology improvements. Use when the user asks to "review signals", "check performance", "how are the recs doing", "signal review", "ledger review", "weekly review of trades", "OOS performance", "out of sample", "track the recs", "hypothetical performance", or "improve the system". Also triggers on scheduled task `weekly-signal-review`. If the SignalLedger has fewer than 5 rows, the skill runs but flags that statistical conclusions are premature.
```

**Preserved:** 11 trigger phrases · `master-data-log.xlsx` (now backtick-quoted for consistency) · `weekly-signal-review` · the <5-row premature-conclusion caveat.

---

## 8. pipeline-recovery  (703 → 604)

**Path:** `/mnt/.claude/skills/pipeline-recovery/SKILL.md`

**Old:**
```
Pipeline health monitoring, integrity checking, and automated recovery for Gerald's daily trading pipeline. Use this skill whenever the user asks to 'check the pipeline', 'is the pipeline healthy', 'recover the brief', 'fix the pipeline', 'what failed today', 'pipeline status', 'recovery check', 'why did the rec abort', 'check pipeline health', or 'run recovery'. Also use when the scheduled task `pipeline-recovery-830pm` fires. Use this skill even if the user just says something like 'anything broken today?' or 'did everything run?' in a trading context — those are pipeline health questions. Not for running the actual brief, news, or trade rec — use those dedicated skills for production runs.
```

**New:**
```
Pipeline health monitoring, integrity checking, and automated recovery for Gerald's daily trading pipeline. Use when the user asks to 'check the pipeline', 'is the pipeline healthy', 'recover the brief', 'fix the pipeline', 'what failed today', 'pipeline status', 'recovery check', 'why did the rec abort', 'check pipeline health', or 'run recovery'. Also triggers on scheduled task `pipeline-recovery-830pm`, and on informal phrasing like 'anything broken today?' or 'did everything run?' in a trading context. Not for running the actual brief, news, or trade rec — use those skills for production runs.
```

**Preserved:** 10 formal trigger phrases · 2 informal phrasings · `pipeline-recovery-830pm` · disambiguation vs brief/news/rec.

---

## Acceptance test

After Gerald applies the patches, re-run the verification snippet at the top. All 8 skills should show <1024 chars and every trigger phrase should still be present. A spot check against the conversation history ("run the 8-step", "review signals", "I entered X", etc.) should still fire the correct skill.
