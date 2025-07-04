import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from yahooquery import Ticker
import time

AUTHORIZED_CODES = ["freelunch"]

st.title("Dynamic Alpha Model")
code_input = st.text_input("Enter your DAM access code:", type="password")
is_code_valid = code_input in AUTHORIZED_CODES if code_input else None

if is_code_valid:
    st.success("Access Granted!")

    # Check if data is current
    test_ticker = "AAPL"
    current_month = datetime.now().strftime("%Y-%m")
    try:
        data_check = yf.download(test_ticker, period="14mo", interval="1mo")
        if isinstance(data_check.columns, pd.MultiIndex):
            data_check.columns = data_check.columns.droplevel(0)
        data_check.reset_index(inplace=True)
        latest_data_month = data_check["Date"].max().strftime("%Y-%m") if not data_check.empty else None
        is_current_data = latest_data_month == current_month if latest_data_month else False
    except Exception:
        is_current_data = False

    st.write(f"Model using current monthly data: {is_current_data}")

    if is_current_data:
        if st.button("Proceed"):
            st.write("Please allow a few minutes for your DAM tickers to load.")

            tickers = ["AAPL", "MSFT", "GOOGL"]
            all_data = pd.DataFrame()

            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - relativedelta(months=13)).replace(day=1).strftime('%Y-%m-%d')

            st.subheader('DAM Tickers')
            status_placeholder = st.empty()

            for ticker in tickers:
                status_placeholder.text(f"Downloading data for {ticker}...")
                try:
                    stock = yf.Ticker(ticker)
                    data = stock.history(period='14mo', interval='1mo')

                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.droplevel(0)

                    if not data.empty:
                        data.reset_index(inplace=True)
                        data['Ticker'] = ticker
                        try:
                            stock_info = stock.info
                            data['Sector'] = stock_info.get('sector', 'N/A')
                        except:
                            data['Sector'] = 'N/A'
                        all_data = pd.concat([all_data, data[['Date', 'Ticker', 'Sector', 'Close']]])
                except Exception as e:
                    st.warning(f"Failed to get {ticker}: {e}")
                time.sleep(1)

            all_data.reset_index(drop=True, inplace=True)
            all_data = all_data[all_data['Sector'] != 'N/A']

            all_data['Excess Return'] = all_data.groupby('Ticker')['Close'].pct_change().sub(0.024 / 12).fillna(0)

            spy_data = yf.Ticker('SPY').history(period='14mo', interval='1mo')
            if isinstance(spy_data.columns, pd.MultiIndex):
                spy_data.columns = spy_data.columns.droplevel(0)
            spy_data.reset_index(inplace=True)
            spy_data['SPY Excess Return'] = spy_data['Close'].pct_change().sub(0.024 / 12).fillna(0)
            spy_return_map = dict(zip(spy_data['Date'], spy_data['SPY Excess Return']))
            all_data['SPY Excess Return'] = all_data['Date'].map(spy_return_map)

            all_data['3 Month Return'] = all_data.groupby('Ticker')['Close'].pct_change(periods=3)

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

            all_data['DAM'] = all_data.apply(lambda row: (
                (row['3 Month Return'] or 0) + 
                (row['3 Month Market Weighted Return'] or 0) + 
                (row['12 Month Beta'] or 0)
            ) if pd.notnull(row['3 Month Return']) and pd.notnull(row['3 Month Market Weighted Return']) else 0, axis=1)

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

            st.subheader("Sector Weights")
            try:
                etf = Ticker('SPY')
                sector_weightings = etf.fund_sector_weightings
                if isinstance(sector_weightings, dict) and 'SPY' in sector_weightings:
                    for sector, weight in sector_weightings['SPY'].items():
                        st.write(f"{sector}: {weight:.2%}")
                else:
                    st.write("Sector weightings for SPY ETF not found or no data available.")
            except:
                st.write("Sector weightings could not be retrieved.")

elif is_code_valid is False:
    st.error("Please enter a valid code.")
