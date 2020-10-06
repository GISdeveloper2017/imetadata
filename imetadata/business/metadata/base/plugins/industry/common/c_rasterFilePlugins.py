# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:40 
# @Author : 王西亚 
# @File : c_rasterFilePlugins.py

from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class CRasterFilePlugins(CFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '影像'
        information[self.Plugins_Info_Code] = None
        information[self.Plugins_Info_Catalog] = '影像'
        information[self.Plugins_Info_Type] = 'raster'
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Raster
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        return information
