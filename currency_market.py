# -*- coding:utf-8 -*-

from currency_db import *



# hanlde the currency db, and basic order operation
class CurrencyMarket:
    def __init__(self):
        self._orders={}
        self._db = CureencyDb()
        self._cur_idx = 0
        self._id_gen = IdGenerator()
        self._cmd_list = []

    # input
    # - years: list of yeas to simulate
    # - no return
    def Init(self, years):
        # 1. loop the list of int yeras

        # 2. use year to create filepath

        # 3. load file into db

        # 4. create cmd list

        # 5. reset order_id

        return

    def NextData(self):
        # 1. safe check
        if None == self._db:
            return None

        # 2. return next CurrencyRow, update the counter

    # process given list of cmds, return the list of orders
    def ExecuteCmd(self, cmds):

        for cmd in cmds:
            _cmd_list[cmd._type].Do(cmd.data, self._orders)

        return False





