---
layout: default
title: Unfilled Market Concern Output (UMCO)
---
# Unfilled Market Concerns Output (UMCO)

The data structure underlying Bitcoin transactions is called Unspent Transaction Output (UTXO), which resembles the process of receiving and giving change. I have named this project "Unfilled Market Concerns Output" (UMCO) because concerns emerge constantly from the news (similar to the creation of a transaction), and the market consumes these risk factors and subsequently makes "changes" (information ferment for next few days' movement).

My motivation for this project: 1) to learn about what is currently being traded in the market and 2) to explore how we can enhance time series prediction with textual information.

I have designed three modules:
(1) Textual Information Handler: I scrape news from Nasdaq and Barchart to identify price drivers and generate a market briefing.
(2) Data Fusion and Analytics Module: (To be Developed) A Hidden Markov Model is a candidate for this module.
(3) Visualization Module: A visualization tool to attribute the underlying causes of price changes.

---

## Project Workflow

<div class="mermaid">
graph TD
    subgraph module1 [Module 1: Market Briefing]
        direction LR
        A[Text data: Commodity News from Nasdaq] --> B1[News Aggregator]
        B1 --> B2[Summary: price changes, price drivers, reversal warnings]    
        B2 --> C_OUT{Market Summary & Risk Factors}
    end
  
    %% Styling %%
    style A fill:#f9f,stroke:#333,stroke-width:2px
</div>

---

## Modules Explained

### 1. Market Daily Briefing

The key role of this module is to identify the support factors and risk factors influencing price movements. I envision a risk factor list, for example: `['weather', 'foreign exchange', 'trade tension', 'geopolitics', 'trend rebound']`.

**Example Input**:
 
```
{
        "title": "Stocks Post Modest Gains as Bond Yields Fall and Chip Stocks Rally",
        "url": "https://www.nasdaq.com/articles/stocks-post-modest-gains-bond-yields-fall-and-chip-stocks-rally",
        "time_published": "Thu, 06/05/2025 — 11:42",
        "summary": "The S&P 500 Index ($SPX ) (SPY ) Wednesday closed up +0.01%, the Dow Jones Industrials Index ($DOWI ) (DIA ) closed down -0.22%, and the Nasdaq 100 Index ($IUXX ) (QQQ ) closed up +0.27%.  June E-mini S&P futures (ESM25 ) are down -0.02%, and June E-mini Nasdaq futures..."
    },
    {
        "title": "Corn Rebounds on Wednesday",
        "url": "https://www.nasdaq.com/articles/corn-rebounds-wednesday",
        "time_published": "Thu, 06/05/2025 — 10:32",
        "summary": "Corn futures posted Wednesday gains of fractionally to 5 1/4 cents, as July continues to be on the selling side of the bear spreading. The front month CmdtyView national average Cash Corn price was up 1/4 cent at $4.14 1/4.  EIA data from this morning showed the weekly ethanol production..."
    },
    {
        "title": "Corn Rebounding on the Midweek Session",
        "url": "https://www.nasdaq.com/articles/corn-rebounding-midweek-session",
        "time_published": "Thu, 06/05/2025 — 10:23",
        "summary": "Corn futures are trading with contracts 3 to 6 cents higher on Wednesday. The front month CmdtyView national average Cash Corn price is up 3 3/4 cents at $4.17 1/2.  EIA data from this morning showed the weekly ethanol production exploding to match the mid-March high at 1.105 million barrels..."
    }
...
```

**Example Output**:
```
{Coffee (Arabica & Robusta Futures)

- Change: July arabica coffee increased by +1.55%, and July ICE robusta coffee rose by +0.83%.
- Price Drivers: A rally in the Brazilian real against the U.S. dollar triggered short covering in coffee futures, pushing prices upward.
- Potential Risk Factors: The rally is closely linked to currency movements (specifically the Brazilian real) and technical short covering, which may not provide sustained long-term support.
}
```
### 2. Analysis & Modeling

Naive idea: add external information to an AR model.

Example: Gaussian HMM.
Three hidden states: \(S_t \in \){Bullish, Bearish, and Neutral}.
Market return: \(r_t|S_t=i \sim N(\mu_i, \sigma_i^2)\)
Transition probability from state \(i\) to \(j\) at time t: \(P_{ij,t}= f(\text{embedding(text info)} \oplus \text{embedding(price info)} )\)

<div class="mermaid">
graph TD
subgraph module2 [Module 2: Data Fusion]
direction LR
A[Textual Data: Market Briefing]
B[Numerical Data: Price time series]
C[Time-varying Hidden Markov Model]
A --> C
B --> C
C --> C_OUT{Inference / Forecasting}
end
</div>

<!-- <div id="module2-container" style="width:100%; height:600px; border:1px solid #ccc; overflow:auto; margin-bottom:20px;">
  <iframe src="module2_showcase.html" width="100%" height="100%" frameborder="0">
    Your browser does not support iframes. Please <a href="module2_showcase.html">click here to view the content</a>.
  </iframe>
</div> -->

### 3. Visualization Module

An example:

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