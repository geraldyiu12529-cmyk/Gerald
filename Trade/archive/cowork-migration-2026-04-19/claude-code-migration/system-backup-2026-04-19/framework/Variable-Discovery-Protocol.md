# Variable Discovery Protocol

**Created:** 2026-04-15
**Authority over:** Variable candidate discovery across all four sources, standardized capture template, per-skill discovery responsibilities, discovery quality checklist.

This document is the authoritative specification for how new variable candidates enter the system. Every skill that runs daily, weekly, or semi-annually has a discovery responsibility defined here. The quarterly-methodology-review skill remains the sole promotion gate — discovery feeds the funnel, the quarterly review controls what exits it.

---

## 1. The Four-Source Framework

Variable ideas arrive from four distinct sources. Each has a natural cadence. The system captures them at that cadence, not semi-annually.

| Source | What it captures | Natural cadence | Responsible skill(s) |
|--------|-----------------|-----------------|---------------------|
| **A — Academic research** | Published papers, working papers, replicated factors, mechanism-grounded anomalies | Semi-annual | literature-review |
| **B — Market observation** | Patterns noticed in flows, positioning, price action, cross-asset behavior during daily scoring | Daily | market-brief, daily-trade-rec |
| **C — Practitioner research** | Sell-side/buy-side commentary, blog posts, podcast insights, conference takeaways found during news scanning | Daily | news-events |
| **D — Repeated market behavior** | Recurring patterns that surface across multiple weeks: seasonal effects, event-response regularities, persistent blocking patterns in the ledger | Weekly | signal-review (weekly) |

**Principle:** If you observe something that repeatedly appears and isn't in the VariableRegistry, flag it as a Candidate. Don't wait for the next review cycle.

---

## 2. Standardized Capture Template

Every variable candidate, regardless of source, must be logged with at minimum these fields. This template applies whether the candidate is discovered by the literature review finding an academic factor or the daily brief noticing a flow pattern.

### Minimum Required Fields (for VariableRegistry entry)

| Field | Description | Example |
|-------|-------------|---------|
| **Name** | Short, descriptive identifier | `Treasury_Auction_Tail` |
| **Definition** | Precise, computable definition — another analyst could reproduce the variable from this sentence alone | Difference between the high yield and the when-issued yield at US Treasury auctions, in basis points |
| **Asset_Class** | Which assets it applies to: All, Equities, Commodities, Crypto, FX, Rates, or a specific subset | Rates, Equities (via risk-appetite channel) |
| **Use_Type** | Which score component it would feed: S, T, C, R, or Overlay | C (event-driven catalyst) |
| **Taxonomy** | Classification: Structural / Tactical / Regime / Event | Event |
| **Horizon** | Expected signal horizon: <5d, 5-14d, 14-28d, >28d, structural (persistent) | 5-14d |
| **Mechanism** | One-sentence economic explanation of WHY this should predict returns. Must name a risk premium, behavioral bias, institutional constraint, or information asymmetry. | Large auction tails signal weak demand for duration → rising term premium → risk-off signal for equities within 1-2 weeks |
| **Source_Type** | A (Academic) / B (Market observation) / C (Practitioner) / D (Repeated behavior) | B |
| **Discovery_Date** | Date the candidate was first registered (YYYY-MM-DD) | 2026-05-12 |
| **Discovery_Source** | Specific origin: which paper, which brief, which observation | market-brief-2026-05-12: noticed auction tail >3bp preceded SPX weakness in 4 of last 5 instances |
| **Initial_Evidence** | Strong / Moderate / Weak / Anecdotal — honest assessment at discovery time | Weak (4 observations, no formal test) |
| **Independence_Check** | Which existing variables might overlap. If correlated r > 0.7, note it. | Partially overlaps with ACM term premium (rates structural), but captures demand-shock timing that term premium misses |
| **Implementability** | Data source, lag, cost. Public/free vs proprietary. | Treasury Direct auction results, published same day, free. Lag: 0 days for dated auctions. |
| **Status** | Always `Candidate` at discovery. The quarterly review promotes. | Candidate |

### Extended Fields (for Source A — literature review only)

These fields supplement the minimum template when the source is an academic paper:

| Field | Description |
|-------|-------------|
| **Source_Paper** | Full citation (authors, title, journal/SSRN, year) |
| **Published_Sharpe** | What the paper reports |
| **Decay_Haircut_Pct** | McLean-Pontiff decay adjustment (default 40%) |
| **Proj_Op_Sharpe** | Projected operational Sharpe after decay |
| **Five_Criteria_Pass** | Which of the five inclusion criteria it passes (peer-reviewed, replicated, mechanism-grounded, independent, real-time implementable) |
| **Source_Hierarchy** | Tier 1 (JF/JFE/RFS) / Tier 2 (JFQA/JEF/JBF) / Tier 3 (SSRN working paper from top-10 dept) / Tier 4 (other) |

---

## 3. Per-Skill Discovery Responsibilities

### 3A. market-brief (daily, Source B)

**When to flag:** During Step 5 (building the asset scorecard), if you notice a pattern in the data that is not captured by any existing Top-28 variable and is not already in the VariableRegistry:

- A cross-asset relationship that's behaving differently than the methodology expects
- A variable you're pulling that consistently provides signal but isn't formally scored
- A data point that's moving a score in practice but isn't in the variable list

**What to do:**

1. At the end of the brief (after Step 7 Memory update, before Step 8 Excel sync), add a section:

```
## 6. Variable Discovery Notes

[If nothing observed: "No new variable candidates observed today."]

[If something noticed:]
**Potential candidate:** {Name}
**Observation:** {What you saw, 1-2 sentences}
**Definition:** {Precise definition}
**Mechanism hypothesis:** {Why it might predict}
**Score component:** {S/T/C/R}
**Asset scope:** {Which assets}
**Evidence so far:** {Anecdotal / Weak — be honest}
```

2. If the observation is strong enough (seen 3+ times, or the mechanism is well-grounded), also write a Candidate row to the VariableRegistry sheet in master-data-log.xlsx using the standardized template from §2.

3. Do NOT let discovery slow down the brief. This is a lightweight pass — if nothing stands out, write "No new variable candidates observed today" and move on. The brief's primary job is the scorecard.

### 3B. daily-trade-rec (daily, Sources B and D)

**When to flag:** During Step 3 (8-step methodology) and Step 5 (pre-entry checklist), if you notice:

- A near-miss (|Sum| = 2) that is repeatedly blocked by the same gap across multiple days — that gap might be a missing variable
- An asset that consistently scores well on S/T/C but fails R (or vice versa) in a way that suggests a missing risk dimension
- A pattern where the pre-entry checklist correlation gate consistently blocks a specific theme — might indicate missing independence structure

**What to do:**

1. In the rec's §4 (Theses Not Taken), when describing a near-miss, add one sentence: "Discovery note: {this blocking pattern has appeared N times in the last M days — if persistent, suggest registering {variable name} as a Candidate in the quarterly review}."

2. In the rec's §8 (Memory Updates Needed), add a bullet for any discovery observation: "Variable discovery: {brief description of pattern, which score leg, which assets}."

3. If the pattern has appeared 3+ times across different trade-rec runs (check Memory.md §8 for prior mentions), write a Candidate row to the VariableRegistry.

4. As with the brief, this is lightweight. The rec's primary job is the decision document. Don't spend more than 2-3 sentences on discovery unless the pattern is striking.

### 3C. news-events (daily, Source C)

**When to flag:** During Steps 2-7 (all search categories), if you encounter:

- Practitioner research, sell-side commentary, or blog posts that identify a tradeable variable with a plausible mechanism
- A recurring theme across multiple sell-side desks that points to an emerging factor (e.g., "everyone is talking about GEX this week")
- Conference takeaways or research notes that describe a systematic relationship

**What to do:**

1. In the news file's §7 (Regime Implications), after the 2-3 line regime assessment (which remains mandatory), add a discovery subsection:

```
**Variable discovery:** [If nothing: "No new variable candidates from today's practitioner research."]
[If something noticed:]
Practitioner signal: {Name} — {1-sentence description}. Source: {who said it, where}. Mechanism: {why it might work}. Status: flagged for registry review.
```

2. Only flag observations where the practitioner is describing a SYSTEMATIC relationship, not a one-off trade idea. "GEX has been driving mean-reversion for three weeks" is a variable candidate. "I think AAPL is going to $250" is a trade opinion.

3. If the same practitioner variable has been flagged in news files 3+ times across different weeks, write a Candidate row to the VariableRegistry.

### 3D. signal-review (weekly, Source D + cleanup)

The weekly signal review has two discovery responsibilities: flagging repeated market behaviors (Source D) and classifying/cleaning candidates accumulated during the week.

**Source D — repeated market behavior:**

During Step 5 (methodology improvement candidates), if the analysis reveals:

- A persistent blocking pattern: the same score leg blocks near-misses repeatedly across weeks, and the blocked signals would have won — suggests a missing variable that would unblock that leg
- A regime-dependent failure mode: signals that work in one regime but fail in another, where the regime distinction isn't captured by current variables
- A time-of-week or calendar pattern: signals logged on certain days or around certain events systematically outperform/underperform
- A cross-asset lead-lag that the scoring system doesn't capture: one asset consistently moves before another, but the lag isn't in the framework

**What to do for Source D:**

In the review file's §7 (Methodology Improvement Candidates), add a subsection:

```
### 7B. Variable Discovery — Repeated Patterns

[If nothing: "No new pattern-based variable candidates this week."]

[If something noticed:]
**Pattern:** {Description of the repeated behavior, with dates and signal IDs}
**Proposed variable:** {Name}
**Definition:** {Precise definition}
**Mechanism:** {Why this pattern might be systematic, not noise}
**Evidence:** {How many times observed, win rate differential, sample size caveat}
**Action:** REGISTER (write to VariableRegistry) / MONITOR (too early, watch for one more week) / REJECT (pattern broke this week)
```

**Weekly cleanup responsibility:**

After writing §7B, review the VariableRegistry for any Candidate-status entries that were added during the past week by the daily skills. For each:

1. Confirm the definition is precise (another analyst could compute it)
2. Confirm the mechanism is stated (not just "it seems to work")
3. Confirm the independence check is filled in (what existing variables does it overlap with?)
4. If any field is missing or vague, fill it in based on the week's data
5. If the candidate has been sitting at Candidate status for 4+ weeks without accumulating more evidence, recommend REJECT or MONITOR in the review

This ensures candidates don't rot — they either accumulate evidence and get promoted at the quarterly review, or they get cleaned out.

### 3E. literature-review (semi-annual, Source A)

The literature review's existing five-criteria screening and decay projection already implement Source A thoroughly. The enhancements from this protocol:

1. **Use the extended capture template** from §2 for every candidate. The existing review file format (§4 of the skill) already captures most fields — ensure Source_Hierarchy, Taxonomy, and Horizon are also recorded.

2. **Cross-reference against weekly discoveries.** Before searching for gaps (Step 2), read the VariableRegistry for any Candidate or Watchlist entries from Sources B/C/D that could benefit from academic support. If the daily pipeline flagged "GEX seems to matter" and the literature review finds papers supporting GEX as a predictive factor, that's convergent evidence — note it.

3. **Apply the "good discovery questions" checklist** from §4 below during the gap analysis (Step 2).

---

## 4. Good Discovery Questions Checklist

When assessing whether an observation deserves to become a variable candidate, ask:

1. **Is this computable?** Can you write a formula or algorithm that produces a number from publicly available data? If the answer is "I'd know it when I see it" — it's not a variable yet.

2. **Is this independent?** Does it tell you something the existing Top-28 don't? If it's just VIX with extra steps, it's redundant. Check correlation with existing variables.

3. **Is there a mechanism?** Can you name the economic channel — risk premium, behavioral bias, institutional constraint, information asymmetry? "It just works" fails this criterion.

4. **Is this timely?** Can you get the data with ≤1 week lag? A variable that's only available with a 2-month lag is useless for pre-open decisions.

5. **Would this have changed a decision?** Look back at the last 5-10 trade-rec files. Would scoring this variable have promoted a near-miss that would have won, or blocked a signal that would have lost? If neither, it's not adding value.

6. **Is this persistent or one-off?** Has the pattern held across at least two distinct market conditions, or is it a single-regime artifact?

7. **What's the implementation cost?** New data source? New compute script? New column in the ledger? The benefit must exceed the complexity cost.

If a candidate passes questions 1-4, it's worth registering. Questions 5-7 determine the urgency of promotion.

---

## 5. Flow Diagram

```
Daily pipeline (Sources B, C, D):
  market-brief → notices pattern → logs in §6 of brief
  news-events → spots practitioner variable → logs in §7 of news file  
  trade-rec → identifies blocking pattern → logs in §4 and §8 of rec
       ↓
  If observed 3+ times → writes Candidate row to VariableRegistry
       ↓
Weekly signal-review (Source D + cleanup):
  Flags repeated behaviors → logs in §7B of review
  Cleans/validates week's Candidate entries in VariableRegistry
       ↓
Quarterly methodology review (promotion gate):
  Reads VariableRegistry → assesses all Candidates/Watchlist
  Promotes with Gerald's sign-off: Candidate → Watchlist → Under Review → ...
       ↓
Semi-annual literature review (Source A):
  Sweeps academic databases → uses extended template
  Cross-references against pipeline Candidates from other sources
  Adds new academic Candidates to VariableRegistry
```

---

## 6. What This Replaces

Previously, the literature review was the only systematic variable discovery mechanism. Sources B, C, and D were informally captured in Memory.md §9 (research questions) but had no structured path into the VariableRegistry.

This protocol:
- Keeps the literature review focused on Source A (its natural strength)
- Distributes B/C/D capture across the skills that already observe those signals
- Standardizes the capture template so all entries are comparable
- Uses the weekly review as the cleanup/classification layer
- Preserves the quarterly review as the sole promotion gate (no change)

No new scheduled tasks are needed. No existing skill cadences change. The daily skills get a lightweight additional step. The weekly review gets a cleanup responsibility. The VariableRegistry gains more entries, which the quarterly review evaluates.

---

## 7. Discipline Rules

- **Discovery is additive, not distracting.** If discovery takes more than 2-3 minutes in a daily skill run, you're overdoing it. The brief's job is the scorecard. The rec's job is the decision. Discovery is a side effect, not the main output.
- **Honest evidence labels.** Don't inflate "I saw this once" into "Moderate evidence." Anecdotal means anecdotal. The quarterly review needs honest input to make good promotion decisions.
- **No self-promotion.** A skill that discovers a variable does not get to promote it. Only the quarterly review promotes, with Gerald's sign-off.
- **Carry forward the rejection list.** If a variable was rejected (in quarterly review or literature review), don't re-discover it unless new evidence addresses the specific failure. Check VariableRegistry for Status = Rejected before writing a new Candidate.
- **Registry hygiene.** The weekly signal-review is responsible for ensuring Candidates don't rot. If a Candidate has no new evidence after 8 weeks, it should be recommended for REJECT at the next quarterly review.
