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
from hftcryptoapi.bitmart import Bitmart

api_key = ""
secret_key = ""
memo = ""

client = Bitmart(api_key, secret_key, memo, exchange=Exchange.BITMART)
```

## System Status

- Get System Time, returns system time in datetime format.

```
bt_time = client.get_system_time()
```

- Get System Service Status, returns system status

```
bt_staus = client.get_service_status()
```

## Public Market Data

Functions to get info from spot market public API.

- Get Currency List

```
currency_list = client.get_currency_list()
```

- Get List of Trading Pairs, return a list of all trading pairs

```
trading_pairs = client.get_list_of_trading_pairs()
```

- Get List of Spot Symbol Details

```
 symbols_details = client.get_spot_symbols_details()
```

- Get Ticker details by Symbol

```
    symbol_details = client.get_spot_ticker_details("BTC_USDT")
```

- Get K-Line, return Kline object for specified symbol and time period for SPOT and FUTURES markets

```
symbol_klines = client.get_symbol_kline(symbol, fromTime, toTime, step, market = Market.SPOT)
```

- Get Depth
  Returns [buys], [sells] wrapped in SportDepth or FuturesDepth object, depends on market type (Market.SPOT or
  Market.FUTURES)

```
symbol_depth = client.get_symbol_depth(symbol, precision, size, market=Market.SPOT)
```

- Get Recent Trades, returns Trade object for specified symbol and number of trades (by default: 50)

```
bt_trades = client.get_symbol_recent_trades(symbol, N)
```

## Funding Account Data

- Get Account Balance, a unified method for all types of markets (SPOT, MARGIN, FUTURES). Market should be defined.
  Returns list of currencies/positions with attributes unique for each market:

```
result = client.get_account_balance(market=Market.FUTURES)
result = client.get_account_balance(market=Market.SPOT_MARGIN)
[print(b) for b in client.get_account_balance(market=Market.SPOT).items]
```

- Get User Fee Rate

```
fee_rate = client.get_spot_user_fee_rate()
```

- Get Actual Trade Fee Rate

```
bt_trade_fee = client.get_trade_fee_rate(symbol)
```

## Spot/Margin Trading

- Place Spot Order (V2)

```
 order = client.submit_order(market=Market.SPOT, symbol=symbol, side=SpotSide.BUY, size=0.1, price=70)
```

- Place Margin Order

```
 order = client.submit_order(market=Market.SPOT_MARGIN, symbol=symbol, side=SpotSide.BUY, size=0.1, price=70)
```

- Cancel an Order (V3)

```
 client.cancel_order(order)
 # OR
 client.cancel_order_by_id(order.symbol, order_id=order.order_id, market=Market.SPOT)

```

- Cancel All Orders

```
 client.cancel_all_orders(symbol=symbol_spot, market=Market.SPOT, side=SpotSide.BUY)
```

- Get Order Detail (V2), get/update order details

```
 order = get_order_details(symbol, order_id, market)
 order = client.update_order_details(order)
```

- Get User Order History (V3), return list of order objects

```
history = client.get_order_history(symbol=symbol_eth, market=Market.SPOT)
```

### Margin Loan

- Get Trading Pair Borrowing Rate and Amount

```
 rate = client.spot_margin_borrowing_rate(symbol_spot)
```

- Get Borrow Record(Isolated)

```
 b_records = client.spot_margin_get_borrow_record(symbol_spot)
```

- Get Repayment Record(Isolated)

```
 r_records = client.spot_margin_get_repay_record(symbol_spot)
```

- Margin Borrow (Isolated)

```
 borrow_id = client.spot_margin_borrow(symbol_spot, "BTC", 0.005)
```

- Margin Repay (Isolated)

```
 repay_id = client.spot_margin_repay(symbol_spot, "BTC", 0.005)
```

# Futures

## Basic Information

To access methods for Futures account/market methods should have a flag Market.FUTURES passed to.

## Futures Market Data

- Get Futures Open Interest

```
futures_open_interest = client.get_futures_open_interest(symbol)
```

- Get Current Funding Rate for futures

```
 funding_rate = client.get_futures_funding_rate(symbol)
```

- Get List of Futures Contract Details

```
 contracts_details = client.get_futures_contracts_details()
```

## Futures Trading

- Get Futures Position details for a specified contract

```
 client.get_futures_position_details(symbol)
```

- Close Futures Position

```
 client.close_futures_position(symbol=symbol, position_side=Position.SHORT, open_type=OrderOpenType.CROSS)
```

- Get Account Balance - see spot description

- Submit Order - see spot description

- Cancel Order - see spot description

- Cancel All orders - see spot description

- Get Order Detail - see spot description

- Get Order History - see spot description

## WebSockets

- Subscribe to one or many WebSocket events

```
 # SPOT
 client.subscribe_public(Market.SPOT, [BtSpotSocketKlineChannels.K_LINE_CHANNEL_1HOUR,
                                      BtSpotSocketDepthChannels.DEPTH_CHANNEL_5LEVEL,
                                      BtSpotTradeChannel,
                                      BtSpotTickerChannel],
                        symbols=[symbol_spot])
 client.subscribe_private(Market.SPOT, [BtSpotOrderChannel], symbols=[symbol_spot])

 # FUTURES
 client.subscribe_public(Market.FUTURES, [BtFuturesTickerChannel])
 client.subscribe_public(Market.FUTURES, [BtFuturesSocketKlineChannels.K_LINE_CHANNEL_1HOUR,
                                         BtFuturesSocketDepthChannels.DEPTH_CHANNEL_5LEVEL], [symbol])
 client.subscribe_private(Market.FUTURES, [BtFuturesTPrivatePositionChannel])
 client.subscribe_private(Market.FUTURES, [BtFuturesTPrivateAssetChannel], ['ETH', 'USDT'])                                         
```

- Unsubscribe from one or many WebSocket events

```
    client.unsubscribe_private(Market.FUTURES, [BtFuturesTPrivatePositionChannel])
    client.unsubscribe_private(Market.FUTURES, [BtFuturesSocketDepthChannels], [symbol])
```

- Start WebSocket listener for market type

```
 def _on_message(self, msg: Union[WebSocketKline, WebSocketPositionFutures]):
     if type(msg) is WebSocketKline:
         # ...
     else:
         # ..         
 client.start_websockets(market=Market.FUTURES, on_message=_on_message)
 client.start_websockets(Market.SPOT, on_message=_on_message_spot))
```

- Stop and disconnect from WebSockets

```
 client.stop_websockets(Market.FUTURES)
```

# ChangeLog
20.12.2022 Version 1.0.6 - Margin Loan implementation

19.12.2022 Version 1.0.5
