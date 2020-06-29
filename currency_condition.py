# -*- coding:utf-8 -*-
import types
from datetime import datetime,timedelta
from currency_db import *

'''
   Check if high, open, low, close in CurencyRow is below threshold
'''
class CondStopLoss:
    def __init__(self):
        self._threshold = 0
        

    def IsOk(self,data):
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False
        
        # 2. check if open, high, low, close is above stop_point
        if data._high <= self._threshold or \
            data._open <= self._threshold or \
            data._low <= self._threshold or \
            data._close <= self._threshold:
            return True

        return False

'''
   Check if high, open, low, close in CurencyRow is above threshold
'''
class CondStopProfit:
    def __init__(self):
        self._threshold = 0
        

    def IsOk(self,data):
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False
        
        # 2. check if open, high, low, close is above stop_point
        if data._high >= self._threshold or \
            data._open >= self._threshold or \
            data._low >= self._threshold or \
            data._close >= self._threshold:
            return True

        return False

'''
   Check if time in CurrencyRow is expire
'''
class CondCloseOut:
    def __init__(self):
        self._expire_data = None

    def IsOk(self, data):
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return False

        # 2. check if data time is expire
        dt = self._expire_data - data._time
        if dt <= timedelta(seconds=0):
            return True

        return False

