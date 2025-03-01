import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

# Define a list of allowed access codes
AUTHORIZED_CODES = ["freelunch"]

# Login page
st.title("Dynamic Alpha Model")
code_input = st.text_input("Enter your DAM access code:", type="password")

# Initialize a flag to check if the code is correct
is_code_valid = code_input in AUTHORIZED_CODES if code_input else None

if is_code_valid:
    st.success("Access Granted!")

    tickers = ['A', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK',
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
    'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZTS']
    all_data = pd.DataFrame()

    # Get the current date
    current_date = datetime.now()
    current_month_year = current_date.strftime('%Y-%m')  # Format as 'YYYY-MM'

    st.write("**DAM Instructions:**")
    st.write("Rotate at the beginning of the month.")
    st.write("Ensure current monthly data is true (before 5th).")
    st.write("Weight portfolio matching S&P sectors.")
    st.write("Errors/questions: tannerterry221@gmail.com")
    st.write("")
    st.write("Loading DAM Monthly Data. Please wait...")

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.history(period='14mo', interval='1mo')
        data.reset_index(inplace=True)

        if not data.empty:
            data['Ticker'] = ticker
            all_data = pd.concat([all_data, data[['Date', 'Ticker', 'Close']].rename(columns={'Close': 'Adj Close'})])

        time.sleep(1)  # Sleep to prevent rate limits

    all_data.reset_index(drop=True, inplace=True)

    # Extract the most recent date in the dataset
    if not all_data.empty:
        latest_data_date = all_data['Date'].max()
        latest_month_year = latest_data_date.strftime('%Y-%m')

        # Check if the latest data is from the current month
        is_current_data = latest_month_year == current_month_year
    else:
        is_current_data = False  # No data available

    st.write(f"Model using current monthly data: {is_current_data}")

    if st.button("Proceed"):
        st.write("Please allow a few minutes for your DAM tickers to load.")
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - relativedelta(months=13)).replace(day=1).strftime('%Y-%m-%d')

        st.subheader('DAM Tickers')
        status_placeholder = st.empty()

        for ticker in tickers:
            status_placeholder.text(f"Downloading data for {ticker}...")
            stock = yf.Ticker(ticker)
            data = stock.history(period='14mo', interval='1mo')
            data.reset_index(inplace=True)

            sector = 'N/A'
            try:
                stock_info = stock.info
                sector = stock_info.get('sector', 'N/A')
            except Exception:
                pass  # Suppress errors

            data['Ticker'] = ticker
            data['Sector'] = sector
            all_data = pd.concat([all_data, data[['Date', 'Ticker', 'Sector', 'Close']].rename(columns={'Close': 'Adj Close'})])

            time.sleep(1)  # Sleep for rate limits

        all_data.reset_index(drop=True, inplace=True)
        all_data = all_data[all_data['Sector'] != 'N/A']
        
        all_data['Excess Return'] = all_data.groupby('Ticker')['Adj Close'].pct_change().sub(0.024 / 12).fillna(0)

        spy_data = yf.Ticker('SPY').history(period='14mo', interval='1mo')
        spy_data.reset_index(inplace=True)
        spy_data['SPY Excess Return'] = spy_data['Close'].pct_change().sub(0.024 / 12).fillna(0)
        spy_return_map = dict(zip(spy_data['Date'], spy_data['SPY Excess Return']))
        all_data['SPY Excess Return'] = all_data['Date'].map(spy_return_map)

        all_data['3 Month Return'] = all_data.groupby('Ticker')['Adj Close'].pct_change(periods=3)

        def calculate_market_weighted_return(df):
            weighted_returns = [None] * 3
            for i in range(3, len(df)):
                weighted_returns.append(
                    df['SPY Excess Return'].iloc[i-3] * 0.04 +
                    df['SPY Excess Return'].iloc[i-2] * 0.16 +
                    df['SPY Excess Return'].iloc[i-1] * 0.36
                )
            return pd.Series(weighted_returns, index=df.index)

        all_data['3 Month Market Weighted Return'] = all_data.groupby('Ticker', group_keys=False).apply(calculate_market_weighted_return)

        def calculate_beta(df):
            beta = [None] * 11
            for i in range(11, len(df)):
                y = df['Excess Return'].iloc[i-11:i+1]
                x = df['SPY Excess Return'].iloc[i-11:i+1]
                beta.append(pd.Series(y).cov(x) / pd.Series(x).var())
            return pd.Series(beta, index=df.index)

        all_data['12 Month Beta'] = all_data.groupby('Ticker', group_keys=False).apply(calculate_beta)

        # Check for missing or zero values in 3 Month Return and 3 Month Market Weighted Return before calculating DAM
        all_data['DAM'] = all_data.apply(lambda row: (
            (row['3 Month Return'] or 0) + 
            (row['3 Month Market Weighted Return'] or 0) + 
            (row['12 Month Beta'] or 0)
        ) if row['3 Month Return'] is not None and row['3 Month Market Weighted Return'] is not None else 0, axis=1)

        tickers_dam = all_data.groupby('Ticker').agg({'DAM': 'mean'}).reset_index()
        tickers_dam_with_sector = all_data[['Ticker', 'Sector']].drop_duplicates()
        tickers_dam = tickers_dam.merge(tickers_dam_with_sector, on='Ticker', how='left')

        def get_top_two_dam_tickers(group):
            sorted_group = group.sort_values(by='DAM', ascending=False)
            top_ticker = sorted_group.iloc[0]
            alt_ticker = sorted_group.iloc[1] if len(sorted_group) > 1 else None
            return pd.Series({'Ticker': top_ticker['Ticker'], 'Alt Ticker': alt_ticker['Ticker'] if alt_ticker is not None else None})

        sector_best_tickers = tickers_dam.groupby('Sector').apply(get_top_two_dam_tickers).reset_index()
        st.write(sector_best_tickers.style.hide(axis="index").to_html(), unsafe_allow_html=True)

        # sector weights
        etf = yf.Ticker('SPY')
        funds_data = etf.funds_data  # Accessing funds data

        st.subheader("Sector Weights")
        try:
            sector_weightings = funds_data.sector_weightings  
            if sector_weightings:
                formatted_weightings = {sector: f"{weight * 100:.2f}%" for sector, weight in sector_weightings.items()}
                st.write(formatted_weightings)
            else:
                st.write("No sector weightings data available for SPY ETF.")
        except Exception:
            st.write("No sector weightings data available or an error occurred for SPY ETF.")

elif is_code_valid is False:
    st.error("Please enter a valid code.")
