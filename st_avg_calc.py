# -*- coding:utf-8 -*-
from typing import List
from currency_db import *
import sys


def _validate(db: List[CurrencyRow], start_idx: int, back_count: int) -> int:
    # 1.1 safe check db is empty
    if 0 == len(db):
        print("[Search]Error: db is empty")
        return -1

    # 1.3 don't support back_count is negative, which means search forward
    if start_idx - back_count > len(db):
        print("[Search]Error: don't support search forward")
        return -1

    return 0


def CalcAvg(db: List[CurrencyRow], start_idx: int, back_count: int) -> float:
    """
        Given input db list, from start idx, calc average according to the back_count
    """
    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    # 3. calc average
    sum_all = 0.0
    for i in range(begin_idx, start_idx):
        sum_all += db[i].close

    avg = sum_all / back_count

    #print("Calc avg: %.5f" % avg)
    return avg

