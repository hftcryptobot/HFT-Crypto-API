# HFT CRYPTO API-BitMart
Python module for Bitmart SDK

## Installation

``` pip install hftcryptoapi```

# Spot Market
## Introduction

``` from hftcryptoapi.bitmart import Bitmart ```

## Basic Information

Initialise an instance of Bitmart client:
```
from hftcryptoapi import BrokerClient

api_key = ""
secret_key = ""
memo = ""

broker_client  = BrokerClient(api_key, secret_key, memo, exchange=Exchange.BITMART)
```

## System Status
Service calls to check Bitmart API service status. Initate a new Bitmart service instance to call methods.
```
form hftcryptoapi import BitmartService
```
- Get System Time, returns system time in datetime format.
```
bitmart_service = BitmartService()
bt_time = bitmart_service.get_system_time()
```
- Get System Service Status, returns system status
```
bitmart_service = BitmartService()
bt_staus = bitmart_service.get_service_status()
```

## Public Market Data
Functions to get info from spot market public API.
Functions are wrapped in class MarketDataAgent and return object (or arrays) as defined in description.
```
from hftcryptoapi import MarketDataAgent
```
- Get Currency List
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
currency_list = market_agent.get_currency_list()
```

-  Get List of Trading Pairs, return a list of all trading pairs
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
[currency_list] = market_agent.get_list_of_trading_pairs()
```
- Get List of Trading Pair Details, returns currency details as Currency  object
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
currency_details = market_agent.get_traiding_pair_detail()
```

- Get Ticker of All Pairs (V2), returns list of currency details as a Currency object
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
[currency_details] = market_agent.get_all_trading_pair_details()
```

- Get K-Line Step, return klines as list
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
k_lines = market_agent.get_kline_steps()
```

- Get K-Line, return Kline object for specified symbol and time period for SPOT and FUTURES markets
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
symbol_klines = market_agent.get_symbol_kline(symbol, fromTime, toTime, step, market = Market.SPOT)
```

- Get Depth
Returns [buys], [sells] wrapped in SportDepth or FuturesDepth object, depends on market type (Market.SPOT or Market.FUTURES)
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
symbol_depth = market_agent.get_symbol_depth(symbol, precision, size)
```

- Get Recent Trades, returns Trade object for specified symbol and number of trades (by default: 50)
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
bt_trades = market_agent.get_symbol_recent_trades(symbol, N)
```

- Get Futures Openinterest
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
futures_open_interest = market_agent.get_open_interest(Currency:object, market=Market.FUTURES)
```

- Get Current Funding Rate for futures
```
market_agent = MarketDataAgent(exchange=Exchange.BITMART)
bt_trades = market_agent.get_current_funding_rate(Currency:object, market=Market.FUTURES)
```


## Funding Account Data
Set of functions to manage used account:
```
from hftcryptoapi import BrokerClient
```
-  Get Account Balance, a unified method for all types of markets (SPOT, MARGIN, FUTURES). Market should be defined. Returns list of currencies/positions with attributes unique for each market:
```
broker_client  = BrokerClient(...)
spot_currencies = broker_client.get_acount_balance(symbol, market=Market.SPOT)
spotmargin_currencies = broker_client.get_acount_balance(symbol, market=Market.SPOT_MARGIN)
future_contracts = broker_client.get_acount_balance(symbol, market=Market.FUTURES)
```

- Get Basic Fee Rate, return account user fee wrapped in Fee object
```
broker_client  = BrokerClient(...)
bt_fee = broker_client.get_basic_fee_rate()
```
- Get Actual Trade Fee Rate, return trade fee rate for specified symbol wrapped in TradeFee object
```
broker_client  = BrokerClient(...)
bt_trade_fee = broker_client.get_trade_fee_rate(symbol)
```


## Spot /Margin Trading
- Place Spot Order (V2)
```
broker_client  = BrokerClient(...)
spot_order = broker_client.create_order(symbol, side, type, market=Market.SPOT)
order_id = broker_client.submit_order(spot_order)
```

- Place Margin Order
```
broker_client  = BrokerClient(...)
margin_order = broker_client.create_order(symbol, side, type, market=Market.SPOT_MARGIN)
order_id = broker_client.submit_order(margin_order)
```
- Cancel an Order (V3), cancel order in the account manager specified by order ID
```
broker_client.cancel_order(order)
```
- Cancel All Orders, cancels all orders in the account manager
```
broker_client.cancel_all_orders(symbol, side, market=Market.SPOT)
broker_client.cancel_all_orders(symbol, side, market=Market.FUTURES)
```
- Get Order Detail (V2), gets order details for specified order object
```
bt_order_with_details = broker_client.get_order_details(order:Order)
```
- Get User Order History (V3), return order histore for user account, return list of order objects
```
[all_orders] = broker_client .get_order_history(symbol, status)
```

# USD-M Futures

## Basic Information
To access methods for Futures account/market methods should have a flag Market.FUTURES passed to.

## Futures Market Data
- Get Contract Details, create contract object for Futures market (contract)
```
broker_client  = BrokerClient(...)
futures_contract = broker_client .get_contract(symbol, side, type, market=Market.FUTURES)
```

## Futures Trading
- Submit Order - see spot description

- Cancel Order - see spot description

- Cancel All orders - see spot description

- Get Order Detail - see spot description

- Get Order History - see spot description

- Get Current Position Detail - see spot description


## WebSocket Subscription

- Get Websocket Data, returns objects from websocket subscription  
```
callback implementation
```

## Error Codes
Error code has be taken from API web-page and implemented into Error objects.

# ChangeLog
25.11.2022 Version 0.1
