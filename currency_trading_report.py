# -*- coding:utf-8 -*-

from currency_account import *


def ExportTradingReport(account: CurrencyAccount) -> str:
    """
        file format would in following format

        op
    """
    # 1. pop order from the op_history in account

    # 2. check order type, if it is closeout, then pop one more order

    # 3. calculate profit

    # 4. print two op_param

    # 5. print sell_gain, buy cost, trading fee etc

    # 6. output whole string
    return ""



