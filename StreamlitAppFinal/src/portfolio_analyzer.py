import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# --- Set page config first ---
st.set_page_config(
    page_title="Portfolio Analyzer", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI with dark theme
st.markdown("""
<style>
    body {
        color: #FFFFFF;
        background-color: #121212;
    }
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        font-weight: 700;
        color: #90CAF9;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #E0E0E0;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 0.15rem 0.3rem rgba(0,0,0,0.3);
        color: #FFFFFF;
    }
    .positive {
        color: #4CAF50;
    }
    .negative {
        color: #F44336;
    }
    .info-text {
        font-size: 0.9rem;
        color: #BDBDBD;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 5px 15px;
        background-color: #333333;
        color: #E0E0E0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2196F3;
        color: white;
    }
    /* Override Streamlit's default theme */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #121212;
    }
    .sidebar .sidebar-content {
        background-color: #1E1E1E;
    }
    .stTextInput>div>div>input {
        background-color: #333333;
        color: white;
    }
    .stDataFrame {
        background-color: #1E1E1E;
    }
    .dataframe {
        background-color: #1E1E1E;
        color: white;
    }
    th {
        background-color: #2C2C2C;
        color: white !important;
    }
    tr {
        background-color: #1E1E1E;
        color: white !important;
    }
    .stSelectbox>div>div>div {
        background-color: #333333;
        color: white;
    }
    div[data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #2196F3, #1E1E1E);
    }
    .stMarkdown {
        color: #FFFFFF;
    }
    .streamlit-expanderHeader {
        color: #FFFFFF;
        background-color: #1E1E1E;
    }
    div[role="radiogroup"] label {
        color: #FFFFFF !important;
    }
    div[data-testid="stToolbar"] {
        background-color: #1E1E1E;
    }
    label[data-baseweb="checkbox"] {
        color: #FFFFFF;
    }
    button[kind="primary"] {
        background-color: #2196F3;
    }
    .stAlert {
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---

@st.cache_data(ttl=3600) # Cache data for 1 hour
def fetch_data(tickers: list[str], start_date: str, end_date: str) -> tuple[pd.DataFrame | None, list[str]]:
    """Fetches adjusted closing prices for a list of tickers."""
    invalid_tickers = []
    all_data = None # Initialize
    try:
        # Download data without immediately selecting 'Adj Close'
        # Use actions=False to potentially avoid issues with dividends/splits data structure
        all_data = yf.download(tickers, start=start_date, end=end_date, progress=False, actions=False)

        if all_data is None or all_data.empty:
            st.warning(f"yfinance returned no data for tickers: {', '.join(tickers)} in the specified date range.")
            return None, tickers

        # Now, try to access 'Adj Close' or 'Close'
        data = None
        if isinstance(all_data.columns, pd.MultiIndex): # Common for multiple tickers
            if 'Adj Close' in all_data.columns.get_level_values(0):
                data = all_data['Adj Close']
            elif 'Close' in all_data.columns.get_level_values(0): # Fallback to 'Close'
                # Silently fall back to Close prices without warning
                data = all_data['Close']
            else:
                st.error("Could not find 'Adj Close' or 'Close' columns in the downloaded multi-index data.")
                return None, tickers
        elif 'Adj Close' in all_data.columns: # Single ticker case
            data = all_data[['Adj Close']] # Keep as DataFrame
            if len(tickers) == 1: data.columns = tickers # Rename column
        elif 'Close' in all_data.columns: # Fallback for single ticker
            # Silently fall back to Close prices without warning
            data = all_data[['Close']] # Keep as DataFrame
            if len(tickers) == 1: data.columns = tickers # Rename column
        else:
            st.error("Downloaded data structure is unexpected and does not contain 'Adj Close' or 'Close'.")
            st.dataframe(all_data.head()) # Show structure for debugging
            return None, tickers

        if data is None or data.empty:
            st.error("Could not extract valid price data ('Adj Close' or 'Close') from download.")
            return None, tickers # No valid price data extracted

        # Data extracted, proceed with validation
        # Check for columns that are all NaN (often indicates ticker download failure)
        invalid_tickers_nan = [ticker for ticker in data.columns if data[ticker].isnull().all()]
        valid_data = data.drop(columns=invalid_tickers_nan)

        if valid_data.empty:
            st.warning(f"All fetched tickers ({', '.join(data.columns)}) had only NaN values in the date range.")
            return None, list(set(tickers)) # Return all originally requested tickers as potentially invalid

        # Drop rows where all remaining valid columns are NaN (handles potential gaps)
        valid_data.dropna(axis=0, how='all', inplace=True)

        # Fill intermediate NaNs using forward fill, then backward fill
        valid_data.ffill(inplace=True)
        valid_data.bfill(inplace=True)

        # Check again if empty after NaN handling
        if valid_data.empty:
            st.warning("Dataframe became empty after removing rows with all NaNs and filling.")
            return None, list(set(tickers))

        # Determine actually invalid tickers based on which columns are NOT in valid_data's final columns
        fetched_valid_tickers = valid_data.columns.tolist()
        invalid_tickers_final = [t for t in tickers if t not in fetched_valid_tickers]

        return valid_data, invalid_tickers_final

    except KeyError as ke:
         st.error(f"Data fetching error: Could not process downloaded data due to unexpected structure ({ke}). Check ticker validity and data availability.")
         if all_data is not None:
             st.write("Downloaded data structure (first 5 rows):")
             st.dataframe(all_data.head()) # Show head of data for debugging
         return None, tickers
    except Exception as e:
        st.error(f"An unexpected error occurred during data fetching: {e}")
        # Consider logging the full traceback here for advanced debugging
        return None, tickers

def calculate_metrics(portfolio_returns: pd.Series, benchmark_returns: pd.Series, risk_free_rate: float = 0.0) -> dict:
    """Calculates key performance metrics."""
    metrics = {}
    trading_days = 252 # Standard assumption

    # --- Portfolio Metrics ---
    if portfolio_returns is not None and not portfolio_returns.empty:
        cumulative_portfolio_return = (1 + portfolio_returns).prod() - 1
        metrics['Total Portfolio Return (%)'] = cumulative_portfolio_return * 100

        # Geometric Mean for Annualized Return (CAGR)
        years = len(portfolio_returns) / trading_days
        if years > 0:
            # Ensure the base is positive before exponentiation
            base = 1 + cumulative_portfolio_return
            if base > 0:
                 annualized_portfolio_return = (base ** (1 / years)) - 1
                 metrics['Annualized Portfolio Return (%)'] = annualized_portfolio_return * 100
            else:
                 # Handle cases with >100% loss
                 metrics['Annualized Portfolio Return (%)'] = -100.0 if np.isclose(base, 0) else np.nan
                 annualized_portfolio_return = -1.0 # Set for Sharpe calculation if needed
        else:
            metrics['Annualized Portfolio Return (%)'] = np.nan # Avoid division by zero
            annualized_portfolio_return = np.nan

        annualized_portfolio_volatility = portfolio_returns.std() * np.sqrt(trading_days)
        metrics['Annualized Portfolio Volatility (%)'] = annualized_portfolio_volatility * 100

        # Sharpe Ratio
        if annualized_portfolio_volatility != 0 and not np.isnan(annualized_portfolio_return):
            metrics['Portfolio Sharpe Ratio'] = (annualized_portfolio_return - risk_free_rate) / annualized_portfolio_volatility
        else:
            metrics['Portfolio Sharpe Ratio'] = np.nan

        # Sortino Ratio
        negative_returns = portfolio_returns[portfolio_returns < 0]
        if not negative_returns.empty:
            downside_deviation = negative_returns.std() * np.sqrt(trading_days)
            if downside_deviation != 0 and not np.isnan(annualized_portfolio_return):
                metrics['Portfolio Sortino Ratio'] = (annualized_portfolio_return - risk_free_rate) / downside_deviation
            else:
                metrics['Portfolio Sortino Ratio'] = np.nan # Handle zero downside deviation or NaN return
        else: # No negative returns
             metrics['Portfolio Sortino Ratio'] = np.inf if annualized_portfolio_return > risk_free_rate else 0.0 # Or np.nan? inf is common

        # Max Drawdown
        cumulative_wealth = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative_wealth.cummax()
        drawdown = (cumulative_wealth - rolling_max) / rolling_max
        max_drawdown_value = drawdown.min()
        metrics['Portfolio Max Drawdown (%)'] = max_drawdown_value * 100 if not pd.isna(max_drawdown_value) else np.nan

    else: # Handle case where portfolio returns are None or empty
        metrics.update({
            'Total Portfolio Return (%)': np.nan,
            'Annualized Portfolio Return (%)': np.nan,
            'Annualized Portfolio Volatility (%)': np.nan,
            'Portfolio Sharpe Ratio': np.nan,
            'Portfolio Sortino Ratio': np.nan,
            'Portfolio Max Drawdown (%)': np.nan
        })
        annualized_portfolio_return = np.nan # Ensure this is defined


    # --- Benchmark Metrics ---
    if benchmark_returns is not None and not benchmark_returns.empty:
        cumulative_benchmark_return = (1 + benchmark_returns).prod() - 1
        metrics['Total Benchmark Return (%)'] = cumulative_benchmark_return * 100

        # Geometric Mean for Annualized Return (CAGR)
        years_bm = len(benchmark_returns) / trading_days
        if years_bm > 0:
            base_bm = 1 + cumulative_benchmark_return
            if base_bm > 0:
                annualized_benchmark_return = (base_bm ** (1 / years_bm)) - 1
                metrics['Annualized Benchmark Return (%)'] = annualized_benchmark_return * 100
            else:
                metrics['Annualized Benchmark Return (%)'] = -100.0 if np.isclose(base_bm, 0) else np.nan
                annualized_benchmark_return = -1.0 # Set for Sharpe calculation
        else:
            metrics['Annualized Benchmark Return (%)'] = np.nan
            annualized_benchmark_return = np.nan

        annualized_benchmark_volatility = benchmark_returns.std() * np.sqrt(trading_days)
        metrics['Annualized Benchmark Volatility (%)'] = annualized_benchmark_volatility * 100

        # Benchmark Sharpe (Optional but good for comparison)
        if annualized_benchmark_volatility != 0 and not np.isnan(annualized_benchmark_return):
            metrics['Benchmark Sharpe Ratio'] = (annualized_benchmark_return - risk_free_rate) / annualized_benchmark_volatility
        else:
            metrics['Benchmark Sharpe Ratio'] = np.nan
    else: # Handle case where benchmark returns are None or empty
        metrics.update({
             'Total Benchmark Return (%)': np.nan,
            'Annualized Benchmark Return (%)': np.nan,
            'Annualized Benchmark Volatility (%)': np.nan,
            'Benchmark Sharpe Ratio': np.nan
        })

    return metrics

# --- Streamlit App Layout ---
st.markdown('<h1 class="main-header">📈 Portfolio Performance Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="info-text">Analyze historical performance of your stock portfolio against a benchmark index.</p>', unsafe_allow_html=True)

# --- Sidebar UI Enhancement ---
with st.sidebar:
    st.markdown('<h2 style="color:#90CAF9;">⚙️ Configuration</h2>', unsafe_allow_html=True)
    
    with st.form(key='portfolio_form'):
        # --- Portfolio Definition with better spacing ---
        st.markdown('<h3 style="color:#E0E0E0;">Portfolio Definition</h3>', unsafe_allow_html=True)
        
        tickers_string = st.text_input(
            "Enter Stock Tickers (comma-separated)", 
            "AAPL, MSFT, GOOG, AMZN", 
            help="Example: AAPL, MSFT, GOOG"
        ).upper()
        
        weights_string = st.text_input(
            "Enter Corresponding Weights (%)", 
            "25, 25, 25, 25", 
            help="Example: 40, 30, 30. Must sum to 100."
        )
        
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # --- Backtest Parameters ---
        st.markdown('<h3 style="color:#E0E0E0;">Backtest Parameters</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            start_date_default = datetime.today() - timedelta(days=5*365)
            start_date = st.date_input("Start Date", start_date_default)
        with col2:
            end_date_default = datetime.today()
            end_date = st.date_input("End Date", end_date_default)
            
        benchmark_ticker = st.text_input(
            "Benchmark Ticker", 
            "SPY",
            help="Standard benchmark is SPY (S&P 500 ETF)"
        ).upper()
        
        initial_investment = st.number_input(
            "Initial Investment ($)", 
            min_value=1.0, 
            value=10000.0, 
            step=1000.0,
            format="%0.2f"
        )
        
        risk_free_rate_input = st.number_input(
            "Risk-Free Rate (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=1.0, 
            step=0.1, 
            help="Annual risk-free rate for Sharpe/Sortino calculation."
        ) / 100
        
        # --- Run Button with better styling ---
        submitted = st.form_submit_button(
            "🚀 Run Analysis",
            use_container_width=True,
            type="primary"
        )

# --- Main Panel Logic ---
if submitted:
    with st.spinner('Running analysis... Please wait.'):
        # --- 1. Input Validation and Portfolio Parsing ---
        valid_input = True
        weights_sum_100 = True # Assume true initially
        tickers = []
        weights = []
        portfolio_df = pd.DataFrame({'Ticker': [], 'Weight': []}) # Initialize empty

        # Date Validation
        if start_date >= end_date:
            st.error("Error: Start date must be before end date.")
            valid_input = False

        # Benchmark Validation
        if not benchmark_ticker:
            st.error("Error: Benchmark ticker cannot be empty.")
            valid_input = False

        # Portfolio Parsing
        if not tickers_string:
            st.error("Error: Tickers cannot be empty.")
            valid_input = False
        else:
            tickers = [t.strip().upper() for t in tickers_string.split(',') if t.strip()]
            if not tickers: # Check if list is empty after stripping
                 st.error("Error: Tickers cannot be empty.")
                 valid_input = False

        if not weights_string:
             st.error("Error: Weights cannot be empty.")
             valid_input = False
        elif valid_input: # Only parse weights if tickers are valid so far
             try:
                 weights_raw = [w.strip() for w in weights_string.split(',') if w.strip()]
                 if not weights_raw:
                     st.error("Error: Weights cannot be empty.")
                     valid_input = False
                 else:
                     weights = [float(w) for w in weights_raw]
             except ValueError:
                 st.error("Error: Weights must be numeric values.")
                 valid_input = False

        # Check lengths and sum only if inputs were valid and parsed correctly
        if valid_input:
            if len(tickers) != len(weights):
                st.error(f"Error: Mismatch between number of tickers ({len(tickers)}) and weights ({len(weights)}).")
                valid_input = False
            else:
                # Check for negative weights
                if any(w < 0 for w in weights):
                    st.error("Error: Portfolio weights cannot be negative.")
                    valid_input = False
                else:
                    total_weight = sum(weights)
                    if np.isclose(total_weight, 0):
                        st.error("Error: Total weight is zero. Please check weights.")
                        valid_input = False
                    elif not np.isclose(total_weight, 100.0):
                        weights_sum_100 = False
                        st.info(f"Weights sum to {total_weight:.2f}%. They will be normalized to 100%.")
                        weights = [(w / total_weight) * 100 for w in weights]
                        weights_sum_100 = True # Set to True after normalization

                    # Create DataFrame only if everything is valid
                    if valid_input:
                        portfolio_df = pd.DataFrame({'Ticker': tickers, 'Weight': weights})


        # --- 2. Fetch Data ---
        all_tickers_to_fetch = []
        raw_data = None
        invalid_tickers_fetch = []
        data_valid = False # Flag to track if we have usable data

        if valid_input:
            # --- Duplicate-ticker guard ---
            if benchmark_ticker in portfolio_df['Ticker'].values:
                st.warning(f"Benchmark ticker '{benchmark_ticker}' was found in your portfolio. It will be removed from the portfolio calculation to prevent duplication, and weights will be renormalized.")
                benchmark_weight = portfolio_df.loc[portfolio_df['Ticker'] == benchmark_ticker, 'Weight'].iloc[0]
                portfolio_df = portfolio_df[portfolio_df['Ticker'] != benchmark_ticker].copy()

                if portfolio_df.empty:
                    st.error("After removing the benchmark ticker, no tickers remain in the portfolio. Analysis cannot proceed.")
                    valid_input = False # Stop further processing
                else:
                    # Re-normalize remaining weights
                    remaining_total_weight = portfolio_df['Weight'].sum()
                    if np.isclose(remaining_total_weight, 0):
                         st.error("Error: Remaining portfolio weights sum to zero after removing benchmark.")
                         valid_input = False
                    else:
                        portfolio_df['Weight'] = (portfolio_df['Weight'] / remaining_total_weight) * 100
                        st.sidebar.subheader("Modified Portfolio (Benchmark Removed)")
                        st.sidebar.dataframe(portfolio_df.set_index('Ticker').style.format({'Weight': '{:.2f}%'}))
                        # Update tickers and weights lists as well for consistency if needed later
                        tickers = portfolio_df['Ticker'].tolist()
                        weights = portfolio_df['Weight'].tolist()


            # Proceed only if input is still valid after potential benchmark removal
            if valid_input:
                all_tickers_to_fetch = list(set(portfolio_df['Ticker'].tolist() + [benchmark_ticker])) # Unique list
                start_str = start_date.strftime('%Y-%m-%d')
                end_str = end_date.strftime('%Y-%m-%d')

                raw_data, invalid_tickers_fetch = fetch_data(all_tickers_to_fetch, start_str, end_str)

                if raw_data is None or raw_data.empty:
                    st.error(f"Could not fetch valid data for any tickers: {', '.join(all_tickers_to_fetch)}. Check tickers and date range.")
                    valid_input = False # Mark as invalid to prevent calculations
                else:
                    data_valid = True # We got some data
                    fetched_tickers = raw_data.columns.tolist()

                    # Report fully invalid tickers from yfinance download
                    if invalid_tickers_fetch:
                        st.warning(f"Could not fetch any data for: {', '.join(invalid_tickers_fetch)}. These were excluded.")

                    # --- Filter Portfolio based on Fetched Data ---
                    original_portfolio_tickers = portfolio_df['Ticker'].tolist()
                    portfolio_tickers_fetched = [t for t in original_portfolio_tickers if t in fetched_tickers]
                    missing_portfolio_tickers = [t for t in original_portfolio_tickers if t not in fetched_tickers]

                    if missing_portfolio_tickers:
                        st.warning(f"Could not fetch/validate data for portfolio tickers: {', '.join(missing_portfolio_tickers)}. They will be excluded.")
                        portfolio_df = portfolio_df[portfolio_df['Ticker'].isin(portfolio_tickers_fetched)].copy()

                        if portfolio_df.empty:
                            st.error("Error: No data fetched for any of the specified portfolio tickers after filtering.")
                            data_valid = False # Cannot proceed
                            valid_input = False
                        else:
                            # Re-normalize weights again if some tickers were dropped
                            current_total_weight = portfolio_df['Weight'].sum()
                            if not np.isclose(current_total_weight, 100.0):
                                st.info("Re-normalizing portfolio weights due to missing ticker data.")
                                if np.isclose(current_total_weight, 0):
                                     st.error("Error: Remaining portfolio weights sum to zero after filtering.")
                                     data_valid = False
                                     valid_input = False
                                else:
                                    portfolio_df['Weight'] = (portfolio_df['Weight'] / current_total_weight) * 100
                                    st.sidebar.subheader("Re-Normalized Portfolio (Data Filtered)")
                                    st.sidebar.dataframe(portfolio_df.set_index('Ticker').style.format({'Weight': '{:.2f}%'}))
                                    # Update tickers/weights lists if needed
                                    tickers = portfolio_df['Ticker'].tolist()
                                    weights = portfolio_df['Weight'].tolist()


                    # --- Check Benchmark Data ---
                    benchmark_data_valid = False
                    if benchmark_ticker not in fetched_tickers:
                        st.warning(f"Could not fetch/validate data for benchmark ticker: {benchmark_ticker}. Benchmark comparison will be unavailable.")
                        benchmark_data = None
                    else:
                        # Check if benchmark column has all NaNs even if fetched
                        if raw_data[benchmark_ticker].isnull().all():
                             st.warning(f"Benchmark ticker {benchmark_ticker} fetched but contains only NaN values. Benchmark comparison unavailable.")
                             benchmark_data = None
                        else:
                            benchmark_data = raw_data[[benchmark_ticker]].copy() # Keep as DataFrame
                            benchmark_data_valid = True


        # --- 3. Calculations ---
        portfolio_daily_returns = None
        benchmark_daily_returns = None
        perf_df = pd.DataFrame() # Initialize performance dataframe

        if valid_input and data_valid and not portfolio_df.empty:
            # Select final valid portfolio data
            portfolio_data = raw_data[portfolio_df['Ticker'].tolist()].copy()

            # Clear any existing cached data that might be affecting calculations
            st.cache_data.clear()
            
            # Align portfolio_df weights with the columns in portfolio_data
            # Get weights from the updated portfolio_df
            aligned_weights = portfolio_df.set_index('Ticker').reindex(portfolio_data.columns)['Weight'] / 100.0 # Convert to decimal
            
            # Calculate daily returns
            portfolio_returns_data = portfolio_data.pct_change().dropna(how='all') # Drop rows where ALL returns are NaN

            # Force recalculation of weighted daily portfolio return
            portfolio_daily_returns = (portfolio_returns_data * aligned_weights).sum(axis=1)
            
            # Verify non-zero returns data has been calculated
            if portfolio_daily_returns.std() < 1e-10:  # Check if returns are extremely small/constant
                st.warning("Portfolio returns appear to be constant, check the input data and weights.")
                
            # Prepare benchmark returns if valid
            if benchmark_data_valid and benchmark_data is not None:
                benchmark_daily_returns = benchmark_data.pct_change().dropna().squeeze() # Convert to Series

                # Align dates using intersection (IMPORTANT!)
                common_index = portfolio_daily_returns.index.intersection(benchmark_daily_returns.index)
                portfolio_daily_returns = portfolio_daily_returns.loc[common_index]
                benchmark_daily_returns = benchmark_daily_returns.loc[common_index]
                
                # Verify the data is different (silently check without displaying)
                correlation = portfolio_daily_returns.corr(benchmark_daily_returns)
                if np.isclose(correlation, 1.0, atol=1e-4):
                    st.warning("Portfolio and benchmark returns are nearly identical. Please check your portfolio weights.")
            else:
                benchmark_daily_returns = pd.Series(dtype=float) # Ensure it's an empty Series for metric calculation


            # --- Calculate cumulative portfolio/benchmark VALUES for visualization ---
            if not portfolio_daily_returns.empty:
                perf_df = pd.DataFrame(index=portfolio_daily_returns.index)
                perf_df['Portfolio_Value'] = initial_investment * (1 + portfolio_daily_returns).cumprod()

                if not benchmark_daily_returns.empty:
                    # Ensure benchmark calculation starts from the same point if dates were aligned
                    perf_df['Benchmark_Value'] = initial_investment * (1 + benchmark_daily_returns).cumprod()
                else:
                     perf_df['Benchmark_Value'] = np.nan # Add NaN column if no benchmark

                # Add the initial investment row at the beginning for plotting
                start_row_date = perf_df.index.min() - pd.Timedelta(days=1) # Day before first return
                initial_values = {'Portfolio_Value': initial_investment}
                if 'Benchmark_Value' in perf_df.columns and benchmark_data_valid:
                    initial_values['Benchmark_Value'] = initial_investment
                else:
                    initial_values['Benchmark_Value'] = np.nan # Keep NaN if no benchmark

                # Use pd.concat to add the initial row
                initial_row_df = pd.DataFrame(initial_values, index=[start_row_date])
                perf_df = pd.concat([initial_row_df, perf_df])
                perf_df.sort_index(inplace=True)


            # --- 4. Calculate Metrics ---
            # Pass the aligned daily return Series to the metrics function
            metrics = calculate_metrics(portfolio_daily_returns, benchmark_daily_returns, risk_free_rate_input)

            # --- 5. Display Results with improved UI ---
            if valid_input and data_valid and not portfolio_df.empty:
                # Create tabs for better organization - removed Statistics tab
                tabs = st.tabs([
                    "📊 Performance Metrics", 
                    "📈 Portfolio Growth", 
                    "🍩 Asset Allocation"
                ])
                
                # --- Tab 1: Key Metrics ---
                with tabs[0]:
                    # Remove the empty box by directly showing the metrics
                    
                    # Format metrics and create more visual display
                    metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
                    
                    # Better formatting function
                    def format_value(x, is_percent=False):
                        if isinstance(x, (int, float)):
                            if pd.isna(x): return 'N/A'
                            if np.isinf(x): 
                                if x > 0: return '<span class="positive">∞</span>'
                                return '<span class="negative">-∞</span>'
                            
                            formatted = f"{x:.2f}"
                            if is_percent: formatted += "%"
                            
                            # Add color for positive/negative values
                            if x > 0:
                                return f'<span class="positive">{formatted}</span>'
                            elif x < 0:
                                return f'<span class="negative">{formatted}</span>'
                            return formatted
                        return x

                    # Format each metric type appropriately
                    metrics_df['Value_Formatted'] = metrics_df.apply(
                        lambda row: format_value(
                            row['Value'], 
                            is_percent=("%" in row['Metric'])
                        ), 
                        axis=1
                    )
                    
                    # Split metrics for side-by-side display
                    portfolio_metrics_df = metrics_df[metrics_df['Metric'].str.contains("Portfolio", na=False)]
                    benchmark_metrics_df = metrics_df[metrics_df['Metric'].str.contains("Benchmark", na=False)]
                    
                    # Make compact metrics display
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.markdown('<h3 class="sub-header">Portfolio Performance</h3>', unsafe_allow_html=True)
                        
                        # Create a cleaner HTML table for metrics
                        html_table = '<table width="100%" style="background-color:#1E1E1E; border-radius:5px; padding:10px;">'
                        for _, row in portfolio_metrics_df.iterrows():
                            metric_name = row['Metric'].replace('Portfolio ', '')
                            html_table += f'<tr><td style="padding:8px;">{metric_name}</td><td align="right" style="padding:8px;">{row["Value_Formatted"]}</td></tr>'
                        html_table += '</table>'
                        
                        st.markdown(html_table, unsafe_allow_html=True)
                    
                    with col_m2:
                        if not benchmark_metrics_df.empty and benchmark_data_valid:
                            st.markdown(f'<h3 class="sub-header">Benchmark Performance ({benchmark_ticker})</h3>', unsafe_allow_html=True)
                            
                            # Create a cleaner HTML table for metrics
                            html_table = '<table width="100%" style="background-color:#1E1E1E; border-radius:5px; padding:10px;">'
                            for _, row in benchmark_metrics_df.iterrows():
                                metric_name = row['Metric'].replace('Benchmark ', '')
                                html_table += f'<tr><td style="padding:8px;">{metric_name}</td><td align="right" style="padding:8px;">{row["Value_Formatted"]}</td></tr>'
                            html_table += '</table>'
                            
                            st.markdown(html_table, unsafe_allow_html=True)
                        else:
                            st.markdown(f'<h3 class="sub-header">Benchmark Data ({benchmark_ticker})</h3>', unsafe_allow_html=True)
                            st.warning("Benchmark metrics unavailable (data could not be fetched)")
                        
                        # Add metric explanations
                        with st.expander("📘 What do these metrics mean?"):
                            st.markdown("""
                            * **Total Return (%)**: Overall percentage gain/loss over the entire period
                            * **Annualized Return (%)**: Return averaged to an annual basis
                            * **Annualized Volatility (%)**: Measure of risk/variability in returns
                            * **Sharpe Ratio**: Risk-adjusted return (higher is better)
                            * **Sortino Ratio**: Similar to Sharpe but only considers downside risk
                            * **Max Drawdown (%)**: Largest percentage drop from peak to trough
                            """)
                
                # --- Tab 2: Growth Chart ---
                with tabs[1]:
                    if not portfolio_daily_returns.empty and 'Portfolio_Value' in perf_df.columns:
                        # Display key summary metrics
                        start_value = perf_df['Portfolio_Value'].iloc[0]
                        end_value = perf_df['Portfolio_Value'].iloc[-1]
                        growth = end_value - start_value
                        total_return = ((end_value / start_value) - 1) * 100 if start_value > 0 else 0
                        
                        # Make metrics more visual
                        summary_cols = st.columns(3)
                        with summary_cols[0]:
                            st.markdown(f"<h3 style='text-align: center; color:#E0E0E0;'>Initial Investment</h3>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='text-align: center; color:#E0E0E0;'>${start_value:.2f}</h2>", unsafe_allow_html=True)
                            
                        with summary_cols[1]:
                            st.markdown(f"<h3 style='text-align: center; color:#E0E0E0;'>Final Value</h3>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='text-align: center; color:#E0E0E0;'>${end_value:.2f}</h2>", unsafe_allow_html=True)
                            
                        with summary_cols[2]:
                            color_class = "positive" if total_return >= 0 else "negative"
                            st.markdown(f"<h3 style='text-align: center; color:#E0E0E0;'>Total Return</h3>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='text-align: center;' class='{color_class}'>{total_return:.2f}%</h2>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align: center;'>Change: <span class='{color_class}'>${growth:.2f}</span></p>", unsafe_allow_html=True)
                        
                        # Enhanced growth chart
                        fig_growth = go.Figure()
                        
                        # Portfolio trace with better style
                        fig_growth.add_trace(go.Scatter(
                            x=perf_df.index.tolist(),
                            y=perf_df['Portfolio_Value'].tolist(),
                            name='Portfolio',
                            mode='lines',
                            line=dict(color='#1E88E5', width=3)
                        ))
                        
                        # Add benchmark if available
                        if 'Benchmark_Value' in perf_df.columns and benchmark_data_valid:
                            fig_growth.add_trace(go.Scatter(
                                x=perf_df.index.tolist(),
                                y=perf_df['Benchmark_Value'].tolist(),
                                name=f'{benchmark_ticker}',
                                mode='lines',
                                line=dict(color='#FFA000', width=2)
                            ))
                        
                        # Better y-axis range
                        min_value = max(0, perf_df['Portfolio_Value'].min() * 0.9)
                        max_value = perf_df['Portfolio_Value'].max() * 1.1
                        min_value = min(min_value, initial_investment * 0.5)
                        max_value = max(max_value, initial_investment * 1.5)
                        
                        # Enhanced layout
                        fig_growth.update_layout(
                            title=None,
                            xaxis_title='Date',
                            yaxis=dict(
                                title='Value ($)',
                                tickprefix='$',
                                range=[min_value, max_value],
                                autorange=False
                            ),
                            template='plotly_white',
                            hovermode='x unified',
                            height=500,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            ),
                            margin=dict(l=60, r=30, t=30, b=60),
                            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                            plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot background
                            font=dict(color='#E0E0E0')      # White text
                        )
                        
                        # Add initial investment line
                        fig_growth.add_shape(
                            type="line",
                            x0=perf_df.index.min(),
                            x1=perf_df.index.max(), 
                            y0=initial_investment,
                            y1=initial_investment,
                            line=dict(color="#757575", width=1.5, dash="dash")
                        )
                        
                        # Add annotation for initial investment
                        fig_growth.add_annotation(
                            x=perf_df.index.min(),
                            y=initial_investment,
                            text="Initial Investment",
                            showarrow=False,
                            xshift=10,
                            yshift=10,
                            bgcolor="#333333",
                            bordercolor="#757575",
                            font=dict(color="#E0E0E0"),
                            borderwidth=1
                        )
                        
                        st.plotly_chart(fig_growth, use_container_width=True)
                    else:
                        st.info("Insufficient data to display investment growth. Please check portfolio data.")
                
                # --- Tab 3: Asset Allocation ---
                with tabs[2]:
                    if not portfolio_df.empty:
                        # Side-by-side layout for table and chart
                        col_alloc1, col_alloc2 = st.columns([1, 2])
                        
                        with col_alloc1:
                            # Direct header without card container
                            st.markdown('<h3 style="color:#E0E0E0; margin-bottom: 15px;">Portfolio Weights</h3>', unsafe_allow_html=True)
                            
                            # Enhance allocation table
                            allocation_df = pd.DataFrame({
                                'Ticker': portfolio_df['Ticker'],
                                'Weight (%)': portfolio_df['Weight']
                            })
                            
                            # Format with colors based on weight - using white text
                            def highlight_weights(val):
                                if isinstance(val, float):
                                    normalized = min(1.0, val / max(allocation_df['Weight (%)']))
                                    r, g, b = 30, 72, 115  # Dark blue base color
                                    r2, g2, b2 = 66, 133, 200  # Lighter blue for highest weights
                                    # Interpolate colors
                                    r_val = int(r + normalized * (r2 - r))
                                    g_val = int(g + normalized * (g2 - g))
                                    b_val = int(b + normalized * (b2 - b))
                                    return f'background-color: rgb({r_val}, {g_val}, {b_val}); color: white'
                                return 'color: white'  # Ensure all text is white
                            
                            # Add explicit styling for all table elements
                            st.dataframe(
                                allocation_df.style
                                .format({'Weight (%)': '{:.2f}'})
                                .applymap(highlight_weights)  # Apply to all cells
                                .set_properties(**{
                                    'font-size': '16px', 
                                    'text-align': 'center', 
                                    'color': 'white',
                                    'background-color': '#121212'
                                })
                                .set_table_styles([
                                    {'selector': 'th', 'props': [
                                        ('font-size', '18px'), 
                                        ('color', 'white'),
                                        ('background-color', '#1E1E1E')
                                    ]},
                                    {'selector': '.row_heading', 'props': [
                                        ('color', 'white'),
                                        ('background-color', '#1E1E1E')
                                    ]}
                                ]),
                                use_container_width=True
                            )
                        
                        with col_alloc2:
                            # Enhanced pie chart with black lines and no title
                            labels = portfolio_df['Ticker'].tolist()
                            values = portfolio_df['Weight'].tolist()
                            
                            # Custom color sequence for pie chart
                            colors = px.colors.qualitative.Safe
                            
                            fig_pie = go.Figure(data=[go.Pie(
                                labels=labels,
                                values=values,
                                hole=0.4,
                                textinfo='label+percent',
                                hoverinfo='label+percent+value',
                                hovertemplate='<b>%{label}</b><br>Weight: %{value:.2f}%<br>Percentage: %{percent}<extra></extra>',
                                marker=dict(colors=colors, line=dict(color='#000000', width=2))
                            )])
                            
                            # Clean layout with no title
                            fig_pie.update_layout(
                                showlegend=True,
                                height=400,
                                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                                plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
                                margin=dict(l=0, r=0, t=0, b=0),  # No margins
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.1,
                                    xanchor="center",
                                    x=0.5,
                                    font=dict(color="white")
                                )
                            )
                            
                            st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("No portfolio allocation data available.")
            
            elif not valid_input:
                st.error("Analysis could not be run due to input errors. Please check the configuration settings.")
            elif not data_valid:
                st.error("Analysis could not be run because no valid market data could be fetched for the portfolio or benchmark.")
            elif portfolio_df.empty:
                st.error("Analysis could not be run because the portfolio is empty after filtering.")

else:
    # Enhanced welcome message with dark theme
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; background-color: #1E1E1E; margin-top: 30px;">
            <h2 style="color:#90CAF9;">Welcome to the Portfolio Analyzer!</h2>
            <p style="color:#E0E0E0;">This tool helps you analyze the historical performance of any custom stock portfolio and compare it to a benchmark index.</p>
            <h3 style="color:#E0E0E0;">Getting Started:</h3>
            <ol style="color:#E0E0E0;">
                <li>Enter your portfolio tickers and weights in the sidebar</li>
                <li>Set your desired backtest period</li>
                <li>Choose a benchmark (default is SPY - S&P 500 ETF)</li>
                <li>Click "Run Analysis" to see your results</li>
            </ol>
            <p style="font-style: italic; margin-top: 15px; color:#BDBDBD;">⬅️ Enter your portfolio details in the sidebar to begin!</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.image("https://img.icons8.com/color/240/000000/stocks-growth.png", width=150)
        st.markdown("""
        <div style="text-align: center; margin-top: 15px; color:#E0E0E0;">
            <h4 style="color:#90CAF9;">Sample Portfolios:</h4>
            <p>Tech Heavy: AAPL, MSFT, GOOG, AMZN<br>with weights 25, 25, 25, 25</p>
            <p>Balanced: VTI, BND, VEA, VWO<br>with weights 40, 30, 20, 10</p>
        </div>
        """, unsafe_allow_html=True) 