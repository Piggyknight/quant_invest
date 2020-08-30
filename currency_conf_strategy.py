# -*- coding:utf-8 -*-
from enum import Enum
import os.path
import configparser


class E_TIME_UNIT(Enum):
    minute = 1
    hour = 2
    day = 3


class CurrencyConf:
    """
         - _buy_time: when to buy in 24 hour format, exp: 12, 18, 23
         - _bottom_duration: how long should we check if we hit the bottom, unit is hour
         - _bottom_search_range: how long should we trace back to calculate the bottom, unit is hour
         - _top_duration: how long should we check if we above the top, unit is hour
         - _top_search_range: how long should we trace back to calculate the top, unit is hour
         - _stop_loss: the point to stop loss
         - _stop_profit the point to stop profit
         - _wait_duration: how long should we wait to close out the former order, unit is hour
         - _time_unit: the time unity, we use this transfer time to data idx

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
        if not os.path.exists(file_path):
            print("[conf]Configuration file %s not found." % file_path)
            return

        # 2. create ConfigParser & load file_path file
        print("[conf]Start Parsing file: %s" % file_path)
        config = configparser.ConfigParser()
        config.read(file_path)

        # 3. find [Strategy] section
        strategy = config['Strategy']

        # 4. get all the data one by one and set into member
        self.buy_time = int(strategy['buy_time'])
        self.bottom_duration = int(strategy['bottom_duration'])
        self.bottom_search_range = int(strategy['bottom_search_range'])
        self.top_duration = int(strategy['top_duration'])
        self.top_search_range = int(strategy['top_search_range'])
        self.stop_loss = float(strategy['stop_loss'])
        self.stop_profit = float(strategy['stop_profit'])
        self.wait_duration = float(strategy['wait_duration'])
        self.time_unit = int(strategy['time_unit'])
        return
