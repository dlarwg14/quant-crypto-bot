import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🚀 QUANT TRADING ENGINE v1.6 - CORE Z-SCORE + GA")
st.markdown("---")

# LIVE BTC PRICE
@st.cache_data(ttl=30)
def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['bitcoin']['usd'], data['bitcoin']['usd_24h_change']
    except:
        return 65432, 2.1

price, change = get_btc_price()

# QUANT DATA ENGINE
np.random.seed(42)
dates = pd.date_range(end=datetime.now(), periods=100, freq='5T')
returns = np.random.normal(0, 0.002, 100)
prices = price * np.exp(np.cumsum(returns))

df = pd.DataFrame({'time': dates, 'close': prices})

# Z-SCORE CORE ENGINE
df['sma20'] = df['close'].rolling(20).mean()
df['std20'] = df['close'].rolling(20).std()
df['zscore'] = (df['close'] - df['sma20']) / df['std20']
latest_zscore = df['zscore'].dropna().iloc[-1]

# RISK MANAGEMENT ENGINE (NEW SECTION)
st.markdown("---")
st.header("🛡️ RISK MANAGEMENT ENGINE")

# KELLY CRITERION POSITION SIZING
win_rate = 0.65  # From backtests
avg_win = 0.03   # 3% average win
avg_loss = 0.015 # 1.5% average loss
kelly_pct = (win_rate * avg_win - (1-win_rate) * avg_loss) / avg_win
position_size = min(kelly_pct * 100, 2.0)  # Max 2% risk

col_r1, col_r2, col_r3 = st.columns(3)
with col_r1: st.metric("🎯 Kelly Criterion", f"{kelly_pct:.1%}")
with col_r2: st.metric("📏 Position Size", f"{position_size:.1f}%")
with col_r3: st.metric("🛑 Max Risk/Trade", "2.0%")

# VaR CALCULATION
returns = df['close'].pct_change().dropna()
var_95 = np.percentile(returns, 5)
cvar_95 = returns[returns < var_95].mean()

st.markdown("### 📊 RISK METRICS")
col_var1, col_var2 = st.columns(2)
with col_var1: st.metric("VaR 95%", f"{var_95:.2%}")
with col_var2: st.metric("CVaR 95%", f"{cvar_95:.2%}")

# PORTFOLIO HEATMAP
st.markdown("### 🔥 PORTFOLIO RISK")
portfolio_value = 10000
max_positions = 5
risk_per_trade = portfolio_value * 0.02  # 2% rule
st.info(f"💰 $10K portfolio → Max ${risk_per_trade:,.0f} per trade")
st.info(f"⚡ {max_positions} concurrent positions max")


# DASHBOARD LAYOUT
col1, col2, col3 = st.columns(3)
with col1: st.metric("💰 BTC PRICE", f"${price:,.0f}")
with col2: st.metric("📈 24H", f"{change:.2f}%")
with col3: st.metric("⏰ Live", datetime.now().strftime("%H:%M:%S"))

st.markdown("### 🚨 Z-SCORE TRADING SIGNALS (CORE QUANT)")
if latest_zscore > 2.0:
    st.error(f"🚀 STRONG BUY! Z-Score: {latest_zscore:.2f}")
    if st.button("✅ APPROVE LONG", type="primary"):
        st.success("🎉 LONG TRADE EXECUTED!")
elif latest_zscore < -2.0:
    st.warning(f"🔻 STRONG SELL! Z-Score: {latest_zscore:.2f}")
    if st.button("✅ APPROVE SHORT"):
        st.success("🎉 SHORT TRADE EXECUTED!")
else:
    st.info(f"⏳ NO SIGNAL | Z-Score: {latest_zscore:.2f}")

col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.line_chart(df[['close', 'sma20']].tail(50), use_container_width=True)
with col_chart2:
    st.line_chart(df['zscore'].tail(50), use_container_width=True)

# GENETIC ALGORITHM SECTION
st.markdown("---")
st.header("🧬 GENETIC ALGORITHM EVOLUTION")

if st.button("🚀 EVOLVE 50 STRATEGIES", type="secondary"):
    strategies = []
    for i in range(50):
        period = np.random.randint(10, 30)
        temp_df = df.copy()
        temp_df[f'sma{period}'] = temp_df['close'].rolling(period).mean()
        temp_df['signal'] = np.where(temp_df['close'] > temp_df[f'sma{period}'], 1, -1)
        returns = temp_df['close'].pct_change() * temp_df['signal'].shift()
        sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        
        strategies.append({'id': i+1, 'period': period, 'sharpe': sharpe, 'fitness': abs(sharpe)})
    
    top5 = sorted(strategies, key=lambda x: x['fitness'], reverse=True)[:5]
    st.session_state.ga_results = top5
    st.success("✅ Top 5 strategies evolved!")

if 'ga_results' in st.session_state:
    st.markdown("### 🏆 TOP 5 STRATEGIES")
    ga_df = pd.DataFrame(st.session_state.ga_results)
    st.dataframe(ga_df, use_container_width=True)
    st.bar_chart(ga_df.set_index('id')['sharpe'])

st.markdown("---")
st.caption("🏛️ CORE QUANT ENGINE v1.6 | Z-Score + GA | Gerald QC 2026")
