import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

AUTHORIZED_CODES = ["freelunch"]

st.title("Dynamic Alpha Model")
code_input = st.text_input("Enter your DAM access code:", type="password")

is_code_valid = code_input in AUTHORIZED_CODES if code_input else None

if is_code_valid:
    st.success("Access Granted!")

    tickers = ["AAPL", "MSFT", "GOOGL"]
    all_data = pd.DataFrame()

    current_date = datetime.now()
    current_month_year = current_date.strftime('%Y-%m')

    st.write("**DAM Instructions:**")
    st.write("Rotate at the beginning of the month.")
    st.write("Ensure current monthly data is true (before 5th).")
    st.write("Weight portfolio matching S&P sectors.")
    st.write("Errors/questions: tannerterry221@gmail.com")
    st.write("")
    st.write("Loading DAM Monthly Data. Please wait...")

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='14mo', interval='1mo')

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(0)

            if not data.empty:
                data.reset_index(inplace=True)
                data['Ticker'] = ticker
                all_data = pd.concat([all_data, data[['Date', 'Ticker', 'Close']]])
            else:
                st.warning(f"No data for {ticker}")
        except Exception as e:
            st.warning(f"Failed to get {ticker}: {e}")
        time.sleep(1)

    all_data.reset_index(drop=True, inplace=True)

    if not all_data.empty:
        latest_data_date = all_data['Date'].max()
        latest_month_year = latest_data_date.strftime('%Y-%m')
        is_current_data = latest_month_year == current_month_year
    else:
        is_current_data = False

    st.write(f"Model using current monthly data: {is_current_data}")

    if st.button("Proceed"):
        st.write("Please allow a few minutes for your DAM tickers to load.")
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - relativedelta(months=13)).replace(day=1).strftime('%Y-%m-%d')

        st.subheader('DAM Tickers')
        status_placeholder = st.empty()

        for ticker in tickers:
            try:
                status_placeholder.text(f"Downloading data for {ticker}...")
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
                else:
                    st.warning(f"No data for {ticker}")
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
            etf = yf.Ticker('SPY')
            funds_data = etf.funds_data
            sector_weightings = funds_data.sector_weightings
            if sector_weightings:
                formatted_weightings = {sector: f"{weight * 100:.2f}%" for sector, weight in sector_weightings.items()}
                st.write(formatted_weightings)
            else:
                st.write("No sector weightings data available for SPY ETF.")
        except:
            st.write("No sector weightings data available or an error occurred for SPY ETF.")

elif is_code_valid is False:
    st.error("Please enter a valid code.")
