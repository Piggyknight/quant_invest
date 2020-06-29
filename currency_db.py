# -*- coding:utf-8 -*-

from datetime import datetime
import csv
import os

_print_format = 'year:%d, month:%d, day:%d, time:%d, open:%.4f, high:%.4f, low:%.4f, close:%.4f'
_data_format = '%Y.%m.%d %H:%M'

'''
 contain info load from the split meta trade 5 csv file
 PS: one important assumption: metra trad csv is always sorted by time
'''
class CurrencyDb:
    def __init__(self):
        self._db=[]

    def Load(self, db_file):
        # 1. check if file is exist
        is_file_exist = os.path.exists(db_file)
        if not is_file_exist:
            print("[CureencyDb]: File not exist: %s" % db_file)

        # 2. read csv file into CurrencyRow
        with open(db_file, 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file)

            print("[CureencyDb]Start analyze csv file...")
            begin_size = len(self._db)
            for row in reader:
                if 0 == len(row):
                    continue;

                cr = CurrencyRow()

                # 2.1 convert string to datetime struct
                d_str = row[0]
                cr._time = datetime.strptime(d_str,_data_format);

                # 2.2 convert other string into float 
                cr._open = float(row[1])
                cr._high = float(row[2])
                cr._low = float(row[3])
                cr._close = float(row[4])

                # 2.3 store into db
                self._db.append(cr)

            end_size = len(self._db)
            print("[CureencyDb]Finished loading file %s, %d rows added" % (db_file, end_size - begin_size))

class CurrencyRow:
    def __init__(self):
        self._time = datetime.now()
        self._open = 0.0
        self._high = 0.0
        self._low = 0.0
        self._close = 0.0

    def __str__(self):
        return _print_format % (self._time.year,
                              self._time.month, 
                              self._time.day, 
                              self._time.hour,
                              self._open,
                              self._high,
                              self._low,
                              self._close)

    __repr__ = __str__
   


    

