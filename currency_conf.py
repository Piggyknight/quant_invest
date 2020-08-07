# -*- coding:utf-8 -*-

from enum import Enum


class E_TIME_UNIT(Enum):
    minute = 1
    hour = 2
    day = 3


class CurrencyConf:
    """
         - buy_time: when to buy in 24 hour format, exp: 12, 18, 23
         - bottom_duration: how long should we check if we hit the bottom, unit is hour
         - bottom_search_range: how long should we trace back to calculate the bottom, unit is hour
         - top_duration: how long should we check if we above the top, unit is hour
         - top_search_range: how long should we trace back to calculate the top, unit is hour
         - stop_loss: the point to stop loss
         - stop_profit the point to stop profit
         - wait_duration: how long should we wait to close out the former order, unit is hour
         - time_unit: the time unity, we use this transfer time to data idx
         - trade_amount: the amount to buy either sell or buy

         file format in ini:

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
                trade_amount = 100
    """

    def __init__(self):
        self.buy_time = 0
        self.bottom_duration = 0
        self.bottom_search_range = 0
        self.top_duration = 0
        self.top_search_range = 0
        self.stop_loss = 0
        self.stop_profit = 0
        self.wait_duration = 0
        self.time_unit = E_TIME_UNIT.hour
        self.trade_amount = 100

    def Load(self, file_path: str) -> None:
        # 1. check if file_path is exist

        # 2. create ConfigParser & load file_path file

        # 3. find [Strategy] section

        # 4. get all the data one by one and set into member

        return
