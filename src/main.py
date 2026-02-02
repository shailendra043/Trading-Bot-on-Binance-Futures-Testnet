import argparse
import sys
from utils import data_loader, data_analyzer
from utils.logger import get_logger
from utils.validation import ValidationError
from market_orders import place_market_order
from limit_orders import place_limit_order
from advanced.stop_limit import place_stop_limit_order
from advanced.oco import place_oco_order
from advanced.twap import place_twap_order
from advanced.grid_orders import place_grid_orders
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Binance USDT-M Futures Trading Bot")
    parser.add_argument('--fear-greed-file', type=str, help='Path to Fear & Greed Index CSV')
    subparsers = parser.add_subparsers(dest='command')

    # Market order
    market_parser = subparsers.add_parser('market')
    market_parser.add_argument('symbol', type=str)
    market_parser.add_argument('side', type=str)
    market_parser.add_argument('quantity', type=float)

    # Limit order
    limit_parser = subparsers.add_parser('limit')
    limit_parser.add_argument('symbol', type=str)
    limit_parser.add_argument('side', type=str)
    limit_parser.add_argument('quantity', type=float)
    limit_parser.add_argument('price', type=float)

    # Stop-Limit/Stop-Market order
    stop_limit_parser = subparsers.add_parser('stop_limit')
    stop_limit_parser.add_argument('symbol', type=str)
    stop_limit_parser.add_argument('side', type=str)
    stop_limit_parser.add_argument('quantity', type=float)
    stop_limit_parser.add_argument('price', type=float, nargs='?')
    stop_limit_parser.add_argument('stop_price', type=float)
    stop_limit_parser.add_argument('--market', action='store_true', help='Place a stop-market order (omit price)')

    # OCO order
    oco_parser = subparsers.add_parser('oco')
    oco_parser.add_argument('symbol', type=str)
    oco_parser.add_argument('side', type=str)
    oco_parser.add_argument('quantity', type=float)
    oco_parser.add_argument('price', type=float)
    oco_parser.add_argument('stop_price', type=float)
    oco_parser.add_argument('stop_limit_price', type=float)

    # TWAP order
    twap_parser = subparsers.add_parser('twap')
    twap_parser.add_argument('symbol', type=str)
    twap_parser.add_argument('side', type=str)
    twap_parser.add_argument('total_quantity', type=float)
    twap_parser.add_argument('price', type=float)
    twap_parser.add_argument('interval_sec', type=int)
    twap_parser.add_argument('chunks', type=int)

    # Grid Orders
    grid_parser = subparsers.add_parser('grid')
    grid_parser.add_argument('symbol', type=str)
    grid_parser.add_argument('side', type=str)
    grid_parser.add_argument('quantity', type=float)
    grid_parser.add_argument('lower_price', type=float)
    grid_parser.add_argument('upper_price', type=float)
    grid_parser.add_argument('grids', type=int)
    # Analyze trades
    analyze_parser = subparsers.add_parser('analyze_trades')
    analyze_parser.add_argument('csv_path', type=str)

    args = parser.parse_args()
    logger = get_logger('main')
    fg_df = None
    if args.fear_greed_file:
        try:
            fg_df = data_loader.load_fear_greed_index(args.fear_greed_file)
        except Exception as e:
            logger.error({'error': f'Failed to load Fear & Greed Index: {e}'})
            sys.exit(1)

    try:
        if args.command == 'market':
            result = place_market_order(args.symbol, args.side, args.quantity, fg_df)
            print(result)
        elif args.command == 'limit':
            result = place_limit_order(args.symbol, args.side, args.quantity, args.price, fg_df)
            print(result)
        elif args.command == 'analyze_trades':
            metrics = data_analyzer.analyze_trades(args.csv_path)
            print(metrics)
        elif args.command == 'stop_limit':
            # If --market is set, price is not required
            if args.market:
                result = place_stop_limit_order(args.symbol, args.side, args.quantity, 0, args.stop_price, fg_df, market=True)
            else:
                if args.price is None:
                    print('Error: price is required for stop-limit orders (omit for stop-market with --market)')
                    sys.exit(1)
                result = place_stop_limit_order(args.symbol, args.side, args.quantity, args.price, args.stop_price, fg_df, market=False)
            print(result)
        elif args.command == 'oco':
            result = place_oco_order(args.symbol, args.side, args.quantity, args.price, args.stop_price, args.stop_limit_price, fg_df)
            print(result)
        elif args.command == 'twap':
            result = place_twap_order(args.symbol, args.side, args.total_quantity, args.price, args.interval_sec, args.chunks, fg_df)
            print(result)
        elif args.command == 'grid':
            result = place_grid_orders(args.symbol, args.side, args.quantity, args.lower_price, args.upper_price, args.grids, fg_df)
            print(result)
        else:
            parser.print_help()
    except ValidationError as ve:
        logger.error({'error': str(ve)})
        print(f'Validation error: {ve}')
    except Exception as e:
        logger.error({'error': str(e)})
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
