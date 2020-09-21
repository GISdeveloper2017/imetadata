# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 18:24 
# @Author : 王西亚 
# @File : c_satPlugins.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.content.c_virtualContent_Dir import CVirtualContentDir
from imetadata.business.metadata.base.content.c_virtualContent_Package import CVirtualContentPackage
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CSatPlugins(CPlugins):
    """
    在这个类中解决卫星压缩数据包解压至目录中, 再进行检查
    """
    def __init__(self, file_info: CFileInfoEx):
        super().__init__(file_info)
        if self.__file_info__.__file_type__ == self.FileType_Dir:
            self.__file_content__ = CVirtualContentDir(self.__file_info__.__file_name_with_full_path__)
        else:
            self.__file_content__ = CVirtualContentPackage(self.__file_info__.__file_name_with_full_path__)

