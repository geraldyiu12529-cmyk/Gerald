# Methodology Sync Report — 2026-04-21
Source of truth: `framework/Methodology Prompt.md` (last known edit: 2026-04-21)

## Summary

| Metric | Count |
|---|---|
| Total files scanned | 36 (12 local skills + 24 scheduled tasks) |
| Files with findings | 9 |
| Total findings | 23 |
| A — GRADE-STALE | 7 (across 3 files) |
| B — VAR-MISSING | 5 (1 file) |
| C — RULE-MISSING | 3 (1 file) |
| D — SHARPE-STALE | 0 |
| E — ANCHOR-MISSING | 2 (LOW — one-time/reference tasks only) |
| F — CITATION-STALE | 3 (3 files) — **auto-patched** |
| G — SOURCE-MISSING | 3 (LOW) |

---

## Findings

### GRADE-STALE (A→B downgrades cited incorrectly) — HIGH

| File | Line | Variable | Current text | Required fix |
|------|------|----------|--------------|--------------|
| `~/.claude/scheduled-tasks/cloud-market-brief/SKILL.md` | 50 | V001 VIX | `VIX (Whaley 2009 — A)` | Change to `(B)` |
| `~/.claude/scheduled-tasks/cloud-market-brief/SKILL.md` | 51 | V007 real yields | `10Y TIPS real yield` in Grade A group | Move to Grade B group or add explicit `(B)` |
| `~/.claude/scheduled-tasks/cloud-market-brief/SKILL.md` | 52 | V004 HY OAS | `CDX HY spread in bp (Gilchrist-Zakrajšek 2012 — A` | Change to `(B)` |
| `~/.claude/scheduled-tasks/cloud-market-brief-6pm/SKILL.md` | 50 | V001 VIX | `VIX (Whaley 2009 — A)` | Change to `(B)` |
| `~/.claude/scheduled-tasks/cloud-market-brief-6pm/SKILL.md` | 51 | V007 real yields | `10Y TIPS real yield` in Grade A group | Move to Grade B group or add explicit `(B)` |
| `~/.claude/scheduled-tasks/cloud-market-brief-6pm/SKILL.md` | 52 | V004 HY OAS | `CDX HY spread in bp (Gilchrist-Zakrajšek 2012 — A` | Change to `(B)` |
| `~/.claude/scheduled-tasks/slack-ingest/SKILL.md` | 143 | V004 | `3. V004 — Credit spreads/excess bond premium (A)` | Change `(A)` to `(B)` |

**Note:** cloud-market-brief and cloud-market-brief-6pm are near-identical files. Both require the same grade fixes. The CDX HY spread is the intraday proxy for HY OAS — V004 — and carries the same A→B downgrade.

---

### VAR-MISSING (new V029–V035 variables absent from scoring skills) — HIGH

| File | Missing variable | Required location in skill |
|------|-----------------|--------------------------|
| `.claude/skills/market-brief/SKILL.md` | V029 BAB (Betting-Against-Beta) | Step 5 scorecard — single-stock + ETF S-input |
| `.claude/skills/market-brief/SKILL.md` | V030 DealerGamma | Step 5 scorecard — R-overlay modifier |
| `.claude/skills/market-brief/SKILL.md` | V031 GP/A (Gross Profitability) | Step 5 scorecard — single-stock S-input |
| `.claude/skills/market-brief/SKILL.md` | V032 CEI (Composite Equity Issuance) | Step 5 scorecard — single-stock S-input |
| `.claude/skills/market-brief/SKILL.md` | V033–V035 Faber TAA Overlay Gate | New Step 1.5 — sleeve ON/OFF state, written into scorecard header |

**Context:** market-brief is the upstream data provider for trade-rec. Its scorecard currently covers only the 2026-04-14 audit additions (V026/V027/V028) via the staging file. The 2026-04-18 meta-integration additions (V029–V035) are absent — meaning the daily scorecard does not compute Overlay Gate state or BAB/GP/A/CEI structural inputs. The cloud-brief and trade-rec skills already include these variables; market-brief needs to be brought into parity.

---

### RULE-MISSING (scoring interaction rules absent) — HIGH

| File | Missing rule | Required text |
|------|-------------|--------------|
| `.claude/skills/market-brief/SKILL.md` | V026/V009 gate | "score V026 only" on single-stock ticker — do NOT co-score V009 |
| `.claude/skills/market-brief/SKILL.md` | Overlay Gate semantics | "post-Sum × 0" for gated-off sleeve → `Taken=NO`, `Block_Reason=OverlayGateOff`, signal preserved in ledger |
| `.claude/skills/market-brief/SKILL.md` | V029/V030 sleeve caps | "1/3 of V009 risk budget" — independent factor sleeves, not aggregated into spine sizing |

**Note:** Rule 2 (V027/V004 double-count gate) is marginally covered in market-brief via "Don't double-count with HY OAS" — acceptable, no fix required for that rule.

---

### SHARPE-STALE (V028 post-decay Sharpe incorrect)

None — compliant. All scanned files that reference V028 Sharpe use the correct `0.35–0.47` (BNMA 4-run consensus) or do not cite a Sharpe value. The stale `0.6–1.0` value does not appear in any SKILL.md.

---

### ANCHOR-MISSING (workspace anchor absent) — LOW

| File | Fix |
|------|-----|
| `~/.claude/scheduled-tasks/setup-claude-code-routines/SKILL.md` | One-time reference guide — add standard anchor block at top as a best-practice, but not operationally critical (task does not write pipeline artifacts) |
| `~/.claude/scheduled-tasks/create-trading-pipeline-routines/SKILL.md` | One-time setup task — same note; no pipeline artifacts at risk |

Both files are retired/one-time tasks. No pipeline data is at risk. No action required unless these tasks are re-activated.

---

### CITATION-STALE (V027 primary anchor incorrect) — CRITICAL — **AUTO-PATCHED**

| File | Line | Previous text | Applied fix |
|------|------|---------|---------|
| `.claude/skills/daily-trade-rec/SKILL.md` | 153 | `He-Kelly-Manela 2017, Grade A` | `Adrian-Etula-Muir 2014 JF 69(6) [primary anchor]; He-Kelly-Manela 2017 JFE [secondary], Grade A` |
| `~/.claude/scheduled-tasks/cloud-market-brief/SKILL.md` | 129 | `NY Fed PD z-score — A, He-Kelly-Manela 2017` | `NY Fed PD z-score — A, Adrian-Etula-Muir 2014 JF 69(6) [primary anchor]; He-Kelly-Manela 2017 JFE [secondary]` |
| `~/.claude/scheduled-tasks/cloud-market-brief-6pm/SKILL.md` | 129 | `NY Fed PD z-score — A, He-Kelly-Manela 2017` | `NY Fed PD z-score — A, Adrian-Etula-Muir 2014 JF 69(6) [primary anchor]; He-Kelly-Manela 2017 JFE [secondary]` |

**Rationale:** The BNMA 2026-04-18 audit re-confirmed AEM 2014 JF 69(6) as the primary anchor for V027 (NY Fed primary-dealer equity/total-capital ratio z-score). HKM 2017 JFE is a secondary replication. All three files cited HKM 2017 as the sole reference, reversing the hierarchy.

---

### SOURCE-MISSING (bnma/meta-analysis/ not referenced) — LOW

| File | Note |
|------|------|
| `.claude/skills/daily-trade-rec/SKILL.md` | Does not explicitly cite `bnma/meta-analysis/` as source for V026–V035 BNMA verdicts |
| `.claude/skills/signal-review/SKILL.md` | Same — no bnma/meta-analysis/ reference |
| `.claude/skills/quarterly-methodology-review/SKILL.md` | Same — reads Trad/Coin cores but not meta-analysis directly |

Low priority — the BNMA source documents are loaded by the Methodology Prompt.md which these skills read. No action required unless explicit source tracing for V026–V035 verdicts is needed.

---

## Auto-patched (CRITICAL)

Three files were patched inline without Gerald's confirmation (CITATION-STALE is classified CRITICAL per the skill's Step 4 policy):

1. `.claude/skills/daily-trade-rec/SKILL.md` — V027 citation corrected: AEM 2014 JF 69(6) added as primary anchor, HKM 2017 demoted to secondary.
2. `~/.claude/scheduled-tasks/cloud-market-brief/SKILL.md` — same fix.
3. `~/.claude/scheduled-tasks/cloud-market-brief-6pm/SKILL.md` — same fix.

---

## Pending Gerald Confirmation (HIGH)

The following HIGH-priority findings require your sign-off before patching:

### HIGH-1 — GRADE-STALE in cloud-market-brief + cloud-market-brief-6pm

Both cloud brief files cite VIX, real yields (10Y TIPS), and CDX HY spread as Grade A. These three variables (V001, V007, V004) were downgraded A→B effective 2026-04-18. The cloud brief uses these grades in its STEP 2 variable pull and RULES sections, potentially inflating their weight as "primary triggers" vs confirmatory context.

**Proposed fix:** In both cloud-market-brief and cloud-market-brief-6pm SKILL.md files, update the STEP 2 PULL section:
- Change `VIX (Whaley 2009 — A)` → `VIX (Whaley 2009 — B)`
- Move `10Y TIPS real yield` to a Grade B group or add explicit `(B)` annotation
- Change `CDX HY spread in bp (Gilchrist-Zakrajšek 2012 — A` → `(B)`
And update the RULES section's grade description to note B status.

**Confirm patch?** (These are identical files — one edit applies to both.)

### HIGH-2 — GRADE-STALE in slack-ingest

The slack-ingest TOP-33 reference section lists `V004 — Credit spreads/excess bond premium (A)`. This is the ingest agent's reference framework — if it uses these grades to explain priority of variables in the narrative, the A citation is stale.

**Proposed fix:** Change `(A)` to `(B)` on the V004 line in the TOP-33 section of slack-ingest/SKILL.md.

**Confirm patch?**

### HIGH-3 — VAR-MISSING + RULE-MISSING in market-brief

The local market-brief skill is missing the entire 2026-04-18 meta-integration layer: no V029 BAB, no V030 DealerGamma, no V031 GP/A, no V032 CEI, and no Step 1.5 Overlay Gate. It also lacks three of the four required scoring interaction rules.

This is the most significant gap found. The daily trade-rec reads the market-brief scorecard as its primary upstream input. A market-brief that does not include meta-integration variables produces a scorecard that trade-rec must independently supplement — which it does (trade-rec has the full implementation), but the market-brief scorecard itself is incomplete as a standalone document.

**Proposed fix:** Add Step 1.5 (Overlay Gate) after Step 4 in market-brief SKILL.md, expand Step 5 to include V029/V030/V031/V032 scoring from `meta-additions-staging-{today}.md`, add the four scoring interaction rules, and add `framework/Methodology Prompt.md` reference update to "Top-33 variables".

This is a material edit to the market-brief skill. Gerald confirmation required before patching.

**Confirm patch?**

---

## Files Fully Compliant

The following 27 files passed all applicable checks:

Local skills: `signal-review`, `quarterly-methodology-review`, `news-events`, `positions-monitor`, `trade-update`, `pipeline-recovery`, `literature-review`, `system-review`, `pipeline-smoketest`, `methodology-sync`

Scheduled tasks: `daily-market-brief-8pm`, `trade-rec-daily`, `cloud-trade-rec-7pm`, `cloud-news-events-630pm`, `news-events-daily`, `preflight-audit-data`, `preflight-meta-additions`, `us-close-snapshot`, `positions-monitor` (task), `weekly-regime-signal-review`, `quarterly-methodology-review` (task), `semi-annual-literature-review`, `semi-annual-system-review`, `monthly-bootstrap-review`, `pipeline-recovery-daily`, `meta-shadow-review-2026-04-25`, `methodology-audit-6mo-review-2026-10-14`, `weekly-backup-sunday`, `workspace-tidy`, `slack-ingest` (anchor + all checks except GRADE-STALE)
