# -*- coding: utf-8 -*- 
# @Time : 2020/11/16 11:23
# @Author : 赵宇飞
# @File : plugins_900601_busdataset_guoqing_frame.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins

class plugins_900601_busdataset_guoqing_frame(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-国情影像_分幅'
        information[self.Plugins_Info_Name] = '国情影像_分幅'
        # information[self.Plugins_Info_Type] = 'business_data_set_guoqing_frame'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_Guoqing_Frame
        information[self.Plugins_Info_Code] = '02010301'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset
        return information