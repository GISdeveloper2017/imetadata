#!/usr/bin/python3
# -*- coding:utf-8 -*-

from __future__ import absolute_import
import uuid
import re
from imetadata.base.c_json import CJson
from imetadata.base.c_resource import CResource


class CUtils(CResource):

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
    def result_success(cls, result_text) -> bool:
        return CJson.json_attr_value(result_text, cls.Name_Result, cls.Failure) == cls.Success

    @classmethod
    def result_message(cls, result_text) -> str:
        return CJson.json_attr_value(result_text, cls.Name_Message, '')

    @classmethod
    def one_id(cls) -> str:
        name = 'metadata.org'
        uuid_text = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid4())))
        uuid_text = uuid_text.replace('-', '')
        return uuid_text

    @classmethod
    def plugins_id_by_file_main_name(cls, file_main_name) -> str:
        super_id = file_main_name
        id_list = super_id.split('_', 2)
        if len(id_list) > 2:
            return id_list[2]
        else:
            return super_id

    @classmethod
    def equal_ignore_case(cls, str1: str, str2: str) -> bool:
        return str1.strip().lower() == str2.strip().lower()

    @classmethod
    def dict_value_by_name(cls, dict_obj: dict, name: str, ignore_case=True) -> any:
        keys = dict_obj.keys()
        for key in keys:
            if ignore_case:
                if cls.equal_ignore_case(key, name):
                    return dict_obj[key]
            else:
                if key.strip() == name.strip():
                    return dict_obj[key]
        else:
            return None

    @classmethod
    def any_2_str(cls, obj) -> str:
        if obj is None:
            return ''
        else:
            return str(obj)

    @classmethod
    def text_match_re(cls, text, regex) -> bool:
        return re.search(regex, text) is not None

    @classmethod
    def text_is_numeric(cls, check_text: str) -> bool:
        """
        判断是否为数字
        :param check_text:
        :return:
        """
        return check_text.isdigit()

    @classmethod
    def text_is_alpha(cls, check_text: str) -> bool:
        """
        判断是否字母
        :param check_text:
        :return:
        """
        return check_text.isalpha()


if __name__ == '__main__':
    text = "The rain in Spain"
    x = re.search(r"\bH\w+", text)
    if x is None:
        print('can not match')
    else:
        print(x.span())
        print(x.string)
        print(x.group())
