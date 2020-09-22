# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 11:08 
# @Author : 王西亚 
# @File : c_zip_tarfile.py

import zipfile
from imetadata.base.c_file import CFile
from imetadata.base.zip.c_zip_base import CZipBase


class CZip_ZipFile(CZipBase):
    """
    压缩包处理
    """

    __zip_obj__ = None

    def __init__(self, file_name_with_path):
        super().__init__(file_name_with_path)
        self.__file_name__ = file_name_with_path

    def open(self):
        self.__zip_obj__ = zipfile.ZipFile(self.__file_name__)

    def file_names(self):
        file_list = list()
        zip_file_list = self.__zip_obj__.infolist()
        for info in zip_file_list:
            file_list.append(info.filename)
        return file_list

    def extract_file(self, filename, targetpath):
        CFile.check_and_create_directory(targetpath)
        self.__zip_obj__.extract(filename, targetpath)

    def extract_all(self, targetpath):
        CFile.check_and_create_directory(targetpath)
        self.__zip_obj__.extractall(targetpath)

    def close(self):
        if self.__zip_obj__ is not None:
            self.__zip_obj__.close()

    @classmethod
    def i_can_read(cls, filename):
        return zipfile.is_zipfile(filename)
