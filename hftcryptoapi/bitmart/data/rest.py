import json
from hftcryptoapi.bitmart.data.constants import *
from datetime import datetime
from typing import Optional, Union
from hftcryptoapi.bitmart.exceptions import *
from typing import List


class BitmartService:
    def __init__(self, title, service_type, status, start_time, end_time):
        self.title = title
        self.service_type = service_type
        self.status = ServiceStatus(int(status))
        self.start_time = datetime.fromtimestamp(start_time / 1000)
        self.end_time = datetime.fromtimestamp(end_time / 1000)


class BitmartOrder(object):
    """
    Represents a request object for buy/sell command.
    Attributes:
    """

    def __init__(self, symbol: str, side: Optional[Union[FuturesSide, SpotSide]] = None,
                 size: float = 0, price: Optional[float] = None,
                 market: Market = Market.SPOT,
                 order_type: OrderType = OrderType.LIMIT,
                 leverage: int = 1,
                 open_type=OrderOpenType.ISOLATED, client_order_id: Optional[str] = "", order_id: Optional[str] = "",
                 create_time: int = 0):
        super().__init__()
        self.symbol = symbol
        self.side = side
        if create_time != 0:
            self.create_time = datetime.fromtimestamp(create_time)

        self.order_type = order_type
        self.price = float(price) if price is not None else None
        self.client_order_id = client_order_id
        self.market = market
        self.order_id = order_id
        self.filled_notional = 0
        self.filled_size = 0
        self.order_status = None
        self.price_avg = None
        self.order_mode = OrderMode.SPOT
        self.update_time = None
        self.unfilled_volume = None
        # futures
        self.leverage = None
        self.open_type = None
        param = {"symbol": self.symbol,
                 "side": self.side.value,
                 "type": self.order_type.value}
        if market == Market.FUTURES:
            if side is SpotSide:
                raise RequestException("Wrong side for futures market")

            self.leverage = leverage
            self.open_type = open_type
            self.size = int(size)

            self.param = {
                **param,
                "leverage": str(self.leverage),
                "open_type": self.open_type.value,
                "size": size,
            }
            if self.price is not None:
                self.param['price'] = str(self.price)

        elif market in [Market.SPOT, Market.SPOT_MARGIN]:
            if side in FuturesSide:
                raise RequestException("Wrong side for spot market")

            param['client_order_id'] = self.client_order_id

            if order_type == OrderType.MARKET:
                if side == SpotSide.SELL:
                    self.notional = ""
                    self.size = float(size)
                    self.param = {
                        **param,
                        'size': str(self.size),
                        'notional': str(self.notional)
                    }
                elif side == SpotSide.BUY:
                    self.notional = size
                    self.size = ""
                    self.param = {
                        **param,
                        'size': "",
                        'notional': str(self.notional)
                    }
            elif order_type == OrderType.LIMIT:
                self.notional = ""
                self.size = float(size)
                self.param = {
                    **param,
                    'size': str(self.size),
                    'price': str(self.price)
                }

    def __str__(self):
        return f"{self.market.name}_{self.symbol}_{self.side.name} " \
               f"{self.size or self.notional}@{self.price or self.price_avg} id: {self.order_id}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class BitmartFee(object):
    """
    Represents a broker fee.
    Attributes:
    """

    def __init__(self):
        self.user_rate_type: int
        self.level: str
        self.taker_fee_rate_A: float
        self.maker_fee_rate_A: float
        self.taker_fee_rate_B: float
        self.maker_fee_rate_B: float


class BitmartTradeFee(object):
    """
    Represents a broker's trade fee.
    Attributes:
    """

    def __init__(self, symbol: str):
        self.symbol: str = symbol
        self.buy_taker_fee_rate: float
        self.sell_taker_fee_rate: float
        self.buy_maker_fee_rate: float
        self.sell_maker_fee_rate: float


class BitmartBatchOrder:
    def __init__(self, bt_orders):
        self.bt_orders = bt_orders


class OrderPosition(object):
    """
    Represents an open long or short position in an asset.
    Attributes:

    """

    def __init__(self, symbol, leverage, current_fee, current_value,
                 mark_price, position_value, position_cross, close_vol, close_avg_price, current_amount,
                 unrealized_value, realized_value, timestamp, open_timestamp):
        self.symbol: str = symbol
        self.timestamp = datetime.fromtimestamp(int(timestamp) / 1000)
        self.current_fee: float = float(current_fee)
        self.leverage: float = float(leverage)
        self.open_timestamp: datetime = datetime.fromtimestamp(int(open_timestamp) / 1000)
        self.current_value: float = float(current_value)
        self.mark_price: float = float(mark_price)
        self.position_value: float = float(position_value)
        self.position_cross: float = float(position_cross)
        self.close_vol: float = float(close_vol)
        self.close_avg_price: float = float(close_avg_price)
        self.current_amount: float = int(current_amount)
        self.unrealized_value: float = float(unrealized_value)
        self.realized_value: float = float(realized_value)


class MarginWalletItem(object):
    """
    Represents an open long or short position in an asset.
    Attributes:

    """

    def __init__(self, symbol: str):
        self.symbol: str = symbol
        self.risk_rate: float
        self.risk_level: float
        self.buy_enabled: bool
        self.sell_enabled: bool
        self.liquidate_price: float
        self.liquidate_rate: float
        self.base = {}
        self.quote = {}


class BitmartCurrency(object):
    """
    Represents an open long or short position in an asset.
    Attributes:

    """

    ticker = str
    name = str
    contract_address = Optional[str]
    network = Optional[str]
    withdraw_enabled = bool
    deposit_enabled = bool
    withdraw_minsize = float
    withdraw_minfee = float


class WalletItem(object):
    def __init__(self, symbol, available, frozen, position_deposit="", equity="", unrealized="",
                 wallet_type=Market.SPOT):
        self.symbol = symbol
        self.available = available
        self.frozen = frozen
        self.wallet_type = wallet_type
        if wallet_type == Market.FUTURES:
            self.position_deposit = position_deposit
            self.equity = equity
            self.unrealized = unrealized
        else:
            self.position_deposit = "Only for futures account"
            self.equity = "Only for futures account"
            self.unrealized = "Only for futures account"

    def __str__(self):
        return f'{self.symbol}[{self.wallet_type.value}] {self.available}/{self.frozen}'


class Currency(object):
    def __init__(self, id, name, withdraw_enabled, deposit_enabled):
        self.id = id
        self.name = name
        self.withdraw_enabled = withdraw_enabled
        self.deposit_enabled = deposit_enabled

    def __str__(self):
        return self.id + ": " + self.name


class SpotTickerDetails(object):
    def __init__(self, symbol, last_price, quote_volume_24h, base_volume_24h, high_24h,
                 low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid, best_bid_size,
                 fluctuation, timestamp, url):
        self.symbol = symbol
        self.last_price = last_price
        self.quote_volume_24h = quote_volume_24h
        self.base_volume_24h = base_volume_24h
        self.high_24h = high_24h
        self.low_24h = low_24h
        self.open_24h = open_24h
        self.close_24h = close_24h
        self.best_ask = best_ask
        self.best_ask_size = best_ask_size
        self.best_bid = best_bid
        self.best_bid_size = best_bid_size
        self.fluctuation = fluctuation
        self.date_time = datetime.fromtimestamp(timestamp / 1000)
        self.funding_rate = None
        self.funding_rate_datetime = None

    def __str__(self):
        return f"{self.symbol}: {self.last_price} ({self.base_volume_24h})"


class FuturesOpenInterest(object):
    def __init__(self, timestamp, symbol, open_interest, open_interest_value):
        self.symbol = symbol
        self.timestamp = datetime.fromtimestamp(timestamp / 1000)
        self.open_interest = float(open_interest)
        self.open_interest_value = float(open_interest_value)


class FuturesFundingRate(object):
    def __init__(self, timestamp, symbol, rate_value):
        self.symbol = symbol
        self.timestamp = datetime.fromtimestamp(timestamp / 1000)
        self.rate_value = float(rate_value)


class TickerFuturesWebSocket(object):
    def __init__(self, symbol, last_price, volume_24, fair_price, range):
        self.volume_24 = float(volume_24)
        self.fair_price = float(fair_price)
        self.last_price = float(last_price)
        self.range = float(range)
        self.symbol = symbol

    def __str__(self):
        return f"{self.symbol}: {self.last_price} ({self.volume_24})"


class TickerSpotWebSocket(object):
    def __init__(self, symbol, last_price, open_24h, high_24h, low_24h, base_volume_24h, s_t):
        self.open_24h = float(open_24h)
        self.high_24h = float(high_24h)
        self.low_24h = float(low_24h)
        self.base_volume_24h = float(base_volume_24h)
        self.last_price = float(last_price)
        self.timestamp = datetime.fromtimestamp(s_t)
        self.symbol = symbol

    def __str__(self):
        return f'{self.symbol}: {self.last_price}'


class BitmartWallet(object):
    def __init__(self, items):
        self.items: List[Union[WalletItem, MarginWalletItem]] = items

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Kline(object):
    def __init__(self, timestamp, open, high, low, close, volume, last_price=None,
                 quote_volume="", market=Market.SPOT):
        self.date_time = datetime.fromtimestamp(timestamp)
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.last_price = float(last_price) if market == Market.SPOT else "Not applied for FUTURES"
        self.volume = float(volume)
        self.quote_volume = float(quote_volume) if market == Market.SPOT else "Not applied for FUTURES"

    def __str__(self):
        return f"{self.date_time}: {self.open}, {self.high}, {self.low}, {self.close} | {self.volume}"


class BitmartSpotBuySells(object):
    def __init__(self, amount, total, price, count):
        self.amount = float(amount)
        self.total = float(total)
        self.price = float(price)
        self.count = float(count)


class BitmartFuturesAskBids(object):
    def __init__(self, price, quantity, quantity_above):
        self.price = float(price)
        self.quantity = float(quantity)
        self.quantity_above = float(quantity_above)


class BitmartDepth(object):
    def __init__(self, asks, bids, timestamp):
        self.asks = asks
        self.bids = bids
        self.timestamp = datetime.fromtimestamp(timestamp / 1000)


class BitmartTrade(object):
    def __init__(self, amount: float, order_time: int, price: float, count: float, bt_type: str):
        self.amount = amount
        self.order_time = order_time
        self.price = float(price)
        self.count = count
        self.bt_type = bt_type


class BitmartFutureContract(object):
    def __init__(self, symbol, product_type, base_currency, quote_currency, vol_precision, price_precision,
                 max_volume, min_volume,
                 contract_size, index_price, index_name, min_leverage, max_leverage, turnover_24h,
                 volume_24h, last_price,
                 open_timestamp, expire_timestamp, settle_timestamp):
        self.symbol = symbol
        self.product_type = FuturesContractType.PERPETUAL if int(product_type) == 1 else FuturesContractType.FUTURES
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.volume_precision = float(vol_precision)
        self.price_precision = float(price_precision)
        self.max_volume = float(max_volume)
        self.min_volume = float(min_volume)
        self.contract_size = float(contract_size)
        self.index_price = float(index_price)
        self.index_name = index_name
        self.min_leverage = min_leverage
        self.max_leverage = max_leverage
        self.turnover_24h = turnover_24h
        self.volume_24h = volume_24h
        self.last_price = last_price
        self.open_date_time = datetime.fromtimestamp(open_timestamp / 1000)
        self.expire_date_time = datetime.fromtimestamp(expire_timestamp / 1000)
        self.settle_date_time = datetime.fromtimestamp(settle_timestamp / 1000)


class BitmartSpotSymbolDetails(object):
    def __init__(self, symbol, symbol_id, base_currency, quote_currency, quote_increment, base_min_size,
                 price_min_precision, price_max_precision,
                 expiration, min_buy_amount, min_sell_amount, trade_status):
        self.symbol = symbol
        self.symbol_id = symbol_id
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.quote_increment = float(quote_increment)
        self.base_min_size = float(base_min_size)
        self.price_min_precision = int(price_min_precision)
        self.price_max_precision = int(price_max_precision)
        self.expiration = expiration
        self.min_buy_amount = float(min_buy_amount)
        self.min_sell_amount = float(min_sell_amount)
        self.trade_status = trade_status


class BorrowRecord(object):
    def __init__(self, borrow_id, symbol, currency,
                 borrow_amount, daily_interest, hourly_interest, interest_amount, create_time, **kwargs):
        self.borrow_id: str = borrow_id
        self.currency: str = currency
        self.symbol: str = symbol
        self.borrow_amount = float(borrow_amount)
        self.daily_interest = float(daily_interest)
        self.hourly_interest = float(hourly_interest)
        self.interest_amount = float(interest_amount or 0)
        self.create_time = datetime.fromtimestamp(create_time / 1000)


class RepayRecord(object):
    def __init__(self, repay_id, repay_time, currency, repaid_amount, repaid_principal, repaid_interest, **kwargs):
        self.repay_id: str = repay_id
        self.repay_time: datetime = datetime.fromtimestamp(repay_time / 1000)
        self.currency: str = currency
        self.repaid_amount = float(repaid_amount)
        self.repaid_principal = float(repaid_principal)
        self.repaid_interest = float(repaid_interest)


class BorrowingRateItem(object):
    def __init__(self, currency: str, daily_interest, hourly_interest, max_borrow_amount, min_borrow_amount,
                 borrowable_amount):

        self.currency = currency
        self.daily_interest = float(daily_interest)
        self.hourly_interest = float(hourly_interest)
        self.max_borrow_amount = float(max_borrow_amount)
        self.min_borrow_amount = float(min_borrow_amount)
        self.borrowable_amount = float(borrowable_amount)


class BorrowingRateAndAmount(object):
    def __init__(self, symbol, max_leverage, symbol_enabled, base, quote):
        self.symbol: str = symbol
        self.max_leverage: int = int(max_leverage)
        self.symbol_enabled = bool(symbol_enabled)
        self.base: BorrowingRateItem = BorrowingRateItem(**base)
        self.quote: BorrowingRateItem = BorrowingRateItem(**quote)
