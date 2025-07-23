---
layout: default
title: News Momentum and Price Momentum
---
# News Momentum and Price Momentum

<!-- Name origin: The data structure underlying Bitcoin transactions is called Unspent Transaction Output (UTXO), which resembles the process of pay - receive change - use change to pay. I feel market concerns has similar linked structure, emerging constantly from the news (similar to the creation of a transaction), and the market consumes these risk factors and leftovers penetrate for next few days' movement, thus I call it UMCO. -->

> **Abstract**: This study examines the relationship between price momentum and news narratives in commodity futures markets. By extracting price drivers from financial news, we developed a novel "theme score" to create a news-enhanced momentum strategy. An empirical test on crude oil futures shows our news-enhanced momentum strategy outperforms traditional momentum and buy-and-hold approaches. Our findings confirm the efficacy of incorporating news narratives in improving trading performance.

Motivation for this project: 1) to learn about what (opinion, opportunity) is currently being traded in the market, to construct market beliefs and 2) to explore how we can integrate textual information into time series modeling.

My ultimate ambition is to design a hypothesis generator, and automatically collect evidence to support or refute price drivers.

-------------
Modules:
(1) Text aggregator: I scrape news from Barchart(a commodities news vendor) to identify price drivers and generate a market briefing.
(2) Analytics Module: I construct a measure termed **theme scores** for each theme, and report theme score along with a trend-following strategy based on theme scores.


## Modules 

### 1. Market Daily Briefing


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
| Date | Commodity | Key Drivers | Reverse Factors |
|------|-----------|-------------|-----------------|
| 2022-01-03 | Crude Oil | OPEC+ surplus cut (supply) | Market volatility (markets); Natural gas decline (markets) |
| 2022-01-04 | Crude Oil | Omicron demand optimism (demand) | OPEC+ meeting outcome (supply) |
| 2022-01-05 | Crude Oil | OPEC+ hike doubts (supply) | OPEC+ compliance potential (supply) |
| 2022-01-06 | Crude Oil | Tight supplies (supply) | |
| 2022-01-07 | Crude Oil | Omicron demand concerns (demand); Travel restrictions (demand) | Demand improvement potential (demand) |

**Briefing Visualization**:
<div id="report" style="width:100%; height:600px; border:1px solid #ccc; overflow:auto;">
  <iframe src="reports/20250722_report.html" width="100%" height="100%" frameborder="0">
    Your browser does not support iframes. Please <a href="reports/20250722_report.html">click here to view the content</a>.
  </iframe>
</div>

### 2. Analysis & Modeling

<figure>
  <img src="assets/images/CompFlow.jpg" alt="Modeling Framework">
  <figcaption>Figure 1: Computational Flow. This diagram illustrates our model's computational process for a three-theme market (Demand, Supply, and Weather). A filter window of size 4 processes the theme-specific information increment time-series. Activated theme is colored in orange and inactive theme is in white. A theme score is calculated for each theme after the filtering process. The next return is sampled from a mixture model of previous theme scores.</figcaption>
</figure>

Themes and Theme scores.
<div id="themescore" style="width:100%; height:600px; border:1px solid #ccc; overflow:auto;">
  <iframe src="interactive_report.html" width="100%" height="100%" frameborder="0">
    Your browser does not support iframes. Please <a href="interactive_report.html">click here to view the content</a>.
  </iframe>
</div>


---

## Contributing

Contributions of all kinds are welcome! Please read `CONTRIBUTING.md` (if created) for more information. -->

---

<!-- ## License

This project is licensed under the [MIT License](LICENSE). -->