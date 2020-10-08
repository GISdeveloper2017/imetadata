#!/usr/bin/python3
# -*- coding:utf-8 -*-
from imetadata.base.c_file import CFile
from imetadata.base.exceptions import PathNotCreateException


class CDataSet:
    __data__ = None

    def __init__(self, data=None):
        self.__data__ = data

    def __value_by_index__(self, row: int, index: int):
        return self.__data__[row][index]

    def __value_by_name__(self, row: int, name: str):
        return self.__data__[row][name]

    def value_by_index(self, row: int, index: int, default_value):
        if self.__data__ is None:
            return default_value

        try:
            value = self.__value_by_index__(row, index)
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
            value = self.__value_by_name__(row, name.lower())
            if value is None:
                return default_value
            else:
                return value
        except:
            return default_value

    def size(self) -> int:
        """
        记录总数
        :return:
        """
        if self.__data__ is None:
            return 0

        return len(self.__data__)

    def field_count(self) -> int:
        """
        字段个数
        :return:
        """
        if self.__data__ is None:
            return 0

        row_data = self.__data__[0]
        return len(row_data)

    def is_empty(self) -> bool:
        return self.size() == 0

    def blob2file(self, row: int, name: str, file_name: str):
        if self.__data__ is None:
            return

        value = self.__value_by_name__(row, name.lower())
        if value is None:
            return

        if not CFile.check_and_create_directory(file_name):
            raise PathNotCreateException(CFile.file_path(file_name))

        f = open(file_name, 'wb')
        try:
            f.write(value)
        finally:
            f.close()

    @classmethod
    def file2param(cls, params: dict, param_name: str, file_name: str):
        if params is None:
            return

        if not CFile.file_or_path_exist(file_name):
            params[param_name] = None
            return

        # 注意这里一定要使用rb，读出二进制文件，否则有读不全等问题
        fp = open(file_name, 'rb')
        try:
            params[param_name] = fp.read()
        finally:
            fp.close()
