# -*- coding:utf-8 -*-

from currency_db import *
from currency_db_search import *

cur_path = os.path.dirname(__file__)
db_file =  cur_path + '/data/2004.csv'
db = CurrencyDb()
db.Load(db_file)

# Test bottom data by input duration 
bottom = SearchBottom(db.db, 1500, 48)
print("Bottom Value: %.4f" % bottom )

# Test if any data in input duration is below the bottom
idx = SearchBelow(db.db, 1500, 24, bottom)
if -1 != idx:
    print("Find idx %d below bottom , %s" %(idx, db.db[idx]))
else:
    print("Can't find below bottom")

# Test top data by input duration
top = SearchTop(db.db, 1500, 48)
print("Top Value: %.4f" % top)

# Test if any data in the input duration is above the data
idx = SearchAbove(db.db, 1500, 24, top)
if -1 != idx:
    print("Find idx %d above top , %s" %(idx, db.db[idx]))
else:
    print("Can't find above top")


