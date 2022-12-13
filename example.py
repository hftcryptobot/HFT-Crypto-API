from hftcryptoapi.bitmart import Bitmart
import time

if __name__ == '__main__':

    api_key = "11bcfe6d2d3a5f0016efc5108a1c64e678201b27"
    secret_key = "953bb4129c221485d71c89cea38a0497e8ca8b36b18e0fdddbcdc45a7c27f35b"
    memo = "artemtest"

    clientBitmart = Bitmart.BitmartClient(api_key, secret_key, memo)
    print(clientBitmart.get_acount_balance())

    print(clientBitmart.get_list_of_trading_pairs())

    print(clientBitmart.get_user_trade_record(symbol= "TRX_USDT",  order_mode= "all"))

    print(clientBitmart.spot_submit_market_order(symbol= "ETH_USDT", side= "buy", amount=0.0001))
    print(clientBitmart.spot_submit_market_order(symbol= "ETH_USDT", side= "sell", amount=0.0001))

    print(clientBitmart.spot_submit_limit_order(symbol= "ETH_USDT", side= "buy", size=0.10, price=70, client_order_id=''))

    print(clientBitmart.get_symbol_kline(symbol="GST_USDT", fromTime=int(time.time())-10000, toTime=int(time.time()), step=1))

