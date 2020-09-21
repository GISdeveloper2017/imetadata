# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:35 
# @Author : 王西亚 
# @File : plugins_9001_busdataset_dom.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9001_busdataset_dom(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-DOM'
        information[self.Plugins_Info_Name] = 'DOM'
        information[self.Plugins_Info_Code] = '110001'
        information[self.Plugins_Info_Catalog] = '业务数据集'
        information[self.Plugins_Info_Type] = 'business_data_set'
        information[self.Plugins_Info_MetaDataEngine] = None
        information[self.Plugins_Info_BusMetaDataEngine] = None
        information[self.Plugins_Info_TagsEngine] = self.TagEngine_Global_Dim_In_MainName
        information[self.Plugins_Info_DetailEngine] = None
        information[self.Plugins_Info_QCEngine] = None

        return information
