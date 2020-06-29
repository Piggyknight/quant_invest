# -*- coding:utf-8 -*-

import sys

'''
    main func
     - argv[0]: start time, format is 2019.01.01
     - argv[1]: end time, format is 2019.12.31
     - argv[2]: when to buy in 24 hour format, exp: 12, 18, 23
     - argv[3]: how long should we check if we hit the bottom, unit is hour
     - argv[4]: how long should we trace back to calculate the bottom, unit is hour
     - argv[5]: how long should we check if we above the top, unit is hour
     - argv[6]: how long should we trace back to calculate the top, unit is hour
     - argv[7]: the point to stop loss
     - argv[8]: the point to stop profit
     - argv[9]: how long should we wait to close out the former order, unit is hour
     - argv[9]: average point diff for each order
'''
def main(argv):

    print(argv[1])
    print(argv[2])
    print(argv[3])


if __name__=="__main__":
    main(sys.argv)