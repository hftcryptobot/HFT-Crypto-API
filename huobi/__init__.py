from datetime import datetime
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode


class Huobi:
    api_key = ''
    secret_key = ''
    account_id = None
    HUOBI_BASE_URI = 'api.huobi.pro'

    def __init__(self, api_key, secret_key, account_id=None, HUOBI_BASE_URI=None):
        print('init')
        self.api_key = api_key
        self.secret_key = secret_key

        if account_id:
            self.account_id = account_id

        if HUOBI_BASE_URI:
            self.HUOBI_BASE_URI = HUOBI_BASE_URI

    def request(self, method, endpoint, params={}, data=None):
        timestamp = str(datetime.utcnow().isoformat())[0:19]

        params = urlencode({
            'AccessKeyId': self.api_key,
            'SignatureMethod': 'HmacSHA256',
            'SignatureVersion': '2',
            'Timestamp': timestamp,
            **params
        })

        pre_signed_text = method + '\n' + self.HUOBI_BASE_URI + '\n' + endpoint + '\n' + params
        hash_code = hmac.new(self.secret_key.encode(), pre_signed_text.encode(), hashlib.sha256).digest()
        signature = urlencode({'Signature': base64.b64encode(hash_code).decode()})
        url = 'https://' + self.HUOBI_BASE_URI + endpoint + '?' + params + '&' + signature
        response = requests.request(method, url, json=data).json()

        return response

    def get_accounts(self):
        return self.request('GET', '/v1/account/accounts')

    def change_account_id(self, new_account_id):
        self.account_id = new_account_id

    def get_symbols(self):
        """
        :return: {
            "status":"ok",
            "data":[
                {
                    "tags": "",
                    "state": "online",
                    "wr": "1.5",
                    "sc": "ethusdt",
                    "p": [
                        {
                            "id": 9,
                            "name": "Grayscale",
                            "weight": 91
                        }
                    ],
                    "bcdn": "ETH",
                    "qcdn": "USDT",
                    "elr": null,
                    "tpp": 2,
                    "tap": 4,
                    "fp": 8,
                    "smlr": null,
                    "flr": null,
                    "whe": false,
                    "cd": false,
                    "te": true,
                    "sp": "main",
                    "d": null,
                    "bc": "eth",
                    "qc": "usdt",
                    "toa": 1514779200000,
                    "ttp": 8,
                    "w": 999400000,
                    "lr": 5,
                    "dn": "ETH/USDT"
                }
            ],
            "ts":"1641870869718",
            "full":1
        }
        """
        return self.request('GET', '/v2/settings/common/symbols/')

    def get_klines(self, symbol):
        return self.request('GET', '/market/history/kline', {'symbol': symbol})

    def get_balances(self):
        return self.request('GET', f'/v1/account/accounts/{self.account_id}/balance')

    def get_open_orders(self):
        return self.request('GET', '/v1/order/openOrders')

    def cancel_order(self, order_id):
        return self.request('POST', f'/v1/order/orders/{order_id}/submitcancel')

    def place_order(
            self,
            symbol: str,
            type: str,
            amount: float,
            price: float = None,
            source: str = None,
            client_order_id: str = None,
            self_match_prevent: int = None,
            stop_price: float = None,
            operator: str = None,
    ):
        data = {
            'symbol': symbol,
            'type': type,
            'amount': amount,
            'price': price,
            'source': source,
            'client-order-id': client_order_id,
            'self-match-prevent': self_match_prevent,
            'stop-price': stop_price,
            'operator': operator,
            'account-id': self.account_id
        }

        new_data = {}

        for i in data:
            if data[i]:
                new_data[i] = data[i]

        return self.request('POST', f'/v1/order/orders/place', data=new_data)
