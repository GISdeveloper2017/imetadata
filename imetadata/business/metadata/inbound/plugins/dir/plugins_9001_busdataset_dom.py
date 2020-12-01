# -*- coding: utf-8 -*- 
# @Time : 2020/9/19 17:35 
# @Author : 王西亚 
# @File : plugins_9001_busdataset_dom.py

from imetadata.business.metadata.base.plugins.c_21ATBusDataSetPlugins import C21ATBusDataSetPlugins


class plugins_9001_busdataset_dom(C21ATBusDataSetPlugins):
    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Title] = 'DOM数据集'
        information[self.Plugins_Info_Code] = '020105'
        information[self.Plugins_Info_Module_Distribute_Engine] = 'distribution_dataset_dom'
        return information
