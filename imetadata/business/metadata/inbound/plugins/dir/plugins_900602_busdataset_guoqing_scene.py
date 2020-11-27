# -*- coding: utf-8 -*- 
# @Time : 2020/11/16 11:21
# @Author : 赵宇飞
# @File : plugins_900602_busdataset_guoqing_scene.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_900602_busdataset_guoqing_scene(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = '业务数据集-国情影像_整景纠正'
        information[self.Plugins_Info_Name] = '国情影像_整景纠正'
        # information[self.Plugins_Info_Type] = 'business_data_set_guoqing_scene'
        information[self.Plugins_Info_Type] = self.Object_Def_Type_DataSet_Guoqing_Scene
        information[self.Plugins_Info_Code] = '02010302'
        information[self.Plugins_Info_Catalog] = self.Object_Def_Catalog_Dataset_Business
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_guoqing'
        return information