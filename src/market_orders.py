from utils.api_client import BinanceApiClient
from utils.validation import validate_symbol, validate_side, validate_quantity
from utils.logger import get_logger
from utils.data_loader import get_latest_fear_greed_value
from typing import Optional
import pandas as pd

def place_market_order(symbol: str, side: str, quantity: float, fear_greed_df: Optional[pd.DataFrame] = None) -> dict:
    logger = get_logger('market_orders')
    try:
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        client = BinanceApiClient()
        order = client.place_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        fg_value = get_latest_fear_greed_value(fear_greed_df) if fear_greed_df is not None else None
        logger.info({
            'action': 'market_order',
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'order_response': order,
            'fear_greed_index': fg_value
        })
        return order
    except Exception as e:
        logger.error({'error': str(e)})
        raise
