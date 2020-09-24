# -*- coding:utf-8 -*-
import os
from currency_conf_strategy import *

print("[ut]Start testing CurrencyConf...")
cur_path = os.path.dirname(__file__)
conf_path = cur_path + '/test_conf/currency_conf.ini'
conf = CurrencyConf()
conf.Load(conf_path)


'''
[Strategy]
buy_time = 22
bottom_duration = 24
bottom_search_range = 48
top_duration = 24
top_search_range = 48
stop_loss = 100
stop_profit = 100
wait_duration = 24
time_unit = 2
'''

assert 22 == conf.buy_time, "buy time load error: %d" % conf.buy_time
assert 24 == conf.bottom_duration, "bottom duration error"
assert 48 == conf.bottom_search_range, "bottom search range error"
assert 24 == conf.top_duration, "top duration error"
assert 48 == conf.top_search_range, "top search range error"
assert 150 == conf.stop_loss, "stop loss error"
assert 24 == conf.wait_duration, "wait duration error"
assert E_TIME_UNIT.hour.value == conf.time_unit, "time unit error"

print("[ut]Success")