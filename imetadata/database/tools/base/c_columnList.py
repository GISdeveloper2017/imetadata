# -*- coding: utf-8 -*- 
# @Time : 2020/11/21 12:32 
# @Author : 王西亚 
# @File : c_columnList.py
from imetadata.base.c_utils import CUtils
from imetadata.database.tools.base.c_column import CColumn


class CColumnList:
    @property
    def columns(self):
        return self.__inner_list

    def __init__(self):
        self.__inner_list = list()

    def add(self, column: CColumn) -> bool:
        if column is not None:
            self.columns.append(column)
            return True
        else:
            return False

    def column_by_name(self, column_name) -> CColumn:
        for column in self.columns:
            if CUtils.equal_ignore_case(column_name, column.name):
                return column
        else:
            return None

    def delete(self, column_index: int):
        if 0 <= column_index <= len(self.__inner_list):
            del self.__inner_list[column_index]
