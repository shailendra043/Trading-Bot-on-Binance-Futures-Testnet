import argparse
import sys
from trading_bot.bot.client import BinanceClient
from trading_bot.bot.orders import place_market_order, place_limit_order
from trading_bot.bot.logging_config import setup_logging

def main():
    logger = setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Market Order Command
    market_parser = subparsers.add_parser('market', help='Place a Market Order')
    market_parser.add_argument('--symbol', type=str, required=True, help='Trading symbol (e.g., BTCUSDT)')
    market_parser.add_argument('--side', type=str, required=True, choices=['BUY', 'SELL'], help='Order side')
    market_parser.add_argument('--qty', type=float, required=True, help='Order quantity')

    # Limit Order Command
    limit_parser = subparsers.add_parser('limit', help='Place a Limit Order')
    limit_parser.add_argument('--symbol', type=str, required=True, help='Trading symbol (e.g., BTCUSDT)')
    limit_parser.add_argument('--side', type=str, required=True, choices=['BUY', 'SELL'], help='Order side')
    limit_parser.add_argument('--qty', type=float, required=True, help='Order quantity')
    limit_parser.add_argument('--price', type=float, required=True, help='Order price')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        # Initialize Client
        # Note: Ideally API keys are loaded from .env inside BinanceClient
        client = BinanceClient()
        
        if args.command == 'market':
            place_market_order(client, args.symbol, args.side, args.qty)
        elif args.command == 'limit':
            place_limit_order(client, args.symbol, args.side, args.qty, args.price)
            
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
