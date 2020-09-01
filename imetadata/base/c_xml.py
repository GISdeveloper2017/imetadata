#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
作者: 王西亚
日期: 2020-08-11
内容: XML对象操作封装

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
from lxml import etree
from copy import deepcopy
from io import StringIO


class CXml:
    Encoding_UTF8 = 'UTF-8'
    Encoding_GBK = 'GB2312'

    __xml_tree__ = None
    __xml_root_node__ = None

    def __init__(self):
        pass

    def get_tree(self) -> etree:
        return self.__xml_tree__

    def get_root(self) -> etree:
        return self.__xml_root_node__

    def load_file(self, filename):
        """
        通过给定的xml文件名, 对xml对象进行初始化

        :param filename:
        :return:
        """
        # parser = etree.XMLParser(encoding='utf-8', strip_cdata=False)
        # self.__xml_tree__ = etree.parse(filename, parser)
        self.__xml_tree__ = etree.ElementTree(file=filename)
        self.__xml_root_node__ = self.__xml_tree__.getroot()

    def load_xml(self, xml_content: str):
        """
        通过给定的xml内容, 对xml对象进行初始化

        :param xml_content:
        :return:
        """
        parser = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
        self.__xml_root_node__ = etree.XML(xml_content.strip(), parser)
        # self.__xml_root_node__ = etree.fromstring(xml_content.strip())
        self.__xml_tree__ = etree.ElementTree(self.__xml_root_node__)

    def new_xml(self, root_element_name):
        """
        新建一个xml对象, 必须给定根节点名称

        :param root_element_name:
        :return:
        """
        self.__xml_root_node__ = etree.Element(root_element_name)
        self.__xml_tree__ = etree.ElementTree(self.__xml_root_node__)

    def save_file(self, filename, encoding=Encoding_UTF8):
        """
        通过给定的xml文件名, 对xml对象进行初始化
        :param filename:
        :param encoding:
        :return:
        """
        self.__xml_tree__ = etree.ElementTree(self.__xml_root_node__)
        self.__xml_tree__.write(filename, encoding=encoding, xml_declaration=True)

    def to_xml(self) -> str:
        """
        通过给定的xml内容, 对xml对象进行初始化
        :return:
        """
        return bytes.decode(etree.tostring(self.__xml_tree__, xml_declaration=False))

    def xpath_one(self, query) -> etree:
        """
        根据给定的xpath查询语句, 查询出合适的第一个节点
        :param query:
        :return:
        """
        result_list = self.xpath_all(query)
        if len(result_list) == 0:
            return None
        else:
            return result_list[0]

    def xpath_all(self, query) -> list:
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :param query:
        :return: 如果没有任何合适的节点, 则返回空的列表, 不会直接返回None
        """
        return self.__xml_tree__.xpath(query)

    @classmethod
    def clone(cls, element) -> etree:
        """
        根据给定的xml节点, 深度克隆节点的全部内容, 创建一个新的节点
        :param element:
        :return:
        """
        return deepcopy(element)[0]

    @classmethod
    def append(cls, element, child_element) -> etree:
        """
        将一个子节点加入到指定节点下
        :param element:
        :param child_element:
        :return:
        """
        return element.append(child_element)

    @classmethod
    def create_element(cls, element, element_name) -> etree:
        """
        在一个节点下创建一个新节点
        :param element:
        :param element_name:
        :return:
        """
        return etree.SubElement(element, element_name)

    @classmethod
    def set_attr(cls, element, attr_name, attr_value):
        """
        设置一个节点的属性

        :param element:
        :param attr_name:
        :param attr_value:
        :return:
        """
        element.set(attr_name, attr_value)

    @classmethod
    def get_attr(cls, element, attr_name, attr_value_default, ignore_case=True) -> str:
        """
        获取一个属性的值, 如果属性不存在, 则返回默认值

        todo 未完成
        :param element:
        :param attr_name:
        :param attr_value_default:
        :param ignore_case: 大小写是否敏感
        :return:
        """
        value = element.get(attr_name)
        if value is None:
            return attr_value_default
        else:
            return value

    @classmethod
    def set_element_text(cls, element, text):
        """
        设置一个节点的文本
        :param element:
        :param text:
        :return:
        """

        element.text = etree.CDATA(text)

    @classmethod
    def get_element_text(cls, element):
        """
        获取一个节点的文本
        :param element:
        :return:
        """
        if element is not None:
            text = element.text
            if text is None:
                return ''
            else:
                return text
        else:
            return ''

    @classmethod
    def get_element_xml(cls, element) -> str:
        """
        获取一个节点内容
        :param element:
        :return:
        """
        if element is None:
            return ''
        else:
            return bytes.decode(etree.tostring(element, xml_declaration=False, encoding='utf-8'))

    @classmethod
    def get_element_name(cls, element) -> etree:
        """
        获取节点的名称
        :param element:
        :return:
        """
        return element.tag

    @classmethod
    def is_element_comment(cls, element) -> bool:
        """
        判断一个节点是否是备注
        :param element:
        :return:
        """
        return isinstance(element, etree._Comment)

    @classmethod
    def is_element_equal(cls, element_1: etree, element_2: etree) -> bool:
        """
        判断一个节点是否是备注
        :param element_1:
        :param element_2:
        :return:
        """
        text_1 = cls.get_element_xml(element_1)
        text_2 = cls.get_element_xml(element_2)
        return text_1 == text_2

    @classmethod
    def is_element_equal_text(cls, element: etree, text: str) -> bool:
        """
        判断一个节点是否是备注
        :param text:
        :param element:
        :return:
        """
        xml = CXml()
        xml.load_xml(text)
        root = xml.get_root()
        print(root)
        return cls.is_element_equal(element, root)

    @classmethod
    def get_tree(cls, element):
        """
        获取节点所在的树对象
        :param element:
        :return:
        """
        return etree.ElementTree(element)

    @classmethod
    def get_tree_root(cls, tree) -> etree:
        """
        获取树对象的根节点
        :param tree:
        :return:
        """
        return tree.getroot()
