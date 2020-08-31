# -*- coding:utf-8 -*-
from typing import List
from currency_db_search import *
from currency_conf_strategy import *
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
        self.last_data = []
        self.data_num = 0
        self.has_bought = False
        self.history_list = []
        self.buy_time = None
        self.conf = currency_conf
        self.account = account

        # 2. init condition trigger
        self.cond_stop_loss = CondStopLoss(currency_conf.stop_loss)
        self.cond_stop_profit = CondStopProfit(currency_conf.stop_profit)
        self.cond_trading_time = CondTradingTime(currency_conf.buy_time, currency_conf.wait_duration)

    def Process(self, data: CurrencyRow) -> List[OpParam]:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return empty_op

        # 2. add to the data
        self.last_data.append(data)
        print("[ai]collect App data: count=%d, row=%s" % (len(self.last_data), data))

        # 3. check if data is enough
        cur_num = len(self.last_data)
        min_data_num = max(self.conf.top_search_range, self.conf.bottom_search_range)
        if cur_num < min_data_num:
            return empty_op

        # 4. check if has orders
        # print("[ai]Data number is enough, start trading...")
        out_param = []
        is_trading_time = self.cond_trading_time.IsTrigger(data)
        if self.account.HasOrders():
            print("\t[ai]Account already has orders...")
            last_op = self.account.PeekOrder()
            is_last_sell_order = E_OP_TYPE.sell == last_op.op_type
            is_last_buy_order = E_OP_TYPE.buy == last_op.op_type
            is_hit_stop_loss = self.cond_stop_loss.IsTrigger(data)
            is_hit_stop_profit = self.cond_stop_profit.IsTrigger(data)
            print("\t[ai]is_last_sell_order: %d, is_last_buy_order: %d" \
                  % (is_last_sell_order, is_last_buy_order))
            print("\t[ai]is_hit_bottom: %d, is_hit_top, %d, is_trading_time: %d"\
                  % (is_hit_stop_loss, is_hit_stop_profit, is_trading_time))

            # 4.1 make decision by all the param
            deci_op = E_OP_TYPE.none
            if is_hit_stop_profit or is_hit_stop_loss:
                if is_last_buy_order:
                    deci_op = E_OP_TYPE.closeout_buy
                else:
                    deci_op = E_OP_TYPE.closeout_sell
            elif is_trading_time:
                if is_last_buy_order:
                    deci_op = E_OP_TYPE.closeout_buy
                else:
                    deci_op = E_OP_TYPE.closeout_sell

            # 4.2 decide price
            if is_hit_stop_profit:
                price = self.cond_stop_profit.threshold
            elif is_hit_stop_loss:
                price = self.cond_stop_loss.threshold
            else:
                price = data.close

            if E_OP_TYPE.none != deci_op:
                print("\t[ai]Decision made: %s, price=%.5f" % (deci_op, price))
                out_param.append(self._gen_op(deci_op, price, data))

        # 5 if trading time is reached, we need to decide buy or sell
        # print("[ai]Continue if reach trading Time...")
        if is_trading_time:
            print("\t[ai]Trading Time, decide whether we need to buy or sell....")
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
            deci_op = E_OP_TYPE.none
            if is_hit_top and is_hit_bottom:
                if below_idx < above_idx:
                    deci_op = E_OP_TYPE.sell
                else:
                    deci_op = E_OP_TYPE.buy
            elif is_hit_bottom:
                deci_op = E_OP_TYPE.sell
            else:
                deci_op = E_OP_TYPE.buy

            if E_OP_TYPE.none != deci_op:
                print("\t[ai]Is Hit top: %d, Is Hit Bottom: %d, decision: %s, price: %.5f" % (is_hit_top, is_hit_bottom, deci_op, data.close))
                # 5.3.2 after we made decision, we need to update the stop loss and profit threshold
                self.cond_stop_profit.threshold = data.close + self.conf.stop_profit * 0.00001
                self.cond_stop_loss.threshold = data.close - self.conf.stop_loss * 0.00001
                out_param.append(self._gen_op(deci_op, data.close, data))

        # 6. according to the decision to create op_param
        if 0 == len(out_param):
            print("[ai]No decision...")

        return out_param

    def _gen_op(self, op_type: E_OP_TYPE, price: float, row_data: CurrencyRow) -> OpParam:
        ret_param = OpParam()
        ret_param.op_type = op_type
        ret_param.price = price
        ret_param.amount = self.conf.trade_amount
        return ret_param
