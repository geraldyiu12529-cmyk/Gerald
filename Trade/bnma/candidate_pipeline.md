# Stage F — Candidate Pipeline

Merged: Provisional/Ungraded registry rows + Catalyst variables + low-power/failed Tier 3 candidates.

| Var_ID | Name | Citation | SC | Peers | Post. Mean | Post. SD | P(>0) | Verdict |
|--------|------|----------|----|-------|-----------|---------|-------|--------|
| V030 | Cross-asset lead-lag | Lo-MacKinlay (1990) RFS | T | V009 | N/A | N/A | N/A | WATCH |
| V029 | GEX | Barbon-Buraschi (2021) | Overlay |  | N/A | N/A | N/A | WATCH |
| V031 | Correlation-regime signal quality | Kritzman et al. (2011) FAJ | Overlay |  | N/A | N/A | N/A | WATCH |
| V032 | Decision tree feature importance | Gu-Kelly-Xiu (2020) RFS | Overlay |  | N/A | N/A | N/A | NEEDS_MORE_EVIDENCE |
| V033 | Calendar/seasonal | Lucca-Moench (2015) JF | C |  | N/A | N/A | N/A | NEEDS_MORE_EVIDENCE |
| V020 | News sentiment | Tetlock (2007) JF; Garcia (2013) | C (event-study) |  | N/A (excluded) | N/A | N/A | WATCH |
| C012 | Price-to-sales (tech) | Barbee et al. (1996) FAJ; Lakonishok-Shleifer-Vishny (1994) JF | S | V003 | 0.0221 | 0.096 | 0.5949 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C001 | Global M2 money supply | M2-Bitcoin Elasticity cointegration (2025 WP, Preprints.org) | S | V012,V013 | 0.0055 | 0.048 | 0.546 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C004 | NVT Signal (90d) | Ferretti-Santoro (2022) NVML variant | S | V019,V012 | 0.0037 | 0.0487 | 0.5401 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C006 | China PMI leading copper | Trad core Grade A; Caixin/NBS PMI academic literature | S | V003 | 0.0027 | 0.0873 | 0.5114 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C003 | Gold/silver ratio | Mittal-Mittal (2025) SSRN; practitioner research | S | V003,V007 | 0.0004 | 0.0484 | 0.5019 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C008 | Fear & Greed Index | Farrell-O'Connor (2024) | T | none | 0.007 | 0.0489 | 0.5551 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C010 | Short-period RSI (2-5d) | Connors-Alvarez (2009); practitioner literature | T | V009 | 0.0052 | 0.0485 | 0.541 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C011 | Whale accumulation ratio | ML classifiers 68-73% accuracy (practitioner) | T | V014,V017 | -0.0024 | 0.0495 | 0.4816 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C009 | Token unlock pressure | Practitioner (16,000+ events studied) | T | V014 | -0.0065 | 0.0496 | 0.4481 | LOW_POWER_CANDIDATE — NEEDS_MORE_EVIDENCE |
| C005 | 200-DMA regime filter | Faber (2007) JWIM; extensive replication literature | Overlay | none | 0.0087 | 0.0478 | 0.5796 | WATCH — fails p_beats_peers vs registry peers |
| C002 | VIX term structure slope | Fassas-Hourvouliades (2018); Macrosynergy (2024) | Overlay | none | 0.0075 | 0.0489 | 0.5604 | WATCH — fails p_beats_peers vs registry peers |
| C007 | Market breadth (pct >200-DMA) | Practitioner + breadth literature | Overlay | none | -0.0005 | 0.0247 | 0.4895 | WATCH — fails p_beats_peers vs registry peers |
