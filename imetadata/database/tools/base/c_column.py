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
    _value = None

    def __init__(self, name: str, db_column_type: str, primary_key: bool = False):
        self._name = name
        self._db_column_type = db_column_type
        self._primary_key = primary_key
        self.reset()

    @property
    def name(self):
        return self._name

    @property
    def db_column_type(self):
        return self._db_column_type

    @property
    def value(self):
        return self._value

    @property
    def is_primary_key(self):
        return self._primary_key

    def reset(self):
        self._value = None

    def set_null(self):
        """
        设置value为标准值
        :param value:
        :return:
        """
        self.set_sql(CResource.Name_Null)

    def set_value(self, value):
        """
        设置value为标准值
        :param value:
        :return:
        """
        if value is None:
            self.set_null()
        else:
            self._value = {CResource.Name_Text: value, CResource.Name_Type: CResource.DataValueType_Value}

    def set_sql(self, sql):
        """
        设置value为原生的sql
        . 如果sql有值, 则表示value为该字符串
        . 如果sql无值, 则表示value为null
        :param sql:
        :return:
        """
        self._value = {CResource.Name_Text: sql, CResource.Name_Type: CResource.DataValueType_SQL}

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
        if CUtils.equal_ignore_case(file_format, CResource.FileFormat_TXT):
            self._value = {
                CResource.Name_Text: CFile.file_2_str(file_name),
                CResource.Name_Type: CResource.DataValueType_SQL
            }
        elif CUtils.equal_ignore_case(file_format, CResource.FileFormat_XML):
            self._value = {
                CResource.Name_Text: CXml.file_2_str(file_name),
                CResource.Name_Type: CResource.DataValueType_SQL
            }
        elif CUtils.equal_ignore_case(file_format, CResource.FileFormat_Json):
            self._value = {
                CResource.Name_Text: CJson.file_2_str(file_name),
                CResource.Name_Type: CResource.DataValueType_SQL
            }
        else:
            self._value = {
                CResource.Name_Text: file_name,
                CResource.Name_Type: CResource.DataValueType_File
            }

    def set_array(self, src_array: list):
        """
        设置value为数组
        :param src_array:
        :return:
        """
        if len(src_array) == 0:
            self.reset()
        else:
            if isinstance(src_array[0], str):
                array_text = CUtils.list_2_str(src_array, "'", ',', "'")
            else:
                array_text = CUtils.list_2_str(src_array, '', ',', '')
            self._value = {
                CResource.Name_Text: array_text,
                CResource.Name_Type: CResource.DataValueType_Value,
                CResource.Name_Value: src_array
            }

    def set_array_str(self, array_text: str):
        """
        设置value为数组
        :param array_text:
        :return:
        """
        self._value = {
            CResource.Name_Text: array_text,
            CResource.Name_Type: CResource.DataValueType_Value,
            CResource.Name_Value: array_text
        }

    def set_geometry(self, wkt: str, srid):
        """
        设置value为几何多边形
        . value 将存储dict字典
        . 根据srid是否提供, value存储的内容, 有所不同
        :param wkt:
        :param srid:
        :return:
        """
        self._value = {
            CResource.Name_Text: wkt,
            CResource.Name_Type: CResource.DataValueType_Value
        }
        if srid is not None:
            self._value[CResource.Name_Srid] = srid
