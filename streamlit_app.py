import streamlit as st

# Define a list of allowed access codes
AUTHORIZED_CODES = ["freelunch"]

# Login page
st.title("DYNAMIC ALPHA MODEL")
code_input = st.text_input("Enter your access code:", type="password")

# Check if the entered code is valid
if code_input in AUTHORIZED_CODES:
    st.success("You're in. Please allow a few minutes for your DAM tickers to load.")
else:
    st.error("Invalid access code. Please try again.")
    st.stop()  # Stops the app if the code is not correct

else:
    st.info("Enter your access code.")

import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from yahooquery import Ticker

# Define tickers and time period
tickers = [
    'SPY', 'A', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK',
    'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT',
    'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH',
    'APTV', 'ARE', 'ATO', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBWI',
    'BBY', 'BDX', 'BEN', 'BF.B', 'BIIB', 'BK', 'BKNG', 'BKR', 'BLK', 'BLL', 'BMY', 'BR', 'BRK.B', 'BRO',
    'BSX', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDNS',
    'CDW', 'CE', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMCSA', 'CME',
    'CMG', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP', 'COST', 'CPB', 'CPRT', 'CPT', 'CRL', 'CRM', 'CRWD', 'CSCO',
    'CSGP', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CTVA', 'CVS', 'CVX', 'D', 'DAL', 'DD', 'DE', 'DELL', 'DECK',
    'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOCU', 'DOV', 'DOW',
    'DPZ', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL',
    'EMN', 'EMR', 'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR', 'ERIE', 'EVRG', 'EW', 'EXC',
    'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FBHS', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV',
    'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRT', 'FTNT', 'FTV', 'GD', 'GDDY', 'GE', 'GEV', 'GEHC', 'GILD', 'GIS', 'GL',
    'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA',
    'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM',
    'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'INCY', 'INTC', 'INTU', 'INVH', 'IP', 'IPG', 'IR', 'IRM',
    'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBHT', 'JCI', 'JKHY', 'JNJ', 'JPM', 'K', 'KEY', 'KEYS', 'KHC', 'KIM',
    'KKR', 'KLAC', 'KMB', 'KMI', 'KO', 'KR', 'L', 'LDOS', 'LEN', 'LH', 'LHX', 'LIN', 'LMT', 'LNC', 'LNT',
    'LOW', 'LRCX', 'LUMN', 'LUV', 'LYB', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ',
    'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPWR',
    'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX',
    'NI', 'NKE', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA',
    'O', 'ODFL', 'OGN', 'OKE', 'OMC', 'ON', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PARA', 'PAYC', 'PAYX', 'PCAR',
    'PCG', 'PEAK', 'PEG', 'PENN', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD',
    'PLTR', 'PM', 'PNC', 'PNR', 'PNW', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PVH', 'PWR',
    'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP',
    'ROST', 'RSG', 'RTX', 'SBAC', 'SBUX', 'SCHW', 'SEDG', 'SEE', 'SHW', 'SIRI', 'SJM', 'SLB', 'SLG',
    'SNA', 'SNPS', 'SMCI', 'SO', 'SOLV', 'SPG', 'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK',
    'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO', 'TMUS',
    'TPR', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TXN', 'TXT', 'TYL', 'UAL', 'UDR',
    'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VICI', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN',
    'VRTX', 'VTR', 'VTRS', 'VZ', 'VST', 'WAB', 'WAT', 'WBA', 'WBD', 'WDC', 'WEC', 'WELL', 'WFC', 'WM',
    'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZTS'
]

all_data = pd.DataFrame()

# Define end date as today
end_date = datetime.now().strftime('%Y-%m-%d')

# Calculate start date as 13 months ago, and adjust to the first day of the month
start_date = (datetime.now() - relativedelta(months=13)).replace(day=1).strftime('%Y-%m-%d')

# Download data for all tickers
for ticker in tickers:
    print(f"Downloading monthly data for {ticker}...")
    
    # Download monthly historical data for each ticker
    data = yf.download(ticker, start=start_date, end=end_date, interval="1mo")
    
    # Get stock info, including sector
    stock_info = yf.Ticker(ticker).info
    sector = stock_info.get('sector', 'N/A')  # Get sector, if not available, return 'N/A'
    
    # Add Ticker, Sector, and Adjusted Close columns
    data['Ticker'] = ticker
    data['Sector'] = sector
    
    # Keep only the required columns
    all_data = pd.concat([all_data, data[['Ticker', 'Sector', 'Adj Close']]])

# Reset index to format DataFrame
all_data.reset_index(inplace=True)

# Calculate Excess Return (Column E)
all_data['Excess Return'] = (
    all_data.groupby('Ticker')['Adj Close']
    .pct_change()
    .sub(0.024 / 12)  # Subtracting the risk-free rate (monthly)
    .fillna(0)
)

# Get SPY data and calculate SPY Excess Return
spy_data = yf.download('SPY', start=start_date, end=end_date, interval="1mo")
spy_data['SPY Excess Return'] = spy_data['Adj Close'].pct_change().sub(0.024 / 12).fillna(0)
spy_data.reset_index(inplace=True)

# Map SPY Excess Return to all_data
spy_return_map = dict(zip(spy_data['Date'], spy_data['SPY Excess Return']))
all_data['SPY Excess Return'] = all_data['Date'].map(spy_return_map)

# Calculate 3 Month Return (Column G)
all_data['3 Month Return'] = all_data.groupby('Ticker')['Adj Close'].pct_change(periods=3)

# Calculate 3 Month Market Weighted Return (Column H)
def calculate_market_weighted_return(df):
    weighted_returns = []
    for i in range(len(df)):
        if i < 3:  # Require at least 3 months of data
            weighted_returns.append(None)
        else:
            weighted_return = (
                df['SPY Excess Return'].iloc[i-3] * 0.04 +  # 3 periods ago
                df['SPY Excess Return'].iloc[i-2] * 0.16 +  # 2 periods ago
                df['SPY Excess Return'].iloc[i-1] * 0.36    # 1 period ago (most recent)
            )
            weighted_returns.append(weighted_return)
    return pd.Series(weighted_returns, index=df.index)

all_data['3 Month Market Weighted Return'] = (
    all_data.groupby('Ticker', group_keys=False).apply(calculate_market_weighted_return)
)

# Calculate 12 Month Beta (Column I)
def calculate_beta(df):
    beta = []
    for i in range(len(df)):
        if i < 11:  # Require at least 12 months of data
            beta.append(None)
        else:
            y = df['Excess Return'].iloc[i-11:i+1]
            x = df['SPY Excess Return'].iloc[i-11:i+1]
            beta.append(pd.Series(y).cov(x) / pd.Series(x).var())
    return pd.Series(beta, index=df.index)

all_data['12 Month Beta'] = (
    all_data.groupby('Ticker', group_keys=False).apply(calculate_beta)
)

# Define DAM calculation function
def calculate_dam(row):
    # Example formula combining 3-month return, market weighted return, and beta.
    return (row['3 Month Return'] or 0) + (row['3 Month Market Weighted Return'] or 0) + (row['12 Month Beta'] or 0)

# Apply DAM calculation
all_data['DAM'] = all_data.apply(calculate_dam, axis=1)

# Group by Sector and select the ticker with the highest DAM for each sector
sector_best_tickers = all_data.groupby('Sector').apply(lambda x: x.loc[x['DAM'].idxmax()])

# Define the ETF symbol for S&P 500 (SPDR S&P 500 ETF Trust - SPY)
symbol = 'SPY'

# Fetch the fund sector data
etf = Ticker(symbol)
sector_weightings = etf.fund_sector_weightings

# Normalize sector names in sector_weightings
normalized_weights = {key.lower().replace(" ", "_"): value for key, value in sector_weightings['SPY'].items()}

# Print concise results: Sector, Ticker, and Sector Weight
st.write(f"{'Sector':<20} | {'Ticker':<6} | {'Sector Weight':>12}")
st.write("-" * 43)
for sector, row in sector_best_tickers.iterrows():
    normalized_sector = sector.lower().replace(" ", "_")  # Match naming convention
    weight = normalized_weights.get(normalized_sector, 'N/A')  # Map to normalized weights
    st.write(f"{sector:<20} | {row['Ticker']:<6} | {weight:>11.2%}" if weight != 'N/A' else f"{sector:<20} | {row['Ticker']:<6} | {'N/A':>11}")
