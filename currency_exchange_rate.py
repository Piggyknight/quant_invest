# -*- coding:utf-8 -*-
from enum import Enum

class E_MONEY_TYPE(Enum):
    usd = 0
    rmb = 1
    eur = 2
    yan = 3

    def __str__(self):
        return '{0}'.format(self.value)

    __repr__ = __str__

class CurrencyExchangeRate:
    def __init__(self):
        self.rate_db = {}

    def Add(self, src: E_MONEY_TYPE, target: E_MONEY_TYPE, rate: float):
        # 1. get key from src % target type

        # 2. check if key is duplicated

        # 3. add key into the rate_db

        return

    def GetExchangeRate(self, src: E_MONEY_TYPE, target: E_MONEY_TYPE) -> float:
        """
            output currency exchange from src money type to target money type
        """
        # 1. get key from src & target type


        # 2. check if exist the key from the db

        # 3. output rate if exist
        return 0.0