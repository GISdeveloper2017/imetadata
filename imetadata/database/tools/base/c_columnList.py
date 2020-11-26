# -*- coding: utf-8 -*- 
# @Time : 2020/11/21 12:32 
# @Author : 王西亚 
# @File : c_columnList.py
from imetadata.base.c_list import CList
from imetadata.base.c_utils import CUtils
from imetadata.database.tools.base.c_column import CColumn


class CColumnList(CList):

    def column_by_name(self, column_name) -> CColumn:
        for column in self.list:
            if CUtils.equal_ignore_case(column_name, column.name):
                return column
        else:
            return None

    def column_by_index(self, column_index) -> CColumn:
        return self.item_by_index(column_index)
