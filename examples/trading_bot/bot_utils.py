from typing import List

import pandas as pd
from hftcryptoapi.bitmart.data import Kline
from ta.momentum import rsi
from ta.volatility import BollingerBands
from hftcryptoapi.bitmart.data.constants import Position


def to_dataframe(kl: List[Kline]) -> pd.DataFrame:
    data = [dict(timestamp=k.date_time, open=k.open, high=k.high, low=k.low, close=k.close) for k in kl]
    df = pd.DataFrame(data=data, columns=["timestamp", "open", "high", "low", "close"])
    df.set_index("timestamp", inplace=True)
    return df


BB_WINDOW = 20
RSI_WINDOW = 14


def get_indicators(df: pd.DataFrame, rsi_window: int = RSI_WINDOW, bb_window: int = BB_WINDOW):
    df["rsi"] = rsi(df.close, window=rsi_window)
    bb = BollingerBands(df.close, window=bb_window)
    df["bb_upper"] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df.dropna(inplace=True)

    return df


def should_buy(r: pd.Series) -> bool:
    return r.rsi < 30 and r.close < r.bb_lower


def should_sell(r: pd.Series) -> bool:
    return r.rsi > 70 and r.close > r.bb_upper


def get_profit(side: Position, open_price: float, close_price: float):
    if side == Position.SHORT:
        return (open_price - close_price) / open_price * 100
    else:
        return (close_price - open_price) / close_price * 100
