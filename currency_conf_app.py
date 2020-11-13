# -*- coding:utf-8 -*-

import os.path
import configparser
from currency_exchange_rate import *
from datetime import datetime

_data_format = '%Y.%m'


class CurrencyConfApp:
    """
        Read currency_data.ini, output start & end time info
    """
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = datetime.now()
        self.money_grp = ""
        self.start_money = 0
        self.src_money = E_MONEY_TYPE.usd
        self.target_money = E_MONEY_TYPE.usd

    def Load(self, file_path: str) -> None:
        # 1. check if file_path is exist
        if not os.path.exists(file_path):
            print("[conf]Data conf: %s not found." % file_path)
            return

        # 2. create ConfigParser & load file_path file
        print("[conf]Start Parsing file: %s" % file_path)
        config = configparser.ConfigParser()
        config.read(file_path)

        # 3. find [Strategy] section
        basic = config['basic']

        # 4. get all the data one by one and set into member
        self.start_time = datetime.strptime(basic['start_time'], _data_format)
        self.end_time = datetime.strptime(basic['end_time'], _data_format)
        self.start_money = int(basic['start_money'])
        self.money_grp = basic['money_grp'].upper()

        if self.money_grp == "EURUSD":
            self.target_money = E_MONEY_TYPE.eur
            self.src_money = E_MONEY_TYPE.usd
        elif self.money_grp == "USDYAN":
            self.target_money = E_MONEY_TYPE.usd
            self.src_money = E_MONEY_TYPE.yan

        return

    def GetYearList(self) -> []:
        ret = [self.start_time.year]
        if self.start_time.year != self.end_time.year:
            year = self.start_time.year
            while year < self.end_time.year:
                year += 1
                ret.append(year)
            ret.append(self.end_time.year)
        return ret


