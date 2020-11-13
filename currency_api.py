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
    data_conf.Load(time_conf)

    # 2. according to the start & end time read excel data into the db
    year_list = data_conf.GetYearList()
    currency_db = CurrencyDb()

    print("[main]Start Loading %d conf..." % len(year_list))
    for year in year_list:
        excel_file = cur_path + '/data/%s_%s_H1.csv' % (year, data_conf.money_grp)
        currency_db.Load(excel_file)

    # 3 Init the exchange rate & account
    exchange_rate = CurrencyExchangeRate()
    exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.eur, 1.18)
    exchange_rate.Add(E_MONEY_TYPE.usd, E_MONEY_TYPE.yan, 106.18)

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
    ai_trading = AiTrading(conf, account, data_conf.src_money, data_conf.target_money)
    op_history = CurrencyOpHistory(data_conf.start_money)

    # 7. according to the test duration, loop all the data
    print("[main]Start Analyze Data...")
    for row in currency_db.db:
        # 7.1 check if row data is in the duration of the data_conf
        is_after_start_time = row.time.year >= data_conf.start_time.year \
                              and row.time.month >= data_conf.start_time.month
        is_before_end_time = row.time.year < data_conf.end_time.year \
                             or (row.time.year == data_conf.end_time.year and row.time.month <= data_conf.end_time.month)
        is_in_duration = is_after_start_time and is_before_end_time
        if not is_in_duration:
            continue

        # 7.2. put into ai_trading to get op_commands
        op_data = ai_trading.Process(row)
        if op_data == empty_op:
            continue

        # 7.3 execute op and store result into account
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
    start_time_str = "%d%d" % (data_conf.start_time.year, data_conf.start_time.month)
    end_time_str = "%d%d" % (data_conf.end_time.year, data_conf.end_time.month)
    report_path = cur_path + "/report/report_%s_%s.csv" % (start_time_str, end_time_str)
    print("[main]Start Export account report: %s ..." % report_path)

    report_lines = ExportTradingReport(op_history)
    with open(report_path, "w") as report:
        report.writelines(report_lines)

    return


if __name__ == "__main__":
    main(sys.argv)
