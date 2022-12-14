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
    def __init__(self, symbol: str, candle: list, market: Market):
        self.market = market
        self.symbol = symbol
        if market == Market.SPOT:
            idx = 1
            self.date_time = datetime.fromtimestamp(candle[0] / 1000)
        else:
            idx = 0
            self.date_time = datetime.now()
        self.open = float(candle[idx])
        self.high = float(candle[idx + 1])
        self.low = float(candle[idx + 2])
        self.close = float(candle[idx + 3])
        self.volume = float(candle[idx + 4])

    def __str__(self):
        return f"{self.date_time}: {self.open}, {self.high}, {self.low}, {self.close} | {self.volume}"


class WebSocketDepthSpot:
    def __init__(self, symbol: str, asks: list, bids: list, ms_t: float):
        self.date_time = datetime.fromtimestamp(ms_t / 1000)
        self.symbol = symbol
        self.asks_price = asks[0]
        self.asks_quantity = asks[1]
        self.bids_price = bids[0]
        self.bids_quantity = bids[1]
        self.best_bid = ""  # TODO: implement
        self.best_ask = ""  # TODO: implement


class WebSocketDepthFutures:
    def __init__(self, symbol: str, way: int, ms_t: float, depths: list):
        self.symbol = symbol
        self.way = WayType(way)
        self.date_time = datetime.fromtimestamp(ms_t / 1000)
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
        self.date_time = datetime.fromtimestamp(s_t/1000)


class WebSocketLogin:
    def __init__(self, event):
        self.event = float(event)


class WebSocketOrderProgress:
    def __init__(self, symbol, order_id, price, size, notional, side, order_type, ms_t, filled_size, filled_notional,
                 margin_trading,
                 trade_order_type, state, last_fill_price, last_fill_count, last_fill_time, exec_type, detail_id,
                 client_order_id):

        self.symbol = symbol
        self.order_id = order_id
        self.price = float(price)
        self.size = float(size)
        self.notional = notional
        self.side = SpotSide(side)
        self.order_type = OrderType(order_type)
        self.date_time = datetime.fromtimestamp(ms_t / 1000)
        self.filled_size = float(filled_size)
        self.filled_notional = float(filled_notional)
        self.margin_trading = margin_trading
        self.trade_order_type = TradeOrderType(trade_order_type)
        self.state = OrderState(state)
        self.last_fill_price = float(last_fill_price)
        self.last_fill_count = float(last_fill_count)
        self.last_fill_time = datetime.fromtimestamp(last_fill_time / 1000)
        self.exec_type = ExecType(exec_type)
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
        self.hold_volume = int(hold_volume)
        self.position_type = Position(position_type)
        self.open_type = OrderOpenType.ISOLATED if open_type == 1 else OrderOpenType.CROSS
        self.frozen_volume = int(frozen_volume)
        self.close_volume = int(close_volume)
        self.hold_avg_price = float(hold_avg_price)
        self.close_avg_price = float(close_avg_price)
        self.open_avg_price = float(open_avg_price)
        self.liquidate_price = float(liquidate_price)
        self.create_time = datetime.fromtimestamp(create_time / 1000)
        self.update_time = datetime.fromtimestamp(update_time / 1000)
