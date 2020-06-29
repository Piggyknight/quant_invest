# Quant Tactics Regression Test Program

## Outline - Program Usage
- by given currency couple's(exp, euro / usd) .csv data from xm mt5, export data by year into folder "data". 
- then through cmd, user can config the program to  using certain trading tactics to calculating profit in certain period
- the program will export a report under the folder "/report/", the report will looks like below:
	
	>	## Summary for Currency couple : xxx / yyy
	>		- total profit: 
	>		- profit percentage:
	>
	>	### Details Data
	>		index , order data, order type(sell/buy/close out), current profit, current profit percentage

## Framework Requirements
1. Support different trading tactics, but cmd should always be the same and easy to use
2. Each tactics will have certain variable to config (probably in ini format)
3. Support different Currrency couple data, and different time data(in hour, day, minuate format)

## Data flow chart


