# -*- coding:utf-8 -*-

from currency_db import *
from currency_condition import *

print("[ut]Start test CondStopLoss....")

#1. 3 test, 
#   - test safe check
#   - low is less then threshold
#   - all bigger then threshold
row1 = CurrencyRow()
row1.open = 1.3
row1.high = 1.4
row1.low = 1.22
row1.close = 1.3

row2 = CurrencyRow()
row2.open = 1.1
row2.high = 1.1
row2.low = 1.1
row2.close = 1.1

stop_loss = CondStopLoss(1.2)
assert False == stop_loss.IsTrigger(row1), "Test bigger than threshold failed"
assert True == stop_loss.IsTrigger(row2), "Test less then threshold failed"
assert False == stop_loss.IsTrigger(2), "Test wrong input failed"


print("[ut]Start test CondStopProfit....")

#2. 3 test, 
#   - test safe check
#   - high is bigger then threshold
#   - all bigger then threshold
stop_profit = CondStopProfit(1.16)
assert False == stop_profit.IsTrigger(row2), "Test less than threshold failed"
assert True == stop_profit.IsTrigger(row1), "Test bigger then threshold failed"
assert False == stop_profit.IsTrigger(2), "Test wrong input failed"

print("[ut]Start test CondTradingTime....")

# 3. 4 test,
#   - test safe check
#   - data is equal , earlyer, later than the expire data
start_data = datetime.now()
earlier = start_data - timedelta(hours=5)
equal = start_data
later = equal + timedelta(hours=4)

trading_time = CondTradingTime(start_data.hour)

row1.time = earlier
assert False == trading_time.IsTrigger(row1), "Test earlier failed"

row1.time = equal
assert True == trading_time.IsTrigger(row1), "Test equal failed"

row1.time = later
assert True == trading_time.IsTrigger(row1), "Test later failed"
assert trading_time.trading_time.day == later.day, "Update day failed after Trigger, %s " % trading_time.trading_time

assert False == trading_time.IsTrigger(stop_profit), "Test wrong input failed"

print("[ut]Success")


