import json 
from .constants import *
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Optional, List, Union

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
        self.start_time = datetime.datetime.fromtimestamp(start_time)
        self.end_time = datetime.datetime.fromtimestamp(end_time)

class BitmartOrder(BaseModel, validate_assignment=True):

    """
    Represents a request object for buy/sell command.
    Attributes:
    """



    def __init__(self, market, symbol:str, side:str, size:str, price:float, order_type=OrderType.LIMIT, leverage=1,
                 open_type=OrderOpenType.ISOLATED, client_order_id="", order_id="", create_time="0"):
        self.symbol = symbol
        self.side = side
        if create_time != 0: self.create_time = datetime.datetime.fromtimestamp(create_time)
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
                return "Wrong side for futures market"
            
            self.leverage = leverage
            self.open_type = open_type
            self.size = size

            self.param = {
            "symbol": self.symbol,
            "side": self.side,
            "type": self.order_type.value,
            "leverage": self.leverage,
            "open_type": self.open_type.value,
            "size": self.size,
            "price": self.price
            }
            
        elif market == Market.SPOT:
            if side in FuturesSide:
                return "Wrong side for spot market"
            self.leverage = "Spot order: leverage is not applicable"
            self.open_type = "Spot order: open type is not applicable"
            if order_type == OrderType.MARKET:
                if side == SpotSide.SELL:
                    self.notional = ""
                    self.size = size
                    self.param = {
                        'symbol': self.symbol,
                        'side': self.side,
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
                        'side': self.side,
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
                    'side': self.side,
                    'type': self.order_type.value,
                    'client_order_id': self.client_order_id,
                    'size': self.size,
                    'price': self.price
                }

    
    def __str__(self):
        return self.symbol + ": " + self.bt_type

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
    buy_taker_fee_rate  = float
    sell_taker_fee_rate = float
    buy_maker_fee_rate  = float
    sell_maker_fee_rate = float


class BitmartBatchOrder():
    def __init__(self, bt_orders):
        self.bt_orders = bt_orders

class OrderPosition(BaseModel, validate_assignment=True):
    """
    Represents an open long or short position in an asset.
    Attributes:

    """

    symbol = str
    date_time = datetime
    current_fee = float
    leverage = float
    open_date_time = datetime
    current_value = float
    mark_price = float
    position_value = float
    position_cross = float
    close_vol = float
    close_avg_price = float
    current_amount = float
    unrealized_value = float
    realized_value = float

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


class BitmartCurrency():
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


class WalletItem():
    def __init__(self, symbol, available, frozen, position_deposit="", equity="", unrealized="", wallet_type=Market.SPOT):
        self.symbol = symbol
        self.available = available
        self.frozen = frozen
        self.wallet_type = wallet_type
        if wallet_type == Market.FUTURES:
            self.position_deposit=position_deposit
            self.equity=equity
            self.unrealized=unrealized
        else:
            self.position_deposit="Only for futures account"
            self.equity="Only for futures account"
            self.unrealized="Only for futures account"

    def __str__(self):
        return self.ticker + ": " + self.name

class Currency():
    def __init__(self, id, name, withdraw_enabled, deposit_enabled):
        self.id = id
        self.name = name
        self.withdraw_enabled = withdraw_enabled
        self.deposit_enabled = deposit_enabled

    def __str__(self):
        return self.id + ": " + self.name

class CurrencyDetailed():
    def __init__(self, symbol, last_price, quote_volume_24h, base_volume_24h, high_24h,
                 low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid, best_bid_size,
                 fluctuation, timestamp):
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
        self.date_time = datetime.datetime.fromtimestamp(timestamp)
        self.open_interest = None
        self.open_interest_value = None
        self.open_interest_datetime = None
        self.funding_rate = None
        self.funding_rate_datetimem = None

    def __str__(self):
        return self.id + ": " + self.name

class CurrencyWebSocket():
    def __init__(self, symbol, last_price, base_volume_24h, high_24h, low_24h, open_24h, s_t):
        self.base_volume_24h = float(base_volume_24h)
        self.high_24h = float(high_24h)
        self.last_price = float(last_price)
        self.low_24h = float(low_24h)
        self.open_24h = float(open_24h)
        self.date_time = datetime.datetime.fromtimestamp(s_t)
        self.symbol =  symbol

    def __str__(self):
        return self.id + ": " + self.name

class BitmartWallet():
    def __init__(self, currencies):
        self.currencies = currencies

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Kline():
    def __init__(self, timestamp, open, high, low, close, last_price,
                       volume, quote_volume="", market=Market.SPOT):
        self.date_time = datetime.datetime.fromtimestamp(timestamp)
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.last_price = float(last_price) if market == Market.SPOT else "Not applied for FUTURES"
        self.volume = float(volume)
        self.quote_volume = float(quote_volume) if market == Market.SPOT else "Not applied for FUTURES"

class BitmartSpotBuySells():
    def __init__(self, amount, total, price, count, bt_type:str):
        self.amount = float(amount)
        self.total = float(total)
        self.price = float(price)
        self.count = float(count)

class BitmartFuturesAskBids():
    def __init__(self, price, quantity, quantity_above):
        self.price = float(price)
        self.quantity  = float(quantity)
        self.quantity_above = float(quantity_above)

class BitmartFutureDepth():
    def __init__(self, asks, bids, timestamp):
        self.price = asks
        self.price = bids
        self.quantity  = datetime.datetime.fromtimestamp(timestamp)
    
class BitmartSpotDepth():
    def __init__(self, buys, sells, timestamp):
        self.buys = buys
        self.sells = sells
        self.quantity  = datetime.datetime.fromtimestamp(timestamp)

class BitmartTrade():
    def __init__(self, amount:float, order_time:int, price:float, count:float, bt_type:str):
        self.amount = amount
        self.order_time = order_time
        self.price = price
        self.count = count
        self.bt_type = bt_type

class BitmartFutureContract():
    def __init__(self, symbol, product_type, base_currency, quote_currency, volume_precision, price_precision, max_volume, min_volume,
                 funding_rate, contract_size, index_price, index_name, min_leverage, max_leverage, turnover_24h, volume_24h, last_price,
                 open_timestamp, expire_timestamp, settle_timestamp):
        self.symbol = symbol
        self.product_type = FuturesContractType.PERPETUAL if int(product_type) == 1 else FuturesContractType.FUTURES
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.volume_precision = volume_precision
        self.price_precision = price_precision
        self.max_volume = max_volume
        self.min_volume = min_volume
        self.funding_rate = funding_rate
        self.contract_size = contract_size
        self.index_price = index_price
        self.index_name = index_name
        self.min_leverage = min_leverage
        self.max_leverage = max_leverage
        self.turnover_24h = turnover_24h
        self.volume_24h = volume_24h
        self.last_price = last_price
        self.open_date_time = datetime.datetime.fromtimestamp(open_timestamp)
        self.expire_date_time = datetime.datetime.fromtimestamp(expire_timestamp)
        self.settle_date_time = datetime.datetime.fromtimestamp(settle_timestamp)