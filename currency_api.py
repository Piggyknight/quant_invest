# -*- coding:utf-8 -*-

import sys
from currency_account import *
from currency_exchange_rate import *
from currency_db import *
from currency_op_param import *
from currency_op import *
from currency_ai_trading import *
from currency_conf_app import *
from currency_conf_strategy import *
from currency_op_history import *
from currency_trading_report import *


def main(argv):
    # 1. read data conf
    cur_path = os.path.dirname(__file__)
    time_conf = cur_path + '/conf/currency_data.ini'
    data_conf = CurrencyConfApp()
    data_conf.Load(cur_path)

    # 2. according to the start & end time read excel data into the db
    year_strs = data_conf.GetYearList()
    currency_db = CurrencyDb()

    print("[main]Start Loading %d conf..." % len(year_strs))
    for year in year_strs:
        excel_file = cur_path + '/data/year.csv'
        currency_db.Load(excel_file)

    # 3 Init the exchange rate & account
    exchange_rate = CurrencyExchangeRate()
    exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur, 1.18)

    account = CurrencyAccount(exchange_rate)
    account.AddMoney(E_MONEY_TYPE.usd, data_conf.start_money)

    # 4 init currency trading strategy conf
    conf_path = cur_path + '/conf/currency_conf.ini'
    conf = CurrencyConf()
    conf.Load(conf_path)

    # 5 init 4 operation
    trading_info = TradingInfo()
    trading_info.trading_fee = 0

    op_sell = OpSell(account, trading_info)
    op_buy = OpBuy(account, trading_info)
    op_closeout_sell = OpCloseOutSell(account, trading_info)
    op_closeout_buy = OpCloseOutBuy(account, trading_info)

    # 6 loop get data from the currency_dab\
    ai_trading = AiTrading(conf, account)
    op_history = CurrencyOpHistory(data_conf.start_money)

    # 7. according to the test duration, loop all the data
    print("[main]Start Analyze Data...")
    for row in currency_db.db:
        # 7.1. put into ai_trading to get op_commands
        op_data = ai_trading.Process(row)
        if op_data == empty_op:
            continue

        # 7.2 execute op and store result into account
        money = 0
        for op in op_data:
            if E_OP_TYPE.closeout_sell == op.op_type:
                money = op_closeout_sell.Do(op)
            elif E_OP_TYPE.closeout_buy == op.op_type:
                money = op_closeout_buy.Do(op)
            elif E_OP_TYPE.buy == op.op_type:
                money = op_buy.Do(op)
                account.PushOrder(op)
            elif E_OP_TYPE.sell == op.op_type:
                money = op_sell.Do(op)
                account.PushOrder(op)

            account.AddMoney(op.src_money, money)
            op_history.AddHistory(row.time, op, money)

    op_history.end_money = account.Total(E_MONEY_TYPE.usd)

    # 4. Finally, according to the account history, export the final report
    report_path = cur_path + "/report.csv"
    print("[main]Start Export account report: %s ..." % report_path)

    report_lines = ExportTradingReport(op_history)
    with open(report_path, "w") as report:
        report.writelines(report_lines)

    return


if __name__ == "__main__":
    main(sys.argv)