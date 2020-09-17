# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 09:11 
# @Author : 王西亚 
# @File : c_fileInfoEx.py

from imetadata.base.c_file import CFile
from imetadata.base.c_fileInfo import CFileInfo


class CFileInfoEx(CFileInfo):
    __file_name_with_rel_path__: str
    __file_path_with_rel_path__: str

    __root_path__ = str

    def __init__(self, file_name_with_full_path, root_path):
        super().__init__(file_name_with_full_path)
        self.__root_path__ = root_path

        self.__file_name_with_rel_path__ = CFile.file_relation_path(self.__file_name_with_full_path__, self.__root_path__)
        self.__file_path_with_rel_path__ = CFile.file_relation_path(self.__file_path__, self.__root_path__)
