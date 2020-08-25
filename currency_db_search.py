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


def SearchBottom(db: List[CurrencyRow], start_idx: int, back_count: int) -> float:
    """"
        Search the min close value by given the list of db
            - input:
                - db: the list of CurrencyRow
                - start_idx: the start search indx
                - back_count: how much idx to search back


            - output:
                - -1: error
                - other value: the bottom close value

    """

    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    # 3. find min value
    min_close = sys.float_info.max
    for i in range(begin_idx, start_idx):
        min_close = min(db[i].close, min_close)

    print("[bottom]Find bottom price: %f" % min_close)
    return min_close


def SearchTop(db: List[CurrencyRow], start_idx: int, back_count: int) -> float:
    """
        Search the max close value by given the list of db
            - input:
                - db: the list of CurrencyRow
                - start_idx: the start search indx
                - back_count: how much idx to search back


            - output:
                - -1: error
                - other value: the bottom close value
    """

    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    # 3. find max
    ret = sys.float_info.min
    for i in range(begin_idx, start_idx):
        ret = max(db[i].close, ret)

    print("[top]Find Top price: %f" % ret)
    return ret


def SearchBelow(db: List[CurrencyRow], start_idx: int, back_count: int, threshold: float) -> int:
    """
        Search in certain range of the db, there exist a value small than the given threshold
            - input:
                - db: the list of CurrencyRow
                - start_idx: the start search index
                - back_count: how much idx to search back
                - threshold: the value to compare with


            - output:
                - -1: error
                - other value: the idx of the value in db list

    """

    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    # 2. find if exist value less then threshold
    idx = -1
    for i in range(begin_idx, start_idx):
        if db[i].close <= threshold:
            idx = i
            break

    if -1 != idx:
        print("[below]Find %d(%s) is below threshold %f, " % (idx, db[idx].time, threshold))
    return idx


def SearchAbove(db: List[CurrencyRow], start_idx: int, back_count: int, threshold: float) -> int:
    """
        Search in certain range of the db, there exist a value bigger than the given threshold
            - input:
                - db: the list of CurrencyRow
                - start_idx: the start search indx
                - back_count: how much idx to search back
                - threshold: the value to compare with


            - output:
                - -1: error
                - other value: the idx of the value in db list

    """

    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    # 2. find if exist value less then threshold
    idx = -1
    for i in range(begin_idx, start_idx):
        if db[i].close >= threshold:
            idx = i
            break

    if -1 != idx:
        print("[above]Find %d(%s) is above threshold %d" % (idx, db[idx].time, threshold))
    return idx
