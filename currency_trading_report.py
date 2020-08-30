# -*- coding:utf-8 -*-

from currency_op_history import *
from currency_op_param import *

_format = '%s,%d,%f,%f,%f\n'


def ExportTradingReport(history: CurrencyOpHistory) -> []:
    # 1. ouput head
    ret = ["时间, 交易数, 当日利润, 目前总盈利, 剩余资金\n"]

    # 2. pop order from the op_history in
    total_profit = 0
    cur_day = history.history[0].time
    history_in_same_day = []

    for item in history.history:
        # 2.1 collect if is the same day
        if _is_same_day(cur_day, item.time):
            history_in_same_day.append(item)
            continue

        # 2.2 sum the order count, money
        trading_count = len(history_in_same_day)
        cur_day_profit = 0
        for s_item in history_in_same_day:
            cur_day_profit += s_item.money

        # 2.3 cal the left money, total profit
        total_profit += cur_day_profit
        left_money = history.start_money - total_profit

        # 2.4 generate the str
        day_str = '%d.%d.%d' % (cur_day.year, cur_day.month, cur_day.day)
        ret.append(_format % (day_str, trading_count, cur_day_profit, total_profit, left_money))

        # 2.5 update cur_day & temp array
        cur_day = item.time
        history_in_same_day = []

    return ret


def _is_same_day(lh: datetime, rh: datetime) -> bool:
    is_same_year = lh.year == rh.year
    is_same_month = lh.month == rh.month
    i_same_day = lh.day == rh.day

    return is_same_year and is_same_month and i_same_day


