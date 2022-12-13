from typing import Any, Union, Optional, List, Dict
import json
import zlib
import rel
import websockets
# from websocket import WebSocketApp, WebSocket
from .bitmart_utils import sign
import threading
import asyncio
from datetime import datetime
from .bitmart_exceptions import *
from .bitmart_objects import *
from .bitmart_websockets import *

class BitmartWs(object):
    def __init__(self, uri: str, market: Market, api_key=None, memo=None, secret_key=None):
        self.uri = uri
        self.market = market
        self.api_key = api_key
        self.memo = memo
        self.secret_key = secret_key
        self.private_thread = threading.Thread(target=self._run_sync, args=())
        self.params = []
        self.on_message = None

    def subscribe(self, channels: List[str], symbols: Optional[List[str]] = None):
        if symbols is None:
            self.params += channels
        else:
            for c in channels:
                for s in symbols:
                    self.params.append(f'{c}:{s}')

    def _run_sync(self):
        asyncio.run(self._socket_loop())

    def start(self, on_message=None):
        self.on_message = on_message
        if len(self.params) > 0:
            self.private_thread.start()

    def _on_message(self, message):
        try:
            if message.get("action", False):
                print(message)
            else:
                # print(message)
                group = message["group"]
                data = message["data"]
                if "/ticker" in group:
                    self.on_message(TickerWebSocket(**data))
                elif "/kline" in group:
                    items = data['items']
                    for item in items:
                        self.on_message(WebSocketKline(symbol=data["symbol"], candle=list(item.values()),
                                                       kline_type=self.market))
                elif "/position" in group:
                    for item in data:
                        self.on_message(WebSocketPositionFutures(**item))
                elif "/asset":
                    self.on_message(WebSocketAssetFutures(**data))
        #             {'group': 'futures/position', 'data': [{'symbol': 'ETHUSDT', 'hold_volume': '1', 'position_type': 1, 'open_type': 2, 'frozen_volume': '0', 'close_volume': '0', 'hold_avg_price': '1326.03', 'close_avg_price': '0', 'open_avg_price': '1326.03', 'liquidate_price': '0', 'create_time': 1670949709045, 'update_time': 1670949709045}]}
        except Exception as e:
            print(e)

    async def _socket_loop(self):
        try:
            async with websockets.connect(self.uri, ping_interval=10, ping_timeout=10) as websocket:
                print(f'[websockets] Connected {self.uri}')
                if self.api_key is not None:
                    timestamp = str(int(datetime.now().timestamp() * 1000))
                    auth = f'{str(timestamp)}#{self.memo}#bitmart.WebSocket'
                    sign_ = sign(auth, self.secret_key)
                    auth_str = json.dumps({"action": "access", "args": [self.api_key, timestamp, sign_, "web"]})
                    await websocket.send(auth_str)
                    message = json.loads(await websocket.recv())
                    if not message.get("success", False):
                        raise AuthException("UNAUTORIZED")

                await websocket.send(json.dumps({"action": "subscribe", "args": self.params}))
                while True:
                    message = await websocket.recv()
                    self._on_message(json.loads(message))
        except Exception as e:
            print(e)

    # def run(self):
    #     try:
    #         self.ws = WebSocketApp(self.uri,
    #                                on_open=self.on_open,
    #                                on_message=self.on_message,
    #                                on_error=self.on_error,
    #                                on_close=self.on_close)
    #         self.ws.run_forever(dispatcher=rel, reconnect=5)
    #
    #     except Exception as e:
    #         print(e)
