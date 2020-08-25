# -*- coding:utf-8 -*-

from currency_account import *
from currency_exchange_rate import *
from currency_db import *
from currency_op_param import *
from currency_op import *
from currency_ai_trading import *

# 1. init currency conf
exchange_rate = CurrencyExchangeRate()
exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur, 1.18)

# 2. init exchange rate % accound
account = CurrencyAccount(exchange_rate)
account.AddMoney(E_MONEY_TYPE.usd, 100)


# 3. init currency row data
# row format  open, high, low, close
currency_string = ["2018.01.02 00:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 01:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 02:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 03:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 04:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 05:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 06:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 07:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 08:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 09:00,1.20276,1.20375,1.20230,1.20354,4774,0",
                   "2018.01.02 10:00,1.20355,1.20470,1.20315,1.20444,5493,0",
                   "2018.01.02 11:00,1.20445,1.20699,1.20414,1.20698,4936,0",
                   "2018.01.02 12:00,1.20697,1.20805,1.20605,1.20677,6063,0",
                   "2018.01.02 13:00,1.20678,1.20700,1.20585,1.20586,3496,0",
                   "2018.01.02 14:00,1.20584,1.20680,1.20560,1.20620,4306,0",
                   "2018.01.02 15:00,1.20620,1.20657,1.20554,1.20566,5047,0",
                   "2018.01.02 16:00,1.20564,1.20580,1.20345,1.20381,6232,0",
                   "2018.01.02 17:00,1.20383,1.20450,1.20254,1.20438,6967,0",
                   "2018.01.02 18:00,1.20437,1.20583,1.20429,1.20483,6034,0",
                   "2018.01.02 19:00,1.20483,1.20528,1.20405,1.20440,3177,0",
                   "2018.01.02 20:00,1.20439,1.20491,1.20411,1.20437,2107,0",
                   "2018.01.02 21:00,1.20437,1.20529,1.20423,1.20525,1581,0",
                   "2018.01.02 22:00,1.20526,1.20598,1.20510,1.20583,1658,0",
                   "2018.01.02 23:00,1.20586,1.20644,1.20537,1.20572,1560,0",
                   "2018.01.03 00:00,1.20572,1.20577,1.20542,1.20566,1215,0",
                   "2018.01.03 01:00,1.20565,1.20654,1.20562,1.20609,1397,0",
                   "2018.01.03 02:00,1.20611,1.20630,1.20485,1.20584,2336,0",
                   "2018.01.03 03:00,1.20584,1.20626,1.20436,1.20522,2397,0",
                   "2018.01.03 04:00,1.20521,1.20521,1.20413,1.20415,2085,0",
                   "2018.01.03 05:00,1.20416,1.20470,1.20410,1.20459,962,0",
                   "2018.01.03 06:00,1.20459,1.20530,1.20457,1.20501,1119,0",
                   "2018.01.03 07:00,1.20504,1.20584,1.20484,1.20575,1431,0",
                   "2018.01.03 08:00,1.20572,1.20597,1.20433,1.20441,2401,0",
                   "2018.01.03 09:00,1.20441,1.20482,1.20338,1.20383,5328,0",
                   "2018.01.03 10:00,1.20382,1.20422,1.20304,1.20418,4532,0",
                   "2018.01.03 11:00,1.20417,1.20427,1.20337,1.20375,3265,0",
                   "2018.01.03 12:00,1.20374,1.20398,1.20141,1.20169,5359,0",
                   "2018.01.03 13:00,1.20169,1.20182,1.20100,1.20142,4671,0",
                   "2018.01.03 14:00,1.20143,1.20228,1.20100,1.20223,3757,0",
                   "2018.01.03 15:00,1.20224,1.20338,1.20190,1.20321,3990,0",
                   "2018.01.03 16:00,1.20320,1.20321,1.20134,1.20159,4714,0",
                   "2018.01.03 17:00,1.20161,1.20239,1.20026,1.20229,7230,0",
                   "2018.01.03 18:00,1.20227,1.20315,1.20190,1.20290,3995,0",
                   "2018.01.03 19:00,1.20290,1.20308,1.20234,1.20265,2028,0",
                   "2018.01.03 20:00,1.20264,1.20286,1.20212,1.20266,1504,0",
                   "2018.01.03 21:00,1.20265,1.20293,1.20005,1.20155,5969,0",
                   "2018.01.03 22:00,1.20155,1.20282,1.20094,1.20116,2846,0",
                   "2018.01.03 23:00,1.20116,1.20152,1.20093,1.20134,1306,0",
                   "2018.01.04 00:00,1.20134,1.20157,1.20095,1.20098,1877,0",
                   "2018.01.04 01:00,1.20098,1.20132,1.20057,1.20100,1605,0"]

currency_db = CurrencyDb()
currency_db.LoadByString(currency_string)

# 4. init currency conf
cur_path = os.path.dirname(__file__)
conf_path = cur_path + '/conf/currency_conf.ini'
conf = CurrencyConf()
conf.Load(conf_path)

# 5. init all op
trading_info = TradingInfo()
trading_info.trading_fee = 0

op_sell = OpSell(account, trading_info)
op_buy = OpBuy(account, trading_info)
op_closeout_sell = OpCloseOutSell(account, trading_info)
op_closeout_buy = OpCloseOutBuy(account, trading_info)


# 4. loop get data from the currency_dab\
ai_trading = AiTrading(conf, account)
for row in currency_db.db:
    # 4.1. put into ai_trading to get op_commands
    op_data = ai_trading.Process(row)
    if op_data == empty_op:
        continue

    # 4.2 generate op abd put into account
    for op in op_data:
        if E_OP_TYPE.closeout_sell == op.op_type:
            op_closeout_sell.Do(op)
        elif E_OP_TYPE.closeout_buy == op.op_type:
            op_closeout_buy.Do(op)
        elif E_OP_TYPE.buy == op.op_type:
            op_buy.Do(op)
        elif E_OP_TYPE.sell == op.op_type:
            op_sell.Do(op)

# 5. assert all the result
# should at least have 2 close out , 2 op(buy or sell)
for op in account.op_history:
    print(op)

