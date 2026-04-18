# Evidence-Graded Decision Framework for High-Stakes Decisions
## A generalizable LLM system prompt derived from Gerald's trading methodology

---

## Core Concept

You have built a **hierarchical, evidence-graded decision system** optimized for **domain-specific, repeatable, high-stakes decisions under uncertainty**. The system has three load-bearing components:

1. **Evidence grading**: rank inputs by credibility (A/B/C), never padding with weak signals
2. **Sequential decision steps**: a deterministic N-step process that gates each decision stage
3. **Persistent memory with real-time updates**: working state + performance tracking + systematic review cycles

This architecture is independent of trading and transfers to any field requiring:
- Rapid synthesis of heterogeneous data sources
- Rejection of narrative/hype in favor of evidence
- Measurable decision outcomes
- Iterative methodology refinement

---

## Generalized Architecture

### Layer 1: Evidence-Grade Schema

Define a three-tier credibility ranking for your domain:

| Grade | Definition | Example use |
|-------|-----------|-------------|
| **A** | Peer-reviewed, replicated across contexts, coherent mechanism, long track record | Foundational variable; gates decisions alone |
| **B** | Moderate evidence, regime-dependent, thinner academic coverage, some replication | Confirms Grade A or breaks ties |
| **C** | Small samples, proxy-sensitive, narrative-heavy, single study | Context-setting only; banned from decision promotion |

**Discipline rule:** Never advance a decision on Grade C or below evidence. Never hide weak signals behind jargon. Fail-loud when Grade A data is missing.

### Layer 2: Deterministic N-Step Decision Sequence

Structure every decision as a fixed-sequence gating process. Use **Stop-If-False logic**: if any step fails, output "No action" rather than forcing the next step.

Template:
- **Step 1:** Context identification (regime, environment, constraint)
- **Step 2:** Structural anchor (slow variables, capacity, constraints)
- **Step 3:** Tactical signal (momentum, sentiment, catalysts)
- **Step 4:** Forward-looking catalyst (what reprices the decision)
- **Step 5:** Risk overlay (crowding, capacity, volatility, correlation)
- **Step 6:** Score aggregation (sum or weighted rule; Grade A only)
- **Step 7:** Expression choice (direct vs. hedged vs. wait)
- **Step 8:** Explicit invalidation criteria (what kills the thesis)

**Output gate:** Only promote to action if |score| ≥ threshold AND Step 8 is concrete (not narrative).

### Layer 3: Persistent Working Memory

Maintain two parallel memory systems:

**A. Working Memory (per-session, actionable state)**
- Current decisions + reasoning
- Open commitments / positions
- Key variables with latest readings
- Upcoming decision points (catalysts)

**B. Auto-Memory (persistent across sessions, retrospective)**
- User profile & constraints
- Feedback rules & behavioral guardrails
- Project state & milestones
- Performance reconciliation (what worked, what didn't)

**Update discipline:** Write to memory immediately when state changes — don't batch to end of session.

### Layer 4: Systematic Review Cycles

Run three nested review frequencies:

| Cycle | Frequency | Scope | Example |
|-------|-----------|-------|---------|
| **Micro** | Per decision | Scorecard compliance, evidence grades, gating logic | Daily trade rec checklist |
| **Meso** | Weekly | Signal outcomes, causality audits, system performance | Weekly performance review |
| **Macro** | Quarterly | Methodology fitness, variable decay, pipeline refresh | Meta-review of the review |

**Each cycle produces:** findings + metric (e.g., hit rate, alpha decay) + actions (promote/demote/retire variables).

---

## Transferable Applications

### Domain: Hiring Decisions

```
Grade A evidence: Reference interviews (blind), work-sample tests, job stability history
Grade B: Prior-employer title, education, technical assessment scores
Grade C: Interview impression, "culture fit", alma mater

8 steps:
1. Regime: Hiring urgency (hot market vs low churn), role seniority
2. Structural: Salary band, team composition, career-growth readiness
3. Tactical: Reference quality, work-sample ranked vs. cohort
4. Catalyst: Start-date pressure, competing offer, role change
5. Risk: Key-person dependency post-hire, skill-gap cost, retention risk
6. Score: S+T+C+R decision rule
7. Expression: Full-time vs. contract-to-hire vs. wait for better match
8. Invalidation: Failed reference check, no-show on work sample, counteroffer accepted

Memory: Open roles + candidate pipeline + past hire performance + team constraints + salary trend.
Cycle: Per-hire decision (micro), weekly hiring metrics (meso), quarterly hiring system audit (macro).
```

### Domain: Investment Portfolio Rebalancing

```
Grade A: Realized correlations (5y rolling), valuation spread (PE deciles), dividend yield history
Grade B: Analyst revisions, fund flows, volatility regime
Grade C: "Tech stocks are hot", newsletter sentiment, stock-picker timing

8 steps:
1. Regime: Bull/bear/ambiguous, correlation state, liquidity
2. Structural: Sector weights vs. benchmark, drawdown tolerance, ESG constraint
3. Tactical: Trend, valuation vs. peers, earnings surprise flow
4. Catalyst: Earnings season, rate decision, policy announcement
5. Risk: Realized volatility, skew, concentration, single-stock risk
6. Score: Aggregate rebalancing signal
7. Expression: Full rebalance vs. trim vs. hold
8. Invalidation: Stop-loss breach, thesis volatility spike, tax-loss harvest window miss

Memory: Holdings + cost basis + tax status + performance attribution + rebalance history.
Cycle: Per-rebalance (micro), quarterly performance review (meso), annual strategy audit (macro).
```

### Domain: Product Launch Go/No-Go

```
Grade A: Beta user retention, product-market fit survey (N>100), competitor pricing
Grade B: Sales pipeline feedback, internal team confidence, feature completeness %
Grade C: "We love it!", founder intuition, analyst predictions

8 steps:
1. Regime: Market timing (bull/bear), competitive intensity, regulatory environment
2. Structural: Unit economics, manufacturing capacity, customer acquisition cost vs. LTV
3. Tactical: Beta NPS, churn curve, feature completion, supply-chain status
4. Catalyst: Competitor launch, holiday season, funding round deadline
5. Risk: Inventory risk, refund rate, support overhead, brand damage if launch fails
6. Score: Go/No-go threshold
7. Expression: Full launch vs. soft launch vs. delay vs. pivot
8. Invalidation: Churn >50%, NPS <0, unit economics deteriorate, key supplier exits

Memory: Product roadmap + beta metrics + manufacturing readiness + sales funnel + past launches.
Cycle: Per decision gate (micro), weekly launch-readiness checklist (meso), post-launch retrospective (macro).
```

---

## Implementation Checklist

When adapting this framework to a new domain:

1. **Define your Grade A/B/C evidence tiers** — be specific, cite standards
2. **Write your 8-step sequence** — customize to domain, keep sequence fixed
3. **Document your scorecard rule** — how S+T+C+R aggregates to decision
4. **Set up working memory** — what goes in, update frequency, archive rule
5. **Set up auto-memory** — what persists, how indexed, quarterly consolidation
6. **Define your micro/meso/macro cycle** — frequency, metrics, output format
7. **Create an invalidation checklist** — concrete, data-driven, not narrative
8. **Track performance** — hit rate, false positive rate, variables that decayed

---

## Key Principles Transferable Across Domains

**Never skip steps in the sequence.** If Step 3 fails, output "Wait" rather than promoting Step 2 alone.

**Cite evidence grades every time you reference a signal.** Readers should know credibility instantly.

**Fail-loud on Grade A gaps.** If you can't get the data, flag it explicitly and hold the decision. Don't infer.

**Memory is decision-critical.** Update immediately. Archive systematically. Review quarterly for stale facts.

**No trade = valid output.** In your domain: No hire, No launch, No rebalance are always available options when evidence is mixed.

**Measure what moved the decision.** Track which Grade A variables actually drove outcomes. Demote variables that don't move the needle in practice — even if they're academically strong.

---

## Why This Works at Scale

- **Removes narrative bias**: Evidence grades force you to distinguish between "I feel good about this" (Grade C) and "This is replicated and causal" (Grade A).
- **Creates accountability**: Every decision is scored, every step is gated, every outcome is tracked. It's hard to hide bad judgment.
- **Enables systematic improvement**: The quarterly macro review surfaces variables that decayed, processes that failed, and methodology that needs patching.
- **Scales across teams**: If multiple people use the same evidence schema and decision sequence, their outputs are comparable and auditable.
- **Survives regime shift**: When new data arrives or markets change, the framework doesn't break — it updates the Structural/Tactical scores and runs through the gating again.

---

## Prompt Template for Your LLM

```
You are helping a user make a [domain] decision.

You have access to:
- A domain-specific evidence-grading schema (A/B/C)
- An 8-step decision sequence (fixed order, gating logic)
- Persistent working memory (current state)
- Performance history (past decisions + outcomes)

For every decision:

1. Read the user's raw input and the working memory.
2. Run the 8-step sequence in order. Stop-if-false: if any step outputs "No", output "No action" unless explicitly overridden by the user.
3. At each step, cite evidence grades (A/B/C) for every variable.
4. Aggregate the scores per your scorecard rule.
5. Verify Step 8 (invalidation) is concrete and data-driven, not narrative.
6. If |score| ≥ threshold AND Step 8 passes, promote to a recommendation.
7. Otherwise, output "Wait" or "No trade".
8. Update working memory and auto-memory immediately upon decision.
9. Schedule a micro review (this decision), meso review (weekly), macro review (quarterly).

Never:
- Pad decisions with Grade C evidence
- Force a decision when evidence is mixed
- Skip a step in the sequence
- Infer Grade A data if it's missing — fail-loud instead
- Hide reasoning behind jargon

Always:
- Show your work (scorecard, evidence grades, step sequence)
- Cite the specific data points that moved the needle
- List concrete invalidation criteria
- Update memory in real-time
- Measure and report what worked
```

---

## Reflection: What Makes This Generalizable

Your trading system works because it **divorces the decision framework from the data source**. The 8 steps, evidence grades, and review cycles would work equally well for:
- Hiring (same gating logic, different Grade A criteria)
- Product launches (same scorecard, different variables)
- Personal finance (same invalidation discipline, different risk overlay)
- Academic research (same evidence hierarchy, different replication standard)

The **shape of the decision** (hierarchical, evidence-graded, sequenced, audited) is what transfers. The **content** (what Grade A means, what the 8 steps are, what metrics you track) is domain-specific and yours to define.

The hardest part is defining Grade A. Everything else follows.
