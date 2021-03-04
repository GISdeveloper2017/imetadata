# -*- coding: utf-8 -*- 
# @Time : 2020/9/22 15:40 
# @Author : 王西亚 
# @File : c_vectorFilePlugins.py
from imetadata.business.metadata.base.parser.metadata.c_metaDataParser import CMetaDataParser
from imetadata.business.metadata.base.plugins.c_filePlugins import CFilePlugins


class CVectorFilePlugins(CFilePlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = '矢量'
        information[self.Plugins_Info_Type_Code] = None
        information[self.Plugins_Info_Group] = self.DataGroup_Vector
        information[self.Plugins_Info_Group_Title] = self.data_group_title(information[self.Plugins_Info_Group])
        information[self.Plugins_Info_Catalog] = self.DataCatalog_Common
        information[self.Plugins_Info_Catalog_Title] = self.data_catalog_title(information[self.Plugins_Info_Catalog])
        information[self.Plugins_Info_MetaDataEngine] = self.MetaDataEngine_Vector
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_DetailEngine] = self.DetailEngine_All_File_Of_Dir
        information[self.Plugins_Info_SpatialEngine] = self.MetaDataEngine_Vector  # 通用的矢量数据的空间引擎（解析自身元数据json用的）

        information[self.Plugins_Info_Is_Spatial] = self.DB_True
        information[self.Plugins_Info_Is_Dataset] = self.DB_False
        information[self.Plugins_Info_Spatial_Qa] = self.DB_True
        information[self.Plugins_Info_Time_Qa] = self.DB_True
        information[self.Plugins_Info_Visual_Qa] = self.DB_False
        return information

    def init_qa_file_list(self, parser: CMetaDataParser) -> list:
        """
        完成 负责人 赵宇飞 在这里检验设定矢量文件的完整性
        """
        return self.init_qa_file_integrity_default_list(self.file_info.file_name_with_full_path)  # 调用默认的规则列表
        # return list_qa
