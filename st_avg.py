# -*- coding:utf-8 -*-
from typing import List
from currency_db_search import *
from currency_op_param import *
from currency_account import *
from currency_condition import *
from st_avg_conf import *
from st_avg_calc import *

file_path = '/conf/st_avg_conf.ini'

class StAvg:
    """
    基本策略是:
        - 80单位平均线 slow1 线
        - 40单位平均线 slow2 线
        - 当前价位 fast 线
        - 持有时间 : 12
    """
    def __init__(self
                 , account: CurrencyAccount
                 , src_money: E_MONEY_TYPE
                 , target_money: E_MONEY_TYPE
                 , point_factor: float) -> None:

        # 1. init basic info
        self.last_data = []
        self.data_num = 0
        self.history_list = []
        self.account = account
        self.src_money = src_money
        self.target_money = target_money
        self.point_factor = point_factor
        self.delay_op = False
        self.op_type = E_OP_TYPE.none
        self.is_last_above_slow1 = False
        self.is_last_above_slow2 = False
        self.is_last_below_slow1 = False
        self.is_last_below_slow2 = False

        # 2. load conf
        cur_path = os.path.dirname(__file__)
        abs_path = cur_path + file_path
        self.conf = StAvgConf()
        self.conf.Load(abs_path)

        # 3. init condition trigger
        self.cond_duration = CondDuration(self.conf.hold_time)

    def Process(self, data: CurrencyRow) -> List[OpParam]:
        # 1. safe check
        if not isinstance(data, CurrencyRow):
            return empty_op

        # 2. add to the data
        self.last_data.append(data)
        print("[ai]collect App data: count=%d, row=%s" % (len(self.last_data), data))

        # 3. check if data is enough
        cur_num = len(self.last_data)
        min_data_num = max(self.conf.slow2_duration, self.conf.slow1_duration)
        if cur_num < min_data_num:
            return empty_op

        # 4. calc avg
        slow1 = CalcAvg(self.last_data, cur_num, self.conf.slow1_duration)
        slow2 = CalcAvg(self.last_data, cur_num, self.conf.slow2_duration)
        fast = data.close

        is_above_slow1 = fast > slow1
        is_above_slow2 = fast > slow2
        is_below_slow1 = fast < slow1
        is_below_slow2 = fast < slow2
        print("slow1: %.5f, slow2: %.5f, fast: %.5f" % (slow1, slow2, fast))

        # 4 if decide close out last frame, then we close out
        out_param = []
        if self.delay_op:
            print("\tOp: %s, price: %s" %(self.op_type, data.open))
            out_param.append(self._gen_op(self.op_type, data.open, data))

            if E_OP_TYPE.buy == self.op_type or E_OP_TYPE.sell == self.op_type:
                self.cond_duration.trading_time = data.time

            self.delay_op = False
            self.op_type = E_OP_TYPE.none
        else:
            # 5. check if has orders
            if self.account.HasOrders():
                # 5.1 prepare all the data
                print("\t[ai]Account already has orders...")
                last_op = self.account.PeekOrder()
                is_last_sell_order = E_OP_TYPE.sell == last_op.op_type
                is_last_buy_order = E_OP_TYPE.buy == last_op.op_type
                is_time_reached = self.cond_duration.IsTrigger(data)

                print("\tis_last_sell: %s, is_last_buy: %s, is_time_reached: %s " % (is_last_sell_order, is_last_buy_order,is_time_reached))
                deci_op = E_OP_TYPE.none

                # 5.2 if last time is buy order
                if is_last_buy_order:
                    # if hold time is reached and fast is below slow1 or slow2, then close out
                    is_below_stop1 = fast < (slow1 - self.conf.stop_loss * self.point_factor)
                    is_below_stop2 = fast < (slow2 - self.conf.stop_loss * self.point_factor)
                    if is_time_reached and (is_below_stop1 or is_below_stop2):
                        deci_op = E_OP_TYPE.closeout_buy
                    elif is_below_stop1:
                        # if time is not reached and fast is below slow1, then close out in next time
                        self.delay_op = True
                        self.op_type = E_OP_TYPE.closeout_buy

                # 5.3 if last time is sell order
                if is_last_sell_order:
                    is_above_stop1 = fast > (slow1 + self.conf.stop_loss * self.point_factor)
                    is_above_stop2 = fast > (slow2 + self.conf.stop_loss * self.point_factor)
                    # if hold time is reached and fast is above slow1 or slow2, then close out
                    if is_time_reached and (is_above_stop1 or is_above_stop2):
                        deci_op = E_OP_TYPE.closeout_sell
                    elif is_above_stop1:
                        # if time is not reached and fast is first above slow 1, then close out in next time
                        self.delay_op = True
                        self.op_type = E_OP_TYPE.closeout_sell

                # 5.4 according to the decision create out_param
                if E_OP_TYPE.none != deci_op:
                    print("\t[ai]Decision made: %s, price=%.5f" % (deci_op, data.close))
                    out_param.append(self._gen_op(deci_op, data.close, data))

            # 6. if has not orders
            if not self.account.HasOrders():
                # 6.1 calc trigger first
                is_just_above_slow1 = self.is_last_below_slow1 and is_above_slow1
                is_just_below_slow1 = self.is_last_above_slow1 and is_below_slow1
                print("\t[ai]Account has no orders, is_just_above_slow1: %s, is_just_below_slow1: %s " % (is_just_above_slow1, is_just_below_slow1))
                if is_just_above_slow1:
                    # 6.2 if fast is just above slow1, then buy next time
                    self.delay_op = True
                    self.op_type = E_OP_TYPE.buy
                elif is_just_below_slow1:
                    # 6.3 if fas is just below slow1, then sell next time
                    self.delay_op = True
                    self.op_type = E_OP_TYPE.sell

        # 7 update avg status
        self.is_last_above_slow1 = is_above_slow1
        self.is_last_above_slow2 = is_above_slow2
        self.is_last_below_slow1 = is_below_slow1
        self.is_last_below_slow2 = is_below_slow2

        # 8. according to the decision to create op_param
        if 0 == len(out_param):
            print("[ai]No decision...")

        return out_param

    def _gen_op(self
                , op_type: E_OP_TYPE
                , price: float
                , row_data: CurrencyRow) -> OpParam:
        ret_param = OpParam()
        ret_param.op_type = op_type
        ret_param.price = price
        ret_param.amount = self.account.GetMoney(self.src_money) / price
        ret_param.src_money = self.src_money
        ret_param.target_money = self.target_money
        return ret_param
