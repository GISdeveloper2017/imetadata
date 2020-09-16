# -*- coding: utf-8 -*- 
# @Time : 2020/9/16 09:04 
# @Author : 王西亚 
# @File : c_mdreader.py
from abc import abstractmethod
from imetadata.base.c_resource import CResource


class CMDReader(CResource):
    """
    栅格数据文件的元数据读取器
    """
    __file_name_with_path__: str

    def __init__(self, file_name_with_path: str):
        self.__file_name_with_path__ = file_name_with_path

    @abstractmethod
    def get_metadata_2_file(self, file_name_with_path: str):
        pass
