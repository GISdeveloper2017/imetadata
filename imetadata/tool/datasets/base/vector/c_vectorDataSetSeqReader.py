# -*- coding: utf-8 -*- 
# @Time : 2020/12/14 16:24 
# @Author : 王西亚 
# @File : c_vector_dataset.py
from imetadata.base.c_dataSetSeqReader import CDataSetSeqReader
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils


class CVectorDataSetSeqReader(CDataSetSeqReader):
    def __init__(self, vector_layer_obj, mdb_flag):
        super().__init__()
        self._data = vector_layer_obj
        self._name = CUtils.any_2_str(vector_layer_obj.GetName())
        self._mdb_flag = mdb_flag  # 用于解决mdb中文问题

    @property
    def dataset_name(self):
        return self.mdb_chinese_conversion(self._name)

    def record_as_dict(self) -> dict:
        result = dict()
        result[CResource.Name_ID] = self.f_id()
        result[CResource.Name_Geometry] = self.geometry()
        for field_index in range(self.field_count()):
            result[self.field_name(field_index).lower()] = self.value_by_index(field_index, None)
        return result

    def first(self) -> bool:
        # 对图层进行初始化，如果对图层进行了过滤操作，执行这句后，之前的过滤全部清空
        self._data.ResetReading()
        return self.next()

    def next(self) -> bool:
        self._record = None
        feature = self._data.GetNextFeature()
        if feature is not None:
            self._record = feature
            return True
        else:
            return False

    def f_id(self):
        if self._record is None:
            return None

        return self._record.GetFID()

    def geometry(self):
        if self._record is None:
            return None

        return self._record.GetGeometryRef()

    def _value_by_name(self, name: str):
        for field_index in range(self.field_count()):
            if CUtils.equal_ignore_case(self.field_name(field_index), name):
                return self._value_by_index(field_index)

        return None

    def size(self) -> int:
        return self._data.GetFeatureCount(0)

    def _value_by_index(self, index: int):
        if self._record.IsFieldSetAndNotNull(index):
            return self.mdb_chinese_conversion(self._record.GetFieldAsString(index))
            # return self._record.GetFieldAsString(index)
        return None

    def field_count(self) -> int:
        layer_def_obj = self._data.GetLayerDefn()
        return layer_def_obj.GetFieldCount()

    def field_obj_by_index(self, index: int):
        return self._data.GetLayerDefn().GetFieldDefn(index)

    def field_name(self, field_index: int):
        return self.mdb_chinese_conversion(self.field_obj_by_index(field_index).GetNameRef())

    def mdb_chinese_conversion(self, content):
        """
        因win下gdal读取mdb的中文内容存在编码异常，所以用此方法解决这个问题
        """
        if self._mdb_flag:
            return CUtils.conversion_chinese_code(content)
        else:
            return content
