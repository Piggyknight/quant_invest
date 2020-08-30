# -*- coding:utf-8 -*-
import types
from typing import List
from datetime import datetime
from currency_op_param import *


class HistoryItem:
    def __init__(self, time: datetime, op_param: OpParam, money: float):
        self.op_param = op_param
        self.money = money
        self.time = time


class CurrencyOpHistory:
    def __init__(self, start_money: float):
        self.start_money = start_money
        self.end_money = 0
        self.history = List[HistoryItem]

    def AddHistory(self,  time: datetime, op_param: OpParam, money: float):
        self.history.append(HistoryItem(time, op_param, money))

