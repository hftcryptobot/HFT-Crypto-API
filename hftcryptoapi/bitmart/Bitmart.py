from .api_client import PyClient
from hftcryptoapi.bitmart.data import *
from typing import Dict, Union, List
from .ws_base import BitmartWs
from typing import Callable
from time import sleep


class BitmartClient(PyClient):

    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, memo: Optional[str] = None,
                 url: str = API_URL, timeout: tuple = TIMEOUT):
        PyClient.__init__(self, api_key, secret_key, memo, url, timeout)
        self.ws_public: Dict[Union[Market], BitmartWs] = {Market.SPOT: BitmartWs(WS_URL, Market.SPOT),
                                                          Market.FUTURES: BitmartWs(CONTRACT_WS_URL, Market.FUTURES)}
        self.ws_private: Dict[Union[Market], BitmartWs] = {
            Market.SPOT: BitmartWs(WS_URL_USER, Market.SPOT, api_key, memo, secret_key),
            Market.FUTURES: BitmartWs(CONTRACT_WS_URL_USER, Market.FUTURES, api_key, memo, secret_key)}

    def subscribe_private(self, market: Market, channels: List[str], symbols: Optional[List[str]] = None):
        self.ws_private[market].subscribe(channels, symbols)

    def subscribe_public(self, market: Market, channels: List[str], symbols: Optional[List[str]] = None):
        self.ws_public[market].subscribe(channels, symbols)

    def unsubscribe_private(self, market: Market, channels: List[str], symbols: Optional[List[str]] = None):
        self.ws_private[market].unsubscribe(channels, symbols)

    def unsubscribe_public(self, market: Market, channels: List[str], symbols: Optional[List[str]] = None):
        self.ws_public[market].unsubscribe(channels, symbols)

    def start_websockets(self, market: Market, on_message: Callable):
        self.ws_public[market].start(on_message)
        self.ws_private[market].start(on_message)

    def stop_websockets(self, market: Market):
        self.ws_public[market].stop()
        self.ws_private[market].stop()

    def wait_for_socket_connection(self, market: Market, is_public: bool = True):
        ws = self.ws_public[market] if is_public else self.ws_private[market]
        while not ws.is_connected:
            sleep(1)

    def get_system_time(self) -> datetime:
        response = self._request_without_params(GET, SYSTEM_TIME)
        server_time = json.loads(response.content)['data']['server_time']
        return datetime.fromtimestamp(server_time / 1000)

    def get_service_status(self) -> List[BitmartService]:
        response = self._request_without_params(GET, SERVICE_STATUS)
        services = []
        for bt_service in json.loads(response.content)['data']['service']:
            title = bt_service["title"]
            service_type = bt_service["service_type"]
            status = bt_service["status"]
            start_time = bt_service["start_time"]
            end_time = bt_service["end_time"]
            services.append(BitmartService(title, service_type, status, start_time, end_time))
        return services

    # Functions for Public Market Data
    def get_currency_list(self):
        bitmart_currencies = []
        response = self._request_without_params(GET, SPOT_CURRENCY_LIST)
        for currency in json.loads(response.content)['data']['currencies']:
            id = currency['id']
            name = currency['name']
            withdraw_enabled = bool(currency['withdraw_enabled'])
            deposit_enabled = bool(currency['deposit_enabled'])
            bitmart_currencies.append(Currency(id, name, withdraw_enabled, deposit_enabled))
        return bitmart_currencies

    def get_spot_user_fee_rate(self) -> BitmartFee:
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

    def get_spot_trade_fee_rate(self, symbol) -> BitmartTradeFee:
        response = self._request_with_params(GET, ACCOUNT_TRADE_FEE, {"symbol": symbol}, Auth.KEYED)
        bt_trade_fee = BitmartTradeFee(symbol)
        data = json.loads(response.content)['data']
        bt_trade_fee.buy_taker_fee_rate = float(data['buy_taker_fee_rate'])
        bt_trade_fee.sell_taker_fee_rate = float(data['sell_taker_fee_rate'])
        bt_trade_fee.buy_maker_fee_rate = float(data['buy_maker_fee_rate'])
        bt_trade_fee.sell_maker_fee_rate = float(data['sell_maker_fee_rate'])

        return bt_trade_fee

    def get_list_of_trading_pairs(self) -> List[str]:
        response = self._request_without_params(GET, SPOT_TRADING_PAIRS_LIST)
        return json.loads(response.content)['data']['symbols']

    def get_spot_symbols_details(self) -> List[BitmartSpotSymbolDetails]:
        response = self._request_without_params(GET, SPOT_TRADING_PAIRS_DETAILS)
        symbols = json.loads(response.content)["data"]['symbols']
        return [BitmartSpotSymbolDetails(**s) for s in symbols]

    def get_spot_ticker_details(self, symbol: str) -> SpotTickerDetails:
        response = self._request_with_params(GET, SPOT_TICKER_DETAILS, {'symbol': symbol})
        data = json.loads(response.content)["data"]
        return SpotTickerDetails(**data)

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
            currency_details = SpotTickerDetails(symbol, last_price, quote_volume_24h, base_volume_24h, high_24h,
                                                 low_24h, open_24h, close_24h, best_ask, best_ask_size, best_bid,
                                                 best_bid_size,
                                                 fluctuation, timestamp)
            list_currency_details.append(currency_details)

        return list_currency_details

    def get_kline_steps(self):
        response = self._request_without_params(GET, SPOT_K_LIE_STEP)
        return json.loads(response.content)['data']['steps']

    def get_symbol_kline(self, symbol: str, from_time: datetime, to_time: datetime, tf: TimeFrame = TimeFrame.tf_1d,
                         market=Market.SPOT) -> List[Kline]:
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

    def get_symbol_depth(self, symbol: str, precision: Optional[int] = None, size: Optional[int] = None,
                         market=Market.SPOT):
        param = {
            'symbol': symbol
        }
        if market == Market.SPOT:
            if precision is not None:
                param['precision'] = precision
            if size is not None:
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

    def get_symbol_recent_trades(self, symbol: str, N: int = 50) -> List[BitmartTrade]:
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

    # Functions for Funding Account Data

    def get_futures_position_details(self, symbol) -> List[OrderPosition]:
        response = self._request_with_params(GET, FUTURES_CURRENT_POSITION, {'symbol': symbol}, Auth.SIGNED)
        order_positions = []
        for position in json.loads(response.content)['data']:
            order_pos = OrderPosition(**position)

            order_positions.append(order_pos)

        return order_positions

    # POST https://api-cloud.bitmart.com/spot/v3/cancel_order
    def cancel_order_by_id(self, symbol: str, order_id="", market=Market.SPOT) -> bool:
        param = {
            'symbol': symbol,
            'order_id': str(order_id),
        }
        url = SPOT_CANCEL_ORDER if market == Market.SPOT else FUTURES_CANCEL_ORDER
        self._request_with_params(POST, url, param, Auth.SIGNED)

        return True

    def cancel_order(self, order: BitmartOrder) -> bool:
        param = {
            'symbol': order.symbol,
            'order_id': str(order.order_id),
        }
        url = FUTURES_CANCEL_ORDER if order.market == Market.FUTURES else SPOT_CANCEL_ORDER
        self._request_with_params(POST, url, param, Auth.SIGNED)

        return True

    # POST https://api-cloud.bitmart.com/spot/v1/cancel_orders
    def cancel_all_orders(self, symbol: str, side: SpotSide, market=Union[Market.SPOT, Market.FUTURES]) -> bool:
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
            order.price = float(data['price'])
            order.order_status = OrderState(data['state'])
            order.side = FuturesSide(data['side'])
            order.order_type = data['type']
            order.leverage = int(data['leverage'])
            order.open_type = OrderOpenType(data['open_type'])
            order.price_avg = float(data['deal_avg_price'])
            order.size = float(data['deal_size'])
            order.create_time = datetime.fromtimestamp(int(data['create_time']) / 1000)
            order.update_time = datetime.fromtimestamp(int(data['update_time']) / 1000)
        else:
            response = self._request_with_params(GET, SPOT_GET_ORDER_DETAILS, param, Auth.KEYED)
            data = json.loads(response.content)['data']
            order.price = float(data['price'])
            order.order_status = data['status']
            order.side = SpotSide(data['side'])
            order.order_type = OrderType(data['type'])
            order.leverage = "Not applied for Spot Market"
            order.price_avg = float(data['price_avg'])
            order.size = float(data['size'])
            order.notional = float(data['notional'])
            order.filled_notional = float(data['filled_notional'])
            order.filled_size = float(data['filled_size'])
            order.unfilled_volume = float(data['unfilled_volume'])
            order.order_mode = OrderMode(data['order_mode'])
            order.create_time = datetime.fromtimestamp(data['create_time'] / 1000)
            order.update_time = datetime.now()

        return order

    def get_order_details(self, symbol: str, order_id: str, market=Market.SPOT) -> BitmartOrder:
        o = BitmartOrder(symbol=symbol, order_id=order_id, market=market)
        return self.update_order_details(o)

    # GET https://api-cloud.bitmart.com/spot/v3/orders
    def get_order_history(self, symbol: str, market=Market.SPOT,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[BitmartOrder]:

        orders = []
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
                bt_order.order_mode = OrderMode(order["order_mode"])
                bt_order.order_type = OrderType(order["type"])
                bt_order.price_avg = order["price_avg"]
                bt_order.order_id = order["order_id"]
                bt_order.notional = order["notional"]
                bt_order.filled_notional = order["filled_notional"]
                bt_order.filled_size = order["filled_size"]
                bt_order.order_status = order["order_status"]
                bt_order.client_order_id = order["client_order_id"]
                orders.append(bt_order)
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
                orders.append(bt_order)

        return orders

    # Unified methods for trading
    def submit_order(self, symbol: str, side: Union[FuturesSide, SpotSide],
                     price: Optional[float] = None, size: Optional[float] = 0, order_type: OrderType = OrderType.LIMIT,
                     market: Market = Market.SPOT, leverage: Optional[int] = 1,
                     open_type: OrderOpenType = OrderOpenType.ISOLATED,
                     client_order_id: Optional[str] = None):

        bm_order = BitmartOrder(symbol, side, size, price, market, order_type, leverage, open_type, client_order_id)
        if market == Market.SPOT:
            response = self._request_with_params(POST, SPOT_PLACE_ORDER, bm_order.param, Auth.SIGNED)
        elif market == Market.SPOT_MARGIN:
            response = self._request_with_params(POST, SPOT_MARGIN_PLACE_ORDER, bm_order.param, Auth.SIGNED)
        else:  # market == Market.FUTURES:
            response = self._request_with_params(POST, FUTURES_SUBMIT_ORDER, bm_order.param, Auth.SIGNED)

        try:
            bm_order.order_id = json.loads(response.content)['data']['order_id']
        except:
            raise APIException(response)

        return bm_order

    def get_futures_contracts_details(self) -> List[BitmartFutureContract]:
        response = self._request_with_params(GET, FUTURES_CONTRACT_DETAILS, params={})
        result: List[BitmartFutureContract] = []
        for item in json.loads(response.content)['data']['symbols']:
            contract = BitmartFutureContract(**item)
            result.append(contract)

        return result

    def get_futures_open_interest(self, symbol: str) -> FuturesOpenInterest:
        response = self._request_with_params(GET, FUTURES_OPEN_INTEREST, {'symbol': symbol})
        data = json.loads(response.content)['data']

        return FuturesOpenInterest(**data)

    def get_futures_funding_rate(self, symbol: str) -> FuturesFundingRate:
        response = self._request_with_params(GET, FUTURES_FUNDING_RATE, {'symbol': symbol})
        data = json.loads(response.content)['data']

        return FuturesFundingRate(**data)

    def get_account_balance(self, market=Market.SPOT) -> BitmartWallet:
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
                margin_acc_symbol = MarginWalletItem(symbol=ticker["symbol"])
                margin_acc_symbol.risk_rate = float(ticker["risk_rate"])
                margin_acc_symbol.risk_level = int(ticker["risk_level"])
                margin_acc_symbol.buy_enabled = ticker["buy_enabled"] == "true"
                margin_acc_symbol.sell_enabled = ticker["sell_enabled"] == "true"
                margin_acc_symbol.liquidate_price = float(ticker.get("liquidate_price", 0) or 0)
                margin_acc_symbol.liquidate_rate = float(ticker["liquidate_rate"])
                margin_acc_symbol.base = ticker['base']
                margin_acc_symbol.quote = ticker['quote']
                wallet_currencies.append(margin_acc_symbol)

        bitmart_wallet = BitmartWallet(wallet_currencies)

        return bitmart_wallet

    def close_futures_position(self, symbol: str, position_side: Position,
                               open_type: OrderOpenType = OrderOpenType.CROSS) -> bool:
        is_cross = open_type == OrderOpenType.CROSS
        order_side = FuturesSide.SELL_CLOSE_LONG if position_side == Position.LONG else FuturesSide.BUY_CLOSE_SHORT
        positions = self.get_futures_position_details(symbol)
        open_positions = [p for p in positions if p.symbol == symbol and p.current_amount != 0]

        result = False
        for p in open_positions:
            if (not is_cross and p.position_cross) or (is_cross and not p.position_cross):
                continue

            size = p.current_amount

            order_open_type = OrderOpenType.CROSS if is_cross and p.position_cross else OrderOpenType.ISOLATED

            self.submit_order(market=Market.FUTURES, symbol=symbol, order_type=OrderType.MARKET,
                              side=order_side,
                              size=size, open_type=order_open_type)
            result = True

        return result

    def spot_margin_borrow(self, symbol: str, currency: str, amount: float) -> str:
        response = self._request_with_params(POST, MARGIN_BORROW,
                                             params=dict(symbol=symbol, currency=currency, amount=amount),
                                             auth=Auth.SIGNED)
        borrow_id = json.loads(response.content)['data']['borrow_id']

        return borrow_id

    def spot_margin_repay(self, symbol: str, currency: str, amount: float) -> str:
        response = self._request_with_params(POST, MARING_REPAY,
                                             params=dict(symbol=symbol, currency=currency, amount=amount),
                                             auth=Auth.SIGNED)
        repay_id = json.loads(response.content)['data']['repay_id']

        return repay_id

    def spot_margin_get_borrow_record(self, symbol: str, borrow_id: Optional[str] = None,
                                      start_time: Optional[datetime] = None,
                                      end_time: Optional[datetime] = None,
                                      records_count: Optional[int] = None) -> List[BorrowRecord]:

        params = dict(symbol=symbol)
        if borrow_id is not None:
            params["borrow_id"] = borrow_id
        if start_time is not None:
            params["start_time"] = int(datetime.timestamp(start_time))
        if end_time is not None:
            params["end_time"] = int(datetime.timestamp(end_time))
        if records_count is not None:
            params["N"] = records_count

        response = self._request_with_params(GET, MARGIN_BORROW_RECORD, params=params, auth=Auth.KEYED)
        return [BorrowRecord(**r) for r in json.loads(response.content)['data']['records']]

    def spot_margin_get_repay_record(self, symbol: str, repay_id: Optional[str] = None,
                                     currency: Optional[str] = None,
                                     start_time: Optional[datetime] = None,
                                     end_time: Optional[datetime] = None,
                                     records_count: Optional[int] = None) -> List[RepayRecord]:

        params = dict(symbol=symbol)
        if repay_id is not None:
            params["repay_id"] = repay_id
        if currency is not None:
            params["currency"] = currency
        if start_time is not None:
            params["start_time"] = int(datetime.timestamp(start_time))
        if end_time is not None:
            params["end_time"] = int(datetime.timestamp(end_time))
        if records_count is not None:
            params["N"] = records_count

        response = self._request_with_params(GET, MARING_REPAYMENT_RECORD, params=params, auth=Auth.KEYED)
        return [RepayRecord(**r) for r in json.loads(response.content)['data']['records']]

    def spot_margin_borrowing_rate(self, symbol: str) -> List[BorrowingRateAndAmount]:
        response = self._request_with_params(GET, MARGIN_TRADING_PAIR_BORROW_RATE_AND_AMOUNT,
                                             params=dict(symbol=symbol), auth=Auth.KEYED)
        return [BorrowingRateAndAmount(**r) for r in json.loads(response.content)['data']['symbols']]