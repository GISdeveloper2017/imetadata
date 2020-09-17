# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:52 
# @Author : 王西亚 
# @File : c_pathPlugins.py

from imetadata.business.metadata.base.plugins.c_plugins import CPlugins


class CPathPlugins(CPlugins):
    def get_group_name(self) -> str:
        return self.FileType_Dir
