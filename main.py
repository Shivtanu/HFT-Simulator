import streamlit as st
import asyncio
import threading
from websocket_client import WebSocketClient
from orderbook import OrderBook
from simulator import TradeSimulator
from ui import show_ui

# Session-wide state
if "orderbook" not in st.session_state:
    st.session_state.orderbook = OrderBook()
    st.session_state.simulator = TradeSimulator(st.session_state.orderbook)
    st.session_state.cost = 0
    st.session_state.fee = 0
    st.session_state.running = True

# Input UI
asset, quantity, volatility, fee_tier = show_ui()

output_placeholder = st.empty()

# Callback for every market tick
def handle_data(data):
    st.session_state.orderbook.update(data)
    cost, fee = st.session_state.simulator.simulate_market_buy(quantity)
    st.session_state.cost = cost
    st.session_state.fee = fee

# WebSocket setup
def start_ws():
    uri = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    client = WebSocketClient(uri)
    client.register_callback(handle_data)
    asyncio.run(client.connect())

# Start WebSocket only once
if "ws_thread" not in st.session_state:
    ws_thread = threading.Thread(target=start_ws, daemon=True)
    ws_thread.start()
    st.session_state.ws_thread = ws_thread

# Live output section
while st.session_state.running:
    with output_placeholder.container():
        st.subheader("💹 Trade Simulation Results")
        st.metric("Net Cost", f"${st.session_state.cost:.2f}")
        st.metric("Estimated Fee", f"${st.session_state.fee:.2f}")
    asyncio.sleep(1)  # add small delay to avoid excessive redraw
