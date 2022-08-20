# Python Crypto API to work with different exhcanges (Huobi, Ftx... )
This library is much more than just a  wrapper around the Huobi, FTX standart API's.
1 object = 4 exchanges. You can create bot and use it with different exchanges. 
It aims to make methods quite simple without tons of nuances and oriented on an algo trading developer.

More examples you can find in 
[huobi_examples](https://github.com/hftcryptobot/HFTcryptobot-API/blob/master/huobi_examples.py) / 
[ftx_examples](https://github.com/hftcryptobot/HFTcryptobot-API/blob/master/ftx_examples.py)

# Initial  

Huobi
```
from huobi import Huobi
huobi = Huobi('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
```
FTX
```
from ftx import FTX
ftx = FTX('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
```

# Send orders 

```
#Place limit order
limit_order_response = huobi.place_order(
    amount=101,
    symbol='trxusdt',
    price=0.05,
    type='buy-limit'
)
```
```
#Place marker order
market_order_response = huobi.place_order(
    amount=1,
    symbol='trxusdt',
    type='buy-market'
)
```

```
# Cancel order by id
cancel_response = huobi.cancel_order('596827573398451')
```

# Special Algo Orders 
```
# Place stop loss order:
ftx.place_trigger_order(
    market="ETH/USDT",
    side='sell',
    size=1.2,
    type='stop',
    triggerPrice=100,
)

# Place trailing stop order:
ftx.place_trigger_order(
    market="ETH/USDT",
    side='sell',
    size=1.2,
    type='trailingStop',
    trailValue=-0.05
)

# Place take profit order:
ftx.place_trigger_order(
    market="ETH/USDT",
    side='sell',
    size=1.2,
    type='takeProfit',
    triggerPrice=10000,
)

# Place twap order
ftx.place_twap_order(
    market="ETH/USDT",
    durationSeconds=600,
    size=1,
    side="buy"
)
```
# Get Orders (Open, History)
```
# Get all open orders
ftx.get_open_orders()

# Get all open orders for "ETH-PERP"
ftx.get_open_orders("ETH-PERP")

# Get orders history
ftx.get_orders_history()

# Get orders history for "ETH-PERP"
ftx.get_orders_history("ETH-PERP")

# Get open trigger orders
ftx.get_trigger_orders()

# Get open trigger orders for "ETH-PERP"
ftx.get_trigger_orders("ETH-PERP")

# Get all twap orders
ftx.get_twap_orders()

# Get all twap orders for "ETH-PERP"
ftx.get_twap_orders("ETH-PERP")

# Get all active twap orders for "ETH-PERP"
ftx.get_twap_orders("ETH-PERP", "running")

```
# Other Trading Information 
```
# Get positions list
ftx.get_positions()

# Get account information
ftx.get_account_information()

# Get account balances list
ftx.get_balances()

# Get symbols list
symbols = huobi.get_symbols()

# Get klines list
klines = huobi.get_klines('btcusdt')

```

