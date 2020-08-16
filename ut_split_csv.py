# -*- coding:utf-8 -*-        
import os
from split_csv import *

# test code

cur_path = os.path.dirname(__file__)
file_path = cur_path +"/mt5_data/EURUSDH1.csv"
op_folder = cur_path + "/data/"

split_mt5_csv(file_path, op_folder)
