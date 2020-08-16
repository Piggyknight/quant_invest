# -*- coding:utf-8 -*-
from currency_account import *
from currency_exchange_rate import *

print("[ut]Start testing CurrencyAccount...")
# 1. init the exchange rate
exchange_rate = CurrencyExchangeRate()
exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.rmb, 7.2)

# 2. init the account and put 100 usd
account = CurrencyAccount(exchange_rate)
account.AddMoney(E_MONEY_TYPE.usd, 100)

assert 5 == len(account.cur_deposit), "len of deposit: %d" % len(account.cur_deposit)

val = account.Total(E_MONEY_TYPE.rmb)
assert 720.0 == val, "Total money in rmb: %f" % val

val = account.Total(E_MONEY_TYPE.usd)
assert 100.0 == val, "Total money in usd: %f" % val

print("[ut]Success")
