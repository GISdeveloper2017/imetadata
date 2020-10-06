# -*- coding: utf-8 -*- 
# @Time : 2020/10/2 20:57 
# @Author : 王西亚 
# @File : c_mdExtractor.py
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx
from imetadata.business.metadata.base.parser.c_parser import CParser


class CSpatialExtractor(CParser):
    __file_content__: CVirtualContent = None

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx, file_content: CVirtualContent):
        self.__file_content__ = file_content
        super().__init__(object_id, object_name, file_info)

    @property
    def file_content(self):
        return self.__file_content__
