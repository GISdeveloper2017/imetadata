# -*- coding: utf-8 -*- 
# @Time : 2020/11/23 21:11 
# @Author : 王西亚 
# @File : c_dbColumnTypes.py
from imetadata.base.c_file import CFile
from imetadata.base.c_list import CList
from imetadata.database.base.dml.c_dbColumnType import CDBColumnType


class CDBColumnTypes(CList):
    def column_type_by_name(self, column_type: str) -> CDBColumnType:
        for db_column_type in self.list:
            if CFile.file_match(column_type, db_column_type.db_column_type_filter):
                return db_column_type
        else:
            return None
