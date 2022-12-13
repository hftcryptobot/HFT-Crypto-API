import json
from .api_client import PyClient
from datetime import datetime
from .constants import *
from .bitmart_objects import *
from .bitmart_exceptions import *
from typing import Dict, Union
from .ws_base import BitmartWs
from typing import Callable

class BitmartClient(PyClient):

    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, memo: Optional[str] = None,
                 url: str = API_URL, timeout: tuple = TIMEOUT):
        PyClient.__init__(self, api_key, secret_key, memo, url, timeout)
        self.ws_public: Dict[Union[Market], BitmartWs] = {Market.SPOT: BitmartWs(WS_URL, Market.SPOT),
                                                          Market.FUTURES: BitmartWs(CONTRACT_WS_URL, Market.FUTURES)}
        self.ws_private: Dict[Union[Market], BitmartWs] = {
            Market.SPOT: BitmartWs(WS_URL_USER, Market.SPOT, api_key, memo, secret_key),
            Market.FUTURES: BitmartWs(CONTRACT_WS_URL_USER, Market.FUTURES,
                                      api_key, memo, secret_key)}

    def subscribe_private(self, market: Market, channels: List[str], symbols: Optional[List[str]] = None):
        self.ws_private[market].subscribe(channels, symbols)

    def subscribe_public(self, market: Market, channels: List[str], symbols: Optional[List[str]] = None):
        self.ws_public[market].subscribe(channels, symbols)

    def start_websockets(self, market: Market, on_message: Callable):
        self.ws_public[market].start(on_message)
        self.ws_private[market].start(on_message)

    def get_system_time(self):
        response = self._request_without_params(GET, SYSTEM_TIME)
        server_time = json.loads(response.content)['data']['server_time']
        return datetime.fromtimestamp(server_time)

    def get_service_status(self):
        response = self._request_without_params(GET, SERVICE_STATUS)
        services = []
        for bt_service in json.loads(response.content)['data']['service']:
            title = bt_service["title"]
            service_type = bt_service["service_type"]
            status = bt_service["status"]
            start_time = bt_service["start_time"]
            end_time = bt_service["end_time"]
            services.append(BitmartService(title, service_type, status, start_time, end_time))
        return datetime.fromtimestamp(services)

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

    def get_basic_fee_rate(self):
        response = self._request_without_params(GET, ACCOUNT_USER_FEE, Auth.KEYED)
        bt_fee = BitmartFee()

        bt_fee.level = json.loads(response.content)['data']['level']
        bt_fee.user_rate_type = json.loads(response.content)['data']['user_rate_type']
        bt_fee.taker_fee_rate_A = float(json.loads(response.content)['data']['taker_fee_rate_A'])
        bt_fee.maker_fee_rate_A = float(json.loads(response.content)['data']['maker_fee_rate_A'])
        bt_fee.taker_fee_rate_B = float(json.loads(response.content)['data']['taker_fee_rate_B'])
        bt_fee.maker_fee_rate_B = float(json.loads(response.content)['data']['maker_fee_rate_B'])

        return bt_fee

    def get_trade_fee_rate(self, symbol):
        response = self._request_without_params(GET, ACCOUNT_TRADE_FEE, Auth.KEYED)
        bt_trade_fee = BitmartTradeFee(symbol)

        bt_trade_fee.buy_taker_fee_rate = float(json.loads(response.content)['data']['buy_taker_fee_rate'])
        bt_trade_fee.sell_taker_fee_rate = float(json.loads(response.content)['data']['sell_taker_fee_rate'])
        bt_trade_fee.buy_maker_fee_rate = float(json.loads(response.content)['data']['buy_maker_fee_rate'])
        bt_trade_fee.sell_maker_fee_rate = float(json.loads(response.content)['data']['sell_maker_fee_rate'])

        return bt_trade_fee

    def get_list_of_trading_pairs(self):
        response = self._request_without_params(GET, SPOT_TRADING_PAIRS_LIST)
        return json.loads(response.content)['data']['symbols']

    def get_traiding_pair_detail(self):
        response = self._request_without_params(GET, SPOT_TRADING_PAIRS_DETAILS)

        return 0

    def get_ticker_of_all_pairs(self):
        list_currency_details = []
        response = self._request_without_params(GET, SPOT_TICKER)
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
                                                low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid,
                                                best_bid_size,
                                                fluctuation, timestamp)
            list_currency_details.append(currency_details)

        return list_currency_details

    def get_ticker_details(self, symbol: str):
        response = self._request_with_params(GET, SPOT_TICKER_DETAILS, {'symbol': symbol})

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
                                            low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid,
                                            best_bid_size,
                                            fluctuation, timestamp)

        return currency_details

    def get_kline_steps(self):
        response = self._request_without_params(GET, SPOT_K_LIE_STEP)
        return json.loads(response.content)['data']['steps']

    def get_symbol_kline(self, symbol: str, from_time: datetime, to_time: datetime, tf: TimeFrame = TimeFrame.tf_1d,
                         market=Market.SPOT):
        klines_data = []

        if market == Market.SPOT:
            param = {
                'symbol': symbol,
                'from': int(datetime.timestamp(from_time)),
                'to': int(datetime.timestamp(to_time)),
                'step': tf.value
            }
            response = self._request_with_params(GET, SPOT_K_LINE, param)

            for kline in json.loads(response.content)['data']['klines']:
                date_time = float(kline['timestamp'])
                open = float(kline['open'])
                high = float(kline['high'])
                low = float(kline['low'])
                close = float(kline['close'])
                last_price = float(kline['last_price'])
                volume = float(kline['volume'])
                quote_volume = float(kline['quote_volume'])
                kline_object = Kline(date_time, open, high, low, close, volume, last_price,  quote_volume,
                                     market=market)
                klines_data.append(kline_object)

        elif Market.FUTURES:
            param = {
                'symbol': symbol,
                'start_time': int(datetime.timestamp(from_time)),
                'end_time': int(datetime.timestamp(to_time)),
                'step': tf.value
            }
            response = self._request_with_params(GET, FUTURES_K_LINE, param)
            for kline in json.loads(response.content)['data']:
                date_time = float(kline['timestamp'])
                open = float(kline['open_price'])
                high = float(kline['high_price'])
                low = float(kline['low_price'])
                close = float(kline['close_price'])
                last_price = ""
                volume = float(kline['volume'])
                quote_volume = ""
                kline_object = Kline(date_time, open, high, low, close, volume, last_price,  quote_volume,
                                     market=market)
                klines_data.append(kline_object)

        return klines_data

    def get_symbol_depth(self, symbol: str, precision: int, size: int, market=Market.SPOT):
        param = {
            'symbol': symbol
        }
        if market == Market.SPOT:
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
            return BitmartDepth(buys, sells, time_stamp)
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
        response = self._request_with_params(GET, SPOT_RECENT_TRADES, param)
        trades = []
        for trade in json.loads(response.content)['data']['trades']:
            amount = trade["amount"]
            order_time = trade["order_time"]
            price = trade["price"]
            count = trade["count"]
            bt_type = trade["type"]
            trades.append(BitmartTrade(amount, order_time, price, count, bt_type))
        return trades

    def get_margin_acount_balance(self):
        wallet_currencies = []
        response = self._request_without_params(GET, ACCOUNT_MARGIN_DETAILS, Auth.KEYED)
        for ticker in json.loads(response.content)['data']['symbols']:
            margin_acc_symbol = MarginAccountSymbol(ticker["symbol"])
            margin_acc_symbol.risk_rate = float(ticker["risk_rate"])
            margin_acc_symbol.risk_level = int(ticker["risk_level"])
            margin_acc_symbol.buy_enabled = True if ticker["buy_enabled"] == "true" else False
            margin_acc_symbol.sell_enabled = True if ticker["sell_enabled"] == "true" else False
            margin_acc_symbol.liquidate_price = float(ticker["liquidate_price"])
            margin_acc_symbol.liquidate_rate = float(ticker["liquidate_rate"])
            wallet_currencies.append(margin_acc_symbol)

        return wallet_currencies

    # Functions for Funding Account Data

    def get_futures_position_details(self, symbol) -> List[OrderPosition]:
        response = self._request_with_params(GET, FUTURES_CURRENT_POSITION, {'symbol': symbol}, Auth.SIGNED)
        order_positions = []
        for position in json.loads(response.content)['data']:
            order_pos = OrderPosition(symbol=symbol)
            order_pos.leverage = float(position["leverage"])
            order_pos.date_time = datetime.fromtimestamp(int(position["timestamp"])/1000)
            order_pos.current_fee = float(position["current_fee"])
            order_pos.open_date_time = datetime.fromtimestamp(int(position["open_timestamp"])/1000)
            order_pos.current_value = float(position["current_value"])
            order_pos.mark_price = float(position["mark_price"])
            order_pos.position_value = float(position["position_value"])
            order_pos.position_cross = float(position["position_cross"])
            order_pos.close_vol = float(position["close_vol"])
            order_pos.close_avg_price = float(position["close_avg_price"])
            order_pos.current_amount = float(position["current_amount"])
            order_pos.unrealized_value = float(position["unrealized_value"])
            order_pos.realized_value = float(position["realized_value"])
            order_positions.append(order_pos)

        return order_positions

    # POST https://api-cloud.bitmart.com/spot/v1/margin/submit_order
    def place_margin_order(self, symbol: str, side: str, type: str, clientOrderId='', size='', price='',
                           notional=''):
        param = {
            'symbol': symbol,
            'side': side,
            'type': type,
            'clientOrderId': clientOrderId,
            'size': size,
            'price': price,
            'notional': notional
        }
        return self._request_with_params(POST, SPOT_MARGIN_PLACE_ORDER, param, Auth.SIGNED)

    # POST https://api-cloud.bitmart.com/spot/v3/cancel_order
    def cancel_order(self, symbol: str, order_id="",  market=Market.SPOT):
        param = {
            'symbol': symbol,
            'order_id': str(order_id),
        }
        if market == Market.SPOT:
            response = self._request_with_params(POST, SPOT_CANCEL_ORDER, param, Auth.SIGNED)
        elif market == Market.FUTURES:
            response = self._request_with_params(POST, FUTURES_CANCEL_ORDER, param, Auth.SIGNED)

        return True

    # POST https://api-cloud.bitmart.com/spot/v1/cancel_orders
    def cancel_all_orders(self, symbol: str, side: SpotSide, market=Market.SPOT):
        param = {
            'symbol': symbol,
            'side': side.value
        }
        if market == Market.SPOT:
            response = self._request_with_params(POST, SPOT_CANCEL_ALL_ORDERS, param, Auth.SIGNED)
        elif market == Market.FUTURES:
            response = self._request_with_params(POST, FUTURES_CANCEL_ALL_ORDERS, param, Auth.SIGNED)

        return True

    # GET https://api-cloud.bitmart.com/spot/v2/order_detail
    def update_order_detail(self, order: BitmartOrder, market=Market.SPOT):
        param = {
            'order_id': order.order_id
        }
        if market == Market.FUTURES:
            response = self._request_with_params(GET, SPOT_GET_ORDER_DETAILS, param, Auth.KEYED)
            order.price = json.loads(response.content)['data']['price']
            order.order_status = json.loads(response.content)['data']['state']
            order.side = json.loads(response.content)['data']['side']
            order.order_type = json.loads(response.content)['data']['type']
            order.leverage = json.loads(response.content)['data']['leverage']
            order.open_type = json.loads(response.content)['data']['open_type']
            order.price_avg = json.loads(response.content)['data']['deal_avg_price']
            order.size = json.loads(response.content)['data']['deal_size']
            order.create_time = json.loads(response.content)['data']['create_time']
            order.update_time = datetime.fromtimestamp(
                int(json.loads(response.content)['data']['update_time']))

        elif market == Market.SPOT:
            response = self._request_with_params(GET, FUTURES_ORDER_DETAIL, param, Auth.KEYED)
            order.price = json.loads(response.content)['data']['price']
            order.order_status = json.loads(response.content)['data']['status']
            order.side = json.loads(response.content)['data']['side']
            order.order_type = json.loads(response.content)['data']['type']
            order.leverage = "Not applied for Spot Market"
            order.open_type = json.loads(response.content)['data']['open_type']
            order.price_avg = json.loads(response.content)['data']['price_avg']
            order.size = json.loads(response.content)['data']['size']
            order.notional = json.loads(response.content)['data']['notional']
            order.filled_notional = json.loads(response.content)['data']['filled_notional']
            order.filled_size = json.loads(response.content)['data']['filled_size']
            order.unfilled_volume = json.loads(response.content)['data']['unfilled_volume']
            order.order_mode = json.loads(response.content)['data']['order_mode']
            order.create_time = json.loads(response.content)['data']['create_time']
            order.update_time = datetime.fromtimestamp(datetime.now())

        return True

    # GET https://api-cloud.bitmart.com/spot/v3/orders
    def get_order_history(self, symbol: str, market=Market.SPOT,
                          start_time: Optional[datetime]=None,
                          end_time:Optional[datetime]=None):

        order_objects = []
        if market == Market.SPOT:
            param = {
                'symbol': symbol,
            }
            response = self._request_with_params(GET, SPOT_USER_ORDER_HISTORY, param, Auth.KEYED)
            for order in json.loads(response.content)['data']['orders']:
                symbol = order["symbol"]
                side = order["side"]
                size = order["size"]
                price = order["price"]
                bt_order = BitmartOrder(symbol, side, size, price, market=Market.SPOT)
                bt_order.create_time = datetime.fromtimestamp(float(order["create_time"]))
                bt_order.order_mode = OrderMode.SPOT if order["order_mode"] == "spot" else OrderMode.ISOLATED_MARGIN
                bt_order.order_type = OrderType.LIMIT if order["type"] == "limit" else OrderType.MARKET
                bt_order.price_avg = order["price_avg"]
                bt_order.order_id = order["order_id"]
                bt_order.notional = order["notional"]
                bt_order.filled_notional = order["filled_notional"]
                bt_order.filled_size = order["filled_size"]
                bt_order.order_status = order["order_status"]
                bt_order.client_order_id = order["client_order_id"]
                order_objects.append(bt_order)
        elif market == Market.FUTURES:
            param = {
                'symbol': symbol,
            }
            response = self._request_with_params(GET, FUTURES_ORDER_HISTORY, param, Auth.KEYED)
            for order in json.loads(response.content)['data']:
                symbol = order["symbol"]
                side = order["side"]
                size = order["size"]
                price = order["price"]
                bt_order = BitmartOrder(symbol, FuturesSide(side), size, price, market=Market.FUTURES)
                bt_order.order_id = order["order_id"]
                bt_order.order_status = OrderState(order["state"])
                bt_order.order_type = OrderType(order["type"])
                bt_order.leverage = int(order["leverage"])
                bt_order.open_type = OrderOpenType(order["open_type"])
                bt_order.price_avg = float(order["deal_avg_price"])
                bt_order.create_time = order["create_time"]
                order_objects.append(bt_order)

        return order_objects

    # Unified methods for trading
    def submit_order(self, symbol: str, side: Union[FuturesSide, SpotSide],
                     price: Optional[float]=None, size: Optional[float]=0, order_type: OrderType = OrderType.LIMIT,
                     market: Market = Market.SPOT, leverage: Optional[int] = 1,
                     open_type: OrderOpenType = OrderOpenType.ISOLATED,
                     client_order_id: Optional[str] = None):

        bm_order = BitmartOrder(symbol, side, size, price, market, order_type, leverage, open_type, client_order_id)
        if market == Market.SPOT or market == Market.SPOT_MARGIN:
            if order_type == OrderType.LIMIT_MAKER:
                return "Not implemented"
            elif order_type == OrderType.IOC:
                return "Not implemented"
            if market == Market.SPOT:
                response = self._request_with_params(POST, SPOT_PLACE_ORDER, bm_order.param, Auth.SIGNED)
            elif market == Market.SPOT_MARGIN:
                response = self._request_with_params(POST, SPOT_MARGIN_PLACE_ORDER, bm_order.param, Auth.SIGNED)
            try:
                bm_order.order_id = json.loads(response.content)['data']['order_id']
            except:
                raise APIException(response)

            return bm_order
        elif market == Market.FUTURES:
            response = self._request_with_params(POST, FUTURES_SUBMIT_ORDER, bm_order.param, Auth.SIGNED)
            try:
                bm_order.order_id = json.loads(response.content)['data']['order_id']
            except:
                raise APIException(response)

            return bm_order

    def submit_batch_order(self, orders):
        return "Not Implemented"

    def get_contract(self, symbol: str, market=Market.FUTURES):
        response = self._request_with_params(GET, FUTURES_CONTRACT_DETAILS, {'symbol': symbol})
        for item in json.loads(response.content)['data']:
            symbol = item['symbol']
            product_type = item['product_type']
            base_currency = item['base_currency']
            quote_currency = item['quote_currency']
            volume_precision = item['volume_precision']
            price_precision = item['price_precision']
            max_volume = item['max_volume']
            min_volume = item['min_volume']
            funding_rate = item['funding_rate']
            contract_size = item['contract_size']
            index_price = item['index_price']
            index_name = item['index_name']
            min_leverage = item['min_leverage']
            max_leverage = item['max_leverage']
            turnover_24h = item['turnover_24h']
            volume_24h = item['volume_24h']
            last_price = item['last_price']
            open_timestamp = item['open_timestamp']
            expire_timestamp = item['expire_timestamp']
            settle_timestamp = item['settle_timestamp']
        return BitmartFutureContract(symbol, product_type, base_currency, quote_currency, volume_precision,
                                     price_precision, max_volume, min_volume,
                                     funding_rate, contract_size, index_price, index_name, min_leverage, max_leverage,
                                     turnover_24h, volume_24h, last_price,
                                     open_timestamp, expire_timestamp, settle_timestamp)

    def update_open_interest(self, bt_Currency: CurrencyDetailed, market=Market.FUTURES):
        response = self._request_with_params(GET, FUTURES_OPEN_INTEREST, {'symbol': bt_Currency.symbol})
        bt_Currency.open_interest_datetime = json.loads(response.content)['data']["timestamp"]
        bt_Currency.open_interest = json.loads(response.content)['data']["open_interest"]
        bt_Currency.open_interest_value = json.loads(response.content)['data']["open_interest_value"]

        return True

    def update_current_funding_rate(self, bt_Currency: CurrencyDetailed, market=Market.FUTURES):
        response = self._request_with_params(GET, FUTURES_OPEN_INTEREST, {'symbol': bt_Currency.symbol})
        bt_Currency.funding_rate = json.loads(response.content)['data']["rate_value"]
        bt_Currency.funding_rate_datetime = json.loads(response.content)['data']["timestamp"]

        return True

    def get_acount_balance(self, market=Market.SPOT):
        wallet_currencies = []
        if market == Market.SPOT:
            response = self._request_without_params(GET, ACCOUNT_BALANCE, Auth.KEYED)
            for currency in json.loads(response.content)['data']['wallet']:
                symbol = currency['currency']
                available = currency['available']
                frozen = currency['frozen']
                wallet_currencies.append(WalletItem(symbol, available, frozen, wallet_type=Market.SPOT))
        elif market == Market.FUTURES:
            response = self._request_without_params(GET, FUTURES_CONTRACT_ASSETS_DETAIL, Auth.KEYED)
            # print(json.loads(response.content)['data'])
            for currency in json.loads(response.content)['data']:
                ticker = currency['currency']
                available = currency['available_balance']
                frozen = currency['frozen_balance']
                position_deposit = currency['position_deposit']
                equity = currency['equity']
                unrealized = currency['unrealized']
                wallet_currencies.append(WalletItem(ticker, available, frozen, position_deposit, equity, unrealized,
                                                    wallet_type=Market.FUTURES))
        elif market == Market.SPOT_MARGIN:
            response = self._request_without_params(GET, ACCOUNT_MARGIN_DETAILS, Auth.KEYED)
            for ticker in json.loads(response.content)['data']['symbols']:
                margin_acc_symbol = MarginAccountSymbol(symbol=ticker["symbol"])
                margin_acc_symbol.risk_rate = float(ticker["risk_rate"])
                margin_acc_symbol.risk_level = int(ticker["risk_level"])
                margin_acc_symbol.buy_enabled = True if ticker["buy_enabled"] == "true" else False
                margin_acc_symbol.sell_enabled = True if ticker["sell_enabled"] == "true" else False
                margin_acc_symbol.liquidate_price = float(ticker["liquidate_price"])
                margin_acc_symbol.liquidate_rate = float(ticker["liquidate_rate"])
                wallet_currencies.append(margin_acc_symbol)

        bitmart_wallet = BitmartWallet(wallet_currencies)

        return bitmart_wallet


"""     def get_websocket_data(self, market:Market,connection, operation, tickers):
        args = []
        if connection == BitmartSocketOperation.SUBSCRIBE:
            for ticker in tickers:
                args.append(market.value + "/ticker:"+ticker)
            if operation in BitmartSocketOperation:
                param = {
                    'op': operation.value,
                    "args": args
            }
            ws = create_connection(connection.value)
            ws.send(json.dumps(param))
            response =  ws.recv()
            curr_ws_objects = []
            print(response)
            for item in json.loads(response)['data']:
                base_volume_24h = item["base_volume_24h"]
                high_24h = item['high_24h']
                last_price = item['last_price']
                low_24h = item['low_24h']
                open_24h = item['open_24h']
                s_t = item['s_t']
                symbol = item['symbol']

                if len(tickers) == 1:
                    cws =  CurrencyWebSocket(symbol, last_price, base_volume_24h, high_24h, low_24h, open_24h, s_t)
                    return cws
                else:
                    curr_ws_objects.append(CurrencyWebSocket(symbol, last_price, base_volume_24h, high_24h, low_24h, open_24h, s_t))
            return curr_ws_objects
        elif connection == BitmartSocketOperation.UNSUBSCRIBE:
            print("Not implemented")
        elif connection == BitmartSocketOperation.LOGIN:
            print("Not implemented") """
