# Skill Patches — 2026-04-15: Signal Review Enhancement

**Purpose:** These patches add 6 new analytical dimensions to the signal review system: score component interactions, time-to-exit, MAE/MFE, catalyst resolution, VIX conditioning, and near-miss counterfactual regression. The hypo-ledger has already been updated with the new columns. These patches must be applied to the skill SKILL.md files.

**How to apply:** Copy each patch section below into the corresponding SKILL.md file at the indicated location. Use the skill-creator skill or manually edit in your `.claude/skills/` directory.

---

## Patch 1: daily-trade-rec/SKILL.md — Step 8 ledger logging

**Location:** Replace the "What to log" section (items 1 and 2) under Step 8.

**Replace from:** `1. **Promoted signals**` through `- `Notes`: the specific trigger that would promote it to |Sum| ≥ 3 (copied from §4 of the rec)`

**Replace with:**

```markdown
1. **Promoted signals** (|Sum| ≥ 3 that passed or conditionally passed the pre-entry checklist): append one row to the "Promoted Signals" table.
   - `ID`: use the next sequential `P###` ID (check the `<!-- Next promoted ID -->` comment and increment it after)
   - `Date`: today YYYY-MM-DD
   - `Asset`, `Dir`: from the rec's §3 Recommendations Table
   - `S`, `T`, `C`, `R`, `Sum`: the confirmed scores from Step 3
   - `Entry Price`: the most current market price available (from the US close snapshot or the brief). This is the hypothetical entry — the price at which a trader reading the rec could have acted.
   - `ATR Stop`, `Target (TP1)`, `Target (TP2)`: from the rec's sizing per Risk Rules §3. If the trade wasn't taken and exact levels weren't computed, estimate using the brief's ATR data and the 2–3× ATR stop / 1.5× / 3× ATR target framework.
   - `Invalidation`, `Inv. Date`: from the rec's Step 8 methodology output
   - `VIX at Entry`: VIX close from the US close snapshot or the brief's cross-asset dashboard. If MISSING, write `~` and note in the rec's §6 Data Gaps.
   - `Taken?`: `YES` if Gerald actually entered (check Memory.md §2), `NO` if the checklist blocked it or Gerald chose not to, `CONDITIONAL` if it passed with a caveat Gerald hasn't resolved
   - `Status`: always `OPEN` at logging time (the signal-review skill updates this weekly)
   - `Exit Price`, `Exit Date`, `Days to Exit`, `MAE %`, `MFE %`, `Catalyst Outcome`, `Hypothetical P&L %`: leave blank at logging time — filled by the signal-review skill
   - `Notes`: one line — the key reason it was/wasn't taken (e.g., "fail-loud: intermediary capital MISSING on R-overlay", "checklist clean — entered at open")

2. **Near-miss signals** (|Sum| = 2, or |Sum| ≥ 3 blocked by fail-loud or checklist failure): append one row to the "Near-Miss Signals" table for each near-miss from the rec's §4.
   - `ID`: next sequential `N###` (check and increment the comment)
   - `Date`, `Asset`, `Dir`, `S`, `T`, `C`, `R`, `Sum`: from the rec
   - `Blocking Leg`: which score component is missing or hostile (`S`, `T`, `C`, `R`, or `fail-loud`)
   - `Block Reason`: one phrase (e.g., "residual momentum MISSING", "R−1 crowding", "no catalyst on calendar")
   - `Price at Signal`: market price at rec time
   - `VIX at Signal`: VIX close from the brief or US close snapshot. If MISSING, write `~`.
   - `Status`: always `OPEN` at logging time
   - Remaining columns (`Price at Review`, `Days Elapsed`, `Hypothetical Move %`, `MAE %`, `MFE %`, `Would Have Hit Target?`, `Would Have Hit Stop?`, `Catalyst Outcome`): leave blank — filled by the signal-review skill
   - `Notes`: the specific trigger that would promote it to |Sum| ≥ 3 (copied from §4 of the rec)
```

---

## Patch 2: signal-review/SKILL.md — New analytical steps

**Location:** Insert as new Step 4A after existing Step 4 (Compute rolling statistics) and before Step 5 (Identify methodology improvement candidates).

**Insert after the line:** `**By Regime Label:** Group signals by the regime label active at signal time (from the rec's §2). Compute win rate per regime.`

**And before:** `**Audit-Addition Variables:**`

```markdown

**Score Component Interaction Matrix (2026-04-15 addition):**
For each pair (S×T, S×R, T×R, T×C, S×C, C×R), build a 3×3 contingency table (+1/0/−1 for each component) and compute win rates in each cell. The key question is whether any pair produces a synergistic or antagonistic interaction — i.e., does S+1 AND T+1 win at a rate meaningfully higher than S+1 alone and T+1 alone would predict? Update the "Score Component Interaction Matrix" table in the Rolling Performance Summary section. Flag any cell with a win-rate differential > 15pp as "SYNERGY" or "CONFLICT" (with sample size caveat).

**Time-to-Exit Distribution (2026-04-15 addition):**
For every closed signal (promoted and near-miss), compute `Days to Exit` = exit date − entry date. Bucket into ≤5 days, 6–14 days, 15–28 days, >28 days. Compute win rate and average P&L within each bucket. Update the "Time-to-Exit Distribution" table in the Rolling Performance Summary. If the >28-day bucket has a worse win rate than shorter buckets, flag for invalidation window review.

**MAE / MFE Analysis (2026-04-15 addition):**
For every closed signal:
- `MAE %` = (worst closing price before exit − entry price) / entry price × 100 × direction multiplier. If intraday data is unavailable, use worst daily close as a conservative estimate.
- `MFE %` = (best closing price before exit − entry price) / entry price × 100 × direction multiplier.

Fill these into the ledger rows and update the "MAE / MFE Summary" table. Key diagnostic questions:
1. What fraction of winners had MAE exceeding half the stop distance? (If high → stops may be too tight, shaking out eventual winners.)
2. What fraction of losers had MFE exceeding half the target distance? (If high → trades that would have won are giving back gains before hitting the target, suggesting the target is too ambitious or trailing stops should be tighter.)

**Catalyst Resolution Tracking (2026-04-15 addition):**
For every signal whose named catalyst date has passed, classify the outcome:
- `SURPRISE`: catalyst broke in a direction the consensus didn't expect
- `IN-LINE`: catalyst delivered approximately at consensus
- `NO-SHOW`: the anticipated catalyst didn't materialize within the signal's window
- `OPPOSITE`: catalyst resolved directly against the signal's thesis direction

Fill `Catalyst Outcome` in the ledger and update the "Catalyst Resolution Tracking" table. Compare win rates across categories. If SURPRISE signals significantly outperform IN-LINE, the system is correctly positioned for convexity. If NO-SHOW signals have the worst outcomes, the C-score may be overweighting event dependency.

**VIX-at-Entry Conditioning (2026-04-15 addition):**
Bucket all signals by VIX at entry: <15, 15–25, 25–35, >35. Compute win rate, average P&L, and average days-to-exit per bucket. Update the "VIX-at-Entry Conditioning" table. The key question: does the R-score adequately capture volatility-regime risk, or do high-VIX entries systematically underperform even when R=0 or R=+1? If so, recommend a VIX-conditional threshold tightening (require |Sum| ≥ 4 when VIX > 30) as a Methodology Change Candidate.
```

---

**Location:** In Step 5, add item 8 to the "What to look for" list (after item 7 on regime dependency):

```markdown

8. **Near-miss counterfactual regression (2026-04-15 addition):** When the ledger has ≥ 20 near-miss signals with resolved outcomes, go beyond counting blocking legs. Ask: among near-misses blocked by the same leg (e.g., all R−1 blocks), which features predict whether they would have won or lost? If R−1 blocks in low-VIX environments would have won at 70%+ (the R filter is over-conservative when vol is calm), that's a specific, actionable finding. If R−1 blocks in high-VIX environments would have hit stops at 80%+ (the R filter is correctly protecting), that validates the filter. Document the pattern in the Methodology Improvement Candidates section with the specific conditioning variable and the sample size. Require N ≥ 15 in the sub-group before labeling RECOMMEND; below that, label MONITOR.
```

---

## Patch 3: signal-review/SKILL.md — Updated review file structure

**Location:** In Step 6, add sections 4A–4E to the review file template, between §4 (Score Component Analysis) and §5 (Gating Rule Assessment):

```markdown
## 4A. Score Component Interactions
[For each component pair: is the interaction synergistic, antagonistic, or neutral? Table from the Rolling Summary. Flag any pair with win-rate differential > 15pp. Sample size caveats.]

## 4B. Time-to-Exit Analysis
[Distribution of days-to-exit by outcome. Is the invalidation window well-calibrated? Are certain asset classes resolving faster or slower than others?]

## 4C. Stop & Target Calibration (MAE/MFE)
[Are stops too tight (many winners had deep MAE before recovering)? Are targets too far (many losers showed significant MFE before reversing)? Specific ATR-multiple adjustment candidates if evidence warrants.]

## 4D. Catalyst Resolution
[How did named catalysts resolve? Is the C-score adding predictive value, or are surprise-dependent theses the only ones that work? Win rates by catalyst outcome category.]

## 4E. Volatility Regime Conditioning
[Do high-VIX entries underperform after controlling for R-score? Should the promotion threshold be regime-adaptive? Evidence from VIX bucketing.]
```

---

## Patch 4: signal-review/SKILL.md — HTML report additions

**Location:** In Step 9 (HTML report), add to the "Required charts" list:

```markdown
- **Score component interaction heatmap** (6-cell grid: S×T, S×R, T×R, T×C, S×C, C×R; color by win rate; annotate with N) — reveals which component combinations carry the system
- **Time-to-exit histogram** (stacked bars by outcome: target hit / stop hit / expired; x-axis = days buckets) — shows whether the invalidation window is well-calibrated
- **MAE/MFE scatter plot** (x = MAE%, y = MFE%, color by outcome; overlay stop/target lines) — the classic trade forensics chart; points clustered near stop line with high MFE = stops too tight
- **Catalyst outcome treemap** (area = count, color = win rate, partitioned by SURPRISE / IN-LINE / NO-SHOW / OPPOSITE) — shows whether catalyst calls add value
- **VIX-at-entry performance bars** (grouped bar: win rate + avg P&L per VIX bucket) — tests whether the R-score captures vol-regime risk
- **Near-miss conditioning chart** (when N ≥ 20: grouped bar by blocking leg, split by VIX bucket or asset class, showing counterfactual win rate) — reveals where the gating rules are over/under-conservative
```

Add this note to the existing "low N" banner logic:
```markdown
For the interaction heatmap, MAE/MFE scatter, and near-miss conditioning chart: if any cell or bucket has fewer than 5 data points, grey it out and label "insufficient data" rather than showing a misleading color/position.
```

---

## Patch 5: signal-review/SKILL.md — Archival tier for ledger growth management

**Location:** Add as a new section after Step 8 (Update Memory) and before Step 9 (HTML report):

```markdown
## Step 8A — Ledger archival (context budget management)

When the ledger's Promoted + Near-Miss tables combined exceed 80 rows, apply the following archival tier to keep the weekly review's input context under budget:

1. **Active tier (always in main ledger):** All rows with Status = `OPEN` or `STILL_OPEN`, plus all rows closed/resolved within the past 8 weeks.
2. **Archive tier:** Rows closed/resolved more than 8 weeks ago. Move these to `/mnt/Trade/hypo-ledger-2026-archive.md` with identical column structure. The archive file is append-only and is only read during quarterly deep reviews (Step 10).
3. **Rolling summary carries forward:** The statistics tables in the main ledger always reflect ALL signals (active + archived). When archiving rows, recompute the rolling statistics to include the archived data before removing the rows.

This tiering exists because the weekly review skill reads the entire ledger. At ~150 tokens per row, an 80-row ledger = ~12,000 tokens. Archiving old closed rows keeps the active ledger lean while preserving the full statistical picture in the summary tables.
```

---

End of patches. The hypo-ledger-2026.md has already been updated with the new columns and summary tables in this session.
