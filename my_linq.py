# -*- coding:utf-8 -*-

from collections.abc import Iterable

class linq(object):
    def __init__(self, iterable):
        if not isinstance(iterable, Iterable):
            raise TypeError('[error]wrong iterable parameter')
        self.__end = False
        self.__iterable = iterable

    def __get_iterable(self):
        if self.__end:
            raise StopIteration('[error]iterator cant be used twice')

        self.__end = True
        return self.__iterable

    def all(self, predicate):
        return all(map(predicate, self.__get_iterable()))

    def any(self, predicate=None):
        return any(map(predicate, self.__get_iterable()))

    def where(self, predicate):
        return linq(filter(predicate, self.__get_iterable()))

    def max(self):
        return max(self.__get_iterable())

    def min(self):
        return min(self.__get_iterable())

    def average(self):
        count = 0
        total = 0.0
        for number in self.__get_iterable():
            total += number
            count += 1
        return total / count

    def union(self, iterable):
        return linq(self.__union(iterable))

    def __union(self, iterable):
        for x in self.__get_iterable():
            yield x
        for x in iterable:
            yield x

    def count(self):
        count = 0
        for number in self.__get_iterable():
            count += 1
        return count

    def first(self, defaultValue=None):
        return next(self.__get_iterable(), defaultValue)

    def last(self, defaultValue=None):
        it = self.__get_iterable()
        x = None
        b = False
        while True:
            try:
                x = next(it)
                b = True
            except StopIteration:
                if b:
                    return x
                return defaultValue

    def sum(self):
        return sum(self.__get_iterable())

    def tolist(self):
        return list(self.__get_iterable())

    def select(self, selector):
        return linq(map(selector, self.__get_iterable()))