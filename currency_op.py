# -*- coding:utf-8 -*-

from enum import Enum

class E_OpType(Enum):
    buy = 0
    sell = 1
    close_out = 2

class IdGenerator:
    def __init__(self):
        self._cur_id = 0
        return

    def GetId(self):
        self._cur_id += 1
        return self._cur_id

class OpSell:
    def __init__(self, id_gen):
        self._id_gen = id_gen
        return

    def Do(self, data, orders):
        #1. validate data & orders

        #2. create sell order

        #3. put into orders
        return

class OpBuy:
    def __init__(self, id_gen):
        self._id_gen = id_gen
        return

    def Do(self, data, orders):
        #1. validate data & orders

        #2. create buy order

        #3. put into orders
        return


class OpCloseOut:
    def __init__(self, id_gen):
        return

    def Do(self, data, orders):
        #1. validate data & orders

        #2. using id in the data to remove orders

        return
