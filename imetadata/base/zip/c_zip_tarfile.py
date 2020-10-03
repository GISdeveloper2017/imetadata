# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 11:08 
# @Author : 王西亚 
# @File : c_zip_tarfile.py

import tarfile

from imetadata.base.c_file import CFile
from imetadata.base.zip.c_zip_base import CZipBase


class CZip_TarFile(CZipBase):
    """
    Tar压缩包处理
    """
    __zip_obj__ = None

    def __init__(self, file_name_with_path):
        super().__init__(file_name_with_path)
        self.__file_name__ = file_name_with_path

    def open(self):
        self.__zip_obj__ = tarfile.open(self.__file_name__, "r:gz")

    def file_names(self):
        file_list = list()
        for tarinfo in self.__zip_obj__:
            file_list.append(tarinfo.name)
        return file_list

    def extract_file(self, file_name, target_path):
        CFile.check_and_create_directory(target_path)
        self.__zip_obj__.extract(file_name, path=target_path)

    def extract_all(self, target_path):
        CFile.check_and_create_directory(target_path)
        self.__zip_obj__.extractall(target_path)

    def close(self):
        if self.__zip_obj__ is not None:
            self.__zip_obj__.close()

    @classmethod
    def i_can_read(cls, file_name):
        return tarfile.is_tarfile(file_name)
