---
layout: default
title: Unfilled Market Concern Output (UMCO)
---
# Unfilled Market Concerns Output (UMCO)

Name origin: The data structure underlying Bitcoin transactions is called Unspent Transaction Output (UTXO), which resembles the process of pay - receive change - use change to pay. I feel market concerns has similar linked structure, emerging constantly from the news (similar to the creation of a transaction), and the market consumes these risk factors and leftovers penetrate for next few days' movement, thus I call it UMCO.

My motivation for this project: 1) to learn about what (opinion, opportunity) is currently being traded in the market, to construct market beliefs and 2) to explore how we can integrate textual information into time series modeling.

My ultimate ambition is to design a hypothesis generator, and automatically collect evidence to support or refute price drivers.

-------------
A design of three modules:
(1) Text aggregator: I scrape news from Nasdaq and Barchart(a commodities news vendor) to identify price drivers and generate a market briefing.
(2) Analytics Module: (To be Developed) A Hidden Markov Model. Input: price movement factors + historical prices -> Mid layer: A Gaussian-HMM of market sentiments(bearish, bullish etc.) -> Output: Price generation.
(3) Visualization Module: A visualization tool to attribute the underlying causes of price changes.

---
## Modules 

### 1. Market Daily Briefing

<div class="mermaid">
graph TD
    subgraph module1 [Module 1: Market Briefing]
        direction LR
        A[Text data: Commodity News from Barchart] --> B1[News Aggregator]
        B1 --> B2[Summary: price changes, price drivers, reversal warnings]    
        B2 --> C_OUT{Market Summary & Risk Factors}
    end
</div>

The key role of this module is to identify the support factors and risk factors influencing price movements. I envision a risk factor list, for example: `['weather', 'foreign exchange', 'trade tension', 'geopolitics', 'trend rebound']`.

**Example Input**:
 
```
    {
        "id": "32902280",
        "title": "Crude Prices Turn Lower as Iran Seeks to End Hostilities",
        "url": "https://www.barchart.com/story/news/32902280/crude-prices-turn-lower-as-iran-seeks-to-end-hostilities",
        "published_str_original": "Mon Jun 16, 2:22PM CDT",
        "published_timestamp_utc": 1750101720,
        "summary": "July WTI crude oil (CLN25 ) Monday closed down -1.21 (-1.66%), and July RBOB gasoline (RBN25 ) closed down -0.0077 (-0.35%). Crude oil prices surged by +5% initially on Sunday night as the Israel-Iran..."
    },
    {
        "id": "32902237",
        "title": "Hot US Temps Lift Nat-Gas Prices",
        "url": "https://www.barchart.com/story/news/32902237/hot-us-temps-lift-nat-gas-prices",
        "published_str_original": "Mon Jun 16, 2:21PM CDT",
        "published_timestamp_utc": 1750101660,
        "summary": "July Nymex natural gas (NGN25 ) on Monday closed up by +0.167 (+4.66%). July nat-gas prices on Monday rallied sharply as forecasts called for hotter temperatures in the eastern US, potentially boosting..."
    },

```

**Example Output**:
<div id="module4" style="width:100%; height:600px; border:1px solid #ccc; overflow:auto;">
  <iframe src="module4.html" width="100%" height="100%" frameborder="0">
    Your browser does not support iframes. Please <a href="module4.html">click here to view the content</a>.
  </iframe>
</div>

### 2. Analysis & Modeling

<div class="mermaid">
graph TD
subgraph module2 [Module 2: Data Fusion]
direction LR
A[Textual Data: Market Briefing]
B[Numerical Data: Price time series]
C[Time-varying Hidden Markov Machine]
A --> C
B --> C
C --> C_OUT{Inference / Forecasting}
end
</div>

- Naive idea: add external information to an AR model.
$$r_t = a_1r_{t-1} + b_1u_{t-1} + \epsilon_t$$, $u$ is the external information(e.g. sentiment score from text).

- Modest idea: Gaussian HMM.
Three hidden states: $S_t \in $ {Bullish, Bearish, and Neutral}.

Market return: $$r_t|S_t=i \sim N(\mu_i, \sigma_i^2)$$.

Transition probability from state $i$ to $j$ at time t: $P_{ij,t}$ based on textual information and historical price data.

A preliminary result for real Wheat futures:
![Combined Wheat Analysis]({{ site.baseurl }}/assets/images/combined_wheat_futures_results.png){: style="width: 80%; max-width: 700px;"}



- Fancy idea: Price attention on text embedding.

<!-- <div id="module2-container" style="width:100%; height:600px; border:1px solid #ccc; overflow:auto; margin-bottom:20px;">
  <iframe src="module2_showcase.html" width="100%" height="100%" frameborder="0">
    Your browser does not support iframes. Please <a href="module2_showcase.html">click here to view the content</a>.
  </iframe>
</div> -->

### 3. Visualization Module

A visualization of price movement attributors.
Excursion on causal inference and event study.

<div id="module3-container" style="width:100%; height:600px; border:1px solid #ccc; overflow:auto;">
  <iframe src="module3_showcase.html" width="100%" height="100%" frameborder="0">
    Your browser does not support iframes. Please <a href="module3_showcase.html">click here to view the content</a>.
  </iframe>
</div>

<!-- ## How to Run (Example)

1.  Clone the repository: `git clone https://github.com/your-username/UMCO.git`
2.  Navigate to the project directory: `cd UMCO`
3.  Install dependencies: `pip install -r requirements.txt`
4.  (Add more running instructions here...)

---

## Contributing

Contributions of all kinds are welcome! Please read `CONTRIBUTING.md` (if created) for more information. -->

---

<!-- ## License

This project is licensed under the [MIT License](LICENSE). -->