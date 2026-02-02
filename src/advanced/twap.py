from utils.api_client import BinanceApiClient
from utils.validation import validate_symbol, validate_side, validate_quantity, validate_price
from utils.logger import get_logger
from utils.data_loader import get_latest_fear_greed_value
from typing import Optional
import pandas as pd
import time

def place_twap_order(symbol: str, side: str, total_quantity: float, price: float, interval_sec: int, chunks: int, fear_greed_df: Optional[pd.DataFrame] = None) -> dict:
    logger = get_logger('twap')
    try:
        validate_symbol(symbol)
        validate_side(side)
        validate_quantity(total_quantity)
        validate_price(price)
        if chunks < 1:
            raise ValueError('Chunks must be >= 1')
        fg_value = get_latest_fear_greed_value(fear_greed_df) if fear_greed_df is not None else None
        # Conditional logic based on Fear & Greed Index
        if fg_value is not None:
            if side.upper() == 'BUY' and fg_value < 30:
                total_quantity *= 1.1  # Increase buy size in fear
                interval_sec = max(1, interval_sec - 2)
            elif side.upper() == 'SELL' and fg_value > 70:
                total_quantity *= 1.1  # Increase sell size in greed
                interval_sec = max(1, interval_sec - 2)
        chunk_qty = total_quantity / chunks
        client = BinanceApiClient()
        responses = []
        for i in range(chunks):
            order = client.place_order(
                symbol=symbol,
                side=side.upper(),
                type="LIMIT",
                quantity=chunk_qty,
                price=price,
                timeInForce="GTC"
            )
            logger.info({
                'action': 'twap_order_chunk',
                'symbol': symbol,
                'side': side,
                'quantity': chunk_qty,
                'price': price,
                'chunk': i+1,
                'order_response': order,
                'fear_greed_index': fg_value
            })
            responses.append(order)
            if i < chunks - 1:
                time.sleep(interval_sec)
        return {'orders': responses}
    except Exception as e:
        logger.error({'error': str(e)})
        raise
