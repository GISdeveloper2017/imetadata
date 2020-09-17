# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_1000_xzqh.py


from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.c_pathPlugins import CPathPlugins


class plugins_1000_xzqh(CPathPlugins):

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        self.__object_name__ = None
        if CFile.file_match(self.__target_file_or_path_name__.lower(), '*行政区划*'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = self.__target_file_or_path_name__
        return self.__object_confirm__, self.__object_name__

    def parser_metadata(self):
        pass

    def parser_bus_metadata(self):
        pass

    def parser_spatial_metadata(self) -> str:
        pass

    def parser_tags_metadata(self) -> list:
        pass

    def parser_time_metadata(self) -> str:
        pass