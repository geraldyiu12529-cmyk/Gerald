# BNMA Consolidated Package

**Status:** analytical approximation; full MCMC required for production use.

This file consolidates the Stage A inventory, summaries, rejected candidates, network construction notes, model code, ranking tables, candidate pipeline, and final report.

## Contents

- [Stage A summary](#stage-a-summary)
- [Stage A enriched data](#stage-a-enriched-data)
- [Stage A raw data](#stage-a-raw-data)
- [Rejected / deferred candidates](#rejected--deferred-candidates)
- [Network construction notes](#network-construction-notes)
- [Model code](#model-code)
- [Ranking tables](#ranking-tables)
- [Candidate pipeline](#candidate-pipeline)
- [Primary report](#primary-report)

## Stage A summary

# Stage A summary

- Registry A/B rows processed: 23
- Replication rows added (Tier 2): 16
- Admitted Tier 3 candidates: 2
- Rejected / deferred Tier 3 candidates: 15
- Registry-validation FAIL rows: 0
- Search-cap note: Tier 3 verification exceeded the nominal search budget by 6 search queries while validating borderline candidates; no further Tier 3 searches were run after detection.

## Studies per variable
| var_id   | name                         |   n_studies |
|:---------|:-----------------------------|------------:|
| C001     | MVRV / NVRV oscillator       |           1 |
| C002     | NVT signal oscillator        |           1 |
| V001     | VIX                          |           1 |
| V002     | MOVE Index                   |           1 |
| V003     | DXY (Dollar Index)           |           2 |
| V004     | HY OAS                       |           2 |
| V005     | NFCI                         |           1 |
| V006     | UST 2Y/10Y yields            |           1 |
| V007     | Real yield / breakevens      |           1 |
| V008     | ACM Term Premium 10Y         |           1 |
| V009     | Time-series momentum (TSMOM) |           5 |
| V010     | Revision breadth             |           1 |
| V011     | Brent M1-M3 curve slope      |           3 |
| V012     | BTC active addresses         |           2 |
| V013     | BTC hash rate                |           2 |
| V014     | BTC exchange netflows        |           1 |
| V015     | BTC realized vol             |           1 |
| V016     | BTC perp funding rate        |           1 |
| V017     | BTC ETF net flows            |           1 |
| V018     | BTC 3m basis                 |           2 |
| V019     | MVRV / SOPR                  |           1 |
| V020     | News sentiment               |           3 |
| V026     | Residual momentum (FF5)      |           2 |
| V027     | Intermediary capital ratio   |           2 |
| V028     | Basis-momentum               |           2 |

## Admitted Tier 3 candidates
| var_id   | name                   | score_component   | grade                     | source_paper                                               | correlation_peers   |
|:---------|:-----------------------|:------------------|:--------------------------|:-----------------------------------------------------------|:--------------------|
| C001     | MVRV / NVRV oscillator | T                 | Candidate (working paper) | Yang & Fantazzini (2022) MPRA / forthcoming in Information | V019; V012          |
| C002     | NVT signal oscillator  | T                 | Candidate (working paper) | Yang & Fantazzini (2022) MPRA / forthcoming in Information | V019; V012          |

## Registry-validation FAILs
None.


## Stage A enriched data

| var_id   | name                         | score_component   | tier   | grade                     | source_paper                                                                | asset_class   | study_id   | is_primary_or_replication   | sharpe_annualized   | sharpe_se          | n_months   | universe                           | sample_start   | sample_end   | is_oos     | transaction_costs_included             | se_imputed   | registry_validation   | score_component_inferred   | correlation_inferred   | correlation_peers   | extraction_flag   |
|:---------|:-----------------------------|:------------------|:-------|:--------------------------|:----------------------------------------------------------------------------|:--------------|:-----------|:----------------------------|:--------------------|:-------------------|:-----------|:-----------------------------------|:---------------|:-------------|:-----------|:---------------------------------------|:-------------|:----------------------|:---------------------------|:-----------------------|:--------------------|:------------------|
| V001     | VIX                          | R                 | Tier1  | A                         | Whaley (2000) JD                                                            | Cross-Asset   | V001-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V002     | MOVE Index                   | R                 | Tier1  | A                         | Siriwardane (2019) JF                                                       | Cross-Asset   | V002-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V003     | DXY (Dollar Index)           | S                 | Tier1  | A                         | Verdelhan (2018) JF                                                         | Cross-Asset   | V003-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V007; V011          | NUMERIC_MISSING   |
| V004     | HY OAS                       | R                 | Tier1  | A                         | Gilchrist-Zakrajsek (2012) AER                                              | Cross-Asset   | V004-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V027                | NUMERIC_MISSING   |
| V005     | NFCI                         | R                 | Tier1  | A                         | Brave-Butters (2012) Chicago Fed                                            | Cross-Asset   | V005-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V006     | UST 2Y/10Y yields            | S                 | Tier1  | A                         | Campbell-Shiller (1991); Adrian-Crump-Moench (2013)                         | Rates         | V006-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V008                | NUMERIC_MISSING   |
| V007     | Real yield / breakevens      | S                 | Tier1  | A                         | D'Amico et al. (2018)                                                       | Rates         | V007-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V003                | NUMERIC_MISSING   |
| V008     | ACM Term Premium 10Y         | S                 | Tier1  | A                         | Adrian-Crump-Moench (2013) JFE                                              | Rates         | V008-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V006                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier1  | A                         | Moskowitz-Ooi-Pedersen (2012) JFE                                           | All           | V009-P1    | primary                     | 0.9                 | 0.0684348838921593 | 300.0      |                                    | 1985-01        | 2009-12      |            | mixed/unspecified                      | True         | PASS                  | False                      | False                  | V026; V030          | OK                |
| V010     | Revision breadth             | T                 | Tier1  | A                         | Gleason-Lee (2003)                                                          | Equities      | V010-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V011     | Brent M1-M3 curve slope      | S                 | Tier1  | A                         | Gorton-Hayashi-Rouwenhorst (2013) JF                                        | Commodities   | V011-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V028                | NUMERIC_MISSING   |
| V012     | BTC active addresses         | S                 | Tier1  | A                         | Liu-Tsyvinski (2021) JF                                                     | Crypto        | V012-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V019                | NUMERIC_MISSING   |
| V013     | BTC hash rate                | S                 | Tier1  | A                         | Cong-He-Li (2021)                                                           | Crypto        | V013-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V012; V019          | NUMERIC_MISSING   |
| V014     | BTC exchange netflows        | T                 | Tier1  | A                         | Aloosh-Ouzan-Shahzad (2023)                                                 | Crypto        | V014-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V017; V016          | NUMERIC_MISSING   |
| V015     | BTC realized vol             | R                 | Tier1  | A                         | Liu-Tsyvinski (2021) JF                                                     | Crypto        | V015-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V016; V018          | NUMERIC_MISSING   |
| V016     | BTC perp funding rate        | R                 | Tier1  | B                         | Aloosh-Ouzan-Shahzad (2023) partial + practitioner                          | Crypto        | V016-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V018; V015          | NUMERIC_MISSING   |
| V017     | BTC ETF net flows            | T                 | Tier1  | B                         | Institutional flow literature / no direct peer-reviewed primary             | Crypto        | V017-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V014                | NUMERIC_MISSING   |
| V018     | BTC 3m basis                 | R                 | Tier1  | B                         | Practitioner + carry literature                                             | Crypto        | V018-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V016; V015          | NUMERIC_MISSING   |
| V019     | MVRV / SOPR                  | S                 | Tier1  | B                         | Practitioner-dominant (limited peer-reviewed)                               | Crypto        | V019-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V012; V013          | NUMERIC_MISSING   |
| V020     | News sentiment               | C                 | Tier1  | B                         | Tetlock (2007) JF                                                           | Cross-Asset   | V020-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V026     | Residual momentum (FF5)      | T                 | Tier1  | A                         | Blitz-Huij-Martens (2011) JEF                                               | Equities      | V026-P1    | primary                     | 0.7                 | 0.0360121507272198 | 960.0      |                                    | 1930-01        | 2009-12      |            | mixed/unspecified                      | True         | PASS                  | False                      | False                  | V009                | OK                |
| V027     | Intermediary capital ratio   | R                 | Tier1  | A                         | He-Kelly-Manela (2017) JFE                                                  | Cross-Asset   | V027-P1    | primary                     | 0.6                 | 0.0478207246434676 | 516.0      |                                    | 1970-01        | 2012-12      |            | mixed/unspecified                      | True         | PASS                  | False                      | False                  | V004                | OK                |
| V028     | Basis-momentum               | S                 | Tier1  | A                         | Boons-Prado (2019) JF                                                       | Commodities   | V028-P1    | primary                     | 0.8                 | 0.0453086872289816 | 643.0      |                                    | 1960-08        | 2014-02      |            | mixed/unspecified                      | True         | PASS                  | False                      | False                  | V011                | OK                |
| V003     | DXY (Dollar Index)           | S                 | Tier2  | A                         | BIS Working Paper 1083 (replication on copper/tin)                          | Cross-Asset   | V003-R1    | replication                 |                     |                    |            | Copper/tin cross-asset replication |                |              |            |                                        | False        |                       | False                      | False                  | V007; V011          | NUMERIC_MISSING   |
| V004     | HY OAS                       | R                 | Tier2  | A                         | Gilchrist-Zakrajsek (2012) excess bond premium / expected default frequency | Cross-Asset   | V004-R1    | replication                 |                     |                    |            | US credit                          |                |              |            |                                        | False        |                       | False                      | False                  | V027                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Hurst-Ooi-Pedersen (2017) AQR                                               | All           | V009-R1    | replication                 |                     |                    |            | 67 markets                         |                |              | mixed      | implementation-adjusted                | False        |                       | False                      | False                  | V026                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Daniel-Moskowitz (2016) JF                                                  | Equities      | V009-R2    | replication                 |                     |                    |            | Equity momentum                    |                |              | mixed      |                                        | False        |                       | False                      | False                  | V026                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Han et al. (2024) crypto TS momentum                                        | Crypto        | V009-R3    | replication                 | 1.51                |                    |            | crypto cross-section / TS          |                |              | likely OOS |                                        | False        |                       | False                      | False                  | V026                | OK                |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Sadaqat-Butt (2023) stop-loss momentum                                      | Crypto        | V009-R4    | replication                 | -0.235              |                    |            | 147 cryptocurrencies               |                |              | mixed      |                                        | False        |                       | False                      | False                  | V026                | OK                |
| V011     | Brent M1-M3 curve slope      | S                 | Tier2  | A                         | Koijen-Moskowitz-Pedersen-Vrugt (2018)                                      | Cross-Asset   | V011-R1    | replication                 | 0.74                | 0.0740980245443784 | 232.0      | carry across asset classes         | 1991-11        | 2011-02      | mixed      | mixed/unspecified                      | True         |                       | False                      | False                  | V028                | OK                |
| V011     | Brent M1-M3 curve slope      | S                 | Tier2  | A                         | Szymanowska-de Roon-Nijman-van den Goorbergh (2014) JF                      | Commodities   | V011-R2    | replication                 |                     |                    |            | commodity futures                  |                |              |            |                                        | False        |                       | False                      | False                  | V028                | NUMERIC_MISSING   |
| V012     | BTC active addresses         | S                 | Tier2  | A                         | Cong-He-Li (2021)                                                           | Crypto        | V012-R1    | replication                 |                     |                    |            | Crypto on-chain fundamentals       |                |              |            |                                        | False        |                       | False                      | False                  | V019                | NUMERIC_MISSING   |
| V013     | BTC hash rate                | S                 | Tier2  | A                         | Cong-He-Li (2021)                                                           | Crypto        | V013-R1    | replication                 |                     |                    |            | Crypto on-chain fundamentals       |                |              |            |                                        | False        |                       | False                      | False                  | V012; V019          | NUMERIC_MISSING   |
| V018     | BTC 3m basis                 | R                 | Tier2  | B                         | Borri et al. (2025) crypto carry                                            | Crypto        | V018-R1    | replication                 | 6.45                | 0.6027886583759408 | 60.0       | Crypto carry 2020-2025             | 2020-01        | 2025-12      | mixed      | likely net of fees not fully specified | True         |                       | False                      | False                  | V016; V015          | OK                |
| V020     | News sentiment               | C                 | Tier2  | B                         | Garcia (2013)                                                               | Cross-Asset   | V020-R1    | replication                 |                     |                    |            | News text sentiment                |                |              |            |                                        | False        |                       | False                      | False                  |                     | NUMERIC_MISSING   |
| V020     | News sentiment               | C                 | Tier2  | B                         | Gu-Kurov (2020) Twitter sentiment                                           | Cross-Asset   | V020-R2    | replication                 | 3.17                |                    |            | Twitter sentiment                  |                |              | pre-cost   | before costs                           | False        |                       | False                      | False                  |                     | OK                |
| V026     | Residual momentum (FF5)      | T                 | Tier2  | A                         | Asness-Moskowitz-Pedersen (2013) JF                                         | Equities      | V026-R1    | replication                 |                     |                    |            | value and momentum everywhere      |                |              |            |                                        | False        |                       | False                      | False                  | V009                | NUMERIC_MISSING   |
| V027     | Intermediary capital ratio   | R                 | Tier2  | A                         | Adrian-Etula-Muir (2014) JF                                                 | Cross-Asset   | V027-R1    | replication                 |                     |                    |            | broker-dealer leverage factor      |                |              |            |                                        | False        |                       | False                      | False                  | V004                | NUMERIC_MISSING   |
| V028     | Basis-momentum               | S                 | Tier2  | A                         | Szymanowska et al. (2014) JF                                                | Commodities   | V028-R1    | replication                 |                     |                    |            | commodity futures risk premia      |                |              |            |                                        | False        |                       | False                      | False                  | V011                | NUMERIC_MISSING   |
| C001     | MVRV / NVRV oscillator       | T                 | Tier3  | Candidate (working paper) | Yang & Fantazzini (2022) MPRA / forthcoming in Information                  | Crypto        | C001-P1    | primary                     | 0.41                | 0.0923895382153928 | 127.0      | BTC daily long-short oscillator    | 2011-08        | 2022-03      | mixed      | backtest; no explicit cost schedule    | True         |                       | True                       | True                   | V019; V012          | OK                |
| C002     | NVT signal oscillator        | T                 | Tier3  | Candidate (working paper) | Yang & Fantazzini (2022) MPRA / forthcoming in Information                  | Crypto        | C002-P1    | primary                     | 0.31                | 0.0908425132012782 | 127.0      | BTC daily long-short oscillator    | 2011-08        | 2022-03      | mixed      | backtest; no explicit cost schedule    | True         |                       | True                       | True                   | V019; V012          | OK                |


## Stage A raw data

| var_id   | name                         | score_component   | tier   | grade                     | source_paper                                                                | asset_class   | study_id   | is_primary_or_replication   | sharpe_annualized   | sharpe_se          | n_months   | universe                           | sample_start   | sample_end   | is_oos     | transaction_costs_included             | se_imputed   | registry_validation   | score_component_inferred   | correlation_inferred   | correlation_peers   | extraction_flag   |
|:---------|:-----------------------------|:------------------|:-------|:--------------------------|:----------------------------------------------------------------------------|:--------------|:-----------|:----------------------------|:--------------------|:-------------------|:-----------|:-----------------------------------|:---------------|:-------------|:-----------|:---------------------------------------|:-------------|:----------------------|:---------------------------|:-----------------------|:--------------------|:------------------|
| V001     | VIX                          | R                 | Tier1  | A                         | Whaley (2000) JD                                                            | Cross-Asset   | V001-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V002     | MOVE Index                   | R                 | Tier1  | A                         | Siriwardane (2019) JF                                                       | Cross-Asset   | V002-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V003     | DXY (Dollar Index)           | S                 | Tier1  | A                         | Verdelhan (2018) JF                                                         | Cross-Asset   | V003-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V007; V011          | NUMERIC_MISSING   |
| V004     | HY OAS                       | R                 | Tier1  | A                         | Gilchrist-Zakrajsek (2012) AER                                              | Cross-Asset   | V004-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V027                | NUMERIC_MISSING   |
| V005     | NFCI                         | R                 | Tier1  | A                         | Brave-Butters (2012) Chicago Fed                                            | Cross-Asset   | V005-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V006     | UST 2Y/10Y yields            | S                 | Tier1  | A                         | Campbell-Shiller (1991); Adrian-Crump-Moench (2013)                         | Rates         | V006-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V008                | NUMERIC_MISSING   |
| V007     | Real yield / breakevens      | S                 | Tier1  | A                         | D'Amico et al. (2018)                                                       | Rates         | V007-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V003                | NUMERIC_MISSING   |
| V008     | ACM Term Premium 10Y         | S                 | Tier1  | A                         | Adrian-Crump-Moench (2013) JFE                                              | Rates         | V008-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V006                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier1  | A                         | Moskowitz-Ooi-Pedersen (2012) JFE                                           | All           | V009-P1    | primary                     | 0.9                 |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V026; V030          | OK                |
| V010     | Revision breadth             | T                 | Tier1  | A                         | Gleason-Lee (2003)                                                          | Equities      | V010-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V011     | Brent M1-M3 curve slope      | S                 | Tier1  | A                         | Gorton-Hayashi-Rouwenhorst (2013) JF                                        | Commodities   | V011-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V028                | NUMERIC_MISSING   |
| V012     | BTC active addresses         | S                 | Tier1  | A                         | Liu-Tsyvinski (2021) JF                                                     | Crypto        | V012-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V019                | NUMERIC_MISSING   |
| V013     | BTC hash rate                | S                 | Tier1  | A                         | Cong-He-Li (2021)                                                           | Crypto        | V013-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V012; V019          | NUMERIC_MISSING   |
| V014     | BTC exchange netflows        | T                 | Tier1  | A                         | Aloosh-Ouzan-Shahzad (2023)                                                 | Crypto        | V014-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V017; V016          | NUMERIC_MISSING   |
| V015     | BTC realized vol             | R                 | Tier1  | A                         | Liu-Tsyvinski (2021) JF                                                     | Crypto        | V015-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V016; V018          | NUMERIC_MISSING   |
| V016     | BTC perp funding rate        | R                 | Tier1  | B                         | Aloosh-Ouzan-Shahzad (2023) partial + practitioner                          | Crypto        | V016-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V018; V015          | NUMERIC_MISSING   |
| V017     | BTC ETF net flows            | T                 | Tier1  | B                         | Institutional flow literature / no direct peer-reviewed primary             | Crypto        | V017-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V014                | NUMERIC_MISSING   |
| V018     | BTC 3m basis                 | R                 | Tier1  | B                         | Practitioner + carry literature                                             | Crypto        | V018-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V016; V015          | NUMERIC_MISSING   |
| V019     | MVRV / SOPR                  | S                 | Tier1  | B                         | Practitioner-dominant (limited peer-reviewed)                               | Crypto        | V019-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V012; V013          | NUMERIC_MISSING   |
| V020     | News sentiment               | C                 | Tier1  | B                         | Tetlock (2007) JF                                                           | Cross-Asset   | V020-P1    | primary                     |                     |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  |                     | NUMERIC_MISSING   |
| V026     | Residual momentum (FF5)      | T                 | Tier1  | A                         | Blitz-Huij-Martens (2011) JEF                                               | Equities      | V026-P1    | primary                     | 0.7                 |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V009                | OK                |
| V027     | Intermediary capital ratio   | R                 | Tier1  | A                         | He-Kelly-Manela (2017) JFE                                                  | Cross-Asset   | V027-P1    | primary                     | 0.6                 |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V004                | OK                |
| V028     | Basis-momentum               | S                 | Tier1  | A                         | Boons-Prado (2019) JF                                                       | Commodities   | V028-P1    | primary                     | 0.8                 |                    |            |                                    |                |              |            |                                        | False        | PASS                  | False                      | False                  | V011                | OK                |
| V003     | DXY (Dollar Index)           | S                 | Tier2  | A                         | BIS Working Paper 1083 (replication on copper/tin)                          | Cross-Asset   | V003-R1    | replication                 |                     |                    |            | Copper/tin cross-asset replication |                |              |            |                                        | False        |                       | False                      | False                  | V007; V011          | NUMERIC_MISSING   |
| V004     | HY OAS                       | R                 | Tier2  | A                         | Gilchrist-Zakrajsek (2012) excess bond premium / expected default frequency | Cross-Asset   | V004-R1    | replication                 |                     |                    |            | US credit                          |                |              |            |                                        | False        |                       | False                      | False                  | V027                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Hurst-Ooi-Pedersen (2017) AQR                                               | All           | V009-R1    | replication                 |                     |                    |            | 67 markets                         |                |              | mixed      | implementation-adjusted                | False        |                       | False                      | False                  | V026                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Daniel-Moskowitz (2016) JF                                                  | Equities      | V009-R2    | replication                 |                     |                    |            | Equity momentum                    |                |              | mixed      |                                        | False        |                       | False                      | False                  | V026                | NUMERIC_MISSING   |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Han et al. (2024) crypto TS momentum                                        | Crypto        | V009-R3    | replication                 | 1.51                |                    |            | crypto cross-section / TS          |                |              | likely OOS |                                        | False        |                       | False                      | False                  | V026                | OK                |
| V009     | Time-series momentum (TSMOM) | T                 | Tier2  | A                         | Sadaqat-Butt (2023) stop-loss momentum                                      | Crypto        | V009-R4    | replication                 | -0.235              |                    |            | 147 cryptocurrencies               |                |              | mixed      |                                        | False        |                       | False                      | False                  | V026                | OK                |
| V011     | Brent M1-M3 curve slope      | S                 | Tier2  | A                         | Koijen-Moskowitz-Pedersen-Vrugt (2018)                                      | Cross-Asset   | V011-R1    | replication                 | 0.74                |                    |            | carry across asset classes         |                |              | mixed      |                                        | False        |                       | False                      | False                  | V028                | OK                |
| V011     | Brent M1-M3 curve slope      | S                 | Tier2  | A                         | Szymanowska-de Roon-Nijman-van den Goorbergh (2014) JF                      | Commodities   | V011-R2    | replication                 |                     |                    |            | commodity futures                  |                |              |            |                                        | False        |                       | False                      | False                  | V028                | NUMERIC_MISSING   |
| V012     | BTC active addresses         | S                 | Tier2  | A                         | Cong-He-Li (2021)                                                           | Crypto        | V012-R1    | replication                 |                     |                    |            | Crypto on-chain fundamentals       |                |              |            |                                        | False        |                       | False                      | False                  | V019                | NUMERIC_MISSING   |
| V013     | BTC hash rate                | S                 | Tier2  | A                         | Cong-He-Li (2021)                                                           | Crypto        | V013-R1    | replication                 |                     |                    |            | Crypto on-chain fundamentals       |                |              |            |                                        | False        |                       | False                      | False                  | V012; V019          | NUMERIC_MISSING   |
| V018     | BTC 3m basis                 | R                 | Tier2  | B                         | Borri et al. (2025) crypto carry                                            | Crypto        | V018-R1    | replication                 | 6.45                | 0.6027886583759408 | 60.0       | Crypto carry 2020-2025             | 2020-01        | 2025-12      | mixed      | likely net of fees not fully specified | True         |                       | False                      | False                  | V016; V015          | OK                |
| V020     | News sentiment               | C                 | Tier2  | B                         | Garcia (2013)                                                               | Cross-Asset   | V020-R1    | replication                 |                     |                    |            | News text sentiment                |                |              |            |                                        | False        |                       | False                      | False                  |                     | NUMERIC_MISSING   |
| V020     | News sentiment               | C                 | Tier2  | B                         | Gu-Kurov (2020) Twitter sentiment                                           | Cross-Asset   | V020-R2    | replication                 | 3.17                |                    |            | Twitter sentiment                  |                |              | pre-cost   | before costs                           | False        |                       | False                      | False                  |                     | OK                |
| V026     | Residual momentum (FF5)      | T                 | Tier2  | A                         | Asness-Moskowitz-Pedersen (2013) JF                                         | Equities      | V026-R1    | replication                 |                     |                    |            | value and momentum everywhere      |                |              |            |                                        | False        |                       | False                      | False                  | V009                | NUMERIC_MISSING   |
| V027     | Intermediary capital ratio   | R                 | Tier2  | A                         | Adrian-Etula-Muir (2014) JF                                                 | Cross-Asset   | V027-R1    | replication                 |                     |                    |            | broker-dealer leverage factor      |                |              |            |                                        | False        |                       | False                      | False                  | V004                | NUMERIC_MISSING   |
| V028     | Basis-momentum               | S                 | Tier2  | A                         | Szymanowska et al. (2014) JF                                                | Commodities   | V028-R1    | replication                 |                     |                    |            | commodity futures risk premia      |                |              |            |                                        | False        |                       | False                      | False                  | V011                | NUMERIC_MISSING   |
| C001     | MVRV / NVRV oscillator       | T                 | Tier3  | Candidate (working paper) | Yang & Fantazzini (2022) MPRA / forthcoming in Information                  | Crypto        | C001-P1    | primary                     | 0.41                | 0.0923895382153928 | 127.0      | BTC daily long-short oscillator    | 2011-08        | 2022-03      | mixed      | backtest; no explicit cost schedule    | True         |                       | True                       | True                   | V019; V012          | OK                |
| C002     | NVT signal oscillator        | T                 | Tier3  | Candidate (working paper) | Yang & Fantazzini (2022) MPRA / forthcoming in Information                  | Crypto        | C002-P1    | primary                     | 0.31                | 0.0908425132012782 | 127.0      | BTC daily long-short oscillator    | 2011-08        | 2022-03      | mixed      | backtest; no explicit cost schedule    | True         |                       | True                       | True                   | V019; V012          | OK                |


## Rejected / deferred candidates

| name                                      | proposed_score_component   | reason                                                                                                                                                                  | citation                                    |
|:------------------------------------------|:---------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------|
| Token unlock events                       | C                          | Event-study scale, not long-short Sharpe-compatible for BNMA main ranking; keep for Stage F pipeline.                                                                   | Animoca Brands Research / Smartkarma (2025) |
| 200-DMA regime filter (equities)          | Overlay                    | Quantitative evidence found, but accessible result is portfolio-level return/vol/drawdown improvement, not conditional Sharpe-gain ON vs OFF required for Overlay BNMA. | Faber (2007/2013 update)                    |
| VIX term structure (backwardation = buy)  | R/Overlay                  | Predictive coefficients found, but not extractable onto Sharpe-gain scale from accessible source; reserve for Stage F.                                                  | Fassas & Hourvouliades (2019)               |
| Market breadth (% constituents >200-DMA)  | Overlay                    | Supportive literature found, but accessible source did not provide a directly extractable Sharpe-compatible effect for the exact %>200DMA signal.                       | Zaremba et al. (2021); Yu (2025)            |
| Global M2 money supply                    | S                          | Citation quality in supplied context was practitioner-grade; no peer-reviewed or high-quality working-paper quantitative effect verified within search budget.          | Not admitted                                |
| Fear & Greed Index (<10 threshold)        | T                          | Thin-event heuristic with very small N and no verified paper-scale quantitative result within search budget.                                                            | Not admitted                                |
| Whale accumulation / exchange whale ratio | T/R                        | Directional-accuracy claims found for volatility/ML contexts, but variable definition and horizon were too model-specific for clean BNMA admission.                     | Herremans et al. (2022) adjacent only       |
| Funding rate arbitrage (delta-neutral)    | S/R                        | Strategy rather than standalone directional/risk variable; mismatched unit of analysis.                                                                                 | Not admitted                                |
| Pairs trading BTC-ETH cointegration       | T                          | Strategy rather than standalone variable; mismatched unit of analysis.                                                                                                  | Not admitted                                |
| Short-period RSI (2–5 day) on S&P         | T                          | Could not verify a peer-reviewed or high-quality working-paper quantitative result within search budget.                                                                | Not admitted                                |
| Price-to-sales (tech)                     | S                          | Valuation concept is defensible, but no verified factor-style long-short Sharpe result for the specific tech-growth implementation within search budget.                | Not admitted                                |
| Gold/silver ratio                         | S                          | No peer-reviewed or high-quality working-paper quantitative result verified within search budget.                                                                       | Not admitted                                |
| China PMI leading copper                  | S                          | Economic intuition is strong, but no verified paper with directly extractable quantitative result located within search budget.                                         | Not admitted                                |
| Dual momentum / Antonacci GEM             | T                          | Practical strategy, but unit of analysis is a multi-signal portfolio rule rather than a single variable.                                                                | Antonacci GEM                               |
| Hierarchical Risk Parity (HRP)            | R                          | Portfolio construction method, not a signal variable.                                                                                                                   | Burggraf et al. (2020)                      |


## Network construction notes

### S

# Network S

**Nodes (9):** V003 DXY (Dollar Index), V006 UST 2Y/10Y yields, V007 Real yield / breakevens, V008 ACM Term Premium 10Y, V011 Brent M1-M3 curve slope, V012 BTC active addresses, V013 BTC hash rate, V019 MVRV / SOPR, V028 Basis-momentum

**Head-to-head / same-study edges:**
- V011 Brent M1-M3 curve slope ↔ V028 Basis-momentum — same curve-family / carry-basis literature
- V012 BTC active addresses ↔ V013 BTC hash rate — same Cong-He-Li on-chain fundamentals study

**Anchor:** asset-class benchmark node with `alpha_a` intercept.

**Peer map used for marginal contribution:**
- V003: V007
- V006: V008
- V007: V003
- V008: V006
- V011: V028
- V028: V011
- V012: V013, V019
- V013: V012, V019
- V019: V012, V013

**Pooling assumption:** cross-asset pooling within this group rests on a common Sharpe-scale plus an asset-class intercept `alpha_a`; it does **not** rely on a dense indirect-evidence network.

### T

# Network T

**Nodes (7):** C001 MVRV / NVRV oscillator, C002 NVT signal oscillator, V009 Time-series momentum (TSMOM), V010 Revision breadth, V014 BTC exchange netflows, V017 BTC ETF net flows, V026 Residual momentum (FF5)

**Head-to-head / same-study edges:**
- C001 MVRV / NVRV oscillator ↔ C002 NVT signal oscillator — same Yang-Fantazzini study compares both oscillators

**Anchor:** asset-class benchmark node with `alpha_a` intercept.

**Peer map used for marginal contribution:**
- V009: V026
- V026: V009
- V014: V017
- V017: V014
- C001: C002
- C002: C001

**Pooling assumption:** cross-asset pooling within this group rests on a common Sharpe-scale plus an asset-class intercept `alpha_a`; it does **not** rely on a dense indirect-evidence network.

### R

# Network R

**Nodes (8):** V001 VIX, V002 MOVE Index, V004 HY OAS, V005 NFCI, V015 BTC realized vol, V016 BTC perp funding rate, V018 BTC 3m basis, V027 Intermediary capital ratio

**Head-to-head / same-study edges:** none identified from Stage A extractions.

**Anchor:** asset-class benchmark node with `alpha_a` intercept.

**Peer map used for marginal contribution:**
- V001: V002
- V002: V001
- V004: V027
- V027: V004
- V015: V016, V018
- V016: V015, V018
- V018: V015, V016

**Pooling assumption:** cross-asset pooling within this group rests on a common Sharpe-scale plus an asset-class intercept `alpha_a`; it does **not** rely on a dense indirect-evidence network.

### Overlay

# Network Overlay

No eligible Grade A/B or admitted Tier 3 nodes were available for pooled BNMA in this group.

Cross-asset pooling statement: not applicable because the pooled node set is empty.


## Model code

### model_S.py

```python
import pandas as pd
import pymc as pm
import arviz as az
import numpy as np
from pathlib import Path

# Group: S
# Install guidance for a fresh environment:
#   pip install pymc arviz --break-system-packages
#
# Note:
# This template is the full hierarchical model requested in the prompt.
# In the current container, production NUTS sampling was not executed because
# PyMC failed to compile its backend (missing Python.h / C-extension build path).
# Use this file in a properly provisioned local environment or notebook.

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "stage_a_enriched.csv")

def is_main(row):
    sc=row['score_component']
    if sc not in ['S','T','R','Overlay']:
        return False
    tier=row['tier']
    grade=str(row['grade'])
    if tier in ['Tier1','Tier2'] and grade in ['A','B']:
        return True
    if tier=='Tier3' and grade.startswith('Candidate'):
        return True
    return False

main = df[df.apply(is_main, axis=1)].copy()
gdf = main[main['score_component']=="S"].copy()
vars_meta = gdf.sort_values(['var_id','tier']).drop_duplicates('var_id')[['var_id','name','asset_class','grade','tier']].reset_index(drop=True)
obs = gdf[gdf['sharpe_annualized'].notna() & gdf['sharpe_se'].notna() & (gdf['extraction_flag']=="OK")].copy()

def prior_sd(group, grade):
    if isinstance(grade, str) and grade.startswith('Candidate'):
        wp = 'working paper' in grade
        if group in ['S','T']:
            return 0.05 if wp else 0.10
        return 0.025 if wp else 0.05
    if group in ['S','T']:
        return 0.40 if grade == 'A' else 0.25
    return 0.20 if grade == 'A' else 0.12

tau_prior = dict(S=0.25, T=0.25, R=0.15, Overlay=0.15)

vars_meta['prior_sd'] = vars_meta['grade'].apply(lambda g: prior_sd("S", g))
var_to_idx = {v:i for i,v in enumerate(vars_meta['var_id'])}
obs['var_idx'] = obs['var_id'].map(var_to_idx)

asset_classes = sorted(obs['asset_class'].dropna().unique().tolist())
asset_to_idx = {a:i for i,a in enumerate(asset_classes)}
obs['asset_idx'] = obs['asset_class'].map(asset_to_idx)

coords = {
    "variable": vars_meta['var_id'].tolist(),
    "asset_class": asset_classes,
    "study": obs['study_id'].tolist(),
}

with pm.Model(coords=coords) as model:
    prior_sd_arr = pm.Data("prior_sd_arr", vars_meta['prior_sd'].values, dims="variable")
    mu = pm.Normal("mu", mu=0, sigma=prior_sd_arr, dims="variable")
    tau = pm.HalfNormal("tau", sigma=tau_prior["S"], dims="variable")
    alpha = pm.Normal("alpha", mu=0, sigma=0.3, dims="asset_class")

    # non-centered study effect
    eps = pm.Normal("eps", 0, 1, dims="study")
    theta = pm.Deterministic(
        "theta",
        mu[obs['var_idx'].values] + alpha[obs['asset_idx'].values] + tau[obs['var_idx'].values] * eps,
        dims="study",
    )

    y = pm.Normal(
        "y",
        mu=theta,
        sigma=obs['sharpe_se'].astype(float).values,
        observed=obs['sharpe_annualized'].astype(float).values,
        dims="study",
    )

    idata = pm.sample(
        chains=4,
        tune=2000,
        draws=2000,
        target_accept=0.95,
        random_seed=42,
    )

az.to_netcdf(idata, BASE / "trace_S.nc")

def analytical_fallback(group_name="S"):
    out = []
    for _, r in vars_meta.iterrows():
        prior = prior_sd(group_name, r['grade'])
        rows = obs[obs['var_id'] == r['var_id']]
        if len(rows) == 0:
            mean, sd = 0.0, prior
        else:
            precision = 1/prior**2 + np.sum(1/np.square(rows['sharpe_se'].astype(float)))
            var = 1/precision
            mean = var * np.sum(rows['sharpe_annualized'].astype(float) / np.square(rows['sharpe_se'].astype(float)))
            sd = np.sqrt(var)
        out.append((r['var_id'], mean, sd))
    return pd.DataFrame(out, columns=["var_id", "posterior_mean", "posterior_sd"])

print(analytical_fallback())
```

### model_T.py

```python
import pandas as pd
import pymc as pm
import arviz as az
import numpy as np
from pathlib import Path

# Group: T
# Install guidance for a fresh environment:
#   pip install pymc arviz --break-system-packages
#
# Note:
# This template is the full hierarchical model requested in the prompt.
# In the current container, production NUTS sampling was not executed because
# PyMC failed to compile its backend (missing Python.h / C-extension build path).
# Use this file in a properly provisioned local environment or notebook.

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "stage_a_enriched.csv")

def is_main(row):
    sc=row['score_component']
    if sc not in ['S','T','R','Overlay']:
        return False
    tier=row['tier']
    grade=str(row['grade'])
    if tier in ['Tier1','Tier2'] and grade in ['A','B']:
        return True
    if tier=='Tier3' and grade.startswith('Candidate'):
        return True
    return False

main = df[df.apply(is_main, axis=1)].copy()
gdf = main[main['score_component']=="T"].copy()
vars_meta = gdf.sort_values(['var_id','tier']).drop_duplicates('var_id')[['var_id','name','asset_class','grade','tier']].reset_index(drop=True)
obs = gdf[gdf['sharpe_annualized'].notna() & gdf['sharpe_se'].notna() & (gdf['extraction_flag']=="OK")].copy()

def prior_sd(group, grade):
    if isinstance(grade, str) and grade.startswith('Candidate'):
        wp = 'working paper' in grade
        if group in ['S','T']:
            return 0.05 if wp else 0.10
        return 0.025 if wp else 0.05
    if group in ['S','T']:
        return 0.40 if grade == 'A' else 0.25
    return 0.20 if grade == 'A' else 0.12

tau_prior = dict(S=0.25, T=0.25, R=0.15, Overlay=0.15)

vars_meta['prior_sd'] = vars_meta['grade'].apply(lambda g: prior_sd("T", g))
var_to_idx = {v:i for i,v in enumerate(vars_meta['var_id'])}
obs['var_idx'] = obs['var_id'].map(var_to_idx)

asset_classes = sorted(obs['asset_class'].dropna().unique().tolist())
asset_to_idx = {a:i for i,a in enumerate(asset_classes)}
obs['asset_idx'] = obs['asset_class'].map(asset_to_idx)

coords = {
    "variable": vars_meta['var_id'].tolist(),
    "asset_class": asset_classes,
    "study": obs['study_id'].tolist(),
}

with pm.Model(coords=coords) as model:
    prior_sd_arr = pm.Data("prior_sd_arr", vars_meta['prior_sd'].values, dims="variable")
    mu = pm.Normal("mu", mu=0, sigma=prior_sd_arr, dims="variable")
    tau = pm.HalfNormal("tau", sigma=tau_prior["T"], dims="variable")
    alpha = pm.Normal("alpha", mu=0, sigma=0.3, dims="asset_class")

    # non-centered study effect
    eps = pm.Normal("eps", 0, 1, dims="study")
    theta = pm.Deterministic(
        "theta",
        mu[obs['var_idx'].values] + alpha[obs['asset_idx'].values] + tau[obs['var_idx'].values] * eps,
        dims="study",
    )

    y = pm.Normal(
        "y",
        mu=theta,
        sigma=obs['sharpe_se'].astype(float).values,
        observed=obs['sharpe_annualized'].astype(float).values,
        dims="study",
    )

    idata = pm.sample(
        chains=4,
        tune=2000,
        draws=2000,
        target_accept=0.95,
        random_seed=42,
    )

az.to_netcdf(idata, BASE / "trace_T.nc")

def analytical_fallback(group_name="T"):
    out = []
    for _, r in vars_meta.iterrows():
        prior = prior_sd(group_name, r['grade'])
        rows = obs[obs['var_id'] == r['var_id']]
        if len(rows) == 0:
            mean, sd = 0.0, prior
        else:
            precision = 1/prior**2 + np.sum(1/np.square(rows['sharpe_se'].astype(float)))
            var = 1/precision
            mean = var * np.sum(rows['sharpe_annualized'].astype(float) / np.square(rows['sharpe_se'].astype(float)))
            sd = np.sqrt(var)
        out.append((r['var_id'], mean, sd))
    return pd.DataFrame(out, columns=["var_id", "posterior_mean", "posterior_sd"])

print(analytical_fallback())
```

### model_R.py

```python
import pandas as pd
import pymc as pm
import arviz as az
import numpy as np
from pathlib import Path

# Group: R
# Install guidance for a fresh environment:
#   pip install pymc arviz --break-system-packages
#
# Note:
# This template is the full hierarchical model requested in the prompt.
# In the current container, production NUTS sampling was not executed because
# PyMC failed to compile its backend (missing Python.h / C-extension build path).
# Use this file in a properly provisioned local environment or notebook.

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "stage_a_enriched.csv")

def is_main(row):
    sc=row['score_component']
    if sc not in ['S','T','R','Overlay']:
        return False
    tier=row['tier']
    grade=str(row['grade'])
    if tier in ['Tier1','Tier2'] and grade in ['A','B']:
        return True
    if tier=='Tier3' and grade.startswith('Candidate'):
        return True
    return False

main = df[df.apply(is_main, axis=1)].copy()
gdf = main[main['score_component']=="R"].copy()
vars_meta = gdf.sort_values(['var_id','tier']).drop_duplicates('var_id')[['var_id','name','asset_class','grade','tier']].reset_index(drop=True)
obs = gdf[gdf['sharpe_annualized'].notna() & gdf['sharpe_se'].notna() & (gdf['extraction_flag']=="OK")].copy()

def prior_sd(group, grade):
    if isinstance(grade, str) and grade.startswith('Candidate'):
        wp = 'working paper' in grade
        if group in ['S','T']:
            return 0.05 if wp else 0.10
        return 0.025 if wp else 0.05
    if group in ['S','T']:
        return 0.40 if grade == 'A' else 0.25
    return 0.20 if grade == 'A' else 0.12

tau_prior = dict(S=0.25, T=0.25, R=0.15, Overlay=0.15)

vars_meta['prior_sd'] = vars_meta['grade'].apply(lambda g: prior_sd("R", g))
var_to_idx = {v:i for i,v in enumerate(vars_meta['var_id'])}
obs['var_idx'] = obs['var_id'].map(var_to_idx)

asset_classes = sorted(obs['asset_class'].dropna().unique().tolist())
asset_to_idx = {a:i for i,a in enumerate(asset_classes)}
obs['asset_idx'] = obs['asset_class'].map(asset_to_idx)

coords = {
    "variable": vars_meta['var_id'].tolist(),
    "asset_class": asset_classes,
    "study": obs['study_id'].tolist(),
}

with pm.Model(coords=coords) as model:
    prior_sd_arr = pm.Data("prior_sd_arr", vars_meta['prior_sd'].values, dims="variable")
    mu = pm.Normal("mu", mu=0, sigma=prior_sd_arr, dims="variable")
    tau = pm.HalfNormal("tau", sigma=tau_prior["R"], dims="variable")
    alpha = pm.Normal("alpha", mu=0, sigma=0.3, dims="asset_class")

    # non-centered study effect
    eps = pm.Normal("eps", 0, 1, dims="study")
    theta = pm.Deterministic(
        "theta",
        mu[obs['var_idx'].values] + alpha[obs['asset_idx'].values] + tau[obs['var_idx'].values] * eps,
        dims="study",
    )

    y = pm.Normal(
        "y",
        mu=theta,
        sigma=obs['sharpe_se'].astype(float).values,
        observed=obs['sharpe_annualized'].astype(float).values,
        dims="study",
    )

    idata = pm.sample(
        chains=4,
        tune=2000,
        draws=2000,
        target_accept=0.95,
        random_seed=42,
    )

az.to_netcdf(idata, BASE / "trace_R.nc")

def analytical_fallback(group_name="R"):
    out = []
    for _, r in vars_meta.iterrows():
        prior = prior_sd(group_name, r['grade'])
        rows = obs[obs['var_id'] == r['var_id']]
        if len(rows) == 0:
            mean, sd = 0.0, prior
        else:
            precision = 1/prior**2 + np.sum(1/np.square(rows['sharpe_se'].astype(float)))
            var = 1/precision
            mean = var * np.sum(rows['sharpe_annualized'].astype(float) / np.square(rows['sharpe_se'].astype(float)))
            sd = np.sqrt(var)
        out.append((r['var_id'], mean, sd))
    return pd.DataFrame(out, columns=["var_id", "posterior_mean", "posterior_sd"])

print(analytical_fallback())
```

### model_Overlay.py

```python
import pandas as pd
import pymc as pm
import arviz as az
import numpy as np
from pathlib import Path

# Group: Overlay
# Install guidance for a fresh environment:
#   pip install pymc arviz --break-system-packages
#
# Note:
# This template is the full hierarchical model requested in the prompt.
# In the current container, production NUTS sampling was not executed because
# PyMC failed to compile its backend (missing Python.h / C-extension build path).
# Use this file in a properly provisioned local environment or notebook.

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "stage_a_enriched.csv")

def is_main(row):
    sc=row['score_component']
    if sc not in ['S','T','R','Overlay']:
        return False
    tier=row['tier']
    grade=str(row['grade'])
    if tier in ['Tier1','Tier2'] and grade in ['A','B']:
        return True
    if tier=='Tier3' and grade.startswith('Candidate'):
        return True
    return False

main = df[df.apply(is_main, axis=1)].copy()
gdf = main[main['score_component']=="Overlay"].copy()
vars_meta = gdf.sort_values(['var_id','tier']).drop_duplicates('var_id')[['var_id','name','asset_class','grade','tier']].reset_index(drop=True)
obs = gdf[gdf['sharpe_annualized'].notna() & gdf['sharpe_se'].notna() & (gdf['extraction_flag']=="OK")].copy()

def prior_sd(group, grade):
    if isinstance(grade, str) and grade.startswith('Candidate'):
        wp = 'working paper' in grade
        if group in ['S','T']:
            return 0.05 if wp else 0.10
        return 0.025 if wp else 0.05
    if group in ['S','T']:
        return 0.40 if grade == 'A' else 0.25
    return 0.20 if grade == 'A' else 0.12

tau_prior = dict(S=0.25, T=0.25, R=0.15, Overlay=0.15)

vars_meta['prior_sd'] = vars_meta['grade'].apply(lambda g: prior_sd("Overlay", g))
var_to_idx = {v:i for i,v in enumerate(vars_meta['var_id'])}
obs['var_idx'] = obs['var_id'].map(var_to_idx)

asset_classes = sorted(obs['asset_class'].dropna().unique().tolist())
asset_to_idx = {a:i for i,a in enumerate(asset_classes)}
obs['asset_idx'] = obs['asset_class'].map(asset_to_idx)

coords = {
    "variable": vars_meta['var_id'].tolist(),
    "asset_class": asset_classes,
    "study": obs['study_id'].tolist(),
}

with pm.Model(coords=coords) as model:
    prior_sd_arr = pm.Data("prior_sd_arr", vars_meta['prior_sd'].values, dims="variable")
    mu = pm.Normal("mu", mu=0, sigma=prior_sd_arr, dims="variable")
    tau = pm.HalfNormal("tau", sigma=tau_prior["Overlay"], dims="variable")
    alpha = pm.Normal("alpha", mu=0, sigma=0.3, dims="asset_class")

    # non-centered study effect
    eps = pm.Normal("eps", 0, 1, dims="study")
    theta = pm.Deterministic(
        "theta",
        mu[obs['var_idx'].values] + alpha[obs['asset_idx'].values] + tau[obs['var_idx'].values] * eps,
        dims="study",
    )

    y = pm.Normal(
        "y",
        mu=theta,
        sigma=obs['sharpe_se'].astype(float).values,
        observed=obs['sharpe_annualized'].astype(float).values,
        dims="study",
    )

    idata = pm.sample(
        chains=4,
        tune=2000,
        draws=2000,
        target_accept=0.95,
        random_seed=42,
    )

az.to_netcdf(idata, BASE / "trace_Overlay.nc")

def analytical_fallback(group_name="Overlay"):
    out = []
    for _, r in vars_meta.iterrows():
        prior = prior_sd(group_name, r['grade'])
        rows = obs[obs['var_id'] == r['var_id']]
        if len(rows) == 0:
            mean, sd = 0.0, prior
        else:
            precision = 1/prior**2 + np.sum(1/np.square(rows['sharpe_se'].astype(float)))
            var = 1/precision
            mean = var * np.sum(rows['sharpe_annualized'].astype(float) / np.square(rows['sharpe_se'].astype(float)))
            sd = np.sqrt(var)
        out.append((r['var_id'], mean, sd))
    return pd.DataFrame(out, columns=["var_id", "posterior_mean", "posterior_sd"])

print(analytical_fallback())
```


## Ranking tables

### S

| var_id   | name                    | tier   | grade   | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width | tau_posterior_median   | peers      |   p_beats_peers | registry_published_sharpe   |   post_decay_sharpe | divergence_flag        | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:------------------------|:-------|:--------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|:-----------------------|:-----------|----------------:|:----------------------------|--------------------:|:-----------------------|:-------------------------|:---------------------|:-----------------|
| V028     | Basis-momentum          | Tier1  | A       | Commodities   |           2 |         0.789866 |   0.701627 |    0.878105 |          1   | 0.9972   |             1 |             1 |              2 |               1 | NA_ANALYTICAL          | V011       |        0.807708 | 0.8                         |         0.473998    | False                  | False                    | False                | False            |
| V011     | Brent M1-M3 curve slope | Tier1  | A       | Commodities   |           3 |         0.715449 |   0.572649 |    0.858249 |          1   | 0.977472 |             2 |             1 |              3 |               2 | NA_ANALYTICAL          | V028       |        0.192292 |                             |         0.715662    | N/A_NO_REGISTRY_SHARPE | False                    | False                | False            |
| V003     | DXY (Dollar Index)      | Tier1  | A       | Cross-Asset   |           2 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.159144 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V007       |        0.501148 |                             |        -0.000322658 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V012     | BTC active addresses    | Tier1  | A       | Crypto        |           2 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.1587   |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V013; V019 |        0.353404 |                             |         0.000238426 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V006     | UST 2Y/10Y yields       | Tier1  | A       | Rates         |           1 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.158624 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V008       |        0.499964 |                             |        -0.00103982  | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V008     | ACM Term Premium 10Y    | Tier1  | A       | Rates         |           1 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.158388 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V006       |        0.500036 |                             |         0.000746731 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V013     | BTC hash rate           | Tier1  | A       | Crypto        |           2 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.157904 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V012; V019 |        0.352532 |                             |         0.000427494 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V007     | Real yield / breakevens | Tier1  | A       | Rates         |           1 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.157688 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V003       |        0.498852 |                             |        -0.000579312 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V019     | MVRV / SOPR             | Tier1  | B       | Crypto        |           1 |         0        |  -0.489991 |    0.489991 |          0.5 | 0.07488  |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V012; V013 |        0.294064 |                             |        -0.000139862 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |

### T

| var_id   | name                         | tier   | grade                     | asset_class   |   n_studies |   posterior_mean |    ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width | tau_posterior_median   | peers   |   p_beats_peers | registry_published_sharpe   |   post_decay_sharpe | divergence_flag        | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:-----------------------------|:-------|:--------------------------|:--------------|------------:|-----------------:|------------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|:-----------------------|:--------|----------------:|:----------------------------|--------------------:|:-----------------------|:-------------------------|:---------------------|:-----------------|
| V009     | Time-series momentum (TSMOM) | Tier1  | A                         | All           |           5 |        0.874405  |  0.742196   |    1.00661  |     1        | 0.999976 |             1 |             1 |              1 |               0 | NA_ANALYTICAL          | V026    |        0.990748 | 0.9                         |         0.52459     | False                  | False                    | False                | False            |
| V026     | Residual momentum (FF5)      | Tier1  | A                         | Equities      |           2 |        0.694372  |  0.624074   |    0.76467  |     1        | 0.997988 |             2 |             2 |              3 |               1 | NA_ANALYTICAL          | V009    |        0.009252 | 0.7                         |         0.416681    | False                  | False                    | False                | False            |
| C001     | MVRV / NVRV oscillator       | Tier3  | Candidate (working paper) | Crypto        |           1 |        0.0928793 |  0.00669297 |    0.179066 |     0.982664 | 0.15956  |             4 |             3 |              6 |               3 | NA_ANALYTICAL          | C002    |        0.631784 |                             |         0.0558069   | N/A_NO_REGISTRY_SHARPE | False                    | False                | False            |
| C002     | NVT signal oscillator        | Tier3  | Candidate (working paper) | Crypto        |           1 |        0.0720772 | -0.0137758  |    0.15793  |     0.950064 | 0.089208 |             5 |             3 |              7 |               4 | NA_ANALYTICAL          | C001    |        0.368216 |                             |         0.0433218   | N/A_NO_REGISTRY_SHARPE | False                    | False                | True             |
| V014     | BTC exchange netflows        | Tier1  | A                         | Crypto        |           1 |        0         | -0.783986   |    0.783986 |     0.5      | 0.284692 |             6 |             3 |              7 |               4 | NA_ANALYTICAL          | V017    |        0.499936 |                             |         0.00041663  | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V010     | Revision breadth             | Tier1  | A                         | Equities      |           1 |        0         | -0.783986   |    0.783986 |     0.5      | 0.28408  |             6 |             3 |              7 |               4 | NA_ANALYTICAL          |         |        0.0156   |                             |         0.000102747 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V017     | BTC ETF net flows            | Tier1  | B                         | Crypto        |           1 |        0         | -0.489991   |    0.489991 |     0.5      | 0.184496 |             6 |             3 |              7 |               4 | NA_ANALYTICAL          | V014    |        0.500064 |                             |         0.000185545 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |

### R

| var_id   | name                       | tier   | grade   | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width | tau_posterior_median   | peers      |   p_beats_peers | registry_published_sharpe   |   post_decay_sharpe | divergence_flag        | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:---------------------------|:-------|:--------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|:-----------------------|:-----------|----------------:|:----------------------------|--------------------:|:-----------------------|:-------------------------|:---------------------|:-----------------|
| V027     | Intermediary capital ratio | Tier1  | A       | Cross-Asset   |           2 |         0.567553 |  0.476395  |    0.65871  |     1        | 1        |             1 |             1 |              1 |               0 | NA_ANALYTICAL          | V004       |        0.997008 | 0.6                         |         0.34058     | False                  | False                    | False                | False            |
| V018     | BTC 3m basis               | Tier1  | B       | Crypto        |           2 |         0.245874 |  0.0152049 |    0.476543 |     0.981653 | 0.796608 |             2 |             2 |              5 |               3 | NA_ANALYTICAL          | V015; V016 |        0.808516 |                             |         0.245575    | N/A_NO_REGISTRY_SHARPE | False                    | False                | False            |
| V002     | MOVE Index                 | Tier1  | A       | Cross-Asset   |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.218412 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V001       |        0.500356 |                             |         0.000539351 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V001     | VIX                        | Tier1  | A       | Cross-Asset   |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.217248 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V002       |        0.499644 |                             |        -0.000243878 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V015     | BTC realized vol           | Tier1  | A       | Crypto        |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.217196 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V016; V018 |        0.136564 |                             |         9.60608e-05 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V004     | HY OAS                     | Tier1  | A       | Cross-Asset   |           2 |         0        | -0.391993  |    0.391993 |     0.5      | 0.216472 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V027       |        0.002992 |                             |        -0.000256885 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V005     | NFCI                       | Tier1  | A       | Cross-Asset   |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.216448 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          |            |        0.002916 |                             |        -0.000100253 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V016     | BTC perp funding rate      | Tier1  | B       | Crypto        |           1 |         0        | -0.235196  |    0.235196 |     0.5      | 0.117616 |             5 |             3 |              8 |               5 | NA_ANALYTICAL          | V015; V018 |        0.05492  |                             |        -1.4637e-05  | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |

### Overlay

| var_id   | name   | tier   | grade   | asset_class   | n_studies   | posterior_mean   | ci95_low   | ci95_high   | p_positive   | p_top3   | median_rank   | rank_ci_low   | rank_ci_high   | rank_ci_width   | tau_posterior_median   | peers   | p_beats_peers   | registry_published_sharpe   | post_decay_sharpe   | divergence_flag   | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|----------|--------|--------|---------|---------------|-------------|------------------|------------|-------------|--------------|----------|---------------|---------------|----------------|-----------------|------------------------|---------|-----------------|-----------------------------|---------------------|-------------------|--------------------------|----------------------|------------------|


## Candidate pipeline

| name                                   | citation                                                   | score_component                  | peers                                           | posterior_summary                                                                              | verdict             |
|:---------------------------------------|:-----------------------------------------------------------|:---------------------------------|:------------------------------------------------|:-----------------------------------------------------------------------------------------------|:--------------------|
| V020 News sentiment                    | Tetlock (2007); Garcia (2013); Gu-Kurov (2020)             | C (registered)                   |                                                 | Not pooled; effect scale is event/text alpha, not long-short Sharpe scale.                     | WATCH               |
| V029 GEX (Gamma Exposure)              | Barbon-Buraschi (2021) + practitioner research             | Overlay (registered provisional) | dealer-hedging / short-horizon reversal filters | Not pooled; no Sharpe-gain extraction in Stage A.                                              | NEEDS_MORE_EVIDENCE |
| V030 Cross-asset lead-lag              | Lo-MacKinlay (1990); Asness-Moskowitz-Pedersen (2013)      | T (registered provisional)       | V009                                            | Not pooled; no clean Sharpe extraction in Stage A.                                             | WATCH               |
| V031 Correlation-regime signal quality | Kritzman et al. (2011)                                     | Overlay (registered provisional) | cross-asset crisis filters                      | Not pooled; no Sharpe-gain extraction in Stage A.                                              | WATCH               |
| V032 Decision tree feature importance  | Gu-Kelly-Xiu (2020)                                        | Overlay (registered ungraded)    | meta-variable                                   | Not pooled; meta-variable rather than standalone signal.                                       | NEEDS_MORE_EVIDENCE |
| V033 Calendar / seasonal               | Lucca-Moench (2015)                                        | C (registered ungraded)          |                                                 | Not pooled; event-study scale mismatch.                                                        | WATCH               |
| C002 NVT signal oscillator             | Yang & Fantazzini (2022) for admitted on-chain oscillators | T (inferred)                     | C001                                            | analytical posterior mean=0.072, 95% CI=(-0.014, 0.158), p_positive=0.950, p_beats_peers=0.368 | NEEDS_MORE_EVIDENCE |


## Primary report

### report.md

**Status:** analytical approximation; full MCMC required for production use.

Reason: the container could execute Python, but PyMC/NUTS could not compile because the environment is missing the Python development headers required for the backend build (`Python.h`). The full model code is provided in `model_{S,T,R,Overlay}.py` for rerun in a provisioned environment.

## 1. Marginal-contribution flags (LEAD)

Variables with `p_beats_peers < 0.40` are listed first; Tier 3 promotion candidates with `p_beats_peers > 0.80` follow.

- **S / V011 Brent M1-M3 curve slope** — `p_beats_peers=0.192` vs dominant peer `V028` → **demote/merge**.
- **S / V012 BTC active addresses** — `p_beats_peers=0.353` vs dominant peer `V013` → **demote/merge**.
- **S / V013 BTC hash rate** — `p_beats_peers=0.353` vs dominant peer `V012` → **demote/merge**.
- **S / V019 MVRV / SOPR** — `p_beats_peers=0.294` vs dominant peer `V012` → **demote/merge**.
- **T / V026 Residual momentum (FF5)** — `p_beats_peers=0.009` vs dominant peer `V009` → **demote/merge**.
- **T / C002 NVT signal oscillator** — `p_beats_peers=0.368` vs dominant peer `C001` → **demote/merge**.
- **R / V015 BTC realized vol** — `p_beats_peers=0.137` vs dominant peer `V016` → **demote/merge**.
- **R / V004 HY OAS** — `p_beats_peers=0.003` vs dominant peer `V027` → **demote/merge**.
- **R / V016 BTC perp funding rate** — `p_beats_peers=0.055` vs dominant peer `V015` → **demote/merge**.

## 2. Per-group ranking tables

### S

| var_id   | name                    | tier   | grade   | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width | tau_posterior_median   | peers      |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag        | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:------------------------|:-------|:--------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|:-----------------------|:-----------|----------------:|----------------------------:|--------------------:|:-----------------------|:-------------------------|:---------------------|:-----------------|
| V028     | Basis-momentum          | Tier1  | A       | Commodities   |           2 |         0.789866 |   0.701627 |    0.878105 |          1   | 0.9972   |             1 |             1 |              2 |               1 | NA_ANALYTICAL          | V011       |        0.807708 |                         0.8 |         0.473998    | False                  | False                    | False                | False            |
| V011     | Brent M1-M3 curve slope | Tier1  | A       | Commodities   |           3 |         0.715449 |   0.572649 |    0.858249 |          1   | 0.977472 |             2 |             1 |              3 |               2 | NA_ANALYTICAL          | V028       |        0.192292 |                       nan   |         0.715662    | N/A_NO_REGISTRY_SHARPE | False                    | False                | False            |
| V003     | DXY (Dollar Index)      | Tier1  | A       | Cross-Asset   |           2 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.159144 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V007       |        0.501148 |                       nan   |        -0.000322658 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V012     | BTC active addresses    | Tier1  | A       | Crypto        |           2 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.1587   |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V013; V019 |        0.353404 |                       nan   |         0.000238426 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V006     | UST 2Y/10Y yields       | Tier1  | A       | Rates         |           1 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.158624 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V008       |        0.499964 |                       nan   |        -0.00103982  | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V008     | ACM Term Premium 10Y    | Tier1  | A       | Rates         |           1 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.158388 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V006       |        0.500036 |                       nan   |         0.000746731 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V013     | BTC hash rate           | Tier1  | A       | Crypto        |           2 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.157904 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V012; V019 |        0.352532 |                       nan   |         0.000427494 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V007     | Real yield / breakevens | Tier1  | A       | Rates         |           1 |         0        |  -0.783986 |    0.783986 |          0.5 | 0.157688 |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V003       |        0.498852 |                       nan   |        -0.000579312 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V019     | MVRV / SOPR             | Tier1  | B       | Crypto        |           1 |         0        |  -0.489991 |    0.489991 |          0.5 | 0.07488  |             6 |             3 |              9 |               6 | NA_ANALYTICAL          | V012; V013 |        0.294064 |                       nan   |        -0.000139862 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |

### T

| var_id   | name                         | tier   | grade                     | asset_class   |   n_studies |   posterior_mean |    ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width | tau_posterior_median   | peers   |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag        | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:-----------------------------|:-------|:--------------------------|:--------------|------------:|-----------------:|------------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|:-----------------------|:--------|----------------:|----------------------------:|--------------------:|:-----------------------|:-------------------------|:---------------------|:-----------------|
| V009     | Time-series momentum (TSMOM) | Tier1  | A                         | All           |           5 |        0.874405  |  0.742196   |    1.00661  |     1        | 0.999976 |             1 |             1 |              1 |               0 | NA_ANALYTICAL          | V026    |        0.990748 |                         0.9 |         0.52459     | False                  | False                    | False                | False            |
| V026     | Residual momentum (FF5)      | Tier1  | A                         | Equities      |           2 |        0.694372  |  0.624074   |    0.76467  |     1        | 0.997988 |             2 |             2 |              3 |               1 | NA_ANALYTICAL          | V009    |        0.009252 |                         0.7 |         0.416681    | False                  | False                    | False                | False            |
| C001     | MVRV / NVRV oscillator       | Tier3  | Candidate (working paper) | Crypto        |           1 |        0.0928793 |  0.00669297 |    0.179066 |     0.982664 | 0.15956  |             4 |             3 |              6 |               3 | NA_ANALYTICAL          | C002    |        0.631784 |                       nan   |         0.0558069   | N/A_NO_REGISTRY_SHARPE | False                    | False                | False            |
| C002     | NVT signal oscillator        | Tier3  | Candidate (working paper) | Crypto        |           1 |        0.0720772 | -0.0137758  |    0.15793  |     0.950064 | 0.089208 |             5 |             3 |              7 |               4 | NA_ANALYTICAL          | C001    |        0.368216 |                       nan   |         0.0433218   | N/A_NO_REGISTRY_SHARPE | False                    | False                | True             |
| V014     | BTC exchange netflows        | Tier1  | A                         | Crypto        |           1 |        0         | -0.783986   |    0.783986 |     0.5      | 0.284692 |             6 |             3 |              7 |               4 | NA_ANALYTICAL          | V017    |        0.499936 |                       nan   |         0.00041663  | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V010     | Revision breadth             | Tier1  | A                         | Equities      |           1 |        0         | -0.783986   |    0.783986 |     0.5      | 0.28408  |             6 |             3 |              7 |               4 | NA_ANALYTICAL          | nan     |        0.0156   |                       nan   |         0.000102747 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |
| V017     | BTC ETF net flows            | Tier1  | B                         | Crypto        |           1 |        0         | -0.489991   |    0.489991 |     0.5      | 0.184496 |             6 |             3 |              7 |               4 | NA_ANALYTICAL          | V014    |        0.500064 |                       nan   |         0.000185545 | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |

### R

| var_id   | name                       | tier   | grade   | asset_class   |   n_studies |   posterior_mean |   ci95_low |   ci95_high |   p_positive |   p_top3 |   median_rank |   rank_ci_low |   rank_ci_high |   rank_ci_width | tau_posterior_median   | peers      |   p_beats_peers |   registry_published_sharpe |   post_decay_sharpe | divergence_flag        | indistinguishable_flag   | rank_unstable_flag   | low_power_flag   |
|:---------|:---------------------------|:-------|:--------|:--------------|------------:|-----------------:|-----------:|------------:|-------------:|---------:|--------------:|--------------:|---------------:|----------------:|:-----------------------|:-----------|----------------:|----------------------------:|--------------------:|:-----------------------|:-------------------------|:---------------------|:-----------------|
| V027     | Intermediary capital ratio | Tier1  | A       | Cross-Asset   |           2 |         0.567553 |  0.476395  |    0.65871  |     1        | 1        |             1 |             1 |              1 |               0 | NA_ANALYTICAL          | V004       |        0.997008 |                         0.6 |         0.34058     | False                  | False                    | False                | False            |
| V018     | BTC 3m basis               | Tier1  | B       | Crypto        |           2 |         0.245874 |  0.0152049 |    0.476543 |     0.981653 | 0.796608 |             2 |             2 |              5 |               3 | NA_ANALYTICAL          | V015; V016 |        0.808516 |                       nan   |         0.245575    | N/A_NO_REGISTRY_SHARPE | False                    | False                | False            |
| V002     | MOVE Index                 | Tier1  | A       | Cross-Asset   |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.218412 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V001       |        0.500356 |                       nan   |         0.000539351 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V001     | VIX                        | Tier1  | A       | Cross-Asset   |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.217248 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V002       |        0.499644 |                       nan   |        -0.000243878 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V015     | BTC realized vol           | Tier1  | A       | Crypto        |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.217196 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V016; V018 |        0.136564 |                       nan   |         9.60608e-05 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V004     | HY OAS                     | Tier1  | A       | Cross-Asset   |           2 |         0        | -0.391993  |    0.391993 |     0.5      | 0.216472 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | V027       |        0.002992 |                       nan   |        -0.000256885 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V005     | NFCI                       | Tier1  | A       | Cross-Asset   |           1 |         0        | -0.391993  |    0.391993 |     0.5      | 0.216448 |             5 |             2 |              8 |               6 | NA_ANALYTICAL          | nan        |        0.002916 |                       nan   |        -0.000100253 | N/A_NO_REGISTRY_SHARPE | True                     | True                 | False            |
| V016     | BTC perp funding rate      | Tier1  | B       | Crypto        |           1 |         0        | -0.235196  |    0.235196 |     0.5      | 0.117616 |             5 |             3 |              8 |               5 | NA_ANALYTICAL          | V015; V018 |        0.05492  |                       nan   |        -1.4637e-05  | N/A_NO_REGISTRY_SHARPE | True                     | False                | False            |

### Overlay

No eligible pooled nodes in this group.

## 3. Heterogeneity flags

All groups are analytical approximations under the simplifying assumption `alpha_a = tau_k = 0` for ranking numerics. `tau_k` posterior medians are therefore not production-estimated; heterogeneity flags are deferred pending full MCMC.

## 4. Registry divergence flags

No registry divergence flags were triggered on the current analytical approximation.

## 5. Grade-rank consistency

- **S / V003 DXY (Dollar Index)** — Grade A bottom 3.
- **S / V007 Real yield / breakevens** — Grade A bottom 3.
- **S / V012 BTC active addresses** — Grade A bottom 3.
- **T / V010 Revision breadth** — Grade A bottom 3.
- **T / V014 BTC exchange netflows** — Grade A bottom 3.
- **T / C001 MVRV / NVRV oscillator** — Tier 3 top 3.
- **R / V001 VIX** — Grade A bottom 3.
- **R / V002 MOVE Index** — Grade A bottom 3.
- **R / V004 HY OAS** — Grade A bottom 3.
- **R / V018 BTC 3m basis** — Grade B top 3.

## 6. Cross-group summary

Top 3 per group and overall top 5 by `p_top3` are shown below. Cross-group comparisons are **not on a common economic scale** and should be read only as within-group posterior ranking summaries.

### S top 3

| var_id   | name                    |   p_top3 |   p_beats_peers |
|:---------|:------------------------|---------:|----------------:|
| V028     | Basis-momentum          | 0.9972   |        0.807708 |
| V011     | Brent M1-M3 curve slope | 0.977472 |        0.192292 |
| V003     | DXY (Dollar Index)      | 0.159144 |        0.501148 |

### T top 3

| var_id   | name                         |   p_top3 |   p_beats_peers |
|:---------|:-----------------------------|---------:|----------------:|
| V009     | Time-series momentum (TSMOM) | 0.999976 |        0.990748 |
| V026     | Residual momentum (FF5)      | 0.997988 |        0.009252 |
| C001     | MVRV / NVRV oscillator       | 0.15956  |        0.631784 |

### R top 3

| var_id   | name                       |   p_top3 |   p_beats_peers |
|:---------|:---------------------------|---------:|----------------:|
| V027     | Intermediary capital ratio | 1        |        0.997008 |
| V018     | BTC 3m basis               | 0.796608 |        0.808516 |
| V002     | MOVE Index                 | 0.218412 |        0.500356 |

### Overall top 5 by p_top3

| group   | var_id   | name                         |   p_top3 |   p_beats_peers |
|:--------|:---------|:-----------------------------|---------:|----------------:|
| R       | V027     | Intermediary capital ratio   | 1        |        0.997008 |
| T       | V009     | Time-series momentum (TSMOM) | 0.999976 |        0.990748 |
| T       | V026     | Residual momentum (FF5)      | 0.997988 |        0.009252 |
| S       | V028     | Basis-momentum               | 0.9972   |        0.807708 |
| S       | V011     | Brent M1-M3 curve slope      | 0.977472 |        0.192292 |

## 7. Prior sensitivity

No variables moved by 3 or more median-rank slots under the uniformly looser prior.

## 8. Feed to 2026-10-14 audit

| var_id   | name                       | group   | go_no_go   | rationale                             |
|:---------|:---------------------------|:--------|:-----------|:--------------------------------------|
| V026     | Residual momentum (FF5)    | T       | NO-GO      | p_positive=1.000; p_beats_peers=0.009 |
| V027     | Intermediary capital ratio | R       | GO         | p_positive=1.000; p_beats_peers=0.997 |
| V028     | Basis-momentum             | S       | GO         | p_positive=1.000; p_beats_peers=0.808 |

## 9. Tier 3 graduation recommendations

| group   | var_id   | name                   |   p_positive |   p_beats_peers |
|:--------|:---------|:-----------------------|-------------:|----------------:|
| T       | C001     | MVRV / NVRV oscillator |     0.982664 |        0.631784 |

## 10. Memory-ready insights

- On the analytical posterior, V027 Intermediary capital ratio leads the R group and materially dominates its declared peer V004.
- V028 Basis-momentum leads the S group versus its static-slope peer V011 on the current pooled approximation.
- V009 TSMOM remains the dominant T-group node on the pooled scale; V026 Residual momentum stays positive but does not beat V009 on current peer comparison.
- Among admitted Tier 3 nodes, C001 MVRV / NVRV is directionally positive but still peer-contested; C002 NVT remains a low-power candidate.

