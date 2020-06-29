# -*- coding:utf-8 -*-

from currency_db import *
import sys


def _validate(db, start_idx, back_count):
    # 1.1 safe check db is empty
    if 0 == len(db):
        print("[Search]Error: db is empty")
        return -1



    # 1.3 don't support back_count is negative, which means search forward    
    if start_idx - back_count > len(db):
        print("[Search]Error: don't support search forward")
        return -1

    return 0
    
'''
    Search the min close value by given the list of db
        - input: 
            - db: the list of CurrencyRow
            - start_idx: the start search indx
            - back_count: how much idx to search back
            

        - output:
            - -1: error 
            - other value: the bottom close value

'''
def SearchBottom(db, start_idx, back_count):
   # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1
    
    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    #3. find min value
    min_close = sys.float_info.max
    for i in range(begin_idx, start_idx):
        min_close = min(db[i]._close, min_close)

    return min_close

'''
    Search the max close value by given the list of db
        - input: 
            - db: the list of CurrencyRow
            - start_idx: the start search indx
            - back_count: how much idx to search back
            

        - output:
            - -1: error 
            - other value: the bottom close value

'''
def SearchTop(db, start_idx, back_count):
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
        ret = max(db[i]._close, ret)

    return ret


'''
    Search in certain range of the db, there exist a value small than the given threshhold
        - input: 
            - db: the list of CurrencyRow
            - start_idx: the start search indx
            - back_count: how much idx to search back
            - threshold: the value to compare with
            

        - output:
            - -1: error 
            - other value: the idx of the value in db list

'''
def SearchBelow(db, start_idx, back_count, threshold):
    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    #2. find if exist value less then threshold
    idx = -1
    for i in range(begin_idx, start_idx):
        if db[i]._close <= threshold : 
            idx = i
            break

    return idx


'''
    Search in certain range of the db, there exist a value bigger than the given threshhold
        - input: 
            - db: the list of CurrencyRow
            - start_idx: the start search indx
            - back_count: how much idx to search back
            - threshold: the value to compare with
            

        - output:
            - -1: error 
            - other value: the idx of the value in db list

'''
def SearchAbove(db, start_idx, back_count, threshold):
    # 1. safe check
    ret = _validate(db, start_idx, back_count)
    if -1 == ret:
        return -1

    # 2 avoid back count exceed the begin of the list
    begin_idx = start_idx - back_count
    if begin_idx < 0:
        begin_idx = 0

    #2. find if exist value less then threshold
    idx = -1
    for i in range(begin_idx, start_idx):
        if db[i]._close >= threshold : 
            idx = i
            break

    return idx


