# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 10:40 
# @Author : 王西亚 
# @File : c_zip.py

from imetadata.base.c_file import CFile
from imetadata.base.zip.c_zip_base import CZipBase
from imetadata.base.zip.c_zip_tarfile import CZip_TarFile
from imetadata.base.zip.c_zip_zipfile import CZip_ZipFile


class CZip:
    """
    压缩包处理
    """
    __file_name__: None
    __zip_obj__: CZipBase = None

    def __init__(self, file_name_with_path):
        self.__file_name__ = file_name_with_path

    def open(self):
        if CZip_ZipFile.i_can_read(self.__file_name__):
            self.__zip_obj__ = CZip_ZipFile(self.__file_name__)
            self.__zip_obj__.open()
        elif CZip_TarFile.i_can_read(self.__file_name__):
            self.__zip_obj__ = CZip_TarFile(self.__file_name__)
            self.__zip_obj__.open()
        else:
            raise Exception('系统不支持解析压缩文件{0}'.format(self.__file_name__))

    def file_names(self):
        return self.__zip_obj__.file_names()

    def extract_file(self, file_name, target_path):
        CFile.check_and_create_directory(target_path)
        self.__zip_obj__.extract_file(file_name, target_path)

    def extract_all(self, target_path):
        CFile.check_and_create_directory(target_path)
        self.__zip_obj__.extract_all(target_path)

    def close(self):
        if self.__zip_obj__ is not None:
            self.__zip_obj__.close()