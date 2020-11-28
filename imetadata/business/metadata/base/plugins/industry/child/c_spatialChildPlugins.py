# -*- coding: utf-8 -*- 
# @Time : 2020/11/26 15:04 
# @Author : 王西亚 
# @File : c_spatialChildPlugins.py
from imetadata.business.metadata.base.plugins.c_childPlugins import CChildPlugins


class CSpatialChildPlugins(CChildPlugins):
    """
    空间数据的子对象插件
    . 直接从父对象的元数据中直接获取元数据信息
    """

    def get_information(self) -> dict:
        information = super().get_information()
        information[self.Plugins_Info_Type] = 'layer'
        information[self.Plugins_Info_Type_Title] = '数据集图层'
        return information
