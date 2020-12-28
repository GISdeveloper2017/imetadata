# -*- coding: utf-8 -*- 
# @Time : 2020/11/05 17:08
# @Author : 赵宇飞
# @File : lugins_3003_busdataset_shp.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9010_busdataset_shp(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'shp'
        information[self.Plugins_Info_Type_Title] = 'SHP数据集'
        information[self.Plugins_Info_Type_Code] = '020201'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_shp'
        return information
