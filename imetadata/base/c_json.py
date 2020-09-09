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

from imetadata.base.c_logger import CLogger
from imetadata.base.c_utils import CMetaDataUtils


class CJson:
    Encoding_UTF8 = 'UTF-8'
    Encoding_GBK = 'GB2312'

    __json_obj__: object

    def __init__(self):
        pass

    def load_file(self, filename):
        """
        通过给定的xml文件名, 对xml对象进行初始化

        :param filename:
        :return:
        """
        self.__json_obj__ = demjson.encode(filename)

    def load_json_text(self, json_content: str):
        """
        通过给定的xml内容, 对xml对象进行初始化

        :param json_content:
        :return:
        """
        self.__json_obj__ = demjson.decode(json_content)

    def load_obj(self, obj):
        """
        通过给定的xml内容, 对xml对象进行初始化

        :param obj:
        :return:
        """
        self.load_json_text(demjson.encode(obj))

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
        result_list = jsonpath.jsonpath(self.__json_obj__, query)
        if not result_list:
            return []
        else:
            return result_list

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
        else:
            json = CJson()
            CLogger().debug('Json解析{0}'.format(json_text))
            try:
                json.load_json_text(json_text)
                return json.xpath_one(json_path_str, attr_value_default)
            except Exception as err:
                return attr_value_default