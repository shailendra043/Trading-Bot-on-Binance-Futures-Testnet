from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class BinanceClient:
    def __init__(self):
        self.logger = logging.getLogger("trading_bot.client")
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        
        if not api_key or not api_secret:
            self.logger.warning("API keys not found in environment variables. Functionality may be limited.")
            
        # Initialize client for Testnet
        try:
            self.client = Client(api_key, api_secret, testnet=True)
            self.logger.info("Binance Client initialized on Testnet.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance Client: {e}")
            raise

    def get_account_info(self):
        """Retrieves account information."""
        try:
            return self.client.futures_account()
        except BinanceAPIException as e:
            self.logger.error(f"Binance API Error in get_account_info: {e}")
            raise
        except BinanceRequestException as e:
            self.logger.error(f"Binance Request Error in get_account_info: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """
        Places an order on Binance Futures Testnet.
        """
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders.")
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good Till Cancelled
                
            self.logger.info(f"Sending order request: {params}")
            response = self.client.futures_create_order(**params)
            self.logger.info(f"Order response: {response}")
            return response
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API Error placing order: {e}")
            raise
        except BinanceRequestException as e:
            self.logger.error(f"Binance Request Error placing order: {e}")
            raise
