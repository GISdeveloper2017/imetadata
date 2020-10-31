# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:11 
# @Author : 王西亚 
# @File : c_fileInfoEx.py

from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfo import CFileInfo
from imetadata.base.c_xml import CXml


class CFileInfoEx(CFileInfo):
    # 入库规则
    __rule_content: str

    __file_name_with_rel_path__: str
    __file_path_with_rel_path__: str

    __root_path__ = str

    def __init__(self, file_type, file_name_with_full_path, root_path, rule_content):
        super().__init__(file_type, file_name_with_full_path)
        self.__root_path__ = root_path

        self.__file_name_with_rel_path__ = CFile.file_relation_path(self.__file_name_with_full_path__,
                                                                    self.__root_path__)
        self.__file_path_with_rel_path__ = CFile.file_relation_path(self.__file_path__, self.__root_path__)

        self.__rule_content = rule_content

    def rule_id(self, default_value):
        if self.__rule_content == '':
            return default_value
        else:
            xml_obj = CXml()
            try:
                xml_obj.load_xml(self.__rule_content)
                return CXml.get_element_text(xml_obj.xpath_one('/root/ProductType'))
            except:
                return default_value

    @property
    def rule_content(self):
        return self.__rule_content
