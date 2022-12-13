from hftcryptoapi.bitmart import Bitmart
from hftcryptoapi.bitmart.ws_base import BitmartWs
from hftcryptoapi.bitmart.constants import *
from datetime import datetime, timedelta
import time
import asyncio

if __name__ == '__main__':

    api_key = "11bcfe6d2d3a5f0016efc5108a1c64e678201b27"
    secret_key = "953bb4129c221485d71c89cea38a0497e8ca8b36b18e0fdddbcdc45a7c27f35b"
    memo = "artemtest"
    to_time = datetime.now()
    from_time = to_time - timedelta(days=10)
    symbol = "BTCUSDT"
    symbol_eth = "ETHUSDT"
    client = Bitmart.BitmartClient(api_key, secret_key, memo)
    [print(b) for b in client.get_acount_balance(market=Market.FUTURES).currencies]
    print(client.get_order_history(symbol=symbol_eth, market=Market.FUTURES))
    print(client.get_list_of_trading_pairs())
    print(client.get_symbol_kline(symbol=symbol, tf=TimeFrame.tf_1h, market=Market.FUTURES,
                                  from_time=from_time, to_time=to_time))
    print(client.get_symbol_kline(symbol="BTC_USDT", tf=TimeFrame.tf_1h, market=Market.SPOT,
                                  from_time=from_time, to_time=to_time))
    print(client.get_futures_position_details(symbol_eth))
    print(client.get_symbol_recent_trades("BTC_USDT"))



    # ------------- WEB SOCKETS
    client.subscribe_private(Market.FUTURES, [BtFuturesTPrivatePositionChannel])
    client.subscribe_private(Market.FUTURES, [BtFuturesTPrivateAssetChannel], ['ETH', 'USDT'])
    client.subscribe_public(Market.FUTURES, [BtFuturesTickerChannel])
    client.subscribe_public(Market.FUTURES, [BtFuturesSocketKlineChannels.K_LINE_CHANNEL_1MIN], [symbol, symbol_eth])

    client.start_websockets(Market.FUTURES, on_message=lambda message: print(f' {message}'))

    # ------------- ORDER
    order = client.submit_order(market=Market.FUTURES, symbol="ETHUSDT", side=FuturesSide.BUY_OPEN_LONG,
                                size=1, price=70, open_type=OrderOpenType.CROSS)
    client.cancel_order(order.symbol, order_id=order.order_id, market=Market.FUTURES)

    print(client.submit_order(market=Market.FUTURES, symbol="ETHUSDT", order_type=OrderType.MARKET,
                              side=FuturesSide.BUY_OPEN_LONG,
                              size=5, open_type=OrderOpenType.CROSS))
    positions = client.get_futures_position_details(symbol_eth)
    amount = [p for p in positions if p.symbol == "ETHUSDT" and p.current_amount !=0][0].current_amount
    print(client.submit_order(market=Market.FUTURES, symbol="ETHUSDT", order_type=OrderType.MARKET,
                              side=FuturesSide.SELL_CLOSE_LONG,
                              size=amount, open_type=OrderOpenType.CROSS))
    # -------------

    time.sleep(10)
    #
    #
    #
    #
    #
    # print(client.get_user_trade_record(symbol="TRX_USDT", order_mode="all"))
