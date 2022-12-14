from hftcryptoapi.bitmart.data.constants import *
from datetime import datetime


class WebSocketTickerSpot(object):
    def __init__(self, symbol, last_price, base_volume_24h, high_24h, low_24h, open_24h, s_t):
        self.base_volume_24h = float(base_volume_24h)
        self.high_24h = float(high_24h)
        self.last_price = float(last_price)
        self.low_24h = float(low_24h)
        self.open_24h = float(open_24h)
        self.date_time = datetime.fromtimestamp(s_t)
        self.symbol = symbol


class WebSocketTickerFutures(object):
    def __init__(self, symbol, volume_24, fair_price, last_price, range):
        self.symbol = symbol
        self.volume_24 = float(volume_24)
        self.fair_price = float(fair_price)
        self.last_price = float(last_price)
        self.range = float(range)


class WebSocketKline(object):
    def __init__(self, symbol: str, candle: list, kline_type: Market):
        self.kline_type = kline_type
        self.symbol = symbol
        if kline_type == Market.SPOT:
            idx = 1
            self.date_time = datetime.fromtimestamp(candle[0])
        else:
            idx = 0
            self.date_time = datetime.now()
        self.open = float(candle[idx])
        self.high = float(candle[idx+1])
        self.low = float(candle[idx+2])
        self.close = float(candle[idx+3])
        self.volume = float(candle[idx+4])

    def __str__(self):
        return f"{self.date_time}: {self.open}, {self.high}, {self.low}, {self.close} | {self.volume}"


class WebSocketDepthSpot:
    def __init__(self, symbol: str, asks: list, bids: list, ms_t: float):
        self.date_time = datetime.fromtimestamp(ms_t)
        self.symbol = symbol
        self.asks_price = asks[0]
        self.asks_quantity = asks[1]
        self.bids_price = bids[0]
        self.bids_quantity = bids[1]
        self.best_bid = ""  # TODO: implement
        self.best_ask = ""  # TODO: implement


class WebSocketDepthFutures:
    def __init__(self, symbol: str, way, bids: list, ms_t: float, depths: list):
        self.symbol = symbol
        self.way = WayType.ASK if way == 1 else WayType.BID
        self.date_time = datetime.fromtimestamp(ms_t)
        self.depths = depths


class WebSocketDepthElementFutures:
    def __init__(self, price, volume):
        self.price = float(price)
        self.volume = float(volume)


class WebSocketTrade:
    def __init__(self, symbol, side, price, size, s_t):
        self.symbol = symbol
        self.side = side
        self.price = float(price)
        self.size = float(size)
        self.date_time = datetime.fromtimestamp(s_t)


class WebSocketLogin:
    def __init__(self, event):
        self.event = float(event)


class WebSocketOrderProcess:
    def __init__(self, symbol, order_id, price, size, notional, side, order_type, ms_t, filled_size, filled_notional,
                 margin_trading,
                 trade_order_type, state, last_fill_price, last_fill_count, last_fill_time, exec_type, detail_id,
                 client_order_id):

        self.symbol = symbol
        self.order_id = order_id
        self.price = float(price)
        self.size = float(size)
        self.notional = notional
        self.side = SpotSide.BUY if side == "buy" else SpotSide.SELL
        self.order_type = OrderType.LIMIT if order_type == "limit" else OrderType.MARKET
        self.date_time = datetime.fromtimestamp(ms_t)
        self.filled_size = float(filled_size)
        self.filled_notional = float(filled_notional)
        self.margin_trading = margin_trading
        if int(trade_order_type) == 0:
            self.trade_order_type = TradeOrderType.REGULAR
        elif int(trade_order_type) == 1:
            self.trade_order_type = TradeOrderType.MAKER_ONLY
        elif int(trade_order_type) == 2:
            self.trade_order_type = TradeOrderType.FILL_OR_KILL
        elif int(trade_order_type) == 3:
            self.trade_order_type = TradeOrderType.IMMEDIATE_OR_CANCEL
        if int(state) == 4:
            self.state = OrderState.ORDER_SUCCESS
        elif int(state) == 5:
            self.state = OrderState.PARTIALLY_FILLED
        elif int(state) == 6:
            self.state = OrderState.FULLY_FILLED
        elif int(state) == 8:
            self.state = OrderState.CANCELLED
        self.last_fill_price = float(last_fill_price)
        self.last_fill_count = float(last_fill_count)
        self.last_fill_time = float(last_fill_time)
        self.exec_type = ExecType.MAKER if exec_type == "M" else ExecType.TAKER
        self.detail_id = detail_id
        self.client_order_id = client_order_id


class WebSocketAssetFutures(object):
    def __init__(self, currency, available_balance, position_deposit, frozen_balance):
        self.ticker = currency
        self.available_balance = float(available_balance)
        self.position_deposit = float(position_deposit)
        self.frozen_balance = float(frozen_balance)


class WebSocketPositionFutures(object):
    def __init__(self, symbol, hold_volume, position_type, open_type, frozen_volume, close_volume, hold_avg_price,
                 close_avg_price, open_avg_price, liquidate_price, create_time, update_time):
        self.ticker = symbol
        self.hold_volume = float(hold_volume)
        self.position_type = Position.LONG if position_type == 1 else Position.SHORT
        self.open_type = OrderOpenType.ISOLATED if open_type == 1 else OrderOpenType.CROSS
        self.frozen_volume = float(frozen_volume)
        self.close_volume = float(close_volume)
        self.hold_avg_price = float(hold_avg_price)
        self.close_avg_price = float(close_avg_price)
        self.open_avg_price = float(open_avg_price)
        self.liquidate_price = float(liquidate_price)
        self.create_time = datetime.fromtimestamp(create_time)
        self.update_time = datetime.fromtimestamp(update_time)
