# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 11:17 
# @Author : 王西亚 
# @File : c_zip_base.py
from abc import abstractmethod


class CZipBase:
    """
    压缩包处理
    """
    __file_name__: None

    def __init__(self, file_name_with_path):
        self.__file_name__ = file_name_with_path

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def file_names(self):
        pass

    @abstractmethod
    def extract_file(self, file_name, target_path):
        pass

    @abstractmethod
    def extract_all(self, target_path):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def new(self, flag):
        pass

    @abstractmethod
    def add_file_or_path(self, file:dict):
        pass
