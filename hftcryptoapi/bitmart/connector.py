import json
from .api_client import PyClient
from datetime import datetime
from .constants import *
from .bitmart_objects import *
from pydantic import BaseModel

class AccountConnector(BaseModel, validate_assignment=True):
    def __init__(self, exchange=Exchange.BITMART):
        self.exchange = exchange

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
            #print(json.loads(response.content)['data'])
            for currency in json.loads(response.content)['data']:
                ticker = currency['currency']
                available = currency['available_balance']
                frozen = currency['frozen_balance']
                position_deposit = currency['position_deposit']
                equity = currency['equity']
                unrealized = currency['unrealized']
                wallet_currencies.append(WalletItem(ticker, available, frozen, position_deposit, equity, unrealized, wallet_type=Market.FUTURES))
        elif market == Market.SPOT_MARGIN:
            response = self._request_without_params(GET, ACCOUNT_MARGIN_DETAILS, Auth.KEYED)
            for ticker in json.loads(response.content)['data']['symbols']:
                margin_acc_symbol = MarginAccountSymbol(ticker["symbol"])
                margin_acc_symbol.risk_rate = float(ticker["risk_rate"])
                margin_acc_symbol.risk_level= int(ticker["risk_level"])
                margin_acc_symbol.buy_enabled = True if ticker["buy_enabled"] == "true" else False
                margin_acc_symbol.sell_enabled = True if ticker["sell_enabled"] == "true" else False
                margin_acc_symbol.liquidate_price = float(ticker["liquidate_price"])
                margin_acc_symbol.liquidate_rate = float(ticker["liquidate_rate"])
                wallet_currencies.append(margin_acc_symbol)
        
        bitmart_wallet = BitmartWallet(wallet_currencies)

        return bitmart_wallet#self._request_without_params(GET, ACCOUNT_BALANCE, Auth.KEYED)

    