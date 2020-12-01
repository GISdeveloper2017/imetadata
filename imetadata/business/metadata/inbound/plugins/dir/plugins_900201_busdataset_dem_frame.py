# -*- coding: utf-8 -*- 
# @Time : 2020/11/16 11:28
# @Author : 赵宇飞
# @File : plugins_900201_busdataset_dem_frame.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_900201_busdataset_dem_frame(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-DEM_分幅'
        information[self.Plugins_Info_Name] = 'DEM_分幅'
        # information[self.Plugins_Info_Type] = 'business_data_set_dem_frame'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_DEM_Frame
        information[self.Plugins_Info_Code] = '02010601'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset_Business
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_dem'
        return information
