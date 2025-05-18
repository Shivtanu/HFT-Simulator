import streamlit as st

def show_ui():
    st.sidebar.title("Trade Simulator Input")
    asset = st.sidebar.selectbox("Asset", ["BTC-USDT"])
    quantity = st.sidebar.slider("USD Quantity", 10, 1000, 100)
    volatility = st.sidebar.slider("Volatility (%)", 0.1, 5.0, 1.0)
    fee_tier = st.sidebar.selectbox("Fee Tier", ["0.1%", "0.05%", "0.01%"])

    st.write("**Output:**")
    return asset, quantity, volatility, fee_tier
