# -*- coding:utf-8 -*-

from enum import Enum


class E_OP_TYPE(Enum):
    none = 0
    buy = 1
    sell = 2
    close_out = 3

    def __str__(self):
        return '{0}'.format(self.value)

    __repr__ = __str__


_print_format = 'OpType:%s, price:%d, number:%d'


class OpParam:
    def __init__(self):
        self.op_type = E_OP_TYPE.none
        self.price = 0
        self.amount = 0

    def __str__(self):
        return _print_format % (self.op_type,
                                self.price,
                                self.amount)

    __repr__ = __str__


empty_op = OpParam()
