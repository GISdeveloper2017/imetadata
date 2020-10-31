# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:00
# @Author : 王西亚
# @File : c_fileInfo.py
from imetadata.base.c_file import CFile
from imetadata.base.c_resource import CResource


class CFileInfo(CResource):
    __file_name_with_full_path: str

    __file_name_without_path: str

    __file_main_name: str
    __file_main_name_with_full_path: str

    __file_ext: str
    __file_path: str

    __file_type: str
    __file_existed: bool

    __file_size: int = 0
    __file_create_time = None
    __file_access_time = None
    __file_modify_time = None

    @property
    def file_name_with_full_path(self):
        return self.__file_name_with_full_path

    @property
    def file_name_without_path(self):
        return self.__file_name_without_path

    @property
    def file_main_name(self):
        return self.__file_main_name

    @property
    def file_main_name_with_full_path(self):
        return self.__file_main_name_with_full_path

    @property
    def file_ext(self):
        return self.__file_ext

    @property
    def file_path(self):
        return self.__file_path

    @property
    def file_type(self):
        return self.__file_type

    @property
    def file_existed(self):
        return self.__file_existed

    @property
    def file_size(self):
        return self.__file_size

    @property
    def file_create_time(self):
        return self.__file_create_time

    @property
    def file_access_time(self):
        return self.__file_access_time

    @property
    def file_modify_time(self):
        return self.__file_modify_time

    def __init__(self, file_type, file_name_with_full_path):
        self.__file_name_with_full_path = file_name_with_full_path

        self.__file_name_without_path = CFile.file_name(self.file_name_with_full_path)
        self.__file_main_name = CFile.file_main_name(self.file_name_with_full_path)
        self.__file_ext = CFile.file_ext(self.file_name_with_full_path)
        self.__file_path = CFile.file_path(self.file_name_with_full_path)

        self.__file_main_name_with_full_path = CFile.join_file(self.file_path, self.file_main_name)

        self.__file_type = file_type
        self.__file_existed = CFile.file_or_path_exist(self.file_name_with_full_path)
        if self.__file_existed:
            if CFile.is_file(self.file_name_with_full_path):
                self.__file_size = CFile.file_size(self.file_name_with_full_path)

            self.__file_create_time = CFile.file_create_time(self.file_name_with_full_path)
            self.__file_access_time = CFile.file_access_time(self.file_name_with_full_path)
            self.__file_modify_time = CFile.file_modify_time(self.file_name_with_full_path)
