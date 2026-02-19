import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3"

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("📊 Crypto Live Dashboard (Developed by- Rohit Denge)")

# Sidebar Controls
coin = st.sidebar.text_input("Enter Coin ID (example: bitcoin, ethereum)", "bitcoin")
currency = st.sidebar.selectbox("Select Currency", ["usd", "inr"])
days = st.sidebar.selectbox("Historical Data", ["7", "30", "90", "365"])

refresh_rate = st.sidebar.slider("Auto Refresh (seconds)", 5, 60, 10)

# =========================
# Get Live Price
# =========================
@st.cache_data(ttl=30)
def get_live_price(coin, currency):
    url = f"{BASE_URL}/simple/price"
    params = {"ids": coin, "vs_currencies": currency}
    response = requests.get(url, params=params)
    return response.json()

# =========================
# Get Historical Data
# =========================
@st.cache_data(ttl=300)
def get_historical_data(coin, currency, days):
    url = f"{BASE_URL}/coins/{coin}/market_chart"
    params = {"vs_currency": currency, "days": days}
    response = requests.get(url, params=params)
    data = response.json()

    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# =========================
# Live Price Section
# =========================
try:
    live_data = get_live_price(coin, currency)
    price = live_data[coin][currency]

    st.metric(label=f"{coin.upper()} Price ({currency.upper()})", value=f"{price}")

except:
    st.error("Invalid Coin ID or API Error")

# =========================
# Historical Chart
# =========================
try:
    df = get_historical_data(coin, currency, days)

    fig = px.line(df, x="timestamp", y="price",
                  title=f"{coin.upper()} Price Chart ({days} days)",
                  labels={"price": f"Price ({currency.upper()})"})

    st.plotly_chart(fig, use_container_width=True)

except:
    st.warning("Could not load historical data.")

# =========================
# Auto Refresh
# =========================
st.caption(f"Auto refreshing every {refresh_rate} seconds")
st.rerun()

