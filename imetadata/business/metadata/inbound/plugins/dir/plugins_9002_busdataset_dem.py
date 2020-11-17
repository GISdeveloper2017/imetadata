# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:48 
# @Author : 王西亚 
# @File : plugins_9002_busdataset_dem.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9002_busdataset_dem(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-DEM'
        information[self.Plugins_Info_Name] = 'DEM'
        # information[self.Plugins_Info_Type] = 'business_data_set_dem'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_DEM
        information[self.Plugins_Info_Code] = '020106'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset
        return information
