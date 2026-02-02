from utils.logger import get_logger
from typing import Optional
import pandas as pd

def place_oco_order(symbol: str, side: str, quantity: float, price: float, stop_price: float, stop_limit_price: float, fear_greed_df: Optional[pd.DataFrame] = None) -> dict:
    logger = get_logger('oco')
    logger.error({'error': 'OCO orders are not supported on Binance USDT-M Futures. This is a spot-only feature.'})
    raise NotImplementedError('OCO orders are not supported on Binance USDT-M Futures. This is a spot-only feature.')
