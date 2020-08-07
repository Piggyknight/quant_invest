# -*- coding:utf-8 -*-

from currency_exchange_rate import *


class CurrencyAccount:
    def __init__(self, exchange_rate: CurrencyExchangeRate):
        self.op_history = []
        self.cur_deposit = {}


    def AddMoney(self):
        """
            Given input op list, hanlder all the opdata
        """

    def Total(self, money_type: E_MONEY_TYPE) -> float:
        """
            - according to the input money type,
            - calculate all the money in the account according to the currency exchange rate
        """
        return 0.0
