# -*- coding:utf-8 -*-
from currency_db import *

cur_path = os.path.dirname(__file__)
db_file = cur_path + '/test_data/2004_EURUSD_H1.csv'
db = CurrencyDb()
db.Load(db_file)

