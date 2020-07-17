# -*- coding:utf-8 -*-

from enum import Enum

class E_OpType(Enum):
    none = 0
    buy = 1
    sell = 2
    close_out = 3

class CmdParam:
    def __init__(self):
        self._op_type = E_OpType.none
        self._price = 0
        self._number = 0



