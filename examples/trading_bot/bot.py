import pandas as pd
from hftcryptoapi import BitmartClient
from hftcryptoapi.bitmart.data import *
from datetime import datetime, timedelta
from typing import Optional, List, Any, Union

from bot_utils import to_dataframe, get_indicators, should_buy, should_sell, get_profit, BB_WINDOW
from config import *


class TradingBot(object):
    def __init__(self, symbol: str, contract_size: int):
        self.client = BitmartClient(API_KEY, SECRET_KEY, MEMO)
        self.candles = pd.DataFrame()
        self.symbol = symbol
        self.contract_size = contract_size
        self.position_side: Optional[Position] = None
        self.profit: float = 0

    def preload(self):
        to_time = datetime.now()
        from_time = to_time - timedelta(hours=BB_WINDOW+1)
        klines = self.client.get_symbol_kline(symbol=self.symbol, market=Market.FUTURES, tf=TimeFrame.tf_1h,
                                              from_time=from_time, to_time=to_time)

        self.candles = get_indicators(to_dataframe(klines))

    def start(self):
        print("Starting bot...")
        self.preload()
        self.client.subscribe_public(market=Market.FUTURES, symbols=[self.symbol],
                                     channels=[BtFuturesSocketKlineChannels.K_LINE_CHANNEL_1HOUR])
        self.client.subscribe_private(market=Market.FUTURES, channels=[BtFuturesTPrivatePositionChannel])

        self.client.start_websockets(market=Market.FUTURES, on_message=self._on_message)

    def open(self, side: Position):
        print(f"Open position {side}")
        order_side = FuturesSide.BUY_OPEN_LONG if side == Position.LONG else FuturesSide.SELL_OPEN_SHORT
        self.client.submit_order(symbol=self.symbol, market=Market.FUTURES, order_type=OrderType.MARKET,
                                 size=self.contract_size, open_type=OrderOpenType.CROSS, side=order_side)

        self.position_side = side

    def close(self):
        print(f"Close position {self.position_side}")
        order_side = FuturesSide.SELL_CLOSE_LONG if self.position_side == Position.LONG else FuturesSide.BUY_CLOSE_SHORT
        self.client.submit_order(symbol=self.symbol, market=Market.FUTURES, order_type=OrderType.MARKET,
                                 size=self.contract_size, open_type=OrderOpenType.CROSS, side=order_side)

        self.position_side = None

    def trade_decision(self):
        row = self.candles.iloc[-1]
        print(f"rsi: {row.rsi} bb: {row.bb_upper} | {row.close} | {row.bb_lower}")

        if should_buy(row) and self.position_side != Position.LONG:
            if self.position_side is None:
                self.open(Position.LONG)
            else:
                self.close()
        elif should_sell(row) and self.position_side != Position.SHORT:
            if self.position_side is None:
                self.open(Position.SHORT)
            else:
                self.close()

    def _on_message(self, msg: Union[WebSocketKline, WebSocketPositionFutures]):
        if type(msg) is WebSocketKline:
            self.trade_decision()
            if self.candles.index[-1] < msg.date_time:
                self.preload()
        else:
            print(f"Position {msg.open_avg_price} [{msg.volume}]")
            if msg.volume == 0:
                profit = get_profit(msg.position_type, msg.open_avg_price, msg.close_avg_price)
                print("POSITION CLOSED: %.3f" % profit)
                self.profit += profit

    def stop(self):
        print("Total profit is %.3f" % self.profit)
        self.client.stop_websockets(market=Market.FUTURES)
        pass


bot = TradingBot(symbol="BTCUSDT", contract_size=5)
bot.start()
input("Press any key to exit...\r")
bot.stop()