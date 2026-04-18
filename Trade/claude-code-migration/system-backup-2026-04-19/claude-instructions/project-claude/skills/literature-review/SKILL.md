---
name: literature-review
description: "Semi-annual academic finance lit scan for new tradeable variables. Five inclusion criteria, McLean-Pontiff decay projection, integration assessment. Use for 'literature review', 'lit review', 'new variables', 'academic scan', 'factor scan'. Scope-limited runs allowed."
model: opus
allowed-tools: Bash(python3 *) Read Write Edit WebSearch Grep Glob
---

# Literature Review — Semi-Annual Variable Discovery

Systematic scan for new variables that could strengthen the framework. Runs semi-annually or on demand. Most papers won't clear the bar — value is in systematic coverage.

## Step 1 — Reads

1. `Methodology Prompt.md` — current Top-28 variables, framework gaps
2. `Trad core.md` — cross-asset factors already covered
3. `Coin core.md` — crypto predictors already covered
4. `Data Sources.md` — current variable-to-source mapping
5. `Memory.md` — §9 research questions
6. `memory-lessons.md` — repeated patterns
7. `master-data-log.xlsx` — RegimeHistory, AuditAdditionLog, PerformanceStats
8. Latest `quarterly-methodology-review-*.md` — variable candidate pipeline
9. Recent `signal-review-*.md` files — §7 improvement candidates

## Step 2 — Identify framework gaps

Analyze: scoring gaps (which S/T/C/R components fail to discriminate?), asset class gaps, regime gaps, temporal gaps, Memory §9 open questions. Produce 3–7 gap list before searching.

## Step 3 — Systematic search

By category: cross-asset factors, commodities, equities, risk/volatility, crypto, microstructure, macro/rates, gap-directed. Use WebSearch for SSRN, NBER, JF, JFE, RFS, working papers.

## Step 4 — Five-criteria screening

Each candidate must pass ALL:
1. Peer-reviewed or credible working paper
2. Replicated across samples/geographies
3. Coherent economic mechanism
4. Independent (not redundant with existing Top-28)
5. Real-time implementable with available data

## Step 5 — McLean-Pontiff decay projection

Published Sharpe → projected operational Sharpe (apply 26% OOS decay + 58% post-publication decay as upper bound).

## Step 6 — Integration assessment

Per candidate: component feed (S/T/C/R), asset scope, double-counting gates, data source, implementation complexity, review window.

## Step 7 — Write output + VariableRegistry sync

Output: structured review file. Sync Candidate rows to VariableRegistry in master-data-log.xlsx.
