# -*- coding: utf-8 -*- 
# @Time : 2020/9/25 08:06 
# @Author : 王西亚 
# @File : c_parser.py
from abc import abstractmethod
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CUtils
from imetadata.business.metadata.base.fileinfo.c_dmFilePathInfoEx import CDMFilePathInfoEx


class CParser(CResource):
    __object_id__ = None
    __object_name__ = None
    __file_info__: CDMFilePathInfoEx = None

    def __init__(self, object_id: str, object_name: str, file_info: CDMFilePathInfoEx):
        self.__object_id__ = object_id
        self.__file_info__ = file_info
        self.__object_name__ = object_name
        self.custom_init()

    @property
    def object_id(self):
        return self.__object_id__

    @property
    def object_name(self):
        return self.__object_name__

    @property
    def file_info(self):
        return self.__file_info__

    @abstractmethod
    def process(self) -> str:
        """
        :return:
        """
        return CUtils.merge_result(self.Success, '处理完毕!')

    def custom_init(self):
        """
        自定义初始化
        对详情文件的路径, 匹配串, 匹配类型和是否递归处理进行设置
        :return:
        """
        pass
