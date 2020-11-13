#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
作者: 王西亚
日期: 2020-08-11
内容: JSON对象操作封装

测试要求:
1.每一个方法均可用
2.每一个方法均支持中文, 包括但不限于
  中文路径
  中文标签名称
  中文标签文本
  中文属性名称
  中文属性值
"""

from __future__ import absolute_import

import demjson
import jsonpath

from imetadata.base.c_utils import CUtils


class CJson:
    Encoding_UTF8 = 'UTF-8'
    Encoding_GBK = 'GB2312'

    __json_obj = None

    def __init__(self):
        self.__json_obj = dict()

    def load_file(self, filename):
        """
        通过给定的xml文件名, 对xml对象进行初始化

        :param filename:
        :return:
        """
        self.__json_obj = demjson.decode_file(filename)

    def load_json_text(self, json_content: str):
        """
        通过给定的xml内容, 对xml对象进行初始化

        :param json_content:
        :return:
        """
        rt_json_content = json_content
        if rt_json_content is None:
            rt_json_content = '{}'
        elif rt_json_content == '':
            rt_json_content = '{}'

        self.__json_obj = demjson.decode(rt_json_content)

    def load_obj(self, obj):
        """
        通过给定的xml内容, 对xml对象进行初始化

        :param obj:
        :return:
        """
        self.load_json_text(demjson.encode(obj))

    def to_json(self) -> str:
        return demjson.encode(self.__json_obj)

    def to_file(self, filename):
        demjson.encode_to_file(filename, self.__json_obj, overwrite=True)

    def set_value_of_name(self, name, value):
        self.__json_obj[name] = value

    @property
    def json_obj(self):
        return self.__json_obj

    def xpath_one(self, query, attr_value_default) -> any:
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :param query:
        :param attr_value_default:
        :return:
        """
        result_list = self.xpath(query)
        if len(result_list) == 0:
            return attr_value_default
        elif len(result_list) >= 1:
            return result_list[0]

    def xpath(self, query) -> list:
        """
        获取一个属性的值, 如果属性不存在, 则返回默认值

        :param query:
        :return:
        """
        result_list = jsonpath.jsonpath(self.__json_obj, query)
        if not result_list:
            return []
        else:
            return result_list

    @classmethod
    def json_path(cls, json_text, json_path_str: str) -> list:
        """
        获取一个属性的值, 如果属性不存在, 则返回默认值

        :param json_path_str:
        :param json_text:
        :param attr_value_default:
        :return:
        """
        if json_text is None:
            return []
        elif str(json_text) == '':
            return []
        else:
            json = CJson()
            try:
                json.load_json_text(json_text)
                return json.xpath(json_path_str)
            except Exception as err:
                return []

    @classmethod
    def json_attr_value(cls, json_text, json_path_str: str, attr_value_default) -> any:
        """
        获取一个属性的值, 如果属性不存在, 则返回默认值

        :param json_path_str:
        :param json_text:
        :param attr_value_default:
        :return:
        """
        if json_text is None:
            return attr_value_default
        elif str(json_text) == '':
            return attr_value_default
        else:
            json = CJson()
            try:
                json.load_json_text(json_text)
                return json.xpath_one(json_path_str, attr_value_default)
            except Exception as err:
                return attr_value_default

    @classmethod
    def json_set_attr(cls, json_text, attr_name: str, attr_value) -> str:
        new_result = CJson()
        rt_json_text = CUtils.any_2_str(json_text)
        if not CUtils.equal_ignore_case(rt_json_text, ''):
            new_result.load_json_text(rt_json_text)

        new_result.set_value_of_name(attr_name, attr_value)
        return new_result.to_json()

    @classmethod
    def json_join(cls, json_path: str, *json_suffix) -> str:
        result_path = json_path
        for suffix in json_suffix:
            result_path = '{0}.{1}'.format(result_path, suffix)
        return result_path

    @classmethod
    def file_2_str(cls, filename) -> str:
        json = CJson()
        json.load_file(filename)
        return json.to_json()

    @classmethod
    def dict_data_by_path(cls, obj: dict, path_str: str) -> list:
        """
        将一个字典对象, 按json解析, 并以指定的path获取其中的对象

        :param path_str:
        :param obj:
        :return:
        """
        if obj is None:
            return []
        elif str(obj) == '':
            return []
        else:
            json = CJson()
            try:
                json.load_obj(obj)
                return json.xpath(path_str)
            except Exception as err:
                return []

    @classmethod
    def dict_attr_by_path(cls, obj: dict, path_str: str, attr_value_default=None):
        """
        将一个字典对象, 按json解析, 并以指定的path获取其中的对象

        :param attr_value_default:
        :param path_str:
        :param obj:
        :return:
        """
        if obj is None:
            return attr_value_default
        elif str(obj) == '':
            return attr_value_default
        else:
            json = CJson()
            try:
                json.load_obj(obj)
                return json.xpath_one(path_str, attr_value_default)
            except Exception as err:
                return attr_value_default


if __name__ == '__main__':
    dict_obj = {'a': {'name': 'a1', 'sex': 0, 'birthday': '2020-01-01'}, 'b': 'other'}
    print(CJson.dict_attr_by_path(dict_obj, 'a.birthday1'))
    dict_obj = {'a': ["a1", "a2", "a3"], 'b': 'other'}
    json_obj = CJson()
    json_obj.load_obj(dict_obj)
    a_list = json_obj.xpath_one('a', None)
    print(a_list)
    print(type(a_list))

