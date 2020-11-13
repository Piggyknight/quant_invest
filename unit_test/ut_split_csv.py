# -*- coding:utf-8 -*-        
import os
from split_csv import *

# test code

cur_path = os.path.dirname(__file__)
#file_path = cur_path +"/test_data/EURUSDH1.csv"
file_path = cur_path +"/test_data/USDJPYH1.csv"
op_folder = cur_path + "/test_export/"

split_mt5_csv(file_path, op_folder)
