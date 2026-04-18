# Systematic review framework for crypto altcoin selection and long/short decisions

**The most effective approach to selecting altcoins and deciding long/short positions combines on-chain valuation metrics (MVRV, NVT), cross-sectional factor models (market, size, momentum), regime-aware risk management, and machine learning ensembles — with risk-managed momentum and statistical arbitrage delivering the highest risk-adjusted returns (Sharpe ratios of 1.42–2.45) across market conditions.** This synthesis draws on 30+ recent academic papers (2022–2026), multiple systematic reviews, and institutional research frameworks to identify which variables, methodologies, and decision frameworks have demonstrated genuine predictive power versus those that are noise. The resulting framework below serves as both a research compendium and a ready-to-use systematic review protocol.

---

## On-chain and tokenomics variables with demonstrated predictive power

The strongest empirically validated on-chain metric is the **MVRV ratio** (Market Value to Realized Value). When MVRV exceeds 3.7, it signals overvaluation; below 1.0 indicates undervaluation. The MVRV Z-Score variant has historically identified cycle tops within two weeks. Its primary limitation is data density — it works reliably for Bitcoin and Ethereum but degrades for illiquid altcoins.

The **NVT Signal** (90-day smoothed Network Value to Transactions) outperforms raw NVT as a trading oscillator. Ferretti & Santoro (2022) found that a Metcalfe's Law variant (NVML) achieved a profit-to-max-drawdown ratio of **2.3** with only 4% capital drawdown. Active address counts feed into Metcalfe's Law models where price scales with n² of active users — mature cryptocurrencies show strong correlation with this relationship.

Exchange flow data provides actionable short-term signals. Sustained net outflows from exchanges precede price appreciation: a 40% acceleration in Bitcoin exchange outflows over 14 days preceded a 28% rally within six weeks in October 2023. ML models trained on whale transaction data achieve **68–73% accuracy** predicting 24–72 hour directional moves, though individual whale alerts have poor signal-to-noise ratios. The Bitcoin Whale Ratio above 85% precedes major corrections; below 70% accompanies accumulation.

Token unlock events are remarkably predictive: analysis of **16,000+ unlock events** shows approximately 90% create negative price pressure regardless of size or recipient category. Prices typically decline in the month preceding unlocks, with the sharpest movements in the final week, stabilizing roughly 14 days post-unlock. The sole positive exception is ecosystem development unlocks, which average +1.18% price impact.

For macro variables, **global M2 money supply** exhibits a correlation coefficient of **0.78** with Bitcoin price at a 60–90 day lag (Sarkar 2025, Fidelity Digital Assets). The DXY dollar index exerts 21–27× greater adverse influence on Bitcoin than gold does. A critical altcoin-specific finding: altcoins follow U.S. liquidity while Bitcoin follows global liquidity — rising M2 combined with falling BTC dominance historically precedes altcoin rallies.

Social sentiment metrics show conditional predictive power. Twitter sentiment achieves ~62.5% prediction accuracy when combined with historical price data. Models integrating TikTok and Twitter sentiment improved crypto return forecasts by up to 20%, with TikTok alone improving short-term Dogecoin predictions by 35%. The **Fear & Greed Index** below 10 has delivered an average 90-day return of +48% with zero negative instances historically — though the sample size is fewer than 10 readings since 2018.

---

## Quantitative methodologies ranked by evidence strength

**Momentum strategies** are the most extensively validated approach. Liu, Tsyvinski & Wu (2022) in the *Journal of Finance* established that market, size, and momentum capture cross-sectional cryptocurrency returns. Time-series momentum with a 28-day lookback and 5-day holding period achieves a **Sharpe ratio of 1.51** versus the market's 0.84 (Han et al.). Risk-managed momentum using Barroso & Santa-Clara volatility scaling improves the annualized Sharpe from 1.12 to **1.42** — notably, the improvement in crypto comes from augmented returns rather than downside mitigation, because crypto markets lack the extended momentum crashes seen in equities. Stop-loss momentum (Sadaqat & Butt 2023, 147 cryptocurrencies) achieves the highest returns and alpha versus all benchmarks while conventional momentum produces a negative Sharpe of −0.235 due to crash risk.

**Statistical arbitrage and pairs trading** deliver strong risk-adjusted returns, particularly at higher frequencies. Cointegration-based BTC-ETH pairs trading achieves a **Sharpe ratio of 2.45** with 16.34% annualized returns and only 8.45% volatility (IJSRA 2026). The critical frequency finding: 5-minute pairs trading returns **11.61% monthly** versus −0.07% at daily frequency — mean reversion is fundamentally an intraday phenomenon in crypto.

**The crypto carry trade** (short perpetual futures, long spot) produced the highest reported Sharpe of **6.45** from 2020–2025 (Borri et al. 2025), but this has declined to 4.06 from 2024 and turned negative in 2025 as funding rates compress with institutional entry. BIS Working Paper 1087 documents carry sometimes exceeding 40% annualized, driven by smaller traders seeking leveraged exposure.

**Factor models** adapted for crypto follow the Liu-Tsyvinski-Wu three-factor framework (Market, Size, Momentum). CF Benchmarks extended this to seven factors adding Value (Fees/TVL, DAU/Market Cap), Growth, Downside Beta, and Liquidity — all showing significant risk premia. A critical finding from the *North American Journal of Economics and Finance* (2026): only **2–3 factors** are needed to eliminate significant portfolio alphas, with turnover volatility, bid-ask spread, and new-address-to-price ratio as the most influential. Liquidity variables dominate.

**Machine learning** shows promise but demands caution. LSTM networks achieve out-of-sample Sharpe ratios of **3.23** (Jaquart et al. 2022), though accuracy is only 52.9–54.1% overall, rising to 57.5–59.5% on the top 10% confidence predictions. Gradient Boosting and XGBoost consistently outperform deep learning with **R² ≈ 0.98** across multiple coins (Adedigba et al. 2025). A sobering counterpoint: Discover Artificial Intelligence (2025) found that naïve models sometimes outperform complex ML/DL, suggesting crypto time series have substantial Brownian noise properties. The strongest ML implementation pattern combines XGBoost for feature selection with LSTM or Transformer models for prediction, using information-driven sampling (volume bars, dollar bars) and Triple Barrier labeling rather than fixed time bars.

---

## Long/short decision frameworks and signal construction

The most reliable technical indicator framework combines three dimensions: trend (MACD), momentum (RSI), and volatility (Bollinger Bands). RSI alone achieves ~65.6% buy-signal accuracy; combined with Bollinger Bands, accuracy rises to **87.5%**. A combined RSI + MACD strategy backtested on Bitcoin achieved a **77% win rate**. For crypto specifically, RSI thresholds should be adjusted to >80 overbought and <20 oversold to account for higher momentum persistence. RSI divergence (price making new highs while RSI declines) is more reliable than absolute threshold crossings.

**Funding rates** serve as contrarian sentiment indicators rather than standalone predictors. Rates exceeding 0.05% per hour indicate excessive leverage; above 0.1% per 8-hour settlement signals overheated markets. Funding rate arbitrage (delta-neutral spot long + perpetual short) consistently offers superior risk-adjusted returns compared to holding strategies and exhibits **no correlation** with directional strategies, providing genuine diversification (ScienceDirect 2024).

**Regime detection** dramatically improves signal quality. Hidden Markov Models with 3–4 states (bull/bear/sideways/turbulent) are the standard approach. Koki et al. (2022) found that a 4-state Non-Homogeneous HMM using series momentum, VIX, and US Treasury Yield as predictors achieved the best forecasting for BTC, ETH, and Ripple. A hybrid K-Means + HMM approach outperformed standalone HMMs. The practical application: bull regimes favor long-biased momentum; bear regimes favor short bias or market-neutral pairs trading; sideways regimes favor mean reversion with reduced position sizes.

**Composite signal scoring** follows a framework where each indicator contributes +1 or −1 to a net conviction score. Entry triggers when the composite exceeds a threshold (e.g., 7+ out of 10 for bullish). Multi-timeframe confirmation across 1-hour, 4-hour, and daily dramatically improves win rates. An AI signal bot study reported TP1 hit rates of 60.6% overall, rising to **86%** during high-volatility regimes.

For **relative value analysis**, altcoins exhibit higher beta to Bitcoin — high-beta altcoins outperform during risk-on periods and underperform more severely during risk-off. The CTREND factor (Fieberg et al. 2023/2025, *Journal of Financial and Quantitative Analysis*) aggregates price and volume information across horizons into a single factor with "remarkably stable" long-short performance, even when classical momentum disappoints post-2017.

---

## Risk management: position sizing, portfolio construction, and tail risk

**Quarter Kelly** is the professional consensus for crypto position sizing. Full Kelly generates drawdowns exceeding 50% even with positive edge; half Kelly captures ~75% of maximum growth with dramatically reduced variance; quarter Kelly means a 30% Bitcoin drop translates to only 7.5% portfolio impact. ATR-based position sizing (risk per trade ÷ ATR × multiplier) maintains consistent risk exposure across assets with varying volatility. Fixed fractional risk of 1–2% per trade provides survivable equity curves — backtesting shows 2% produces manageable ~25% maximum drawdown while 5% yields the best returns (+239%) but with −61.5% drawdown.

For **portfolio construction**, Hierarchical Risk Parity (HRP) outperforms mean-variance optimization for crypto. Standard Markowitz fails because crypto returns are non-normal with heavy tails and extreme kurtosis. Burggraf et al. (2020) demonstrated HRP's superior tail-risk-adjusted returns. The Stanford approach (Johansson & Boyd 2024) proposes dynamic dilution with cash to achieve target risk — a crypto portfolio applying 10% annualized volatility limits holds approximately **90% cash** due to crypto's extreme volatility. Grayscale Monte Carlo simulations suggest ~5% total portfolio allocation to crypto optimizes Sharpe for traditional balanced portfolios.

**Stop-loss methodology** should use ATR-based stops: stop-loss at 2× ATR from entry, TP1 at 1.5× ATR, TP2 at 3× ATR. When TP1 hits, move stop to breakeven. With a 60%+ TP1 hit rate, expected value is +0.8R per trade. Chandelier exits (3× ATR trailing below highest high) are well-suited for crypto trend-following.

For **tail risk**, GARCH models show crypto volatility persistence (β) typically exceeds 0.7, with some assets near 0.9 — volatility shocks have much longer-lasting effects than in equities. EGARCH works best for Ethereum (captures leverage effect), TGARCH for Bitcoin (asymmetric shocks), and CGARCH for altcoins with distinct short/long-term volatility components. CVaR with regime-adaptive calibration is preferred over VaR because VaR underestimates tail risk in fat-tailed distributions. The SVCJ model (Stochastic Volatility with Correlated Jumps) provides Basel-compliant risk measurement for crypto.

---

## Systematic review methodology: PRISMA adaptation and bias mitigation

Five published systematic reviews provide templates for crypto trading research. Fang et al. (2022, *Financial Innovation*) covered 146 papers; Almeida & Gonçalves (2023, *J. Behavioral and Experimental Finance*) used full PRISMA protocol reducing 3,744 articles to 166 through structured screening; Peng et al. (2024, *China Accounting and Finance Review*) searched Scopus, Web of Science, and EBSCOhost with explicit PRISMA flow diagrams (563 → 88 final articles).

**Database selection** should include Scopus (broadest coverage), Web of Science (highest quality indexing), IEEE Xplore (algorithmic/ML papers), SSRN and arXiv (critical grey literature for reducing publication bias), and Google Scholar as supplementary. **Inclusion criteria** should require: peer-reviewed or high-quality preprint, English language, empirical with quantitative results, defined performance metrics, and out-of-sample testing. **Exclusion criteria**: no methodology description, purely theoretical without validation, conference abstracts only, blockchain technology without trading application.

A custom **quality scoring rubric** (0–20 scale) should assess eight dimensions: data quality (0–3), out-of-sample testing (0–3), transaction cost inclusion (0–2), benchmark comparison (0–2), statistical rigor (0–3), robustness checks (0–3), reproducibility (0–2), and overfitting controls (0–2). Studies scoring 16+ are high quality; 10–15 moderate; below 10 low.

**Critical biases** to assess in every included study:

- **Survivorship bias**: ~75% of crypto assets over a 10-year window delist; inflates annual returns by 1–4%. Borri et al. (2025) is notable for including 29,230 inactive coins
- **Overfitting**: Use Probability of Backtest Overfitting (PBO), Deflated Sharpe Ratio (DSR), and walk-forward validation. Short crypto history makes this especially dangerous
- **Transaction cost neglect**: Momentum portfolios have ~85% weekly turnover; alphas fall 26–53% after realistic costs of 15+ bps per trade
- **Look-ahead bias**: On-chain data providers like Glassnode revise Bitcoin data within ~2 hours; signals must account for publication delays
- **Publication bias**: Detect with funnel plots (minimum 10 studies) and Egger's regression test; mitigate by including SSRN/arXiv preprints

For **meta-analysis**, use random-effects models given expected high heterogeneity (I² likely >75%). Standardize effect sizes to annualized Sharpe ratio as the primary metric. Meta-regression should examine moderators including asset type, time period, strategy class, ML usage, and transaction cost inclusion.

---

## Performance across market regimes: what works when

| Strategy | Bull Markets | Bear Markets | Sideways | Best Sharpe Reported |
|---|---|---|---|---|
| Risk-managed momentum | Very strong | Return augmentation helps | Good | 1.42 |
| Stop-loss momentum | Equally effective | Equally effective | Equally effective | Highest alpha vs. benchmarks |
| Stat arb (BTC-ETH cointegration) | Positive | Positive (market-neutral) | Best environment | 2.45 |
| Crypto carry trade | Exceptional | Good | Good | 6.45 (declining to negative) |
| CTREND factor | Stable | Stable post-2017 | Stable | >1.0 |
| LSTM ensemble | Captures uptrends | Mixed/uncertain | Limited evidence | 3.23 (OOS) |
| Sentiment-based | Strongest alignment | Weaker signals | Noise-dominated | Variable |
| Plain momentum | Strong (3%+ weekly) | Crash-prone (negative Sharpe) | Moderate | 1.12 |

The crypto carry trade's decline from Sharpe 6.45 to negative in 2025 illustrates **market maturation eroding alpha** — institutional participation compresses the very inefficiencies that systematic strategies exploit. Cross-sectional anomalies persist in illiquid segments precisely because they are hard to trade. Factor anomalies are weakening for large-cap cryptos post-2024.

---

## Synthesized prompt for conducting the systematic review

The following prompt integrates all findings into a structured protocol that can be used to conduct a rigorous systematic review:

---

> **SYSTEMATIC REVIEW PROTOCOL: Crypto Altcoin Selection and Long/Short Decision-Making**
>
> **Objective:** Conduct a PRISMA 2020-compliant systematic review and meta-analysis of quantitative strategies for cryptocurrency altcoin selection and long/short positioning, covering on-chain analytics, factor models, machine learning, sentiment analysis, and risk management frameworks.
>
> **Registration:** Register protocol on OSF (Open Science Framework) before beginning. Use PRISMA-P 17-item checklist for protocol documentation.
>
> **Research Questions:**
> 1. Which variables and indicators demonstrate statistically significant predictive power for altcoin returns across different time horizons?
> 2. Which quantitative methodologies (momentum, mean-reversion, factor models, ML/DL, sentiment analysis) produce the highest risk-adjusted returns after transaction costs?
> 3. What composite signal frameworks and regime detection approaches improve long/short decision accuracy?
> 4. How do strategy performance metrics vary across bull, bear, and sideways market regimes?
> 5. What risk management frameworks (position sizing, portfolio construction, stop-loss, tail risk) are most effective for crypto altcoin portfolios?
>
> **Database Search Strategy:**
> - Primary databases: Scopus, Web of Science, IEEE Xplore
> - Grey literature: SSRN, arXiv (q-fin and cs.LG sections), NBER Working Papers
> - Supplementary: Google Scholar, ScienceDirect, ACM Digital Library
> - Industry sources: Glassnode Research, Coinbase Institutional, Binance Research, CF Benchmarks, CoinMetrics
> - Citation chaining: Backward and forward from all included studies
>
> **Search String (adapt per database):**
> ("cryptocurrency" OR "crypto" OR "altcoin" OR "digital asset" OR "Bitcoin" OR "Ethereum" OR "DeFi") AND ("trading strategy" OR "algorithmic trading" OR "systematic trading" OR "factor model" OR "momentum" OR "mean reversion" OR "machine learning" OR "deep learning" OR "on-chain" OR "sentiment analysis" OR "portfolio construction" OR "long short") AND ("performance" OR "return" OR "Sharpe ratio" OR "backtest" OR "prediction" OR "profitability" OR "alpha")
>
> **Inclusion Criteria:**
> - Peer-reviewed journal articles, high-quality conference proceedings (ACM, IEEE, NeurIPS), or substantive preprints (SSRN, arXiv) with rigorous methodology
> - Published January 2018 – April 2026
> - English language
> - Empirical studies with quantitative results reporting at least one performance metric (Sharpe ratio, annualized return, maximum drawdown, accuracy, alpha, information ratio)
> - Studies addressing cryptocurrency trading strategies, altcoin selection, price prediction, or portfolio construction
> - Must include out-of-sample, walk-forward, or live trading validation
>
> **Exclusion Criteria:**
> - Purely theoretical without empirical validation
> - Conference abstracts, posters, book chapters, editorials
> - Studies focused solely on blockchain technology without financial trading application
> - Studies reporting only in-sample results without any out-of-sample testing
> - Studies without clear methodology description sufficient for replication
> - Duplicate publications (retain most complete version)
>
> **Variable Categories to Extract:**
>
> *A. On-Chain Metrics:* MVRV ratio and Z-Score, NVT Signal (90-day smoothed), SOPR, active addresses, transaction volume, exchange inflows/outflows, whale ratio, realized cap, NUPL, supply distribution by age (HODL Waves), Metcalfe's Law variants
>
> *B. Tokenomics:* Circulating/total/max supply ratios, inflation rate, token burn rates, vesting schedule and unlock events (timing, size relative to circulating supply, recipient category), staking yield, token velocity, emissions schedule
>
> *C. Developer & Ecosystem:* GitHub commit frequency and developer count (Electric Capital methodology), TVL (Total Value Locked), protocol upgrade events, smart contract deployments, ecosystem growth rate
>
> *D. Social Sentiment:* Twitter/X sentiment scores (VADER, RoBERTa, CryptoBERT, FinBERT), Reddit activity and sentiment, weighted social sentiment (Santiment), social dominance, Fear & Greed Index, Google Trends, TikTok sentiment (emerging)
>
> *E. Market Microstructure:* Funding rates (perpetual futures), open interest, liquidation data, long/short ratio, order book depth, bid-ask spread, taker buy/sell volume ratio
>
> *F. Macro/Cross-Asset:* BTC dominance, M2 money supply (with 60-90 day lag), DXY, S&P 500/NASDAQ correlation, VIX, US Treasury yields, gold price, risk-on/risk-off regime indicators
>
> *G. Factor Model Variables:* Market beta, size (market cap), momentum (1-4 week lookback), value proxies (Fees/TVL, DAU/Market Cap, coin-to-token ratio), liquidity (bid-ask spread, dollar volume, Roll's measure), volatility (realized vol, skewness), downside beta, growth, turnover volatility, new-address-to-price ratio
>
> *H. Technical Indicators:* RSI (14-period, crypto-adjusted thresholds >80/<20), MACD (12/26/9), Bollinger Bands (20-period, 2σ), Volume Profile (VPVR), OBV, Ichimoku Cloud, ATR, moving average crossovers (10-30 day optimal for crypto)
>
> **Methodologies to Categorize:**
> 1. Momentum strategies: time-series, cross-sectional, risk-managed, stop-loss, volume-weighted, CTREND
> 2. Mean-reversion: cointegration-based pairs trading, Ornstein-Uhlenbeck calibration, Z-score signals
> 3. Factor models: Fama-French adapted (3-factor, 7-factor), Fama-MacBeth regressions, IPCA
> 4. Machine learning: Random Forest, XGBoost/LightGBM, LSTM/GRU, Transformer/TFT, CNN-LSTM hybrids, Reinforcement Learning (DQN, PPO, A2C)
> 5. Network analysis: Graph-based blockchain analysis, topological data analysis (Betti derivatives), wallet clustering
> 6. NLP sentiment: VADER, BERT/RoBERTa/CryptoBERT, zero-shot classifiers (BART MNLI), LLM-based (GPT-4)
> 7. Regime detection: Hidden Markov Models (3-4 state), Markov-Switching GARCH, K-Means + HMM hybrids
> 8. Carry/arbitrage: Funding rate arbitrage, cash-and-carry basis trading, cross-exchange arbitrage
> 9. Composite/ensemble: Multi-indicator scoring, multi-model ensembles, regime-aware signal combination
>
> **Risk Management Frameworks to Assess:**
> - Position sizing: Kelly criterion (full, half, quarter), fixed fractional (1-2%), ATR-based volatility-adjusted
> - Portfolio construction: Mean-variance, Risk Parity, Hierarchical Risk Parity (HRP), Black-Litterman, dynamic cash dilution (Stanford approach), maximum diversification
> - Stop-loss: Fixed percentage, ATR-based (2× ATR), chandelier exits, time-based, breakeven trailing
> - Volatility models: GARCH(1,1), EGARCH, TGARCH, CGARCH, IGARCH, Stochastic Volatility, EWMA
> - Tail risk: VaR (historical simulation, GARCH-based), CVaR/Expected Shortfall, EVT (GPD), SVCJ, regime-adaptive calibration
> - Drawdown: Maximum drawdown limits (15-25%), CDaR, progressive de-risking, portfolio-level risk budgeting
>
> **Data Extraction Form Fields:**
> Study ID | Authors/Year/Journal | Asset(s) studied | Time period | Data frequency | Data source | Strategy type | Methodology | In-sample period | Out-of-sample period | Walk-forward (Y/N) | Transaction costs included (Y/N, amount) | Performance metrics (Sharpe, return, max drawdown, alpha, accuracy, win rate) | Benchmark(s) | Statistical tests reported | Overfitting controls (PBO, DSR, cross-validation) | Market regime tested (bull/bear/sideways) | Code/data availability | Quality score (0-20)
>
> **Quality Assessment Rubric (0-20):**
> - Data quality (0-3): 0=no description; 1=source stated; 2=cleaned with description; 3=point-in-time, survivorship-free
> - Out-of-sample testing (0-3): 0=none; 1=simple split; 2=walk-forward; 3=multiple OOS periods or live trading
> - Transaction costs (0-2): 0=ignored; 1=fixed costs; 2=realistic costs with slippage
> - Benchmark comparison (0-2): 0=none; 1=buy-and-hold; 2=multiple benchmarks including risk-free
> - Statistical rigor (0-3): 0=none; 1=basic metrics; 2=significance tests; 3=multiple testing corrections
> - Robustness checks (0-3): 0=none; 1=parameter sensitivity; 2=different assets/periods; 3=Monte Carlo + stress tests
> - Reproducibility (0-2): 0=not reproducible; 1=methodology described; 2=code/data available
> - Overfitting controls (0-2): 0=none; 1=acknowledged; 2=formal tests (PBO, deflated Sharpe)
>
> **Bias Assessment (evaluate for every included study):**
> - Survivorship bias: Does the study include delisted assets? Universe definition methodology?
> - Look-ahead bias: Point-in-time data? Signal publication delay accounted for?
> - Overfitting: Number of parameters vs. observations? Multiple testing corrections? PBO/DSR reported?
> - Selection bias: Time period selection justified? Multiple regimes tested?
> - Transaction cost realism: Fees, slippage, market impact, funding rates included?
> - Publication bias: Assess at review level with funnel plots + Egger's test (minimum 10 studies)
>
> **Meta-Analysis Specification:**
> - Primary effect size: Annualized Sharpe ratio (standardized)
> - Secondary: Annualized return, maximum drawdown, alpha relative to benchmark
> - Model: Random-effects (REML estimation) given expected high heterogeneity
> - Heterogeneity: Report Q statistic, I², τ², and prediction intervals
> - Moderators for meta-regression: Strategy type, asset class (BTC-only vs. altcoins vs. cross-section), time period (pre/post-2020), ML usage (Y/N), transaction cost inclusion (Y/N), market regime, data frequency, quality score
> - Subgroup analyses: By methodology category, by market regime, by quality score tier
> - Publication bias: Funnel plots, Egger's regression test, trim-and-fill adjustment
> - Sensitivity: Leave-one-out analysis, influence diagnostics
>
> **Synthesis Structure:**
> 1. PRISMA flow diagram with identification, screening, eligibility, and inclusion counts
> 2. Descriptive statistics of included studies (by year, methodology, asset class, quality)
> 3. Narrative synthesis by methodology category
> 4. Forest plots comparing risk-adjusted returns by strategy type
> 5. Meta-regression identifying moderators of strategy performance
> 6. Regime-conditional performance analysis (bull vs. bear vs. sideways)
> 7. Risk management framework comparison
> 8. Quality-weighted evidence summary
> 9. Summary of Findings table (adapted GRADE)
> 10. Research gaps and future directions
>
> **Key Reference Papers to Anchor the Review:**
> - Liu, Tsyvinski & Wu (2022), "Common Risk Factors in Cryptocurrency," *Journal of Finance* — foundational three-factor model
> - Borri, Liu, Tsyvinski & Wu (2025), "Cryptocurrency as an Investable Asset Class" — 10 stylized facts, carry trade analysis
> - Fang et al. (2022), "Cryptocurrency Trading: A Comprehensive Survey," *Financial Innovation* — 146-paper survey
> - Jaquart et al. (2022), "Short-term bitcoin market prediction via machine learning," *Journal of Finance and Data Science* — LSTM benchmark
> - Fieberg et al. (2023/2025), CTREND factor, *Journal of Financial and Quantitative Analysis*
> - Han et al. (2024), Time-series and cross-sectional momentum analysis
> - Burggraf et al. (2020), HRP for crypto portfolios, *ScienceDirect*
> - Giudici & Abu Hashish (2020), HMM regime detection, *Quality and Reliability Engineering International*
> - Bailey & López de Prado (2014), Deflated Sharpe Ratio framework
> - Gort et al. (2022), DRL overfitting detection, NeurIPS ICAIF

---

## Conclusion: what the evidence actually shows

Three findings stand out from this synthesis. First, **simplicity often wins** — a parsimonious 2–3 factor model (turnover volatility, bid-ask spread, new-address-to-price ratio) eliminates significant portfolio alphas, and naïve models sometimes outperform complex deep learning architectures. This suggests crypto markets retain substantial random-walk properties that sophisticated models mistake for learnable patterns. Second, **regime awareness is the single highest-leverage improvement** across all strategy types — stop-loss momentum works equally well in all regimes, while plain momentum's Sharpe swings from strongly positive to deeply negative depending on market conditions. Implementing a 3–4 state HMM as a meta-strategy layer transforms most underlying strategies from fragile to robust. Third, **market maturation is rapidly eroding alpha** — the crypto carry trade collapsed from Sharpe 6.45 to negative in five years, momentum turnover costs consume 26–53% of gross alpha, and cross-sectional anomalies survive only in illiquid segments that cannot absorb meaningful capital. Any systematic review conducted using this framework should explicitly track the time-decay of strategy effectiveness and distinguish between strategies that exploit fundamental economic mechanisms (network value, liquidity provision) versus those that exploit temporary market inefficiencies that institutional capital is systematically compressing.