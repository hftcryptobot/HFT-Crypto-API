from hftcryptoapi.bitmart import Bitmart
from hftcryptoapi.bitmart.data.constants import *
from datetime import datetime, timedelta
import time

if __name__ == '__main__':
    api_key = "11bcfe6d2d3a5f0016efc5108a1c64e678201b27"
    secret_key = "953bb4129c221485d71c89cea38a0497e8ca8b36b18e0fdddbcdc45a7c27f35b"
    memo = "artemtest"
    to_time = datetime.now()
    from_time = to_time - timedelta(days=10)
    symbol = "BTCUSDT"
    symbol_spot = "BTC_USDT"
    symbol_eth = "ETHUSDT"
    client = Bitmart.BitmartClient(api_key, secret_key, memo)
    # GENERAL PUBLIC
    bt_status = client.get_service_status()
    items = client.get_system_time()
    currency_list = client.get_currency_list()
    trading_pairs = client.get_list_of_trading_pairs()
    symbols_details = client.get_spot_symbols_details()
    contracts_details = client.get_futures_contracts_details()
    symbol_details = client.get_spot_ticker_details(symbol_spot)
    kline_steps = client.get_kline_steps() # Not used
    print(client.get_symbol_kline(symbol="BTC_USDT", tf=TimeFrame.tf_1h, market=Market.SPOT,
                                  from_time=from_time, to_time=to_time))
    print(client.get_symbol_kline(symbol=symbol, tf=TimeFrame.tf_1h, market=Market.FUTURES,
                                  from_time=from_time, to_time=to_time))
    bt_trades = client.get_symbol_recent_trades(symbol_spot, N=100)
    depth_futures = client.get_symbol_depth(symbol=symbol_spot, precision=6, size=50, market=Market.SPOT)
    depth_spot = client.get_symbol_depth(symbol=symbol, precision=6, size=50, market=Market.FUTURES)
    futures_open_interest = client.get_futures_open_interest(symbol)
    funding_rate = client.get_futures_funding_rate(symbol)
    [print(b) for b in client.get_account_balance(market=Market.FUTURES).items]
    [print(b) for b in client.get_account_balance(market=Market.SPOT).items]
    fee_rate = client.get_spot_user_fee_rate()
    bt_trade_fee = client.get_spot_trade_fee_rate(symbol_spot)

    # ------------- WEB SOCKETS
    client.subscribe_private(Market.FUTURES, [BtFuturesTPrivatePositionChannel])
    client.subscribe_private(Market.FUTURES, [BtFuturesTPrivateAssetChannel], ['ETH', 'USDT'])
    client.subscribe_public(Market.FUTURES, [BtFuturesTickerChannel])
    client.subscribe_public(Market.FUTURES, [BtFuturesSocketKlineChannels.K_LINE_CHANNEL_1HOUR,
                                             BtFuturesSocketDepthChannels.DEPTH_CHANNEL_5LEVEL], [symbol])

    client.start_websockets(Market.FUTURES, on_message=lambda message: print(f' {message}'))
    client.subscribe_public(Market.SPOT, [BtSpotSocketKlineChannels.K_LINE_CHANNEL_1HOUR,
                                          BtSpotSocketDepthChannels.DEPTH_CHANNEL_5LEVEL,
                                          BtSpotTradeChannel,
                                          BtSpotTickerChannel],
                            symbols=[symbol_spot])
    client.subscribe_private(Market.SPOT, [BtSpotOrderChannel], symbols=[symbol_spot])

    client.start_websockets(Market.SPOT, on_message=lambda message: print(f' {message}'))
    client.wait_for_socket_connection(market=Market.FUTURES)
    client.wait_for_socket_connection(market=Market.SPOT)
    # input("Press any key")
    # client.unsubscribe_private(Market.FUTURES, [BtFuturesTPrivatePositionChannel])
    client.unsubscribe_private(Market.FUTURES, [BtFuturesSocketDepthChannels], [symbol])
    client.stop_websockets(Market.FUTURES)
    client.stop_websockets(Market.SPOT)

    # ------------- ORDER
    order = client.submit_order(market=Market.SPOT, symbol="ETH_USDT", side=SpotSide.BUY, size=0.1, price=70)
    order = client.update_order_details(order)
    client.cancel_order(order)
    order = client.submit_order(market=Market.FUTURES, symbol="ETHUSDT", side=FuturesSide.BUY_OPEN_LONG,
                                size=1, price=70, open_type=OrderOpenType.CROSS)
    client.update_order_details(order)

    client.cancel_order(order)
    order = client.update_order_details(order)

    print(client.submit_order(market=Market.FUTURES, symbol=symbol_eth, order_type=OrderType.MARKET,
                              side=FuturesSide.SELL_OPEN_SHORT,
                              size=1, open_type=OrderOpenType.CROSS))
    positions = client.get_futures_position_details(symbol_eth)
    amount = [p for p in positions if p.symbol == "ETHUSDT" and p.current_amount != 0][0].current_amount

    print(client.close_futures_position(symbol=symbol_eth, position_side=Position.SHORT, open_type=OrderOpenType.CROSS))
    print(client.submit_order(market=Market.SPOT, symbol=symbol_spot, order_type=OrderType.MARKET,
                              side=SpotSide.BUY,
                              size=10))
    print(client.submit_order(market=Market.SPOT, symbol=symbol_spot, order_type=OrderType.MARKET,
                              side=SpotSide.SELL,
                              size=0.00050000))
    # -------------
