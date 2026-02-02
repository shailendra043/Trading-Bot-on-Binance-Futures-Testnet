# Binance USDT-M Futures Testnet Trading Bot

## Overview
A robust Python CLI bot for trading on Binance USDT-M Futures Testnet. Supports market, limit, stop-limit, TWAP, grid, and OCO (error for unsupported) orders, with full logging, error handling, and bonus features.

## Setup

### 1. Python Environment
- Python 3.8+ recommended.
- Create a virtual environment:
  ```
  python -m venv .venv
  ```
- Activate it:
  - Windows: `.venv\Scripts\activate`
  - macOS/Linux: `source .venv/bin/activate`

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Binance Testnet API
- Register at [Binance Futures Testnet](https://testnet.binancefuture.com/).
- Generate API Key and Secret.
- Copy `.env.example` to `.env` and fill in your credentials, or provide them via CLI.

### 4. Usage

#### Market Order
```
python -m src.main market BTCUSDT BUY 0.01
```

#### Limit Order
```
python -m src.main limit BTCUSDT SELL 0.01 60000
```

#### Stop-Limit Order
```
python -m src.main stop_limit BTCUSDT BUY 0.01 61000 60000
```

#### TWAP Order
```
python -m src.main twap BTCUSDT BUY 0.03 60000 5 3
```

#### Grid Order
```
python -m src.main grid BTCUSDT BUY 0.01 59000 61000 5
```

#### Analyze Trades
```
python -m src.main analyze_trades historical_data.csv
```

- Add `--fear-greed-file fear_greed_index.csv` to use the Fear & Greed Index for advanced strategies.

### 5. Logging
- All API requests, responses, and errors are logged to `bot.log` in the project directory.

## Code Structure
- `src/main.py` — CLI entry point, argument parsing, and user interaction.
- `src/market_orders.py`, `src/limit_orders.py`, `src/advanced/` — Order logic modules.
- `src/utils/` — Utilities for API, logging, validation, config, data loading, and analysis.
- `requirements.txt` — Python dependencies.
- `.env.example` — Example environment variable file.

## Notes
- All orders are placed on the Binance Futures Testnet.
- The bot validates all user input and handles errors gracefully.
- The code is modular, clean, and follows Python best practices.
- For full test coverage, run the test suite in `testing/test_bot.py`.


---
**Author:** CKShetty4

**Assignment:** Proprietary submission for Primetrade.ai internship application, 2025.

**Ownership:** All code, documentation, and logic in this repository are original and created solely by CKShetty4 for the purpose of this assignment. No code is copied from external sources. All rights reserved.

---