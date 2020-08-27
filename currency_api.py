# -*- coding:utf-8 -*-

import sys
from currency_account import *
from currency_exchange_rate import *
from currency_db import *
from currency_op_param import *
from currency_op import *
from currency_ai_trading import *



def main(argv):
    # 1. read excel data into the market



    # 2. init all the class
    # 2.1 init currency conf
    exchange_rate = CurrencyExchangeRate()
    exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur, 1.18)

    # 2.2 init exchange rate % accound
    account = CurrencyAccount(exchange_rate)
    account.AddMoney(E_MONEY_TYPE.usd, 100)

    # 2.3 load db data
    currency_db = CurrencyDb()
    currency_db.Load(file_path)

    # 2.4 init currency conf
    cur_path = os.path.dirname(__file__)
    conf_path = cur_path + '/conf/currency_conf.ini'
    conf = CurrencyConf()
    conf.Load(conf_path)

    # 2.5 init all op
    trading_info = TradingInfo()
    trading_info.trading_fee = 0

    op_sell = OpSell(account, trading_info)
    op_buy = OpBuy(account, trading_info)
    op_closeout_sell = OpCloseOutSell(account, trading_info)
    op_closeout_buy = OpCloseOutBuy(account, trading_info)

    # 2.6 loop get data from the currency_dab\
    ai_trading = AiTrading(conf, account)

    # 3. according to the test duration, loop all the data
    for row in currency_db.db:
        # 3.1. put into ai_trading to get op_commands
        op_data = ai_trading.Process(row)
        if op_data == empty_op:
            continue

        # 3.2 execute op and store result into account
        for op in op_data:
            if E_OP_TYPE.closeout_sell == op.op_type:
                op_closeout_sell.Do(op)
            elif E_OP_TYPE.closeout_buy == op.op_type:
                op_closeout_buy.Do(op)
            elif E_OP_TYPE.buy == op.op_type:
                op_buy.Do(op)
            elif E_OP_TYPE.sell == op.op_type:
                op_sell.Do(op)


    # 4. Finally, according to the account history, export the final report


    return
    


if __name__=="__main__":
    main(sys.argv)