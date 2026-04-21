# Semi-Annual Literature Review — News & Event Taxonomy
## Focus: High-Evidence Event Categories and Non-Overlapping Monitoring Domains

**Purpose:** Research and document the academic and practitioner evidence for market-moving news categories. Define what the daily news-events skill should monitor, with explicit deduplication against the market-brief skill. This is NOT a variable-promotion review; it is a framework audit.

**Output:** 
- `lit-review-news-taxonomy-YYYY-MM-DD.md` — structured findings with evidence citations
- Updated `news-events/README.md` hotspot list and monitoring scope (if findings change monitoring priorities)
- Optional: Updated news-events skill description with revised watchlist boundaries

---

## Part A: Research Scope

### A1. Core Question
What categories of news/events have peer-reviewed or high-credibility evidence for moving markets, and how should monitoring be split between **daily market-brief** (regime-state variables) and **daily news-events** (discrete announcements/updates)?

### A2. Evidence Standards
- **Tier 1:** NBER, Federal Reserve, ECB, IMF, BIS working papers with pre-2020 publication or established institutional backing
- **Tier 2:** Major financial firms' published research (BlackRock, JP Morgan, etc.)
- **Tier 3:** Reputable finance journalism documenting measurable market reactions (Reuters, Bloomberg, FT)

Accept findings only if they include:
- A named asset class or correlation effect
- A measured reaction horizon (intraday, days, regime-level)
- A quantified impact (e.g., basis points, percentage move, vol spike)

Reject vague claims ("markets care about X") without empirical support.

### A3. Scope Boundaries

**IN SCOPE:**
- Central-bank decisions, statements, speeches, interviews, forward guidance
- Top-tier macro releases (inflation, labor, activity, spending; especially regime-shifters)
- Government policy: tariffs, sanctions, fiscal packages, trade restrictions, executive actions
- Geopolitical escalation/de-escalation (war, ceasefires, shipping disruptions)
- Corporate earnings, guidance, profit warnings
- Funding/liquidity events (auctions, repo stress, dealer constraints)
- Commodity-specific shocks (OPEC, EIA, supply disruptions)
- Regulatory/legal actions (approval, ban, enforcement)
- Credit deterioration and restructuring
- Political communication (Truth Social, official channels) when policy-linked
- News tone, novelty, and textual signal quality

**OUT OF SCOPE:**
- Analyst commentary and price-target changes (unless from primary earnings)
- Generic market "takes" and opinion pieces
- Recycled headlines and low-substance press releases
- Sensational political commentary without implementation path

---

## Part B: Literature Review Template

For each category below, research and document:

### B1. Central-Bank Communication
**Research questions:**
- What is the evidence that central-bank statements, speeches, and press conferences move rates, FX, equities, and credit?
- How large and persistent are the effects?
- Do unscheduled remarks differ in impact from scheduled meetings?
- How does communication compare to actual rate moves in magnitude?

**Search strategy:**
- NBER: "central bank communication" + "asset prices"
- Federal Reserve economic letters on policy communication
- ECB working papers on communication effects
- Key authors: Blinder, Kohn, Lucca & Trebbi, Lucca & Nosbusch

**Document:**
- Key papers and findings
- Estimated effect sizes (basis points on yields, % on indices, etc.)
- Persistence (minutes to months; separate by asset)
- Implication: What daily news-events should capture here (e.g., unscheduled remarks, guidance shifts, vs. scheduled meetings already in calendar)

---

### B2. Top-Tier Macro Data Releases
**Research questions:**
- Which macro releases have the strongest evidence for market repricing?
- Are surprise components more important than the actual release?
- How do effects vary by regime (inflation scare vs. growth scare)?
- Which assets move most reliably to macro surprises?

**Search strategy:**
- NBER: "macro announcement" + "asset prices" or "equity returns"
- Federal Reserve work on macro surprises and financial conditions
- Andersen, Bollerslev, Diebold papers on announcement effects
- ECB/Eurostat on European macro calendar impact

**Document:**
- Ranked list of "high-impact" macro releases by evidence quality
- Effect sizes by asset class (rates, FX, equities, vol, commodities)
- Timing (intraday vs. multi-day drift)
- Implication: Daily news-events captures the *surprise*, while market-brief captures the *forecast/consensus* — define the handoff clearly

---

### B3. Government Policy / Fiscal / Trade / Sanctions
**Research questions:**
- What is the evidence that tariff announcements, fiscal packages, and sanctions move markets?
- How quickly do markets reprice?
- Do announcement vs. implementation matter?
- Which assets are most sensitive (FX, sectors, commodities)?

**Search strategy:**
- NBER: "trade policy" + "stock returns" or "exchange rates"
- Trump tariff papers (2018–2020, 2024–present)
- Barrot, Servenay papers on tariff surprises
- BIS on policy uncertainty indices and market impact

**Document:**
- Evidence for tariff impacts (direction, magnitude, persistence)
- Fiscal/debt-ceiling effects
- Sanctions effects (sectoral vs. asset-class)
- Implication: Which policy channels daily news-events should actively monitor (e.g., Truth Social, official trade office, Treasury statements) vs. market-brief tracking policy-uncertainty indices

---

### B4. Major Geopolitical Escalation / De-Escalation
**Research questions:**
- What is the evidence that war, ceasefires, and shipping disruptions move asset prices?
- Which assets are most affected?
- How persistent are the effects?
- How much of the move is vol/risk-premium vs. directional?

**Search strategy:**
- IMF working papers on geopolitical risk and asset prices
- Caldara & Iacoviello on geopolitical risk indices
- Ukraine war literature (2022–present) on energy, equity, and FX effects
- Commodity research on supply shocks vs. sentiment

**Document:**
- Effect sizes by asset (oil, gold, FX, equities, vol)
- Persistence (immediate jump vs. weeks-long repricing)
- Implication: Which geopolitical developments daily news-events should flag (e.g., chokepoint disruptions, escalation/de-escalation) vs. market-brief regime tracking (e.g., risk-on/off, crude oil levels)

---

### B5. Corporate Earnings, Guidance, Profit Warnings
**Research questions:**
- What is the evidence that earnings announcements and guidance changes move stock prices?
- Do tone and margin changes matter beyond the headline number?
- How much is permanent vs. drift?
- How important are conference-call signals?

**Search strategy:**
- NBER: "earnings announcements" + "stock returns"
- Campbell, Lettau, Malkiel, Xu on stock-level predictability
- Cohen, Lou, Malloy on conference call tone
- Loh & Stulz on SEC filings and stock returns

**Document:**
- Effect sizes and persistence
- Implication: Daily news-events focuses on *out-of-consensus* guidance and margin shocks; market-brief tracks sector earnings-season cycles and beta

---

### B6. Funding, Liquidity, Market-Functioning Events
**Research questions:**
- Do Treasury auctions, repo stress, and dealer constraints affect financial conditions?
- How quickly do funding shocks propagate across asset classes?
- What are the spillovers to equity and commodity liquidity?

**Search strategy:**
- Federal Reserve Bank of New York on repo, Treasury auctions, dealer constraints
- Nagel on dealer inventory dynamics
- Goldstein & Jiang on Treasury market depth
- Recent papers on QT and reserve tightness

**Document:**
- Evidence for liquidity shocks affecting cross-asset vol, bid-ask spreads, and repricing horizon
- Implication: Daily news-events captures *stress events* (auction failures, repo spikes); market-brief tracks Treasury depth, dealer utilization, reserve levels

---

### B7. Commodity-Specific Supply/Demand Shocks
**Research questions:**
- What is the evidence that OPEC meetings, EIA releases, and production outages move oil and gas prices?
- How persistent are the effects?
- Do they spill into inflation and FX?

**Search strategy:**
- BIS on oil price shocks and macroeconomic effects
- Kilian on oil supply shocks vs. demand shocks
- EIA/IEA data on inventory surprises and price elasticity
- Crypto commodity analogue: mining disruptions, fork events

**Document:**
- Effect sizes and persistence for physical commodities
- Spillover evidence to equities and FX
- Implication: Daily news-events tracks supply shocks (outages, OPEC surprises); market-brief tracks inventory levels, production trends

---

### B8. Regulatory / Legal / Enforcement Events
**Research questions:**
- Do SEC/CFTC approvals, bans, and enforcement actions move stock prices?
- Are effects strongest in crypto and fintech sectors?
- How persistent are they?

**Search strategy:**
- BIS on regulatory announcements and crypto asset prices
- SEC/CFTC case studies and market reactions
- Crypto approval literature (ETF approvals, custody rules)
- Tech/healthcare sector regulatory papers

**Document:**
- Evidence for regulatory shocks in exposed sectors
- Implication: Daily news-events captures *surprise* regulatory actions; market-brief tracks regulatory calendars and approval probabilities

---

### B9. Credit Deterioration / Restructuring / Default Risk
**Research questions:**
- Do downgrades, distress signals, and restructuring announcements move credit and equity prices?
- How much is information vs. mechanical?
- What is the lead/lag structure?

**Search strategy:**
- BIS on credit events and spillovers
- Huang & Huang on credit spreads and default risk
- Gilson & Vetsuypens on distressed issuers
- Recent papers on fallen angels and rating downgrades

**Document:**
- Evidence for credit shocks propagating to equities and indices
- Lead/lag structure (distress signal → spread widening → downgrade)
- Implication: Daily news-events captures *early distress signals* (funding warnings, covenant pressure); market-brief tracks credit spreads

---

### B10. Political Social Media / Informal Communication
**Research questions:**
- Do Trump Truth Social posts, leaked policy chatter, and informal government channels move markets?
- What is the effect size and persistence?
- Which assets are most sensitive (FX, indices, sectors)?
- How do you separate signal from noise?

**Search strategy:**
- NBER papers on Trump tweets and Fed/Treasury effects
- Reuters/Bloomberg analysis of 2024–2026 tariff communication
- IDEAS/RePEc on social media and asset prices
- Politician communication literature

**Document:**
- Evidence for political communication moving FX, rates, sector equities
- Filters for credibility and policy relevance (implementation power, asset exposure, prior follow-through)
- Implication: Daily news-events monitors *credible, policy-linked* communications; market-brief ignores rhetorical noise

---

### B11. News Tone, Novelty, and Textual Features
**Research questions:**
- Do machine-readable features (surprise, sentiment, novelty) predict near-term returns or volatility?
- Is the signal durable or does it decay quickly?
- What is the evidence for redundancy (duplicated headlines) reducing signal?

**Search strategy:**
- NBER: "news sentiment" + "stock returns"
- Gentzkow & Shapiro on media slant and asset prices
- Tetlock on language and financial markets
- Gentzkow, Kelly, Taddy on media and returns

**Document:**
- Evidence for novelty and sentiment predicting vol and returns
- Persistence and cost implications (is signal large enough to trade after costs?)
- Implication: Daily news-events filters by *novelty* and *non-redundancy*

---

### B12. What to Ignore (Noise Filters)
**Research questions:**
- What is the evidence that analyst commentary, generic opinion, and low-substance press releases do NOT move markets persistently?
- How quickly do duplicated headlines reverse?

**Search strategy:**
- NBER on analyst forecast revisions vs. actual earnings
- Literature on noise vs. information
- Brown et al. on mispricing reversals and analyst chatter

**Document:**
- Evidence for low signal-to-noise in analyst commentary and recycled headlines
- Implication: Daily news-events explicitly *excludes* these categories to focus monitoring

---

## Part C: Non-Overlap Framework

### C1. Market-Brief Scope (Regime State Variables)
Daily market-brief tracks **static or slowly-changing** regime states:
- Central-bank rates and forward guidance (as a state, not a change)
- Top-tier macro data (latest prints, not surprises)
- Policy stance (tariff regime, fiscal regime, as a state)
- Commodity levels (crude, gas, metals)
- VIX, credit spreads, Treasury yields
- FX levels
- Equity index levels and sector beta
- Funding conditions and repo rates (as a state)

**Cadence:** Daily snapshot at a fixed time (before market open)

### C2. Daily News-Events Scope (Discrete Announcements & Surprises)
Daily news-events captures **changes or new information**:
- Central-bank *announcements, speeches, surprise guidance shifts* (not the rate level itself)
- Macro *surprises* (actual vs. consensus; not the forecast)
- Policy *announcements* (tariff shift, sanctions, fiscal bill passes) — not the regime level
- Geopolitical *events* (war escalates, ceasefire, shipping disruption) — not the risk-on/off state
- Earnings *surprises* (guidance beats/misses) — not sector earnings-season calendar
- Funding *stress events* (auction failure, repo spike) — not repo rate level
- Commodity *shocks* (OPEC surprise, outage) — not crude price level
- Regulatory *decisions* (approval, ban, enforcement) — not regulatory calendar
- Credit *distress signals* (covenant breach warning, downgrade) — not spread level
- Political *communication with policy implications* — not every post
- News *with high novelty/surprise* — not recycled headlines

**Cadence:** Intraday or daily as events break

### C3. Handoff Rules
To avoid double-counting and confusion:

1. **Market-brief produces the regime context; news-events produces the *change* or *surprise* within that regime.**
   - Market-brief: "Fed funds rate is 4.5%, term premia at +120bps"
   - News-events: "Fed Chair signals 25bp cut probability increased from 15% to 40%"

2. **Market-brief feeds news-events for interpretation; news-events triggers market-brief re-run if needed.**
   - A large geopolitical shock (news-events capture) may require an out-of-cycle market-brief update if risk regime shifts sharply

3. **No schedule overlap:** Market-brief runs before news-events in the daily pipeline (20:00 → 20:10 UTC+8). News-events does not re-rank variables; it flags *what changed in the last 24 hours* that market-brief did not capture.

4. **Novelty is the gating filter.** If an event was already fully priced into market-brief states (e.g., the Fed decision was 99% consensus), news-events still mentions it for the record but does not elevate it as a "new driver."

---

## Part D: Research Execution Checklist

### D1. Search & Documentation
- [ ] **Central-bank communication:** 3–5 NBER/Fed papers, effect sizes documented
- [ ] **Macro surprises:** 3–5 papers, list of "high-impact" releases ranked by evidence
- [ ] **Policy (tariffs, fiscal, sanctions):** 3–5 papers, asset-by-asset effect table
- [ ] **Geopolitics:** 2–3 IMF/BIS papers, asset effects table
- [ ] **Earnings:** 3–4 papers, effect sizes and drift evidence
- [ ] **Funding/liquidity:** 2–3 Fed/BIS papers, spillover map
- [ ] **Commodity shocks:** 2–3 papers (oil, ags, metals), spill-over evidence
- [ ] **Regulatory/legal:** 2–3 papers (crypto + sector case studies)
- [ ] **Credit deterioration:** 2–3 papers on downgrades and spreads
- [ ] **Political communication:** 2–3 papers (Trump tweets, policy leaks, implementation filters)
- [ ] **News tone/novelty:** 2–3 papers on textual signal and decay
- [ ] **Noise filters:** 2–3 papers on analyst chatter, redundancy, reversal

### D2. Evidence Quality Assurance
- [ ] Every finding includes author, year, publication venue (NBER, Fed, BIS, etc.)
- [ ] Every finding includes a measured effect size (bps, %, volatility, correlation)
- [ ] Every finding includes a reaction horizon (intraday, days, weeks, regime)
- [ ] Every finding includes named asset classes (rates, FX, equities, commodities, vol, credit)
- [ ] Rejected claims without empirical backing are logged and explained

### D3. Implications for News-Events Skill
- [ ] Current hotspot list reviewed and validated against findings
- [ ] Any changes to monitoring priorities documented
- [ ] Handoff rules between market-brief and news-events clarified and codified
- [ ] Noise-filter rules documented with evidence
- [ ] Political communication filters (credibility, implementation power) formalized

### D4. Optional: Variable Candidate Pipeline
- [ ] Any new tradeable variables suggested by the news taxonomy research logged separately
- [ ] Do not promote to production; pass to quarterly-methodology-review for vetting

---

## Part E: Output Structure

### E1. Main Document: `lit-review-news-taxonomy-YYYY-MM-DD.md`

**Sections:**
1. Executive summary (findings, implications, changes to news-events scope)
2. Central-bank communication (papers, findings, effect sizes, implications)
3. Macro surprises (papers, findings, high-impact release list, implications)
4. Policy announcements (papers, findings, asset-by-asset table, implications)
5. Geopolitical events (papers, findings, asset effects, implications)
6. Earnings surprises (papers, findings, drift evidence, implications)
7. Funding & liquidity (papers, findings, spillover map, implications)
8. Commodity shocks (papers, findings, asset effects, implications)
9. Regulatory/legal (papers, findings, sector focus, implications)
10. Credit deterioration (papers, findings, lead/lag structure, implications)
11. Political communication (papers, findings, signal/noise filters, implications)
12. News tone & novelty (papers, findings, persistence, implications)
13. Noise filters (papers, findings, false-positive costs, implications)
14. Recommendations for news-events skill (changes to hotspot list, monitoring scope, handoff rules)
15. Evidence audit (table: finding → source → effect size → persistence → confidence)

### E2. Updated Files (if applicable)
- `news-events/README.md` — updated hotspot list and watchlist scope
- `news-events` skill description — updated with revised boundaries

---

## Part F: Success Criteria

✓ **Evidence is peer-reviewed or high-credibility institutional sourcing; vague claims are rejected.**

✓ **Every finding includes effect size, persistence, and asset class; "just matters" is not accepted.**

✓ **Market-brief and news-events scopes are explicitly non-overlapping and documented.**

✓ **Noise filters are evidence-grounded, not opinion.**

✓ **Political communication has formal credibility and implementation filters.**

✓ **Any recommended changes to daily workflows are justified by findings and include estimated impact.**

✓ **The output is referenceable and citeable for future methodology reviews.**

---

## Part G: Research Baseline

You are being provided with a curated reading list above (Parts 3–7 of the input document). Your review will:

1. **Validate** these rankings against primary literature (search NBER, Fed, BIS, IMF for the cited sources and papers)
2. **Deepen** each category with 2–4 additional papers beyond what is cited
3. **Quantify** effect sizes where the input is qualitative ("High" → "±50–150 bps on 10Y yields, persistent for 2–5 days")
4. **Clarify** the handoff between market-brief and news-events scope
5. **Formalize** noise filters with evidence and cost implications

---

## Notes

- **Do not run the daily-trade-rec, daily-news-events, or market-brief skills during this review.** This is a framework audit, not a production run.
- **Do not modify variable-promotion logic or grade-A variable core lists.** Focus exclusively on news-event taxonomy and monitoring scope.
- **Use `fail-loud` if Grade-A papers cannot be found for a category; document the gap.**
- **Cross-reference findings against Gerald's `Coin core.md` and `Trad core.md` where applicable** (e.g., if geopolitical risk is a ranked variable, what does the literature say about the news categories that move it?).
- **Estimated effort:** 4–6 hours of research and synthesis.

---

**Created:** 2026-04-17  
**Status:** READY TO EXECUTE (do not run until explicitly requested)
