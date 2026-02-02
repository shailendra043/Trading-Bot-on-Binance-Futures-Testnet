from utils.api_client import BinanceApiClient
from utils.validation import validate_symbol, validate_side, validate_quantity, validate_price
from utils.logger import get_logger
from utils.data_loader import get_latest_fear_greed_value
from typing import Optional
import pandas as pd

def place_grid_orders(symbol: str, side: str, quantity: float, lower_price: float, upper_price: float, grids: int, fear_greed_df: Optional[pd.DataFrame] = None) -> dict:
    logger = get_logger('grid_orders')
    try:
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(quantity)
        validate_price(lower_price)
        validate_price(upper_price)
        if grids < 2:
            raise ValueError('Grids must be >= 2')
        fg_value = get_latest_fear_greed_value(fear_greed_df) if fear_greed_df is not None else None
        # Example: Only activate buy grid if F&G < 50, sell grid if > 50
        if (side.upper() == 'BUY' and fg_value is not None and fg_value >= 50) or \
           (side.upper() == 'SELL' and fg_value is not None and fg_value < 50):
            logger.info({'action': 'grid_order_skipped', 'reason': 'F&G index condition not met', 'fear_greed_index': fg_value})
            return {'skipped': True, 'reason': 'F&G index condition not met', 'fear_greed_index': fg_value}
        price_step = (upper_price - lower_price) / (grids - 1)
        client = BinanceApiClient()
        responses = []
        for i in range(grids):
            grid_price = lower_price + i * price_step
            order = client.place_order(
                symbol=symbol,
                side=side.upper(),
                type="LIMIT",
                quantity=quantity,
                price=grid_price,
                timeInForce="GTC"
            )
            logger.info({
                'action': 'grid_order',
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'price': grid_price,
                'grid': i+1,
                'order_response': order,
                'fear_greed_index': fg_value
            })
            responses.append(order)
        return {'orders': responses}
    except Exception as e:
        logger.error({'error': str(e)})
        raise
