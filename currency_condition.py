# -*- coding:utf-8 -*-
import types
from datetime import datetime,timedelta
from currency_db import *
import copy

class CondStopBelow:
    """
       Check if high, open, low, close in CurencyRow is below threshold
    """
    def __init__(self, threshold: float):
        self.threshold = threshold

    def IsTrigger(self, data: CurrencyRow) -> bool:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False
        
        # 2. check if open, high, low, close is above stop_point
        if data.high <= self.threshold or \
            data.open <= self.threshold or \
            data.low <= self.threshold or \
            data.close <= self.threshold:
            return True

        return False


class CondStopAbove:
    """
       Check if high, open, low, close in CurencyRow is above threshold
    """
    def __init__(self, threshold: float):
        self.threshold = threshold

    def IsTrigger(self, data: CurrencyRow) -> bool:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False
        
        # 2. check if open, high, low, close is above stop_point
        if data.high >= self.threshold or \
            data.open >= self.threshold or \
            data.low >= self.threshold or \
            data.close >= self.threshold:
            return True

        return False


class CondBuyTime:
    """
       - Check if buy time is reached
       - midnight should be 24 not zeor
    """
    def __init__(self, expire_hour: int, wait_duration: int):
        self.expire_hour = expire_hour
        self.wait_duration = wait_duration
        self.trading_time = None

    def IsTrigger(self, data: CurrencyRow) -> bool:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False

        # 2 if everything is ok, then we check the time if it reached the buy time
        # 2.1 init the buy time
        if self.trading_time is None:
            self.trading_time = data.time.replace(hour=self.expire_hour)
        # print("[cond]trading time: %s,  expire_hour: %s" % (self.trading_time, self.expire_hour))

        # 2.2 calculate the timedelta
        dt = self.trading_time - data.time
        # print("[cond]cur time: %s, delta_time: %s" % (data.time, dt))

        # 3. check if data time is expire, then update the day
        if dt <= timedelta(seconds=0):
            # 3.1 add wait duration
            delta_time = timedelta(hours=self.wait_duration)
            self.trading_time += delta_time

            # 3.2 if weekday is saturday or sunday, then add unitl next day
            while True:
                weekday = self.trading_time.weekday()
                if weekday != 5 and weekday != 6:
                    break
                self.trading_time += delta_time

            # 3.3 skip chrismas & 1.1
            if self.trading_time.month == 12 and self.trading_time.day == 25:
                self.trading_time += delta_time
            elif self.trading_time.month == 1 and self.trading_time.day == 1:
                self.trading_time += delta_time

            print("[cond]Time reached, update trading_time: %s" % self.trading_time)
            return True

        return False


class CondDuration:
    """
       - Check if duration is reached
       - start time is updated by out sider
    """
    def __init__(self, wait_duration: int):
        self.wait_duration = wait_duration
        self.trading_time = None

    def IsTrigger(self, data: CurrencyRow) -> bool:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False

        # 2 if everything is ok, then we check the time if it reached the buy time
        # 2.1 init the buy time
        if self.trading_time is None:
            return False

        # 2.2 calculate the timedelta
        dt = data.time - self.trading_time

        # 3. check if data time is expire, then update the day
        delta_time = timedelta(hours=self.wait_duration)

        if dt >= delta_time:
            return True

        return False
