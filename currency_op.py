# -*- coding:utf-8 -*-
from currency_account import *
from currency_op_param import *


class OpSell:
    def __init__(self, account: CurrencyAccount):
        self.account = account
        return

    def Do(self, op_param: OpParam):
        # 1. calculate trading cost

        # 2. update the account money

        # 3. push order into stack
        self.account.PushOrder(op_param)

        return

class OpCloseOutSell:
    def __init__(self, account: CurrencyAccount):
        self.account = None
        return

    def Do(self, op_param: OpParam):
        # 1. get corresponding sell order

        # 2. profit calculation
        #    - sell gain = sell order's amount * sell order's price * rate(target -> src)
        #    - buy cost = sell order's amount * curret price
        #    - profit = sell gain - buy cost

        # 3. update corresponding src money

        return


class OpBuy:
    def __init__(self, account: CurrencyAccount):
        self.account = account
        return

    def Do(self, op_param: OpParam):
        # 1. calculate trading cost

        # 2. update the account money

        # 3. push order into stack
        self.account.PushOrder(op_param)
        return



class OpCloseOutSell:
    def __init__(self, account: CurrencyAccount):
        self.account = None
        return

    def Do(self, data, orders):
        # 1. get corresponding buy order

        # 2. profit calculation
        #    - buy cost = buy order's amount * buy order's price
        #    - sell gain = buy order's amount * current price * rate(targe -> src)
        #    - profit = sell gain - buy cost

        # 3. update corresponding src money

        return