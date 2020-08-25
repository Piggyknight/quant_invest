# -*- coding:utf-8 -*-
from typing import List
from currency_db_search import *
from currency_conf import *
from currency_op_param import *
from currency_account import *
from currency_condition import *


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
    def __init__(self, currency_conf: CurrencyConf, account: CurrencyAccount) -> None:
        # 1. init basic info
        self.last_data = List[CurrencyRow]
        self.data_num = 0
        self.has_bought = False
        self.history_list = []
        self.buy_time = None
        self.conf = currency_conf
        self.account = account

        # 2. init condition trigger
        self.cond_stop_loss = CondStopLoss(currency_conf.stop_loss)
        self.cond_stop_profit = CondStopProfit(currency_conf.stop_profit)
        self.cond_trading_time = CondTradingTime(currency_conf.buy_time)

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

        # 4. check if has orders
        decision = []
        is_trading_time = self.cond_trading_time.IsTrigger(data)
        if self.account.HasOrders:
            last_op = self.account.PeekOrder()
            is_last_sell_order = E_OP_TYPE.sell == last_op.op_type
            is_last_buy_order = E_OP_TYPE.buy == last_op.op_type
            is_hit_stop_loss = self.cond_stop_loss.IsTrigger(data)
            is_hit_stop_profit = self.cond_stop_profit.IsTrigger(data)
            print("is_last_sell_order: %d, is_last_buy_order: %d" \
                  % (is_last_sell_order, is_last_buy_order))
            print(" is_hit_loss: %d, is_hit_profit, %d, is_trading_time: %d"\
                  % (is_hit_stop_loss, is_hit_stop_profit, is_trading_time))

            # 4.1 make decision by all the param
            if is_last_sell_order and is_hit_stop_loss:
                decision.append(E_OP_TYPE.closeout_sell)
            elif is_last_buy_order and self.cond_stop_profit.IsTrigger(data):
                decision.append(E_OP_TYPE.closeout_buy)
            elif is_last_buy_order and is_trading_time:
                decision.append(E_OP_TYPE.closeout_buy)
            elif is_last_sell_order and is_trading_time:
                decision.append(E_OP_TYPE.closeout_sell)

        # 5 if trading time is reached, we need to decide buy or sell
        if is_trading_time:
            # 5.1. check if hit the bottom
            bottom = SearchBottom(self.last_data, cur_num, self.conf.bottom_search_range)
            below_idx = SearchBelow(self.last_data, cur_num, self.conf.bottom_duration, bottom)
            is_hit_bottom = False
            if below_idx > -1:
                is_hit_bottom = True

            # 5.2 check if hit the top
            top = SearchTop(self.last_data, cur_num, self.conf.top_search_range)
            above_idx = SearchAbove(self.last_data, cur_num, self.conf.top_duration, top)
            is_hit_top = False
            if above_idx > -1:
                is_hit_top = True

            # 5.3 according to the result, decide what we need to do
            # 5.3.1 if both hit top & bottom, then we need decide which one is earlier
            if is_hit_top and is_hit_bottom :
                if below_idx < above_idx:
                    decision.append(E_OP_TYPE.sell)
                else:
                    decision.append(E_OP_TYPE.buy)
            elif is_hit_top:
                decision.append(E_OP_TYPE.buy)
            elif is_hit_bottom:
                decision.append(E_OP_TYPE.sell)

        # 6. according to the decision to create op_param
        op_param = []
        for op_type in decision:
            single_op = self._gen_op(op_type, data)
            # avoid empty op
            if single_op is empty_op:
                continue
            op_param.append(single_op)

        return op_param

    def _gen_op(self, op_type: E_OP_TYPE, row_data: CurrencyRow) -> OpParam:
        ret_param = OpParam()
        ret_param.op_type = op_type
        ret_param.price = row_data.close
        ret_param.amount = self.conf.trade_amount
        return ret_param
