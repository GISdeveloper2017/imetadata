#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
c_xml.py的测试文
"""

from lxml import etree

from imetadata.base.c_xml import CXml


class Test_Base_C_XML:
    test_filename: str = r"C:\Users\Clare\PycharmProjects\pythonProject\test1.xml"

    def test_load_file(self):
        """
        通过给定的xml文件名, 对xml对象进行初始化
        """
        xml = CXml()
        xml.load_file(self.test_filename)
        assert True

    def test_load_xml(self):
        """
        通过给定的xml内容, 对xml对象进行初始化
        """
        xml_content = '''
        <root name="hello world"></root>
        '''
        xml = CXml()
        xml.load_xml(xml_content)
        assert True

    def test_new_xml(self):
        """
        新建一个xml对象, 必须给定根节点名称
        """
        root_element_name = "root"
        xml = CXml()
        xml.new_xml(root_element_name)
        assert True

    def test_save_file(self):
        """
        通过给定的xml文件名, 对xml对象进行初始化
        """
        xml_content = '''
        <root name="hello world">hello</root>
        '''
        xml = CXml()
        xml.load_xml(xml_content)
        xml.save_file(self.test_filename, encoding=CXml.Encoding_UTF8)
        assert True

    def test_to_xml(self):
        """
        通过给定的xml内容, 对xml对象进行初始化
        :return:
        """
        xml = CXml()
        xml_content = '''
        <root><element>hello</element></root>
        '''
        xml.load_xml(xml_content)
        xmlString = xml.to_xml()
        assert xmlString == '<root><element>hello</element></root>'

    def test_xpath(self):
        """
        根据给定的xpath查询语句, 查询出合适的节点
        :return:
        """
        xml = CXml()
        xml_comment = u'<root name="hello world"><element name="zg">hello</element></root>'
        xml.load_xml(xml_comment)
        xmlString = xml.to_xml()
        result = xml.xpath_one('./element')
        assert CXml.get_element_xml(result) == '<element name="zg">hello</element>'

    def test_clone(self):
        """
        根据给定的xml节点, 深度克隆节点的全部内容, 创建一个新的节点
        :return:
        """
        xml = CXml()
        xml_comment = '''<root name="hello world"><element>hello</element></root>'''
        xml.load_xml(xml_comment)
        element = CXml.clone(xml.__xml_root_node__)
        assert CXml.get_element_xml(element) == xml_comment

    def test_append(self):
        """
        将一个子节点加入到指定节点下
        :return:
        """
        xml_content = '''<root name="hello world"></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        child_element = etree.Element('train', name='wing')
        element = xml.__xml_root_node__
        CXml.append(element, child_element)
        assert CXml.get_element_xml(element) == '<root name="hello world"><train name="wing"/></root>'

    def test_creat_element(self):
        """
        在一个节点下创建一个新节点
        :return:
        """
        xml_content = '''
            <root name="hello world"><element name="hello"></element></root>
            '''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.__xml_root_node__
        CXml.create_element(element, "element1")
        assert CXml.get_element_xml(element) == '<root name="hello world"><element name="hello"/><element1/></root>'

    def test_set_attr(self):
        """
        设置一个节点的属性
        :return:
        """
        xml_content = '''<root name="hello world"></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.xpath_one('/root')
        CXml.set_attr(element, 'name', 'championing')
        assert CXml.get_element_xml(element) == '<root name="championing"/>'

    def test_get_attr(self):
        """
        获取一个属性的值, 如果属性不存在, 则返回默认值
        :return:
        """
        xml_content = '''<root name="hello world"><element hello="中国"></element><element hello="美国"></element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.xpath('/root/element')[1]
        value = CXml.get_attr(element, 'Hello', "null")
        assert value == '美国'

    def test_set_element_text(self):
        """
        设置一个节点的文本
        :return:
        """
        xml_content = '''<root name="hello world"></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.xpath('/root')[0]
        CXml.set_element_text(element, 'hello')
        assert CXml.get_element_xml(element) == '<root name="hello world"><![CDATA[hello]]></root>'

    def test_get_element_text(self):
        """
        获取一个节点的文本
        :return:
        """
        xml_content = '''<root name="hello world"><element>world</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.xpath('/root/element')[0]
        text = CXml.get_element_text(element)
        assert text == 'world'

    def test_get_element_root(self):
        """
        获取节点的根节点
        :return:
        """
        xml_content = '''<root name="hello world"><element>hello</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.__xml_root_node__[0]
        rt = CXml.get_element_root(element)
        assert CXml.get_element_xml(rt) == xml_content

    def test_get_element_xml(self):
        """
        获取一个节点内容
        :return:
        """
        xml_content = '''<root name="hello world"><element>hello</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        assert CXml.get_element_xml(xml.__xml_tree__) == xml_content

    def test_get_element_name(self):
        """
        获取节点的名称
        :return:
        """
        xml_content = '''<root name="hello world"><element>hello</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.xpath('/root/element')[0]
        name = CXml.get_element_name(element)
        assert name == 'element'

    def test_is_element_comment(self):
        """
        判断一个节点是否是备注
        """
        xml_content = '''<root name="hello world"><element>hello</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.xpath('/root/element')[0]
        flag = xml.is_element_comment(element)
        assert flag is False

    def test_get_tree(self):
        """
        获取节点所在的树对象
        :return:
        """
        xml_content = '''<root name="hello world"><element>hello</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        element = xml.__xml_root_node__
        tree = CXml.get_tree(element)
        assert CXml.get_element_xml(tree) == xml_content

    def test_get_tree_root(self):
        """
        获取树对象的根节点
        :return:
        """
        xml_content = '''<root name="hello world"><element>hello</element></root>'''
        xml = CXml()
        xml.load_xml(xml_content)
        tree = CXml.get_tree_root(xml.__xml_tree__)
        assert CXml.get_element_xml(tree) == xml_content
