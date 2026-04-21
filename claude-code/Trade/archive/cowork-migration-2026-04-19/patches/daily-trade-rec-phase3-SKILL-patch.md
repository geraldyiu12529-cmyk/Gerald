# Phase 3 Patch — daily-trade-rec SKILL.md (meta-integration consumer)

**Source:** 2026-04-18 meta-integration deployment (`deployment-memo-2026-04-18.md`, `meta-analysis-integration-plan-2026-04-18.md`).
**Applies when:** 2026-04-25 shadow-mode review (`meta-shadow-review-2026-04-25.md`) returns GO verdicts for V029, V033, V034, V035. V030/V031/V032 remain MISSING and are NOT consumed by this patch.
**Target file (Windows):** `C:\Users\Lokis\Documents\Claude\skills\daily-trade-rec\SKILL.md`
**Scope test:** edits total ~2.1 KB against the ~18 KB SKILL.md (~12%) → minimum-surface edit, NOT full rewrite.

## Summary

Phase 3 wires four behaviors into `daily-trade-rec`:

1. **Extend Step 1 startup reads** to include `meta-additions-staging-{YYYY-MM-DD}.md`.
2. **Insert a new Step 1.5 — Overlay Regime Gate** between Step 1 and Step 2. Applies the Faber TAA multiply-by-zero sleeve logic per `Methodology Prompt.md §Step 1.5` and `Risk Rules.md §4.B` / §7 checklist item 7.
3. **Extend Step 5 pre-entry checklist** with items 7 (overlay gate ON) and 8 (V027 sizing tier applied), matching `Risk Rules.md §7`.
4. **Extend Step 8 SignalLedger append** to populate the four new cols (positions 33–36: `overlay_gate_status`, `v027_regime_bucket`, `bab_sleeve_weight`, `dealergamma_sleeve_weight`) on every promoted and near-miss row. A Sum +3 signal whose sleeve is overlay-gated OFF is logged as **Promoted, Taken=NO, Block_Reason=OverlayGateOff** (per `Methodology Prompt.md §Step 1.5` gating semantics).

Sum arithmetic is untouched. The overlay gate multiplies post-Sum position size by 0 — it does NOT subtract from the Sum. V030/V031/V032 stay MISSING; only V029 / V027 / V033 / V034 / V035 participate in Phase 3 scoring if they received GO verdicts on 2026-04-25.

## SignalLedger column-read order (positions 33–36, schema confirmed 2026-04-18)

| # | Col | Value domain | Source this run |
|---|---|---|---|
| 33 | `overlay_gate_status` | `equity={ON\|OFF}\|commodity={ON\|OFF}\|crypto={ON\|OFF}` (string, pipe-delimited per sleeve) | staging file V033/V034/V035 Faber table |
| 34 | `v027_regime_bucket` | `expansion` \| `neutral` \| `contraction` \| `MISSING` | staging file V027 reconciliation row |
| 35 | `bab_sleeve_weight` | float 0.0–0.333 (capped at 1/3 of V009 budget per Risk Rules §8) | staging file V029 BAB proxy (0 if ANTI-BAB) |
| 36 | `dealergamma_sleeve_weight` | float 0.0–0.333 or `None` if V030 still MISSING | staging file V030 (expected `None` until subscription confirmed) |

Populate on **every** row appended this run, even near-misses, even rows whose sleeve is gated OFF. A blank or `MISSING` value is informationally distinct from zero — do not conflate.

## Before/after edits

### Edit 1 — Add staging file to Step 1 reads

**Anchor:**
```markdown
9. *(optional)* Most recent `/mnt/Trade/signal-review-*.md` — read only the `## 8. Escalation Flags` section if it exists. If the section is present, carry the flags forward into the rec's §2 (Regime Read) as a one-line notice per flag.
```

**Replace with:**
```markdown
9. *(optional)* Most recent `/mnt/Trade/signal-review-*.md` — read only the `## 8. Escalation Flags` section if it exists. If the section is present, carry the flags forward into the rec's §2 (Regime Read) as a one-line notice per flag.
10. **(Phase 3, post-2026-04-25)** `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` — produced by `preflight-meta-additions-1952pm` at 19:52. Extract `overlay_gate_status` (per-sleeve ON/OFF), `v027_regime_bucket`, `v029_bab_spread`. If missing, treat as fail-loud — Step 1.5 blocks ALL Phase-3-gated sleeves and logs Block_Reason=OverlayStagingMissing in Step 8.
```

### Edit 2 — Insert Step 1.5 between Step 1 and Step 2

**Anchor (end of Step 1 into Step 2 header):**
```markdown
If a framework file is missing, stop and surface the gap — do not fabricate the methodology. If an upstream artifact is missing, log it under "Data Gaps" in the output and proceed; do not silently skip. The reason these four upstream files are non-negotiable is that today's recommendation must be reproducible from named, dated source files; if you can't cite where a fact came from, it can't carry a Grade-A claim.

## Step 2 — Build the Upstream Synthesis block
```

**Replace with:**
```markdown
If a framework file is missing, stop and surface the gap — do not fabricate the methodology. If an upstream artifact is missing, log it under "Data Gaps" in the output and proceed; do not silently skip. The reason these four upstream files are non-negotiable is that today's recommendation must be reproducible from named, dated source files; if you can't cite where a fact came from, it can't carry a Grade-A claim.

## Step 1.5 — Overlay Regime Gate (Phase 3, added 2026-04-25)

This step sits between Step 1 (reads) and Step 2 (synthesis). It is **non-additive to Sum** — it is a binary sleeve-on/sleeve-off switch that multiplies post-Sum position size by 0 for any gated-off sleeve. Authoritative: `Methodology Prompt.md §Step 1.5` and `Risk Rules.md §4.B, §7 item 7, §8`.

**Inputs (from the staging file read in Step 1 item 10):**

- `overlay_gate_status` — per-sleeve ON/OFF from V033/V034/V035 (Faber 10m-SMA at previous month-end close).
- `v027_regime_bucket` — expansion / neutral / contraction. Drives Risk Rules §1.B gross-exposure tier.
- `v029_bab_spread` — USMV − SPLV 12m. If spread > 0, BAB sleeve is active (long low-β / short high-β stocks); if ≤ 0, ANTI-BAB and the sleeve is flat this month.
- `v030_dealergamma` — expected MISSING until subscription confirmed; do not block on its absence.

**Sleeve mapping (asset class → sleeve):**

| Asset class | Gated by | Variables in scope |
|---|---|---|
| Equity (SPY, QQQ, individual stocks) | V033 SPY Faber gate | NVDA, TSLA, AAPL, GOOGL, AMZN, META, TSM, INTC, MU, PYPL, PLTR, WDC, SPY, QQQ |
| International equity | V033 EFA optional | EWJ, EWY |
| Commodity | V034 GSCI Faber gate | Brent, WTI, Gold, Silver, Copper, Palladium, Platinum |
| Crypto | V035 BTC-USD Faber gate | BTC, ETH |
| FX, rates | Not gated (no overlay applies) | EURUSD, USDJPY, DGS2, DGS10 |

**Gate-application logic (per asset under scoring):**

1. Identify the asset's sleeve from the table above.
2. If the sleeve is **ON**: proceed to Step 2 normally. Signal is entry-eligible.
3. If the sleeve is **OFF**: the asset is still scored through Steps 2–5 (S/T/C/R, Sum, invalidation, stop, target) because the ledger needs the full score record, but `Taken=NO` and `Block_Reason=OverlayGateOff` will be written in Step 8 regardless of |Sum|. The §3 Recommendations Table omits the row; the §4 Theses Not Taken section flags it.
4. If the sleeve status is `MISSING` (staging file absent or staging row missing for that sleeve): treat as **OFF** (fail-loud default). Block_Reason=OverlayStagingMissing.

**Gating is non-additive.** Do NOT reduce S/T/C/R or Sum because a sleeve is OFF. The Sum is what the methodology says it is; the overlay just prevents today's *execution* on that sleeve.

**V027 sizing tier (from v027_regime_bucket):**

- `expansion` → full inverse-ATR sizing (no tier adjustment)
- `neutral` → standard sizing
- `contraction` → halve gross exposure on all risk-asset sleeves (binds alongside quarter-Kelly; take the more restrictive)

The V027 tier is applied *after* Step 5 per-position sizing is computed. Record the tier in the §7 Pre-Entry Checklist (item 8) and in SignalLedger col 34.

**V029 BAB sleeve weight:**

- If `v029_bab_spread > 0` (BAB regime): BAB sleeve is active on single-stock longs; sleeve weight ≤ 1/3 of V009 (momentum) risk budget. Compute `bab_sleeve_weight` as the fraction of V009 budget allocated today. Correlation gate applies — a BAB sleeve leg and a V009 spine long on the same ticker size to the combined sector cap, not double-sized.
- If `v029_bab_spread ≤ 0` (ANTI-BAB): `bab_sleeve_weight = 0.0`.

**V030 DealerGamma sleeve weight:**

- Expected MISSING this cohort. If value is present, compute `dealergamma_sleeve_weight` analogously (≤ 1/3 V009 budget). Otherwise write `None` to col 36.

**Output of Step 1.5:** a one-paragraph gate panel written into the rec's §2 Regime Read, naming the sleeve status per class, the V027 bucket, and the BAB regime. This panel is read by positions-monitor via the output rec; see `positions-monitor-phase3-SKILL-patch.md`.

## Step 2 — Build the Upstream Synthesis block
```

### Edit 3 — Extend Step 5 pre-entry checklist (items 7 and 8)

**Anchor:**
```markdown
6. Catalyst asymmetry stated — surprise-dependent vs confirmation-dependent. Surprise-dependent catalysts carry positive convexity and are preferred; confirmation-dependent catalysts where the bar is elevated (e.g. an earnings print already discounted) carry poor asymmetry and usually fail the overall thesis even when scored C+1.

"No trade" is always a valid output.
```

**Replace with:**
```markdown
6. Catalyst asymmetry stated — surprise-dependent vs confirmation-dependent. Surprise-dependent catalysts carry positive convexity and are preferred; confirmation-dependent catalysts where the bar is elevated (e.g. an earnings print already discounted) carry poor asymmetry and usually fail the overall thesis even when scored C+1.
7. **Step 1.5 Overlay Gate status for this sleeve is ON** (Phase 3, added 2026-04-25). If OFF → position size × 0 → no trade regardless of Sum. Authoritative: `Risk Rules.md §7` item 7.
8. **V027 intermediary-capital sizing tier applied** (Phase 3, added 2026-04-25). If `v027_regime_bucket = contraction` (z < −1σ), the halved-gross-exposure rule is the binding constraint above quarter-Kelly. Authoritative: `Risk Rules.md §1.B` and `§7` item 8.

"No trade" is always a valid output.
```

### Edit 4 — Extend Step 8 SignalLedger append with 4 new cols

**Anchor:**
```markdown
**For promoted signals** (|Sum| ≥ 3): append one row with ID (next sequential P###), Type='Promoted', Date, Asset, AssetClass, Direction, S/T/C/R/Sum, Entry_Price, ATR_Stop, Target_TP1, Target_TP2, Invalidation, Inv_Date, VIX_at_Entry, Regime_Label, Taken (check Memory.md §2), Status='OPEN'. Exit columns blank.

**For near-miss signals** (|Sum| = 2, or |Sum| ≥ 3 blocked): append one row with ID (next sequential N###), Type='Near-Miss', same score fields, Blocking_Leg, Block_Reason, Price_at_Signal, VIX_at_Signal, Status='OPEN'. Exit columns blank.
```

**Replace with:**
```markdown
**For promoted signals** (|Sum| ≥ 3): append one row with ID (next sequential P###), Type='Promoted', Date, Asset, AssetClass, Direction, S/T/C/R/Sum, Entry_Price, ATR_Stop, Target_TP1, Target_TP2, Invalidation, Inv_Date, VIX_at_Entry, Regime_Label, Taken (check Memory.md §2), Status='OPEN'. Exit columns blank.

**For near-miss signals** (|Sum| = 2, or |Sum| ≥ 3 blocked): append one row with ID (next sequential N###), Type='Near-Miss', same score fields, Blocking_Leg, Block_Reason, Price_at_Signal, VIX_at_Signal, Status='OPEN'. Exit columns blank.

**Phase 3 meta-integration cols (positions 33–36, added 2026-04-25).** On every row — promoted AND near-miss — write:

| Col | Value source | Missing-value rule |
|---|---|---|
| 33 `overlay_gate_status` | `equity={ON\|OFF}\|commodity={ON\|OFF}\|crypto={ON\|OFF}` — from Step 1.5 gate panel | write `MISSING` string if staging absent |
| 34 `v027_regime_bucket` | `expansion`/`neutral`/`contraction` — from Step 1.5 | write `MISSING` if staging absent |
| 35 `bab_sleeve_weight` | float 0.0–0.333 — from Step 1.5 | write `None` if V029 MISSING |
| 36 `dealergamma_sleeve_weight` | float 0.0–0.333 — from Step 1.5 | write `None` if V030 MISSING (expected for this cohort) |

**Overlay-gated Sum +3 handling (per `Methodology Prompt.md §Step 1.5`).** A signal with |Sum| ≥ 3 on an overlay-OFF sleeve is logged as Type='Promoted', Taken='NO', Status='OPEN', Block_Reason='OverlayGateOff' (or 'OverlayStagingMissing' if fail-loud). This preserves the Sum arithmetic record for out-of-sample tracking while flagging why the trade wasn't executed. signal-review reads these rows to mark-to-market the overlay gate's hit rate separately from the Taken=YES population.
```

### Edit 5 — Extend §7 Pre-Entry Checklist output template

**Anchor:**
```markdown
## 7. Pre-Entry Checklist (binding)
[If a trade was taken: walk through items 1–6 with pass/fail.
 If no trade: write "Not applied — no candidate cleared |Sum| ≥ 3 (item 1 fails)." and list items 1–6 for reference.]
```

**Replace with:**
```markdown
## 7. Pre-Entry Checklist (binding)
[If a trade was taken: walk through items 1–8 with pass/fail (items 7 and 8 added 2026-04-25 Phase 3).
 If no trade: write "Not applied — no candidate cleared |Sum| ≥ 3 (item 1 fails)." and list items 1–8 for reference.
 If a candidate cleared items 1–6 but failed item 7 (sleeve OFF): write "Item 7 fail — sleeve gated OFF per Step 1.5. Logged as Promoted/Taken=NO in SignalLedger with Block_Reason=OverlayGateOff."]
```

## PowerShell apply block (idempotent)

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\daily-trade-rec\SKILL.md"
if (-not (Test-Path $path)) { Write-Error "SKILL.md not found at $path"; exit 1 }

$content = Get-Content $path -Raw

if ($content -match "## Step 1\.5 — Overlay Regime Gate \(Phase 3") {
    Write-Host "daily-trade-rec Phase 3 patch already applied — skipping"
    exit 0
}

# --- Edit 1 — Add meta-staging to Step 1 reads ---
$e1Anchor  = "9. *(optional)* Most recent ``/mnt/Trade/signal-review-*.md`` — read only the ``## 8. Escalation Flags`` section if it exists. If the section is present, carry the flags forward into the rec's §2 (Regime Read) as a one-line notice per flag."
$e1Replace = @'
9. *(optional)* Most recent `/mnt/Trade/signal-review-*.md` — read only the `## 8. Escalation Flags` section if it exists. If the section is present, carry the flags forward into the rec's §2 (Regime Read) as a one-line notice per flag.
10. **(Phase 3, post-2026-04-25)** `/mnt/Trade/meta-additions-staging-{YYYY-MM-DD}.md` — produced by `preflight-meta-additions-1952pm` at 19:52. Extract `overlay_gate_status` (per-sleeve ON/OFF), `v027_regime_bucket`, `v029_bab_spread`. If missing, treat as fail-loud — Step 1.5 blocks ALL Phase-3-gated sleeves and logs Block_Reason=OverlayStagingMissing in Step 8.
'@
if (-not $content.Contains($e1Anchor)) { Write-Error "Edit 1 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e1Anchor, $e1Replace)

# --- Edit 2 — Insert Step 1.5 before Step 2 ---
$e2Anchor  = "If a framework file is missing, stop and surface the gap — do not fabricate the methodology. If an upstream artifact is missing, log it under ""Data Gaps"" in the output and proceed; do not silently skip. The reason these four upstream files are non-negotiable is that today's recommendation must be reproducible from named, dated source files; if you can't cite where a fact came from, it can't carry a Grade-A claim.`r`n`r`n## Step 2 — Build the Upstream Synthesis block"
$e2Replace = @'
If a framework file is missing, stop and surface the gap — do not fabricate the methodology. If an upstream artifact is missing, log it under "Data Gaps" in the output and proceed; do not silently skip. The reason these four upstream files are non-negotiable is that today's recommendation must be reproducible from named, dated source files; if you can't cite where a fact came from, it can't carry a Grade-A claim.

## Step 1.5 — Overlay Regime Gate (Phase 3, added 2026-04-25)

This step sits between Step 1 (reads) and Step 2 (synthesis). It is **non-additive to Sum** — it is a binary sleeve-on/sleeve-off switch that multiplies post-Sum position size by 0 for any gated-off sleeve. Authoritative: `Methodology Prompt.md §Step 1.5` and `Risk Rules.md §4.B, §7 item 7, §8`.

**Inputs (from the staging file read in Step 1 item 10):**

- `overlay_gate_status` — per-sleeve ON/OFF from V033/V034/V035 (Faber 10m-SMA at previous month-end close).
- `v027_regime_bucket` — expansion / neutral / contraction. Drives Risk Rules §1.B gross-exposure tier.
- `v029_bab_spread` — USMV − SPLV 12m. If spread > 0, BAB sleeve is active (long low-β / short high-β stocks); if ≤ 0, ANTI-BAB and the sleeve is flat this month.
- `v030_dealergamma` — expected MISSING until subscription confirmed; do not block on its absence.

**Sleeve mapping (asset class → sleeve):**

| Asset class | Gated by | Variables in scope |
|---|---|---|
| Equity (SPY, QQQ, individual stocks) | V033 SPY Faber gate | NVDA, TSLA, AAPL, GOOGL, AMZN, META, TSM, INTC, MU, PYPL, PLTR, WDC, SPY, QQQ |
| International equity | V033 EFA optional | EWJ, EWY |
| Commodity | V034 GSCI Faber gate | Brent, WTI, Gold, Silver, Copper, Palladium, Platinum |
| Crypto | V035 BTC-USD Faber gate | BTC, ETH |
| FX, rates | Not gated (no overlay applies) | EURUSD, USDJPY, DGS2, DGS10 |

**Gate-application logic (per asset under scoring):**

1. Identify the asset's sleeve from the table above.
2. If the sleeve is **ON**: proceed to Step 2 normally. Signal is entry-eligible.
3. If the sleeve is **OFF**: the asset is still scored through Steps 2–5 (S/T/C/R, Sum, invalidation, stop, target) because the ledger needs the full score record, but `Taken=NO` and `Block_Reason=OverlayGateOff` will be written in Step 8 regardless of |Sum|. The §3 Recommendations Table omits the row; the §4 Theses Not Taken section flags it.
4. If the sleeve status is `MISSING` (staging file absent or staging row missing for that sleeve): treat as **OFF** (fail-loud default). Block_Reason=OverlayStagingMissing.

**Gating is non-additive.** Do NOT reduce S/T/C/R or Sum because a sleeve is OFF. The Sum is what the methodology says it is; the overlay just prevents today's *execution* on that sleeve.

**V027 sizing tier (from v027_regime_bucket):**

- `expansion` → full inverse-ATR sizing (no tier adjustment)
- `neutral` → standard sizing
- `contraction` → halve gross exposure on all risk-asset sleeves (binds alongside quarter-Kelly; take the more restrictive)

The V027 tier is applied *after* Step 5 per-position sizing is computed. Record the tier in the §7 Pre-Entry Checklist (item 8) and in SignalLedger col 34.

**V029 BAB sleeve weight:**

- If `v029_bab_spread > 0` (BAB regime): BAB sleeve is active on single-stock longs; sleeve weight ≤ 1/3 of V009 (momentum) risk budget. Compute `bab_sleeve_weight` as the fraction of V009 budget allocated today. Correlation gate applies — a BAB sleeve leg and a V009 spine long on the same ticker size to the combined sector cap, not double-sized.
- If `v029_bab_spread ≤ 0` (ANTI-BAB): `bab_sleeve_weight = 0.0`.

**V030 DealerGamma sleeve weight:**

- Expected MISSING this cohort. If value is present, compute `dealergamma_sleeve_weight` analogously (≤ 1/3 V009 budget). Otherwise write `None` to col 36.

**Output of Step 1.5:** a one-paragraph gate panel written into the rec's §2 Regime Read, naming the sleeve status per class, the V027 bucket, and the BAB regime. This panel is read by positions-monitor via the output rec; see `positions-monitor-phase3-SKILL-patch.md`.

## Step 2 — Build the Upstream Synthesis block
'@
if (-not $content.Contains($e2Anchor)) { Write-Error "Edit 2 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e2Anchor, $e2Replace)

# --- Edit 3 — Extend Step 5 pre-entry checklist with items 7 & 8 ---
$e3Anchor  = "6. Catalyst asymmetry stated — surprise-dependent vs confirmation-dependent. Surprise-dependent catalysts carry positive convexity and are preferred; confirmation-dependent catalysts where the bar is elevated (e.g. an earnings print already discounted) carry poor asymmetry and usually fail the overall thesis even when scored C+1.`r`n`r`n""No trade"" is always a valid output."
$e3Replace = @'
6. Catalyst asymmetry stated — surprise-dependent vs confirmation-dependent. Surprise-dependent catalysts carry positive convexity and are preferred; confirmation-dependent catalysts where the bar is elevated (e.g. an earnings print already discounted) carry poor asymmetry and usually fail the overall thesis even when scored C+1.
7. **Step 1.5 Overlay Gate status for this sleeve is ON** (Phase 3, added 2026-04-25). If OFF → position size × 0 → no trade regardless of Sum. Authoritative: `Risk Rules.md §7` item 7.
8. **V027 intermediary-capital sizing tier applied** (Phase 3, added 2026-04-25). If `v027_regime_bucket = contraction` (z < −1σ), the halved-gross-exposure rule is the binding constraint above quarter-Kelly. Authoritative: `Risk Rules.md §1.B` and `§7` item 8.

"No trade" is always a valid output.
'@
if (-not $content.Contains($e3Anchor)) { Write-Error "Edit 3 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e3Anchor, $e3Replace)

# --- Edit 4 — Extend Step 8 SignalLedger append ---
$e4Anchor  = "**For near-miss signals** (|Sum| = 2, or |Sum| ≥ 3 blocked): append one row with ID (next sequential N###), Type='Near-Miss', same score fields, Blocking_Leg, Block_Reason, Price_at_Signal, VIX_at_Signal, Status='OPEN'. Exit columns blank."
$e4Replace = @'
**For near-miss signals** (|Sum| = 2, or |Sum| ≥ 3 blocked): append one row with ID (next sequential N###), Type='Near-Miss', same score fields, Blocking_Leg, Block_Reason, Price_at_Signal, VIX_at_Signal, Status='OPEN'. Exit columns blank.

**Phase 3 meta-integration cols (positions 33–36, added 2026-04-25).** On every row — promoted AND near-miss — write:

| Col | Value source | Missing-value rule |
|---|---|---|
| 33 `overlay_gate_status` | `equity={ON\|OFF}\|commodity={ON\|OFF}\|crypto={ON\|OFF}` — from Step 1.5 gate panel | write `MISSING` string if staging absent |
| 34 `v027_regime_bucket` | `expansion`/`neutral`/`contraction` — from Step 1.5 | write `MISSING` if staging absent |
| 35 `bab_sleeve_weight` | float 0.0–0.333 — from Step 1.5 | write `None` if V029 MISSING |
| 36 `dealergamma_sleeve_weight` | float 0.0–0.333 — from Step 1.5 | write `None` if V030 MISSING (expected for this cohort) |

**Overlay-gated Sum +3 handling (per `Methodology Prompt.md §Step 1.5`).** A signal with |Sum| ≥ 3 on an overlay-OFF sleeve is logged as Type='Promoted', Taken='NO', Status='OPEN', Block_Reason='OverlayGateOff' (or 'OverlayStagingMissing' if fail-loud). This preserves the Sum arithmetic record for out-of-sample tracking while flagging why the trade wasn't executed. signal-review reads these rows to mark-to-market the overlay gate's hit rate separately from the Taken=YES population.
'@
if (-not $content.Contains($e4Anchor)) { Write-Error "Edit 4 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e4Anchor, $e4Replace)

# --- Edit 5 — Update §7 output template to items 1–8 ---
$e5Anchor  = "## 7. Pre-Entry Checklist (binding)`r`n[If a trade was taken: walk through items 1–6 with pass/fail.`r`n If no trade: write ""Not applied — no candidate cleared |Sum| ≥ 3 (item 1 fails)."" and list items 1–6 for reference.]"
$e5Replace = @'
## 7. Pre-Entry Checklist (binding)
[If a trade was taken: walk through items 1–8 with pass/fail (items 7 and 8 added 2026-04-25 Phase 3).
 If no trade: write "Not applied — no candidate cleared |Sum| ≥ 3 (item 1 fails)." and list items 1–8 for reference.
 If a candidate cleared items 1–6 but failed item 7 (sleeve OFF): write "Item 7 fail — sleeve gated OFF per Step 1.5. Logged as Promoted/Taken=NO in SignalLedger with Block_Reason=OverlayGateOff."]
'@
if (-not $content.Contains($e5Anchor)) { Write-Error "Edit 5 anchor not found — aborting"; exit 1 }
$content = $content.Replace($e5Anchor, $e5Replace)

# Backup + write
$backup = "$path.bak-phase3-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item $path $backup
Set-Content $path $content -NoNewline
Write-Host "daily-trade-rec Phase 3 patch applied. Backup: $backup"
```

## Verify

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\daily-trade-rec\SKILL.md"
$c = Get-Content $path -Raw
$checks = @(
    @{ Name = "Step 1 item 10 (staging read)";      Pattern = "meta-additions-staging-\{YYYY-MM-DD\}\.md" },
    @{ Name = "Step 1.5 header";                    Pattern = "## Step 1\.5 — Overlay Regime Gate \(Phase 3" },
    @{ Name = "Sleeve mapping table";               Pattern = "V033 SPY Faber gate" },
    @{ Name = "Checklist item 7 (overlay ON)";      Pattern = "Step 1\.5 Overlay Gate status for this sleeve is ON" },
    @{ Name = "Checklist item 8 (V027 tier)";       Pattern = "V027 intermediary-capital sizing tier applied" },
    @{ Name = "SignalLedger 4-col append rule";     Pattern = "Phase 3 meta-integration cols \(positions 33" },
    @{ Name = "OverlayGateOff logging rule";        Pattern = "Block_Reason='OverlayGateOff'" },
    @{ Name = "§7 template items 1–8 updated";      Pattern = "walk through items 1–8 with pass/fail" }
)
foreach ($chk in $checks) {
    $found = $c -match $chk.Pattern
    "{0,-38} {1}" -f $chk.Name, $(if ($found) { "OK" } else { "MISSING" })
}
```

Expected: all 8 checks `OK`.

## Rollback

```powershell
$path = "$env:USERPROFILE\Documents\Claude\skills\daily-trade-rec\SKILL.md"
$backup = Get-ChildItem -Path "$path.bak-phase3-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($backup) {
    Copy-Item $backup.FullName $path -Force
    Write-Host "Restored from $($backup.Name)"
} else {
    Write-Error "No pre-Phase-3 backup found — cannot auto-rollback"
}
```

## Sandbox note

Read-only mount applies; see `market-brief-phase3-SKILL-patch.md` sandbox note. Because this SKILL.md has 5 separate edit points, the PowerShell script aborts if any anchor has drifted — do NOT partially apply. If drift is detected, re-generate the patch against the current SKILL.md snapshot.
