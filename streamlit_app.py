import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.title("Monthly Data Freshness Check")

# Step 1: Get monthly data for SPY (reliable ETF)
try:
    spy_data = yf.download("SPY", period="14mo", interval="1mo")

    if not spy_data.empty:
        # Get latest available date from the index
        latest_date = spy_data.index.max()
        latest_month = latest_date.strftime("%Y-%m")

        # Get current system month
        current_month = datetime.now().strftime("%Y-%m")

        st.write(f"Latest SPY data month: {latest_month}")
        st.write(f"Current month: {current_month}")

        # Step 2: Compare
        is_current_data = latest_month == current_month
        st.write(f"Model using current monthly data: {is_current_data}")

    else:
        st.warning("SPY data is empty. Check connection or try again.")
        st.write("Model using current monthly data: False")

except Exception as e:
    st.error(f"Data load failed: {e}")
    st.write("Model using current monthly data: False")
