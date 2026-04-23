---
name: literature-review
description: Semi-annual scan of academic finance literature for new tradeable variables. Searches working papers and journals for factors meeting five inclusion criteria (peer-reviewed, replicated, mechanism-grounded, independent, real-time implementable), assesses them against Gerald's framework gaps, and writes structured candidate proposals for the variable pipeline. Use when the user asks for a "literature review", "lit review", "new variables", "academic scan", "paper scan", "factor scan", "what's new in the research", "any new factors", "scan for new signals", or "research update". Also triggers on scheduled task `semi-annual-literature-review`. NOT the quarterly methodology review (use quarterly-methodology-review) — this searches for NEW variables outside the framework; quarterly evaluates those already inside.
---

# Literature Review — Semi-Annual Academic Variable Discovery

This skill systematically scans the academic finance literature for new tradeable variables that could strengthen Gerald's cross-asset + crypto framework. It runs twice a year (July 1 and January 1) or on demand, and produces a structured assessment of candidates for the variable pipeline.

The core principle: the framework should evolve with the research, but conservatively. Most new papers won't clear the bar. The value of this skill is in the systematic search — ensuring nothing important is missed — not in adding variables for their own sake.

---

## Step 1 — Read the inputs

Read these files to understand the current state of the framework before searching for gaps:

1. `/mnt/.auto-memory/MEMORY.md` — scan index, read all project memories (especially methodology audit, quarterly review, and performance tracking memories)
2. `/mnt/Trade/Methodology Prompt.md` — the master 8-step framework and Top-28 variable list. This is what you're trying to improve.
3. `/mnt/Trade/Trad core.md` — cross-asset factor review. Know what's already covered.
4. `/mnt/Trade/Coin core.md` — crypto predictor families. Know what's already covered.
5. `/mnt/Trade/Data Sources.md` — current variable-to-source mapping. Know what data is already being pulled.
6. `/mnt/Trade/Memory.md` — §9 research questions
6b. `/mnt/Trade/memory-lessons.md` — the full lessons log (split from Memory.md §8). Read this for repeated patterns and prior methodology notes.
6b. `/mnt/Trade/master-data-log.xlsx` — read the latest row of **RegimeHistory** (current regime state) and the **AuditAdditionLog** sheet (audit-addition contribution history) using openpyxl
7. The most recent `quarterly-methodology-review-*.md` in `/mnt/Trade/` — check the Variable Candidate Pipeline section for existing candidates
8. The most recent `signal-review-*.md` files (last 4 weeks) — check §7 Methodology Improvement Candidates for recurring failure modes that might point toward missing variables

If a quarterly review exists, pay special attention to:
- Any dimension classified as non-discriminating (a variable the system tracks but that isn't predicting anything — a gap a new variable might fill)
- Any recurring failure mode flagged across multiple weekly reviews
- The variable candidate pipeline status (what's already queued for evaluation)

## Step 2 — Identify framework gaps

Before searching, articulate what you're looking for. Build a gap list by analyzing:

**Scoring gaps:** For each score component (S, T, C, R), ask: is there an asset class or regime where this component consistently fails to discriminate? Cross-reference with the signal review's score component analysis and interaction matrix. A component that doesn't discriminate in a specific context is a gap a new variable might fill.

**Asset class gaps:** Are any assets in the universe systematically harder to score? If commodity signals underperform while equity signals outperform, there may be a missing commodity-specific variable.

**Regime gaps:** Does the framework handle all regime types equally well? If risk-off regimes produce worse signal quality, there may be a missing stress/contagion variable.

**Temporal gaps:** Does the framework have adequate coverage across time horizons? If short-term signals (≤5 days) underperform, there may be a missing high-frequency variable. If long-term signals (>28 days) underperform, a missing slow-moving structural variable.

**Known research questions:** Read Memory.md §9 for open research questions that previous reviews have flagged.

Write a structured gap list (3-7 items) before proceeding to the search. Each gap should specify: which score component it affects, which asset classes, and what kind of variable would fill it.

## Step 3 — Systematic literature search

Search for new academic papers published since the last literature review (or since the framework was established, if this is the first review). Use WebSearch to scan across these categories:

**Search strategy — search by category, not by specific paper name:**

1. **Cross-asset factors and anomalies**
   - Search: `"cross-asset" OR "multi-asset" factor anomaly predictability {current year} site:ssrn.com OR site:nber.org`
   - Search: `"time-series momentum" OR "carry trade" OR "value factor" new evidence {current year - 1} {current year}`
   - Search: `Journal of Finance Journal of Financial Economics Review of Financial Studies factor {current year}`

2. **Commodity-specific**
   - Search: `commodity futures predictability basis term-structure {current year} site:ssrn.com`
   - Search: `"convenience yield" OR "inventory" OR "backwardation" commodity return prediction new`

3. **Equity factors**
   - Search: `equity factor anomaly machine learning {current year} site:ssrn.com`
   - Search: `"momentum" OR "quality" OR "profitability" equity new factor {current year - 1} {current year}`

4. **Risk and volatility**
   - Search: `volatility risk premium prediction VIX {current year} site:ssrn.com`
   - Search: `"intermediary" OR "dealer" OR "market maker" asset pricing constraint {current year}`
   - Search: `tail risk contagion systemic financial {current year} site:ssrn.com`

5. **Crypto-specific**
   - Search: `Bitcoin cryptocurrency factor return predictability {current year} site:ssrn.com`
   - Search: `"on-chain" OR "blockchain" OR "DeFi" crypto asset pricing {current year}`
   - Search: `Bitcoin ETF flow institutional crypto market structure {current year}`

6. **Market microstructure and flow**
   - Search: `order flow imbalance return prediction {current year} site:ssrn.com`
   - Search: `"gamma exposure" OR "dealer hedging" OR "options market maker" equity {current year}`

7. **Macro and rates**
   - Search: `"term premium" OR "yield curve" OR "monetary policy" predictability new {current year}`
   - Search: `FX carry momentum crash risk new evidence {current year}`

8. **Gap-directed searches:** For each gap identified in Step 2, construct 1-2 targeted searches. For example, if commodity S-scores are the weak link, search specifically for new commodity structural variables.

For each search, read the titles and abstracts of the top results. Download or read papers that look relevant. You're looking for variables that:
- Are NOT already in the Top-28 list or the existing candidate pipeline
- Address one of the identified framework gaps
- Have a plausible mechanism, not just a statistical pattern

## Step 4 — Five-criteria screening

For each promising variable found in Step 3, apply the five inclusion criteria from the April 2026 methodology audit:

| Criterion | Question | Pass/Fail |
|-----------|----------|-----------|
| **Peer-reviewed** | Published in a reputable journal (JF, JFE, RFS, JFQA, JEF, JBF) or has 50+ SSRN downloads with clear methodology? Working papers from top-10 finance departments count as provisional. | |
| **Replicated** | Tested across at least two samples, time periods, or asset classes? If only one sample, is the sample large (>20 years) and the effect economically large (Sharpe >0.5 pre-decay)? | |
| **Mechanism-grounded** | Is there a coherent economic explanation (risk premium, behavioral bias, institutional constraint, information asymmetry)? Pure statistical patterns without mechanism fail this criterion. | |
| **Independent information** | Does the variable provide information not already captured by the existing Top-28? Check correlation with existing variables. If r > 0.7 with an existing variable, it's redundant unless it captures a specific regime or asset class the existing variable misses. | |
| **Real-time implementable** | Can the variable be computed from publicly available data with ≤1 week lag? Variables requiring proprietary data, long publication lags (>1 month), or expensive subscriptions fail unless a free proxy exists. | |

A variable must pass all five criteria to enter the candidate pipeline. Passing 4/5 with a clear path to fixing the fifth (e.g., "not yet replicated but the mechanism is strong and a replication study is underway") earns a WATCH classification.

## Step 5 — Decay projection

For every variable that passes the five-criteria screen, apply the McLean-Pontiff (2016) decay framework:

1. **Published Sharpe ratio** — what the paper reports
2. **Post-publication decay** — apply 30-50% haircut (use 40% as default unless there's reason to adjust)
3. **Time-since-publication decay** — if the paper is >5 years old, apply an additional 10-20% haircut for continued arbitrage erosion
4. **Projected operational Sharpe** — the number that matters for sizing and expectation-setting

If the projected operational Sharpe falls below 0.3, the variable is unlikely to be worth the complexity cost. Flag it but don't recommend implementation.

## Step 6 — Integration assessment

For each variable that clears Steps 4 and 5, map how it would integrate into the existing framework:

1. **Which score component does it feed?** (S, T, C, R, or a new overlay)
2. **Which assets does it apply to?** (all, equities only, commodities only, crypto only, etc.)
3. **Does it replace or supplement an existing variable?** If it supplements, define the interaction rule (analogous to how basis-momentum supplements static F1-F2 slope with a divergence cap).
4. **Double-counting risk:** What existing variables is it correlated with? Define a de-duplication rule if needed (analogous to the intermediary-capital / HY OAS gate).
5. **Data source and pull path:** Where does the data come from? Is there a free public source? What's the pull frequency and lag?
6. **Implementation complexity:** New ledger columns? New compute script? Changes to the daily-trade-rec skill? Estimate the effort.
7. **Proposed review window:** How long should the pilot run before a GO/NO-GO decision? Default is 6 months unless there's reason to shorten (high-frequency variable with fast feedback) or lengthen (slow-moving structural variable).

## Step 7 — Write the review file

Path: `/mnt/Trade/literature-review-{YYYY-MM-DD}.md`. Use this structure:

```
# Literature Review — YYYY-MM-DD

## 1. Review Summary
[One paragraph: period covered, number of papers scanned, number of candidates identified, headline finding. Is the framework well-covered or are there meaningful gaps?]

## 2. Framework Gap Analysis
[The gap list from Step 2, with assessment of severity. Which gaps are the most pressing based on signal review evidence?]

## 3. Literature Scan Results
[For each search category: number of papers reviewed, notable findings, anything trending in the field that's relevant even if no specific variable emerged.]

## 4. Variable Candidates — Full Assessment

### Candidate LR-{YYYY}-{NN}: {Variable Name}
**Source paper:** [citation]
**Variable definition:** [precise definition]
**Five-criteria screening:**
| Criterion | Assessment | Pass/Fail |
|-----------|------------|-----------|
| Peer-reviewed | ... | ... |
| Replicated | ... | ... |
| Mechanism-grounded | ... | ... |
| Independent information | ... | ... |
| Real-time implementable | ... | ... |

**Decay projection:**
- Published Sharpe: ...
- Post-publication haircut: ...
- Projected operational Sharpe: ...

**Integration map:**
- Score component: ...
- Asset scope: ...
- Replaces/supplements: ...
- Double-counting gate: ...
- Data source: ...
- Implementation complexity: ...
- Proposed review window: ...

**Gap addressed:** [which gap from §2 this fills]
**Recommendation:** PIPELINE (add to quarterly review's candidate list) / WATCH (promising but missing one criterion) / REJECT (fails screening)
**Gerald sign-off:** PENDING

[Repeat for each candidate]

## 5. Candidates Considered and Rejected
[Table of variables that looked promising but failed one or more criteria. Brief reason for each rejection. This prevents re-scanning the same papers next cycle.]

## 6. Field Trends
[2-3 paragraphs on where academic finance research is heading that might produce useful variables in the next 1-2 years. What should we watch for next time?]

## 7. Updates to Candidate Pipeline
[Summary of what's being added to the quarterly review's variable candidate pipeline, with tier assignments (Tier 2 = needs data infrastructure, Tier 3 = needs signal count).]

## 8. Action Items
[Bulleted list: what to implement now, what to monitor, when the next literature review is due.]

---

Review covers: {date range}. Papers scanned: ~{N}. Candidates identified: {N} (PIPELINE: {N}, WATCH: {N}, REJECT: {N}).
```

## Step 8 — Update downstream files

After writing the review file:

1. **Update the quarterly review's candidate pipeline.** If the next quarterly-methodology-review skill file has a Step 4 candidate list, add any PIPELINE-status candidates to it with their tier assignment. If you can't edit the skill file (read-only), write the additions to the review file §7 and note that they need to be incorporated.

2. **Update Memory.md §9** with any new research questions surfaced by the review.

3. **Update `/mnt/Trade/memory-lessons.md`** with a one-line summary: `YYYY-MM-DD literature review: N papers scanned, N candidates identified (N PIPELINE, N WATCH, N REJECT). File: literature-review-YYYY-MM-DD.md.` (Memory.md §8 is a pointer to this file.)

4. **Update auto-memory** — create or update `/mnt/.auto-memory/project_literature_review_{YYYY-MM-DD}.md` with key findings and next review date. Update MEMORY.md index.

5. **Log rejected candidates** — maintain a running list so future reviews don't re-scan the same papers. Append to the "Candidates Considered and Rejected" table in the review file. If a prior literature review exists, carry forward its rejection list.

## Step 8.5 — Sync to master-data-log.xlsx (MANDATORY)

After updating downstream files, sync new variable candidates to the **VariableRegistry** sheet in `master-data-log.xlsx` using openpyxl. Read `Excel-Sync-Protocol.md` §5 (literature-review) for the authoritative column mapping.

For each new variable candidate identified:
- Append a new row with the next sequential Var_ID (V034, V035, ...)
- Fill all known fields from the five-criteria screening
- Status = 'Candidate' (if 5/5 pass → 'Watchlist')
- Discovery_Date = today, Discovery_Source = 'Literature review YYYY-MM-DD'
- Fill Source_Paper, Intuition, Published_Sharpe, Decay_Haircut_Pct, Proj_Op_Sharpe

For rejected candidates: still add a row with Status = 'Rejected' and fill the failure reason in Notes. This prevents re-scanning.

## Step 9 — HTML report

Produce a single-file HTML report at `/mnt/Trade/report-{YYYY-MM-DD}-literature-review.html`. Use Chart.js via CDN (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`).

**Required charts:**

- **Gap severity radar** — the framework gaps from §2 on a radar chart, scored by how much signal review evidence supports each gap
- **Candidate funnel** — papers scanned → passed mechanism screen → passed independence screen → passed implementability screen → PIPELINE recommendation
- **Variable coverage heatmap** — rows = score components (S/T/C/R), columns = asset classes, cells = number of Grade A variables covering that combination. Highlights gaps.
- **Decay-adjusted Sharpe comparison** — bar chart comparing projected operational Sharpe of new candidates vs existing Top-28 variables
- **Timeline** — when each current variable was added to the framework, when candidates are proposed, and when reviews are due. Gives a visual sense of framework evolution pace.

---

## Discipline rules

- Every candidate requires Gerald's sign-off before entering even the pilot phase. This skill discovers and assesses — it never adds variables to the binding framework.
- The five-criteria screen is non-negotiable. A variable that fails any criterion does not enter the pipeline, regardless of how compelling the paper looks. WATCH status is the exception for 4/5 passes with a clear remediation path.
- Apply McLean-Pontiff decay to everything. The published Sharpe is not the operational Sharpe.
- Prefer parsimony. A framework with 28 well-chosen variables is better than one with 40 variables where 12 are redundant. Every candidate must demonstrate independence from existing variables.
- Do not recommend variables that require proprietary or expensive data. Gerald's system runs on public sources. If a free proxy exists for a proprietary variable, assess the proxy's quality before recommending.
- Carry forward the rejection list. Re-scanning rejected variables wastes time. A rejected variable can re-enter consideration only if new evidence (replication study, regime change, new data source) addresses the specific criterion it failed.
- The literature review is complementary to the quarterly methodology review, not a replacement. This skill searches outward (new research); the quarterly review looks inward (is what we have working?). They feed each other through the candidate pipeline.
