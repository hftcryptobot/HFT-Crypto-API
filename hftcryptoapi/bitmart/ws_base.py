import websockets
from .bitmart_utils import sign, get_timestamp, get_kline_time
import threading
import asyncio
from hftcryptoapi.bitmart.data import *
import logging
from typing import List, Optional


# logging.getLogger().setLevel(logging.INFO)


class BitmartWs(object):
    def __init__(self, uri: str, market: Market, api_key=None, memo=None, secret_key=None):
        self.uri = uri
        self.ws: websockets.WebSocketClientProtocol = None
        self.loop = asyncio.new_event_loop()
        self.is_connected = False
        self.market = market
        self.api_key = api_key
        self.memo = memo
        self.secret_key = secret_key
        self.ws_thread = threading.Thread(target=self._run_sync, args=())
        self.params = []
        self.on_message = None
        self.is_stop = False
        self.name_of_group = "group" if market == market.FUTURES else "table"

    def _get_subscription_list(self, channels: List[str], symbols: Optional[List[str]] = None):
        params = []
        if symbols is None:
            params += channels
        else:
            for c in channels:
                for s in symbols:
                    params.append(f'{c}:{s}')
        return params

    def _mange_socket_subscriptions(self, channels: List[str], symbols: Optional[List[str]] = None,
                                    subscribe: bool=True):
        params = self._get_subscription_list(channels, symbols)
        self.params += params
        if self.is_connected:
            if subscribe:
                asyncio.run(self._subscribe(params))
            else:
                asyncio.run(self._unsubscribe(params))

    def subscribe(self, channels: List[str], symbols: Optional[List[str]] = None):
        self._mange_socket_subscriptions(channels, symbols, True)

    def unsubscribe(self, channels: List[str], symbols: Optional[List[str]] = None):
        self._mange_socket_subscriptions(channels, symbols, False)

    def _run_sync(self):
        asyncio.run(self._socket_loop())

    def start(self, on_message=None):
        self.on_message = on_message
        if len(self.params) > 0:
            self.ws_thread.start()
            return True
        self.is_stop = False
        return False

    def stop(self):
        self.is_stop = True
        try:
            if self.is_connected:
                pass
                # self.loop.call_soon_threadsafe(self.loop.stop)
                try:
                    self.loop.run_until_complete(self.ws.close())
                    self.loop.stop()
                except ValueError:
                    pass
            self.ws_thread.join()
        except RuntimeError:
            pass

    def _on_message(self, message):
        try:
            if message.get("errorMessage"):
                raise WebSocketException(message)
            if message.get("action", False):
                logging.debug(message)
            else:
                group = message[self.name_of_group]
                data = message["data"]
                if "/ticker" in group:
                    is_futures = self.market == Market.FUTURES
                    if is_futures:
                        self.on_message(TickerFuturesWebSocket(**data))
                    else:
                        for item in data:
                            ticker = TickerSpotWebSocket(**item)
                            self.on_message(ticker)
                elif "spot/kline" in group:
                    for item in data:
                        kline = WebSocketKline(symbol=item["symbol"], candle=list(item['candle']),
                                               market=self.market)
                        self.on_message(kline)
                elif "futures/kline" in group:
                    items = data['items']
                    for item in items:
                        kline = WebSocketKline(symbol=data["symbol"], candle=list(item.values()),
                                               market=self.market)
                        if self.market == Market.FUTURES:
                            kline.date_time = get_kline_time(BtFuturesSocketKlineChannels(group.split(":")[0]))
                        self.on_message(kline)
                elif "/position" in group:
                    for item in data:
                        self.on_message(WebSocketPositionFutures(**item))
                elif "/asset" in group:
                    self.on_message(WebSocketAssetFutures(**data))
                elif "spot/depth" in group:
                    for item in data:
                        self.on_message(WebSocketDepthSpot(**item))
                elif "futures/depth" in group:
                    self.on_message(WebSocketDepthFutures(**data))
                elif "spot/trade" in group:
                    for item in data:
                        self.on_message(WebSocketTrade(**item))
                elif "spot/order" in group:
                    for item in data:
                        self.on_message(WebSocketOrderProgress(**item))
        except WebSocketException as e:
            raise e
        except Exception as e:
            logging.error(f"WS on message: {e}")

    async def _connect(self):
        while True:
            try:
                if self.is_connected:
                    logging.warning(f"WS {self.market} Closing")
                    await self.ws.close()
                logging.info(f"WS {self.market} Connecting")
                self.ws = await websockets.connect(self.uri, ping_interval=10, ping_timeout=10)
                self.is_connected = True
                logging.info(f"WS {self.market} Connected")
                break
            except TimeoutError:
                logging.error(f"WS {self.market} timeout.")
            except Exception as ex:
                logging.error(f"WS {self.market} exception: {ex}")
                await asyncio.sleep(1)

    async def _read_socket(self):
        try:
            while not self.is_stop:
                message = await self.ws.recv()
                try:
                    for line in str(message).splitlines():
                        self._on_message(json.loads(line))  # await
                except Exception as e:
                    logging.info(f"WS read error {e}")
        except websockets.ConnectionClosedError as e:
            sleep_time = 3
            logging.warning(f"WS {self.market} Connection Error: {e}. Sleep {sleep_time}...")
            await asyncio.sleep(sleep_time)
        except Exception as e:
            if not self.is_stop:
                logging.warning(f"WS {self.market} Connection Lost at {datetime.utcnow()} {e}")

    async def _auth(self):
        if self.api_key is not None:
            timestamp = get_timestamp()
            sign_ = sign(f'{timestamp}#{self.memo}#bitmart.WebSocket', self.secret_key)
            params = {"args": [self.api_key, timestamp, sign_]}
            if self.market is Market.FUTURES:
                params["action"] = "access"
                params["args"].append("web")
            else:
                params["op"] = "login"
            auth_str = json.dumps(params)
            await self.ws.send(auth_str)
            message = await self.ws.recv()

    async def _subscribe(self, params):
        action_name = "action" if self.market == Market.FUTURES else "op"
        await self.ws.send(json.dumps({action_name: "subscribe", "args": params}))

    async def _unsubscribe(self, params):
        action_name = "action" if self.market == Market.FUTURES else "op"
        await self.ws.send(json.dumps({action_name: "unsubscribe", "args": params}))

    async def _socket_loop(self):
        asyncio.set_event_loop(self.loop)
        while not self.is_stop:
            await self._connect()
            await self._auth()
            await self._subscribe(self.params)
            await self._read_socket()
            self.is_connected = False
            # await self.ws.close()
