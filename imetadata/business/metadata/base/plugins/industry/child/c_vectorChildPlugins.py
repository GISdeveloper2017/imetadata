# -*- coding: utf-8 -*- 
# @Time : 2020/11/26 15:06 
# @Author : 王西亚 
# @File : c_vectorChildPlugins.py
from imetadata.business.metadata.base.plugins.industry.child.c_spatialChildPlugins import CSpatialChildPlugins


class CVectorChildPlugins(CSpatialChildPlugins):

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Name] = 'vector_layer'
        information[self.Plugins_Info_Title] = '矢量数据集图层'
        return information
