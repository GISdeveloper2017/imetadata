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

    __file_name_with_rel_path: str
    __file_path_with_rel_path: str

    __root_path: str

    @property
    def file_name_with_rel_path(self):
        return self.__file_name_with_rel_path

    @property
    def root_path(self):
        return self.__root_path

    @property
    def file_path_with_rel_path(self):
        return self.__file_path_with_rel_path

    def __init__(self, file_type, file_name_with_full_path, root_path, rule_content):
        super().__init__(file_type, file_name_with_full_path)
        self.__root_path = root_path

        self.__file_name_with_rel_path = CFile.file_relation_path(
            self.file_name_with_full_path,
            self.__root_path)
        self.__file_path_with_rel_path = CFile.file_relation_path(self.file_path, self.__root_path)

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
