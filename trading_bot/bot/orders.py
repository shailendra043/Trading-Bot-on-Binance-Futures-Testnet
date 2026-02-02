import logging
from .client import BinanceClient
from .validators import validate_order_input

logger = logging.getLogger("trading_bot.orders")

def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: float):
    """Places a Market Order."""
    try:
        validate_order_input(symbol, side, 'MARKET', quantity)
        logger.info(f"Placing MARKET {side} order for {quantity} {symbol}...")
        
        response = client.place_order(symbol, side, 'MARKET', quantity)
        
        print("\n=== Order Executed Successfully ===")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        print(f"Avg Price: {response.get('avgPrice')}")
        print("===================================\n")
        return response
        
    except Exception as e:
        logger.error(f"Failed to place MARKET order: {e}")
        print(f"\n[ERROR] Failed to place order: {e}\n")
        return None

def place_limit_order(client: BinanceClient, symbol: str, side: str, quantity: float, price: float):
    """Places a Limit Order."""
    try:
        validate_order_input(symbol, side, 'LIMIT', quantity, price)
        logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} at {price}...")
        
        response = client.place_order(symbol, side, 'LIMIT', quantity, price)
        
        print("\n=== Order Placed Successfully ===")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Price: {response.get('price')}")
        print(f"Orig Qty: {response.get('origQty')}")
        print("=================================\n")
        return response
        
    except Exception as e:
        logger.error(f"Failed to place LIMIT order: {e}")
        print(f"\n[ERROR] Failed to place order: {e}\n")
        return None
