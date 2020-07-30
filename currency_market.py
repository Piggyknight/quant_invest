# -*- coding:utf-8 -*-

from typing import List
from currency_db import *


class CurrencyMarket:
    C_FILE_PATH_FORMAT = "./data/%d.csv"

    # handle the currency db, and basic order operation
    def __init__(self):
        self.orders = {}
        self.db = CurrencyDb()
        self.cur_idx = 0

    def Init(self, years: List[int]):
        """
        :param years: list of yeas to simulate 
        :return: error during init 
        """
        # 1. loop the list of int years
        for year in years:
            # 2. use year to create file path
            file_path = self.C_FILE_PATH_FORMAT.format(year)

            # 3. load file into db
            is_success = self.db.Load(file_path)
            print("[market]Load db: %s, result: %d", file_path, is_success)

        return

    def NextData(self) -> CurrencyRow:
        # 1. safe check
        if self.db is None:
            print("[market]db is null")
            return None

        # 2. return next CurrencyRow, update the counter
        row = self.db.Get(self.cur_idx)
        self.cur_idx = self.cur_idx + 1

        return row
