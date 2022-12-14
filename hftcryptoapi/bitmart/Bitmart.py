from .api_client import PyClient
from hftcryptoapi.bitmart.data import *
from typing import Dict, Union, List
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
        data = json.loads(response.content)['data']
        bt_fee.level = data['level']
        bt_fee.user_rate_type = data['user_rate_type']
        bt_fee.taker_fee_rate_A = float(data['taker_fee_rate_A'])
        bt_fee.maker_fee_rate_A = float(data['maker_fee_rate_A'])
        bt_fee.taker_fee_rate_B = float(data['taker_fee_rate_B'])
        bt_fee.maker_fee_rate_B = float(data['maker_fee_rate_B'])

        return bt_fee

    def get_trade_fee_rate(self, symbol):
        response = self._request_without_params(GET, ACCOUNT_TRADE_FEE, Auth.KEYED)
        bt_trade_fee = BitmartTradeFee(symbol)
        data = json.loads(response.content)['data']
        bt_trade_fee.buy_taker_fee_rate = float(data['buy_taker_fee_rate'])
        bt_trade_fee.sell_taker_fee_rate = float(data['sell_taker_fee_rate'])
        bt_trade_fee.buy_maker_fee_rate = float(data['buy_maker_fee_rate'])
        bt_trade_fee.sell_maker_fee_rate = float(data['sell_maker_fee_rate'])

        return bt_trade_fee

    def get_list_of_trading_pairs(self):
        response = self._request_without_params(GET, SPOT_TRADING_PAIRS_LIST)
        return json.loads(response.content)['data']['symbols']

    def get_spot_ticker_details(self, symbol: str):
        response = self._request_with_params(GET, SPOT_TICKER_DETAILS, {'symbol': symbol})
        data = json.loads(response.content)["data"]
        return CurrencyDetailed(**data)

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
                kline_object = Kline(date_time, open, high, low, close, volume, last_price, quote_volume,
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
                kline_object = Kline(date_time, open, high, low, close, volume, last_price, quote_volume,
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
            data = json.loads(response.content)['data']
            for depth in data['buys']:
                amount = depth["amount"]
                total = depth["total"]
                price = depth["price"]
                count = depth["count"]
                buys.append(BitmartSpotBuySells(amount, total, price, count))
            for depth in data['sells']:
                amount = depth["amount"]
                total = depth["total"]
                price = depth["price"]
                count = depth["count"]
                sells.append(BitmartSpotBuySells(amount, total, price, count))
            time_stamp = data['timestamp']
            return BitmartDepth(buys, sells, time_stamp)
        elif Market.FUTURES:
            response = self._request_with_params(GET, FUTURES_MARKET_DEPTH, param)
            data = json.loads(response.content)['data']
            asks = []
            bids = []
            for depth in data['asks']:
                price = depth[0]
                quantity = depth[1]
                quantity_above = depth[2]
                asks.append(BitmartFuturesAskBids(price, quantity, quantity_above))
            for depth in data['bids']:
                price = depth[0]
                quantity = depth[1]
                quantity_above = depth[2]
                bids.append(BitmartFuturesAskBids(price, quantity, quantity_above))
            time_stamp = data['timestamp']
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
            order_pos.date_time = datetime.fromtimestamp(int(position["timestamp"]) / 1000)
            order_pos.current_fee = float(position["current_fee"])
            order_pos.open_date_time = datetime.fromtimestamp(int(position["open_timestamp"]) / 1000)
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
    def cancel_order(self, symbol: str, order_id="", market=Market.SPOT) -> bool:
        param = {
            'symbol': symbol,
            'order_id': str(order_id),
        }
        url = SPOT_CANCEL_ORDER if market == Market.SPOT else FUTURES_CANCEL_ORDER
        self._request_with_params(POST, url, param, Auth.SIGNED)

        return True

    # POST https://api-cloud.bitmart.com/spot/v1/cancel_orders
    def cancel_all_orders(self, symbol: str, side: SpotSide, market=Market.SPOT) -> bool:
        param = {
            'symbol': symbol,
            'side': side.value
        }
        url = SPOT_CANCEL_ALL_ORDERS if market == Market.SPOT else FUTURES_CANCEL_ALL_ORDERS

        self._request_with_params(POST, url, param, Auth.SIGNED)

        return True

    # GET https://api-cloud.bitmart.com/spot/v2/order_detail
    def update_order_details(self, order: BitmartOrder) -> BitmartOrder:
        param = {
            'order_id': order.order_id
        }
        market = order.market
        if market == Market.FUTURES:
            param["symbol"] = order.symbol
            response = self._request_with_params(GET, FUTURES_ORDER_DETAIL, param, Auth.KEYED)
            data = json.loads(response.content)['data']
            order.price = data['price']
            order.order_status = data['state']
            order.side = data['side']
            order.order_type = data['type']
            order.leverage = data['leverage']
            order.open_type = data['open_type']
            order.price_avg = data['deal_avg_price']
            order.size = data['deal_size']
            order.create_time = data['create_time']
            order.update_time = datetime.fromtimestamp(
                int(data['update_time']) / 1000)

        elif market == Market.SPOT:
            response = self._request_with_params(GET, SPOT_GET_ORDER_DETAILS, param, Auth.KEYED)
            data = json.loads(response.content)['data']
            order.price = data['price']
            order.order_status = data['status']
            order.side = data['side']
            order.order_type = data['type']
            order.leverage = "Not applied for Spot Market"
            order.open_type = data['open_type']
            order.price_avg = data['price_avg']
            order.size = data['size']
            order.notional = data['notional']
            order.filled_notional = data['filled_notional']
            order.filled_size = data['filled_size']
            order.unfilled_volume = data['unfilled_volume']
            order.order_mode = data['order_mode']
            order.create_time = data['create_time']
            order.update_time = datetime.now()

        return order

    # GET https://api-cloud.bitmart.com/spot/v3/orders
    def get_order_history(self, symbol: str, market=Market.SPOT,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None):

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
                     price: Optional[float] = None, size: Optional[float] = 0, order_type: OrderType = OrderType.LIMIT,
                     market: Market = Market.SPOT, leverage: Optional[int] = 1,
                     open_type: OrderOpenType = OrderOpenType.ISOLATED,
                     client_order_id: Optional[str] = None):

        bm_order = BitmartOrder(symbol, side, size, price, market, order_type, leverage, open_type, client_order_id)
        if market == Market.SPOT or market == Market.SPOT_MARGIN:
            if order_type == OrderType.LIMIT_MAKER:
                raise NotImplemented
            elif order_type == OrderType.IOC:
                raise NotImplemented
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
        raise NotImplemented

    def get_futures_contracts_details(self)->List[BitmartFutureContract]:
        response = self._request_with_params(GET, FUTURES_CONTRACT_DETAILS, params={})
        result: List[BitmartFutureContract] = []
        for item in json.loads(response.content)['data']['symbols']:
            contract = BitmartFutureContract(**item)
            result.append(contract)

        return result

    def update_open_interest(self, bt_currency: CurrencyDetailed) -> CurrencyDetailed:
        response = self._request_with_params(GET, FUTURES_OPEN_INTEREST, {'symbol': bt_currency.symbol})
        data = json.loads(response.content)['data']
        bt_currency.open_interest_datetime = data["timestamp"]
        bt_currency.open_interest = data["open_interest"]
        bt_currency.open_interest_value = data["open_interest_value"]
        bt_currency.funding_rate = data["rate_value"]
        bt_currency.funding_rate_datetime = data["timestamp"]

        return bt_currency

    def get_account_balance(self, market=Market.SPOT):
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
                margin_acc_symbol.buy_enabled = ticker["buy_enabled"] == "true"
                margin_acc_symbol.sell_enabled = ticker["sell_enabled"] == "true"
                margin_acc_symbol.liquidate_price = float(ticker["liquidate_price"])
                margin_acc_symbol.liquidate_rate = float(ticker["liquidate_rate"])
                wallet_currencies.append(margin_acc_symbol)

        bitmart_wallet = BitmartWallet(wallet_currencies)

        return bitmart_wallet
