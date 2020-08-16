# -*- coding:utf-8 -*-
from currency_account import *
from currency_op_param import *


class TradingInfo:
    trading_fee = 0.03


class OpSell:
    def __init__(self, account: CurrencyAccount, trading_info: TradingInfo):
        self.account = account
        self.trading_info = trading_info
        return

    def Do(self, op_param: OpParam):
        # 1. calculate trading cost
        cur_val = op_param.price * op_param.amount
        trading_fee = cur_val * self.trading_info.trading_fee

        # 2. update the account money
        self.account.AddMoney(op_param.src_money, -trading_fee)

        # 3. push order into stack
        self.account.PushOrder(op_param)
        return


class OpCloseOutSell:
    def __init__(self, account: CurrencyAccount,trading_info: TradingInfo):
        self.account = account
        self.trading_info = trading_info

    def Do(self, op_param: OpParam):
        # 1. get corresponding sell order
        order = self.account.PopOrder()
        if order is None:
            print("[op]Closeout sell order failed, order is none")
            return

        if order.op_type is not E_OP_TYPE.sell:
            print("[op]Closeout failed, last order is not sell, type is %d", order.op_type)
            return

        # 2. profit calculation
        #    - sell gain = sell order's amount * sell order's price
        #    - buy cost = sell order's amount * curret price
        #    - profit = sell gain - buy cost
        sell_gain = order.amount * order.price
        buy_cost = order.amount * op_param.price
        cost = buy_cost * self.trading_info.trading_fee
        profit = sell_gain - buy_cost - cost
        print("[op]Clostout sell: sell_gain=%f, buy_cost=%f, profit=%f" % (sell_gain, buy_cost, profit))

        # 3. update corresponding src money
        self.account.AddMoney(op_param.src_money, profit)

        # 4. push order into account history
        self.account.PushHistory(op_param)


class OpBuy:
    def __init__(self, account: CurrencyAccount,trading_info: TradingInfo):
        self.account = account
        self.trading_info = trading_info

    def Do(self, op_param: OpParam):
        # 1. calculate trading cost
        cur_val = op_param.price * op_param.amount
        trading_fee = cur_val * self.trading_info.trading_fee

        # 2. update the account money
        self.account.AddMoney(op_param.src_money, -trading_fee)

        # 3. push order into stack
        self.account.PushOrder(op_param)
        return


class OpCloseOutBuy:
    def __init__(self, account: CurrencyAccount,trading_info: TradingInfo):
        self.account = account
        self.trading_info = trading_info

    def Do(self, op_param: OpParam):
        # 1. get corresponding buy order
        order = self.account.PopOrder()
        if order is None:
            print("[op]Closeout buy order failed, order is none")
            return

        if order.op_type is not E_OP_TYPE.buy:
            print("[op]Closeout failed, last order is not buy, type is %d", order.op_type)
            return

        # 2. profit calculation
        #    - sell gain = sell order's amount * sell order's price
        #    - buy cost = sell order's amount * curret price
        #    - profit = sell gain - buy cost
        buy_cost = order.amount * order.price
        sell_gain = order.amount * op_param.price
        cost = sell_gain * self.trading_info.trading_fee
        profit = sell_gain - buy_cost - cost
        print("[op]Clostout buy: sell_gain=%f, buy_cost=%f, profit=%f" % (sell_gain, buy_cost, profit))

        # 3. update corresponding src money
        self.account.AddMoney(op_param.src_money, profit)

        # 4. push order into account history
        self.account.PushHistory(op_param)
