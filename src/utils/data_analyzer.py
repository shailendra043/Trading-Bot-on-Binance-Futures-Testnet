import pandas as pd
from typing import Dict, Any

def analyze_trades(csv_path: str) -> Dict[str, Any]:
    import os
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")
    df = pd.read_csv(csv_path)
    col_map = {
        'side': ['side', 'Side'],
        'qty': ['qty', 'Size Tokens', 'size tokens'],
        'price': ['price', 'Execution Price', 'execution price'],
        'fee': ['fee', 'Fee'],
        'pnl': ['pnl', 'Closed PnL', 'closed pnl']
    }
    df_cols_lower = {c.lower(): c for c in df.columns}
    mapped_cols = {}
    for key, aliases in col_map.items():
        found = None
        for alias in aliases:
            if alias.lower() in df_cols_lower:
                found = df_cols_lower[alias.lower()]
                break
        if not found:
            raise ValueError(f"CSV must contain a column for '{key}' (aliases: {aliases})")
        mapped_cols[key] = found
    if df.empty:
        return {}
    side_col = mapped_cols['side']
    qty_col = mapped_cols['qty']
    price_col = mapped_cols['price']
    fee_col = mapped_cols['fee']
    pnl_col = mapped_cols['pnl']
    buy_trades = df[df[side_col].str.upper() == 'BUY']
    sell_trades = df[df[side_col].str.upper() == 'SELL']
    result = {}
    result['num_buy_trades'] = int(len(buy_trades))
    result['num_sell_trades'] = int(len(sell_trades))
    result['avg_buy_price'] = float(buy_trades[price_col].mean()) if not buy_trades.empty else None
    result['avg_sell_price'] = float(sell_trades[price_col].mean()) if not sell_trades.empty else None
    result['total_fees'] = float(df[fee_col].sum())
    result['total_closed_pnl'] = float(df[pnl_col].sum())
    return result
