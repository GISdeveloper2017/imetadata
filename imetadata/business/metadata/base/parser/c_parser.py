# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:06 
# @Author : 王西亚 
# @File : c_parser.py
from abc import abstractmethod

from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils


class CParser(CResource):
    __db_server_id__ = None
    __object_id__ = None
    __file_info__: CFileInfoEx = None

    def __init__(self, db_server_id: str, object_id: str, file_info: CFileInfoEx):
        self.__db_server_id__ = db_server_id
        self.__object_id__ = object_id
        self.__file_info__ = file_info
        self.custom_init()

    @abstractmethod
    def process(self) -> str:
        """
        :return:
        """
        return CUtils.merge_result(self.Success, '处理完毕!')

    @abstractmethod
    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        pass
