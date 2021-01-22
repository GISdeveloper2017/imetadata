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

import re
from copy import deepcopy

from lxml import etree

from imetadata.base.c_file import CFile
from imetadata.base.c_utils import CUtils
from imetadata.base.c_exceptions import PathNotCreateException


class CXml:
    Encoding_UTF8 = 'UTF-8'
    Encoding_GBK = 'GB2312'

    __xml_tree = None
    __xml_root_node = None

    def __init__(self):
        pass

    def load_file(self, filename):
        """
        通过给定的xml文件名, 对xml对象进行初始化

        :param filename:
        :return:
        """
        # parser = etree.XMLParser(encoding='utf-8', strip_cdata=False)
        # self.__xml_tree__ = etree.parse(filename, parser)
        self.__xml_tree = etree.ElementTree(file=filename)
        self.__xml_root_node = self.__xml_tree.getroot()

    def load_xml(self, xml_content: str):
        """
        通过给定的xml内容, 对xml对象进行初始化

        :param xml_content:
        :return:
        """
        if not CUtils.equal_ignore_case(CUtils.any_2_str(xml_content), ''):
            parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
            self.__xml_root_node = etree.XML(xml_content.strip(), parser)
            self.__xml_tree = etree.ElementTree(self.__xml_root_node)

    def new_xml(self, root_element_name) -> etree.Element:
        """
        新建一个xml对象, 必须给定根节点名称

        :param root_element_name:
        :return:
        """
        self.__xml_root_node = etree.Element(root_element_name)
        self.__xml_tree = etree.ElementTree(self.__xml_root_node)
        return self.__xml_root_node

    def save_file(self, filename, encoding=Encoding_UTF8):
        """
        通过给定的xml文件名, 对xml对象进行初始化
        :param filename:
        :param encoding:
        :return:
        """
        CFile.check_and_create_directory(filename)
        self.__xml_tree = etree.ElementTree(self.__xml_root_node)
        self.__xml_tree.write(filename, encoding=encoding, xml_declaration=True)

    def to_file(self, filename, encoding=Encoding_UTF8):
        self.save_file(filename, encoding)

    def to_xml(self) -> str:
        """
        通过给定的xml内容, 对xml对象进行初始化
        :return:
        """
        return etree.tostring(self.__xml_tree, xml_declaration=False, pretty_print=False, encoding="utf-8").decode(
            'utf-8')

    def xpath_one(self, query, namespace=None) -> etree:
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :param query:
        :param namespace:
        :return:
        """
        list_result = self.xpath(query, namespace)
        if len(list_result) == 0:
            return None
        else:
            return list_result[0]

    def xpath(self, query, namespace=None) -> list:
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :param query:
        :param namespace:
        :return:
        """
        if self.__xml_tree is None:
            return []
        else:
            return self.__xml_tree.xpath(query, namespaces=namespace)

    @classmethod
    def node_xpath_one(cls, xml_node, query) -> etree:
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :param xml_node:
        :param query:
        :return:
        """
        list_result = cls.node_xpath(xml_node, query)
        if len(list_result) == 0:
            return None
        else:
            return list_result[0]

    @classmethod
    def node_xpath(cls, xml_node, query) -> etree:
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :param xml_node:
        :param query:
        :return:
        """
        if xml_node is None:
            return []
        else:
            return xml_node.xpath(query)

    @classmethod
    def clone(cls, element) -> etree:
        """
        根据给定的xml节点, 深度克隆节点的全部内容, 创建一个新的节点
        :param element:
        :return:
        """
        if element is not None:
            return deepcopy(element)

    @classmethod
    def append(cls, element, child_element):
        """
        将一个子节点加入到指定节点下
        :param element:
        :param child_element:
        :return:
        """
        if element is not None:
            return element.append(child_element)

    @classmethod
    def create_element(cls, element, element_name):
        """
        在一个节点下创建一个新节点
        :param element:
        :param element_name:
        :return:
        """
        if element is not None:
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
        if element is not None:
            element.set(attr_name, CUtils.any_2_str(attr_value))

    @classmethod
    def get_attr(cls, element, attr_name, attr_value_default, ignore_case=True) -> str:
        """
        获取一个属性的值, 如果属性不存在, 则返回默认值

        :param element:
        :param attr_name:
        :param attr_value_default:
        :param ignore_case:
        :return:
        """
        if element is None:
            return attr_value_default

        if ignore_case is True:
            ac = element.keys()[0]
            attr_name = re.findall(attr_name, ac, re.IGNORECASE)
            if len(attr_name) == 0:
                return attr_value_default
            else:
                name = attr_name[0]
        else:
            name = attr_name

        value = element.get(name)
        if value is None:
            return attr_value_default
        else:
            return value

    @classmethod
    def attr_exist(cls, element, attr_name, ignore_case=True) -> bool:
        if element is None:
            return False

        ac = element.keys()[0]
        if ignore_case is True:
            attr_name = re.findall(attr_name, ac, re.IGNORECASE)
        else:
            attr_name = re.findall(attr_name, ac)
        return len(attr_name) > 0

    @classmethod
    def set_element_text(cls, element, text):
        """
        设置一个节点的文本
        :param element:
        :param text:
        :return:
        """
        if element is not None:
            element.text = etree.CDATA(CUtils.any_2_str(text))

    @classmethod
    def get_element_text(cls, element):
        """
        获取一个节点的文本
        :param element:
        :return:
        """
        if element is None:
            return ''
        else:
            return element.text

    def get_element_text_by_xpath_one(self, query: str, namespace=None):
        """
        根据xpath路径获取对应节点的文本
        :param query:
        :param namespace:
        :return:
        """
        node_element = self.xpath_one(query, namespace)
        node_text = self.get_element_text(node_element)
        return node_text

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
            return bytes.decode(etree.tostring(element, xml_declaration=False))

    def root_element(self) -> etree.Element:
        """
        获取节点的根节点
        :param element:
        :return:
        """
        if self.__xml_root_node is None:
            self.__xml_root_node = self.__xml_tree.getroot()
        return self.__xml_root_node

    def tree(self) -> etree.ElementTree:
        """
        获取节点的根节点
        :param element:
        :return:
        """
        return self.__xml_tree

    @classmethod
    def get_element_root(cls, element: etree.Element) -> etree.Element:
        """
        获取节点的根节点
        :param element:
        :return:
        """
        return cls.get_tree_root(cls.get_element_tree(element))

    @classmethod
    def get_element_tree(cls, element: etree.Element) -> etree.ElementTree:
        if element is None:
            return None
        else:
            return element.getroottree()

    @classmethod
    def get_element_name(cls, element) -> str:
        """
        获取节点的名称
        :param element:
        :return:
        """
        if element is None:
            return None
        else:
            return element.tag

    @classmethod
    def is_element_comment(cls, element) -> bool:
        """
        判断一个节点是否是备注
        :param element:
        :return:
        """
        if element is None:
            return False
        else:
            return isinstance(element, etree._Comment)

    @classmethod
    def get_tree_root(cls, tree: etree.ElementTree) -> etree.Element:
        """
        获取树对象的根节点
        :param tree:
        :return:
        """
        if tree is None:
            return None
        else:
            return tree.getroot()

    @classmethod
    def file_2_str(cls, filename) -> str:
        if not CFile.file_or_path_exist(filename):
            return ''

        xml_obj = CXml()
        xml_obj.load_file(filename)
        return xml_obj.to_xml()

    @classmethod
    def str_2_file(cls, xml_content: str, filename: str) -> str:
        if not CFile.check_and_create_directory(filename):
            raise PathNotCreateException(filename)

        xml_obj = CXml()
        xml_obj.load_xml(xml_content)
        xml_obj.to_file(filename, cls.Encoding_UTF8)

    @classmethod
    def remove(cls, xml_node: etree):
        if xml_node is None:
            return

        parent_node = xml_node.getparent()
        if parent_node is None:
            return

        parent_node.remove(xml_node)

    @classmethod
    def xml_xpath(cls, xml_str: str, query: str) -> list:
        try:
            xml_obj = CXml()
            xml_obj.load_xml(xml_str)
            return xml_obj.xpath(query)
        except:
            return []

    @classmethod
    def xml_xpath_one(cls, xml_str: str, query: str):
        try:
            xml_obj = CXml()
            xml_obj.load_xml(xml_str)
            return xml_obj.xpath_one(query)
        except:
            return None

    @classmethod
    def file_xpath(cls, file_name: str, query: str) -> list:
        try:
            xml_obj = CXml()
            xml_obj.load_file(file_name)
            return xml_obj.xpath(query)
        except:
            return []

    @classmethod
    def file_xpath_one(cls, file_name: str, query: str):
        try:
            xml_obj = CXml()
            xml_obj.load_file(file_name)
            return xml_obj.xpath_one(query)
        except:
            return None


if __name__ == '__main__':
    xml_content = '''<root name="hello world"><parent><![CDATA[this is root.]]><grandson>hello</grandson></parent></root>'''
    xml = CXml()
    xml.load_xml(xml_content)
    root = xml.root_element()
    print(CXml.get_element_xml(root))
    grandson_list = CXml.node_xpath(root, './parent/*')
    print(len(grandson_list))
    for grandson in grandson_list:
        print(type(grandson))
        print(CXml.get_element_xml(grandson))
