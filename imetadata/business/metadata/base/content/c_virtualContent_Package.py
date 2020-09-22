# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 18:03 
# @Author : 王西亚 
# @File : c_virtualContent_File.py
from imetadata.base.c_file import CFile
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CUtils
from imetadata.base.c_zip import CZip
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent


class CVirtualContentPackage(CVirtualContent):
    __temp_package_subpath_name__: str

    """
    虚拟内容目录
    . 在读取普通文件数据时, 虚拟内容目录是文件所在的子目录
    . 在读取普通子目录数据时, 虚拟内容目录是子目录本身
    . 在读取压缩数据时, 虚拟目录时压缩包解压的临时子目录
    """

    def create_virtual_content(self) -> str:
        """

        :return:
        """
        self.__temp_package_subpath_name__ = CUtils.one_id()
        self.__virtual_content_root_dir__ = CFile.join_file(CSys.get_work_root_dir(),
                                                            self.__temp_package_subpath_name__)
        zip_obj = CZip(self.__target_name__)
        zip_obj.open()
        try:
            zip_obj.extract_all(self.__virtual_content_root_dir__)
        finally:
            zip.close()

        return self.__virtual_content_root_dir__

    def destroy_virtual_content(self):
        CFile.remove_dir(self.__virtual_content_root_dir__)


if __name__ == '__main__':
    file_name1 = r'/Users/wangxiya/Documents/交换/1.给我的/GF1/GF1_PMS1_E65.2_N26.6_20130927_L1A0000090284.tar.gz'
    file_name = r'/Users/wangxiya/Documents/交换/test.zip'
    target_path = r'/Users/wangxiya/Documents/交换/1.给我的/GF1/GF1_PMS1_E65.2_N26.6_20130927_L1A0000090284'
    zip = CZip(file_name)
    zip.open()
    file_list = zip.file_names()
    for file_name in file_list:
        print(file_name)
    zip.extract_all(target_path)
    zip.close()
