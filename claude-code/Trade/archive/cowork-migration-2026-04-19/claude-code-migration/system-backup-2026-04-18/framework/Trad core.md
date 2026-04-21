# Systematic review of multi-asset long/short signal generation

**The most robust trading signals across crypto, equities, commodities, and ETFs share a common trait: they combine momentum with regime awareness.** Time-series momentum (12-month lookback) delivers a diversified Sharpe ratio of ~1.0 across 58 futures markets and is the single most replicated finding in quantitative finance. Analyst earnings revision momentum is the strongest individual equity predictor, while MVRV Z-Score dominates crypto on-chain analytics, and carry (term structure) rivals momentum in commodity futures. Across every asset class examined, multi-factor composite scoring that blends technical, fundamental, sentiment, and macro signals—weighted dynamically by volatility regime—produces the most stable risk-adjusted returns and the lowest regime dependency. The current macro environment (April 2026: extreme fear, VIX in the high 20s, Fed Funds at ~3.25%, geopolitical disruption from the Iran conflict) favors contrarian mean-reversion entries over trend-following, with reduced position sizes and elevated gold allocation.

---

## Phase 1: the variables that actually predict asset returns

### Technical and price-based variables

Momentum dominates every asset class at horizons of one week to twelve months. The landmark Moskowitz, Ooi & Pedersen (2012) study documented statistically significant time-series momentum across all 58 liquid futures contracts tested, with **annualized Sharpe ratios near 1.0** for a diversified portfolio. Cross-sectional momentum (Jegadeesh & Titman, 1993) produces 55–89 basis points per month in winner-minus-loser equity portfolios, with the tech sector contributing disproportionately during bull markets. Critically, Daniel & Moskowitz (2016) showed that **volatility-scaled momentum approximately doubles the Sharpe ratio** of static implementations by reducing crash exposure.

Moving average crossovers represent the second-strongest technical signal category. For crypto, shorter periods (20/50 rather than 50/200) perform better given higher volatility. The 200-day moving average serves as the most robust single regime filter for SPY and QQQ—price above the 200-DMA with breadth confirmation (percentage of constituents above their own 200-DMA exceeding 50%) identifies sustained bull regimes with high reliability. Volume confirmation substantially improves crossover accuracy: high-volume crossovers showed **72% accuracy** in predicting sustained trends versus 54% for low-volume crossovers.

RSI performs best at shorter lookback periods for mean-reversion strategies. A 2-day RSI strategy on S&P 500 constituents (buy at RSI < 15, sell at RSI > 85) generates competitive returns while being invested only 42% of the time. For volatile tech stocks, RSI is less effective because these names trend more than they mean-revert. MACD and Bollinger Bands function primarily as confirmation tools rather than standalone signal generators—their standalone predictive power receives only Grade C evidence quality.

| Technical Variable | Best Asset Class | Optimal Lookback | Evidence Grade |
|---|---|---|---|
| Time-series momentum | All futures, crypto | 12-month lookback, 1-month hold | **A** |
| Cross-sectional momentum | Equities (especially tech) | 12-1 month (skip recent month) | **A** |
| 200-DMA regime filter | Equity indices (SPY, QQQ) | 200 days | **B+** |
| Short-period RSI (2–5 day) | Large-cap equities | 2–5 days, thresholds 15/85 | **B** |
| MA crossover (volume-confirmed) | Crypto, commodities | 20/50 (crypto), 50/200 (equities) | **B+** |
| Volume-price divergence | Crypto (monthly), equities | 1–4 weeks | **B−** |

### Fundamental and valuation variables across asset classes

**For equities**, analyst earnings revision momentum stands as the most persistent and highest-information-coefficient signal. Stocks in the top 20% of net upward revisions outperform the bottom 20% by **more than 16% annually**. Revision breadth (percentage of analysts revising up versus down) is more persistent than revision magnitude, and PGIM research found that price momentum becomes statistically insignificant once earnings revisions are controlled for, while revisions maintain significance even controlling for momentum. Post-earnings announcement drift has largely been arbitraged away in mega-cap tech stocks (Martineau 2022), though text-based PEAD using NLP on earnings call transcripts still generates **8.01% annual drift** (Philadelphia Fed, 2021). Price-to-sales is the most appropriate valuation lens for tech stocks because it works for unprofitable/high-growth companies and is less manipulable than earnings-based metrics.

**For crypto**, the MVRV Z-Score (Market Value to Realized Value) is the top on-chain predictor, having **identified every major cycle top within two weeks** historically. Key thresholds: MVRV above 3.7 signals overvaluation; below 1.0 signals undervaluation. Funding rates in perpetual futures rank as the most actionable short-term crypto signal—extreme positive funding (above 0.10% per 8-hour period) preceded 10–30% corrections during the 2021 bull market, while extreme negative funding signals capitulation bottoms. Exchange net outflows accelerating 40% preceded a 28% BTC rally in six weeks during October 2023. Random forest classifiers trained on whale wallet data achieve **68–73% accuracy** for predicting 24–72 hour directional moves.

**For commodities**, the carry signal derived from term structure (backwardation versus contango) is among the strongest predictors. Gorton, Hayashi & Rouwenhorst (2013) showed that roll yield contributed more to total commodity returns than spot price appreciation over 1959–2004. Koijen, Moskowitz, Pedersen & Vrugt (2018) documented carry strategy Sharpe ratios averaging **0.74** across asset classes. EIA weekly inventory surprises remain the top short-term crude oil signal, while China's manufacturing PMI is the single most important leading indicator for copper prices.

**For ETFs**, market breadth indicators—particularly the percentage of constituents above their 200-day moving average—provide the strongest regime signals. VIX term structure backwardation (front-month implied volatility exceeding back-month) is a statistically significant contrarian buy signal for SPY, with coefficients strengthening at longer horizons. Fund flow data has mixed predictive value; large retail inflows function as a contrarian indicator at extremes.

### Macro and cross-asset variables

The **US Dollar Index (DXY)** exerts the broadest cross-asset influence. BIS Working Paper 1083 confirms copper and tin exhibit the strongest inverse dollar correlation among all commodities. For BTC, the DXY has **21–27 times greater adverse influence** than gold price (Frontiers in Blockchain, 2025). Rising DXY signals overweight US domestic equities and underweight international/commodities/crypto; falling DXY reverses this signal.

**M2 money supply growth** shows the highest positive correlation and R-squared with BTC among all macro variables tested by Fidelity Digital Assets. Johansen cointegration tests reveal a long-run elasticity of **2.65**—a 1% increase in M2 associates with a 2.65% BTC price increase, with a typical lag of 60–70 days. Gold also cointegrates with M2 over 53 years (Synek, 2024), though the relationship operates at much longer horizons.

**Real yields (TIPS spreads)** historically showed an R-squared of 84% with gold prices from 2005–2021, but this relationship has experienced a **structural break since 2022**, with R-squared collapsing to 3–7%. Central bank buying and geopolitical hedging now dominate gold pricing. This is a critical example of regime-dependent variable reliability.

**Credit spreads (HY OAS)** serve as a leading risk barometer with 0.86 correlation to expected default frequency. Spread widening typically precedes equity drawdowns by weeks to months. The **yield curve** (2Y/10Y) has predicted 6 of 7 recessions since 1976 with a median 14-month lead, though the un-inversion (return to positive slope) provides a more immediate recession warning than the initial inversion.

| Macro Variable | Most Sensitive Assets | Evidence Grade |
|---|---|---|
| DXY strength/weakness | Copper, crypto, gold, EM equities | **A−** |
| M2 money supply growth | BTC (elasticity 2.65), gold | **A−** |
| Real yields (TIPS) | Gold (broken since 2022), tech/growth | **B+** (regime-dependent) |
| VIX term structure | SPY, QQQ (backwardation = buy) | **A−** |
| Credit spreads (HY OAS) | All risk assets (leading indicator) | **A−** |
| 2Y/10Y yield curve | Equities, cyclicals (recession timing) | **A** (recession prediction) |
| China manufacturing PMI | Copper, oil, EWY | **A** |
| Geopolitical risk index | Gold (+), oil (+), equities (−) | **A** |

### Sentiment and alternative data variables

**Gamma exposure (GEX)** has emerged as one of the most actionable sentiment signals. SpotGamma data shows **78% of days SPX closes inside their predicted range**. When GEX is positive, market makers hedge by buying dips and selling rallies, suppressing volatility and creating mean-reversion conditions. Negative GEX amplifies volatility and favors trend-following. This regime identification—mean-reverting versus trending—is arguably more valuable than directional prediction.

Twitter sentiment contains genuinely new information according to Gu & Kurov (2020), with a Bloomberg Twitter sentiment-based strategy earning an **annualized Sharpe of 3.17** before transaction costs. FinBERT achieves ~97% accuracy on financial phrase classification and represents the current state-of-the-art for sentiment NLP. However, signal decay is rapid—predictive power diminishes substantially after 24–48 hours for large caps. Reddit sentiment shows stronger signals for **abrupt volatility shifts** but explains negligible return variance during normal periods.

The CNN Fear & Greed Index Granger-causes returns on the S&P 500, Nasdaq Composite, and Russell 3000 according to Farrell & O'Connor (2024), and **outperforms VIX as a standalone equity return predictor**. Google Trends search volume predicts higher returns over 1–2 weeks with subsequent reversal (Da, Engelberg & Gao, 2011), functioning as an attention-driven buying signal.

### Inter-asset lead-lag relationships that survive scrutiny

The most robust lead-lag relationships provide genuine cross-asset alpha when monitored systematically. **BTC leads ETH** in market cycles by 1–5 days during trend changes; rising BTC dominance signals risk-off within crypto. **NVDA has become the bellwether** for the entire semiconductor and AI cycle—earnings and guidance cascade to AMD, TSMC, Samsung, and SK Hynix, directly impacting EWY. **Copper's year-over-year price change** correlates with ISM Manufacturing PMI and S&P 500 returns, earning its "Dr. Copper" reputation (Grade B+). The **Nikkei/KOSPI overnight session** provides directional bias for US equity opens during macro-driven risk events, as demonstrated by the August 2024 yen carry trade unwind that cascaded from a 12% Nikkei crash into US equities.

The **MOVE Index** (bond market volatility) generally lags VIX in normal conditions but **leads VIX during systemic stress**—in the March 2023 banking crisis, MOVE spiked several days before VIX responded. This makes MOVE a critical early-warning signal for multi-asset portfolio managers. The **gold/silver ratio** functions as a risk regime indicator: above 80 signals risk-off (recession fears depressing silver's industrial demand), below 60 signals risk-on.

---

## Phase 2: seven methodologies ranked by empirical robustness

### The definitive methodology comparison

| Methodology | Net Sharpe | Win Rate | Max DD | Best Assets | Worst Assets | Evidence |
|---|---|---|---|---|---|---|
| Trend following / TSMOM | 0.5–1.0 | 45–55% | −18% to −25% | Futures (all classes), crypto | Choppy/range-bound markets | **A** |
| Mean reversion / pairs | 0.8–1.35 | 55–65% | −10% to −25% | Same-sector equities, spreads | Trending macro, crypto | **B+** |
| Factor-based (multi-factor) | 0.6–0.8 | N/A | −30% to −50% | Developed market equities | Tech (value trap), EM | **A** |
| Machine learning | 0.5–1.5 (realistic) | 50–55% | −15% to −40% | US large-cap cross-section | Illiquid, crypto, FX | **B** |
| Regime detection | +0.1–0.3 (overlay) | N/A | Reduces DD 30–50% | Equity indices, multi-asset | Rapid regime changes | **B** |
| Event-driven | 0.5–1.0 | 55–60% | −15% to −30% | Small-cap (PEAD), FX (FOMC) | Large-cap (arbitraged away) | **B+** |
| Multi-factor composite | 0.6–1.0 | N/A | −15% to −25% | Equities, multi-asset | Concentrated sectors | **B+** |

### Trend following remains the gold standard

The Hurst, Ooi & Pedersen (2017) AQR study validated trend following across **137 years and 67 markets** with positive Sharpe ratios in every asset class and every decade. The SG CTA Trend Index delivered 0.61 Sharpe from 2000–2024 with positive skewness—providing "portfolio insurance" by performing best during extreme market moves (Fung & Hsieh, 2001). The 2022 calendar year was a standout: +27.3% return with Sharpe above 1.0, driven by energy, fixed income, and currency trends. Multi-horizon blending (combining short and long lookback periods) improves the Sharpe-to-max-drawdown ratio. The critical risk is **momentum crashes**, which Daniel & Moskowitz documented as forecastable via volatility state: the worst monthly loss was −88.5% in August 1932. Volatility scaling eliminates most of this tail risk.

### Machine learning: powerful but treacherous

The landmark Gu, Kelly & Xiu (2020) study in the Review of Financial Studies demonstrated that neural networks and gradient-boosted trees produce long-short decile strategies with **out-of-sample Sharpe ratios of 1.35 (value-weighted) to 2.45 (equal-weighted)**—roughly doubling linear model performance. However, the overfitting problem is severe: Bailey, López de Prado et al. (2015) found that in-sample Sharpe has **R-squared below 0.025** for predicting out-of-sample performance across 888 Quantopian strategies. Fischer & Krauss (2018) reported LSTM Sharpe of 5.8 before costs, but **excess returns disappeared entirely after 2010** once transaction costs were included. McLean & Pontiff (2015) showed anomaly returns decline **26% out-of-sample and 58% post-publication**. ML is best deployed as a signal enhancement layer atop established factors, not as a standalone signal generator. All ML models converge on the same dominant features: momentum variants, liquidity measures, and volatility.

### Multi-factor composite scoring delivers the most stable returns

MSCI's Adaptive Multi-Factor Allocation framework (macro, momentum, valuation, sentiment pillars) generated **2.73% active return** over MSCI World from 1986–2018 with the highest increment per unit of active risk. Equal-weight factor combinations are surprisingly competitive due to robustness against estimation error (DeMiguel, Garlappi & Uppal, 2009). Signal decay rates differ dramatically by type: momentum signals decay in days to weeks, fundamental signals in months to quarters, and sentiment signals at intermediate rates. Four to six signal categories maximize information content; beyond six to eight, diminishing returns set in. The MSCI framework uses a growth/inflation quadrant to determine which factors to overweight: momentum and growth outperform in "heating up" regimes, quality and low-volatility in slowdowns, and value in stagflation.

---

## Phase 3: asset-specific signal construction

### Bitcoin (BTC)

| Rank | Variable | Category | Optimal Lookback | Evidence |
|---|---|---|---|---|
| 1 | MVRV Z-Score | On-chain | Rolling (2-year baseline) | B+ |
| 2 | Global M2 growth | Macro | 60–70 day lag | A− |
| 3 | Funding rate extremes | Derivatives | 8-hour snapshots | B+ |
| 4 | 20/50-day MA crossover | Technical | 20/50 days | B+ |
| 5 | Exchange net flows + whale accumulation | On-chain | Weekly aggregation | B |

**Best methodology:** Multi-factor composite combining on-chain (MVRV, exchange flows), technical (MA crossovers, RSI), macro (M2, DXY), and derivatives (funding rates). Overlay with Markov-switching GARCH for regime detection. Combined momentum + mean reversion strategies delivered **Sharpe 1.71 with 56% annualized returns** in systematic backtests. **Worst methodology:** Pure RSI mean-reversion—crypto trends dominate at weekly-to-monthly horizons. Naive halving-cycle trading is diminishing in effectiveness with only four data points and increasing institutional pre-positioning. **Regime dependency:** Signals fail when BTC-equity correlation spikes during systemic deleveraging (March 2020, May 2022). DXY-M2 correlation regime shifts alter the macro signal channel unpredictably. **Long signal:** MVRV < 1.5 AND M2 accelerating AND funding rate negative or neutral AND price above 50-DMA. **Short signal:** MVRV > 3.5 AND funding rate extreme positive (> 0.10%/8hr) AND exchange inflows spiking AND price below 50-DMA.

### Ethereum (ETH)

| Rank | Variable | Category | Optimal Lookback | Evidence |
|---|---|---|---|---|
| 1 | ETH/BTC ratio | Relative value | 90-day trend | B |
| 2 | DeFi TVL + gas fees | Ecosystem | Weekly change | B |
| 3 | Funding rate extremes | Derivatives | 8-hour snapshots | B+ |
| 4 | MVRV (ETH-adapted) | On-chain | Rolling 2-year baseline | B |
| 5 | Social sentiment + Fear & Greed | Sentiment | 7-day rolling average | B+ |

ETH carries additional ecosystem-specific risk versus BTC: staking yield dynamics (~4–5% annually, with ~25–30% of supply locked), L2 adoption effects on gas fees (Dencun upgrade reduced L2 fees 90–95%), and competitive threats from Solana. BTC leads ETH in cycle transitions, making BTC signals a leading indicator for ETH positioning.

### Tech mega-caps (NVDA, AAPL, GOOGL, AMZN, META)

| Rank | Variable | Category | Optimal Lookback | Evidence |
|---|---|---|---|---|
| 1 | Analyst revision momentum (breadth) | Fundamental | Rolling 3-month | A |
| 2 | Cross-sectional price momentum | Technical | 12-1 month, vol-scaled | A |
| 3 | Earnings surprise (multi-quarter NLP) | Fundamental | 4 quarters | A− |
| 4 | P/S vs own history and peers | Valuation | 5-year z-score | B+ |
| 5 | Rate/VIX regime classification | Macro | Real-time | A− |

**Best methodology:** Multi-factor composite scoring weighting revisions (30%), momentum (25%), relative valuation (20%), earnings quality (15%), and insider activity (10%). Expected out-of-sample Sharpe: **0.8–1.2** after accounting for post-publication decay. Apply volatility scaling to manage momentum crash risk. Rebalance monthly with sector-neutral constraints. **Worst methodology:** Pure mean-reversion after earnings gaps—large-cap tech incorporates information efficiently, and gap-fill strategies fail. Value-based shorting of high-growth tech names is the classic "value trap." **Regime dependency:** Growth stocks have negative exposure to rising real yields. Momentum profits compress to **18 bps/month in high-sentiment** versus 71 bps/month in low-sentiment environments. When VIX exceeds 30, tech stock correlations spike and long/short alpha evaporates.

### Semiconductors (INTC, TSM, MU, WDC)

These cyclical names require additional sector-specific overlays. The **P/E ratio is counterintuitive for semiconductors**—it appears high at cycle troughs and low near peaks. Price-to-book is the better cycle positioning metric; P/B in the 8x range signals extreme overvaluation while 1.25–1.5x signals recession bottoms. SEMI equipment billings (year-over-year change) lead semiconductor stock performance by 3–6 months. DRAM and NAND spot pricing drives earnings volatility for MU and WDC. For TSM, advanced-node capacity utilization and Apple revenue concentration (~25%) are the primary risk factors. INTC's signal construction should account for its structural decline in competitive positioning—long signals require stronger fundamental confirmation than peers.

### Tesla (TSLA) and Palantir (PLTR)

Both names are sentiment-dominated with elevated retail participation. TSLA's quarterly delivery numbers versus consensus is the single most-watched metric. PLTR is driven by government contract announcements and commercial revenue growth acceleration. For both, momentum and social sentiment signals dominate fundamentals. Short interest was historically a significant factor for TSLA (short-squeeze dynamics) but has normalized. Position sizes should be reduced for both due to elevated idiosyncratic volatility; PLTR additionally carries wider bid-ask spreads (3–8 bps versus 1–3 bps for mega-caps).

### Crude oil (WTI/Brent)

| Rank | Variable | Category | Optimal Lookback | Evidence |
|---|---|---|---|---|
| 1 | EIA inventory surprise | Fundamental | Weekly | A |
| 2 | OPEC+ production decisions | Event-driven | Per meeting | A |
| 3 | Term structure (backwardation/contango) | Carry | Rolling front-month | A |
| 4 | DXY | Macro | Daily | A− |
| 5 | 12-month TSMOM signal | Technical | 12-month | A |

**Best methodology:** Trend following + carry + EIA event overlay. Expected Sharpe: **0.5–0.8**. The term structure signal is directly observable and model-free—long backwardated contracts, short contango. **Worst methodology:** Short-term mean reversion—oil trends persistently on geopolitical and OPEC catalysts. Standard MACD (12,26,9) without optimization consistently generates losses. **Long signal:** 12-month return positive AND backwardation in term structure AND EIA draws exceeding consensus AND DXY weakening. **Short signal:** 12-month return negative AND contango deepening AND EIA builds AND managed money net long at Z-score > 2.0.

### Gold (XAU)

| Rank | Variable | Category | Optimal Lookback | Evidence |
|---|---|---|---|---|
| 1 | Central bank buying trend | Fundamental | Quarterly (Q3 2025: ~980 tonnes) | A |
| 2 | DXY direction | Macro | Daily/weekly | A |
| 3 | 12-month TSMOM | Technical | 12-month | A |
| 4 | Real yields direction | Macro | Monthly (structural break warning) | B+ |
| 5 | Geopolitical risk index | Macro | Real-time | B |

The gold signal regime has fundamentally shifted since 2022. The formerly dominant real-yield relationship (R² = 84%) has collapsed to **3–7%** as central bank buying (led by China, India, and Turkey) and de-dollarization themes now drive pricing. MKS Pamp describes gold as showing "reduced sensitivity to real yields or the Dollar" in the current structural regime. This means historical backtests relying on the gold-TIPS relationship will substantially overstate signal reliability.

### Silver, copper, and platinum group metals

**Silver** is best traded as a derivative of gold using the gold/silver ratio for mean-reversion (historically oscillates between 60x and 80x) combined with gold's directional trend. Solar panel demand now accounts for over 10% of silver consumption, adding an industrial demand component.

**Copper** is the most macro-sensitive commodity. China PMI above 50 combined with declining LME inventories and a weakening DXY constitutes the highest-conviction long signal. Goldman Sachs projects copper surplus narrowing from ~500kt in 2025 to 160kt in 2026.

**Palladium and platinum** present significant liquidity challenges. Palladium's bid-ask spread can widen to **3–10% during volatile periods**, making it unsuitable for high-frequency strategies. Position sizes should not exceed 1–2% of average daily volume. Platinum's long-term thesis centers on hydrogen economy demand (projected 15% of total by 2030, 35% by 2040).

### ETFs (SPY, QQQ, EWJ, EWY)

| Rank | Variable | Best ETF(s) | Evidence |
|---|---|---|---|
| 1 | % constituents above 200-DMA | SPY, QQQ | A− |
| 2 | VIX term structure (backwardation = buy) | SPY, QQQ | A− |
| 3 | Dual momentum (12-month relative + absolute) | SPY vs EFA vs AGG | A− |
| 4 | USD/JPY direction and BOJ policy | EWJ (unhedged) | B+ |
| 5 | Semiconductor cycle indicators | EWY | B |

Antonacci's Global Equity Momentum produced **CAGR 17.43% with Sharpe 0.87 and max drawdown −22.72%** from 1974–2013, versus S&P 500 CAGR 10.5% with max drawdown −51%. However, Newfound Research identified **high sensitivity to lookback period specification**—diversifying across 10/11/12/13-month lookback windows reduces model specification risk. EWJ requires currency overlay awareness: DXJ (yen-hedged) returned 213% over five years versus EWJ's 39% during the persistent yen depreciation of 2020–2025. As BOJ tightens toward 0.75%+ and the Fed eases toward 3.00–3.25%, the narrowing yield differential forecasts yen appreciation, favoring unhedged EWJ.

---

## Phase 4: portfolio-level integration framework

### Cross-asset correlation structure and diversification

The correlation matrix reveals both diversification opportunities and hidden redundancies. BTC-S&P 500 correlation ranges from **0.15–0.35 in normal regimes** but spikes to 0.40–0.60 during stress—diversification benefits erode precisely when most needed. BTC-ETH correlation is persistently high at 0.75–0.85 (rising to 0.85–0.95 in stress), meaning these positions are largely redundant from a risk perspective. Stock-bond correlation has turned structurally positive since 2022, undermining traditional 60/40 diversification (BlackRock, 2025). Gold maintains the most reliable low/negative equity correlation during geopolitical stress. Commodities (ex-gold) show near-zero crypto correlation, offering genuine diversification.

**Signal diversification:** The most diversifying signal combinations are momentum + value (−0.5 to −0.6 correlation globally per Asness, Moskowitz & Pedersen, 2013) and momentum + mean-reversion (complementary across regimes). Regime detection overlays are synergistic with momentum, eliminating false signals in choppy markets. The most redundant combination is running multiple momentum variants across correlated assets—BTC momentum and ETH momentum signals will fire simultaneously ~80% of the time.

### Position sizing: inverse ATR with fractional Kelly overlay

**Inverse ATR volatility targeting** improves Sharpe ratios by **25–45%** across asset classes compared to naive fixed-percentage approaches. Position size = (Target Risk $) / (ATR × Multiplier), with multipliers of 2–3x ATR for trending assets (commodities, crypto) and 1.5–2x for equities.

The **Kelly criterion** maximizes geometric growth but requires accurate probability and payoff estimation. Full Kelly is excessively aggressive for real-world trading, producing 40–60%+ drawdowns. Practitioners should use **quarter-Kelly to half-Kelly** (Maclean et al., 2010). For the current elevated-VIX environment, quarter-Kelly with a 20–25% maximum position cap provides appropriate risk scaling. The multivariate Kelly extension requires covariance matrix estimation that introduces substantial estimation error—keep implementations simple.

### Risk management rules

- **Maximum portfolio heat:** 6–8% total portfolio risk at any time (sum of all position risks at stop-loss levels)
- **Individual position risk:** 0.5–2% of portfolio per position; reduce to 0.5% for illiquid names (PLTR, palladium, platinum)
- **Sector concentration:** Maximum 25% in any single sector; crypto capped at 5–15% of total portfolio
- **Correlation-based hedging pairs:** BTC/gold (partial hedge during risk-off), SPY/VIX derivatives, copper/EWY (high correlation enables hedge)
- **Stop-losses:** ATR-based trailing stops at 2–3x ATR reduce momentum strategy max drawdown from **−49.79% to −11.36%** (Han et al., 2016). Fixed-percentage stops underperform due to whipsaws
- **Drawdown circuit breaker:** At −15% portfolio drawdown, reduce exposure to 50%; at −20%, move to defensive positioning

### Rebalancing cadence and execution

Vanguard's 2022 research found no material outcome difference between monthly and annual rebalancing for buy-and-hold portfolios. For systematic signal-based portfolios, **hybrid threshold-based rebalancing** is optimal: monitor daily, rebalance when 5% absolute drift or signal change occurs. Crypto requires tighter 3% bands given higher volatility. Calendar-based monthly rebalancing works adequately for equities and commodities. The Daryanani study confirmed that "look constantly, trade rarely" (threshold-based) outperforms fixed-interval approaches.

**Slippage estimates for the universe:**

| Asset | Bid-Ask Spread | Slippage/Trade | Liquidity Grade |
|---|---|---|---|
| SPY, QQQ | $0.01 | < 1 bp | Excellent |
| AAPL, NVDA, GOOGL, AMZN, META | $0.01–0.03 | 1–3 bps | Excellent |
| TSLA, TSM, INTC, MU | $0.02–0.05 | 2–5 bps | Very good |
| WDC, PYPL, PLTR | $0.02–0.08 | 3–8 bps | Good |
| BTC (major exchanges) | 0.01–0.05% | 2–5 bps | Very good |
| ETH | 0.02–0.10% | 3–10 bps | Good |
| Gold futures (COMEX) | $0.10 | 1–2 bps | Excellent |
| WTI/Brent crude | $0.01/bbl | 1–2 bps | Excellent |
| Copper (COMEX) | Moderate | 2–5 bps | Good |
| Platinum | $0.50–2.00 | 5–15 bps | Moderate |
| Palladium | $0.50–2.00 | **5–15 bps** (3–10% in stress) | **Poor** |
| EWJ, EWY | $0.02–0.05 | 2–5 bps | Good |

---

## Phase 5: evidence quality and what to trust

### Variables graded A — peer-reviewed with out-of-sample replication

Time-series momentum across futures (Moskowitz et al., Hurst et al. with 137 years of data), cross-sectional equity momentum (Jegadeesh & Titman, replicated across 40+ countries), carry in commodity futures (Koijen et al.), yield curve recession prediction (6/7 recessions since 1976), geopolitical risk index impact on asset returns (Caldara & Iacoviello, Fed), DXY inverse commodity correlation (BIS Working Paper 1083), China PMI leading copper, OPEC decision impact on oil, profitability factor (RMW, most consistent Fama-French factor across all periods).

### Variables graded B — institutional white papers with robust backtests

MVRV Z-Score for crypto cycle timing, funding rate extremes, exchange net flows, analyst revision momentum for equities (extensively documented but primarily practitioner literature), VIX term structure signals (Fassas & Hourvouliades 2018), M2–BTC cointegration (Fidelity Digital Assets), Twitter/news sentiment (Gu & Kurov 2020), gamma exposure regime identification (SpotGamma), COT positioning for commodities (weakening post-financialization), seasonal patterns (declining effectiveness over time), Fear & Greed Index (Granger-causal but time-varying).

### Variables graded C — single study or insufficient validation

Hash rate as leading indicator for BTC (mostly coincident), Google Trends standalone (mixed replication results), stablecoin supply ratio, active address counts for crypto, dark pool activity signals, P/E ratio for semiconductor cycle timing (counterintuitive and unreliable), 13F filings for timing (excessive lag and data quality issues).

### Critical bias flags

**Survivorship bias** affects virtually all crypto studies—analyses use currently active coins, overstating historical strategy performance. **Look-ahead bias** is pervasive in ML research where feature engineering incorporates future information. McLean & Pontiff (2015) demonstrated portfolio returns decline **26% out-of-sample and 58% post-publication** across documented anomalies. The Quantopian study of 888 strategies found **in-sample Sharpe ratio has R² < 0.025** for predicting out-of-sample performance. All reported Sharpe ratios should be discounted 40–60% for realistic implementation expectations. The gold-TIPS relationship breakdown since 2022 illustrates how even Grade A historical relationships can experience structural breaks.

### Universally strong variables across all asset classes

Three signal categories show robust predictive power regardless of asset class: **(1) momentum/trend** (12-month lookback, volatility-scaled), **(2) carry/term structure** (directly observable, model-free), and **(3) DXY regime** (inverse relationship with nearly all non-USD-denominated assets). These should form the core of any multi-asset signal framework, with asset-specific variables added as complementary layers.

### Free versus paid data sources

| Data Type | Free Sources | Paid Sources |
|---|---|---|
| Price/volume | Yahoo Finance, FRED, Quandl (basic) | Bloomberg ($25K/yr), Refinitiv ($20K/yr) |
| On-chain crypto | Blockchain.com, Mempool.space | Glassnode ($40/mo+), CryptoQuant, CoinMetrics |
| COT/CFTC positioning | CFTC.gov (weekly) | Bloomberg (integrated), Barchart Plus |
| EIA inventory | EIA.gov (weekly) | Bloomberg (real-time) |
| Macro indicators | FRED, BLS, Census | Bloomberg, Macrobond |
| Sentiment/NLP | GDELT, StockTwits API, pytrends | RavenPack ($$$), Bloomberg Social |
| Options/GEX | CBOE delayed, OCC | SpotGamma, Unusual Whales |
| Factor data | Kenneth French library, AQR datasets | MSCI, FactSet |

---

## Adapting to the April 2026 regime

The current macro environment presents a specific configuration: **Fed Funds at ~3.25%** (paused after 50 bps of cuts in H2 2025), core PCE sticky around 2.5–3%, GDP growth expected at 1.8–2.6%, the Iran conflict disrupting energy markets with a fragile ceasefire, and the CNN Fear & Greed Index at **extreme fear (10–14)**—the lowest since the 2022 bear market bottom. The S&P 500 has declined approximately 9% from its January high near 7,000, with VIX sustained in the mid-to-high 20s.

This regime configuration suggests several signal weight adjustments. **Increase contrarian signal weight**: extreme fear readings have historically preceded above-average forward returns. **Reduce trend-following weight**: choppy, corrective markets reduce momentum strategy effectiveness and increase whipsaw risk. **Elevate GEX and volatility signals**: VIX in the high 20s typically corresponds to negative gamma, amplifying volatility and requiring tighter stops. **Overweight gold**: safe-haven demand is rising structurally, and gold shows reliably positive returns during geopolitical risk spikes (+1.6% weekly average during GPR spikes greater than 100%). **Reduce crypto allocation**: BTC-equity correlation elevates during stress, eliminating diversification benefits precisely when they're needed. **Reduce position sizes across the board**: use quarter-Kelly given elevated VIX, and let inverse ATR sizing naturally reduce exposure to volatile assets.

## Addendum — 2026-04-14 methodology audit additions

Three Grade A variables were added to the Top-25 monitor after an external audit against the peer-reviewed literature. Each is mechanism-grounded, replicated, and independent of signals already in the framework. Each carries McLean-Pontiff post-publication decay risk; expect 30–50% Sharpe haircut vs. published. Fail-loud rule applies.

### 26. Residual momentum (equity single-stock) — Grade A

**Concept.** 12-month trailing stock return residualized against the Fama-French 5-factor model (market, SMB, HML, RMW, CMA). Strips away factor-loading noise so the signal isolates idiosyncratic persistence rather than momentum-that-is-really-value or momentum-that-is-really-profitability.

**Primary citation.** Blitz, D., Huij, J., & Martens, M. (2011). *Residual Momentum.* Journal of Empirical Finance 18(3), 506–521.

**Replication.** Asness, C., Moskowitz, T., & Pedersen, L. (2013). *Value and Momentum Everywhere.* Journal of Finance 68(3), 929–985.

**Mechanism.** Raw 12m returns are contaminated by stable factor loadings (value, quality, size). For mega-cap tech specifically, value and momentum are often confounded. Residualization removes the contaminant. Information coefficient rises because noise falls; the signal also becomes orthogonal to fundamental mean-reversion.

**What it adds.** Independent of raw TSMOM (already Grade A) on single stocks where factor-loading contamination is largest. Orthogonal to earnings-revision breadth and ATH distance.

**Scope.** Single-stock equities only (NVDA, TSLA, AAPL, GOOGL, AMZN, META, TSM, INTC, MU, PYPL, PLTR, WDC). Not applied to indices/ETFs/commodities/FX/crypto, where raw TSMOM remains authoritative.

**Caveats.** (a) Requires monthly pull of Kenneth French factor returns; (b) crashes in correlation-1 regimes (Oct-2008, Mar-2020) — Daniel-Moskowitz (2016) volatility scaling is mandatory; (c) post-publication decay expected to bring Sharpe from ~1.0–1.4 down to ~0.6–0.9 live.

### 27. Intermediary capital ratio (cross-asset risk overlay) — Grade A

**Concept.** NY Fed primary-dealer equity-to-total-capital ratio, expressed as a z-score vs. 3-year rolling mean. Low ratio = constrained dealer balance sheets = contracted cross-asset risk-bearing capacity.

**Primary citation.** He, Z., Kelly, B., & Manela, A. (2017). *Intermediary Asset Pricing: New Evidence from Many Asset Classes.* Journal of Financial Economics 124(2), 264–279.

**Replication.** Adrian, T., Etula, E., & Muir, T. (2014). *Financial Intermediaries and the Cross-Section of Asset Returns.* Journal of Finance 69(6), 2557–2596 (broker-dealer leverage factor — complementary mechanism).

**Mechanism.** Dealer capital is the binding constraint on market-making across equities, Treasuries, corporate credit, FX, and commodity derivatives simultaneously. When dealer equity falls (losses, regulatory ratios tightening), liquidity provision contracts everywhere at once. This is the *cause* of the risk-off signals (widening HY OAS, rising MOVE) that the existing framework observes ex post.

**What it adds.** Leads HY OAS by ~1–2 weeks in published tests. Complementary to VIX and MOVE, which are price measures of realized/implied stress; this is the capacity-side input.

**Caveats.** (a) Post-2008 correlation with HY OAS is 0.65–0.75 — do not double-count; take the more negative of the two; (b) regime break around Dodd-Frank 2012, so use z-score not level; (c) weekly NY Fed primary-dealer release has ~1-week lag; (d) post-decay Sharpe projected 0.4–0.7 (structural signal, low adoption friction, but limited alpha capacity).

### 28. Basis-momentum (commodity structural input) — Grade A

**Concept.** 4-week and 12-week change in the front-month-to-deferred futures slope. Captures the *acceleration* of the term-structure shape — whether backwardation is intensifying or flattening, contango steepening or easing.

**Primary citation.** Boons, M., & Prado, M. P. (2019). *Basis-Momentum.* Journal of Finance 74(1), 239–279.

**Replication.** Szymanowska, M., de Roon, F., Nijman, T., & van den Goorbergh, R. (2014). *An Anatomy of Commodity Futures Risk Premia.* Journal of Finance 69(1), 453–482.

**Mechanism.** Captures hedging-pressure dynamics and intermediary constraint cycles in commodity futures. When speculators lose risk-bearing capacity, demand for carry (long backwardation, short contango) steepens the curve further; when capacity returns, the curve mean-reverts. Published Sharpe ~1.2–1.5 across 23 commodities; economically significant nearby returns ~18% annualized.

**What it adds.** Pure carry (F1–F2 static slope, Grade A, already in framework) is static; basis-momentum is its derivative. Orthogonal to EIA inventory changes. For Brent specifically — Gerald's #1 watched regime variable — basis-momentum answers "is the backwardation intensifying (add) or exhausting (reduce)?" that F1–F2 alone cannot.

**Caveats.** (a) Weakest in near-zero-funding regimes (2020–2021 COVID) — mechanism depends on intermediary/hedging imbalance; (b) strongest in financialized commodities (WTI, Brent, gold, silver); weaker in metals with strong physical convenience (copper, platinum); (c) most recent publication among the three additions, so highest decay uncertainty — post-decay Sharpe projected 0.6–1.0.

## Conclusion

The most important insight from this systematic review is not which individual variable ranks highest for a given asset—it is that **no single signal survives across all regimes**, and the margin between robust and overfitted signals is razor-thin. The three cross-asset universals that come closest to regime-independence are volatility-scaled momentum, carry, and dollar regime. Every other variable requires regime awareness to avoid catastrophic failure: the gold-TIPS relationship broke in 2022, PEAD vanished for large-caps after 2001, pairs trading profitability has declined continuously since 1989, and ML strategies lose 58% of returns post-publication.

The practical implication is clear: **build signal systems that are modular and regime-adaptive rather than monolithic and optimized.** A multi-factor composite using four to six signal categories with equal or simple information-coefficient weighting, overlaid with a three-state regime detection model (bull/bear/high-volatility), and implemented with inverse-ATR position sizing and fractional Kelly risk budgeting, will outperform any single-methodology approach over a full market cycle. The expected realistic Sharpe ratio for such a system across this multi-asset universe, after transaction costs, post-publication decay, and slippage, is **0.7–1.2**—well above the SG CTA Trend Index's long-run 0.61 but below the seductive 2.0+ numbers that populate academic backtests and rarely survive contact with live markets.