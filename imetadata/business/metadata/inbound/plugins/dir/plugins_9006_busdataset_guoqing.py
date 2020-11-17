# -*- coding: utf-8 -*- 
# @Time : 2020/11/05 17:10
# @Author : 赵宇飞
# @File : plugins_9006_busdataset_guoqing.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9006_busdataset_guoqing(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-国情影像'
        information[self.Plugins_Info_Name] = '国情影像'
        # information[self.Plugins_Info_Type] = 'business_data_set_guoqing'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_Guoqing
        information[self.Plugins_Info_Code] = '020103'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset
        return information