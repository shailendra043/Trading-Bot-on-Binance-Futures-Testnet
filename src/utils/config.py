import os
from dotenv import load_dotenv
from typing import Tuple

load_dotenv()

def get_api_keys() -> Tuple[str, str]:
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    if not api_key or not api_secret:
        raise ValueError('API key and/or secret not set in environment variables.')
    return api_key, api_secret
