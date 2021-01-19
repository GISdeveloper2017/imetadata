# -*- coding: utf-8 -*- 
# @Time : 2020/10/3 12:42 
# @Author : 王西亚 
# @File : c_result.py
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource


class CResult(CResource):

    @classmethod
    def merge_result(cls, result, message=None, base=None) -> str:
        new_result = CJson()
        if base is not None:
            new_result.load_json_text(base)

        new_result.set_value_of_name(cls.Name_Result, result)
        if message is not None:
            new_result.set_value_of_name(cls.Name_Message, message)
        return new_result.to_json()

    @classmethod
    def merge_result_info(cls, result_text, info_name: str, value):
        return CJson.json_set_attr(result_text, info_name, value)

    @classmethod
    def result_success(cls, result_text) -> bool:
        return CJson.json_attr_value(result_text, cls.Name_Result, cls.Failure) == cls.Success

    @classmethod
    def result_info(cls, result_text, info_name: str, default_value):
        return CJson.json_attr_value(result_text, info_name, default_value)

    @classmethod
    def result_message(cls, result_text) -> str:
        return CJson.json_attr_value(result_text, cls.Name_Message, '')

    @classmethod
    def to_file(cls, result_text, file_name):
        return CJson.str_2_file(result_text, file_name)
