# -*- coding:utf-8 -*-
from currency_op import *
from currency_db import *
from currency_op_param import *

print("[ut]Start testing currency_op...")
# 1. init the test environment(account, exchange_rate, trading info, OpParam)
# 1.1 init the exchange rate
exchange_rate = CurrencyExchangeRate()
exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur, 1.18)

# 1.2 init the account and put 100 usd
account = CurrencyAccount(exchange_rate)
account.AddMoney(E_MONEY_TYPE.usd, 100)

trading_info = TradingInfo()
trading_info.trading_fee = 0
print("[ut]init account, exchange_rate, trading_info...")

# 1. Test OpSell
print("[ut]Testing OpSell...")
sell_param = OpParam()
sell_param.price = 1.3
sell_param.amount = 100
sell_param.op_type = E_OP_TYPE.sell

op_sell = OpSell(account, trading_info)
op_sell.Do(sell_param)

assert 1 == len(account.orders), "order not pushed correctly: count=%d" % len(account.orders)
assert 1 == len(account.op_history), "history not pushed correctly: count=%d" % len(account.op_history)
assert 100 == account.cur_deposit[E_MONEY_TYPE.usd], "trading fee calc is not correct: cur_usd_repo=%f" \
                                                     % account.cur_deposit[E_MONEY_TYPE.usd]

# 2. Test OpCloseoutSell
print("[ut]Testing OpCloseoutSell...")
close_sell_param = OpParam()
close_sell_param.price = 1.4
close_sell_param.amount = 100
close_sell_param.op_type = E_OP_TYPE.closeout_sell
op_closeout_sell = OpCloseOutSell(account, trading_info)
op_closeout_sell.Do(close_sell_param)

assert 0 == len(account.orders), "order not closedout correctly: count=%d" % len(account.orders)
assert 2 == len(account.op_history), "op_history not append correctly: count=%d" % len(account.op_history)
assert 90 == account.cur_deposit[E_MONEY_TYPE.usd], "profit calc is not correctly: cur_usd_repo=%f" \
                                                    % account.cur_deposit[E_MONEY_TYPE.usd]

# 3. Test OpBuy
print("[ut]Testing OpBuy...")
buy_param = OpParam()
buy_param.price = 1.3
buy_param.amount = 100
buy_param.op_type = E_OP_TYPE.buy

op_buy = OpBuy(account, trading_info)
op_buy.Do(buy_param)

assert 1 == len(account.orders), "order not pushed correctly: count=%d" % len(account.orders)
assert 3 == len(account.op_history), "history not pushed correctly: count=%d" % len(account.op_history)
assert 90 == account.cur_deposit[E_MONEY_TYPE.usd], "trading fee calc is not correct: cur_usd_repo=%f" \
                                                     % account.cur_deposit[E_MONEY_TYPE.usd]

# 4. Test OpCloseoutBuy
print("[ut]Testing OpCloseoutBuy...")
close_buy_param = OpParam()
close_buy_param.price = 1.4
close_buy_param.amount = 100
close_buy_param.op_type = E_OP_TYPE.closeout_sell

op_closeout_buy = OpCloseOutBuy(account, trading_info)
op_closeout_buy.Do(close_buy_param)

assert 0 == len(account.orders), "order not closedout correctly: count=%d" % len(account.orders)
assert 4 == len(account.op_history), "op_history not append correctly: count=%d" % len(account.op_history)
assert 100 == account.cur_deposit[E_MONEY_TYPE.usd], "profit calc is not correctly: cur_usd_repo=%f" \
                                                    % account.cur_deposit[E_MONEY_TYPE.usd]

print("[ut]Success")
