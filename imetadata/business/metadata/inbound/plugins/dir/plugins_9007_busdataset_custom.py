# -*- coding: utf-8 -*- 
# @Time : 2020/11/05 17:10
# @Author : 赵宇飞
# @File : plugins_9007_busdataset_custom.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9007_busdataset_custom(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-自定义影像'
        information[self.Plugins_Info_Name] = '自定义影像'
        # information[self.Plugins_Info_Type] = 'business_data_set_custom'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_Custom
        information[self.Plugins_Info_Code] = '020107'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset_Business
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_custom'
        return information
