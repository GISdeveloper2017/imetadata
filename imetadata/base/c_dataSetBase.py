# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 15:08 
# @Author : 王西亚 
# @File : c_dataSetBase.py
from abc import abstractmethod


class CDataSetBase:
    """
    数据集基类
    设定了数据集的基本操作模式
    """
    _data = None

    @abstractmethod
    def _value_by_index(self, row: int, index: int):
        return None

    @abstractmethod
    def _value_by_name(self, row: int, name: str):
        return None

    @abstractmethod
    def record(self, row: int) -> dict:
        return None

    def value_by_index(self, row: int, index: int, default_value):
        if self._data is None:
            return default_value

        try:
            value = self._value_by_index(row, index)
            if value is None:
                return default_value
            else:
                return value
        except:
            return default_value

    def value_by_name(self, row: int, name: str, default_value):
        """
        根据数据行序号和字段名, 获取记录值
        注意:
        字段名大小写敏感!!!
        :param row:
        :param name:
        :param default_value:
        :return:
        """
        if self._data is None:
            return default_value

        try:
            value = self._value_by_name(row, name)
            if value is None:
                return default_value
            else:
                return value
        except:
            return default_value

    @abstractmethod
    def size(self) -> int:
        """
        记录总数
        :return:
        """
        return 0

    @abstractmethod
    def field_count(self) -> int:
        """
        字段个数
        :return:
        """
        return 0

    @abstractmethod
    def field_name(self, field_index: int) -> str:
        """
        字段名称
        :param field_index:
        :return:
        """
        return ''

    def is_empty(self) -> bool:
        return self.size() == 0
