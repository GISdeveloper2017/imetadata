# -*- coding: utf-8 -*- 
# @Time : 2020/9/15 09:54 
# @Author : 王西亚 
# @File : plugins_6002_gf1_pms.py.py

from imetadata.base.c_file import CFile
from imetadata.business.base.c_satPlugins import CSatPlugins


class plugins_6002_gf1_pms(CSatPlugins):
    def get_id(self) -> str:
        return 'gf1-pms'

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        self.__object_name__ = None
        if CFile.file_match(self.__target_file_or_path_name__.lower(), 'gf1-pms*'):
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