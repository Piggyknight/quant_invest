# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime
import csv
import os

_print_format = 'year:%d, month:%d, day:%d, time:%d, open:%.4f, high:%.4f, low:%.4f, close:%.4f'
_data_format = '%Y.%m.%d %H:%M'


class CurrencyRow:
    def __init__(self):
        self.time = datetime.now()
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0

    def __str__(self):
        return _print_format % (self.time.year,
                                self.time.month,
                                self.time.day,
                                self.time.hour,
                                self.open,
                                self.high,
                                self.low,
                                self.close)

    __repr__ = __str__


class CurrencyDb:
    """
     contain info load from the split meta trade 5 csv file
     PS: one important assumption: meta trade's csv is always sorted by time
    """

    def __init__(self):
        self.db = List[CurrencyRow]

    def Load(self, db_file: str) -> int:
        # 1. check if file is exist
        is_file_exist = os.path.exists(db_file)
        if not is_file_exist:
            print("[market]: File not exist: %s" % db_file)
            return -1

        # 2. read csv file into CurrencyRow
        with open(db_file, 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)

            print("[market]Start analyze csv file...")
            begin_size = len(self.db)
            for row in reader:
                if 0 == len(row):
                    continue

                cr = CurrencyRow()

                # 2.1 convert string to datetime struct
                d_str = row[0]
                cr.time = datetime.strptime(d_str, _data_format)

                # 2.2 convert other string into float 
                cr.open = float(row[1])
                cr.high = float(row[2])
                cr.low = float(row[3])
                cr.close = float(row[4])

                # 2.3 store into db
                self.db.append(cr)

            end_size = len(self.db)
            print("[market]Finished loading file %s, %d rows added" % (db_file, end_size - begin_size))

        return 0

    def Get(self, idx: int) -> CurrencyRow:
        if idx > len(self.db) or idx < 0:
            print("[market]idx(%d) out of range when getting data from CurrencyDb", idx)
        return self.db[idx]

