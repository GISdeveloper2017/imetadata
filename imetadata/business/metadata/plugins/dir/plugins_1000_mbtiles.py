# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_1000_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.c_dirPlugins import CDirPlugins


class plugins_1000_mbtiles(CDirPlugins):

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        self.__object_name__ = None

        current_path = self.__file_info__.__file_name_with_full_path__
        if CFile.find_file_or_subpath_of_path(current_path, '*_0.mbtiles') \
                and CFile.find_file_or_subpath_of_path(current_path, '*.xml'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = self.__file_info__.__file_main_name__
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
