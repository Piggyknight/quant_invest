# -*- coding:utf-8 -*-

class Trigger:
    def __init__(self):
        self._condition = None
        self._reactor = None

    def Process(self, data):
        #1. safe check
        if self._condition is None:
            print("Error: Trigger condition is none")
            return
        
        if self._reactor is None:
            print("Error: Trigger reactor is none")
            return

        # 2. trigger the condition and reactor
        if self._condition.IsOk(data):
            self._reactor(data)