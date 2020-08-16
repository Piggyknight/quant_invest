# -*- coding:utf-8 -*-
from currency_exchange_rate import *

print("[ut]Start Testing CurrencyExchangeRate", end="...")
currency_rate = CurrencyExchangeRate()
currency_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur, 0.85)
currency_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.rmb, 7.01)


assert 4 == len(currency_rate.rate_db)
assert 0.85 == currency_rate.GetExchangeRate(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur)
assert 1.0 / 0.85 == currency_rate.GetExchangeRate(E_MONEY_TYPE.eur, E_MONEY_TYPE.usd)
assert 1.0 / 7.01 == currency_rate.GetExchangeRate(E_MONEY_TYPE.rmb, E_MONEY_TYPE.usd)

print("Success")
