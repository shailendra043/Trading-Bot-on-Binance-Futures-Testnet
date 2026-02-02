from binance.um_futures import UMFutures
from binance.error import ClientError
from typing import Any, Dict, Optional
from .config import get_api_keys

BINANCE_TESTNET_URL = "https://testnet.binancefuture.com"

class BinanceApiClient:
    def __init__(self):
        api_key, api_secret = get_api_keys()
        self.client = UMFutures(key=api_key, secret=api_secret, base_url=BINANCE_TESTNET_URL)

    def place_order(self, **kwargs) -> Dict[str, Any]:
        try:
            return self.client.new_order(**kwargs)
        except ClientError as e:
            raise RuntimeError(f"Binance API error: {e.error_message}")

