# -*- coding:utf-8 -*-

from currency_db import *
from currency_condition import *

print(">>Start test CondStopLoss....")

#1. 3 test, 
#   - test safe check
#   - low is less then threshold
#   - all bigger then threshold
row1 = CurrencyRow()
row1._open = 1.3
row1._high = 1.4
row1._low = 1.22
row1._close = 1.3

row2 = CurrencyRow()
row2._open = 1.1
row2._high = 1.1
row2._low = 1.1
row2._close = 1.1

stop_loss = CondStopLoss()
stop_loss._threshold = 1.2
assert False == stop_loss.IsOk(row1), "Test bigger than threshold failed"
assert True == stop_loss.IsOk(row2), "Test less then threshold failed"
assert False == stop_loss.IsOk(2), "Test wrong input failed"


print(">>Start test CondStopProfit....")

#2. 3 test, 
#   - test safe check
#   - high is bigger then threshold
#   - all bigger then threshold
stop_profit = CondStopProfit()
stop_profit._threshold = 1.16
assert False == stop_profit.IsOk(row2), "Test less than threshold failed"
assert True == stop_profit.IsOk(row1), "Test bigger then threshold failed"
assert False == stop_profit.IsOk(2), "Test wrong input failed"

print(">>Start test CondCloseOut....")

#3. 4 test, 
#   - test safe check
#   - data is equal , earlyer, later than the expire data
start_data = datetime.now()
earlier = start_data + timedelta(seconds=2)
equal = start_data + timedelta(days=1)
later = equal + timedelta(seconds=20000)


close_out = CondCloseOut()
close_out._expire_data = equal

row1._time = earlier
assert False == close_out.IsOk(row1), "Test earlier failed"

row1._time = equal
assert True == close_out.IsOk(row1), "Test equal failed"

row1._time = later
assert True == close_out.IsOk(row1), "Test later failed"

assert False== close_out.IsOk(stop_profit), "Test wrong input failed"


