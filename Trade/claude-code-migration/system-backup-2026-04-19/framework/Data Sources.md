# Data Source Manifest

**Last updated:** 2026-04-18 (added V029–V035 meta-integration rows)
**Purpose:** Explicit mapping of every Grade-A / Grade-B variable to a pull source. If a Grade A source cannot be pulled, the brief MUST fail loudly on that row, not silently write `n/a`.

Free-first. Paid data only where free is unusable.

---

## Cross-Asset Risk

| Variable | Grade | Source | URL / Series | Method |
|---|---|---|---|---|
| VIX (close) | A | CBOE / Yahoo | `^VIX` | Yahoo Finance scrape |
| VIX term structure (VIX/VIX3M) | A− | CBOE | `^VIX3M` | Yahoo scrape + ratio |
| MOVE | A | Refinitiv via Yahoo | `^MOVE` | Yahoo scrape |
| DXY | A | ICE / Yahoo | `DX-Y.NYB` | Yahoo scrape |
| HY OAS | A | FRED | `BAMLH0A0HYM2` | FRED API (free) |
| NFCI | A | Chicago Fed | weekly release | ChiFed CSV |
| **Intermediary capital ratio (PD equity/total capital, z-score)** | **A** | **NY Fed primary dealer statistics** | **`newyorkfed.org/markets/counterparties/primary-dealers-statistics` (weekly)** | **Weekly CSV pull; compute z-score vs 3y rolling mean** |
| FCI (Goldman proxy) | B | Bloomberg | n/a free | skip unless paid |

Intermediary-capital citation: `Methodology Prompt.md:Step 5` integration; `Trad core.md:Addendum §27` mechanism and caveats (He-Kelly-Manela 2017 JFE).

**Automated compute pipeline (2026-04-15):** The `audit-data-compute-750pm` scheduled task fires at 19:50 UTC+8 Mon-Fri (10 min before the brief) to fetch NY Fed PD data via web search and compute the z-score. Results written to `audit-data-staging-YYYY-MM-DD.md`. Compute script: `scripts/compute_audit_additions.py`.

Citation for grades: `Methodology Prompt.md:103`, `Trad core.md:48-53`.

## Rates

| Variable | Grade | Source | Series |
|---|---|---|---|
| 2Y UST | A | FRED | `DGS2` |
| 10Y UST | A | FRED | `DGS10` |
| 2s10s | A | derived | `DGS10 - DGS2` |
| 10Y real yield | A | FRED | `DFII10` |
| 10Y breakeven | A | FRED | `T10YIE` |
| ACM term premium | A | NY Fed | ACM CSV (monthly) |
| Forward-rate factor | A | derived | see `Trad core.md:122` |

Citation: `Trad core.md:122-126`.

## Equities

| Variable | Grade | Source |
|---|---|---|
| Index/stock closes | A | Yahoo Finance |
| Revision breadth | A | Zacks / I/B/E/S via SimplyWallSt (free tier) |
| Earnings calendar | A | Nasdaq earnings calendar / WSH |
| % constituents above 200DMA (SPY/QQQ) | A− | StockCharts (free) |
| **Fama-French 5-factor monthly returns** | **A** | **Kenneth French data library** | `mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html` (monthly CSV) |
| **Residual momentum (12m FF5-residualized, single-stock)** | **A** | **derived** | **Run monthly OLS of stock excess returns on Mkt-RF, SMB, HML, RMW, CMA over rolling 12m window; rank 12m residual returns for single-stock universe. Automated via `audit-data-compute-750pm` task and `scripts/compute_audit_additions.py`** |

Citation: `Trad core.md:183`, `Trad core.md:28`.

## Commodities

| Variable | Grade | Source |
|---|---|---|
| Brent / WTI spot | A | EIA / oilpriceAPI |
| **Brent M1–M3 curve** (PRIORITY) | A | CME / ICE settlement pages; Barchart free |
| **Basis-momentum (4w / 12w change in F1–F2 slope)** | **A** | **derived from front-curve daily settles** | **Compute front-month-to-deferred slope daily; take 4w and 12w differences. Compute for Brent, WTI, Gold, Silver, Copper** |
| EIA crude stocks | A | EIA weekly release |
| Gold / Silver / Copper spot | A | TradingEconomics / Kitco |
| LME copper stocks | A | LME public |
| China manufacturing PMI | A | NBS / Caixin release |

Basis-momentum citation: `Methodology Prompt.md:Step 2` commodity integration; `Trad core.md:Addendum §28` (Boons-Prado 2019 JF).

**Automated compute pipeline (2026-04-15):** The `audit-data-compute-750pm` task computes basis-momentum for Brent, WTI, Gold, Silver, Copper from front-curve daily settles. Results written to `audit-data-staging-YYYY-MM-DD.md`. Compute script: `scripts/compute_audit_additions.py`.

Citation: `Trad core.md:148-177`. Brent curve is your #1 watched regime variable (`Memory.md:37`).

## FX

| Variable | Grade | Source |
|---|---|---|
| EUR, JPY, GBP, AUD spot | A | Yahoo `EURUSD=X` etc. |
| USD/JPY + BOJ path | B+ | Yahoo + BOJ minutes |
| CFTC COT speculative net | B | CFTC.gov weekly |

Citation: `Methodology Prompt.md:107`, `Trad core.md:189`.

## Crypto

| Variable | Grade | Source |
|---|---|---|
| BTC / ETH spot | A | CoinGecko / Yahoo |
| BTC realized vol | A | derived from OHLC (30d) |
| BTC DVOL (implied) | B | Deribit public API |
| BTC perp funding | B | CoinGlass public / Binance API |
| 3m basis | B | Deribit / CME basis |
| BTC ETF net flows | B | Farside Investors / CoinDesk |
| Active addresses | A | blockchain.com / Glassnode free |
| Hash rate | A | blockchain.com |
| Exchange netflows | A | CryptoQuant free tier |
| Stablecoin supply | B | DefiLlama |
| MVRV / SOPR | B | regime context only — Glassnode free |

Citation: `Methodology Prompt.md:50, 108, 142-148`, `Coin core.md:9-17, 107-125`.

## Meta-integration additions (V029–V035, added 2026-04-18)

All five variable rows below obey the 4-tier fail-loud rule. Wire into `preflight-audit-data-1945pm` extension (Phase 2 of the 2026-04-18 rollout; see `meta-analysis-integration-plan-2026-04-18.md §3.3` and `deployment-memo-2026-04-18.md`).

| Variable | Grade | Source | Frequency | Fallback chain | Notes |
|---|---|---|---|---|---|
| **V029 BAB (Betting-Against-Beta)** | A | AQR BAB factor returns (canonical, for grading) OR ETF proxy (USMV/SPLV spread, tactical) OR self-compute from CRSP β-bucketed deciles | Monthly (canonical); daily (ETF proxy) | AQR → Ken French library → ETF proxy (USMV/SPLV) → self-compute | ETF proxy is tactical-use only. Canonical BAB required for 2026-10-14 review evidence. |
| **V030 DealerGamma (options dealer gamma positioning)** | B | SqueezeMetrics GEX OR SpotGamma daily composite | Daily | SqueezeMetrics → SpotGamma → MISSING (no self-compute option) | **Paid data — subscription required. CONFIRM with Gerald before Phase 2 coding.** If neither source is subscribed, row stays MISSING until resolved. |
| **V031 GP/A (Gross Profitability / Assets)** | A | Compustat / Ken French GP portfolio | Quarterly (financial statements) | Ken French library → Compustat → self-compute from CRSP + Compustat | Slow-moving; monthly rebalance of ranked basket, not daily rescore. |
| **V032 CEI (Composite Equity Issuance)** | A | Daniel-Titman composite equity issuance (self-computed from CRSP + Compustat) | Quarterly | self-compute only | Document computation in `scripts/compute_cei.py` (new, created in Phase 2). Quarterly financial-statement data has reporting lag — replicate equal-weight quarterly rebalance. |
| **V033–V035 C009 Faber TAA 10m-SMA** | A | Yahoo Finance monthly closes on SPY (V033) / GSCI (V034) / BTC-USD (V035) | Monthly (end-of-month) | Yahoo → Stooq → MISSING | EFA optional (for EWJ/EWY sleeve). Trivial computation; extend `scripts/compute_audit_additions.py`. Overlay state flips only at month-end. |

Citation: `Methodology Prompt.md §Step 1.5`, `Methodology Prompt.md §4` entries 29–33, `Trad core.md` Addendum 2026-04-18, `Risk Rules.md §1.B, §4.B, §5.A, §8`.

**Automated compute pipeline (extended 2026-04-18):** The `preflight-audit-data-1945pm` scheduled task will pull V029 / V031 / V032 / V033–V035 during Phase 2 rollout (extension of `scripts/compute_audit_additions.py` or new sibling script). DealerGamma (V030) pull wires in only after the subscription question is resolved.

**Expected Phase 2 runtime impact:** +3–5 minutes on preflight. The 20:00 market-brief SLA must hold.

---

## On-demand-only (no routine pull)

- Token unlocks calendar (when BTC/ETH not the focus): TokenUnlocks.app
- FedWatch (rate-path surprise): CME FedWatch
- Geopolitical risk index (Caldara-Iacoviello): matteoiacoviello.com

---

## Fail-loud rule (updated 2026-04-16 with fallback framework)

Any row marked Grade A above must be retrieved via the 4-tier fallback chain (`Data-Retrieval-Fallback-Framework.md`) before being declared MISSING:

1. **Tier 1 — Direct HTTP** (Yahoo Finance, CoinGecko, Blockchain.info, etc.)
2. **Tier 2 — Web Search** (2-3 query patterns per variable)
3. **Tier 3 — Persistent Cache** (`/mnt/Trade/.data-cache/`, staleness-classified)
4. **Tier 4 — MISSING** (fail-loud): print as `MISSING — [all sources attempted]`, leave score leg blank, log to DataQuality.

Only after ALL tiers fail should a variable be marked MISSING. Stale-but-usable cached values (within staleness window) are valid readings with a staleness tag, not MISSING.

**Implementation:** Use `scripts/data_retrieval_engine.py` for the retrieval chain and `scripts/cache_manager.py` for cache reads. Every successful retrieval auto-writes to cache for future sessions.

**Staleness windows** vary by variable type: 1 day for prices/VIX, 2 days for HY OAS, 7 days for NFCI/weekly data, 14 days for intermediary capital, 30-60 days for structural/monthly data (FF5, residual momentum, ACM term premium). See `cache_manager.STALENESS_WINDOWS` for the full map.

Basis: `Methodology Prompt.md:163` ("Do not present ungrounded assertions as evidence").
