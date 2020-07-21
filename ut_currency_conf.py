# -*- coding:utf-8 -*-

from currency_conf import *

conf_path = 'd:\\project\\git\\python_learning_scripts\\quant\\conf\\currency_conf.ini'
conf = CurrencyConf()
conf.Load(conf_path)


'''
[Strategy]
buy_time = 12
bottom_duration = 24
bottom_search_range = 48
top_duration = 24
top_search_range = 48
stop_loss = 100
stop_profit = 100
wait_duration = 24
time_unit = 2
'''
assert 12 == conf._buy_time, "buy time load error"
assert 24 == conf._bottom_duration, "bottom duration error"
assert 48 == conf._bottom_search_range, "bottom search range error"
assert 24 == conf._top_duration, "top duration error"
assert 48 == conf._top_search_range, "top search range error"
assert 100 == conf._stop_loss, "stop loss error"
assert 24 == conf._wait_duration, "wait duration error"
assert E_TimeUnit.hour == conf._time_unit, "time unit error"