# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:40 
# @Author : 王西亚 
# @File : c_rasterFilePlugins.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
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
        information[self.Plugins_Info_Group_Name] = self.DataGroup_Raster
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group_Name])
        return information

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        完成 负责人 赵宇飞 在这里检验设定影像的质检列表
        """
        return self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path)  # 调用默认的规则列表
        # return list_qa
