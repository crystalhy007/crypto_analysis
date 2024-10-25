# Crypto Futures Funding Rate Analysis

## Overview

This project analyzes cryptocurrency futures funding rates using data from the Gate.io API. The initiative began when a friend reached out, requesting an automated list of futures prices to assist with investment decisions. This request sparked my interest to dive deeper into crypto analysis, aiming to not only provide timely information but also explore patterns, trends, and relationships within the data.

The main goals are to automate data extraction, perform comprehensive analyses, and develop insights that can inform better trading and investment strategies in the crypto futures market.
## Project Goals

- **Extract** funding rate data for various cryptocurrency contracts from the Gate.io API.
- **Transform** and clean the data for analysis, including timestamp conversion and rate normalization.
- **Analyze** funding rates over different time windows (1 day, 2 days, 3 days).
- **Visualize** the results to identify patterns and insights across different contracts.

## Data Source

The data for this project is sourced from the Gate.io API:

- **Tickers List Endpoint:** `/futures/usdt/tickers`
- **Funding Rate Endpoint:** `/futures/usdt/funding_rate`

## Tools and Technologies

- **Python** for data extraction, transformation, and analysis.
- **Pandas** for data manipulation.
- **NumPy** for numerical computations.
- **Requests** for API interaction.

## Key Steps

1. **API Data Extraction:**
    - The script initiates API requests to fetch the list of USDT futures contracts and funding rates.
    - The data is limited to a sample of the first 5 contracts for demonstration purposes.

2. **Data Transformation:**
    - The raw data is cleaned by converting timestamps to readable datetime formats.
    - Funding rates are normalized and converted to percentages for easier interpretation.

3. **Analysis:**
    - The data is grouped into three time windows:
        - **1 Day:** Represents the first third of the total data.
        - **2 Days:** Represents the first two-thirds of the total data.
        - **3 Days:** Represents the full three-day dataset.
    - Average funding rates are calculated for each time window.


## Results

The final output is a merged DataFrame containing average funding rates over three different time windows for each contract. This analysis provides insights into how funding rates vary over time and across contracts.

## Next Steps

- **Expand the Analysis:** Include more contracts or increase the time window for deeper insights.
- **Visualize Trends:** Use visualization libraries like Matplotlib or Seaborn to create graphical representations of the data.
- **Automate Data Retrieval:** Implement a scheduling mechanism to automate data extraction at regular intervals.


## Acknowledgments

- **Gate.io API** for providing the data.



