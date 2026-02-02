import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from binance.error import ClientError
from trading_bot.bot.client import BinanceClient
from trading_bot.bot.orders import place_market_order, place_limit_order

# Page Configuration
st.set_page_config(
    page_title="Binance Futures Bot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# CSS for styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #F0B90B;
        color: black;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #D9A505;
        color: black;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

def get_client():
    """Initialize the Binance Client."""
    try:
        return BinanceClient()
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")
        return None

def main():
    st.title("⚡ Binance Futures Testnet Bot")
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    api_key_status = "✅ Found" if os.getenv("BINANCE_API_KEY") else "❌ Missing"
    st.sidebar.info(f"API Key: {api_key_status}")
    
    if st.sidebar.button("Reload Client"):
        st.cache_resource.clear()
        
    client = get_client()

    if not client:
        st.warning("Please configure your API keys in .env file to proceed.")
        return

    # Dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Account Info")
        if st.button("Refresh Account Info"):
            try:
                info = client.get_account_info()
                # Extract USDT Balance
                usdt_balance = next((asset for asset in info['assets'] if asset['asset'] == 'USDT'), None)
                if usdt_balance:
                    st.metric("Wallet Balance (USDT)", f"{float(usdt_balance['walletBalance']):.2f}")
                    st.metric("Available Balance (USDT)", f"{float(usdt_balance['availableBalance']):.2f}")
                else:
                    st.warning("USDT asset not found.")
            except Exception as e:
                st.error(f"Error fetching account info: {e}")

    with col2:
        st.subheader("📝 Place Order")
        with st.form("order_form"):
            symbol = st.text_input("Symbol", value="BTCUSDT")
            side = st.selectbox("Side", ["BUY", "SELL"])
            order_type = st.selectbox("Type", ["MARKET", "LIMIT"])
            quantity = st.number_input("Quantity", min_value=0.001, step=0.001, format="%.3f")
            price = st.number_input("Price (Limit Only)", min_value=0.0, step=0.1, format="%.2f")
            
            submitted = st.form_submit_button("Place Order")
            
            if submitted:
                with st.spinner("Sending order..."):
                    try:
                        if order_type == 'MARKET':
                            resp = place_market_order(client, symbol, side, quantity)
                        else:
                            resp = place_limit_order(client, symbol, side, quantity, price)
                        
                        if resp:
                            st.success(f"Order Placed! ID: {resp.get('orderId')}")
                            st.json(resp)
                        else:
                            st.error("Order failed. Check logs.")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # Divider
    st.markdown("---")
    
    # Logs Viewer
    st.subheader("📜 Recent Logs")
    try:
        if os.path.exists("trading_bot.log"):
            with open("trading_bot.log", "r") as f:
                logs = f.readlines()
                # Show last 20 lines
                for line in logs[-20:]:
                    st.text(line.strip())
        else:
            st.info("No logs found yet.")
    except Exception as e:
        st.error(f"Could not read logs: {e}")

if __name__ == "__main__":
    main()
