# -*- coding:utf-8 -*-

from enum import Enum
from currency_exchange_rate import *


class E_OP_TYPE(Enum):
    none = 0
    buy = 1
    sell = 2
    closeout_buy = 3
    closeout_sell = 4

    def __str__(self):
        return '{0}'.format(self.value)

    __repr__ = __str__


_print_format = 'OpType:%s, price:%d, number:%d, money_type: %d'


class OpParam:
    def __init__(self):
        self.op_type = E_OP_TYPE.none
        self.price = 0
        self.amount = 0
        self.src_money = E_MONEY_TYPE.usd
        self.target_money = E_MONEY_TYPE.eur

    def __str__(self):
        return _print_format % (self.op_type,
                                self.price,
                                self.amount,
                                self.src_money,
                                self.target_money)

    __repr__ = __str__


empty_op = OpParam()
