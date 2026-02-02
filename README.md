# Simplified Binance Futures Trading Bot

A structured Python application for trading on Binance Futures Testnet (USDT-M).

## Features
- Place Market and Limit orders (BUY/SELL)
- Input validation
- Logging to console and `trading_bot.log`
- CLI interface using `argparse`

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory (or ensure variables are set in your environment):
   ```
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```
   > **Note**: Get your credentials from [Binance Futures Testnet](https://testnet.binancefuture.com).

## Usage

Run the bot using the `trading_bot.cli` module.

### Market Order
Place a market buy order for 0.001 BTC:
```bash
python -m trading_bot.cli market --symbol BTCUSDT --side BUY --qty 0.001
```

### Limit Order
Place a limit sell order for 0.001 BTC at $50,000:
```bash
python -m trading_bot.cli limit --symbol BTCUSDT --side SELL --qty 0.001 --price 50000
```

### UI Dashboard
Launch the visual dashboard:
```bash
streamlit run trading_bot/ui.py
```

### Help
View all available commands:
```bash
python -m trading_bot.cli --help
```

## Logs
Logs are saved to `trading_bot.log` in the project root.

## Structure
- `trading_bot/`: Main package
  - `cli.py`: Command Line Interface entry point
  - `bot/`: Core logic
    - `client.py`: Binance API wrapper
    - `orders.py`: Order placement logic
    - `validators.py`: Input validation
    - `logging_config.py`: Logging setup