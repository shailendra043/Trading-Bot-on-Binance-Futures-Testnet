from typing import Optional

def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None):
    """
    Validates input parameters for an order.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Order price (required for LIMIT)
        
    Raises:
        ValueError: If any validation fails.
    """
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
        
    if order_type.upper() not in ['MARKET', 'LIMIT', 'STOP_LOSS', 'TAKE_PROFIT']: # Added extras for future
        raise ValueError(f"Invalid order type: {order_type}. Must be MARKET or LIMIT.")
        
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
        
    if order_type.upper() == 'LIMIT':
        if price is None or price <= 0:
            raise ValueError("Price must be greater than 0 for LIMIT orders.")
