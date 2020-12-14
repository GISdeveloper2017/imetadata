# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 18:44 
# @Author : 王西亚 
# @File : c_dbDataSetSeqReader.py

from imetadata.base.c_dataSetSeqReader import CDataSetSeqReader
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.database.base.c_dataset import CDataSet


class CVectorDataSetSeqReader(CDataSetSeqReader):
    def __init__(self, dataset: CDataSet):
        super().__init__()
        self._data = dataset
        self.__record_index = -1

    def record_as_dict(self) -> dict:
        return self._data.record(self.__record_index)

    def first(self) -> bool:
        if self._data.is_empty():
            return False
        self.__record_index = -1
        return self.next()

    def next(self) -> bool:
        self._record = None
        if self.__record_index < self.size() - 1:
            self.__record_index = self.__record_index + 1
            return True
        else:
            return False

    def _value_by_name(self, name: str):
        return self._data.value_by_name(self.__record_index, name, None)

    def size(self) -> int:
        return self._data.size()

    def _value_by_index(self, index: int):
        return self._data.value_by_index(self.__record_index, index, None)

    def field_count(self) -> int:
        return self._data.field_count()
