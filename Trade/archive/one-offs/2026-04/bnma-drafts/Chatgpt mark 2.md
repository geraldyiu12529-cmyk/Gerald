# BNMA Consolidated Master Markdown

This file consolidates the available BNMA materials into one self-contained markdown artifact.

**Important status note:** downstream scoring remains an **analytical approximation only**. Full MCMC is still required for production use because many Stage A rows do not have model-ready annualized Sharpe and study-level SE inputs.

---


# Stage A Registry Validation and Evidence Intake

## Files

The working files had previously been written as:

- `stage_a.csv`
- `stage_a_summary.md`
- `candidates_rejected.csv`
- `stage_a_table.md`

These separate Stage A artifacts were not present on disk at consolidation time, so the Stage A content below is embedded directly in this combined markdown.

## Intake summary

Tier 1 Grade A/B registry rows were treated as authoritative from the embedded registry. I did not find any contradiction strong enough to overturn a registry row, so every Grade A/B registry row validated as `PASS`. The only material caveat worth carrying forward is the one already embedded in the registry itself: V007’s gold/real-yield linkage has weakened materially in the post-2022 regime, so it remains valid but clearly regime-sensitive rather than universally stable.

Replication depth is strongest in momentum, commodity carry/curve structure, and crypto flow-related timing. The replication bench for momentum is especially deep: the century-scale trend-following extension reports positive average returns in every decade since 1880; dynamic momentum roughly doubles alpha and Sharpe versus static momentum in the crash-aware formulation; CTREND remains robust across subperiods in a 3,000-plus-coin crypto universe; and stop-loss crypto momentum dominates conventional crypto momentum in a 147-cryptocurrency sample from January 2015 through June 2022. Commodity/carry support is also strong: cross-asset carry averages a 0.74 Sharpe, commodity basis sorts deliver 5%–14% annual spot premia and 1%–3% term premia, and crypto carry posted an annualized Sharpe of 6.45 over 2020–2025 before turning negative in 2025.

Crypto-flow augmentation materially improved the intake for V014 and V017. World crypto order flow has strong explanatory and predictive power for returns; early U.S. spot-BTC ETF flows exceeded $500 million per day and were reported with a 95% R-squared linkage to BTC price in the launch-window study; a follow-on paper finds cointegration between ETF assets and BTC price from January 11, 2024 to May 16, 2025; and blockchain characteristics such as network size and computing power are documented as co-moving with cryptocurrency prices and returns.

Five Tier 3 candidates cleared admission: 200-DMA regime filter, market breadth, VIX term-structure backwardation, dual momentum/GEM, and Global M2. The first four have coherent mechanisms plus direct quantitative support: Faber reports returns roughly 60% lower and volatility 30% higher when markets are below the 10-month SMA; global market breadth robustly predicts future stock returns; the VIX futures term structure contains market-timing information for the U.S. equity market; and Antonacci’s composite dual-momentum portfolio is reported with a 1.07 Sharpe versus 0.50 for the equal-weight benchmark. Global M2 cleared admission only as a working-paper structural candidate, backed by reported BTC–M2 cointegration over 2015–2025 and therefore assigned a very skeptical prior and explicit overlap peers.

The model-readiness caveat is important. Stage A inventory is broad enough to proceed, but numerically thin in many rows because many papers report predictive relationships, drifts, premia, or explanatory power without giving a directly usable annualized long-short Sharpe and study-level SE in the abstract/snippet layer. I therefore marked those rows `PARTIAL_NUMERIC` or `NUMERIC_MISSING` rather than inventing conversions.

## Studies per variable

| var_id | name | n_studies |
|---|---|---:|
| C001 | 200-DMA regime filter | 1 |
| C002 | Market breadth (% constituents >200-DMA) | 1 |
| C003 | VIX term structure backwardation | 1 |
| C004 | Dual momentum / GEM | 1 |
| C005 | Global M2 money supply | 1 |
| V001 | VIX | 1 |
| V002 | MOVE Index | 1 |
| V003 | DXY | 2 |
| V004 | HY OAS | 1 |
| V005 | NFCI | 1 |
| V006 | UST 2Y/10Y yields | 1 |
| V007 | Real yield / Breakevens | 2 |
| V008 | ACM Term Premium 10Y | 1 |
| V009 | Time-series momentum | 5 |
| V010 | Revision breadth | 3 |
| V011 | Brent M1-M3 curve slope | 3 |
| V012 | BTC active addresses | 2 |
| V013 | BTC hash rate | 1 |
| V014 | BTC exchange netflows | 2 |
| V015 | BTC realized vol | 1 |
| V016 | BTC perp funding rate | 2 |
| V017 | BTC ETF net flows | 3 |
| V018 | BTC 3m basis | 2 |
| V019 | MVRV / SOPR | 1 |
| V020 | News sentiment | 2 |
| V026 | Residual momentum (FF5) | 2 |
| V027 | Intermediary capital ratio | 2 |
| V028 | Basis-momentum | 2 |

## Stage A study table

Tier 1 primary rows below are copied from the embedded registry. External citations were attached in the original Stage A intake when replication or candidate evidence was added.

### Risk overlay

| var_id | name | score_component | tier | grade | source_paper | asset_class | study_id | is_primary_or_replication | sharpe_annualized | sharpe_se | n_months | universe | sample_start | sample_end | is_oos | transaction_costs_included | se_imputed | registry_validation | score_component_inferred | correlation_inferred | correlation_peers | extraction_flag |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|
| V001 | VIX | R | Tier 1 | A | Whaley (2000) — registry primary | Cross-Asset | V001-P | primary | NA | NA | NA | US equity vol index | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V004; V027 | NUMERIC_MISSING |
| V002 | MOVE Index | R | Tier 1 | A | Siriwardane (2019) — registry primary | Cross-Asset | V002-P | primary | NA | NA | NA | US Treasury vol index | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V001 | NUMERIC_MISSING |
| V004 | HY OAS | R | Tier 1 | A | Gilchrist-Zakrajsek (2012) — registry primary | Cross-Asset | V004-P | primary | NA | NA | NA | US corporate credit | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V027 | NUMERIC_MISSING |
| V005 | NFCI | R | Tier 1 | A | Brave-Butters (2012) — registry primary | Cross-Asset | V005-P | primary | NA | NA | NA | US financial conditions | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | NA | NUMERIC_MISSING |
| V015 | BTC realized vol | R | Tier 1 | A | Liu-Tsyvinski (2021) — registry primary | Crypto | V015-P | primary | NA | NA | NA | Major cryptocurrencies | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | NA | NUMERIC_MISSING |
| V016 | BTC perp funding rate | R | Tier 1 | B | Aloosh-Ouzan-Shahzad (2023) / practitioner — registry primary | Crypto | V016-P | primary | NA | NA | NA | BTC perpetual futures | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V018 | NUMERIC_MISSING |
| V018 | BTC 3m basis | R | Tier 1 | B | Practitioner + carry literature — registry primary | Crypto | V018-P | primary | NA | NA | NA | BTC dated futures | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V016 | NUMERIC_MISSING |
| V027 | Intermediary capital ratio | R | Tier 1 | A | He-Kelly-Manela (2017) — registry primary | Cross-Asset | V027-P | primary | 0.6 | NA | NA | 7 asset classes | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V004 | PARTIAL_NUMERIC |
| V016 | BTC perp funding rate | R | Tier 2 | B | Zhivkov (2026) two-tiered funding-rate markets | Crypto | V016-R1 | replication | NA | NA | NA | CEX cryptocurrency funding-rate markets | NA | NA | NA | TRUE | FALSE | NA | FALSE | FALSE | V018 | PARTIAL_NUMERIC |
| V018 | BTC 3m basis | R | Tier 2 | B | Borri et al. (2025) crypto carry | Crypto | V018-R1 | replication | 6.45 | NA | NA | Cryptocurrency carry strategy | 2020 | 2025 | NA | NA | FALSE | NA | FALSE | FALSE | V016 | PARTIAL_NUMERIC |
| V027 | Intermediary capital ratio | R | Tier 2 | A | Adrian-Etula-Muir (2014) intermediary leverage factor | Cross-Asset | V027-R1 | replication | NA | NA | NA | Stocks and bonds | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V004 | NUMERIC_MISSING |

### Structural directional

| var_id | name | score_component | tier | grade | source_paper | asset_class | study_id | is_primary_or_replication | sharpe_annualized | sharpe_se | n_months | universe | sample_start | sample_end | is_oos | transaction_costs_included | se_imputed | registry_validation | score_component_inferred | correlation_inferred | correlation_peers | extraction_flag |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|
| V003 | DXY | S | Tier 1 | A | Verdelhan (2018) — registry primary | Cross-Asset | V003-P | primary | NA | NA | NA | FX / cross-asset | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | Gold; Brent | NUMERIC_MISSING |
| V006 | UST 2Y/10Y yields | S | Tier 1 | A | Campbell-Shiller (1991) — registry primary | Rates | V006-P | primary | NA | NA | NA | US Treasuries | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V008 | NUMERIC_MISSING |
| V007 | Real yield / Breakevens | S | Tier 1 | A | D'Amico et al. (2018) — registry primary | Rates | V007-P | primary | NA | NA | NA | US TIPS / nominals | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | Gold | NUMERIC_MISSING |
| V008 | ACM Term Premium 10Y | S | Tier 1 | A | Adrian-Crump-Moench (2013) — registry primary | Rates | V008-P | primary | NA | NA | NA | US Treasury term structure | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V006 | NUMERIC_MISSING |
| V011 | Brent M1-M3 curve slope | S | Tier 1 | A | Gorton-Hayashi-Rouwenhorst (2013) — registry primary | Commodities | V011-P | primary | NA | NA | NA | Commodity futures | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V028 | NUMERIC_MISSING |
| V012 | BTC active addresses | S | Tier 1 | A | Liu-Tsyvinski (2021) — registry primary | Crypto | V012-P | primary | NA | NA | NA | Major cryptocurrencies / Bitcoin on-chain | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V013; V019 | NUMERIC_MISSING |
| V013 | BTC hash rate | S | Tier 1 | A | Cong-He-Li (2021) — registry primary | Crypto | V013-P | primary | NA | NA | NA | Bitcoin on-chain / mining | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V012 | NUMERIC_MISSING |
| V019 | MVRV / SOPR | S | Tier 1 | B | Practitioner-dominant — registry primary | Crypto | V019-P | primary | NA | NA | NA | Bitcoin on-chain valuation | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V012 | NUMERIC_MISSING |
| V028 | Basis-momentum | S | Tier 1 | A | Boons-Prado (2019) — registry primary | Commodities | V028-P | primary | 0.8 | NA | NA | 23 commodity futures | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V011 | PARTIAL_NUMERIC |
| V003 | DXY | S | Tier 2 | A | Rees (2023) BIS WP 1083 commodity prices and USD | Cross-Asset | V003-R1 | replication | NA | NA | NA | Commodity prices and USD | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V011; V028 | NUMERIC_MISSING |
| V007 | Real yield / Breakevens | S | Tier 2 | A | Abrahams-Adrian-Crump-Moench-Yu (2016) decomposing real and nominal yield curves | Rates | V007-R1 | replication | NA | NA | NA | US real and nominal yield curves | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V008 | NUMERIC_MISSING |
| V011 | Brent M1-M3 curve slope | S | Tier 2 | A | Koijen-Moskowitz-Pedersen-Vrugt (2018) carry | Commodities | V011-R1 | replication | 0.74 | NA | NA | Cross-asset carry strategies | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V028 | PARTIAL_NUMERIC |
| V011 | Brent M1-M3 curve slope | S | Tier 2 | A | Szymanowska-de Roon-Nijman-van den Goorbergh (2014) commodity futures risk premia | Commodities | V011-R2 | replication | NA | NA | NA | Commodity futures | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V028 | PARTIAL_NUMERIC |
| V012 | BTC active addresses | S | Tier 2 | A | Cong-Li-Tang-Yang (2019/2021) blockchain characteristics and cryptocurrency returns | Crypto | V012-R1 | replication | NA | NA | NA | Cryptocurrency prices and blockchain characteristics | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V013; V019 | NUMERIC_MISSING |
| V028 | Basis-momentum | S | Tier 2 | A | Szymanowska-de Roon-Nijman-van den Goorbergh (2014) commodity futures risk premia | Commodities | V028-R1 | replication | NA | NA | NA | Commodity futures | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V011 | NUMERIC_MISSING |
| C005 | Global M2 money supply | S | Tier 3 | Candidate (working paper) | Kokabian (2025) M2-Bitcoin elasticity cointegration study | Crypto | C005-P | candidate | NA | NA | NA | BTC and global/US M2 | 2015-01 | 2025-04 | NA | NA | FALSE | NA | TRUE | TRUE | V003; V007; V012; V019 | PARTIAL_NUMERIC |

### Tactical timing

| var_id | name | score_component | tier | grade | source_paper | asset_class | study_id | is_primary_or_replication | sharpe_annualized | sharpe_se | n_months | universe | sample_start | sample_end | is_oos | transaction_costs_included | se_imputed | registry_validation | score_component_inferred | correlation_inferred | correlation_peers | extraction_flag |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|
| V009 | Time-series momentum | T | Tier 1 | A | Moskowitz-Ooi-Pedersen (2012) — registry primary | All | V009-P | primary | 0.9 | NA | NA | 58 liquid futures | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V026 | PARTIAL_NUMERIC |
| V010 | Revision breadth | T | Tier 1 | A | Gleason-Lee (2003) — registry primary | Equities | V010-P | primary | NA | NA | NA | US equities / analyst revisions | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | NA | NUMERIC_MISSING |
| V014 | BTC exchange netflows | T | Tier 1 | A | Aloosh-Ouzan-Shahzad (2023) — registry primary | Crypto | V014-P | primary | NA | NA | NA | BTC exchange flow data | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V017 | NUMERIC_MISSING |
| V017 | BTC ETF net flows | T | Tier 1 | B | No direct peer-reviewed primary in registry; institutional flow literature | Crypto | V017-P | primary | NA | NA | NA | US spot BTC ETFs / BTC | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V014 | NUMERIC_MISSING |
| V026 | Residual momentum (FF5) | T | Tier 1 | A | Blitz-Huij-Martens (2011) — registry primary | Equities | V026-P | primary | 0.7 | NA | NA | Equities | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | V009 | PARTIAL_NUMERIC |
| V009 | Time-series momentum | T | Tier 2 | A | Hurst-Ooi-Pedersen (2017) century of trend-following | All | V009-R1 | replication | NA | NA | NA | 67 markets across 4 asset classes | 1880 | 2016 | NA | TRUE | FALSE | NA | FALSE | FALSE | V026 | NUMERIC_MISSING |
| V009 | Time-series momentum | T | Tier 2 | A | Daniel-Moskowitz (2016) momentum crashes / dynamic momentum | All | V009-R2 | replication | NA | NA | NA | Equities and asset classes | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V026 | NUMERIC_MISSING |
| V009 | Time-series momentum | T | Tier 2 | A | Fieberg et al. (2025) CTREND | Crypto | V009-R3 | replication | NA | NA | NA | >3,000 cryptocurrencies | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V014; V017 | NUMERIC_MISSING |
| V009 | Time-series momentum | T | Tier 2 | A | Sadaqat-Butt (2023) stop-loss momentum in crypto | Crypto | V009-R4 | replication | NA | NA | NA | 147 cryptocurrencies | 2015-01 | 2022-06 | NA | NA | FALSE | NA | FALSE | FALSE | V014; V017 | NUMERIC_MISSING |
| V010 | Revision breadth | T | Tier 2 | A | Meursault et al. (2023) PEAD.txt | Equities | V010-R1 | replication | NA | NA | NA | Earnings-call text, US equities | 2010 | 2019 | NA | NA | FALSE | NA | FALSE | FALSE | NA | PARTIAL_NUMERIC |
| V010 | Revision breadth | T | Tier 2 | A | PGIM Quantitative Solutions (2021) analyst revisions implementation note | Equities | V010-R2 | replication | NA | NA | NA | MSCI / IBES / Datastream universes | 2003-12 | 2021-05 | NA | NA | FALSE | NA | FALSE | FALSE | NA | NUMERIC_MISSING |
| V014 | BTC exchange netflows | T | Tier 2 | A | Anastasopoulos et al. (2025) order flow and cryptocurrency returns | Crypto | V014-R1 | replication | NA | NA | NA | Cross-section of cryptocurrencies / world order flow | NA | NA | TRUE | NA | FALSE | NA | FALSE | FALSE | V017 | NUMERIC_MISSING |
| V017 | BTC ETF net flows | T | Tier 2 | B | Mazur (2024) bitcoin spot ETF flows and price formation | Crypto | V017-R1 | replication | NA | NA | NA | US spot BTC ETFs | 2024-01-11 | 2024-05 | NA | NA | FALSE | NA | FALSE | FALSE | V014 | PARTIAL_NUMERIC |
| V017 | BTC ETF net flows | T | Tier 2 | B | Guliyev-Ahmadova (2025) ETF assets and BTC price cointegration | Crypto | V017-R2 | replication | NA | NA | NA | 11 US spot BTC ETFs / BTC | 2024-01-11 | 2025-05-16 | NA | NA | FALSE | NA | FALSE | FALSE | V014 | PARTIAL_NUMERIC |
| V026 | Residual momentum (FF5) | T | Tier 2 | A | Asness-Moskowitz-Pedersen (2013) value and momentum everywhere | Equities | V026-R1 | replication | NA | NA | NA | Global equities and other asset classes | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | V009 | NUMERIC_MISSING |
| C004 | Dual momentum / GEM | T | Tier 3 | Candidate (working paper) | Antonacci GEM / dual momentum | Cross-Asset | C004-P | candidate | 0.87 | 0.054 | 480 | Global Equities Momentum strategy | 1974 | 2013 | FALSE | FALSE | TRUE | NA | TRUE | TRUE | V009; V026 | OK |

### Overlay candidates

| var_id | name | score_component | tier | grade | source_paper | asset_class | study_id | is_primary_or_replication | sharpe_annualized | sharpe_se | n_months | universe | sample_start | sample_end | is_oos | transaction_costs_included | se_imputed | registry_validation | score_component_inferred | correlation_inferred | correlation_peers | extraction_flag |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|
| C001 | 200-DMA regime filter | Overlay | Tier 3 | Candidate (working paper) | Faber (2007/2013) quantitative tactical asset allocation | Equities | C001-P | candidate | NA | NA | NA | Multi-asset / US equities | 1900 | 2012 | NA | NA | FALSE | NA | TRUE | TRUE | V009; V026; C002 | PARTIAL_NUMERIC |
| C002 | Market breadth (% constituents >200-DMA) | Overlay | Tier 3 | Candidate (peer-reviewed) | Zaremba et al. (2021) market breadth and global equity returns | Equities | C002-P | candidate | NA | NA | NA | 38 equity markets | NA | NA | NA | NA | FALSE | NA | TRUE | TRUE | C001; V031; V009 | NUMERIC_MISSING |
| C003 | VIX term structure backwardation | Overlay | Tier 3 | Candidate (peer-reviewed) | Fassas-Hourvouliades (2019) VIX futures as market timing indicator | Equities | C003-P | candidate | NA | NA | NA | S&P 500 / VIX futures | 2010 | 2017 | NA | NA | FALSE | NA | TRUE | TRUE | V001; V002; V031 | NUMERIC_MISSING |

### Catalyst rows parked for Stage F

| var_id | name | score_component | tier | grade | source_paper | asset_class | study_id | is_primary_or_replication | sharpe_annualized | sharpe_se | n_months | universe | sample_start | sample_end | is_oos | transaction_costs_included | se_imputed | registry_validation | score_component_inferred | correlation_inferred | correlation_peers | extraction_flag |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|
| V020 | News sentiment | C | Tier 1 | B | Tetlock (2007) — registry primary | Cross-Asset | V020-P | primary | NA | NA | NA | News text / equities | NA | NA | NA | NA | FALSE | PASS | FALSE | FALSE | NA | NUMERIC_MISSING |
| V020 | News sentiment | C | Tier 2 | B | Garcia (2013) text sentiment and stock market | Cross-Asset | V020-R1 | replication | NA | NA | NA | News text / stock market | NA | NA | NA | NA | FALSE | NA | FALSE | FALSE | NA | NUMERIC_MISSING |

## Candidate pipeline status

### Admitted Tier 3 candidates

| var_id | name | score_component | grade | asset_class | correlation_peers | extraction_flag |
|---|---|---|---|---|---|---|
| C001 | 200-DMA regime filter | Overlay | Candidate (working paper) | Equities | V009; V026; C002 | PARTIAL_NUMERIC |
| C002 | Market breadth (% constituents >200-DMA) | Overlay | Candidate (peer-reviewed) | Equities | C001; V031; V009 | NUMERIC_MISSING |
| C003 | VIX term structure backwardation | Overlay | Candidate (peer-reviewed) | Equities | V001; V002; V031 | NUMERIC_MISSING |
| C004 | Dual momentum / GEM | T | Candidate (working paper) | Cross-Asset | V009; V026 | OK |
| C005 | Global M2 money supply | S | Candidate (working paper) | Crypto | V003; V007; V012; V019 | PARTIAL_NUMERIC |

### Rejected or parked candidates

| name | inferred_score_component | disposition | reason |
|---|---|---|---|
| MVRV Z-Score | S | Reject | Redundant with V019 and no peer-reviewed/high-quality working-paper study surfaced in admissible search set; practitioner usage only. |
| NVT Signal (90d smoothed) | S | Reject | Could not verify with a peer-reviewed or high-quality working paper giving a model-ready effect-size on the Sharpe scale within search budget. |
| Token unlock events | C | Stage F | Event-study / catalyst scale; BNMA skips C and the quantitative evidence located is non-peer-reviewed. |
| Fear & Greed Index (<10) | T/Overlay | Reject | Sample is extremely thin, threshold-specific claim not anchored by a robust peer-reviewed paper, and signal overlaps sentiment/news variables. |
| Whale accumulation / exchange whale ratio | T | Reject | Classifier-accuracy evidence is sample-specific; no sufficiently strong peer-reviewed or high-quality working-paper source verified for admission. |
| Funding rate arbitrage (delta-neutral) | Outside main scale | Reject | Standalone delta-neutral arbitrage is not on the same directional/overlay Sharpe scale as the BNMA target variables. |
| Pairs trading BTC-ETH cointegration | T | Reject | Source quality below admission bar and frequency (5-minute) mismatches the framework's horizons. |
| Short-period RSI (2-5 day) | T | Reject | Insufficient peer-reviewed evidence retrieved within budget for a stable, model-ready signal in the target universe. |
| Price-to-sales (tech) | S | Reject | Valuation lens is plausible but a variable-specific return-predictive study on the target universe and scale was not verified. |
| Gold/silver ratio | S | Reject | Long-run co-movement is documented, but robust predictive trading evidence for the stated thresholds was not verified. |
| China PMI leading copper | S | Reject | Economic intuition is strong, but a variable-specific, model-ready study with extractable quantitative effect was not confirmed within budget. |
| EIA inventory surprises (crude) | C | Stage F | Event-study / catalyst variable; skipped from BNMA by design. |
| OPEC+ production decisions | C | Stage F | Event-study / catalyst variable; skipped from BNMA by design. |
| Hierarchical Risk Parity (HRP) | Portfolio construction | Reject | Portfolio construction method, not a predictive signal variable. |

Provisional/Ungraded registry rows V029, V030, V031, V032, and V033 were not pooled in Stage A because the prior design explicitly parks them for Stage F. V020 is validated above but also remains in the Stage F output because Catalyst-scale effects are off the main BNMA Sharpe scale.

## Stop point

Registry-validation FAILs: **none**.

This completes Stage A.


---

# Stage B-F Summary

# BNMA Stage B-F summary

## Estimable variables used in the analytical approximation

| var_id   | study_id   |    y |   n_months | source                                                   | se_note                                                       |        se |
|:---------|:-----------|-----:|-----------:|:---------------------------------------------------------|:--------------------------------------------------------------|----------:|
| V011     | V011-R1    | 0.74 |        232 | Koijen-Moskowitz-Pedersen-Vrugt (2018) carry replication | SE imputed from prior-session sample window Nov 1991–Feb 2011 | 0.074098  |
| V028     | V028-P     | 0.8  |        643 | Boons-Prado (2019) registry primary                      | SE imputed from prior-session sample window Aug 1960–Feb 2014 | 0.0453087 |
| V009     | V009-P     | 0.9  |        300 | Moskowitz-Ooi-Pedersen (2012) registry primary           | SE imputed from prior-session sample window Jan 1985–Dec 2009 | 0.0684349 |
| V026     | V026-P     | 0.7  |        960 | Blitz-Huij-Martens (2011) registry primary               | SE imputed from prior-session sample window Jan 1930–Dec 2009 | 0.0360122 |
| V027     | V027-P     | 0.6  |        516 | He-Kelly-Manela (2017) registry primary                  | SE imputed from prior-session sample window Jan 1970–Dec 2012 | 0.0478207 |
| C004     | C004-P     | 0.87 |        480 | Antonacci GEM / dual momentum                            | SE taken from Stage A                                         | 0.054     |

All numerics are analytical approximations with alpha_a = tau_k = 0 for scored rows only.


---

# Main Report

# report.md

**Status:** analytical approximation only. Full MCMC remains required for production use because many Stage A rows lack model-ready annualized Sharpe and study-level SE inputs.

## 1. Marginal-contribution flags (lead)

| var_id   | name                                     | group   | p_beats_peers   | action                   | note                                                                        |
|:---------|:-----------------------------------------|:--------|:----------------|:-------------------------|:----------------------------------------------------------------------------|
| C001     | 200-DMA regime filter                    | Overlay | NA              | NEEDS_NUMERIC_EXTRACTION | Admitted candidate but not estimable from current Stage A numerics.         |
| C002     | Market breadth (% constituents >200-DMA) | Overlay | NA              | NEEDS_NUMERIC_EXTRACTION | Admitted candidate but not estimable from current Stage A numerics.         |
| C003     | VIX term structure backwardation         | Overlay | NA              | NEEDS_NUMERIC_EXTRACTION | Admitted candidate but not estimable from current Stage A numerics.         |
| V027     | Intermediary capital ratio               | R       | 1.000           | KEEP                     | No marginal-contribution issue detected in the estimable subset.            |
| V028     | Basis-momentum                           | S       | 0.807           | KEEP                     | No marginal-contribution issue detected in the estimable subset.            |
| V011     | Brent M1-M3 curve slope                  | S       | 0.193           | DEMOTE_OR_MERGE          | Marginal contribution versus declared peers is weak under the strict prior. |
| C005     | Global M2 money supply                   | S       | NA              | NEEDS_NUMERIC_EXTRACTION | Admitted candidate but not estimable from current Stage A numerics.         |
| V009     | Time-series momentum                     | T       | 0.991           | KEEP                     | No marginal-contribution issue detected in the estimable subset.            |
| V026     | Residual momentum (FF5)                  | T       | 0.009           | DEMOTE_OR_MERGE          | Marginal contribution versus declared peers is weak under the strict prior. |
| C004     | Dual momentum / GEM                      | T       | 0.000           | DEMOTE_OR_MERGE          | Marginal contribution versus declared peers is weak under the strict prior. |

## 2. Per-group ranking tables

### S

| var_id   | name                    | tier   | grade                     | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width |   tau_posterior_median | peers                   |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag   | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:------------------------|:-------|:--------------------------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|-----------------------:|:------------------------|----------------:|----------------------------:|--------------------:|:------------------|:-------------------------|:---------------------|:-----------------|
| V028     | Basis-momentum          | Tier 1 | A                         | Commodities   |           2 |            0.790 |      0.716 |       0.864 |        1.000 |    1.000 |         1.000 |         1.000 |          2.000 |           1.000 |                    nan | V011                    |           0.807 |                       0.800 |               0.474 | ANALYTICAL_ONLY   | FALSE                    | FALSE                | FALSE            |
| V011     | Brent M1-M3 curve slope | Tier 1 | A                         | Commodities   |           3 |            0.715 |      0.596 |       0.835 |        1.000 |    1.000 |         2.000 |         1.000 |          2.000 |           1.000 |                    nan | V028                    |           0.193 |                     nan     |             nan     | ANALYTICAL_ONLY   | FALSE                    | FALSE                | FALSE            |
| V008     | ACM Term Premium 10Y    | Tier 1 | A                         | Rates         |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V006; V007              |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V012     | BTC active addresses    | Tier 1 | A                         | Crypto        |           2 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V013; V019; C005        |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V013     | BTC hash rate           | Tier 1 | A                         | Crypto        |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V012                    |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V003     | DXY                     | Tier 1 | A                         | Cross-Asset   |           2 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | Gold; Brent; V011; V028 |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| C005     | Global M2 money supply  | Tier 3 | Candidate (working paper) | Crypto        |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V003; V007; V012; V019  |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | NO_NUMERIC_INPUT |
| V019     | MVRV / SOPR             | Tier 1 | B                         | Crypto        |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V012; C005              |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V007     | Real yield / Breakevens | Tier 1 | A                         | Rates         |           2 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | Gold; V008              |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V006     | UST 2Y/10Y yields       | Tier 1 | A                         | Rates         |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V008                    |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |

Estimable subnetwork size: 2 of 10 nodes.

### T

| var_id   | name                    | tier   | grade                     | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width |   tau_posterior_median | peers      |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag   | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:------------------------|:-------|:--------------------------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|-----------------------:|:-----------|----------------:|----------------------------:|--------------------:|:------------------|:-------------------------|:---------------------|:-----------------|
| V009     | Time-series momentum    | Tier 1 | A                         | All           |           5 |            0.874 |      0.763 |       0.985 |        1.000 |    1.000 |         1.000 |         1.000 |          1.000 |           0.000 |                    nan | V026; C004 |           0.991 |                       0.900 |               0.525 | ANALYTICAL_ONLY   | FALSE                    | FALSE                | FALSE            |
| V026     | Residual momentum (FF5) | Tier 1 | A                         | Equities      |           2 |            0.694 |      0.635 |       0.753 |        1.000 |    1.000 |         2.000 |         2.000 |          2.000 |           0.000 |                    nan | V009; C004 |           0.009 |                       0.700 |               0.417 | ANALYTICAL_ONLY   | FALSE                    | FALSE                | FALSE            |
| C004     | Dual momentum / GEM     | Tier 3 | Candidate (working paper) | Cross-Asset   |           1 |            0.402 |      0.341 |       0.462 |        1.000 |    1.000 |         3.000 |         3.000 |          3.000 |           0.000 |                    nan | V009; V026 |           0.000 |                       0.870 |               0.241 | ANALYTICAL_ONLY   | FALSE                    | FALSE                | FALSE            |
| V017     | BTC ETF net flows       | Tier 1 | B                         | Crypto        |           3 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V014       |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V014     | BTC exchange netflows   | Tier 1 | A                         | Crypto        |           2 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V017       |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V010     | Revision breadth        | Tier 1 | A                         | Equities      |           3 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan |            |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |

Estimable subnetwork size: 3 of 6 nodes.

### R

| var_id   | name                       | tier   | grade   | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width |   tau_posterior_median | peers      |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag   | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:---------------------------|:-------|:--------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|-----------------------:|:-----------|----------------:|----------------------------:|--------------------:|:------------------|:-------------------------|:---------------------|:-----------------|
| V027     | Intermediary capital ratio | Tier 1 | A       | Cross-Asset   |           2 |            0.568 |      0.491 |       0.644 |        1.000 |    1.000 |         1.000 |         1.000 |          1.000 |           0.000 |                    nan | V004       |           1.000 |                       0.600 |               0.341 | ANALYTICAL_ONLY   | FALSE                    | FALSE                | FALSE            |
| V018     | BTC 3m basis               | Tier 1 | B       | Crypto        |           2 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V016       |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V016     | BTC perp funding rate      | Tier 1 | B       | Crypto        |           2 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V018       |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V015     | BTC realized vol           | Tier 1 | A       | Crypto        |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan |            |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V004     | HY OAS                     | Tier 1 | A       | Cross-Asset   |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V027       |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V002     | MOVE Index                 | Tier 1 | A       | Cross-Asset   |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V001       |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V005     | NFCI                       | Tier 1 | A       | Cross-Asset   |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan |            |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |
| V001     | VIX                        | Tier 1 | A       | Cross-Asset   |           1 |          nan     |    nan     |     nan     |      nan     |  nan     |       nan     |       nan     |        nan     |         nan     |                    nan | V004; V027 |         nan     |                     nan     |             nan     | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | FALSE            |

Estimable subnetwork size: 1 of 8 nodes.

### Overlay

| var_id   | name                                     | tier   | grade                     | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width |   tau_posterior_median | peers            |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag   | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:-----------------------------------------|:-------|:--------------------------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|-----------------------:|:-----------------|----------------:|----------------------------:|--------------------:|:------------------|:-------------------------|:---------------------|:-----------------|
| C001     | 200-DMA regime filter                    | Tier 3 | Candidate (working paper) | Equities      |           1 |              nan |        nan |         nan |          nan |      nan |           nan |           nan |            nan |             nan |                    nan | V009; V026; C002 |             nan |                         nan |                 nan | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | NO_NUMERIC_INPUT |
| C002     | Market breadth (% constituents >200-DMA) | Tier 3 | Candidate (peer-reviewed) | Equities      |           1 |              nan |        nan |         nan |          nan |      nan |           nan |           nan |            nan |             nan |                    nan | C001; V031; V009 |             nan |                         nan |                 nan | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | NO_NUMERIC_INPUT |
| C003     | VIX term structure backwardation         | Tier 3 | Candidate (peer-reviewed) | Equities      |           1 |              nan |        nan |         nan |          nan |      nan |           nan |           nan |            nan |             nan |                    nan | V001; V002; V031 |             nan |                         nan |                 nan | ANALYTICAL_ONLY   | NO_NUMERIC_INPUT         | NO_NUMERIC_INPUT     | NO_NUMERIC_INPUT |

Estimable subnetwork size: 0 of 3 nodes.

## 3. Heterogeneity flags

Not estimable in the analytical fallback. `tau_k` is `NA` in every group. Any production action requires full MCMC.

## 4. Registry divergence flags

| var_id   | name                       |   registry_published_sharpe |   posterior_median | registry_divergence_flag   |
|:---------|:---------------------------|----------------------------:|-------------------:|:---------------------------|
| V027     | Intermediary capital ratio |                       0.600 |              0.568 | FALSE                      |
| V028     | Basis-momentum             |                       0.800 |              0.790 | FALSE                      |
| V009     | Time-series momentum       |                       0.900 |              0.874 | FALSE                      |
| V026     | Residual momentum (FF5)    |                       0.700 |              0.694 | FALSE                      |

No estimable registry variable breached the `|registry - posterior| > 2 × se` divergence rule.

## 5. Grade-rank consistency

| group   | var_id   | name                    | grade                     |   rank | flag               |
|:--------|:---------|:------------------------|:--------------------------|-------:|:-------------------|
| S       | V011     | Brent M1-M3 curve slope | A                         |      2 | GRADE_A_BOTTOM_3   |
| T       | V026     | Residual momentum (FF5) | A                         |      2 | GRADE_A_BOTTOM_3   |
| T       | C004     | Dual momentum / GEM     | Candidate (working paper) |      3 | TIER3_TOP_3_REVIEW |

## 6. Cross-group summary

| group   | var_id   | name                       |   p_top3 |   p_beats_peers |
|:--------|:---------|:---------------------------|---------:|----------------:|
| S       | V028     | Basis-momentum             |        1 |           0.807 |
| S       | V011     | Brent M1-M3 curve slope    |        1 |           0.193 |
| T       | V009     | Time-series momentum       |        1 |           0.991 |
| T       | V026     | Residual momentum (FF5)    |        1 |           0.009 |
| T       | C004     | Dual momentum / GEM        |        1 |           0     |
| R       | V027     | Intermediary capital ratio |        1 |           1     |

Cross-group values are not on a common scale and must not be used to rank S versus T versus R versus Overlay directly.

Because the estimable subnetworks are small (S=2, T=3, R=1), `p_top3` is mechanically uninformative in this pass. `p_beats_peers` carries the useful discrimination.

## 7. Prior sensitivity

| var_id   | score_component   |   strict_rank |   loose_rank |   rank_shift | prior_dependent   |
|:---------|:------------------|--------------:|-------------:|-------------:|:------------------|
| V027     | R                 |             1 |            1 |            0 | False             |
| V028     | S                 |             1 |            1 |            0 | False             |
| V011     | S                 |             2 |            2 |            0 | False             |
| V009     | T                 |             1 |            1 |            0 | False             |
| V026     | T                 |             2 |            3 |            1 | False             |
| C004     | T                 |             3 |            2 |           -1 | False             |

No variable moved by 3 or more ranks under the loose-prior rerun. The main sensitivity was C004 improving by one rank inside the T estimable subset when the candidate prior was relaxed.

## 8. Feed to 2026-10-14 audit

| var_id   | name                       |   posterior_mean |   p_beats_peers | registry_divergence   | GO_NO_GO   | rationale                                                                                                            |
|:---------|:---------------------------|-----------------:|----------------:|:----------------------|:-----------|:---------------------------------------------------------------------------------------------------------------------|
| V026     | Residual momentum (FF5)    |            0.694 |           0.009 | FALSE                 | NO-GO      | posterior clearly positive                                                                                           |
| V027     | Intermediary capital ratio |            0.568 |           1     | FALSE                 | GO         | posterior clearly positive; beats peers; peer comparison falls back to p_rank1 because V004 lacks numeric extraction |
| V028     | Basis-momentum             |            0.79  |           0.807 | FALSE                 | GO         | posterior clearly positive; beats peers                                                                              |

## 9. Tier 3 graduation recommendations

| var_id   | name                                     | p_positive   | p_beats_peers   | recommend_grade_B   | note                               |
|:---------|:-----------------------------------------|:-------------|:----------------|:--------------------|:-----------------------------------|
| C005     | Global M2 money supply                   | NA           | NA              | NO                  | No numeric extraction yet.         |
| C004     | Dual momentum / GEM                      | 1.000        | 0.000           | NO                  | Not enough evidence for promotion. |
| C001     | 200-DMA regime filter                    | NA           | NA              | NO                  | No numeric extraction yet.         |
| C002     | Market breadth (% constituents >200-DMA) | NA           | NA              | NO                  | No numeric extraction yet.         |
| C003     | VIX term structure backwardation         | NA           | NA              | NO                  | No numeric extraction yet.         |

## 10. Memory-ready insights

- The estimable T subset is still dominated by registered momentum variables; under the strict candidate prior, V009 remains the clear leader and C004 shrinks materially.
- V028 basis-momentum beats its declared peer V011 with high probability in the estimable S subset and remains audit-worthy.
- V027 intermediary capital stays positive after shrinkage, but peer comparison is incomplete until V004 HY OAS receives a model-ready Sharpe/SE extraction.
- The current bottleneck is numeric extraction depth, not variable breadth. Most overlay and several structural/risk rows are conceptually admitted yet quantitatively unscored.
- No estimable registry variable triggered a 2×SE registry-divergence update in the analytical pass.


---

# Candidate Pipeline

# Candidate pipeline

| var_id   | name                                     | score_component   | status                 | peers                  | verdict             | note                                                                                                               |
|:---------|:-----------------------------------------|:------------------|:-----------------------|:-----------------------|:--------------------|:-------------------------------------------------------------------------------------------------------------------|
| V020     | News sentiment                           | C                 | registered             | NA                     | WATCH               | Catalyst-scale effect; off main Sharpe scale and kept outside BNMA main pool.                                      |
| V029     | GEX (Gamma Exposure)                     | Overlay           | registered provisional | V001; V002; C003       | WATCH               | Mechanism is coherent but prior design parks it for Stage F until direct long-short scale extraction is available. |
| V030     | Cross-asset lead-lag                     | T                 | registered provisional | V009; V014; V017       | WATCH               | Independent information is plausible, but the intake is too thin to distinguish it from existing timing signals.   |
| V031     | Correlation-regime signal quality        | Overlay           | registered provisional | C002; C003             | NEEDS_MORE_EVIDENCE | Useful as a crisis-state filter, but no model-ready Sharpe/SE pair was extracted.                                  |
| V032     | Decision tree feature importance         | Overlay           | registered ungraded    | V029; V031             | NEEDS_MORE_EVIDENCE | Meta-variable rather than standalone signal; keep out of pooled ranking until a stable effect-size design exists.  |
| V033     | Calendar/seasonal                        | C                 | registered ungraded    | NA                     | WATCH               | Event-study scale; keep in catalyst sleeve instead of the main BNMA.                                               |
| C001     | 200-DMA regime filter                    | Overlay           | Tier 3 admitted        | V009; V026; C002       | NEEDS_MORE_EVIDENCE | Admitted on mechanism, but no model-ready Sharpe/SE pair is available yet.                                         |
| C002     | Market breadth (% constituents >200-DMA) | Overlay           | Tier 3 admitted        | C001; V031; V009       | NEEDS_MORE_EVIDENCE | Admitted on mechanism, but the current intake remains non-numeric for BNMA scoring.                                |
| C003     | VIX term structure backwardation         | Overlay           | Tier 3 admitted        | V001; V002; V031       | NEEDS_MORE_EVIDENCE | Good economic rationale, insufficient quantitative extraction for scoring.                                         |
| C004     | Dual momentum / GEM                      | T                 | Tier 3 admitted        | V009; V026             | WATCH               | Posterior stays positive but loses the peer contest under the strict candidate prior.                              |
| C005     | Global M2 money supply                   | S                 | Tier 3 admitted        | V003; V007; V012; V019 | NEEDS_MORE_EVIDENCE | Working-paper support exists, but Stage A lacked a directly usable Sharpe/SE pair.                                 |

## Stage G

Skipped. No out-of-sample signal ledger was provided.

