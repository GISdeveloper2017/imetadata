# -*- coding: utf-8 -*- 
# @Time : 2020/9/14 16:24 
# @Author : 王西亚 
# @File : c_plugins.py

from abc import abstractmethod
from imetadata.base.c_logger import CLogger
from imetadata.base.c_resource import CResource
from imetadata.base.c_utils import CMetaDataUtils


class CPlugins(CResource):
    """
    数据识别插件
    """
    __target_file_or_path_name__: str
    __target_type__: str

    def __init__(self, target_file_or_path_name, target_type):
        self.__target_file_or_path_name__ = target_file_or_path_name
        self.__target_type__ = target_type

    @abstractmethod
    def get_group_name(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def classified(self):
        """
        对目标目录或文件进行分类
        :return: 返回四个结果
        .[0]: 识别的对象的名称, 如GF1-xxxxxx-000-000
        .[1]: 识别的对象类型, 如gf1, gf2, ...
        .[2]: 识别的对象类型的分组, 如sat-卫星数据
        .[3]: 概率, 0-不知道;1-可能是;-1确认是
        """
        pass

    @abstractmethod
    def parser_metadata(self):
        """
        对目标目录或文件的元数据进行提取
        :return: 返回三个结果
        .[0]: 元数据的类型, 0-txt,1-json,2-xml
        .[1]: 元数据的返回格式: 0-文本,1-文件
        .[2]: 元数据的存储名称: 如果[1]=文本, 则[2]中直接返回元数据的内容; 如果[1]=文件, 则[2]中直接返回元数据内容存储的文件名
        """
        pass

    @abstractmethod
    def parser_bus_metadata(self):
        """
        对目标目录或文件的业务元数据进行提取
        :return: 返回三个结果
        .[0]: 元数据的类型, 0-txt,1-json,2-xml
        .[1]: 元数据的返回格式: 0-文本,1-文件
        .[2]: 元数据的存储名称: 如果[1]=文本, 则[2]中直接返回元数据的内容; 如果[1]=文件, 则[2]中直接返回元数据内容存储的文件名
        """
        pass

    @abstractmethod
    def parser_spatial_metadata(self) -> str:
        """
        对目标目录或文件的空间信息进行提取
        :return:
        """
        pass

    @abstractmethod
    def parser_tags_metadata(self) -> list:
        """
        对目标目录或文件的元数据进行提取
        :return:
        """
        pass

    @abstractmethod
    def parser_time_metadata(self) -> str:
        """
        对目标目录或文件的元数据进行提取
        :return:
        """
        pass
