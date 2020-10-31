# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 10:40 
# @Author : 王西亚 
# @File : c_zip.py
from imetadata.base.c_file import CFile
from imetadata.base.exceptions import ZipFileCanNotOpenException
from imetadata.base.zip.c_zip_base import CZipBase
from imetadata.base.zip.c_zip_tarfile import CZip_TarFile
from imetadata.base.zip.c_zip_zipfile import CZip_ZipFile


class CZip:
    """
    压缩包处理
    """
    __file_name: None
    __zip_obj: CZipBase = None

    def __init__(self, file_name_with_path):
        self.__file_name = file_name_with_path

    def open(self):
        if CZip_ZipFile.i_can_read(self.__file_name):
            self.__zip_obj = CZip_ZipFile(self.__file_name)
            self.__zip_obj.open()
        elif CZip_TarFile.i_can_read(self.__file_name):
            self.__zip_obj = CZip_TarFile(self.__file_name)
            self.__zip_obj.open()
        else:
            raise ZipFileCanNotOpenException(self.__file_name)

    def file_names(self):
        return self.__zip_obj.file_names()

    def extract_file(self, file_name, target_path):
        CFile.check_and_create_directory(target_path)
        self.__zip_obj.extract_file(file_name, target_path)

    def extract_all(self, target_path):
        CFile.check_and_create_directory_itself(target_path)
        self.__zip_obj.extract_all(target_path)

    def close(self):
        if self.__zip_obj is not None:
            self.__zip_obj.close()


if __name__ == '__main__':
    zip_obj = CZip('/Users/wangxiya/Documents/交换/1.给我的/数据入库3/卫星数据/压缩包/内网通截图20200916172248.tar.gz')
    try:
        zip_obj.open()
        zip_obj.extract_all('/Users/wangxiya/Documents/交换/test')
    finally:
        zip_obj.close()
