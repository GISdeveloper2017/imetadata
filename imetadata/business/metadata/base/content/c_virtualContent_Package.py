# -*- coding: utf-8 -*- 
# @Time : 2020/9/21 18:03 
# @Author : 王西亚 
# @File : c_virtualContent_File.py
from imetadata.base.c_file import CFile
from imetadata.base.c_sys import CSys
from imetadata.base.c_utils import CMetaDataUtils
from imetadata.business.metadata.base.content.c_virtualContent import CVirtualContent


class CVirtualContentPackage(CVirtualContent):
    __temp_unpackage_path__: str
    __temp_unpackage_subpath_name__: str
    """
    虚拟内容目录
    . 在读取普通文件数据时, 虚拟内容目录是文件所在的子目录
    . 在读取普通子目录数据时, 虚拟内容目录是子目录本身
    . 在读取压缩数据时, 虚拟目录时压缩包解压的临时子目录
    """
    def create_virtual_content(self) -> str:
        """

        todo 在这里将数据解压缩至临时目录下
        :return:
        """
        self.__temp_unpackage_subpath_name__ = CMetaDataUtils.one_id()
        self.__temp_unpackage_path__ = CFile.join_file(CSys.get_work_root_dir(), self.__temp_unpackage_subpath_name__)

        return self.__temp_unpackage_path__

    def destroy_virtual_content(self):
        CFile.remove_dir(self.__temp_unpackage_path__)
