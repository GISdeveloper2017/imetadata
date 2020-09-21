# -*- coding: utf-8 -*- 
# @Time : 2020/9/17 16:51 
# @Author : 王西亚 
# @File : plugins_1000_mbtiles.py


from imetadata.base.c_file import CFile
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class plugins_1000_mbtiles(CFilePlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '二十一世纪公司切片'
        information[self.Plugins_Info_Name] = '21at_mbtiles'
        information[self.Plugins_Info_Code] = None
        information[self.Plugins_Info_Catalog] = '切片'
        information[self.Plugins_Info_Type] = 'tiles'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_21AT_MBTiles
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        information[self.Plugins_Info_QCEngine] = None
        return information

    def classified(self):
        self.__object_confirm__ = self.Object_Confirm_IUnKnown
        self.__object_name__ = None

        current_path = self.__file_info__.__file_name_with_full_path__
        if CFile.find_file_or_subpath_of_path(current_path, '*_0.mbtiles') \
                and CFile.find_file_or_subpath_of_path(current_path, '*.xml'):
            self.__object_confirm__ = self.Object_Confirm_IKnown
            self.__object_name__ = self.__file_info__.__file_main_name__
        return self.__object_confirm__, self.__object_name__
