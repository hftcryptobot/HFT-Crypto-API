# Endpoint URL constants for API
# Changelog:
# 26/11/2022 First version

from enum import Enum, EnumMeta, unique

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True   


""" Base urls for API endpoints """
# Domain constants
API_URL = 'https://api-cloud.bitmart.com'
WS_URL = 'wss://ws-manager-compress.bitmart.com/api?protocol=1.1'
WS_URL_USER = 'wss://ws-manager-compress.bitmart.com/user?protocol=1.1'
CONTRACT_WS_URL = 'wss://openapi-ws.bitmart.com/api?protocol=1.1'
CONTRACT_WS_URL_USER = 'wss://openapi-ws.bitmart.com/user?protocol=1.1'

# http headers
CONTENT_TYPE = 'Content-Type'
USER_AGENT = 'User-Agent'
X_BM_KEY = 'X-BM-KEY'
X_BM_SIGN = 'X-BM-SIGN'
X_BM_TIMESTAMP = 'X-BM-TIMESTAMP'
APPLICATION_JSON = 'application/json'
GET = "GET"
POST = "POST"
DELETE = "DELETE"
VERSION = "0.1"

# connection timeout, read timeout
TIMEOUT = (5, 10)

# 1 Spot Market API
# System Status
SYSTEM_TIME = "/system/time"
SERVICE_STATUS = "/system/service"

# Public Market Data
SPOT_CURRENCY_LIST = "/spot/v1/currencies"
SPOT_TRADING_PAIRS_LIST = "/spot/v1/symbols"
SPOT_TRADING_PAIRS_DETAILS = "/spot/v1/symbols/details"
SPOT_TICKER = "/spot/v2/ticker"
SPOT_TICKER_DETAILS = "/spot/v1/ticker_detail"
SPOT_K_LIE_STEP = "/spot/v1/steps"
SPOT_K_LINE = "/spot/v1/symbols/kline"
SPOT_BOOK_DEPTH = "/spot/v1/symbols/book"
SPOT_RECENT_TRADES = "/spot/v1/symbols/trades"

# Sub-Account Data
MAIN_ACCOUNT_SPOT_ASSET = "/account/sub-account/main/v1/sub-to-main"
SUB_ACCOUNT_SPOT_ASSET_TRANSFER = "/account/sub-account/sub/v1/sub-to-main"
MAIN_ACCOUNT_SPOT_ASSET_TRANSFER = "/account/sub-account/main/v1/main-to-sub"
SUB_ACCOUNT_SUB2SUB_SPOT_ASSET_TRANSFER = "/account/sub-account/sub/v1/sub-to-sub"
MAIN_ACCOUNT_SUB2SUB_SPOT_ASSET_TRANSFER = "/account/sub-account/main/v1/sub-to-sub"
MAIN_ACCOUNT_TRANSFER_LIST = "/account/sub-account/main/v1/transfer-list"
ACCOUNT_TRANSFER_HISTORY = "/account/sub-account/v1/transfer-history"
SUB_ACCOUNT_BALANCE = "/account/sub-account/main/v1/wallet"
ALL_SUB_ACCOUNTS_LIST = "/account/sub-account/main/v1/subaccount-list"

## Funding Account Data
ACCOUNT_BALANCE = "/account/v1/wallet"
ACOUNT_ALL_CURRENCIES = "/account/v1/currencies"
ACCOUNT_SPOT_BALANCE = "/spot/v1/wallet"
ACCOUNT_DEPOSIT_ADDRESS = "/account/v1/deposit/address"
ACCOUNT_WITHDRAW_QUOTA = "/account/v1/withdraw/charge"
ACCOUNT_WITHDRAW = "/account/v1/withdraw/apply"
ACCOUNT_WITHDRAW_DEPOSIT_HISTORY = "/account/v2/deposit-withdraw/history"
ACCOUNT_DEPOSIT_WITHDRAW_DETAILS = "/account/v1/deposit-withdraw/detail"
ACCOUNT_MARGIN_DETAILS = "/spot/v1/margin/isolated/account"
ACCOUNT_MARGIN_ASSET_TRANSFER = "/spot/v1/margin/isolated/transfer"
ACCOUNT_USER_FEE = "/spot/v1/user_fee"
ACCOUNT_TRADE_FEE = "/spot/v1/trade_fee"

## Spot /Margin Trading
SPOT_PLACE_ORDER = "/spot/v2/submit_order"
SPOT_MARGIN_PLACE_ORDER = "/spot/v1/margin/submit_order"
SPOT_BATCH_ORDER = "/spot/v2/batch_orders"
SPOT_CANCEL_ORDER = "/spot/v3/cancel_order"
SPOT_CANCEL_ALL_ORDERS = "/spot/v1/cancel_orders"
SPOT_GET_ORDER_DETAILS = "/spot/v2/order_detail"
SPOT_USER_ORDER_HISTORY = "/spot/v3/orders"
SPOT_USER_TRADE_HISTORY = "/spot/v2/trades"

## Margin Loan
MARGIN_BORROW = "/spot/v1/margin/isolated/borrow"
MARING_REPAY = "/spot/v1/margin/isolated/repay"
MARGIN_BORROW_RECORD = "/spot/v1/margin/isolated/borrow_record"
MARING_REPAYMENT_RECORD = "/spot/v1/margin/isolated/repay_record"
MARGIN_TRADING_PAIR_BORROW_RATE_AND_AMOUNT = "/spot/v1/margin/isolated/pairs"

# 2 USD-M Futures Market API
# Futures Market Data
FUTURES_CONTRACT_DETAILS = "/contract/public/details"
FUTURES_MARKET_DEPTH = "/contract/public/depth"
FUTURES_OPEN_INTEREST = "/contract/public/open-interest"
FUTURES_FUNDING_RATE = "/contract/public/funding-rate"
FUTURES_K_LINE = "/contract/public/kline"

## Futures Account Data
FUTURES_CONTRACT_ASSETS_DETAIL = "/contract/private/assets-detail"

## Futures Trading
FUTURES_ORDER_DETAIL = "/contract/private/order"
FUTURES_ORDER_HISTORY = "/contract/private/order-history"
FUTURES_CURRENT_POSITION = "/contract/private/position"
FUTURES_TRADE_DETAIL = "/contract/private/trades"
FUTURES_SUBMIT_ORDER = "/contract/private/submit-order"
FUTURES_CANCEL_ORDER = "/contract/private/cancel-order"
FUTURES_CANCEL_ALL_ORDERS = "/contract/private/cancel-orders"



@unique
class Auth(int, Enum):
    NONE = 1
    KEYED = 2
    SIGNED = 3

class Sort(str, Enum):
    ASC = "asc"
    DESC = "desc"

@unique
class Exchange(int, Enum):
    BITMART = 1
    BINANCE = 2
    HUOBI = 3

@unique
class ServiceStatus(int, Enum):
    WAITING = 0
    WORKING = 1
    COMPLETED = 2

@unique
class TimeFrame(int, Enum):
    tf_1m = 1
    tf_5m = 5
    tf_15m = 15
    tf_30m = 30
    tf_1h = 60
    tf_2h = 120
    tf_4h = 240
    tf_1d = 60*24
    tf_1w = 60*24*7

@unique
class Market(str, Enum):
    SPOT = "spot"
    FUTURES = "futures"
    SPOT_MARGIN = "margin"

@unique
class OrderMode(str, Enum):
    SPOT = "spot"
    ISOLATED_MARGIN = "iso_margin"

@unique
class OrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"
    LIMIT_MAKER = "limit_maker" # only for spot market
    IOC = "ioc" # only for spot market

@unique
class SpotSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

@unique
class Position(int, Enum):
    LONG = 1
    SHORT = 2

@unique
class FuturesSide(int, Enum, metaclass=MetaEnum):
    BUY_OPEN_LONG = 1
    BUY_CLOSE_SHORT = 2
    SELL_CLOSE_LONG = 3
    SELL_OPEN_SHORT = 4

@unique
class OrderOpenType(str, Enum):
    ISOLATED = "isolated"
    CROSS = "cross"


@unique
class OrderState(int, Enum):
    STATUS_CHECK = 2
    ORDER_SUCCESS = 4
    PARTIALLY_FILLED = 5
    FULLY_FILLED = 6
    CANCELLED = 8
    OUTSTANDING = 9
    MIX_6_8_11 = 10
    PARTIALLY_FILLED_AND_CANCELED = 11

@unique
class ExecType(str, Enum):
    MAKER = "M"
    TAKER = "T"

@unique
class TradeOrderType(int, Enum):
    REGULAR = 0
    MAKER_ONLY = 1
    FILL_OR_KILL = 2
    IMMEDIATE_OR_CANCEL = 3


@unique
class WayType(int, Enum):
    ASK = 1
    BID = 2

@unique
class FuturesContractType(int, Enum):
    PERPETUAL = 1
    FUTURES = 2

@unique
class BtWebSocket(str, Enum):
    """Base urls for websocket endpoints"""
    PUBLIC = "wss://ws-manager-compress.bitmart.com/api?protocol=1.1"
    PRIVATE = "wss://ws-manager-compress.bitmart.com/user?protocol=1.1"

@unique
class BtSocketOperation(str, Enum, metaclass=MetaEnum):
    """Base operation data for Bitmart websockets"""
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    LOGIN = "login"


@unique
class BtSpotSocketKlineChannels(str, Enum):
    """Base websocket channels for Bitmart Spot Klines"""
    K_LINE_CHANNEL_1MIN = "spot/kline1m"
    K_LINE_CHANNEL_3MIN = "spot/kline3m"
    K_LINE_CHANNEL_5MIN = "spot/kline5m"
    K_LINE_CHANNEL_15MIN = "spot/kline15m"
    K_LINE_CHANNEL_30MIN = "spot/kline30m"
    K_LINE_CHANNEL_1HOUR = "spot/kline1H"
    K_LINE_CHANNEL_2HOURS = "spot/kline2H"
    K_LINE_CHANNEL_4HOURS = "spot/kline4H"
    K_LINE_CHANNEL_1DAY = "spot/kline1D"
    K_LINE_CHANNEL_1WEEK = "spot/kline1W"
    K_LINE_CHANNEL_1MONTH = "spot/kline1M"

@unique
class BtFuturesSocketKlineChannels(str, Enum):
    K_LINE_CHANNEL_1MIN = "futures/klineBin1m"
    K_LINE_CHANNEL_5MIN = "futures/klineBin5m"
    K_LINE_CHANNEL_15MIN = "futures/klineBin15m"
    K_LINE_CHANNEL_30MIN = "futures/klineBin30m"
    K_LINE_CHANNEL_1HOUR = "futures/klineBin1h"
    K_LINE_CHANNEL_2HOURS = "futures/klineBin2h"
    K_LINE_CHANNEL_4HOURS = "futures/klineBin4h"
    K_LINE_CHANNEL_1DAY = "futures/klineBin1d"
    K_LINE_CHANNEL_1WEEK = "futures/klineBin1w"

@unique
class BtSpotSocketDepthChannels(str, Enum):
    DEPTH_CHANNEL_5LEVEL = "spot/depth5"
    DEPTH_CHANNEL_20LEVEL = "spot/dept20"
    DEPTH_CHANNEL_50LEVEL = "spot/depth50"

@unique
class BtFuturesSocketDepthChannels(str, Enum):
    DEPTH_CHANNEL_5LEVEL = "futures/depth5"
    DEPTH_CHANNEL_20LEVEL = "futures/dept20"
    DEPTH_CHANNEL_50LEVEL = "futures/depth50"


BtFuturesTickerChannel = "futures/ticker"
BtFuturesTPrivatePositionChannel = "futures/position"
BtFuturesTPrivateAssetChannel = "futures/asset"

