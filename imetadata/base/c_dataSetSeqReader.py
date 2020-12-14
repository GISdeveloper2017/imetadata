# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 15:08 
# @Author : 王西亚 
# @File : c_dataSetBase.py
from abc import abstractmethod


class CDataSetSeqReader:
    """
    顺序读取的数据集基类
    设定了数据集的基本操作模式
    """

    def __init__(self):
        super().__init__()
        self._data = None
        self._record = None

    @abstractmethod
    def _value_by_index(self, index: int):
        return None

    @abstractmethod
    def _value_by_name(self, name: str):
        return None

    @property
    def data_obj(self):
        return self._data

    @property
    def record(self):
        return self._record

    @abstractmethod
    def first(self) -> bool:
        return False

    @abstractmethod
    def next(self) -> bool:
        return False

    def value_by_index(self, index: int, default_value):
        if self._data is None:
            return default_value

        try:
            value = self._value_by_index(index)
            if value is None:
                return default_value
            else:
                return value
        except:
            return default_value

    def value_by_name(self, name: str, default_value):
        """
        根据数据行序号和字段名, 获取记录值
        注意:
        字段名大小写敏感!!!
        :param name:
        :param default_value:
        :return:
        """
        if self._data is None:
            return default_value

        try:
            value = self._value_by_name(name)
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

    def is_empty(self) -> bool:
        return self.size() == 0
