# -*- coding:utf-8 -*-
from currency_op_param import *


class CurrencyAccount:
    def __init__(self, exchange_rate: CurrencyExchangeRate):
        # 1. init
        self.exchange_rate = exchange_rate

        # 2 ini all money type
        self.cur_deposit = {}
        for val in E_MONEY_TYPE:
            self.cur_deposit[val] = 0.0

        # 3. init order
        self.orders = []

    def PushOrder(self, op_param: OpParam):
        self.orders.append(op_param)

    def PopOrder(self)-> OpParam:
        # 1. avoid empty stack
        if 0 == len(self.orders):
            return None

        return self.orders.pop()

    def PeekOrder(self) -> OpParam:
        if len(self.orders) == 0:
            return empty_op

        return self.orders[-1]

    def HasOrders(self) -> bool:
        return 0 != len(self.orders)

    def AddMoney(self, money_type: E_MONEY_TYPE, val: float):
        if money_type not in self.cur_deposit.keys():
            print("[account]Money type %d not exist", money_type)
            return

        self.cur_deposit[money_type] += val

    def GetMoney(self, money_type: E_MONEY_TYPE) -> float:
        if money_type not in self.cur_deposit.keys():
            print("[account]Money type %d not exist", money_type)
            return 0.0

        return self.cur_deposit[money_type]

    def Total(self, money_type: E_MONEY_TYPE) -> float:
        """
            - according to the input money type,
            - calculate all the money in the account according to the currency exchange rate
        """
        print("[account]Cal all the money into type: %s", money_type)
        sum = 0.0
        # 1. loop all the money type
        for key, value in self.cur_deposit.items():
            # 2. get corresponding exchange rate
            exchange_rate = self.exchange_rate.GetExchangeRate(key, money_type)

            if 0.0 == exchange_rate:
                continue

            # 3. sum all the money
            convert = exchange_rate * value
            sum += convert

            # 4 print debug info
            print("[account]Money Type: %d, rate: %f,  cur_reposit: %f, convert=%f , sum=%f"
                  % (key, exchange_rate, value, convert, sum))

        return sum
