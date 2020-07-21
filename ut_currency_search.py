# -*- coding:utf-8 -*-

from currency_db import *
from currency_db_search import *


db_file = 'd:\\project\\git\\python_learning_scripts\\quant\\data\\2004.csv'
db = CureencyDb()
db.Load(db_file)

# Test bottom data by input duration 
bottom = SearchBottom(db._db, 1500, 48)
print("Bottom Value: %.4f" % bottom )

# Test if any data in input duration is below the bottom
idx = SearchBelow(db._db, 1500, 24, bottom)
if -1 != idx:
    print("Find idx %d below bottom , %s" %(idx, db._db[idx]))
else:
    print("Can't find below bottom")

# Test top data by input duration
top = SearchTop(db._db, 1500, 48)
print("Top Value: %.4f" % top)

# Test if any data in the input duration is above the data
idx = SearchAbove(db._db, 1500, 24, top)
if -1 != idx:
    print("Find idx %d above top , %s" %(idx, db._db[idx]))
else:
    print("Can't find above top")


