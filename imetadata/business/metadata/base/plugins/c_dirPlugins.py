# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:52 
# @Author : 王西亚 
# @File : c_dirPlugins.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.content.c_virtualContent_Dir import CVirtualContentDir
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CDirPlugins(CPlugins):
    """
    常规目录识别插件
    """

    def __init__(self, file_info: CFileInfoEx):
        super().__init__(file_info)
        if self.__file_info__ is not None:
            self.__file_content__ = CVirtualContentDir(self.__file_info__.__file_name_with_full_path__)
