import json
from hftcryptoapi.bitmart.data.constants import *
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union
from hftcryptoapi.bitmart.exceptions import *

class BitmartService():
    def __init__(self, title, service_type, status, start_time, end_time):
        self.title = title
        self.service_type = "Spot API service" if service_type == "spot" else "Contract API service"
        if int(status) == 0:
            self.status = ServiceStatus.WAITING
        elif int(status) == 1:
            self.status = ServiceStatus.WORKING
        elif int(status) == 2:
            self.status = ServiceStatus.COMPLETED
        self.start_time = datetime.fromtimestamp(start_time)
        self.end_time = datetime.fromtimestamp(end_time)


class BitmartOrder(object):
    """
    Represents a request object for buy/sell command.
    Attributes:
    """

    def __init__(self, symbol: str, side: Union[FuturesSide, SpotSide], size: float, price: float, market: Market,
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
        self.price = price
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

        if market == Market.FUTURES:
            if side == SpotSide.BUY or side == SpotSide.SELL:
                raise RequestException("Wrong side for futures market")

            self.leverage = leverage
            self.open_type = open_type
            self.size = int(size)

            self.param = {
                "symbol": self.symbol,
                "side": self.side.value,
                "type": self.order_type.value,
                "leverage": str(self.leverage),
                "open_type": self.open_type.value,
                "size": self.size,
            }
            if self.price is not None:
                self.param['price'] = str(self.price)

        elif market == Market.SPOT:
            if side in FuturesSide:
                raise RequestException("Wrong side for spot market")
            self.leverage = "Spot order: leverage is not applicable"
            self.open_type = "Spot order: open type is not applicable"
            if order_type == OrderType.MARKET:
                if side == SpotSide.SELL:
                    self.notional = ""
                    self.size = size
                    self.param = {
                        'symbol': self.symbol,
                        'side': self.side.value,
                        'type': self.order_type.value,
                        'client_order_id': self.client_order_id,
                        'size': self.size,
                        'notional': self.notional
                    }
                elif side == SpotSide.BUY:
                    self.notional = size
                    self.size = ""
                    self.param = {
                        'symbol': self.symbol,
                        'side': self.side.value,
                        'type': self.order_type.value,
                        'client_order_id': self.client_order_id,
                        'size': "",
                        'notional': self.size
                    }
            elif order_type == OrderType.LIMIT:
                self.notional = ""
                self.size = size
                self.param = {
                    'symbol': self.symbol,
                    'side': self.side.value,
                    'type': self.order_type.value,
                    'client_order_id': self.client_order_id,
                    'size': self.size,
                    'price': self.price
                }

    def __str__(self):
        return f"{self.symbol}_{self.side} {self.size}@{self.price} id: {self.order_id}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class BitmartFee(BaseModel, validate_assignment=True):
    """
    Represents a broker fee.
    Attributes:
    """
    user_rate_type = int
    level = str
    taker_fee_rate_A = float
    maker_fee_rate_A = float
    taker_fee_rate_B = float
    maker_fee_rate_B = float


class BitmartTradeFee(BaseModel, validate_assignment=True):
    """
    Represents a broker's trade fee.
    Attributes:
    """
    symbol = str
    buy_taker_fee_rate = float
    sell_taker_fee_rate = float
    buy_maker_fee_rate = float
    sell_maker_fee_rate = float


class BitmartBatchOrder():
    def __init__(self, bt_orders):
        self.bt_orders = bt_orders


class OrderPosition(object):
    """
    Represents an open long or short position in an asset.
    Attributes:

    """
    def __init__(self, symbol):
        self.symbol: str = symbol
        self.date_time: datetime
        self.current_fee: float
        self.leverage: float
        self.open_date_time: datetime
        self.current_value: float
        self.current_amount: float = 0
        self.mark_price: float
        self.position_value: float
        self.position_cross: float
        self.close_vol: float
        self.close_avg_price: float
        self.current_amount: float
        self.unrealized_value: float
        self.realized_value: float


class MarginAccountSymbol(BaseModel, validate_assignment=True):
    """
    Represents an open long or short position in an asset.
    Attributes:

    """

    symbol = str
    risk_rate = float
    risk_level = float
    buy_enabled = bool
    sell_enabled = bool
    liquidate_price = float
    liquidate_rate = float


"""  def get_margin_acount_balance(self, symbol):
        wallet_currencies = []
        response = self._request_with_params(GET, ACCOUNT_MARGIN_DETAILS, {'symbol': symbol}, Auth.KEYED)
        for ticker in json.loads(response.content)['data']['symbols']:
            self.symbol = symbol
            self.risk_rate = float(ticker["risk_rate"])
            self.risk_level= int(ticker["risk_level"])
            self.buy_enabled = True if ticker["buy_enabled"] == "true" else False
            self.sell_enabled = True if ticker["sell_enabled"] == "true" else False
            self.liquidate_price = float(ticker["liquidate_price"])
            self.liquidate_rate = float(ticker["liquidate_rate"])
             = float(ticker["base"])

    class MarginAccountSymbolBase():
        def __init__(self, currency):
            self.currency = currency
            self.borrow_enabled = False
            self.borrowed = None
            self.borrow_unpaid = None
            self.interest_unpaid = None
            self.available = None
            self.frozen = None
            self.net_asset = None
            self.net_assetBTC = None
            self.total_asset = None
    
    class MarginAccountSymbolQuote():
        def __init__(self, currency):
            self.currency = currency
            self.borrow_enabled = False
            self.borrowed = None
            self.borrow_unpaid = None
            self.interest_unpaid = None
            self.available = None
            self.frozen = None
            self.net_asset = None
            self.net_assetBTC = None
            self.total_asset = None """


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


class CurrencyDetailed(object):
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
        self.date_time = datetime.fromtimestamp(timestamp/1000)
        self.open_interest = None
        self.open_interest_value = None
        self.open_interest_datetime = None
        self.funding_rate = None
        self.funding_rate_datetime = None

    def __str__(self):
        return f"{self.symbol}: {self.last_price} ({self.base_volume_24h}"


class TickerWebSocket(object):
    def __init__(self, symbol, last_price, volume_24, fair_price, range):
        self.volume_24 = float(volume_24)
        self.fair_price = float(fair_price)
        self.last_price = float(last_price)
        self.range = float(range)
        self.symbol = symbol

    def __str__(self):
        return f'{self.symbol}: {self.last_price}'


class BitmartWallet(object):
    def __init__(self, currencies):
        self.currencies = currencies

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Kline(object):
    def __init__(self, timestamp, open, high, low, close,  volume, last_price=None,
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
        self.price = asks
        self.price = bids
        self.quantity = datetime.fromtimestamp(timestamp)


class BitmartTrade(object):
    def __init__(self, amount: float, order_time: int, price: float, count: float, bt_type: str):
        self.amount = amount
        self.order_time = order_time
        self.price = price
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
        self.volume_precision = vol_precision
        self.price_precision = price_precision
        self.max_volume = max_volume
        self.min_volume = min_volume
        self.contract_size = contract_size
        self.index_price = index_price
        self.index_name = index_name
        self.min_leverage = min_leverage
        self.max_leverage = max_leverage
        self.turnover_24h = turnover_24h
        self.volume_24h = volume_24h
        self.last_price = last_price
        self.open_date_time = datetime.fromtimestamp(open_timestamp/1000)
        self.expire_date_time = datetime.fromtimestamp(expire_timestamp/1000)
        self.settle_date_time = datetime.fromtimestamp(settle_timestamp/1000)
