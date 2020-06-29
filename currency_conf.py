# -*- coding:utf-8 -*-

class E_TimeUnit(Enum):
    minute = 1
    hour = 2
    day = 3

'''
     - _buy_time: when to buy in 24 hour format, exp: 12, 18, 23
     - _bottom_duration: how long should we check if we hit the bottom, unit is hour
     - _bottom_search_range: how long should we trace back to calculate the bottom, unit is hour
     - _top_duration: how long should we check if we above the top, unit is hour
     - _top_search_range: how long should we trace back to calculate the top, unit is hour
     - _stop_loss: the point to stop loss
     - _stop_profit the point to stop profit
     - _wait_duration: how long should we wait to close out the former order, unit is hour
     - _time_unit: the time unity, we use this transfer time to data idx
'''
class CurrencyConf:
    def __init__(self):
        self._buy_time = 0
        self._bottom_duration = 0
        self._bottom_search_range = 0
        self._top_duration = 0
        self._top_search_range = 0
        self._stop_loss = 0
        self._stop_profit = 0
        self._wait_duration = 0
        self._time_unit = E_TimeUnit.hour

    def ResetTimeUnit(self):
        # 1. according to the time unit 


