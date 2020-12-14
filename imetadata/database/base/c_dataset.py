#!/usr/bin/python3
# -*- coding:utf-8 -*-
from imetadata.base.c_dataSetBase import CDataSetBase
from imetadata.base.c_file import CFile
from imetadata.base.exceptions import PathNotCreateException


class CDataSet(CDataSetBase):
    def __init__(self, data=None):
        super().__init__()
        self._data = data

    def _value_by_index(self, row: int, index: int):
        return self._data[row][index]

    def _value_by_name(self, row: int, name: str):
        return self._data[row][name]

    def record(self, row: int) -> dict:
        return self._data[row]

    def size(self) -> int:
        """
        记录总数
        :return:
        """
        if self._data is None:
            return 0

        return len(self._data)

    def field_count(self) -> int:
        """
        字段个数
        :return:
        """
        if self._data is None:
            return 0

        row_data = self._data[0]
        return len(row_data)

    def blob2file(self, row: int, name: str, file_name: str):
        if self._data is None:
            return

        value = self._value_by_name(row, name)
        if value is None:
            return

        if not CFile.check_and_create_directory(file_name):
            raise PathNotCreateException(CFile.file_path(file_name))

        f = open(file_name, 'wb')
        try:
            f.write(value)
        finally:
            f.close()
