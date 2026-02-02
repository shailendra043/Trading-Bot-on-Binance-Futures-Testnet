import pandas as pd
from typing import Optional

def load_fear_greed_index(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if 'timestamp' not in df.columns or 'value' not in df.columns:
        raise ValueError('CSV must contain timestamp and value columns.')
    df = df.sort_values('timestamp')
    return df

def get_latest_fear_greed_value(df: pd.DataFrame) -> Optional[int]:
    if df.empty:
        return None
    return int(df.iloc[-1]['value'])
