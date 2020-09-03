#!/usr/bin/python3
# -*- coding:utf-8 -*-


from sqlalchemy.engine.result import ResultProxy


class CDataSet:
    __data__ = None

    def __init__(self, data=None):
        self.__data__ = data

    def value_by_index(self, row: int, index: int, default_value):
        if self.__data__ is None:
            return default_value

        try:
            value = self.__data__[row][index]
            if value is None:
                return default_value
            else:
                return value
        except:
            return default_value

    def value_by_name(self, row: int, name: str, default_value):
        if self.__data__ is None:
            return default_value

        try:
            value = self.__data__[row][name.lower()]
            if value is None:
                return default_value
            else:
                return value
        except:
            return default_value

    def size(self) -> int:
        if self.__data__ is None:
            return 0

        return len(self.__data__)

    def is_empty(self) -> bool:
        return self.size() == 0
