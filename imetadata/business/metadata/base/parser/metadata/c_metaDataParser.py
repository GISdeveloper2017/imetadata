# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 09:08 
# @Author : 王西亚 
# @File : c_metaDataParser.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent
from imetadata.business.metadata.base.parser.c_parser import CParser


class CMetaDataParser(CParser):
    """
    对象元数据处理类
    在本对象中, 要处理如下内容:
    . 对象的业务元数据
    . 对象的基础元数据
    . 对象的质检
    . 对象的可视元数据
    . 对象的元数据优化
    """
    __information__: dict
    __file_content__: CVirtualContent = None

    def __init__(self, db_server_id: str, object_id: str, file_info: CFileInfoEx, file_content: CVirtualContent, information: dict):
        self.__information__ = information
        self.__file_content__ = file_content
        super().__init__(db_server_id, object_id, file_info)

    def process(self) -> str:
        pass

    def custom_init(self):
        pass
