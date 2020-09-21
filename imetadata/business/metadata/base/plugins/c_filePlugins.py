# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:50 
# @Author : 王西亚 
# @File : c_filePlugins.py
from imetadata.base.c_fileInfoEx import CFileInfoEx
from imetadata.business.metadata.base.content.c_virtualContent_File import CVirtualContentFile
from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CFilePlugins(CPlugins):
    """
    常规文件识别插件
    """
    def __init__(self, file_info: CFileInfoEx):
        super().__init__(file_info)
        self.__file_content__ = CVirtualContentFile(self.__file_info__.__file_name_with_full_path__)
