# Portfolio Performance Analyzer & Backtester

An interactive web application built with Streamlit for analyzing the historical performance of stock portfolios against a benchmark.

## Features

- **Portfolio Performance Analysis**: Analyze how your custom stock portfolio would have performed historically
- **Benchmark Comparison**: Compare your portfolio performance against a market benchmark (e.g., SPY)
- **Key Metrics Calculation**: View important performance metrics like:
  - Total & Annualized Returns
  - Volatility
  - Sharpe & Sortino Ratios
  - Maximum Drawdown
- **Interactive Visualizations**:
  - Portfolio Asset Allocation
  - Investment Growth Over Time

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application with:

```bash
python run.py
```

Then follow the instructions in the web interface:
1. Enter your portfolio tickers and weights in the sidebar
2. Set your backtest parameters (start/end date, benchmark, etc.)
3. Click "Run Analysis" to view the results

## Project Structure

- `src/` - Contains the main application code
- `data/` - Directory for any data files
- `utils/` - Utility functions and helpers

## Dependencies

- streamlit - Web application framework
- pandas - Data analysis
- numpy - Numerical computing
- yfinance - Yahoo Finance data retrieval
- plotly - Interactive visualizations 