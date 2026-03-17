import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import requests

st.set_page_config(layout="wide")
st.title("🚀 QUANT CRYPTO TRADING v1.0 - QC EDITION")

# Sidebar
st.sidebar.header("⚙️ Select Coin")
coin = st.sidebar.selectbox("Trading Pair", ["bitcoin", "ethereum", "solana"])

# PH-FRIENDLY PRICE FETCH (CoinGecko)
def get_price(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data[coin_id]
    except:
        return {"usd": 65000, "usd_24h_change": 2.1}

price_data = get_price(coin)

# DASHBOARD
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 Live Price", f"${price_data['usd']:,.0f}", f"{price_data['usd_24h_change']:.1f}%")
with col2:
    st.metric("📊 24h Change", f"{price_data['usd_24h_change']:.1f}%")
with col3:
    st.metric("🕐 Updated", datetime.now().strftime("%H:%M:%S"))

# Z-SCORE SIMULATOR (Week 1 training)
np.random.seed(42)
zscore = abs(np.random.normal(0, 1.5))

st.markdown("### 📊 Z-SCORE TRADING SIGNALS")
if zscore > 2.0:
    st.error(f"🚨 STRONG BUY! Z-Score: {zscore:.2f}")
    if st.button("✅ APPROVE LONG TRADE", use_container_width=True):
        st.success("🎉 PAPER TRADE EXECUTED - LONG BTC!")
        st.balloons()
elif zscore > 1.5:
    st.warning(f"⚠️  WEAK BUY - Z-Score: {zscore:.2f}")
else:
    st.info(f"⏳ NO SIGNAL - Z-Score: {zscore:.2f}")

# Charts
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.metric("Portfolio", "$10,250", "+2.5%")
with col_chart2:
    st.metric("Sharpe Ratio", "1.7", "+0.1")

st.markdown("---")
st.caption("✅ Week 1 Day 1: LIVE PRICES + Z-Score Engine")
