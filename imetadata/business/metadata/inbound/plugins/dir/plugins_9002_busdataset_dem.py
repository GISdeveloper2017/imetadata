# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:48 
# @Author : 王西亚 
# @File : plugins_9002_busdataset_dem.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9002_busdataset_dem(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'DEM'
        information[self.Plugins_Info_Type_Title] = 'DEM数据集'
        information[self.Plugins_Info_Type_Code] = '020106'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_dem'
        return information
