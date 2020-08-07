# -*- coding:utf-8 -*-

from typing import List
from currency_db_search import *
from currency_conf import *
from currency_op_param import *
import copy


class AiTrading:
    """
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

    """
    def __init__(self, currency_conf: CurrencyConf) -> None:
        self.last_data = List[CurrencyRow]
        self.data_num = 0
        self.has_bought = False
        self.history_list = []
        self.buy_time = None
        self.conf = currency_conf

    def Process(self, data: CurrencyRow) -> List[OpParam]:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return empty_op

        # 2. add to the data
        self.last_data.append(data)

        # 3. check if data is enough
        cur_num = len(self.last_data)
        min_data_num = max(self.conf.top_search_range, self.conf.bottom_search_range)
        if cur_num < min_data_num:
            return empty_op

        # 4. first check if hit the stop loss or stop profit

        
        # 5. if not hit, then check if the time is reached buy time



        # 4. check if hit the bottom
        bottom = SearchBottom(self.last_data, cur_num, self.conf.bottom_search_range)
        below_idx = SearchBelow(self.last_data, cur_num, self.conf.bottom_duration, bottom)
        is_hit_bottom = False
        if below_idx > -1:
            is_hit_bottom = True

        # 5. check if hit the top
        top = SearchTop(self.last_data, cur_num, self.conf.top_search_range)
        above_idx = SearchAbove(self.last_data, cur_num, self.conf.top_duration, top)
        is_hit_top = False
        if above_idx > -1:
            is_hit_top = True

        # 6. according to the result, decide what we need to do
        #  6.1 if both hit top & bottom, then we need decide which one is earlier
        actions_idxs = []
        if is_hit_top and is_hit_bottom :
            if below_idx < above_idx:
                actions_idxs.append(1)
            else:
                actions_idxs.append(2)
        elif is_hit_top:
            actions_idxs.append(2)
        elif is_hit_bottom:
            actions_idxs.append(1)
        else:
            # 6.2 if everything is ok, then we check the time if it reached the buy time
            # 6.2.1 init the buy time
            if self.buy_time is None:
                self.buy_time = copy.deepcopy(data.time)
                self.buy_time.hour = self.conf.buy_time

            self.buy_time.year = data.time.year
            self.buy_time.month = data.time.month

            # 6.2.2 calculate the timedelta
            time_delta = self.buy_time - data.time
            print("current time: %s, conf time: %s, delta_time: %s (min)" % (data.time, self.buy_time, time_delta.min))

            # 6.2.3 if time is reached, we
            if time_delta.min < 0:




            data.time.clone
            action_idx = 3

        # 7. use tuple as switch case, according to the action_idx to generate OpParam
        actions = {
            0: "_gen_nothing_op_param",
            1: "_gen_sell",
            2: "_gen_buy",
            3: "_gen_buy",
            4: "_gen_closeout",
        }

        method = getattr(self, actions[action_idx])
        if method is None:
            print("[trading]Can't get method %s" % actions[action_idx])
        op_param = method(data)

        # 8. add op_param into history for debug usage
        self.history_list.append(op_param)

        return op_param


    def _gen_nothing_op_param(self, row_data: CurrencyRow) -> OpParam:
        return empty_op

    def _gen_sell(self,  row_data: CurrencyRow) -> OpParam:
        return self._gen_op(E_OP_TYPE.sell, row_data)

    def _gen_buy(self, row_data: CurrencyRow) -> OpParam:
        return self._gen_op(E_OP_TYPE.buy, row_data)

    def _gen_closeout(self, row_data: CurrencyRow) -> OpParam:
        return self._gen_op(E_OP_TYPE.close_out, row_data)

    def _gen_op(self, op_type: E_OP_TYPE, row_data: CurrencyRow) -> OpParam:
        ret_param = OpParam()
        ret_param.op_type = op_type
        ret_param.price = row_data.close
        ret_param.amount = self.conf.trade_amount
        return ret_param


