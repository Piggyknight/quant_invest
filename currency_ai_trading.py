# -*- coding:utf-8 -*-

import types
from currency_db import *
from currency_db_search import *
from currency_conf import *



'''
基本策略是:制定时间段内
	- 每天固定时间点买入（最好自己可以调时间点，比如：0:00，10:00），
	- 如果过去24小时没有创造48小时内的最低点（也就是没有底部突破）那就买多，否则就卖空；
	- 如果过去24小时有创造48小时内的高点，那就买多。买入时，设置上下100点的波动（+-50）止盈和止损，
	- 如果昨天的买盘没有触及止盈止损线，那第二天买盘的时候自动平仓，继续第二天的操作。看看这样下来一年的结果是赚几个点

    可调参数:
		- 使用起始年日 格式: 2019.01.01
		- 使用结束年日: 格式: 2019.01.02
		- 每天买入时间点: 24进制时间, 单位小时
		- 过去多少时间内没有底部突破: 单位小时
		- 过去多少时间内作为最低点的统计: 单位小时
		- 过去多少时间内没有高点突破: 单位小时
		- 过去多少时间内作为最高点的统计: 单位小时
		- 止损点
		- 止盈点
		- 买入后多少小时平仓
		- 每次交易平均点差

'''
class AiTrading:
    def __init__(self):
        self._last_data = []
        self._data_num = 0
        self._buy_time = None
        self._buy_amount = 1
        self._last_bottom = 0
        self._last_top = 0
        self._conf = None

    def Set(currency_conf):
        self._conf = currency_conf
        return

    def Process(self, data):
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return

        # 2. check if data is enough
        if len(_last_data) < _data_num:
            return

        # 3. convert time conf to idx in the row


        # 3. check if hit the bottom
        bottom = SearchBottom(self._last_data, )


        #4. check if hit the top


        #5. generate command list

        #6. generate stop profit & stop loss triggers

        return
        