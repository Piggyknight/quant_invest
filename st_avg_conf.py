# -*- coding:utf-8 -*-
from enum import Enum
import os.path
import configparser


class StAvgConf:
    """
        -hold time: 持有固定时间
        -slow1_duration: 80个时间单位
        -slow2_duration: 40个时间单位
        -stop_lost: 止损区间, 点单位

         file format in ini:

            [Strategy]
                hold_time = 12
                slow1_duration = 80
                slow2_duration = 40
                stop_loss = 100
    """
    def __init__(self):
        self.hold_time = 0
        self.slow1_duration = 0
        self.slow2_duration = 0
        self.stop_loss = 0
        self.lever = 0

    def Load(self, file_path: str) -> None:
        # 1. check if file_path is exist
        if not os.path.exists(file_path):
            print("[conf]Configuration file %s not found." % file_path)
            return

        # 2. create ConfigParser & load file_path file
        print("[conf]Start Parsing file: %s" % file_path)
        config = configparser.ConfigParser()
        config.read(file_path)

        # 3. find [Strategy] section
        strategy = config['Strategy']

        # 4. get all the data one by one and set into member
        self.hold_time = int(strategy['hold_time'])
        self.slow1_duration = int(strategy['slow1_duration'])
        self.slow2_duration = int(strategy['slow2_duration'])
        self.stop_loss = float(strategy['stop_loss'])
        return
