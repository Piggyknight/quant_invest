# -*- coding:utf-8 -*-


class OpSell:
    def __init__(self, id_gen):
        self._id_gen = id_gen
        self.account = None
        return

    def Do(self, data, orders):
        #1. validate data & orders

        #2. create sell order

        #3. put into orders
        return


class OpBuy:
    def __init__(self, id_gen):
        self._id_gen = id_gen
        self.account = None
        return

    def Do(self, data, orders):
        #1. validate data & orders

        #2. create buy order

        #3. put into orders
        return


class OpCloseOut:
    def __init__(self, id_gen):
        self.account = None
        return

    def Do(self, data, orders):
        #1. validate data & orders

        #2. using id in the data to remove orders

        return
