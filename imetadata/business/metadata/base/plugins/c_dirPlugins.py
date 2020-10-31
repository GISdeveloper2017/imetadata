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
        if self.file_info is not None:
            self._file_content = CVirtualContentDir(self.file_info.file_name_with_full_path)
