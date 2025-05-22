import streamlit as st
import asyncio
import threading

from orderbook import OrderBook
from websocket_client import WebSocketClient
from simulator import TradeSimulator

# Streamlit Setup
st.set_page_config(page_title="Crypto Trade Simulator", layout="wide")
st.title("📊 Real-Time Crypto Trade Simulator")

# Layout
left_col, right_col = st.columns(2)

# Initialize OrderBook and WebSocket
orderbook = OrderBook()
ws_client = WebSocketClient(orderbook)

# WebSocket run in background thread
def run_ws():
    asyncio.run(ws_client.connect())

if "ws_started" not in st.session_state:
    threading.Thread(target=run_ws, daemon=True).start()
    st.session_state.ws_started = True

# Left Panel: Input Parameters
with left_col:
    st.header("🛠 Input Parameters")

    exchange = st.selectbox("Exchange", ["OKX"], index=0)
    asset = st.selectbox("Spot Asset", ["BTC-USDT-SWAP"])
    order_type = st.selectbox("Order Type", ["Market"], index=0)
    quantity_usd = st.number_input("Order Quantity (USD)", min_value=10.0, max_value=100000.0, value=100.0, step=10.0)
    volatility = st.slider("Market Volatility (σ)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
    fee_tier = st.selectbox("Fee Tier", ["Standard", "VIP1", "VIP2"])  # Logic for fee can be expanded

    simulate_button = st.button("Simulate Trade")

# Right Panel: Output
with right_col:
    st.header("📈 Output Metrics")
    output_placeholder = st.empty()

    if simulate_button:
        simulator = TradeSimulator(orderbook)
        net_cost, fee, slippage, impact = simulator.simulate_market_buy(
            quantity_usd, volatility
        )

        # Store in session state
        st.session_state.cost = net_cost
        st.session_state.fee = fee
        st.session_state.slippage = slippage
        st.session_state.impact = impact

        # Display Output
        with output_placeholder.container():
            st.subheader("💹 Trade Simulation Results")
            st.metric("Net Cost", f"${net_cost:.2f}")
            st.metric("Estimated Fee", f"${fee:.2f}")
            st.metric("Estimated Slippage", f"${slippage:.2f}")
            st.metric("Estimated Market Impact", f"${impact:.2f}")
