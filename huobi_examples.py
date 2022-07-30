from huobi import Huobi

huobi = Huobi('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# Get all accounts list
accounts = huobi.get_accounts()

if accounts.get('status') == 'ok':
    spot_account = list(filter(lambda i: i['type'] == 'spot', accounts.get('data')))[0]

    huobi.change_account_id(spot_account.get('id'))

# Get open orders
open_orders = huobi.get_open_orders()

# Cancel order by id
cancel_response = huobi.cancel_order('596827573398451')

# Get symbols list
symbols = huobi.get_symbols()

# Get klines list
klines = huobi.get_klines('btcusdt')

# Get balances
balances = huobi.get_balances()

# Place limit order
limit_order_response = huobi.place_order(
    amount=101,
    symbol='trxusdt',
    price=0.05,
    type='buy-limit'
)

# Place marker order
market_order_response = huobi.place_order(
    amount=1,
    symbol='trxusdt',
    type='buy-market'
)
