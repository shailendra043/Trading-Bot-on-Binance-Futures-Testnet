from utils.api_client import BinanceApiClient
from utils.validation import validate_symbol, validate_side, validate_quantity, validate_price
from utils.logger import get_logger
from utils.data_loader import get_latest_fear_greed_value
from typing import Optional
import pandas as pd

def place_stop_limit_order(symbol: str, side: str, quantity: float, price: float, stop_price: float, fear_greed_df: Optional[pd.DataFrame] = None, market: bool = False) -> dict:
    """
    Place a stop-limit or stop-market order.
    If market=True, places a stop-market order (no price param, type=STOP_MARKET).
    If market=False, places a stop-limit order (needs price, type=STOP).
    """
    logger = get_logger('stop_limit')
    from utils.validation import round_to_precision
    try:
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        validate_price(stop_price)
        # Hardcoded precision for BTCUSDT: 3 for quantity, 2 for price (can be improved with exchange info)
        qty_prec = 3
        price_prec = 2
        quantity = round_to_precision(quantity, qty_prec)
        stop_price = round_to_precision(stop_price, price_prec)
        if not market:
            price = round_to_precision(price, price_prec)
        client = BinanceApiClient()
        params = {
            'symbol': symbol,
            'side': side.upper(),
            'quantity': quantity,
            'stopPrice': stop_price,
            'recvWindow': 10000
        }
        if market:
            params['type'] = 'STOP_MARKET'
            params['timeInForce'] = 'GTC'
        else:
            validate_price(price)
            params['type'] = 'STOP'
            params['price'] = price
            params['timeInForce'] = 'GTC'
        order = client.place_order(**params)
        fg_value = get_latest_fear_greed_value(fear_greed_df) if fear_greed_df is not None else None
        logger.info({
            'action': 'stop_market_order' if market else 'stop_limit_order',
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price if not market else None,
            'stop_price': stop_price,
            'order_response': order,
            'fear_greed_index': fg_value
        })
        return order
    except Exception as e:
        logger.error({'error': str(e)})
        raise
