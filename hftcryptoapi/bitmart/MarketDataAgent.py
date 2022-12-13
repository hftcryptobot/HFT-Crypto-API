import json
from .api_client import PyClient
from datetime import datetime
from .constants import *
from .bitmart_objects import *
from websocket import create_connection
import asyncio
import websockets

class MarketDataAgent():
    def __init__(self, exchange=Exchange.BITMART):
        self.exchange = exchange

# Region: market data handlers
    # Functions for Public Market Data
    def get_currency_list(self):
        bitmart_currencies = []
        response = self._request_without_params(GET, SPOT_CURRENCY_LIST)
        for currency in json.loads(response.content)['data']['currencies']:
            id = currency['currency']
            name = currency['name']
            withdraw_enabled = bool(currency['withdraw_enabled'])
            deposit_enabled = bool(currency['deposit_enabled'])
            bitmart_currencies.append(Currency(id, name, withdraw_enabled, deposit_enabled))
        return bitmart_currencies

    def get_list_of_trading_pairs(self, symbols:list):
        response =  self._request_without_params(GET, SPOT_TRADING_PAIRS_LIST)
        return json.loads(response.content)['data']['symbols']

    def get_all_trading_pair_details(self):
        list_currency_details = []
        response =  self._request_without_params(GET, SPOT_TICKER)
        for ticker in json.loads(response.content)['data']['tickers']:
            symbol = ticker['symbol']
            last_price = ticker['last_price']
            quote_volume_24h = ticker['uote_volume_24h']
            base_volume_24h = ticker['base_volume_24h']
            high_24h = ticker['high_24h']
            low_24h = ticker['low_24h']
            open_24h = ticker['open_24h']
            close_24h = ticker['close_24h']
            best_ask = ticker['best_ask']
            best_ask_size = ticker['best_ask_size']
            best_bid = ticker['best_bid']
            best_bid_size = ticker['best_bid_size']
            fluctuation = ticker['fluctuation']
            timestamp = ticker['timestamp']
            currency_details = CurrencyDetailed(symbol, last_price, quote_volume_24h, base_volume_24h, high_24h,
                 low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid, best_bid_size,
                 fluctuation,timestamp)
            list_currency_details.append(currency_details)
        
        return list_currency_details


    def get_traiding_pair_detail(self, symbol: str):
        response =  self._request_with_params(GET, SPOT_TICKER_DETAILS, {'symbol': symbol})
       
        symbol = json.loads(response.content)['data']['symbol']
        last_price = json.loads(response.content)['data']['symbol']
        quote_volume_24h = json.loads(response.content)['data']['symbol']
        base_volume_24h = json.loads(response.content)['data']['symbol']
        high_24h = json.loads(response.content)['data']['symbol']
        low_24h = json.loads(response.content)['data']['symbol']
        open_24h = json.loads(response.content)['data']['symbol']
        close_24h = json.loads(response.content)['data']['symbol']
        best_ask = json.loads(response.content)['data']['symbol']
        best_ask_size = json.loads(response.content)['data']['symbol']
        best_bid = json.loads(response.content)['data']['symbol']
        best_bid_size = json.loads(response.content)['data']['symbol']
        fluctuation = json.loads(response.content)['data']['symbol']
        timestamp = json.loads(response.content)['data']['timestamp']
        
        currency_details = CurrencyDetailed(symbol, last_price, quote_volume_24h, base_volume_24h, high_24h,
                 low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid, best_bid_size,
                 fluctuation,timestamp)

        return currency_details


    def get_kline_steps(self):
        response = self._request_without_params(GET, SPOT_K_LIE_STEP)
        return json.loads(response.content)['data']['steps']

    def get_symbol_kline(self, symbol: str, fromTime: datetime, toTime: datetime, step: int = 1, market = Market.SPOT):
        klines_data = []
        if market == Market.SPOT:
            param = {
                'symbol': symbol,
                'from': datetime.datetime.timestamp(fromTime),
                'to': datetime.datetime.timestamp(toTime),
                'step': step
            }
            response =  self._request_with_params(GET, SPOT_K_LINE, param)
            for kline in json.loads(response.content)['data']['klines']:
                    date_time = float(kline['timestamp'])
                    open = float(kline['open'])
                    high = float(kline['high'])
                    low = float(kline['low'])
                    close = float(kline['close'])
                    last_price = float(kline['last_price'])
                    volume = float(kline['volume'])
                    quote_volume = float(kline['quote_volume'])
                    kline_object = Kline(date_time, open, high, low, close, last_price, volume, quote_volume)
                    klines_data.append(kline_object)

        elif Market.FUTURES:
            param = {
                'symbol': symbol,
                'start_time': datetime.datetime.timestamp(fromTime),
                'end_time': datetime.datetime.timestamp(toTime),
                'step': step
            }
            response =  self._request_with_params(GET, FUTURES_K_LINE, param)
            for kline in json.loads(response.content)['data']:
                    date_time = float(kline['timestamp'])
                    open = float(kline['open_price'])
                    high = float(kline['high_price'])
                    low = float(kline['low_price'])
                    close = float(kline['close_price'])
                    last_price = ""
                    volume = float(kline['volume'])
                    quote_volume = ""
                    kline_object = Kline(date_time, open, high, low, close, last_price, volume, quote_volume)
                    klines_data.append(kline_object)
        return klines_data


    def get_symbol_depth(self, symbol: str, precision: int, size: int, market = Market.SPOT):
        if market == Market.SPOT:
            param = {
                'symbol': symbol
            }

            if precision:
                param['precision'] = precision

            if size:
                param['size'] = size
            response = self._request_with_params(GET, SPOT_BOOK_DEPTH, param)
            buys = []
            sells = []
            for depth in json.loads(response.content)['data']['buys']:
                amount = depth["amount"]
                total = depth["total"]
                price = depth["price"]
                count = depth["count"]
                buys.append(BitmartSpotBuySells(amount, total, price, count))
            for depth in json.loads(response.content)['data']['sells']:
                amount = depth["amount"]
                total = depth["total"]
                price = depth["price"]
                count = depth["count"]
                sells.append(BitmartSpotBuySells(amount, total, price, count))
            time_stamp = json.loads(response.content)['data']['timestamp']
            return BitmartDepth( buys, sells, time_stamp)
        elif Market.FUTURES:
            response = self._request_with_params(GET, FUTURES_MARKET_DEPTH, param)
            asks = []
            bids = []
            for depth in json.loads(response.content)['data']['asks']:
                price = depth[0]
                quantity = depth[1]
                quantity_above = depth[2]
                asks.append(BitmartFuturesAskBids(price, quantity, quantity_above))
            for depth in json.loads(response.content)['data']['bids']:
                price = depth[0]
                quantity = depth[1]
                quantity_above = depth[2]
                bids.append(BitmartFuturesAskBids(price, quantity, quantity_above))
            time_stamp = json.loads(response.content)['data']['timestamp']
            return BitmartDepth(asks, bids, time_stamp)



    def get_symbol_recent_trades(self, symbol: str, N: int = 50):
        param = {
            'symbol': symbol,
            'N': N
        }
        response =  self._request_with_params(GET, SPOT_RECENT_TRADES, param)
        trades = []
        for trade in json.loads(response.content)['data']['trades']:
            amount = trade["amount"]
            order_time = trade["order_time"]
            price = trade["price"]
            count = trade["count"]
            bt_type = trade["bt_type"]
            trades.append(BitmartTrade(amount, order_time, price, count, bt_type))
        return trades








# Region: Websocket methods
    async def get_ticker_wsdata(self, symbol, market:Market.SPOT, operation=BtSocketOperation.SUBSCRIBE, address=BtWebSocket.PUBLIC):
        args = []
        if operation == BtSocketOperation.SUBSCRIBE:
            args.append(market.value + "/ticker:"+symbol)
            if operation in BtSocketOperation:
                param = {
                    'op': operation.value,
                    "args": args
            }
            async with websockets.connect(address.value) as ws:
            #ws = create_connection(address.value)
                await ws.send(json.dumps(param))
                response = await ws.recv()
                #print(response)
                for item in json.loads(response)['data']:
                    base_volume_24h = item["base_volume_24h"]
                    high_24h = item['high_24h']
                    last_price = item['last_price']
                    low_24h = item['low_24h']
                    open_24h = item['open_24h']
                    s_t = item['s_t']
                    symbol = item['symbol']
                    return  CurrencyWebSocket(symbol, last_price, base_volume_24h, high_24h, low_24h, open_24h, s_t)
        elif operation == BtSocketOperation.UNSUBSCRIBE:
            print("Not implemented")
        elif operation == BtSocketOperation.LOGIN:
            print("Not implemented")
        

    async def get_kline_wsdata(self, symbol, channel=BtSpotSocketKlineChannels.K_LINE_CHANNEL_1MIN, operation=BtSocketOperation.SUBSCRIBE):
        return False

    async def get_depth_wsdata(symbol, channel=BtSpotSocketDepthChannels.DEPTH_CHANNEL_5LEVEL, operation=BtSocketOperation.SUBSCRIBE):
        return False

    async def get_trade_wsdata(symbol, channel=Market.SPOT, operation=BtSocketOperation.SUBSCRIBE):
        return False