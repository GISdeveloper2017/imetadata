# -*- coding: utf-8 -*- 
# @Time : 2020/11/21 12:33 
# @Author : 王西亚 
# @File : c_column.py
from imetadata.base.c_file import CFile
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.base.c_xml import CXml


class CColumn:
    def __init__(self, name: str, db_column_type: str, primary_key: bool = False):
        self._name = name
        self._db_column_type = db_column_type
        self._primary_key = primary_key
        self._data_type = ''
        self._value = None
        self._value_type = CResource.DataValueType_SQL

    @property
    def name(self):
        return self._name

    @property
    def db_column_type(self):
        return self._db_column_type

    @property
    def data_type(self):
        return self._data_type

    def set_value(self, value):
        """
        设置value为标准值
        :param value:
        :return:
        """
        self._value_type = CResource.DataValueType_Value
        self._value = value

    def set_value_as_sql(self, sql):
        """
        设置value为原生的sql
        . 如果sql有值, 则表示value为该字符串
        . 如果sql无值, 则表示value为null
        :param sql:
        :return:
        """
        self._value_type = CResource.DataValueType_SQL
        self._value = sql

    def set_value_from_file(self, file_name: str, file_format: str, file_encoding: str):
        """
        设置value为文件内容
        . 根据文件格式, 可以加载文件内容
        . 如果文件格式为二进制, 则value存储文件名
        :param file_name:
        :param file_format:
        :param file_encoding:
        :return:
        """
        self._value_type = CResource.DataValueType_Value
        if CUtils.equal_ignore_case(file_format, CResource.FileFormat_TXT):
            self._value = CFile.file_2_str(file_name)
        elif CUtils.equal_ignore_case(file_format, CResource.FileFormat_XML):
            self._value = CXml.file_2_str(file_name)
        elif CUtils.equal_ignore_case(file_format, CResource.FileFormat_Json):
            self._value = CJson.file_2_str(file_name)
        else:
            self._value_type = CResource.DataValueType_File
            self._value = file_name

    def set_array(self, src_array: list, array_data_type: int):
        """
        设置value为数组
        . 数组数据类型可以为标准单一类型
            . DataType_String = 1
            . DataType_DateTime = 2
            . DataType_Numeric = 3
            . DataType_Bool = 4
            . DataType_Integer = 5
            ...
        . 注意: value_type为数组的特殊类型, 它的计算方法为
            . CResource.DataValueType_Array * 10 + array_data_type
        :param src_array:
        :param array_data_type:
        :return:
        """
        self._value_type = CResource.DataValueType_Array * 10 + array_data_type
        self._value = src_array

    def set_geometry(self, wkt: str, srid):
        """
        设置value为几何多边形
        . value 将存储dict字典
        . 根据srid是否提供, value存储的内容, 有所不同
        :param wkt:
        :param srid:
        :return:
        """
        self._value_type = CResource.DataValueType_Geometry
        if srid is None:
            self._value = {'wkt': wkt, 'type': CResource.DataValueType_Geometry_NoSrid}
        else:
            self._value = {'wkt': wkt, 'srid': srid, 'type': CResource.DataValueType_Geometry_Srid}
