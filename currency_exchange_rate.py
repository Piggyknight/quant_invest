# -*- coding:utf-8 -*-
from enum import IntEnum


class E_MONEY_TYPE(IntEnum):
    usd = 0
    rmb = 1
    eur = 2
    yan = 3
    max = 4

    def __str__(self):
        return '{0}'.format(self.value)

    __repr__ = __str__


def GetKey(src: E_MONEY_TYPE, target: E_MONEY_TYPE) -> int:
    return int(src) << 16 | int(target)


class CurrencyExchangeRate:
    def __init__(self):
        self.rate_db = {}

    def Add(self, src: E_MONEY_TYPE, target: E_MONEY_TYPE, rate: float):
        # 1. defensive check
        if 0.0 == rate:
            return

        if src == target:
            return

        # 2. get key from src % target type
        #    we'll add two key, src => target & target => src
        key1 = GetKey(src, target)
        key2 = GetKey(target, src)

        # 3. check if key is duplicated
        if key1 in self.rate_db.keys():
            print("[account]Key1 %d already exist, value: %f src: %s, target: %s" % (key1, self.rate_db[key1], src, target))

        if key2 in self.rate_db.keys():
            print("[account]Key2 %d already exist, value: %f src: %s, target: %s" % (key2, self.rate_db[key2], src, target))

        # 4. add key into the rate_db
        self.rate_db[key1] = rate
        self.rate_db[key2] = 1.0 / rate
        return

    def GetExchangeRate(self, src: E_MONEY_TYPE, target: E_MONEY_TYPE) -> float:
        """
            output currency exchange from src money type to target money type
        """
        # 1. if src == target, just return 1.0
        if src == target:
            return 1.0

        # 2. get key from src & target type
        key = GetKey(src, target)

        # 3. check if exist the key from the db
        if key not in self.rate_db.keys():
            print("[account]Key %d not exist, src: %s, target: %s" % (key, src, target))
            return 0.0

        # 4. output rate if exist
        return self.rate_db[key]

