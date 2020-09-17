# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:00 
# @Author : 王西亚 
# @File : c_fileInfo.py
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource


class CFileInfo(CResource):
    __file_name_with_full_path__: str

    __file_name_without_path__: str

    __file_main_name__: str
    __file_ext__: str
    __file_path__: str

    __file_type__: str
    __file_existed__: bool

    __file_size__: int = 0
    __file_attr__: int = 32
    __file_create_time__ = None
    __file_access_time__ = None
    __file_modify_time__ = None

    def __init__(self, file_name_with_full_path):
        self.__file_name_with_full_path__ = file_name_with_full_path

        self.__file_name_without_path__ = CFile.file_name(self.__file_name_with_full_path__)
        self.__file_main_name__ = CFile.file_main_name(self.__file_name_with_full_path__)
        self.__file_ext__ = CFile.file_ext(self.__file_name_with_full_path__)
        self.__file_path__ = CFile.file_path(self.__file_name_with_full_path__)

        self.__file_type__ = self.FileType_Unknown
        self.__file_existed__ = CFile.file_or_path_exist(self.__file_name_with_full_path__)
        if self.__file_existed__:
            if CFile.is_file(self.__file_name_with_full_path__):
                self.__file_type__ = self.FileType_File
                self.__file_size__ = CFile.file_size(self.__file_name_with_full_path__)
            else:
                self.__file_type__ = self.FileType_Path

            self.__file_create_time__ = CFile.file_create_time(self.__file_name_with_full_path__)
            self.__file_access_time__ = CFile.file_access_time(self.__file_name_with_full_path__)
            self.__file_modify_time__ = CFile.file_modify_time(self.__file_name_with_full_path__)
