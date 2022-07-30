import hmac
import time
from requests import Request, Session


class FTX:
    api_key = ''
    secret_key = ''
    sub_account = None
    FTX_REST_API = 'https://ftx.com/api'

    def __init__(self, api_key, secret_key, sub_account=None, FTX_REST_API=None):
        print('init')
        self.api_key = api_key
        self.secret_key = secret_key
        self.sub_account = sub_account

        if FTX_REST_API:
            self.FTX_REST_API = FTX_REST_API

    def send_request(self, endpoint, method, json=None, params=None):
        ts = int(time.time() * 1000)
        request = Request(method, self.FTX_REST_API + endpoint)

        if json:
            request.json = json

        if params:
            request.params = params

        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()

        if prepared.body:
            signature_payload += prepared.body

        signature = hmac.new(self.secret_key.encode(), signature_payload, 'sha256').hexdigest()

        prepared.headers['FTX-KEY'] = self.api_key
        prepared.headers['FTX-SIGN'] = signature
        prepared.headers['FTX-TS'] = str(ts)

        if self.sub_account:
            prepared.headers['FTX-SUBACCOUNT'] = self.sub_account

        session = Session()
        response = session.send(prepared)

        return response.json()

    def get_positions(self):
        """
        :return:
        {
            "success": true,
            "result": [
                {
                    "cost": -31.7906,
                    "cumulativeBuySize": 1.2,
                    "cumulativeSellSize": 0.0,
                    "entryPrice": 138.22,
                    "estimatedLiquidationPrice": 152.1,
                    "future": "ETH-PERP",
                    "initialMarginRequirement": 0.1,
                    "longOrderSize": 1744.55,
                    "maintenanceMarginRequirement": 0.04,
                    "netSize": -0.23,
                    "openSize": 1744.32,
                    "realizedPnl": 3.39441714,
                    "recentAverageOpenPrice": 135.31,
                    "recentBreakEvenPrice": 135.31,
                    "recentPnl": 3.1134,
                    "shortOrderSize": 1732.09,
                    "side": "sell",
                    "size": 0.23,
                    "unrealizedPnl": 0,
                    "collateralUsed": 3.17906
                }
            ]
        }
        """
        return self.send_request('/positions?showAvgPrice=true', 'GET')

    def get_account_information(self):
        """
        :return:
        {
            "success": true,
            "result": {
                "backstopProvider": true,
                "collateral": 3568181.02691129,
                "freeCollateral": 1786071.456884368,
                "initialMarginRequirement": 0.12222384240257728,
                "leverage": 10,
                "liquidating": false,
                "maintenanceMarginRequirement": 0.07177992558058484,
                "makerFee": 0.0002,
                "marginFraction": 0.5588433331419503,
                "openMarginFraction": 0.2447194090423075,
                "takerFee": 0.0005,
                "totalAccountValue": 3568180.98341129,
                "totalPositionSize": 6384939.6992,
                "username": "user@domain.com",
                "positions": [
                    {
                        "cost": -31.7906,
                        "entryPrice": 138.22,
                        "future": "ETH-PERP",
                        "initialMarginRequirement": 0.1,
                        "longOrderSize": 1744.55,
                        "maintenanceMarginRequirement": 0.04,
                        "netSize": -0.23,
                        "openSize": 1744.32,
                        "realizedPnl": 3.39441714,
                        "shortOrderSize": 1732.09,
                        "side": "sell",
                        "size": 0.23,
                        "unrealizedPnl": 0
                    }
                ]
            }
        }
        """
        return self.send_request('/account', 'GET')

    def get_balances(self):
        """
        :return:
        {
            "success": true,
            "result": [
                {
                    "coin": "USDTBEAR",
                    "free": 2320.2,
                    "spotBorrow": 0.0,
                    "total": 2340.2,
                    "usdValue": 2340.2,
                    "availableWithoutBorrow": 2320.2
                }
            ]
        }
        """
        return self.send_request('/wallet/balances', 'GET')

    def get_open_orders(self, market: str = None):
        """
        :parameter market: "ETH-PERP" or "ETH/USDT"

        :returns: {
            "success": true,
            "result": {
                "createdAt": "2019-03-05T09:56:55.728933+00:00",
                "filledSize": 10,
                "future": "XRP-PERP",
                "id": 9596912,
                "market": "XRP-PERP",
                "price": 0.306525,
                "avgFillPrice": 0.306526,
                "remainingSize": 31421,
                "side": "sell",
                "size": 31431,
                "status": "open",
                "type": "limit",
                "reduceOnly": false,
                "ioc": false,
                "postOnly": false,
                "clientId": null,
                "liquidation": False
            }
        }
        """
        return self.send_request('/orders', 'GET', params={'market': market})

    def get_orders_history(self, market=None):
        """
        market : None | str
            None - All orders

            "ETH-PERP" - orders of "ETH-PERP" instrument


        :returns: {
            "success": true,
            "result": [
                {
                    "avgFillPrice": 10135.25,
                    "clientId": null,
                    "createdAt": "2019-06-27T15:24:03.101197+00:00",
                    "filledSize": 0.001,
                    "future": "BTC-PERP",
                    "id": 257132591,
                    "ioc": false,
                    "market": "BTC-PERP",
                    "postOnly": false,
                    "price": 10135.25,
                    "reduceOnly": false,
                    "remainingSize": 0.0,
                    "side": "buy",
                    "size": 0.001,
                    "status": "closed",
                    "type": "limit"
                },
            ],
            "hasMoreData": false,
        }
        """

        return self.send_request(f'/orders/history', 'GET', params={'market': market})

    def get_trigger_orders(self, market=None):
        """
        market : None | str
            None - All trigger orders

            "ETH-PERP" - trigger orders of "ETH-PERP" instrument


        :returns:
        {
            "success": true,
            "result": [
                {
                    "createdAt": "2019-03-05T09:56:55.728933+00:00",
                    "error": null,
                    "future": "XRP-PERP",
                    "id": 50001,
                    "market": "XRP-PERP",
                    "orderId": null,
                    "orderPrice": null,
                    "reduceOnly": false,
                    "side": "buy",
                    "size": 0.003,
                    "status": "open",
                    "trailStart": null,
                    "trailValue": null,
                    "triggerPrice": 0.49,
                    "triggeredAt": null,
                    "type": "stop"
                    "orderType": "market",
                     "filledSize": 0,
                    "avgFillPrice": null,
                    "retryUntilFilled": false
                }
            ]
        }
        """

        return self.send_request(f'/conditional_orders', 'GET', params={'market': market})

    def get_twap_orders(self, market=None, status=None):
        """
        market : None or str
            None - All TWAP orders

            "ETH-PERP" - TWAP orders of "ETH-PERP" instrument

        status : None or str
            None - All TWAP orders
            "running" - TWAP orders with status running

        :returns
        {
            "success": true,
            "result": [
                {
                    "id": 50001,
                    "createdAt": "2019-03-05T09:56:55.728933+00:00",
                    "status": "running",
                    "market": "XRP-PERP",
                    "side": "buy",
                    "size": 1.003,
                    "durationSeconds": 600,
                    "maxSpread": 0.01,
                    "maxIndividualOrderSize": 5.0,
                    "maxDistanceThroughBook": 0.1,
                    "randomizeSize": false
                    "filledSize": 0.5,
                    "avgFillPrice": 5000,
                }
            ]
        }
        """

        return self.send_request(f'/twap_orders', 'GET', params={'market': market, 'status': status})

    def place_order(
            self,
            market: str,
            side: str,
            type: str,
            size: float,
            price: float = None,
            reduceOnly: bool = False,
            ioc: bool = False,
            postOnly: bool = False,
            clientId: str = None,
            rejectOnPriceBand: bool = False,
            rejectAfterTs: int = None
    ):
        """
        :param market: "ETH-PERP" or "ETH/USDT"
        :param side: "buy" or "sell"
        :param price: 0.306525 or None on market
        :param type: "limit" or "market"
        :param size: 31431.05
        :param reduceOnly: True or False
        :param ioc: True or False
        :param postOnly: True or False
        :param clientId: "3005422e-5906-466f-933b-bf28913aa32f" or None
        :param rejectOnPriceBand: True or False
        :param rejectAfterTs: 1234567 or None
        :return:
        {
            'result': {
                'avgFillPrice': None,
                'clientId': None,
                'createdAt': '2022-07-27T05:25:40.531060+00:00',
                'filledSize': 0.0,
                'future': 'TRX-PERP',
                'id': 166473993086,
                'ioc': False,
                'liquidation': None,
                'market': 'TRX-PERP',
                'postOnly': False,
                'price': 0.01,
                'reduceOnly': False,
                'remainingSize': 4.0,
                'side': 'buy',
                'size': 4.0,
                'status': 'new',
                'type': 'limit'
            },
            'success': True
        }

        """

        data = {
            'market': market,
            'side': side,
            'price': price,
            'type': type,
            'size': size,
            'reduceOnly': reduceOnly,
            'ioc': ioc,
            'postOnly': postOnly,
            'clientId': clientId,
            'rejectOnPriceBand': rejectOnPriceBand,
            'rejectAfterTs': rejectAfterTs,
        }

        if type == 'limit' and not price:
            raise Exception('Price is required on limit order')

        response = self.send_request('/orders', 'POST', json=data)
        return response

    def place_trigger_order(
            self,
            market: str,
            side: str,
            size: float,
            triggerPrice: float=None,
            orderPrice: float=None,
            trailValue: float = None,
            retryUntilFilled=False,
            reduceOnly=False,
            type: str = 'stop',
    ):

        """
        :param market: "ETH-PERP" or "ETH/USDT"
        :param side: "buy" or "sell"
        :param size: 4.2
        :param type: "stop", "trailingStop", "takeProfit"; default is "stop"
        :param reduceOnly: optional; default is false
        :param retryUntilFilled: Whether or not to keep re-triggering until filled. optional, default True for market orders
        :param triggerPrice: Required for stop loss and take profit orders
        :param orderPrice: Required for stop loss and take profit orders. None for market order
        :param trailValue: Required for trailing stop; negative for "sell"; positive for "buy"
        :return:
        {
            "success": true,
            "result": {
                "createdAt": "2019-03-05T09:56:55.728933+00:00",
                "future": "XRP-PERP",
                "id": 9596912,
                "market": "XRP-PERP",
                "triggerPrice": 0.306525,
                "orderId": null,
                "side": "sell",
                "size": 31431,
                "status": "open",
                "type": "stop",
                "orderPrice": null,
                "error": null,
                "triggeredAt": null,
                "reduceOnly": false,
                "orderType": "market",
                "retryUntilFilled": false,
            }
        }
        """

        data = {
            'market': market,
            'side': side,
            'size': size,
            'type': type,
            'reduceOnly': reduceOnly,
            'retryUntilFilled': retryUntilFilled,
            'triggerPrice': triggerPrice,
            'orderPrice': orderPrice,
            'trailValue': trailValue,
        }

        response = self.send_request('/conditional_orders', 'POST', json=data)
        return response

    def place_twap_order(
            self,
            market: str,
            side: str,
            size: float,
            durationSeconds,
            randomizeSize: bool = False,
            maxSpread: float = None,
            maxIndividualOrderSize: float = None,
            maxDistanceThroughBook: float = None
    ):

        """
        :param market: "ETH-PERP" or "ETH/USDT"
        :param side: "buy" or "sell"
        :param size: 4.2
        :param durationSeconds:
        :param randomizeSize: Boolean
        :param maxSpread: 0.01
        :param maxIndividualOrderSize: 0.01
        :param maxDistanceThroughBook: 0.01
        :return:
        {
            "success": true,
            "result": [
                {
                    "id": 50001,
                    "createdAt": "2019-03-05T09:56:55.728933+00:00",
                    "status": "running",
                    "market": "XRP-PERP",
                    "side": "buy",
                    "size": 1.003,
                    "durationSeconds": 600,
                    "maxSpread": 0.01,
                    "maxIndividualOrderSize": 5.0,
                    "maxDistanceThroughBook": 0.1,
                    "randomizeSize": false
                    "filledSize": 0.5,
                    "avgFillPrice": 5000,
                }
            ]
        }
        """

        data = {
            'market': market,
            'side': side,
            'size': size,
            'durationSeconds': durationSeconds,
            'randomizeSize': randomizeSize,
            'maxSpread': maxSpread,
            'maxIndividualOrderSize': maxIndividualOrderSize,
            'maxDistanceThroughBook': maxDistanceThroughBook,
        }

        response = self.send_request('/twap_orders', 'POST', json=data)
        return response
