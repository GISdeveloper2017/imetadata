# -*- coding: utf-8 -*- 
# @Time : 2020/11/16 11:29
# @Author : 赵宇飞
# @File : plugins_900202_busdataset_dem_noframe.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_900202_busdataset_dem_noframe(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-DEM_非分幅'
        information[self.Plugins_Info_Name] = 'DEM_非分幅'
        information[self.Plugins_Info_Type] = 'business_data_set_dem_noframe'
        information[self.Plugins_Info_Code] = '02010602'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset
        return information